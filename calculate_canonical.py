import pandas as pd

xl = pd.ExcelFile('data/real_estate_dataset.xlsx')
deals = xl.parse('Deals')
exp = xl.parse('Expenses')
props = xl.parse('Properties')
leads = xl.parse('Leads')
visits = xl.parse('Site_Visits')
perf = xl.parse('Agent_Performance')

closed = deals[deals['deal_status'] == 'Closed Won']
rev = closed['sale_price'].sum()
comm = (closed['sale_price'] * closed['commission_rate']).sum()
exp_tot = exp['amount'].sum()
profit = comm - exp_tot
margin = (profit / comm) * 100
converted_leads = len(leads[leads['lead_status'] == 'Converted'])
sold_props = len(props[props['listing_status'] == 'Sold'])

print("--- CANONICAL DATASET TOTALS ---")
print(f"Total Revenue (Closed Won): ₹{rev:,.2f}")
print(f"Total Commission: ₹{comm:,.2f}")
print(f"Total Expenses: ₹{exp_tot:,.2f}")
print(f"Net Operating Profit: ₹{profit:,.2f}")
print(f"Net Profit Margin: {margin:.2f}%")
print(f"Total Deals: {len(deals)}")
print(f"Closed Won Deals: {len(closed)} ({len(closed)/len(deals)*100:.2f}%)")
print(f"Total Leads: {len(leads)}")
print(f"Converted Leads: {converted_leads} ({converted_leads/len(leads)*100:.2f}%)")
print(f"Total Properties: {len(props)}")
print(f"Sold Properties: {sold_props} ({sold_props/len(props)*100:.2f}%)")
print(f"Total Site Visits: {len(visits)}")
print(f"Total Performance Rows: {len(perf)}")
