# Food Delivery Marketplace Analytics Dashboard

**Live Dashboard:** [View Here](https://danilo-masiero-projects-cury-company.streamlit.app/)

## Overview
Interactive analytics dashboard analyzing 2+ months of delivery operations data for a food marketplace platform in India, featuring metrics across company operations, restaurant performance, and delivery driver efficiency.

*Note: This is a portfolio project using synthetic data to demonstrate data analysis and dashboard development skills.*

## Problem Statement
Food delivery marketplaces generate massive amounts of operational data, but without proper visualization, executives struggle to make data-driven decisions. This project addresses that gap by creating an executive dashboard that tracks KPIs across three stakeholder perspectives: company operations, restaurants, and delivery drivers.

## Tech Stack
- **Python**: Data processing and analysis
- **Pandas**: Data manipulation
- **Plotly/Streamlit**: Interactive visualizations and dashboard
- **Cloud Hosting**: Streamlit Cloud

## Key Features
- **Multi-perspective analysis**: Company, restaurant, and driver views
- **Real-time filtering**: By date, city, traffic conditions, weather
- **Interactive visualizations**: time series, maps, distributions
- **Performance metrics**: Delivery times, ratings, order volumes

## Data & Methodology
- **Dataset**: 45,593 delivery records (Feb-Apr 2022)
- **Key variables**: Order timing, location, traffic conditions, weather, ratings, delivery times
- **Data cleaning**: Remove spaces, transformation column type, str extraction

## Key Insights

1. **Operational Efficiency Opportunity**
   - Delivery times show 25% higher variance during sunny weather
   - Recommendation: Investigate route optimization during peak sun hours

2. **Market Segmentation Finding**
   - Semi-urban areas never experience low traffic conditions
   - Impact: Different delivery time SLAs needed for urban vs. semi-urban zones

3. **Demand Patterns**
   - Daily order volumes show ~10% consecutive-day variation
   - Application: Predictive staffing models could reduce driver idle time

## Business Impact
- Enables data-driven decisions on driver allocation
- Identifies underperforming areas for operational improvement
- Provides benchmarking metrics for delivery performance

## Future Improvements
- Add predictive analytics for demand forecasting
- Integrate real-time data updates
- Include cost analysis and profitability metrics
- Add A/B testing framework for operational experiments

## Contact
[LinkedIn](https://www.linkedin.com/in/danilo-masiero/) | [Email](danilomls3@gmail.com) | [Portfolio](https://danilomasiero.github.io/portfolio/)
