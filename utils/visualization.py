"""
Visualization utilities for ShiftWise dashboard.
Supports both dark and light themes with adaptive colors.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

class ThemeColors:
    """Adaptive color scheme for dark/light themes."""
    
    @staticmethod
    def detect_theme():
        """Detect if we're in dark mode."""
        try:
            import streamlit as st
            # Try multiple methods to detect dark theme
            try:
                # Method 1: Check theme option
                return st.get_option("theme.base") == "dark"
            except:
                try:
                    # Method 2: Check if we can access theme from config
                    import streamlit.web.cli as stcli
                    return False  # Default to light mode
                except:
                    return False
        except:
            return False
    
    @staticmethod
    def get_colors():
        """Get color palette based on Streamlit theme."""
        is_dark = ThemeColors.detect_theme()
        
        if is_dark:
            return {
                'primary': '#4A9EFF',      # Brighter blue for dark mode
                'secondary': '#FFB366',    # Brighter orange for dark mode
                'success': '#4CAF50',      # Brighter green for dark mode
                'warning': '#FF6B6B',      # Brighter red for dark mode
                'info': '#17A2B8',         # Keep info color
                'light': '#2B2B2B',        # Dark surface
                'dark': '#1A1A1A',         # Darker surface
                'background': '#0E1117',   # Streamlit dark background
                'surface': '#262730',      # Dark surface
                'text': '#FFFFFF',         # Pure white text
                'text_secondary': '#FFFFFF' # Pure white for secondary text too
            }
        else:
            return {
                'primary': '#1f77b4',      # Standard blue
                'secondary': '#ff7f0e',    # Standard orange
                'success': '#28a745',      # Standard green
                'warning': '#fd7e14',      # Standard orange-red
                'info': '#17a2b8',         # Standard info blue
                'light': '#f8f9fa',        # Light gray
                'dark': '#343a40',         # Dark gray
                'background': '#ffffff',   # White background
                'surface': '#f8f9fa',      # Light surface
                'text': '#212529',         # Dark text
                'text_secondary': '#6c757d' # Medium gray text
            }

def create_demand_vs_staff_chart(demand_df: pd.DataFrame, schedule_df: pd.DataFrame, 
                                title: str = "Demand vs Staff Coverage") -> go.Figure:
    """Create a chart comparing forecasted demand to scheduled staff."""
    
    colors = ThemeColors.get_colors()
    
    # Aggregate staff hours by date
    if not schedule_df.empty:
        staff_hours = schedule_df.groupby('Date')['HoursWorked'].sum().reset_index()
        staff_hours['Date'] = pd.to_datetime(staff_hours['Date'])
    else:
        staff_hours = pd.DataFrame(columns=['Date', 'HoursWorked'])
    
    # Merge with demand data
    merged_df = demand_df.merge(staff_hours, on='Date', how='left')
    merged_df['HoursWorked'] = merged_df['HoursWorked'].fillna(0)
    
    # Create figure
    fig = go.Figure()
    
    # Add demand line
    fig.add_trace(go.Scatter(
        x=merged_df['Date'],
        y=merged_df['ForecastedDemand'],
        mode='lines+markers',
        name='Forecasted Demand',
        line=dict(color=colors['primary'], width=3),
        marker=dict(size=6)
    ))
    
    # Add staff coverage line (convert hours to equivalent demand coverage)
    # Assume 1 hour of work covers 10 customers
    staff_coverage = merged_df['HoursWorked'] * 10
    fig.add_trace(go.Scatter(
        x=merged_df['Date'],
        y=staff_coverage,
        mode='lines+markers',
        name='Staff Coverage (Hours × 10)',
        line=dict(color=colors['secondary'], width=3),
        marker=dict(size=6)
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=24, color=colors['text']),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text='Date', font=dict(size=16, color=colors['text'])),
            tickfont=dict(size=14, color=colors['text']),
            gridcolor=colors['text_secondary'],
            color=colors['text']
        ),
        yaxis=dict(
            title=dict(text='Number of Customers', font=dict(size=16, color=colors['text'])),
            tickfont=dict(size=14, color=colors['text']),
            gridcolor=colors['text_secondary'],
            color=colors['text']
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text']),
        legend=dict(
            x=1.02,  # Move legend to the right side
            y=1,     # Position at the top
            xanchor='left',  # Anchor to left edge
            yanchor='top',   # Anchor to top edge
            bgcolor=colors['surface'],
            bordercolor=colors['text_secondary'],
            font=dict(size=14, color=colors['text'])
        ),
        margin=dict(r=150)  # Add right margin to accommodate legend
    )
    
    return fig

