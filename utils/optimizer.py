"""
Workforce scheduling optimization using OR-Tools.
Implements constraint programming to minimize labor costs while meeting demand.
"""

import pandas as pd
import numpy as np
from ortools.sat.python import cp_model
from typing import Dict, List, Tuple, Optional
import streamlit as st

class WorkforceOptimizer:
    """Optimizer for workforce scheduling with cost minimization objective."""
    
    def __init__(self, availability_df: pd.DataFrame, demand_df: pd.DataFrame):
        self.availability_df = availability_df
        self.demand_df = demand_df
        self.model = None
        self.variables = {}
        self.solution = None
        
    def prepare_data(self) -> Dict:
        """Prepare data for optimization."""
        
        # Get unique dates and employees
        dates = sorted(self.availability_df['Date'].unique())
        employees = self.availability_df['EmployeeID'].unique()
        
        # Create demand lookup
        demand_lookup = dict(zip(self.demand_df['Date'], self.demand_df['ForecastedDemand']))
        
        # Create availability matrix
        availability_matrix = {}
        wage_matrix = {}
        role_matrix = {}
        
        for _, row in self.availability_df.iterrows():
            key = (row['Date'], row['EmployeeID'])
            availability_matrix[key] = row['HoursAvailable']
            wage_matrix[key] = row['HourlyWage']
            role_matrix[key] = row['Role']
        
        return {
            'dates': dates,
            'employees': employees,
            'demand_lookup': demand_lookup,
            'availability_matrix': availability_matrix,
            'wage_matrix': wage_matrix,
            'role_matrix': role_matrix
        }
    
    def build_model(self, data: Dict) -> cp_model.CpModel:
        """Build the constraint programming model."""
        
        model = cp_model.CpModel()
        
        dates = data['dates']
        employees = data['employees']
        demand_lookup = data['demand_lookup']
        availability_matrix = data['availability_matrix']
        wage_matrix = data['wage_matrix']
        role_matrix = data['role_matrix']
        
        # Decision variables: x[date, employee] = hours worked
        variables = {}
        for date in dates:
            for employee in employees:
                key = (date, employee)
                if key in availability_matrix and availability_matrix[key] > 0:
                    max_hours = availability_matrix[key]
                    variables[key] = model.NewIntVar(0, max_hours, f'hours_{date}_{employee}')
        
        # Objective: minimize total labor cost
        total_cost = []
        for (date, employee), var in variables.items():
            wage = wage_matrix[(date, employee)]
            total_cost.append(var * wage)
        
        model.Minimize(sum(total_cost))
        
        # Constraints
        
        # 1. Meet demand constraint (simplified: assume 1 hour of work covers 10 customers)
        for date in dates:
            demand = demand_lookup.get(date, 0)
            required_hours = max(1, demand // 10)  # At least 1 hour, then 1 hour per 10 customers
            
            available_employees = [var for (d, emp), var in variables.items() if d == date]
            if available_employees:
                model.Add(sum(available_employees) >= required_hours)
        
        # 2. Supervisor constraint: at least one supervisor per day
        for date in dates:
            supervisor_vars = []
            for employee in employees:
                key = (date, employee)
                if key in variables and role_matrix.get(key) == 'supervisor':
                    supervisor_vars.append(variables[key])
            
            if supervisor_vars:
                # At least one supervisor must work at least 4 hours
                supervisor_working = []
                for var in supervisor_vars:
                    working = model.NewBoolVar(f'supervisor_working_{date}_{var}')
                    model.Add(var >= 4).OnlyEnforceIf(working)
                    model.Add(var == 0).OnlyEnforceIf(working.Not())
                    supervisor_working.append(working)
                
                model.Add(sum(supervisor_working) >= 1)
        
        # 3. Weekly hours constraint
        for employee in employees:
            # Get employee's max weekly hours
            emp_data = self.availability_df[self.availability_df['EmployeeID'] == employee].iloc[0]
            max_weekly_hours = emp_data['MaxWeeklyHours']
            
            # Group dates by week
            weekly_hours = {}
            for date in dates:
                week_start = date - pd.Timedelta(days=date.weekday())
                if week_start not in weekly_hours:
                    weekly_hours[week_start] = []
                
                key = (date, employee)
                if key in variables:
                    weekly_hours[week_start].append(variables[key])
            
            # Add weekly constraint for each week
            for week_start, week_vars in weekly_hours.items():
                if week_vars:
                    model.Add(sum(week_vars) <= max_weekly_hours)
        
        # 4. Availability constraint (already handled by variable bounds)
        
        self.variables = variables
        return model
    
    def solve(self, time_limit_seconds: int = 30) -> Dict:
        """Solve the optimization problem."""
        
        data = self.prepare_data()
        model = self.build_model(data)
        
        # Create solver
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit_seconds
        
        # Solve
        status = solver.Solve(model)
        
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            # Extract solution
            solution = {}
            total_cost = 0
            
            for (date, employee), var in self.variables.items():
                hours_worked = solver.Value(var)
                if hours_worked > 0:
                    wage = data['wage_matrix'][(date, employee)]
                    cost = hours_worked * wage
                    total_cost += cost
                    
                    solution[(date, employee)] = {
                        'hours_worked': hours_worked,
                        'wage': wage,
                        'cost': cost,
                        'role': data['role_matrix'][(date, employee)]
                    }
            
            return {
                'status': 'optimal' if status == cp_model.OPTIMAL else 'feasible',
                'solution': solution,
                'total_cost': total_cost,
                'solver_time': solver.WallTime()
            }
        else:
            return {
                'status': 'infeasible',
                'solution': {},
                'total_cost': 0,
                'solver_time': solver.WallTime()
            }
    
    def get_schedule_dataframe(self, solution: Dict) -> pd.DataFrame:
        """Convert solution to a pandas DataFrame for display."""
        
        if not solution:
            return pd.DataFrame()
        
        records = []
        for (date, employee), data in solution.items():
            records.append({
                'Date': date,
                'EmployeeID': employee,
                'HoursWorked': data['hours_worked'],
                'Wage': data['wage'],
                'Cost': data['cost'],
                'Role': data['role']
            })
        
        df = pd.DataFrame(records)
        if not df.empty:
            df = df.sort_values(['Date', 'EmployeeID'])
        
        return df
    
    def calculate_kpis(self, solution: Dict, original_data: Dict) -> Dict:
        """Calculate key performance indicators."""
        
        if not solution:
            return {}
        
        # Total cost
        total_cost = sum(data['cost'] for data in solution.values())
        
        # Total hours
        total_hours = sum(data['hours_worked'] for data in solution.values())
        
        # Overtime calculation (simplified)
        overtime_hours = 0
        for (date, employee), data in solution.items():
            if data['hours_worked'] > 8:  # Overtime if more than 8 hours
                overtime_hours += data['hours_worked'] - 8
        
        # Coverage calculation
        total_demand = sum(original_data['demand_lookup'].values())
        coverage_percentage = min(100, (total_hours * 10) / total_demand * 100)  # 1 hour covers 10 customers
        
        # Average staff per day
        dates = original_data['dates']
        avg_staff_per_day = len(solution) / len(dates) if dates else 0
        
        return {
            'total_cost': total_cost,
            'total_hours': total_hours,
            'overtime_hours': overtime_hours,
            'coverage_percentage': coverage_percentage,
            'avg_staff_per_day': avg_staff_per_day,
            'total_employees': len(set(emp for (_, emp) in solution.keys()))
        }

def optimize_workforce_schedule(availability_df: pd.DataFrame, demand_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict, Dict]:
    """
    Main function to optimize workforce schedule.
    
    Returns:
        - schedule_df: Optimized schedule as DataFrame
        - kpis: Key performance indicators
        - solution_info: Solution metadata
    """
    
    optimizer = WorkforceOptimizer(availability_df, demand_df)
    
    with st.spinner("Optimizing workforce schedule..."):
        solution_info = optimizer.solve(time_limit_seconds=30)
    
    if solution_info['status'] in ['optimal', 'feasible']:
        schedule_df = optimizer.get_schedule_dataframe(solution_info['solution'])
        data = optimizer.prepare_data()
        kpis = optimizer.calculate_kpis(solution_info['solution'], data)
        
        return schedule_df, kpis, solution_info
    else:
        st.error("Unable to find a feasible solution. Please check your constraints.")
        return pd.DataFrame(), {}, solution_info
