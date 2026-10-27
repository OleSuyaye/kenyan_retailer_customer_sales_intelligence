"""Reproducible synthetic Kenyan minimarket retail dataset (NOT real transactions).

Dependency: numpy, pandas. Run: python generate_dataset.py
All records, except separately attributed 2019 county population counts, are invented.
"""
from pathlib import Path
from datetime import timedelta
import json
import numpy as np
import pandas as pd

SEED = 20261027
rng = np.random.default_rng(SEED)
ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)
START = pd.Timestamp('2024-01-01')
END = pd.Timestamp('2026-09-30')

# Fictional company, branches, products, customers and sales.
branch_specs = [
    ('S001', 'Mwangaza MiniMart - Ngara', 'Nairobi', 'Ngara', '2024-01-01', 'Neighbourhood', 1.15),
    ('S002', 'Mwangaza MiniMart - South B', 'Nairobi', 'South B', '2024-01-01', 'Neighbourhood', 1.12),
    ('S003', 'Mwangaza MiniMart - Thika', 'Kiambu', 'Thika', '2024-01-01', 'Neighbourhood', 1.00),
    ('S004', 'Mwangaza MiniMart - Nakuru', 'Nakuru', 'Nakuru', '2024-01-01', 'Neighbourhood', 1.07),
    ('S005', 'Mwangaza MiniMart - Nyali', 'Mombasa', 'Nyali', '2024-01-01', 'Neighbourhood', 1.08),
    ('S006', 'Mwangaza MiniMart - Kisumu', 'Kisumu', 'Kisumu', '2024-01-01', 'Neighbourhood', 0.94),
    ('S007', 'Mwangaza MiniMart - Ruiru', 'Kiambu', 'Ruiru', '2025-02-01', 'Neighbourhood', 1.02),
    ('S008', 'Mwangaza MiniMart - Athi River', 'Machakos', 'Athi River', '2025-06-01', 'Neighbourhood', 0.98),
    ('S009', 'Mwangaza MiniMart - Eldoret', 'Uasin Gishu', 'Eldoret', '2026-01-01', 'Neighbourhood', 1.04),
    ('S010', 'Mwangaza MiniMart - Kitengela', 'Kajiado', 'Kitengela', '2026-04-01', 'Neighbourhood', 0.98),
]
stores = pd.DataFrame(branch_specs, columns=['store_id','store_name','county','town','opening_date','store_format','relative_footfall_factor'])
stores.drop(columns=['relative_footfall_factor']).to_csv(DATA/'stores.csv', index=False)

