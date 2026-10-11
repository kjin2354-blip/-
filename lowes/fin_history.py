"""Annual financial history (SEC XBRL, 10-K values) + fiscal-year-end valuation multiples for LOW, and TTM LOW vs HD.
Usage: python3 fin_history.py <scratch_dir>"""
import json, sys, datetime as dt, pandas as pd
D = sys.argv[1]
def annual(fn, tags):
    g = json.load(open(f"{D}/{fn}"))['facts']['us-gaap']; out = {}
    for t in tags:
        if t not in g: continue
        for x in list(g[t]['units'].values())[0]:
            if x.get('form') != '10-K': continue
            if 'start' in x and (dt.date.fromisoformat(x['end']) - dt.date.fromisoformat(x['start'])).days < 350: continue
            out.setdefault(x['end'], x['val'])
    return pd.Series(out)
T = {'Revenue': ['RevenueFromContractWithCustomerExcludingAssessedTax', 'SalesRevenueNet'], 'Gross profit': ['GrossProfit'],
     'Operating income': ['OperatingIncomeLoss'], 'Net income': ['NetIncomeLoss'], 'Diluted EPS (GAAP)': ['EarningsPerShareDiluted'],
     'CFO': ['NetCashProvidedByUsedInOperatingActivities'], 'Capex': ['PaymentsToAcquirePropertyPlantAndEquipment'],
     'Dividends paid': ['PaymentsOfDividendsCommonStock'], 'Buybacks': ['PaymentsForRepurchaseOfCommonStock'],
     'LT debt': ['LongTermDebtAndCapitalLeaseObligations'], 'Current debt': ['LongTermDebtAndCapitalLeaseObligationsCurrent'],
     'ST borrowings': ['ShortTermBorrowings', 'CommercialPaper'], 'Cash': ['CashAndCashEquivalentsAtCarryingValue'], 'ST inv': ['ShortTermInvestments'],
     'Diluted shares (m)': ['WeightedAverageNumberOfDilutedSharesOutstanding'], 'D&A': ['DepreciationDepletionAndAmortization'],
     'Acquisitions': ['PaymentsToAcquireBusinessesNetOfCashAcquired']}
df = pd.DataFrame({k: annual('low_facts.json', v) for k, v in T.items()}); df.index = pd.to_datetime(df.index); df = df.sort_index()
df = df[(df.index >= '2016-01-01')].fillna(0); df = df[df['Revenue'] > 0]
m = df.copy()
for c in m.columns:
    if c not in ('Diluted EPS (GAAP)',): m[c] = m[c] / 1e6
