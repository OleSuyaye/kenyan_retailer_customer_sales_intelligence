-------------- MILESTONE 4: SQL ANALYTICS---------------
----4.1 CREATING TABLES

SELECT current_database()

-- Create orders table 
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    store_id TEXT,
    order_datetime TIMESTAMP,
    customer_id TEXT,
    channel TEXT,
    payment_method TEXT,
    order_date DATE,
    item_units INTEGER,
    gross_amount_kes NUMERIC(12,2),
    discount_amount_kes NUMERIC(12,2),
    net_amount_kes NUMERIC(12,2),
    promotion_applied BOOLEAN,
    year INTEGER,
    month INTEGER,
    year_month TEXT
);

-- Create customers table 
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    registration_date DATE,
    home_county TEXT,
    preferred_store_id TEXT,
    age_band TEXT,
    acquisition_channel TEXT
);

-- Create a table to store purchased items
CREATE TABLE order_items (
    line_id TEXT PRIMARY KEY,
    order_id TEXT,
    product_id TEXT,
    quantity INTEGER,
    unit_price_kes NUMERIC(12,2),
    unit_cost_kes NUMERIC(12,2),
    discount_pct INTEGER,
    line_gross_kes NUMERIC(12,2),
    line_discount_kes NUMERIC(12,2),
    line_net_kes NUMERIC(12,2)
);

-- Create a table to store product information
CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    category TEXT,
    product_name TEXT,
    base_list_price_kes INTEGER,
    base_unit_cost_kes NUMERIC(12,2),
    is_perishable BOOLEAN,
    is_active BOOLEAN
);

-- Create a table to store retail branches
CREATE TABLE stores (
    store_id TEXT PRIMARY KEY,
    store_name TEXT,
    county TEXT,
    town TEXT,
    opening_date DATE,
    store_format TEXT
);

-- Create a table for county population data
CREATE TABLE county_population_2019_knbs (
    county TEXT PRIMARY KEY,
    census_year INTEGER,
    population_2019 INTEGER,
    source TEXT,
    source_url TEXT
);


-- Check record counts for all six tables

SELECT
    (SELECT COUNT(*) FROM stores) AS stores,
    (SELECT COUNT(*) FROM products) AS products,
    (SELECT COUNT(*) FROM customers) AS customers,
    (SELECT COUNT(*) FROM county_population_2019_knbs) AS county_population,
    (SELECT COUNT(*) FROM orders) AS orders,
    (SELECT COUNT(*) FROM order_items) AS order_items;

-- Verify total revenue and quantities after importing

SELECT
    (SELECT SUM(net_amount_kes) FROM orders) AS orders_revenue,
    (SELECT SUM(line_net_kes) FROM order_items) AS items_revenue,
    (SELECT SUM(item_units) FROM orders) AS orders_units,
    (SELECT SUM(quantity) FROM order_items) AS items_units;

----4.2 SQL ANALYTICS
----4.2.1 Joins
-----Q1. Which stores generated highest revenues?

SELECT
    s.store_name,
    SUM(o.net_amount_kes) AS total_revenue
FROM orders o
JOIN stores s
    ON o.store_id = s.store_id
GROUP BY s.store_name
ORDER BY total_revenue DESC;

-----Q2. Which product categories generate the highest revenue?
SELECT
    p.category,
    SUM(oi.line_net_kes) AS total_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

----4.2.2 Window Functions and Aggregations
-----Q3. Rank stores based on total sales revenue

SELECT
    s.store_name,
    SUM(o.net_amount_kes) AS total_revenue,
    RANK() OVER (
        ORDER BY SUM(o.net_amount_kes) DESC
    ) AS revenue_rank
FROM orders o
JOIN stores s
    ON o.store_id = s.store_id
GROUP BY s.store_name
ORDER BY revenue_rank;

----4.2.3 Customer Cohort Analysis
-----Q4. How many customers made their first purchase each month?

WITH first_purchases AS (
    SELECT
        customer_id,
        MIN(order_date) AS first_order_date
    FROM orders
    WHERE customer_id IS NOT NULL
  	AND TRIM(customer_id) <> ''
    GROUP BY customer_id
)
SELECT
    TO_CHAR(first_order_date, 'YYYY-MM') AS cohort_month,
    COUNT(*) AS new_customers
FROM first_purchases
GROUP BY cohort_month
ORDER BY cohort_month;

---- Q5. How many customers returned the following month?

WITH first_purchases AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) AS cohort_month
    FROM orders
    WHERE customer_id IS NOT NULL
    AND TRIM(customer_id) <> ''
    GROUP BY customer_id
)
SELECT
    TO_CHAR(f.cohort_month, 'YYYY-MM') AS cohort_month,
    COUNT(DISTINCT f.customer_id) AS total_customers,
    COUNT(DISTINCT o.customer_id) AS returned_customers,
    ROUND(
        COUNT(DISTINCT o.customer_id) * 100.0 /
        COUNT(DISTINCT f.customer_id), 2
    ) AS retention_pct
FROM first_purchases f
LEFT JOIN orders o
    ON f.customer_id = o.customer_id
    AND DATE_TRUNC('month', o.order_date) =
        f.cohort_month + INTERVAL '1 month'
WHERE f.cohort_month < '2026-09-01'
GROUP BY f.cohort_month
ORDER BY f.cohort_month;


---- 4.2.4 RFM Customer Segmentation
-----Q6. Calculate recency, frequency and monetary value

SELECT
    customer_id,
    DATE '2026-09-30' - MAX(order_date) AS recency,
    COUNT(order_id) AS frequency,
    SUM(net_amount_kes) AS monetary
FROM orders
WHERE customer_id IS NOT NULL
AND TRIM(customer_id) <> ''
GROUP BY customer_id
ORDER BY monetary DESC
LIMIT 10;


---- Q7. Segment customers using RFM values

WITH rfm AS (
    SELECT
        customer_id,
        DATE '2026-09-30' - MAX(order_date) AS recency,
        COUNT(order_id) AS frequency,
        SUM(net_amount_kes) AS monetary
    FROM orders
    WHERE customer_id IS NOT NULL
    AND TRIM(customer_id) <> ''
    GROUP BY customer_id
)
SELECT
    customer_id,
    recency,
    frequency,
    monetary,
    CASE
        WHEN recency > 90 THEN 'At Risk'
        WHEN recency <= 30 AND frequency >= 20
             AND monetary >= 20000 THEN 'High Value'
        WHEN recency <= 60 AND frequency >= 5 THEN 'Regular'
        ELSE 'Other'
    END AS customer_segment
FROM rfm
ORDER BY monetary DESC
LIMIT 10;

-- Q8. Count customers in each RFM segment

WITH rfm AS (
    SELECT
        customer_id,
        DATE '2026-09-30' - MAX(order_date) AS recency,
        COUNT(order_id) AS frequency,
        SUM(net_amount_kes) AS monetary
    FROM orders
    WHERE customer_id IS NOT NULL
      AND TRIM(customer_id) <> ''
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN recency > 90 THEN 'At Risk'
        WHEN recency <= 30 AND frequency >= 20
             AND monetary >= 20000 THEN 'High Value'
        WHEN recency <= 60 AND frequency >= 5 THEN 'Regular'
        ELSE 'Other'
    END AS customer_segment,
    COUNT(*) AS total_customers
FROM rfm
GROUP BY customer_segment
ORDER BY total_customers DESC;

