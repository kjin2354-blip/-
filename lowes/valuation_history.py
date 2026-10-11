"""Historical trailing P/E (GAAP diluted TTM EPS, lagged 25 days after quarter end to approximate
report date) and 'ex-post forward' P/E (price / realized next-4-quarter GAAP EPS; NOT historical consensus).
Usage: python3 valuation_history.py <scratch_dir>"""
import json, sys, pandas as pd, numpy as np
D = sys.argv[1]
def px(f):
    r = json.load(open(f"{D}/{f}"))['chart']['result'][0]
    return pd.Series(r['indicators']['quote'][0]['close'], index=pd.to_datetime(r['timestamp'], unit='s').normalize()).dropna()
res = {}
for tk, pf, qf in [('LOW', 'low_y.json', 'output/low_quarterly.csv'), ('HD', 'y_HD.json', 'output/hd_quarterly.csv')]:
    p = px(pf); q = pd.read_csv(qf, index_col=0, parse_dates=True)
    ttm = q['eps'].rolling(4).sum(); fwd = q['eps'][::-1].rolling(4).sum()[::-1].shift(-1)
    avail = ttm.copy(); avail.index = avail.index + pd.Timedelta(days=25)
    m = p.resample('ME').last()
    t = avail.reindex(m.index.union(avail.index)).ffill().reindex(m.index)
    f_ = fwd.copy(); f_.index = f_.index + pd.Timedelta(days=25); f_ = f_.reindex(m.index.union(f_.index)).ffill().reindex(m.index)
    res[tk + '_PE_ttm'] = m / t; res[tk + '_PE_fwd_expost'] = m / f_
v = pd.DataFrame(res).loc['2011':]
v['LOW_minus_HD_ttm'] = v['LOW_PE_ttm'] - v['HD_PE_ttm']
v.to_csv('output/pe_history_monthly.csv', float_format='%.2f')
def stats(s, yrs):
    s = s.dropna(); s = s[s.index[-1] - pd.DateOffset(years=yrs):]
    return {'min': s.min(), 'p25': s.quantile(.25), 'median': s.median(), 'p75': s.quantile(.75), 'max': s.max(), 'latest': s.iloc[-1]}
out = {f"{c}_{y}y": stats(v[c], y) for c in ['LOW_PE_ttm', 'HD_PE_ttm', 'LOW_minus_HD_ttm'] for y in (5, 10)}
print(pd.DataFrame(out).T.round(1).to_string())
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.plot(v['LOW_PE_ttm'], label='LOW trailing P/E (GAAP)', color='#1f4e9a'); ax.plot(v['HD_PE_ttm'], label='HD trailing P/E (GAAP)', color='#e8710a')
ax.axhline(v['LOW_PE_ttm']['2016':].median(), color='#1f4e9a', ls=':', lw=1, label='LOW 10y median')
ax.set_ylim(0, 35); ax.set_title('Trailing P/E on GAAP diluted EPS, month-end (FY2018 LOW spike = Orchard/Mexico/Canada charges)'); ax.legend(frameon=False)
ax.spines[['top', 'right']].set_visible(False); fig.tight_layout(); fig.savefig('output/chart_pe_history.png', dpi=130)
print(v.tail(3).round(1))