def create_cost_breakdown_chart(schedule_df: pd.DataFrame, title: str = "Cost Breakdown by Role") -> go.Figure:
    """Create a pie chart showing cost breakdown by employee role."""
    
    if schedule_df.empty:
        return go.Figure()
    
    colors = ThemeColors.get_colors()
    
    # Calculate costs by role
    role_costs = schedule_df.groupby('Role')['Cost'].sum().reset_index()
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=role_costs['Role'],
        values=role_costs['Cost'],
        hole=0.3,
        marker_colors=[colors['primary'], colors['secondary'], colors['success']]
    )])
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=22, color=colors['text']),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text']),
        legend=dict(
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor=colors['surface'],
            bordercolor=colors['text_secondary'],
            font=dict(size=14, color=colors['text'])
        ),
        margin=dict(r=150)
    )
    
    return fig

def create_weekly_hours_chart(schedule_df: pd.DataFrame, title: str = "Weekly Hours Distribution") -> go.Figure:
    """Create a bar chart showing weekly hours distribution."""
    
    if schedule_df.empty:
        return go.Figure()
    
    colors = ThemeColors.get_colors()
    
    # Calculate weekly hours
    schedule_df['Date'] = pd.to_datetime(schedule_df['Date'])
    schedule_df['Week'] = schedule_df['Date'].dt.to_period('W')
    
    weekly_hours = schedule_df.groupby('Week')['HoursWorked'].sum().reset_index()
    weekly_hours['Week_Str'] = weekly_hours['Week'].astype(str)
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=weekly_hours['Week_Str'],
            y=weekly_hours['HoursWorked'],
            marker_color=colors['primary'],
            text=weekly_hours['HoursWorked'],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=22, color=colors['text']),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text='Week', font=dict(size=16, color=colors['text'])),
            tickfont=dict(size=14, color=colors['text']),
            gridcolor=colors['text_secondary'],
            color=colors['text']
        ),
        yaxis=dict(
            title=dict(text='Total Hours', font=dict(size=16, color=colors['text'])),
            tickfont=dict(size=14, color=colors['text']),
            gridcolor=colors['text_secondary'],
            color=colors['text']
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text']),
        legend=dict(
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor=colors['surface'],
            bordercolor=colors['text_secondary'],
            font=dict(size=14, color=colors['text'])
        ),
        margin=dict(r=150)
    )
    
    return fig

