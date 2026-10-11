"""Lowe's (LOW) valuation model: DCF (unlevered FCF), sensitivities, exit-multiple cross-check,
EPS/P-E valuation, and five-year bear/base/bull total-return scenarios.
All $ in billions except per-share. Fiscal years end late Jan/early Feb (FY2025 = year ended 2026-01-30).
Every input is in the ASSUMPTIONS block; sources/labels in README.md. Run: python3 model.py"""
import json, itertools, numpy as np, pandas as pd

PRICE, PRICE_DATE = 186.00, '2026-10-09'           # NYSE close (Yahoo Finance)
SHARES = 0.560                                     # bn diluted shares, Q2 FY26 weighted avg (10-Q)
DEBT = 35.204 + 2.352                              # LT debt incl. finance leases + current maturities, 2026-07-31 (10-Q XBRL)
CASH = 3.172                                       # cash & equivalents 2026-07-31 (seasonal high; see notes)
NET_DEBT = DEBT - CASH                             # operating leases excluded on both EBIT and debt side (consistent)
FY25_SALES = 86.286; FY26_SALES = 92.0             # FY25 actual; FY26 = mgmt guidance (Aug 19 2026)
DPS_NOW = 1.25 * 4                                 # annualised quarterly dividend
TAX = 0.245; DA_PCT = 0.027; CAPEX_PCT = 0.027; NWC_PCT = 0.05   # D&A incl. acquired-intangible amortisation
NET_INTEREST = 1.55                                # $bn/yr, ~TTM run-rate (10-Q)

def dcf(growth, margins, wacc, g, net_debt=NET_DEBT, shares=SHARES, ret_tv=False):
    """growth: FY27-30 sales growth list (FY26 fixed at guidance); margins: FY26-30 EBIT margin (GAAP-like)."""
    sales = [FY26_SALES]; [sales.append(sales[-1] * (1 + x)) for x in growth]
    prev = FY25_SALES; fcf = []
    for s, m in zip(sales, margins):
        ebit = s * m; nopat = ebit * (1 - TAX)
        f = nopat + s * DA_PCT - s * CAPEX_PCT - (s - prev) * NWC_PCT; fcf.append(f); prev = s
    # valuation date ~ Oct 2026; FY26 ends Jan 2027 -> discount FY26 cash flow (remaining ~1 quarter, take 25%) at 0.3y,
    t = np.array([0.3, 1.3, 2.3, 3.3, 4.3]); w = np.array([0.25, 1, 1, 1, 1])
    pv = (np.array(fcf) * w / (1 + wacc) ** t).sum()
    tv = fcf[-1] * (1 + g) / (wacc - g); pv_tv = tv / (1 + wacc) ** t[-1]
    ev = pv + pv_tv; eq = ev - net_debt; ps = eq / shares
    if ret_tv: return dict(sales=sales, fcf=fcf, pv=pv, tv=tv, pv_tv=pv_tv, ev=ev, eq=eq, ps=ps, tv_share=pv_tv / ev,
                           implied_ev_ebitda=tv / (sales[-1] * (margins[-1] + DA_PCT)))
    return ps

BASE_G = [0.030, 0.040, 0.040, 0.035]; BASE_M = [0.110, 0.113, 0.117, 0.120, 0.122]
WACC, TG = 0.0825, 0.025
out = {}
b = dcf(BASE_G, BASE_M, WACC, TG, ret_tv=True); out['dcf_base'] = b
sens1 = pd.DataFrame({f"g={g:.1%}": {f"WACC={w:.2%}": dcf(BASE_G, BASE_M, w, g) for w in (0.0725, 0.0775, 0.0825, 0.0875, 0.0925)} for g in (0.015, 0.02, 0.025, 0.03)})
sens2 = pd.DataFrame({f"FY30 margin={m:.1%}": {f"growth {x:+.1%} vs base": dcf([g + x for g in BASE_G], list(np.linspace(0.110, m, 5)), WACC, TG)
                                                for x in (-0.02, -0.01, 0, 0.01)} for m in (0.10, 0.11, 0.122, 0.13, 0.135)})