# Names and price assumptions are designed for the exercise, not observed market prices.
category_catalogue = {
 'Staples': [('Maize Flour 2kg',168),('Rice 1kg',215),('Rice 2kg',420),('Wheat Flour 2kg',188),('Sugar 1kg',175),('Dry Beans 1kg',225),('Green Grams 1kg',260),('Porridge Flour 1kg',168),('Spaghetti 500g',145),('Cooking Oil 1L',305),('Salt 1kg',55),('Breakfast Cereal 500g',395)],
 'Fresh Produce': [('Tomatoes 1kg',140),('Onions 1kg',165),('Sukuma Wiki Bunch',45),('Spinach Bunch',50),('Potatoes 2kg',260),('Bananas 1kg',125),('Oranges 1kg',180),('Avocado Each',65),('Carrots 1kg',130),('Cabbage Each',115),('Mangoes 1kg',175),('Watermelon 1kg',110)],
 'Dairy & Eggs': [('Fresh Milk 500ml',75),('Fresh Milk 1L',150),('Mala 500ml',105),('Plain Yoghurt 500ml',170),('Flavoured Yoghurt 250ml',95),('Cheese 200g',340),('Eggs Tray 6',125),('Eggs Tray 12',240),('Butter 250g',335),('Margarine 500g',285)],
 'Bakery & Snacks': [('Sliced Bread 400g',75),('Brown Bread 400g',85),('Mandazi Pack 4',100),('Biscuits 200g',105),('Biscuits 400g',195),('Groundnuts 200g',145),('Potato Crisps 125g',155),('Popcorn 100g',105),('Cookies 200g',195),('Cake Slice',115)],
 'Beverages': [('Black Tea 100g',145),('Black Tea 250g',310),('Instant Coffee 50g',260),('Instant Coffee 100g',480),('Drinking Water 500ml',45),('Drinking Water 1.5L',85),('Fruit Juice 1L',210),('Soda 500ml',80),('Soda 1.25L',155),('Malted Drink 500g',395),('Energy Drink 250ml',145)],
 'Personal Care': [('Bath Soap 175g',95),('Toothpaste 100ml',175),('Toothbrush Each',115),('Body Lotion 200ml',285),('Shampoo 250ml',335),('Deodorant 150ml',315),('Sanitary Pads 8 Pack',125),('Tissues 2 Rolls',115),('Petroleum Jelly 200ml',215),('Hand Sanitiser 250ml',190)],
 'Household': [('Laundry Powder 500g',175),('Laundry Powder 1kg',330),('Dishwashing Liquid 500ml',210),('Bleach 500ml',140),('Toilet Cleaner 500ml',250),('Floor Cleaner 1L',330),('Washing Bar Soap',110),('Bin Liners Pack 10',175),('Kitchen Paper Roll',130),('Matches Pack 10',80)],
 'Meat & Fish': [('Beef 500g',390),('Chicken 500g',435),('Tilapia 500g',425),('Sausages Pack 6',345),('Minced Beef 500g',440),('Frozen Fish Fillet 500g',520),('Chicken Wings 500g',370),('Beef Sausages 500g',410)],
 'Stationery': [('Exercise Book 96 Page',65),('Exercise Book 200 Page',125),('Ballpoint Pen Pack 3',90),('Pencil Pack 3',65),('Ruler 30cm',65),('Glue Stick',100),('Drawing Book',155),('Notebook A5',185)],
 'Baby Care': [('Diapers Small Pack',520),('Baby Wipes 80 Pack',245),('Baby Soap 100g',135),('Baby Lotion 200ml',320),('Infant Cereal 250g',385),('Baby Shampoo 200ml',315),('Baby Powder 200g',225),('Diaper Cream 100g',345)]
}
items_catalog = [(cat,name,price) for cat, entries in category_catalogue.items() for name, price in entries]
products = pd.DataFrame(items_catalog, columns=['category','product_name','base_list_price_kes'])
products.insert(0,'product_id', [f'P{i:04d}' for i in range(1,len(products)+1)])
products['base_unit_cost_kes'] = np.round(products.base_list_price_kes.to_numpy() * rng.uniform(.66,.83,len(products)),2)
products['is_perishable'] = products.category.isin(['Fresh Produce','Meat & Fish','Dairy & Eggs','Bakery & Snacks'])
products['is_active'] = True
products.to_csv(DATA/'products.csv', index=False)

# Source: Kenya National Bureau of Statistics (2019 census); county-level counts only.
county_counts = {
 'Nairobi':4397073,'Kiambu':2417735,'Nakuru':2162202,'Mombasa':1208333,
 'Kisumu':1155574,'Machakos':1421932,'Uasin Gishu':1163186,'Kajiado':1117840,
}
context = pd.DataFrame([{'county':k,'census_year':2019,'population_2019':v,
                        'source':'KNBS 2019 Kenya Population and Housing Census',
                        'source_url':'https://www.knbs.or.ke/reports/kenya-census-2019/'} for k,v in county_counts.items()])
context.to_csv(DATA/'county_population_2019_knbs.csv',index=False)

