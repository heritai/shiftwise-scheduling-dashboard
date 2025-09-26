"""
Data preparation utilities for ShiftWise workforce scheduling.
Generates synthetic but realistic staff data for demonstration purposes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import List, Dict, Tuple

def generate_employee_data(num_employees: int = 25) -> pd.DataFrame:
    """Generate synthetic employee data with realistic patterns."""
    
    # Employee roles and their characteristics
    roles = {
        'cashier': {'base_wage': 15.0, 'max_hours': 40, 'skill_level': 1},
        'stock': {'base_wage': 16.0, 'max_hours': 40, 'skill_level': 2},
        'supervisor': {'base_wage': 22.0, 'max_hours': 45, 'skill_level': 3}
    }
    
    employees = []
    employee_id = 1
    
    # Generate employees for each role
    for role, config in roles.items():
        if role == 'supervisor':
            count = 5  # Fewer supervisors
        elif role == 'stock':
            count = 8
        else:
            count = 12  # More cashiers
        
        for _ in range(count):
            # Part-time vs full-time availability
            is_part_time = random.random() < 0.3 if role != 'supervisor' else False
            
            # Availability patterns
            if is_part_time:
                max_weekly_hours = random.randint(15, 25)
                preferred_days = random.sample(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
                                             random.randint(2, 4))
            else:
                max_weekly_hours = config['max_hours']
                preferred_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            
            # Weekend availability (some employees prefer weekends)
            weekend_preference = random.random() < 0.4
            
            employee = {
                'EmployeeID': f'EMP{employee_id:03d}',
                'Name': f'Employee {employee_id}',
                'Role': role,
                'HourlyWage': config['base_wage'] + random.uniform(-1.0, 2.0),
                'MaxWeeklyHours': max_weekly_hours,
                'PreferredDays': preferred_days,
                'WeekendPreference': weekend_preference,
                'SkillLevel': config['skill_level'],
                'IsPartTime': is_part_time
            }
            
            employees.append(employee)
            employee_id += 1
    
    return pd.DataFrame(employees)

def generate_demand_forecast(start_date: datetime, num_days: int = 90) -> pd.DataFrame:
    """Generate synthetic demand forecast with realistic patterns."""
    
    dates = []
    day_of_weeks = []
    forecasted_demands = []
    
    for i in range(num_days):
        current_date = start_date + timedelta(days=i)
        day_of_week = current_date.strftime('%A')
        
        # Base demand patterns
        base_demand = 100
        
        # Weekend effect (higher demand)
        if day_of_week in ['Saturday', 'Sunday']:
            weekend_multiplier = random.uniform(1.3, 1.8)
        else:
            weekend_multiplier = random.uniform(0.8, 1.2)
        
        # Seasonal variation (simulate some seasonality)
        seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * i / 365)
        
        # Random variation
        random_factor = random.uniform(0.8, 1.2)
        
        # Calculate final demand
        demand = int(base_demand * weekend_multiplier * seasonal_factor * random_factor)
        
        dates.append(current_date)
        day_of_weeks.append(day_of_week)
        forecasted_demands.append(demand)
    
    return pd.DataFrame({
        'Date': dates,
        'DayOfWeek': day_of_weeks,
        'ForecastedDemand': forecasted_demands
    })

def generate_availability_data(employees_df: pd.DataFrame, demand_df: pd.DataFrame) -> pd.DataFrame:
    """Generate daily availability data for each employee."""
    
    availability_records = []
    
    for _, employee in employees_df.iterrows():
        for _, day in demand_df.iterrows():
            date = day['Date']
            day_of_week = day['DayOfWeek']
            
            # Check if employee is available on this day
            is_available = day_of_week in employee['PreferredDays']
            
            # Weekend availability logic
            if day_of_week in ['Saturday', 'Sunday']:
                if not employee['WeekendPreference']:
                    is_available = random.random() < 0.3  # 30% chance even if not preferred
                else:
                    is_available = is_available and random.random() < 0.9  # 90% chance if preferred
            
            # Random absences (sick days, personal time)
            if is_available and random.random() < 0.05:  # 5% chance of absence
                is_available = False
            
            if is_available:
                # Determine hours available for this day
                if employee['IsPartTime']:
                    hours_available = random.choice([4, 6, 8])
                else:
                    hours_available = random.choice([6, 8, 10])
                
                # Supervisors might work longer shifts
                if employee['Role'] == 'supervisor':
                    hours_available = max(hours_available, 8)
            else:
                hours_available = 0
            
            availability_records.append({
                'Date': date,
                'DayOfWeek': day_of_week,
                'EmployeeID': employee['EmployeeID'],
                'Name': employee['Name'],
                'Role': employee['Role'],
                'HourlyWage': employee['HourlyWage'],
                'MaxWeeklyHours': employee['MaxWeeklyHours'],
                'HoursAvailable': hours_available,
                'IsAvailable': is_available
            })
    
    return pd.DataFrame(availability_records)

def create_sample_dataset() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Create the complete sample dataset for ShiftWise."""
    
    print("Generating employee data...")
    employees_df = generate_employee_data(25)
    
    print("Generating demand forecast...")
    start_date = datetime.now() - timedelta(days=90)
    demand_df = generate_demand_forecast(start_date, 90)
    
    print("Generating availability data...")
    availability_df = generate_availability_data(employees_df, demand_df)
    
    return employees_df, demand_df, availability_df

def save_sample_data(employees_df: pd.DataFrame, demand_df: pd.DataFrame, 
                    availability_df: pd.DataFrame, output_dir: str = "sample_data"):
    """Save the generated data to CSV files."""
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Save individual datasets
    employees_df.to_csv(f"{output_dir}/employees.csv", index=False)
    demand_df.to_csv(f"{output_dir}/demand_forecast.csv", index=False)
    availability_df.to_csv(f"{output_dir}/staff_data.csv", index=False)
    
    print(f"Data saved to {output_dir}/")
    print(f"- employees.csv: {len(employees_df)} employees")
    print(f"- demand_forecast.csv: {len(demand_df)} days of demand data")
    print(f"- staff_data.csv: {len(availability_df)} availability records")

if __name__ == "__main__":
    # Generate and save sample data
    employees_df, demand_df, availability_df = create_sample_dataset()
    save_sample_data(employees_df, demand_df, availability_df)
