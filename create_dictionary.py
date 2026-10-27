from pathlib import Path
import pandas as pd
D=Path(__file__).resolve().parent
spec={
 'stores.csv':{
 'store_id':('text','Fictional branch identifier','Primary key'),
 'store_name':('text','Fictional retail branch name','Not a real business'),
 'county':('text','Real Kenyan county name of fictional branch','Join to 2019 census county reference'),
 'town':('text','Town/neighbourhood','Fictional branch placement'),
 'opening_date':('date YYYY-MM-DD','Simulated branch opening','No receipts should precede this date'),
 'store_format':('text','Retail branch format','All currently neighbourhood minimarkets')},
 'products.csv':{
 'product_id':('text','Fictional SKU identifier','Primary key'),
 'category':('text','Retail category grouping','Dimension'),
 'product_name':('text','Generic product and package size','Synthetic SKU label'),
 'base_list_price_kes':('decimal','Simulation reference price in KES','Not a observed Kenyan shop price'),
 'base_unit_cost_kes':('decimal','Simulation reference purchase cost in KES','Not actual supplier cost'),
 'is_perishable':('boolean','Whether item is classed as perishable','Invented designation'),
 'is_active':('boolean','Product catalogue status','All true in this version')},
 'customers.csv':{
 'customer_id':('text','Invented loyalty member ID','Primary key; no personal identifier'),
 'registration_date':('date YYYY-MM-DD','Simulated date registered','Must be on/before known-customer purchase'),
 'home_county':('text','Simulated home county','Same as preferred branch county'),
 'preferred_store_id':('text','Preferred branch','FK stores.store_id'),
 'age_band':('text; nullable','Invented age group','Some genuine raw blanks for cleaning'),
 'acquisition_channel':('text','Invented registration acquisition channel','Categorical')},
 'orders.csv':{
 'order_id':('text','Synthetic receipt ID','Primary key; unique'),
 'store_id':('text','Branch processing purchase','FK stores.store_id'),
 'order_datetime':('datetime YYYY-MM-DD HH:MM:SS','Local Kenya wall-clock time of purchase','EAT UTC+03, no explicit offset stored'),
 'customer_id':('text; nullable','Loyalty ID, blank for guest checkout','Not all blanks are errors; FK if nonblank'),
 'channel':('text','In-store, delivery or click-and-collect','Dimension'),
 'payment_method':('text; nullable','M-Pesa, cash, cards or bank transfer','Some unintended blank values for cleaning'),
 'order_date':('date YYYY-MM-DD','Purchase date extracted from timestamp','Useful for date joins and time-series'),
 'item_units':('integer','Total physical units on receipt','Based on pristine line items, before raw errors injected'),
 'gross_amount_kes':('decimal','Receipt sales before discount','Sum pristine item line_gross_kes'),
 'discount_amount_kes':('decimal','Receipt discount amount','Sum pristine item line_discount_kes'),
 'net_amount_kes':('decimal','Receipt revenue after discount','gross_amount minus discount_amount'),
 'promotion_applied':('boolean','Any receipt line had an applied discount','Discount does not prove causal impact')},
 'order_items.csv':{
 'line_id':('text','Receipt line ID','Intended PK after removing intentionally duplicated rows'),
 'order_id':('text','Receipt parent','FK orders.order_id'),
 'product_id':('text','Product bought','FK products.product_id'),
 'quantity':('integer','Units purchased on that line','Some intentional extreme entry mistakes'),
 'unit_price_kes':('decimal; nullable','Gross price per unit before line discount','Some artificial missing values'),
 'unit_cost_kes':('decimal','Estimated unit acquisition cost','Synthetic figure'),
 'discount_pct':('integer','Discount percentage 0, 5, 10, or 15','Not causal effect'),
 'line_gross_kes':('decimal','Pre-discount quantity times price','Retains correct value before injected raw errors'),
 'line_discount_kes':('decimal','Gross times discount percentage / 100','Retains correct value before injected raw errors'),
 'line_net_kes':('decimal','Gross less discount','Retains correct value before injected raw errors')},
 'county_population_2019_knbs.csv':{
 'county':('text','Real county name','PK; join to stores.county'),
 'census_year':('integer','Census reference year','2019; do not treat as 2026 census'),
 'population_2019':('integer','KNBS enumerated county population in 2019','Real contextual data, distinct from synthetic sales'),
 'source':('text','Statistical source publisher and dataset','Attribution'),
 'source_url':('url','Official KNBS source URL','Attribution / licence verification')}
}
rows=[]
for fname,fields in spec.items():
 for col,(dtype,description,note) in fields.items():rows.append([fname,col,dtype,description,note])
pd.DataFrame(rows,columns=['file','column','suggested_data_type','description','notes']).to_csv(D/'data_dictionary.csv',index=False)