# Customers are invented pseudonymous IDs, never personal data.
customers_per_store = 1900
customer_rows = []
for b in branch_specs:
    sid,_,county,_,opening,_,_ = b
    op = pd.Timestamp(opening)
    # Existing branches may have people sign up just before the analysed period.
    first_reg = max(pd.Timestamp('2023-09-01'),op-pd.Timedelta(days=75))
    last_reg = END-pd.Timedelta(days=6)
    reg_days = rng.integers(0, (last_reg-first_reg).days+1, size=customers_per_store)
    reg_dates = first_reg + pd.to_timedelta(reg_days, unit='D')
    ages = rng.choice(['18-24','25-34','35-44','45-54','55+'], size=customers_per_store,
                      p=[.18,.33,.24,.16,.09])
    sources = rng.choice(['In-store signup','Referral','Social media','Website'], size=customers_per_store,
                         p=[.52,.25,.15,.08])
    for j in range(customers_per_store):
        customer_rows.append([f'C{len(customer_rows)+1:06d}',str(reg_dates[j].date()),county,sid,ages[j],sources[j]])
customers = pd.DataFrame(customer_rows,columns=['customer_id','registration_date','home_county','preferred_store_id','age_band','acquisition_channel'])
customers.to_csv(DATA/'customers.csv',index=False)  # rewritten below after controlled missingness

# Branch and calendar dependent demand; explicitly made-up behavioural patterns.
order_partitions = []
for b in branch_specs:
    sid,_,county,_,opening,_,foot = b
    op = pd.Timestamp(opening)
    days = pd.date_range(op, END, freq='D')
    if len(days)==0: continue
    weekday = days.dayofweek.to_numpy()
    month = days.month.to_numpy()
    dom = days.day.to_numpy()
    year_age = ((days-op).days.to_numpy()) / 365.25
    promo_day = (weekday>=4) & (dom>=23) & (dom<=31)  # synthetic promotional weekend
    avg = 32.0 * foot * (1+np.minimum(year_age, 3)*.075)
    avg *= np.where(weekday>=5,1.20,1.0)
    avg *= np.where(month==12,1.31,1.0)
    avg *= np.where(np.isin(month,[1,8]),1.08,1.0)
    avg *= np.where(dom>=25,1.12,1.0)
    avg *= np.where(promo_day,1.12,1.0)
    daily_n = rng.poisson(avg).astype(int)
    dates = np.repeat(days.to_numpy(dtype='datetime64[D]'),daily_n)
    n=len(dates)
    # Market-shop times: 8am - 9pm.
    hours = rng.choice(np.arange(8,22), n,p=np.array([.025,.03,.045,.065,.075,.08,.09,.105,.11,.115,.10,.075,.05,.035]))
    mins = rng.integers(0,60,n)
    seconds=rng.integers(0,60,n)
    times = dates.astype('datetime64[s]') + hours.astype('timedelta64[h]') + mins.astype('timedelta64[m]') + seconds.astype('timedelta64[s]')
    order_partitions.append(pd.DataFrame({'store_id':sid,'order_datetime':times,'promo_day':np.repeat(promo_day,daily_n)}))
orders = pd.concat(order_partitions,ignore_index=True)
orders.sort_values('order_datetime',inplace=True,kind='stable',ignore_index=True)
N=len(orders)
orders.insert(0,'order_id',[f'O{i:07d}' for i in range(1,N+1)])
# Membership draws reflect heterogeneous repeat buying, with no future registration leakage.
orders['customer_id']=''
for sid in stores.store_id:
    own = customers.loc[customers.preferred_store_id.eq(sid)].copy()
    own.sort_values('registration_date',inplace=True)
    eligible = np.searchsorted(own.registration_date.to_numpy(dtype='datetime64[D]'),
                               orders.loc[orders.store_id.eq(sid),'order_datetime'].to_numpy(dtype='datetime64[D]'),side='right')
    weight = rng.gamma(1.0,1.0,len(own)) + 0.05
    cumulative = weight.cumsum()
    upper = cumulative[np.maximum(eligible-1,0)]
    chosen = np.searchsorted(cumulative,rng.random(len(upper))*upper)
    chosen_ids=own.customer_id.to_numpy()[chosen].astype(object)
    chosen_ids[eligible==0]='' # guest checkout when no registered customer yet
    guest=rng.random(len(chosen_ids))<0.22
    chosen_ids[guest]=''
    orders.loc[orders.store_id.eq(sid),'customer_id']=chosen_ids
