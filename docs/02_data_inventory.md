
# Milestone 1: Data Inventory

## 1. Dataset Overview

The project uses six CSV files covering synthetic retail transactions and real public population data.

The retail data represents Mwangaza MiniMart, a fictional chain with 10 stores across eight Kenyan counties.

The transactions cover January 2024 to September 2026.

## 2. Data Inventory

| Dataset | Records | Primary Identifier | Purpose |
|---|---:|---|---|
| customers.csv | 19,000 | customer_id | Customer information and purchasing profiles |
| stores.csv | 10 | store_id | Store locations and counties |
| products.csv | 99 | product_id | Product details and categories |
| orders.csv | 316,277 | order_id | Purchase dates, payments, and sales totals |
| order_items.csv | 824,761 | line_id | Purchased products, quantities, prices, and discounts |
| county_population_2019_knbs.csv | 8 | county | Historical county population context |

Note: The raw order_items.csv contains intentional duplicate records, so line_id is not unique until cleaning.

## 3. Data Sources

### Synthetic Retail Data

- Source: Python-generated dataset.
- Generation method: Reproducible simulation using a fixed random seed.
- Usage: Educational capstone project.
- Limitations: Fictional transactions, not real customer purchases.

### Public Population Data

- Source: Kenya National Bureau of Statistics (KNBS).
- Publication: 2019 Kenya Population and Housing Census.
- Licence: CC BY-NC-SA 4.0.
- Usage: Historical population context for the eight counties.
- Reference: https://www.knbs.or.ke/reports/kenya-census-2019/

## 4. Dataset Relationships

- orders.customer_id connects to customers.customer_id.
- orders.store_id connects to stores.store_id.
- order_items.order_id connects to orders.order_id.
- order_items.product_id connects to products.product_id.
- stores.county connects to county_population_2019_knbs.county.

## 5. Business Questions Supported

1. Sales performance: orders, order_items, products, and stores.
2. Customer behaviour: customers and orders.
3. Promotional analysis: orders and order_items.
4. Demand forecasting: orders, order_items, products, and stores.

The KNBS population dataset provides additional geographical context.

## 6. Data Limitations

The retail dataset is synthetic. It contains deliberately introduced missing values, duplicate records, and unusual quantities for data-cleaning practice.

Blank customer IDs can represent guest purchases and are not automatically errors.

The KNBS population data refers to 2019 and must not be interpreted as current population figures.

## 7. Dataset Generation and Validation

### What Was Built

A synthetic Kenyan retail dataset containing six related CSV files was prepared for the capstone.

The dataset includes customers, stores, products, orders, order items, and public county population data.

### How It Works

The retail transactions were generated using Python scripts. The data contains historical sales, customer purchases, payment methods, promotions, and store locations.

The six CSV files are connected through identifiers such as customer_id, order_id, product_id, and store_id.

### How It Was Tested

The dataset was examined using validate_dataset.py.

The script reported:

- 316,277 orders
- 824,761 transaction item rows
- 989 duplicate line IDs
- 1,648 missing unit prices
- 791 missing payment methods
- 412 unusually large quantities
- 69,853 guest checkout records
- Sales period: January 2024 to September 2026
- Reported net sales: KES 253,971,298.29

The validation script executed successfully.

The identified data-quality issues will be investigated and addressed during Milestone 2: Data Cleaning and Preparation.