# exit-multiple cross-check: FY30 EBITDA x multiple, discounted
def exit_mult(mult, growth=BASE_G, margins=BASE_M, wacc=WACC):
    d = dcf(growth, margins, wacc, TG, ret_tv=True); ebitda30 = d['sales'][-1] * (margins[-1] + DA_PCT)
    pv_fcf = d['pv']; ev = pv_fcf + ebitda30 * mult / (1 + wacc) ** 4.3
    return (ev - NET_DEBT) / SHARES
out['exit_mult'] = {f"{m}x FY30 EBITDA": exit_mult(m) for m in (9, 10, 11, 12, 13)}

# ---------------- Scenarios (5-year hold: Oct 2026 -> Oct 2031, exit on FY2031E (NTM) EPS) ----------------
SCN = {
 'Bear': dict(p=0.25, comps=[0.0, -0.5, 1.0, 1.5, 2.0, 2.0], other=0.005, m=[0.108, 0.104, 0.104, 0.106, 0.108, 0.110], pe=13.0, buyback=2.0, int_rate=0.047),
 'Base': dict(p=0.50, comps=[0.0, 1.5, 3.0, 3.0, 3.0, 3.0], other=0.010, m=[0.110, 0.113, 0.117, 0.120, 0.122, 0.123], pe=16.0, buyback=4.0, int_rate=0.045),
 'Bull': dict(p=0.25, comps=[0.0, 3.5, 5.0, 4.5, 4.0, 3.5], other=0.012, m=[0.112, 0.118, 0.124, 0.128, 0.131, 0.133], pe=18.5, buyback=6.0, int_rate=0.045),
}
# comps[0] = FY26 (guidance 'approximately flat'); other = non-comp growth (new Pro distribution branches, FBM/ADG organic growth beyond comp base)
def scenario(s):
    sales = FY26_SALES; shares = SHARES; debt = NET_DEBT; dps = DPS_NOW; rows = []; cum_div = 0
    for i, yr in enumerate(range(2026, 2032)):
        if i > 0: sales *= 1 + s['comps'][i] / 100 + s['other']
        ebit = sales * s['m'][i]; interest = debt * s['int_rate'] if i > 0 else NET_INTEREST
        ni = (ebit - interest) * (1 - TAX); eps = ni / shares
        fcf_eq = ni + sales * DA_PCT - sales * CAPEX_PCT - (sales * NWC_PCT * (s['comps'][i] / 100 + s['other']) if i else 0)
        div = dps * shares; dps_next = dps * (1 + max(0.0, min(0.06, (eps / rows[-1]['eps'] - 1) if rows else 0.04)))
        # buyback $bn/yr capped by FCF after dividends; leverage held ~flat in $ (target ~2.75x lease-adj EBITDAR is mgmt policy)
        bb = min(s['buyback'], max(0.0, fcf_eq - div)) if i > 0 else 0.4
        debt += -(fcf_eq - div - bb) if i > 0 else 0
        rows.append(dict(FY=yr, sales=sales, comp=s['comps'][i], ebit_m=s['m'][i], ebit=ebit, ni=ni, shares=shares, eps=eps, fcf_eq=fcf_eq, dps=dps, buyback=bb, net_debt=debt))
        if i > 0:
            px_avg = None
        dps = dps_next
        shares -= bb / (PRICE * (1.0 + 0.05 * i)) if i > 0 else 0   # buybacks executed at a price drifting +5%/yr from today (simplification)
    df = pd.DataFrame(rows)
    exit_eps = df.loc[df.FY == 2031, 'eps'].item()       # Oct 2031 price on forward (FY2031) EPS
    exit_px = exit_eps * s['pe']
    divs = df.loc[df.FY.between(2027, 2031), 'dps'].sum()  # ~5 years of dividends received Oct26-Oct31 (approx.)
    tot = (exit_px + divs) / PRICE; cagr = tot ** (1 / 5) - 1
    return df, dict(exit_eps=exit_eps, exit_pe=s['pe'], exit_px=exit_px, divs=divs, total_mult=tot, cagr=cagr,
                    fy27_eps=df.loc[df.FY == 2027, 'eps'].item(), fy30_fcf=df.loc[df.FY == 2030, 'fcf_eq'].item())
