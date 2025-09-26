# 🚀 Streamlit Cloud Deployment Guide

## Repository Information
- **GitHub Repository**: https://github.com/heritai/shiftwise-scheduling-dashboard
- **Main File**: `app.py`
- **Python Version**: 3.9+ (recommended)

## Deployment Steps

### 1. Go to Streamlit Cloud
Visit [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.

### 2. Deploy New App
1. Click **"New app"**
2. Select your GitHub account: **heritai**
3. Select repository: **shiftwise-scheduling-dashboard**
4. Select branch: **main**
5. Main file path: **app.py**

### 3. Advanced Settings (Optional)
- **Python version**: 3.9
- **Dependencies**: Will use `requirements.txt` automatically
- **Secrets**: Not needed for this demo

### 4. Deploy
Click **"Deploy!"** and wait for the deployment to complete.

## What's Included

### 📁 Project Structure
```
shiftwise-scheduling-dashboard/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── .streamlit/
│   └── config.toml          # Streamlit configuration (light theme default)
├── utils/
│   ├── data_prep.py         # Synthetic data generation
│   ├── optimizer.py         # OR-Tools optimization engine
│   └── visualization.py     # Chart utilities with dark/light support
├── sample_data/
│   ├── employees.csv        # 25 employees across 3 roles
│   ├── demand_forecast.csv  # 90 days of demand data
│   └── staff_data.csv       # 2,250 availability records
└── reports/
    └── example_report.pdf   # Sample optimization report
```

### 🎯 Features
- **Global Insights**: KPIs, demand analysis, role distribution
- **Schedule Optimizer**: AI-powered workforce optimization
- **Scenario Explorer**: Test different business scenarios
- **Dark/Light Theme**: Excellent readability in both modes
- **Interactive Charts**: Plotly visualizations with proper legends

### 🔧 Technical Stack
- **Streamlit**: Web application framework
- **OR-Tools**: Constraint programming optimization
- **Plotly**: Interactive visualizations
- **Pandas/NumPy**: Data processing
- **Matplotlib/Seaborn**: Additional plotting

## Post-Deployment

### ✅ Verification Checklist
- [ ] App loads without errors
- [ ] All 3 pages are accessible
- [ ] Charts render properly
- [ ] Dark/light theme switching works
- [ ] Optimization runs successfully
- [ ] Data loads correctly

### 🔗 Your App URL
Once deployed, your app will be available at:
`https://shiftwise-scheduling-dashboard.streamlit.app`

## Troubleshooting

### Common Issues
1. **Import errors**: Ensure all dependencies are in `requirements.txt`
2. **Data loading**: Check that CSV files are in the repository
3. **Theme issues**: Verify `.streamlit/config.toml` is present
4. **Memory issues**: The app uses synthetic data, should be fine

### Support
- Check the [Streamlit Cloud documentation](https://docs.streamlit.io/streamlit-community-cloud)
- Review the [GitHub repository](https://github.com/heritai/shiftwise-scheduling-dashboard) for code details

## 🎉 Success!
Your ShiftWise dashboard is now live and ready to demonstrate AI-powered workforce scheduling!
