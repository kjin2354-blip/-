"""Event-study chart (Jun 2025 - Oct 2026) and valuation football field. Usage: python3 charts_event.py <scratch_dir>"""
import json, sys, pandas as pd, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
D = sys.argv[1]
def L(f):
    r = json.load(open(f"{D}/{f}"))['chart']['result'][0]
    return pd.Series(r['indicators']['quote'][0]['close'], index=pd.to_datetime(r['timestamp'], unit='s').normalize()).dropna()
df = pd.DataFrame({'LOW': L('low_y.json'), 'HD': L('y_HD.json'), 'S&P 500': L('y_GSPC.json'), 'XHB': L('y_XHB.json')})['2025-06-02':]
n = df / df.iloc[0] * 100
fig, ax = plt.subplots(figsize=(12, 6)); C = {'LOW': '#1f4e9a', 'HD': '#e8710a', 'S&P 500': '#5f6368', 'XHB': '#2ca02c'}
for c in n: ax.plot(n[c], label=c, color=C[c], lw=1.6 if c == 'LOW' else 1.0)
ev = [('2025-08-20', 'Q2 FY25 + FBM deal;\nbuyback pause'), ('2026-01-09', 'GSE $200bn MBS order'), ('2026-02-13', 'LOW record close $287'),
      ('2026-02-25', 'Q4 FY25: FY26 guide\nbelow consensus (-5.6%)'), ('2026-05-20', 'Q1 FY26'), ('2026-08-19', 'Q2 FY26: guide to\nlow end'),
      ('2026-09-16', 'Fed hikes 25bp'), ('2026-09-24', 'Mortgage >7%;\nGordon Haskett downgrade'), ('2026-10-05', '52w low $179.50')]
for i, (d, t) in enumerate(ev):
    x = pd.Timestamp(d); y = n['LOW'][:x].iloc[-1]
    ax.annotate(t, (x, y), xytext=(0, 38 if i % 2 == 0 else -46), textcoords='offset points', ha='center', fontsize=7.5,
                arrowprops=dict(arrowstyle='-', lw=.5, color='k'))
ax.set_title('Event study: LOW vs HD, S&P 500 and XHB, price indexed to 100 on 2 Jun 2025'); ax.legend(frameon=False, loc='upper left')
ax.spines[['top', 'right']].set_visible(False); fig.tight_layout(); fig.savefig('output/chart_event_study.png', dpi=130); plt.close()
# Football field
R = json.load(open('output/model_results.json'))
bars = [('DCF (WACC 8.25-9.25%, g 2.0-3.0%)', 154, 228), ('DCF base 8.75% / 2.5%', 185, 185),
        ('Exit EV/EBITDA 9-11x FY30', R['exit_mult']['9x'], R['exit_mult']['11x']),
        ('P/E on FY27E adj EPS (13x 11.60 to 18x 13.70)', R['eps_val']['Conservative']['value'], R['eps_val']['Optimistic']['value']),
        ('Scenario PV @ CoE 10.15% (bear - bull)', R['scenarios']['Bear']['pv_today_at_coe'], R['scenarios']['Bull']['pv_today_at_coe']),
        ('Prob-weighted scenario PV', R['prob_weighted']['pv_today_at_coe'], R['prob_weighted']['pv_today_at_coe']),
        ('52-week trading range', 179.5, 287.39), ('Sell-side targets (low - mean)', 190, 252.42)]
fig, ax = plt.subplots(figsize=(11, 5))
for i, (lab, lo, hi) in enumerate(bars[::-1]):
    if hi - lo < 2: ax.plot([lo], [i], 'D', color='#1f4e9a')
    else: ax.barh(i, hi - lo, left=lo, color='#9db7e0' if 'range' not in lab and 'targets' not in lab else '#cccccc'); ax.text(hi + 2, i, f"${lo:.0f}-{hi:.0f}", va='center', fontsize=8)
ax.set_yticks(range(len(bars))); ax.set_yticklabels([b[0] for b in bars[::-1]], fontsize=8.5)
ax.axvline(186, color='#c0392b', ls='--', lw=1); ax.text(187, len(bars) - .4, 'Price $186.00 (9 Oct 2026)', color='#c0392b', fontsize=8)
ax.axvline(195, color='#1f4e9a', ls=':', lw=1); ax.text(196, -.7, 'Base intrinsic value ~$195', color='#1f4e9a', fontsize=8)
ax.set_title("LOW valuation football field ($/share)"); ax.spines[['top', 'right']].set_visible(False); fig.tight_layout(); fig.savefig('output/chart_football_field.png', dpi=130)
# scenario CAGR by entry price
e = pd.read_csv('output/entry_price_cagr.csv', index_col=0) * 100
fig, ax = plt.subplots(figsize=(10, 4.5))
for c, col in zip(e.columns, ['#c0392b', '#1f4e9a', '#2ca02c', 'k']): ax.plot(e.index, e[c], marker='o', label=c, color=col, lw=2.2 if 'Expected' in c else 1.2)
ax.axhline(10.15, color='grey', ls=':', lw=1); ax.text(e.index.min(), 10.6, 'Cost of equity 10.15%', fontsize=8, color='grey')
ax.axvline(186, color='#c0392b', ls='--', lw=.8); ax.set_xlabel('Entry price ($)'); ax.set_ylabel('5-yr annualised total return (%)')
ax.set_title('Five-year annualised total return by entry price and scenario'); ax.legend(frameon=False); ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig('output/chart_entry_returns.png', dpi=130)