def create_employee_utilization_chart(schedule_df: pd.DataFrame, title: str = "Employee Utilization") -> go.Figure:
    """Create a chart showing employee utilization rates."""
    
    if schedule_df.empty:
        return go.Figure()
    
    colors = ThemeColors.get_colors()
    
    # Calculate utilization by employee
    employee_stats = schedule_df.groupby('EmployeeID').agg({
        'HoursWorked': 'sum',
        'Role': 'first'
    }).reset_index()
    
    # Sort by hours worked
    employee_stats = employee_stats.sort_values('HoursWorked', ascending=True)
    
    # Create horizontal bar chart
    fig = go.Figure(data=[
        go.Bar(
            y=employee_stats['EmployeeID'],
            x=employee_stats['HoursWorked'],
            orientation='h',
            marker_color=colors['primary'],
            text=employee_stats['HoursWorked'],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=22, color=colors['text']),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Total Hours Worked',
            gridcolor=colors['text_secondary'],
            color=colors['text']
        ),
        yaxis=dict(
            title='Employee ID',
            gridcolor=colors['text_secondary'],
            color=colors['text']
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text']),
        height=600,
        legend=dict(
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor=colors['surface'],
            bordercolor=colors['text_secondary'],
            font=dict(size=14, color=colors['text'])
        ),
        margin=dict(r=150)
    )
    
    return fig

def create_heatmap(schedule_df: pd.DataFrame, title: str = "Schedule Heatmap") -> go.Figure:
    """Create a heatmap showing employee schedules."""
    
    if schedule_df.empty:
        return go.Figure()
    
    colors = ThemeColors.get_colors()
    
    # Prepare data for heatmap
    schedule_df['Date'] = pd.to_datetime(schedule_df['Date'])
    pivot_data = schedule_df.pivot_table(
        values='HoursWorked',
        index='EmployeeID',
        columns='Date',
        fill_value=0
    )
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns.strftime('%Y-%m-%d'),
        y=pivot_data.index,
        colorscale='Blues',
        showscale=True,
        colorbar=dict(title="Hours Worked")
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=22, color=colors['text']),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Date',
            gridcolor=colors['text_secondary'],
            color=colors['text']
        ),
        yaxis=dict(
            title='Employee ID',
            gridcolor=colors['text_secondary'],
            color=colors['text']
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text']),
        legend=dict(
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor=colors['surface'],
            bordercolor=colors['text_secondary'],
            font=dict(size=14, color=colors['text'])
        ),
        margin=dict(r=150)
    )
    
    return fig

def display_kpi_cards(kpis: Dict) -> None:
    """Display KPI cards in a grid layout."""
    
    colors = ThemeColors.get_colors()
    
    if not kpis:
        st.warning("No KPI data available.")
        return
    
    # Create columns for KPI cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Cost",
            value=f"${kpis.get('total_cost', 0):,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Total Hours",
            value=f"{kpis.get('total_hours', 0):,.0f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Coverage %",
            value=f"{kpis.get('coverage_percentage', 0):.1f}%",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Overtime Hours",
            value=f"{kpis.get('overtime_hours', 0):,.0f}",
            delta=None
        )

def create_scenario_comparison_chart(original_kpis: Dict, scenario_kpis: Dict, 
                                   scenario_name: str = "Scenario") -> go.Figure:
    """Create a comparison chart between original and scenario results."""
    
    colors = ThemeColors.get_colors()
    
    metrics = ['total_cost', 'total_hours', 'coverage_percentage', 'overtime_hours']
    metric_labels = ['Total Cost ($)', 'Total Hours', 'Coverage (%)', 'Overtime Hours']
    
    original_values = [original_kpis.get(metric, 0) for metric in metrics]
    scenario_values = [scenario_kpis.get(metric, 0) for metric in metrics]
    
    # Normalize values for comparison (except coverage percentage)
    normalized_original = []
    normalized_scenario = []
    
    for i, metric in enumerate(metrics):
        if metric == 'coverage_percentage':
            normalized_original.append(original_values[i])
            normalized_scenario.append(scenario_values[i])
        else:
            max_val = max(original_values[i], scenario_values[i])
            if max_val > 0:
                normalized_original.append(original_values[i] / max_val * 100)
                normalized_scenario.append(scenario_values[i] / max_val * 100)
            else:
                normalized_original.append(0)
                normalized_scenario.append(0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Original',
        x=metric_labels,
        y=normalized_original,
        marker_color=colors['primary']
    ))
    
    fig.add_trace(go.Bar(
        name=scenario_name,
        x=metric_labels,
        y=normalized_scenario,
        marker_color=colors['secondary']
    ))
    
    fig.update_layout(
        title=f"Original vs {scenario_name} Comparison",
        xaxis_title="Metrics",
        yaxis_title="Normalized Values (%)",
        barmode='group',
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text'])
    )
    
    return fig
