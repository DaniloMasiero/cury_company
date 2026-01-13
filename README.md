# 1. Business Problem
Cury Company is a technology company that created an application connecting restaurants, delivery drivers, and customers.

Through this application, customers can order meals from any registered restaurant and receive them at home through a delivery driver also registered in the Cury Company app.

The company facilitates transactions between restaurants, delivery drivers, and customers, generating vast amounts of data about deliveries, order types, weather conditions, driver ratings, and more. Despite growing delivery volumes, the CEO lacks complete visibility into the company's growth KPIs.

You were hired as a Data Scientist to create data solutions for deliveries. However, before training algorithms, the company needs to have the main strategic KPIs organized in a single tool, allowing the CEO to make simple yet important decisions.

Cury Company operates a Marketplace business model, intermediating business between three main customers: restaurants, delivery drivers, and buyers. To track business growth, the CEO wants to see the following growth metrics:
  
## Company Perspective:

1. Number of orders per day
2. Number of orders per week
3. Distribution of orders by traffic type
4. Comparison of order volume by city and traffic type
5. Number of orders per delivery driver per week
6. Central location of each city by traffic type

## Delivery Driver Perspective:

1. Youngest and oldest delivery driver age
2. Worst and best vehicle condition
3. Average rating per delivery driver
4. Average rating and standard deviation by traffic type
5. Average rating and standard deviation by weather conditions
6. Top 10 fastest delivery drivers by city
7. Top 10 slowest delivery drivers by city

## Restaurant Perspective:

1. Number of unique delivery drivers
2. Average distance between restaurants and delivery locations
3. Average delivery time and standard deviation by city
4. Average delivery time and standard deviation by city and order type
5. Average delivery time and standard deviation by city and traffic type
5. Average delivery time during festivals

The goal of this project is to create a set of graphs and/or tables that display these metrics in the best possible way for the CEO.

# 2. Assumptions for Analysis

1. Analysis was performed with data between 02/11/2022 and 04/06/2022
2. Marketplace was the assumed business model
3. The 3 main business views were: Order transaction view, restaurant view, and delivery driver view

# 3. Solution Strategy

The strategic dashboard was developed using metrics reflecting the company's 3 main business model views:

1. Company growth view
2. Restaurant growth view
3. Delivery driver growth view

Each view is represented by the following set of metrics
  
1. Company Growth View  
  1.1. Orders per day  
  1.2. Percentage of orders by traffic conditions  
  1.3. Number of orders by type and city  
  1.4. Orders per week  
  1.5. Number of orders by delivery type  
  1.6. Number of orders by traffic conditions and city type  
  
2. Restaurant Growth View  
  2.1. Number of unique orders  
  2.2. Average distance traveled  
  2.3. Average delivery time during festivals and normal days  
  2.4. Standard deviation of delivery time during festivals and normal days  
  2.5. Average delivery time by city  
  2.6. Distribution of average delivery time by city  
  2.7. Average delivery time by order type  
  
3. Delivery Driver Growth View  
  3.1. Age of oldest and youngest delivery driver  
  3.2. Rating of best and worst vehicle  
  3.3. Average rating per delivery driver  
  3.4. Average rating by traffic conditions  
  3.5. Average rating by weather conditions  
  3.6. Average time of fastest delivery driver  
  3.7. Average time of fastest delivery driver by city  

# 4. Top 3 Data Insights

1. Order quantity seasonality is daily. There's approximately a 10% variation in the number of orders on consecutive days.
2. Semi-Urban cities don't have low traffic conditions.
3. The largest variations in delivery time occur during sunny weather.

# 5. Final Project Deliverable
Online dashboard, hosted in the Cloud and available for access on any internet-connected device.

The dashboard can be accessed through this link: [https://project-curry-company.streamlit.app/](https://danilo-masiero-projects-cury-company.streamlit.app/)

# 6. Conclusion
  The goal of this project is to create a set of graphs and/or tables that display these metrics in the best possible way for the CEO.
  
  From the Company view, we can conclude that the number of orders grew between week 06 and week 13 of 2022.
  
# 7. Next Steps
1. Reduce the number of metrics
2. Create new filters
3. Add new business views
