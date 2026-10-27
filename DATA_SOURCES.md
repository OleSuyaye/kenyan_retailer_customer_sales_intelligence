
# Data Sources and Usage

## 1. Synthetic Retail Dataset

- **Source:** Generated specifically for this capstone project.
- **Retailer:** Mwangaza MiniMart (fictional Kenyan retail chain).
- **Contents:** Customers, stores, products, transactions, quantities, prices, promotions, and payment methods.
- **Period:** January 2024 – September 2026.
- **Usage:** Educational and portfolio purposes.
- **Limitation:** The transactions are synthetic and do not represent actual Kenyan retail purchases.

## 2. KNBS County Population Data

- **Source:** Kenya National Bureau of Statistics (KNBS).
- **Publication:** 2019 Kenya Population and Housing Census, Volume I.
- **Contents:** Population figures by county.
- **Usage terms:** Verify the applicable licence and redistribution conditions before public distribution.
- **Reference:** [KNBS Census Publication](https://repository.knbs.or.ke/handle/knbs-ke-repo/385)
- **Limitation:** The 2019 population figures provide historical context and do not represent 2024–2026 population estimates.

## 3. Data Integration

The synthetic retail dataset includes store locations across Kenyan counties.

County population data will be joined to the retail dataset using the county field.

This will allow us to explore relationships between store performance and county population size.

Because the retail data is synthetic, any identified relationships will be illustrative rather than evidence of actual Kenyan consumer behaviour.
