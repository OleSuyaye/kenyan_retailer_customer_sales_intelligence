
# Customer and Sales Intelligence for a Kenyan Retailer

## Project Overview

This project analyses sales and customer behaviour for Mwangaza MiniMart, a fictional Kenyan retail chain. It uses Python, PostgreSQL, machine learning and Power BI to support retail business decisions.

The project investigates sales trends, store and product performance, customer retention, purchasing behaviour and future demand.

## Dataset

The project uses a synthetic retail dataset covering January 2024 to September 2026.

- 10 stores across 8 Kenyan counties
- 19,000 registered customers
- 99 products
- 316,277 orders
- 823,772 cleaned order-item records

The project also includes county population data from the 2019 Kenya Population and Housing Census.

All data sources, limitations and usage information are documented in `DATA_SOURCES.md`.

**Note:** Retail transactions are synthetic and do not represent actual purchases.

## Tools Used

- Python: pandas, matplotlib, SciPy and scikit-learn
- PostgreSQL and DBeaver: SQL analytics
- Power BI Desktop: Interactive dashboard
- Git and GitHub: Version control

## Project Structure

- `data/raw/` — Original datasets
- `data/processed/` — Cleaned datasets and October forecast
- `notebooks/` — Cleaning, EDA, statistical analysis and forecasting
- `sql/` — Database schema, analytical queries and results
- `dashboard/` — Power BI report and screenshots
- `docs/` — Project documentation
- `requirements.txt` — Python dependencies

## How to Run the Project

### 1. Clone the Repository

```powershell
git clone https://github.com/OleSuyaye/kenyan_retailer_customer_sales_intelligence.git
cd kenyan_retailer_customer_sales_intelligence
```

### 2. Set Up Python

Python 3.13 was used during development.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 3. Run the Jupyter Notebooks

Open the project in VS Code and select the `.venv` Python kernel.

Run the notebooks in this order:

1. `01_data_cleaning.ipynb` — Clean and validate datasets.
2. `02_exploratory_data_analysis.ipynb` — Analyse sales trends, stores, products and customers.
3. `03_statistical_analysis.ipynb` — Perform hypothesis tests and confidence intervals.
4. `04_demand_forecasting.ipynb` — Train and evaluate a demand forecasting model.

The notebooks use relative paths to the `data/` folder and were developed with the `notebooks/` directory as the working directory.

### 4. Run SQL Analytics

1. Install PostgreSQL and DBeaver.
2. Create a database named `kenya_retail_capstone`.
3. Open `sql/01_schema_and_analysis.sql`.
4. Execute the table creation statements.
5. Import the six cleaned CSV datasets from `data/processed/` into their corresponding tables using DBeaver.
6. Run the analytical queries.

Previously exported SQL results are available in `sql/results/`.

### 5. Open the Power BI Dashboard

Open:

`dashboard/Mwangaza_MiniMart_Dashboard.pbix`

The report contains two pages:

- Performance
- Customer and Demand Forecast

If opening the report on another computer, update the CSV source paths through Power Query to match the new project location.

Dashboard screenshots are available in `dashboard/screenshots/`.

## Main Findings

- Total retail revenue was approximately KES 253.97 million.
- Ngara was the highest-revenue store.
- Staples generated the most product-category revenue.
- Customer segmentation identified 4,250 at-risk customers and 1,814 high-value customers.
- Promotional orders had significantly higher average values, although this does not establish causation.
- M-Pesa and other payment methods showed no statistically significant difference in average order value.

## Demand Forecasting

A Random Forest model was trained using previous monthly sales and calendar-month information.

The model was compared with a previous-month baseline using time-based training, validation and testing.

On the test dataset:

| Metric | Baseline | Random Forest |
|---|---:|---:|
| MAE | 455.37 | 264.55 |
| RMSE | 507.15 | 322.30 |

The model forecast **50,136 units** across 10 stores for October 2026.

Forecasts estimate future units sold, not necessarily total customer demand when stock shortages occur.

## Business Recommendations

1. Investigate the causes of underperformance in lower-revenue stores.
2. Prioritise retention campaigns for customers identified as at risk.
3. Use seasonal sales patterns to support inventory planning.
4. Use demand forecasts alongside stock availability and operational information when planning purchases.

## Limitations

- Retail transactions were synthetically generated.
- The population data is historical.
- Observed differences in sales do not prove causation.
- Forecasts can be inaccurate during unexpected changes in demand.

## Dashboard and Results

See `dashboard/screenshots/` for report previews and `sql/results/` for exported SQL results.

