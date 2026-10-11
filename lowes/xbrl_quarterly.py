"""Build quarterly (3-month) series from SEC XBRL companyfacts; Q4 = FY - (Q1+Q2+Q3).
Usage: python3 xbrl_quarterly.py <companyfacts.json> <out.csv>"""
import json, sys, datetime as dt, pandas as pd
g = json.load(open(sys.argv[1]))['facts']['us-gaap']
TAGS = {'rev': ['RevenueFromContractWithCustomerExcludingAssessedTax', 'SalesRevenueNet', 'Revenues'],
        'gp': ['GrossProfit'], 'oi': ['OperatingIncomeLoss'], 'ni': ['NetIncomeLoss'], 'eps': ['EarningsPerShareDiluted'],
        'da': ['DepreciationAndAmortization', 'DepreciationDepletionAndAmortization']}
def series(tags):
    q, a = {}, {}
    for t in tags:
        if t not in g: continue
        for x in list(g[t]['units'].values())[0]:
            if 'start' not in x or not x.get('form', '').startswith('10-'): continue
            s, e = dt.date.fromisoformat(x['start']), dt.date.fromisoformat(x['end']); n = (e - s).days
            if 80 < n < 100: q.setdefault(e, x['val'])
            elif 350 < n < 380 and x['form'] == '10-K': a.setdefault(e, (s, x['val']))
    for e, (s, v) in a.items():  # derive Q4
        if e in q: continue
        prior = [k for k in q if s < k < e]
        if len(prior) == 3: q[e] = v - sum(q[k] for k in prior)
    return pd.Series(q).sort_index()
df = pd.DataFrame({k: series(v) for k, v in TAGS.items()}); df.index = pd.to_datetime(df.index)
df = df[df.index >= '2009-01-01']; df.to_csv(sys.argv[2]); print(df.tail(10))
