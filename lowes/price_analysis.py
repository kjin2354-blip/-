"""LOW price & total-return analytics. Data: Yahoo Finance chart API (daily close and adjclose,
adjclose = split- and dividend-adjusted). Run: python3 price_analysis.py <data_dir> <out_dir>"""
import json, sys, numpy as np, pandas as pd
D, O = sys.argv[1], sys.argv[2]
def load(f):
    r = json.load(open(f))['chart']['result'][0]
    idx = pd.to_datetime(r['timestamp'], unit='s').normalize()
    q = r['indicators']
    df = pd.DataFrame({'close': q['quote'][0]['close']}, index=idx)
    if 'adjclose' in q: df['adj'] = q['adjclose'][0]['adjclose']
    else: df['adj'] = df['close']
    divs = pd.Series({pd.to_datetime(int(k), unit='s').normalize(): v['amount'] for k, v in r.get('events', {}).get('dividends', {}).items()}).sort_index()
    return df.dropna(), divs
S = {k: load(f"{D}/{f}") for k, f in {'LOW': 'low_y.json', 'HD': 'y_HD.json', 'SPY': 'y_SPY.json', 'XHB': 'y_XHB.json', 'SPX': 'y_GSPC.json', 'SPXTR': 'y_SP500TR.json'}.items()}
END = S['LOW'][0].index[-1]
px = pd.DataFrame({k: v[0]['close'] for k, v in S.items()}).loc['2005':]
tr = pd.DataFrame({k: v[0]['adj'] for k, v in S.items()}).loc['2005':]
tr['SPX_TR'] = tr['SPXTR']  # S&P 500 total-return index
out = {'end_date': str(END.date()), 'last_close': {k: round(float(px[k].dropna().iloc[-1]), 2) for k in px}}
# annual returns (calendar years) price vs total
ye = lambda s: s.dropna().groupby(s.dropna().index.year).last()
ann = {}
for k in ['LOW', 'HD', 'SPX', 'XHB']:
    p = ye(px[k]); t = ye(tr[k] if k != 'SPX' else tr['SPX_TR'])
    ann[k + '_price'] = p.pct_change(); ann[k + '_TR'] = t.pct_change()
ann = pd.DataFrame(ann).loc[2011:]
ann.index = [str(i) if i < END.year else f"{i} YTD" for i in ann.index]
ann.to_csv(f"{O}/annual_returns.csv", float_format='%.4f')
# CAGRs to END
def cagr(s, yrs):
    s = s.dropna(); start = END - pd.DateOffset(years=yrs); s0 = s[:start].iloc[-1]
    return (s.iloc[-1] / s0) ** (1 / yrs) - 1
cg = {}
for k, col_tr in [('LOW', 'LOW'), ('HD', 'HD'), ('S&P 500', 'SPX_TR'), ('XHB', 'XHB')]:
    col_p = {'S&P 500': 'SPX'}.get(k, k)
    cg[k] = {f'{y}y_price': cagr(px[col_p], y) for y in (1, 3, 5, 10, 15)} | {f'{y}y_TR': cagr(tr[col_tr], y) for y in (1, 3, 5, 10, 15)}
cg = pd.DataFrame(cg).T; cg.to_csv(f"{O}/cagr.csv", float_format='%.4f')
# risk stats, 10y daily TR
rs = {}
for k, c in [('LOW', 'LOW'), ('HD', 'HD'), ('S&P 500', 'SPX_TR'), ('XHB', 'XHB')]:
    for yrs in (5, 10, 15):
        s = tr[c].dropna()[END - pd.DateOffset(years=yrs):]
        r = s.pct_change().dropna(); vol = r.std() * np.sqrt(252)
        c_ = (s.iloc[-1] / s.iloc[0]) ** (1 / yrs) - 1
        dd = (s / s.cummax() - 1).min()
        rs[(k, yrs)] = {'CAGR_TR': c_, 'vol': vol, 'ret/vol': c_ / vol, 'max_dd': dd}
    # beta vs S&P TR (10y, weekly)
w = tr.resample('W-FRI').last().pct_change().loc[END - pd.DateOffset(years=10):]
rs = pd.DataFrame(rs).T
for k, c in [('LOW', 'LOW'), ('HD', 'HD'), ('XHB', 'XHB')]:
    x = w[[c, 'SPX_TR']].dropna(); rs.loc[(k, 10), 'beta_10y_weekly'] = np.cov(x[c], x['SPX_TR'])[0, 1] / x['SPX_TR'].var()
rs.to_csv(f"{O}/risk_stats.csv", float_format='%.4f')
# drawdown episodes LOW (price, unadjusted is fine for ranking; use adjusted TR)
s = tr['LOW'].dropna(); peak = s.cummax(); dd = s / peak - 1
eps = []; in_dd = False
for d, v in dd.items():
    if not in_dd and v < -0.20: in_dd = True; st = peak[:d].idxmax() if False else s[:d].idxmax()
    if in_dd and v == 0:
        seg = dd[st:d]; eps.append((st.date(), seg.idxmin().date(), round(seg.min(), 3), d.date())); in_dd = False
