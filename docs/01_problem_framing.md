
# Milestone 1: Problem Framing and Data Acquisition

## 1. Business Problem

Mwangaza MiniMart is a fictional Kenyan retail chain operating across eight counties. The business needs a better understanding of its sales performance, customer purchasing behaviour, and future product demand.

The project aims to identify high-performing and declining sales segments, understand customer purchasing patterns, examine promotional sales, and forecast future demand.

The findings will help demonstrate how data-driven decisions can support resource allocation, marketing strategies, and inventory planning.

## 2. Project Objectives

The project has four main objectives:

1. Analyse sales performance across stores, products, and time periods.
2. Identify customer purchasing patterns and customers who may be becoming inactive.
3. Examine the relationship between promotions and sales performance.
4. Develop and evaluate a machine learning model for monthly demand forecasting.

## 3. Business Questions and Success Measures

### Question 1: Sales Performance

Which stores and product categories generate the highest revenue, and how does sales performance change over time?

**Success measures:**
- Total sales revenue
- Total units sold
- Monthly revenue growth
- Revenue by store and product category

### Question 2: Customer Behaviour

Which customers purchase frequently, and which customers show signs of becoming inactive?

**Success measures:**
- Recency: time since the last purchase
- Frequency: number of purchases
- Monetary value: total customer spending
- Customer segments based on purchasing behaviour

### Question 3: Promotional Effectiveness

How do promotions relate to sales performance?

**Success measures:**
- Sales revenue during promotional and non-promotional transactions
- Average quantities sold
- Statistical tests and confidence intervals

These comparisons will not automatically establish that promotions caused changes in sales.

### Question 4: Demand Forecasting

Can historical sales data help predict monthly demand across stores and product categories?

**Success measures:**
- Mean Absolute Error (MAE)
- Comparison against a simple baseline forecast
- Performance on future periods excluded from model training

The forecasting model will be considered useful for this capstone if it outperforms the baseline on held-out data.

## 4. Project Scope

The analysis will use synthetic Kenyan retail transactions covering January 2024 to September 2026.

The project will also incorporate public county population data from the Kenya National Bureau of Statistics.

The analysis will cover data cleaning, exploratory data analysis, PostgreSQL analytics, statistical testing, machine learning, and Power BI visualization.

## 5. Limitations

The retail transactions are synthetic and do not represent actual customer purchases.

The 2019 county population figures provide historical context rather than current population estimates.

Consequently, findings and predictions will demonstrate analytical methods rather than establish real-world Kenyan retail trends.