m['FY'] = [f"FY{d.year - 1}" for d in m.index]
m = m.set_index('FY')
# verified from Lowe's Q4 releases (see README): comps and adjusted EPS
COMP = {'FY2014': None, 'FY2015': 4.8, 'FY2016': 4.2, 'FY2017': 4.0, 'FY2018': 2.4, 'FY2019': 2.6, 'FY2020': 26.1, 'FY2021': 6.9, 'FY2022': -0.9, 'FY2023': -4.7, 'FY2024': -2.7, 'FY2025': 0.2}
ADJ = {'FY2015': 3.29, 'FY2016': 3.99, 'FY2017': 4.39, 'FY2018': None, 'FY2019': 5.74, 'FY2020': 8.86, 'FY2021': 12.04, 'FY2022': 13.81, 'FY2023': 13.09, 'FY2024': 11.99, 'FY2025': 12.28}
m['Comp %'] = [COMP.get(i) for i in m.index]; m['Adj EPS'] = [ADJ.get(i) for i in m.index]
m['Rev growth %'] = m['Revenue'].pct_change() * 100; m['Gross margin %'] = m['Gross profit'] / m['Revenue'] * 100
m['Op margin %'] = m['Operating income'] / m['Revenue'] * 100; m['FCF'] = m['CFO'] - m['Capex']
m['Total debt'] = m['LT debt'] + m['Current debt'] + m['ST borrowings']; m['Net debt'] = m['Total debt'] - m['Cash'] - m['ST inv']
m['EBITDA'] = m['Operating income'] + m['D&A']; m['FCF/share'] = m['FCF'] / m['Diluted shares (m)']
m['FCF conversion (FCF/NI)'] = m['FCF'] / m['Net income']; m['Shareholder payout/FCF'] = (m['Dividends paid'] + m['Buybacks']) / m['FCF']
# FYE valuation (price on fiscal year-end date; EPS of the year just ended)
r = json.load(open(f"{D}/low_y.json"))['chart']['result'][0]
px = pd.Series(r['indicators']['quote'][0]['close'], index=pd.to_datetime(r['timestamp'], unit='s').normalize()).dropna()
p = [px[:d].iloc[-1] for d in df.index]; m['FYE price'] = p
m['Mkt cap'] = m['FYE price'] * m['Diluted shares (m)']; m['EV'] = m['Mkt cap'] + m['Net debt']
m['P/E (GAAP)'] = m['FYE price'] / m['Diluted EPS (GAAP)']; m['P/E (adj)'] = m['FYE price'] / m['Adj EPS'].astype(float)
m['EV/EBITDA'] = m['EV'] / m['EBITDA']; m['P/FCF'] = m['Mkt cap'] / m['FCF']; m['FCF yield %'] = 100 / m['P/FCF']
DPS = {'FY2015': 1.07, 'FY2016': 1.33, 'FY2017': 1.58, 'FY2018': 1.85, 'FY2019': 2.13, 'FY2020': 2.30, 'FY2021': 3.00, 'FY2022': 3.95, 'FY2023': 4.35, 'FY2024': 4.55, 'FY2025': 4.75}
m['DPS declared'] = [DPS.get(i) for i in m.index]; m['Div yield %'] = m['DPS declared'].astype(float) / m['FYE price'] * 100
m['Payout (GAAP) %'] = m['DPS declared'].astype(float) / m['Diluted EPS (GAAP)'] * 100
m['Net debt/EBITDA'] = m['Net debt'] / m['EBITDA']
m.round(2).to_csv('output/low_financial_history.csv')
cols1 = ['Revenue', 'Rev growth %', 'Comp %', 'Gross margin %', 'Op margin %', 'Net income', 'Diluted EPS (GAAP)', 'Adj EPS', 'Diluted shares (m)']
cols2 = ['CFO', 'Capex', 'FCF', 'FCF conversion (FCF/NI)', 'Dividends paid', 'Buybacks', 'Acquisitions', 'Total debt', 'Cash', 'Net debt', 'Net debt/EBITDA']
cols3 = ['FYE price', 'P/E (GAAP)', 'P/E (adj)', 'EV/EBITDA', 'P/FCF', 'FCF yield %', 'Div yield %', 'Payout (GAAP) %']
for c in (cols1, cols2, cols3): print(m[c].round(2).to_markdown()); print()
# EPS bridge FY2015 -> FY2025: growth from net income vs share count
for a, b in [('FY2015', 'FY2025'), ('FY2019', 'FY2025'), ('FY2021', 'FY2025')]:
    ni = m.loc[b, 'Net income'] / m.loc[a, 'Net income']; sh = m.loc[a, 'Diluted shares (m)'] / m.loc[b, 'Diluted shares (m)']
    eps = m.loc[b, 'Diluted EPS (GAAP)'] / m.loc[a, 'Diluted EPS (GAAP)']; n = int(b[2:]) - int(a[2:])
    print(f"{a}->{b}: EPS x{eps:.2f} ({eps**(1/n)-1:.1%}/yr) = net income x{ni:.2f} ({ni**(1/n)-1:.1%}/yr) * share shrink x{sh:.2f} ({sh**(1/n)-1:.1%}/yr)")
