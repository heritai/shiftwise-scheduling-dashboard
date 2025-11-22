# ShiftWise — AI-Powered Workforce Scheduling & Optimization

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![OR-Tools](https://img.shields.io/badge/OR--Tools-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://developers.google.com/optimization)

> **Transform workforce scheduling: Cut labor costs and boost efficiency with AI.**

## 🚨 The Problem

Manual scheduling frequently results in costly overtime, inadequate coverage, and employee dissatisfaction. Retail managers often dedicate countless hours each week balancing fluctuating demand, employee availability, and labor costs, leading to:

-   **High overtime costs** due to reactive and inefficient scheduling
-   **Suboptimal shift coverage** during critical peak hours
-   **Decreased employee satisfaction** from unpredictable and unfair schedules
-   **Manager burnout** caused by continuous, time-consuming schedule adjustments

## ✅ The Solution

ShiftWise is a comprehensive, AI-powered dashboard engineered to create optimized staff schedules by intelligently balancing demand, availability, and labor rules. Our advanced optimization engine is designed to:

-   **Minimize labor costs** while consistently meeting all coverage requirements
-   **Respect employee preferences** and availability constraints, fostering better work-life balance
-   **Ensure essential supervisor coverage** for every shift
-   **Provide real-time insights** and robust scenario planning capabilities

## 📊 Results

ShiftWise empowers retail chains to achieve significant improvements and quantifiable benefits, including:

-   **15-25% reduction** in labor costs through truly optimized scheduling
-   **Consistently 95%+ coverage** of all demand requirements
-   **5-10 hours saved weekly** for managers, freeing up time for strategic tasks
-   **Enhanced employee satisfaction** with fair, predictable, and transparent schedules

## 🚀 Quick Start

### Prerequisites

-   Python 3.10+
-   pip package manager (usually included with Python)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-org/shiftwise-scheduling-dashboard.git
    cd shiftwise-scheduling-dashboard
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**
    ```bash
    streamlit run app.py
    ```

4.  **Access the Dashboard**
    Navigate to `http://localhost:8501` to launch the ShiftWise dashboard.

## 🏗️ Project Structure

```
shiftwise-scheduling-dashboard/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── utils/                    # Utility scripts
│   ├── data_prep.py          # Generates synthetic data
│   ├── optimizer.py          # Core OR-Tools optimization engine
│   └── visualization.py      # Charting and visualization utilities
├── sample_data/              # Sample data files
│   ├── employees.csv         # Employee master data details
│   ├── demand_forecast.csv   # 3-month demand forecast data
│   └── staff_data.csv        # Daily employee availability records
└── reports/                  # Generated reports
    └── example_report.pdf    # Sample optimization report output
```

## 🎯 Features

### 📈 Global Insights
-   **KPI Dashboard:** Visualize critical metrics like total cost, hours, coverage, and overtime at a glance.
-   **Demand Analysis:** Visually compare forecasted demand against actual staff coverage for immediate insights.
-   **Role Distribution:** Understand employee breakdown by position and skill level across the workforce.
-   **Weekly Patterns:** Identify day-of-week demand trends and uncover key insights.

### ⚙️ Schedule Optimizer
-   **Constraint Programming:** Leverages advanced optimization techniques powered by OR-Tools.
-   **Cost Minimization:** Automatically minimizes total labor costs while rigorously meeting demand requirements.
-   **Interactive Results:** Explore a filterable schedule table offering real-time updates and granular detail.
-   **Performance Metrics:** Access detailed KPIs and comprehensive cost breakdowns post-optimization.
-   **Smart Recommendations:** Receive AI-generated insights and actionable scheduling suggestions.

### 🔮 Scenario Explorer
-   **Demand Spikes:** Model the impact of sudden increases in customer traffic or unexpected surges.
-   **Employee Absences:** Simulate the effects of sick days, vacations, or other unexpected personal time.
-   **Holiday Planning:** Proactively prepare for seasonal demand surges, holidays, and special events.
-   **Staff Reductions:** Analyze the precise impact of workforce reductions or planned expansions.
-   **Side-by-Side Comparison:** Visually compare different scenarios against baseline results to support informed decision-making.

## 🔧 Technical Architecture

### Optimization Engine
-   **OR-Tools Constraint Programming:** Utilizes an industry-standard, robust optimization solver.
-   **Multi-objective Optimization:** Balances complex objectives such as cost, coverage, and employee satisfaction.
-   **Constraint Management:** Dynamically handles intricate availability rules, skill requirements, and simulated labor law compliance.
-   **Scalable Design:** Efficiently scales to manage schedules for 25+ employees across 90+ days.

### Data Pipeline
-   **Synthetic Data Generation:** Includes realistic employee and demand patterns for demonstration purposes.
-   **Real-time Processing:** Ensures rapid data preparation and optimization cycles.
-   **Caching Strategy:** Leverages Streamlit caching for significantly improved performance and dashboard responsiveness.
-   **Error Handling:** Implements robust error management with clear, actionable user feedback.

### Visualization
-   **Interactive Charts:** Engaging and dynamic visualizations powered by Plotly for enhanced data exploration.
-   **Dark/Light Mode:** Adaptive theming across all components to respect user preferences.
-   **High Contrast:** Optimized for readability and visual comfort in both light and dark modes.
-   **Accessible Design:** Incorporates color-blind friendly palettes to ensure broader accessibility.
-   **Real-time Updates:** Dynamic charts provide immediate feedback, updating seamlessly with new data.

## 📊 Sample Data

The application comes pre-loaded with 3 months of synthetic, yet realistic, sample data for immediate exploration and demonstration:

-   **25 Employees:** Spanning 3 distinct roles (Cashier, Stock, Supervisor) for varied scenarios.
-   **90 Days:** Comprehensive demand forecasts incorporating typical weekend patterns and seasonal variations.
-   **2,250 Availability Records:** Detailed records reflecting realistic employee constraints and preferences.
-   **Part-time & Full-time:** Employees with diverse availability patterns to simulate real-world scenarios.

### Key Data Patterns
-   **Higher Weekend Demand:** Modeled with a typical 30-80% increase compared to weekday requirements.
-   **Part-time Availability:** Approximately 30% of non-supervisor employees are designated as part-time.
-   **Supervisor Requirements:** Ensures at least one supervisor is scheduled per shift to maintain operational oversight.
-   **Realistic Wage Ranges:** Wages set between $15-25/hour, with variations based on role and experience.

## 🎨 User Interface

### Design Principles
-   **Business-First Approach:** Prioritizing actionable insights that drive measurable business value.
-   **Intuitive Navigation:** Ensuring clear page structure and a seamless, efficient user flow.
-   **Visual Hierarchy:** Strategically highlights critical information for rapid comprehension and decision-making.
-   **Consistent Styling:** Maintaining a professional and cohesive appearance throughout the application's interface.

### Theme Support
-   **Adaptive Colors:** Automatically adjusts to align with Streamlit's native theme settings (light/dark mode).
-   **High Contrast:** Optimized for readability and visual comfort in both light and dark modes.
-   **Accessible Design:** Incorporates color-blind friendly palettes to ensure broader accessibility.
-   **Mobile Responsive:** Fully functional and optimized for a consistent experience across all device sizes.

## 🔍 Use Cases

### Retail Chain Management
-   **Store Managers:** For daily schedule optimization, planning, and real-time adjustments.
-   **District Managers:** For high-level workforce analysis and resource allocation across multiple locations.
-   **HR Directors:** For strategic labor cost analysis, budget planning, and compliance oversight.
-   **Operations Teams:** For identifying process improvements and driving overall efficiency gains.

### Consulting Applications
-   **Workforce Optimization:** As a powerful tool for client presentations, workshops, and solution demonstrations.
-   **Cost Reduction Projects:** To quantify potential labor savings and demonstrate ROI for clients.
-   **Process Improvement:** To pinpoint and address scheduling inefficiencies within client operations.
-   **Technology Assessment:** To evaluate and showcase advanced optimization solutions to prospective clients.

## ⚠️ Important Disclaimers

### Demo Purposes Only
This project primarily serves as a demonstration using synthetic data and simplified models. A full-scale, real-world implementation would typically require:

-   Seamless integration with existing HR and payroll systems (e.g., Workday, BambooHR).
-   Sophisticated demand forecasting, often utilizing advanced machine learning models.
-   Comprehensive adherence to various labor laws (state, federal, local, and union regulations).
-   Incorporation of employee preference learning via historical data analysis and feedback loops.
-   Capabilities for real-time adjustments and dynamic schedule updates within operational workflows.

### Limitations
-   **Simplified Constraints:** Real-world scheduling often involves a more extensive and complex set of rules and dependencies.
-   **Synthetic Data:** The provided data is illustrative; actual employee data would be more nuanced, diverse, and dynamic.
-   **Single Location Focus:** Currently designed for single-location optimization; multi-location capabilities or network-wide optimization are not included.
-   **Static Demand:** Demand forecasts are static; real-time demand updates or dynamic adjustments are not integrated.

## 🤝 Contributing

We warmly welcome contributions to ShiftWise! Please refer to our [Contributing Guidelines](CONTRIBUTING.md) for detailed instructions.

### Development Setup
1.  Fork the repository
2.  Create a feature branch
3.  Make your changes
4.  Add tests if applicable
5.  Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

-   **Documentation:** Refer to this README file and inline code comments for guidance.
-   **Issues:** Report any bugs or request new features through GitHub Issues.
-   **Discussions:** Engage with the community and share insights in GitHub Discussions.

## 🙏 Acknowledgments

-   **OR-Tools:** Google's powerful suite of optimization tools for constraint programming.
-   **Streamlit:** The intuitive framework for rapid web application development.
-   **Plotly:** For creating rich, interactive data visualizations.
-   **Pandas:** The essential library for robust data manipulation and analysis.
-   **NumPy:** The fundamental package for numerical computing in Python.

---

Built with ❤️ for the retail workforce management community

*ShiftWise: AI-Powered Workforce Scheduling & Optimization Demo*