sc = {k: scenario(v) for k, v in SCN.items()}
pw_cagr = sum(SCN[k]['p'] * sc[k][1]['cagr'] for k in SCN)
pw_px = sum(SCN[k]['p'] * sc[k][1]['exit_px'] for k in SCN)
pw_tot = sum(SCN[k]['p'] * sc[k][1]['total_mult'] for k in SCN)
# entry-price table: CAGR by scenario for alternative entry prices
entry = {}
for P in (150, 160, 170, 186, 200, 215, 230):
    entry[P] = {k: ((sc[k][1]['exit_px'] + sc[k][1]['divs']) / P) ** 0.2 - 1 for k in SCN}
    entry[P]['Prob-wtd (of total multiple)'] = sum(SCN[k]['p'] * (sc[k][1]['exit_px'] + sc[k][1]['divs']) / P for k in SCN) ** 0.2 - 1
entry = pd.DataFrame(entry).T
# tornado: base CAGR sensitivity to single variables
def base_cagr(**kw):
    s = json.loads(json.dumps(SCN['Base'])); s.update(kw); return scenario(s)[1]['cagr']
torn = {
 'Exit P/E 13x / 19x': (base_cagr(pe=13.0), base_cagr(pe=19.0)),
 'FY31 EBIT margin -150bp / +150bp': (base_cagr(m=[*SCN['Base']['m'][:1], *[x - 0.015 * (i + 1) / 5 for i, x in enumerate(SCN['Base']['m'][1:])]]),
                                      base_cagr(m=[*SCN['Base']['m'][:1], *[x + 0.015 * (i + 1) / 5 for i, x in enumerate(SCN['Base']['m'][1:])]])),
 'Comps -1.5pt / +1.5pt per yr (FY27-31)': (base_cagr(comps=[0.0] + [c - 1.5 for c in SCN['Base']['comps'][1:]]), base_cagr(comps=[0.0] + [c + 1.5 for c in SCN['Base']['comps'][1:]])),
 'Buybacks $1bn / $7bn per yr': (base_cagr(buyback=1.0), base_cagr(buyback=7.0)),
 'Interest rate on net debt 5.5% / 4.0%': (base_cagr(int_rate=0.055), base_cagr(int_rate=0.04)),
}
# ------------- EPS / P-E valuation (12-month view on FY2027E EPS) -------------
eps_cases = {'Conservative': (12.00, 13.0), 'Base': (13.20, 16.0), 'Optimistic': (14.20, 18.0)}
eps_val = {k: dict(fy27_eps=e, pe=m, value=e * m, vs_price=e * m / PRICE - 1) for k, (e, m) in eps_cases.items()}

if __name__ == '__main__':
    pd.set_option('display.width', 200)
    print(f"Net debt ${NET_DEBT:.2f}bn; mkt cap ${PRICE*SHARES:.1f}bn; EV ${PRICE*SHARES+NET_DEBT:.1f}bn")
    print('DCF base:', {k: (round(v, 2) if isinstance(v, float) else [round(x, 2) for x in v]) for k, v in b.items()})
    print('\nWACC x g ($/sh)\n', sens1.round(0)); print('\nGrowth x FY30 margin ($/sh)\n', sens2.round(0))
    print('\nExit multiple', {k: round(v) for k, v in out['exit_mult'].items()})
    for k in SCN:
        df, r = sc[k]; print(f"\n== {k} (p={SCN[k]['p']})"); print(df.round(3).to_string(index=False)); print({a: round(v, 3) for a, v in r.items()})
    print(f"\nProb-weighted exit price {pw_px:.0f}; prob-wtd total multiple {pw_tot:.2f} -> CAGR {pw_tot**0.2-1:.1%}; mean of CAGRs {pw_cagr:.1%}")
    print('\nEntry-price CAGR table\n', (entry * 100).round(1))
    print('\nTornado (Base CAGR = %.1f%%)' % (sc['Base'][1]['cagr'] * 100)); [print(f"  {k}: {a:.1%} / {c:.1%}") for k, (a, c) in torn.items()]
    print('\nEPS valuation', {k: {a: round(x, 2) for a, x in v.items()} for k, v in eps_val.items()})
    # persist
    sens1.round(1).to_csv('output/dcf_sens_wacc_g.csv'); sens2.round(1).to_csv('output/dcf_sens_growth_margin.csv'); entry.round(4).to_csv('output/entry_price_cagr.csv')
    pd.concat({k: sc[k][0] for k in SCN}).round(3).to_csv('output/scenarios.csv')
