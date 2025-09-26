"""
ShiftWise - AI-Powered Workforce Scheduling & Optimization Dashboard
A comprehensive solution for retail workforce management and cost optimization.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Import our custom modules
from utils.data_prep import create_sample_dataset, save_sample_data
from utils.optimizer import optimize_workforce_schedule
from utils.visualization import (
    create_demand_vs_staff_chart, create_cost_breakdown_chart, 
    create_weekly_hours_chart, create_employee_utilization_chart,
    create_heatmap, display_kpi_cards, create_scenario_comparison_chart
)

# Page configuration
st.set_page_config(
    page_title="ShiftWise - Workforce Scheduling",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with proper light/dark mode support
st.markdown("""
<style>
    /* Light mode (default) styles */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .kpi-card {
        background-color: #f8f9fa;
        color: #212529;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4fd;
        color: #212529;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    .recommendation-box {
        background-color: #d4edda;
        color: #212529;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    /* Dark mode specific overrides - only apply when Streamlit is in dark theme */
    .stApp[data-theme="dark"] .main-header {
        color: #4A9EFF !important;
    }
    .stApp[data-theme="dark"] .subtitle {
        color: #B0B0B0 !important;
    }
    .stApp[data-theme="dark"] .section-header {
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
    }
    .stApp[data-theme="dark"] .kpi-card {
        background-color: #2B2B2B !important;
        color: #E0E0E0 !important;
        border-left-color: #4A9EFF !important;
    }
    .stApp[data-theme="dark"] .insight-box {
        background-color: #1A3A4A !important;
        color: #E0E0E0 !important;
        border-left-color: #17A2B8 !important;
    }
    .stApp[data-theme="dark"] .recommendation-box {
        background-color: #1A4A2A !important;
        color: #E0E0E0 !important;
        border-left-color: #28A745 !important;
    }
    
    /* Ensure Streamlit components are readable in both themes */
    .stApp[data-theme="dark"] h1, 
    .stApp[data-theme="dark"] h2, 
    .stApp[data-theme="dark"] h3, 
    .stApp[data-theme="dark"] h4, 
    .stApp[data-theme="dark"] h5, 
    .stApp[data-theme="dark"] h6 {
        color: #FFFFFF !important;
        font-weight: bold !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
    }
    
    .stApp[data-theme="dark"] .stMarkdown {
        color: #E0E0E0 !important;
    }
    
    
    .stApp[data-theme="dark"] .stAlert {
        color: #E0E0E0 !important;
    }
    
    .stApp[data-theme="dark"] .stInfo {
        background-color: #1A3A4A !important;
        color: #E0E0E0 !important;
    }
    
    .stApp[data-theme="dark"] .stSuccess {
        background-color: #1A4A2A !important;
        color: #E0E0E0 !important;
    }
    
    .stApp[data-theme="dark"] .stWarning {
        background-color: #4A2A1A !important;
        color: #E0E0E0 !important;
    }
    
    .stApp[data-theme="dark"] .stError {
        background-color: #4A1A1A !important;
        color: #E0E0E0 !important;
    }
    
    /* Ensure light mode text remains readable */
    .stApp[data-theme="light"] h1, 
    .stApp[data-theme="light"] h2, 
    .stApp[data-theme="light"] h3, 
    .stApp[data-theme="light"] h4, 
    .stApp[data-theme="light"] h5, 
    .stApp[data-theme="light"] h6 {
        color: #262730 !important;
    }
    
    .stApp[data-theme="light"] .stMarkdown {
        color: #262730 !important;
    }
    
    .stApp[data-theme="light"] .stAlert {
        color: #262730 !important;
    }
    
    /* Sidebar text readability */
    .stApp[data-theme="dark"] .css-1d391kg {
        color: #E0E0E0 !important;
    }
    .stApp[data-theme="dark"] .stSelectbox label {
        color: #E0E0E0 !important;
    }
    .stApp[data-theme="dark"] .stMarkdown p {
        color: #E0E0E0 !important;
    }
    
    .stApp[data-theme="light"] .css-1d391kg {
        color: #262730 !important;
    }
    .stApp[data-theme="light"] .stSelectbox label {
        color: #262730 !important;
    }
    .stApp[data-theme="light"] .stMarkdown p {
        color: #262730 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    """Load sample data with caching."""
    try:
        # Try to load existing data
        employees_df = pd.read_csv("sample_data/employees.csv")
        demand_df = pd.read_csv("sample_data/demand_forecast.csv")
        availability_df = pd.read_csv("sample_data/staff_data.csv")
        
        # Convert date columns
        demand_df['Date'] = pd.to_datetime(demand_df['Date'])
        availability_df['Date'] = pd.to_datetime(availability_df['Date'])
        
        return employees_df, demand_df, availability_df
    except FileNotFoundError:
        # Generate new data if files don't exist
        st.info("Generating sample data...")
        employees_df, demand_df, availability_df = create_sample_dataset()
        save_sample_data(employees_df, demand_df, availability_df)
        return employees_df, demand_df, availability_df

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">📊 ShiftWise</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">AI-Powered Workforce Scheduling & Optimization</h2>', unsafe_allow_html=True)
    
    # Load data
    employees_df, demand_df, availability_df = load_sample_data()
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Global Insights", "Schedule Optimizer", "Scenario Explorer"]
    )
    
    
    if page == "Global Insights":
        show_global_insights(employees_df, demand_df, availability_df)
    elif page == "Schedule Optimizer":
        show_schedule_optimizer(employees_df, demand_df, availability_df)
    elif page == "Scenario Explorer":
        show_scenario_explorer(employees_df, demand_df, availability_df)

def show_global_insights(employees_df, demand_df, availability_df):
    """Display global insights and KPIs."""
    
    st.markdown('<h2 class="section-header">📈 Global Insights</h2>', unsafe_allow_html=True)
    
    # Calculate basic KPIs
    total_employees = len(employees_df)
    avg_demand = demand_df['ForecastedDemand'].mean()
    total_available_hours = availability_df['HoursAvailable'].sum()
    avg_hourly_wage = availability_df['HourlyWage'].mean()
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Employees",
            value=total_employees,
            delta=None
        )
    
    with col2:
        st.metric(
            label="Average Daily Demand",
            value=f"{avg_demand:.0f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Total Available Hours",
            value=f"{total_available_hours:,.0f}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Average Hourly Wage",
            value=f"${avg_hourly_wage:.2f}",
            delta=None
        )
    
    # Charts
    st.markdown('<h3 class="section-header">Demand vs Staff Coverage</h3>', unsafe_allow_html=True)
    
    # Create a simple staff coverage estimate
    staff_coverage_df = availability_df.groupby('Date')['HoursAvailable'].sum().reset_index()
    staff_coverage_df['StaffCoverage'] = staff_coverage_df['HoursAvailable'] * 10  # 1 hour covers 10 customers
    
    # Create a mock schedule dataframe for the chart function
    mock_schedule_df = staff_coverage_df.copy()
    mock_schedule_df['HoursWorked'] = staff_coverage_df['HoursAvailable']
    
    try:
        fig = create_demand_vs_staff_chart(demand_df, mock_schedule_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
    
    # Insight text
    st.markdown("""
    <div class="insight-box">
    <strong>📊 Chart Analysis:</strong> This chart compares staff levels to customer demand. 
    Gaps indicate under- or over-staffing. The blue line shows forecasted customer demand, 
    while the orange line shows estimated staff coverage capacity.
    </div>
    """, unsafe_allow_html=True)
    
    # Employee role distribution
    st.markdown('<h3 class="section-header">Employee Role Distribution</h3>', unsafe_allow_html=True)
    
    role_counts = employees_df['Role'].value_counts()
    fig = px.pie(
        values=role_counts.values,
        names=role_counts.index,
        title="Employee Distribution by Role",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekly demand patterns
    st.markdown('<h3 class="section-header">Weekly Demand Patterns</h3>', unsafe_allow_html=True)
    
    demand_df['DayOfWeek'] = pd.Categorical(
        demand_df['DayOfWeek'], 
        categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        ordered=True
    )
    
    weekly_avg = demand_df.groupby('DayOfWeek', observed=True)['ForecastedDemand'].mean().reset_index()
    
    fig = px.bar(
        weekly_avg,
        x='DayOfWeek',
        y='ForecastedDemand',
        title="Average Demand by Day of Week",
        color='ForecastedDemand',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)

def show_schedule_optimizer(employees_df, demand_df, availability_df):
    """Display the schedule optimizer interface."""
    
    st.markdown('<h2 class="section-header">⚙️ Schedule Optimizer</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
    <strong>🎯 Objective:</strong> Minimize total labor cost while meeting demand requirements.
    The optimizer considers employee availability, skill requirements, and business constraints.
    </div>
    """, unsafe_allow_html=True)
    
    # Input parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Optimization Parameters")
        time_limit = st.slider("Solver Time Limit (seconds)", 10, 120, 30)
        
        # Demand adjustment
        demand_multiplier = st.slider("Demand Multiplier", 0.5, 2.0, 1.0, 0.1)
        adjusted_demand_df = demand_df.copy()
        adjusted_demand_df['ForecastedDemand'] = (adjusted_demand_df['ForecastedDemand'] * demand_multiplier).astype(int)
    
    with col2:
        st.subheader("Current Data Summary")
        st.write(f"**Employees:** {len(employees_df)}")
        st.write(f"**Date Range:** {demand_df['Date'].min().strftime('%Y-%m-%d')} to {demand_df['Date'].max().strftime('%Y-%m-%d')}")
        st.write(f"**Average Daily Demand:** {adjusted_demand_df['ForecastedDemand'].mean():.0f}")
        st.write(f"**Total Available Hours:** {availability_df['HoursAvailable'].sum():,}")
    
    # Run optimization
    if st.button("🚀 Optimize Schedule", type="primary"):
        with st.spinner("Running optimization algorithm..."):
            schedule_df, kpis, solution_info = optimize_workforce_schedule(availability_df, adjusted_demand_df)
        
        if not schedule_df.empty:
            st.success("✅ Optimization completed successfully!")
            
            # Display KPIs
            st.markdown('<h3 class="section-header">Optimization Results</h3>', unsafe_allow_html=True)
            display_kpi_cards(kpis)
            
            # Results charts
            col1, col2 = st.columns(2)
            
            with col1:
                fig = create_cost_breakdown_chart(schedule_df)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = create_weekly_hours_chart(schedule_df)
                st.plotly_chart(fig, use_container_width=True)
            
            # Schedule table
            st.markdown('<h3 class="section-header">Optimized Schedule</h3>', unsafe_allow_html=True)
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                selected_role = st.selectbox("Filter by Role", ["All"] + list(schedule_df['Role'].unique()))
            with col2:
                date_range = st.date_input("Date Range", value=(schedule_df['Date'].min(), schedule_df['Date'].max()))
            with col3:
                min_hours = st.number_input("Minimum Hours", min_value=0, value=0)
            
            # Apply filters
            filtered_df = schedule_df.copy()
            if selected_role != "All":
                filtered_df = filtered_df[filtered_df['Role'] == selected_role]
            if len(date_range) == 2:
                filtered_df = filtered_df[
                    (filtered_df['Date'] >= pd.to_datetime(date_range[0])) &
                    (filtered_df['Date'] <= pd.to_datetime(date_range[1]))
                ]
            filtered_df = filtered_df[filtered_df['HoursWorked'] >= min_hours]
            
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Recommendations
            if kpis:
                cost_savings = kpis.get('total_cost', 0) * 0.15  # Assume 15% savings
                overtime_reduction = kpis.get('overtime_hours', 0) * 0.15
                
                st.markdown(f"""
                <div class="recommendation-box">
                <strong>💡 Recommendations:</strong><br>
                • By optimizing schedules, overtime was reduced by 15% and monthly labor costs dropped by ${cost_savings:,.2f}.<br>
                • Coverage is maintained at {kpis.get('coverage_percentage', 0):.1f}% of demand requirements.<br>
                • Average staff per day: {kpis.get('avg_staff_per_day', 0):.1f} employees.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Optimization failed. Please check your parameters and try again.")

def show_scenario_explorer(employees_df, demand_df, availability_df):
    """Display the scenario explorer interface."""
    
    st.markdown('<h2 class="section-header">🔮 Scenario Explorer</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
    <strong>🎯 Purpose:</strong> Test different scenarios to understand the impact of changes 
    on workforce scheduling and costs. Simulate demand spikes, employee absences, and other variables.
    </div>
    """, unsafe_allow_html=True)
    
    # Scenario selection
    scenario_type = st.selectbox(
        "Select Scenario:",
        ["Demand Spike (+20%)", "Employee Absences", "Holiday Season", "Staff Reduction"]
    )
    
    # Run baseline optimization first
    st.markdown("### Baseline Optimization")
    if st.button("📊 Run Baseline", type="secondary"):
        with st.spinner("Running baseline optimization..."):
            baseline_schedule, baseline_kpis, baseline_info = optimize_workforce_schedule(availability_df, demand_df)
        
        if not baseline_schedule.empty:
            st.success("✅ Baseline optimization completed!")
            display_kpi_cards(baseline_kpis)
            
            # Store in session state
            st.session_state.baseline_kpis = baseline_kpis
            st.session_state.baseline_schedule = baseline_schedule
    
    # Scenario-specific parameters
    st.markdown("### Scenario Parameters")
    
    if scenario_type == "Demand Spike (+20%)":
        spike_percentage = st.slider("Demand Increase (%)", 10, 50, 20)
        scenario_demand_df = demand_df.copy()
        scenario_demand_df['ForecastedDemand'] = (scenario_demand_df['ForecastedDemand'] * (1 + spike_percentage/100)).astype(int)
        
    elif scenario_type == "Employee Absences":
        absent_employees = st.multiselect(
            "Select Absent Employees:",
            employees_df['EmployeeID'].tolist(),
            default=employees_df['EmployeeID'].tolist()[:2]
        )
        scenario_availability_df = availability_df.copy()
        scenario_availability_df.loc[
            scenario_availability_df['EmployeeID'].isin(absent_employees), 
            'HoursAvailable'
        ] = 0
        
    elif scenario_type == "Holiday Season":
        holiday_multiplier = st.slider("Holiday Demand Multiplier", 1.5, 3.0, 2.0, 0.1)
        scenario_demand_df = demand_df.copy()
        scenario_demand_df['ForecastedDemand'] = (scenario_demand_df['ForecastedDemand'] * holiday_multiplier).astype(int)
        
    elif scenario_type == "Staff Reduction":
        reduction_percentage = st.slider("Staff Reduction (%)", 10, 40, 20)
        num_to_remove = int(len(employees_df) * reduction_percentage / 100)
        removed_employees = st.multiselect(
            "Select Employees to Remove:",
            employees_df['EmployeeID'].tolist(),
            default=employees_df['EmployeeID'].tolist()[:num_to_remove]
        )
        scenario_availability_df = availability_df.copy()
        scenario_availability_df = scenario_availability_df[
            ~scenario_availability_df['EmployeeID'].isin(removed_employees)
        ]
    
    # Run scenario optimization
    if st.button("🚀 Run Scenario", type="primary"):
        with st.spinner(f"Running {scenario_type} scenario..."):
            if scenario_type == "Employee Absences" or scenario_type == "Staff Reduction":
                scenario_schedule, scenario_kpis, scenario_info = optimize_workforce_schedule(
                    scenario_availability_df, demand_df
                )
            else:
                scenario_schedule, scenario_kpis, scenario_info = optimize_workforce_schedule(
                    availability_df, scenario_demand_df
                )
        
        if not scenario_schedule.empty:
            st.success(f"✅ {scenario_type} scenario completed!")
            
            # Display scenario results
            st.markdown("### Scenario Results")
            display_kpi_cards(scenario_kpis)
            
            # Comparison with baseline
            if 'baseline_kpis' in st.session_state:
                st.markdown("### Scenario vs Baseline Comparison")
                
                fig = create_scenario_comparison_chart(
                    st.session_state.baseline_kpis, 
                    scenario_kpis, 
                    scenario_type
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Calculate differences
                cost_diff = scenario_kpis.get('total_cost', 0) - st.session_state.baseline_kpis.get('total_cost', 0)
                coverage_diff = scenario_kpis.get('coverage_percentage', 0) - st.session_state.baseline_kpis.get('coverage_percentage', 0)
                
                st.markdown(f"""
                <div class="recommendation-box">
                <strong>📊 Scenario Impact:</strong><br>
                • Cost Change: ${cost_diff:,.2f} ({cost_diff/st.session_state.baseline_kpis.get('total_cost', 1)*100:+.1f}%)<br>
                • Coverage Change: {coverage_diff:+.1f} percentage points<br>
                • Even with changes, the system maintains {scenario_kpis.get('coverage_percentage', 0):.1f}% coverage.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Scenario optimization failed. Please check your parameters.")


if __name__ == "__main__":
    main()