if in_dd: seg = dd[st:]; eps.append((st.date(), seg.idxmin().date(), round(seg.min(), 3), None))
out['drawdowns_gt20_TR'] = [list(map(str, e)) for e in eps]
# recent peak, ytd
p = px['LOW'].dropna()
r2 = p['2024-01-01':]; out['peak_since_2024'] = [str(r2.idxmax().date()), round(float(r2.max()), 2)]
out['ath_close'] = [str(p.idxmax().date()), round(float(p.max()), 2)]
out['ytd_start'] = round(float(p[:'2025-12-31'].iloc[-1]), 2)
out['low_52w'] = [str(p[END - pd.DateOffset(weeks=52):].idxmin().date()), round(float(p[END - pd.DateOffset(weeks=52):].min()), 2)]
out['high_52w'] = [str(p[END - pd.DateOffset(weeks=52):].idxmax().date()), round(float(p[END - pd.DateOffset(weeks=52):].max()), 2)]
d = S['LOW'][1]; out['divs_last8'] = {str(k.date()): v for k, v in d.iloc[-8:].items()}
dy = d.groupby(d.index.year).sum(); out['div_by_year'] = {int(k): round(v, 3) for k, v in dy.items() if k >= 2010}
# dividend contribution: TR CAGR minus price CAGR
json.dump(out, open(f"{O}/price_summary.json", 'w'), indent=1)
# ---- charts
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
C = {'LOW': '#1f4e9a', 'HD': '#e8710a', 'S&P 500': '#5f6368', 'XHB': '#2ca02c'}
fig, ax = plt.subplots(2, 1, figsize=(11, 8), gridspec_kw={'height_ratios': [2, 1]}, sharex=True)
ax[0].plot(p['2011':], color=C['LOW'], lw=1.2, label='LOW close (split-adjusted, price only)')
for x, lab in [('2020-03-23', 'COVID low'), ('2021-12-10', '2021 peak'), ('2022-06-16', 'Rate shock'), ('2025-04-08', 'Tariff low'), (out['peak_since_2024'][0], 'Recent peak'), (str(END.date()), 'Latest')]:
    xd = pd.Timestamp(x); y = p[:xd].iloc[-1]; ax[0].annotate(f"{lab}\n${y:.0f}", (xd, y), textcoords='offset points', xytext=(0, 14), ha='center', fontsize=8, arrowprops=dict(arrowstyle='-', lw=.5))
ax[0].set_title(f"Lowe's (LOW) share price, 2011 – {END.date()}"); ax[0].set_ylabel('USD'); ax[0].legend(loc='upper left', frameon=False)
ax[1].fill_between(dd['2011':].index, dd['2011':] * 100, 0, color=C['LOW'], alpha=.35); ax[1].set_ylabel('Drawdown from peak, % (TR)')
fig.tight_layout(); fig.savefig(f"{O}/chart_price_drawdown.png", dpi=130); plt.close()
# growth of $100 TR, 15y
fig, ax = plt.subplots(figsize=(11, 5.5))
st = END - pd.DateOffset(years=15)
for k, c in [('LOW', 'LOW'), ('HD', 'HD'), ('S&P 500', 'SPX_TR'), ('XHB', 'XHB')]:
    s = tr[c].dropna()[st:]; ax.plot(s / s.iloc[0] * 100, label=k, color=C[k], lw=1.3)
ax.set_yscale('log'); ax.set_title(f"Growth of $100, total return (dividends reinvested), {st.date()} – {END.date()} (log scale)"); ax.legend(frameon=False); ax.set_ylabel('USD (log)')
fig.tight_layout(); fig.savefig(f"{O}/chart_growth_100.png", dpi=130); plt.close()
# annual TR bars
fig, ax = plt.subplots(figsize=(12, 5)); a = ann[[ 'LOW_TR', 'HD_TR', 'SPX_TR']] * 100
x = np.arange(len(a)); wd = .27
for i, (col, k) in enumerate([('LOW_TR', 'LOW'), ('HD_TR', 'HD'), ('SPX_TR', 'S&P 500')]):
    ax.bar(x + (i - 1) * wd, a[col], wd, label=k, color=C[k])
ax.set_xticks(x); ax.set_xticklabels(a.index, rotation=0, fontsize=8); ax.axhline(0, color='k', lw=.6)
ax.set_title('Calendar-year total returns (%), dividends reinvested'); ax.legend(frameon=False)
fig.tight_layout(); fig.savefig(f"{O}/chart_annual_tr.png", dpi=130); plt.close()
# LOW / HD relative
rel = (tr['LOW'] / tr['HD']).dropna()['2011':]; fig, ax = plt.subplots(figsize=(11, 4)); ax.plot(rel / rel.iloc[0], color=C['LOW'])
ax.set_title('LOW total return relative to HD (2011 = 1.0)'); fig.tight_layout(); fig.savefig(f"{O}/chart_low_vs_hd.png", dpi=130); plt.close()
print(json.dumps(out, indent=1)); print(ann.round(3).to_string()); print(cg.round(3).to_string()); print(rs.round(3).to_string())