orders['channel'] = rng.choice(['In-store','Delivery','Click & collect'],size=N,p=[.90,.07,.03])
orders['payment_method'] = rng.choice(['M-Pesa','Cash','Debit card','Credit card','Bank transfer'],size=N,p=[.60,.245,.092,.043,.02])
# Delivery nearly always paid digitally.
delivery=orders.channel.eq('Delivery').to_numpy()
orders.loc[delivery,'payment_method']=rng.choice(['M-Pesa','Debit card','Credit card','Bank transfer'],delivery.sum(),p=[.82,.10,.04,.04])
orders['order_date']=pd.to_datetime(orders.order_datetime).dt.strftime('%Y-%m-%d')
orders['order_datetime']=pd.to_datetime(orders.order_datetime).dt.strftime('%Y-%m-%d %H:%M:%S')
orders['promo_day']=orders.promo_day.astype(bool)

# Product selection with different seasonal purchase mixes (invented, not empirical).
weights_by_category = {'Staples':1.75,'Fresh Produce':1.65,'Dairy & Eggs':1.55,'Bakery & Snacks':1.35,'Beverages':1.55,
                       'Personal Care':.95,'Household':1.15,'Meat & Fish':.80,'Stationery':.45,'Baby Care':.60}
base_weight = np.array([weights_by_category[c] for c in products.category],dtype=float)
# SKU popularity varies, allowing Pareto-style product concentration.
base_weight *= rng.lognormal(0,.55,len(products))
num_items = rng.choice([1,2,3,4,5,6], size=N,p=[.23,.30,.23,.14,.075,.025])
order_idx=np.repeat(np.arange(N,dtype=np.int32),num_items)
M=len(order_idx)
order_month=pd.to_datetime(orders.order_date).dt.month.to_numpy()
line_month=order_month[order_idx]
product_ix=np.empty(M,dtype=np.int16)
for m in range(1,13):
    mask=line_month==m
    w=base_weight.copy()
    if m in (1,8,9): w[products.category.eq('Stationery').to_numpy()] *= 3.1
    if m==12: w[products.category.eq('Beverages').to_numpy()] *= 1.35
    if m in (6,7): w[products.category.eq('Personal Care').to_numpy()] *= 1.12
    w /= w.sum()
    product_ix[mask]=rng.choice(len(products),size=mask.sum(),p=w)
item_qty = rng.choice([1,2,3,4,5],size=M,p=[.66,.235,.07,.025,.01]).astype(np.int16)
months_since_start=((pd.to_datetime(orders.order_date).dt.year.to_numpy()-2024)*12 +
                   (pd.to_datetime(orders.order_date).dt.month.to_numpy()-1))
month_of_line=months_since_start[order_idx]
# Price drift is a SIMULATED inflation-like trend; not actual CPI.
price_drift=np.power(1.0038,month_of_line)
store_price_factor=np.array([1.02,1.01,1,1,.99,1,1,1,1,1])
store_index=orders.store_id.str[1:].astype(int).to_numpy()-1
p0=products.base_list_price_kes.to_numpy()[product_ix]
unit_price=np.round(p0*price_drift*store_price_factor[store_index[order_idx]]*rng.normal(1,0.018,M),2)
unit_price=np.maximum(5,unit_price)
cost0=products.base_unit_cost_kes.to_numpy()[product_ix]
unit_cost=np.round(cost0*price_drift,2)
item_promo_prob=.09 + .19*orders.promo_day.to_numpy()[order_idx] + .065*(line_month==12)
item_promoted=rng.random(M)<item_promo_prob
disc=np.zeros(M,dtype=np.int16)
disc[item_promoted]=rng.choice([5,10,15],size=item_promoted.sum(),p=[.33,.49,.18])
gross=np.round(unit_price*item_qty,2)
reduction=np.round(gross*disc/100,2)
net=np.round(gross-reduction,2)
line_items=pd.DataFrame({
 'line_id':[f'L{i:08d}' for i in range(1,M+1)],
 'order_id':orders.order_id.to_numpy()[order_idx],
 'product_id':products.product_id.to_numpy()[product_ix],
 'quantity':item_qty,
 'unit_price_kes':unit_price,
 'unit_cost_kes':unit_cost,
 'discount_pct':disc,
 'line_gross_kes':gross,
 'line_discount_kes':reduction,
 'line_net_kes':net
})
# Monetary totals derived from pristine line items; anomalies added after summation.
np_gross=np.bincount(order_idx,weights=gross,minlength=N)
np_disc=np.bincount(order_idx,weights=reduction,minlength=N)
np_net=np.bincount(order_idx,weights=net,minlength=N)
orders['item_units']=np.bincount(order_idx,weights=item_qty,minlength=N).astype(int)
orders['gross_amount_kes']=np.round(np_gross,2)
orders['discount_amount_kes']=np.round(np_disc,2)
orders['net_amount_kes']=np.round(np_net,2)
orders['promotion_applied']=orders.order_id.isin(line_items.loc[line_items.discount_pct.gt(0),'order_id']).to_numpy()
orders.drop(columns=['promo_day'],inplace=True)

