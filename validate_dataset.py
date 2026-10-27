"""Basic independent checks for the synthetic raw dataset. Run: python validate_dataset.py"""
from pathlib import Path
import json
import pandas as pd
import numpy as np

root=Path(__file__).resolve().parent
D=root/'data'/'raw'
orders=pd.read_csv(D/'orders.csv',parse_dates=['order_date','order_datetime'],dtype={'order_id':'string','store_id':'string','customer_id':'string'})
lines=pd.read_csv(D/'order_items.csv',dtype={'line_id':'string','order_id':'string','product_id':'string'})
customers=pd.read_csv(D/'customers.csv',dtype={'customer_id':'string'})
stores=pd.read_csv(D/'stores.csv')
products=pd.read_csv(D/'products.csv')
pop=pd.read_csv(D/'county_population_2019_knbs.csv')
assert orders.order_id.is_unique
assert customers.customer_id.is_unique
assert stores.store_id.is_unique
assert products.product_id.is_unique
assert pop.county.is_unique
assert orders.store_id.isin(stores.store_id).all()
assert lines.order_id.isin(orders.order_id).all()
assert lines.product_id.isin(products.product_id).all()
assert orders.customer_id.dropna().isin(customers.customer_id).all()
assert stores.county.isin(pop.county).all()
assert (orders.order_date.dt.year>=2024).all() and orders.order_date.max()==pd.Timestamp('2026-09-30')
assert orders.order_date.min()==pd.Timestamp('2024-01-01')
assert (orders.gross_amount_kes-orders.discount_amount_kes-orders.net_amount_kes).abs().max()<0.011
assert orders.net_amount_kes.gt(0).all()
opening=stores.set_index('store_id').opening_date
assert (orders.order_date >= pd.to_datetime(orders.store_id.map(opening))).all()
# Remove duplicate raw line IDs before reconciliation, without changing their monetary amounts.
dedup=lines.drop_duplicates('line_id')
rec=dedup.groupby('order_id',sort=False)[['line_gross_kes','line_discount_kes','line_net_kes']].sum()
left=orders.set_index('order_id')[['gross_amount_kes','discount_amount_kes','net_amount_kes']]
difference=(rec.to_numpy()-left.loc[rec.index].to_numpy())
assert np.max(np.abs(difference))<0.011, 'Reference sums should reconcile once exact duplicate lines are removed'
assert (dedup.line_gross_kes-dedup.line_discount_kes-dedup.line_net_kes).abs().max()<0.011
actual={
 'orders':len(orders),'item_rows_raw':len(lines),'unique_line_ids':dedup.line_id.nunique(),
 'duplicate_line_ids':int(lines.line_id.duplicated().sum()),
 'missing_item_unit_price':int(lines.unit_price_kes.isna().sum()),
 'large_quantity_at_least_49':int(lines.quantity.ge(49).sum()),
 'blank_payment_method':int(orders.payment_method.isna().sum()),
 'blank_customer_age_band':int(customers.age_band.isna().sum()),
 'blank_customer_id_guest_checkout':int(orders.customer_id.isna().sum()),
 'date_range':[str(orders.order_date.min().date()),str(orders.order_date.max().date())],
 'total_net_sales_kes':float(np.round(orders.net_amount_kes.sum(),2))
}
print(json.dumps(actual,indent=2))