# Deliberate small RAW quality issues. The original accurate order totals are retained as a check.
qa={}
missing_prices_idx=rng.choice(M,size=round(M*.002),replace=False)
line_items.loc[missing_prices_idx,'unit_price_kes']=np.nan
qa['blank_unit_prices']=len(missing_prices_idx)
# Some typos in quantity, inconsistent with the original line totals.
outlier_candidates=np.setdiff1d(np.arange(M),missing_prices_idx,assume_unique=False)
qty_corrupt_idx=rng.choice(outlier_candidates,size=round(M*.0005),replace=False)
line_items.loc[qty_corrupt_idx,'quantity']=rng.choice([49,75,99],size=len(qty_corrupt_idx)).astype(np.int16)
qa['quantity_typo_rows']=len(qty_corrupt_idx)
# Duplicate full rows, including duplicated line_id, intended to be deduplicated.
dup_candidates=np.setdiff1d(outlier_candidates,qty_corrupt_idx,assume_unique=False)
dup_idx=rng.choice(dup_candidates,size=round(M*.0012),replace=False)
line_items=pd.concat([line_items,line_items.iloc[dup_idx].copy()],ignore_index=True)
line_items=line_items.iloc[rng.permutation(len(line_items))].reset_index(drop=True)
qa['duplicate_order_item_rows']=len(dup_idx)
# Missing payment methods and customer age bands reflect incomplete POS/loyalty entry.
method_blank_idx=rng.choice(N,size=round(N*.0025),replace=False)
orders.loc[method_blank_idx,'payment_method']=np.nan
qa['blank_payment_methods']=len(method_blank_idx)
missing_age_idx=rng.choice(len(customers),size=round(len(customers)*.008),replace=False)
customers.loc[missing_age_idx,'age_band']=np.nan
qa['blank_customer_age_bands']=len(missing_age_idx)

# Write CSVs; dates in ISO-8601 format; UTF-8; KES. Orders contain legitimate blank customer IDs for guest checkout.
orders.to_csv(DATA/'orders.csv',index=False,float_format='%.2f')
line_items.to_csv(DATA/'order_items.csv',index=False,float_format='%.2f')
customers.to_csv(DATA/'customers.csv',index=False)
qa.update({
 'seed':SEED,'start_date':str(START.date()),'end_date':str(END.date()),
 'stores':len(stores),'counties':stores.county.nunique(),'customers':len(customers),'products':len(products),
 'orders':len(orders),'order_item_rows_raw':len(line_items),'order_item_rows_before_duplicates':M,
 'guest_checkout_orders':int(orders.customer_id.eq('').sum()),
 'mpesa_orders_nonmissing':int(orders.payment_method.eq('M-Pesa').sum()),
 'net_revenue_reference_kes':round(float(np_net.sum()),2),
 'synthetic_retail_data':True,'real_context':'KNBS 2019 county population only'
})
(ROOT/'generation_summary.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
print(json.dumps(qa,indent=2))
