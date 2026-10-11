"""Lowe's (LOW) valuation model: DCF (unlevered FCF) + sensitivities, exit-multiple cross-check,
EPS x P/E valuation, and five-year bear/base/bull total-return scenarios.
$ in billions except per-share. Lowe's fiscal year ends ~Jan 31 (FY2026 = year ending Jan 29 2027).
Model EBIT is GAAP-basis (after acquired-intangible amortisation); 'adjusted' EPS adds amortisation back
(Lowe's schedule: $397m FY26, $329m FY27-29, $323m FY30; FY25 10-K). Run: python3 model.py"""
import json, copy, numpy as np, pandas as pd

# ---------------- Market & balance-sheet inputs (verified; see README source appendix) ----------------
PRICE, PRICE_DATE = 186.00, '2026-10-09'          # NYSE close
SHARES = 0.561054                                 # bn shares outstanding, 2026-08-25 (10-Q cover)
DEBT = 35.204 + 2.352                             # LT debt incl. finance leases + current maturities, 2026-07-31
CASH = 3.172 + 0.235                              # cash + short-term investments, 2026-07-31 (Q2 seasonal high)
NET_DEBT = DEBT - CASH                            # operating leases excluded from debt AND their cost left in EBIT (consistent)
FY25_SALES, FY26_SALES = 86.286, 92.0             # FY25 actual; FY26 guidance (Aug 19 2026)
DPS = 5.00                                        # $1.25 quarterly, annualised
# ---------------- Operating assumptions ----------------
TAX = 0.245                                       # guidance ~24.5%
DA_PCT = 0.028                                    # D&A incl. intangible amortisation / sales (TTM ~2.7%; FBM/ADG amortisation)
CAPEX_PCT = 0.027                                 # FY26 guide ~$2.5bn = 2.7% of sales
NWC_PCT = 0.05                                    # incremental NWC per $ of incremental sales (inventory largely vendor-funded)
INTEREST_FY26 = 1.60                              # guidance
AMORT = {2026: .397, 2027: .329, 2028: .329, 2029: .329, 2030: .323, 2031: .30}
WACC, TG = 0.0875, 0.025
# WACC build: rf 5.2% (10y UST 10/8/26) + beta 1.1 x ERP 4.5% = CoE 10.15%; pre-tax CoD 5.8% -> 4.4% after tax;
# weights E 104 / D 37.6 -> 0.735/0.265 -> 8.6%; rounded up to 8.75% for lease-adjusted leverage (~3.0x) and cyclicality.

def dcf(growth, margins, wacc=WACC, g=TG, full=False):
    """growth: FY27-30 sales growth; margins: FY26-30 GAAP EBIT margin. Valuation date Oct 2026."""
    sales = [FY26_SALES]
    for x in growth: sales.append(sales[-1] * (1 + x))
    prev, fcf = FY25_SALES, []
    for s, m in zip(sales, margins):
        f = s * m * (1 - TAX) + s * DA_PCT - s * CAPEX_PCT - (s - prev) * NWC_PCT; fcf.append(f); prev = s
    t = np.array([0.3, 1.3, 2.3, 3.3, 4.3]); w = np.array([0.25, 1, 1, 1, 1])   # only ~1 quarter of FY26 FCF remains
    pv = float((np.array(fcf) * w / (1 + wacc) ** t).sum())
    tv = fcf[-1] * (1 + g) / (wacc - g); pv_tv = tv / (1 + wacc) ** t[-1]
    ev = pv + pv_tv; ps = (ev - NET_DEBT) / SHARES
    if not full: return ps
    ebitda30 = sales[-1] * (margins[-1] + DA_PCT)
    return dict(sales=sales, fcf=fcf, pv_fcf=pv, tv=tv, pv_tv=pv_tv, ev=ev, equity=ev - NET_DEBT, per_share=ps,
                tv_pct_ev=pv_tv / ev, tv_implied_ev_ebitda=tv / ebitda30, tv_implied_fcf_yield=fcf[-1] * (1 + g) / tv)

BASE_G = [0.020, 0.035, 0.040, 0.040]                  # FY27-30 total sales growth (comps + ~1pt non-comp)
BASE_M = [0.112, 0.113, 0.116, 0.119, 0.121]           # FY26 = GAAP guide 11.2%
def exit_mult(mult, wacc=WACC):
    d = dcf(BASE_G, BASE_M, wacc, TG, full=True); e30 = d['sales'][-1] * (BASE_M[-1] + DA_PCT)
    return (d['pv_fcf'] + e30 * mult / (1 + wacc) ** 4.3 - NET_DEBT) / SHARES

# ---------------- 5-year scenarios: buy Oct 2026, sell Oct 2031 at exit P/E x FY2031E adjusted EPS (~NTM) ----------------
SCN = {
 'Bear': dict(p=0.30, comps=[0.0, -2.0, 0.0, 1.5, 2.0, 2.0], other=0.005, m=[0.112, 0.105, 0.103, 0.105, 0.107, 0.109],
              pe=12.5, lev=None, int_rate=0.050),
 'Base': dict(p=0.50, comps=[0.0, 1.0, 2.5, 3.0, 3.0, 3.0], other=0.010, m=[0.112, 0.113, 0.116, 0.119, 0.121, 0.122],
              pe=16.0, lev=2.6, int_rate=0.047),
 'Bull': dict(p=0.20, comps=[0.0, 3.0, 5.0, 4.5, 4.0, 3.5], other=0.012, m=[0.112, 0.117, 0.122, 0.126, 0.129, 0.131],
              pe=19.0, lev=2.6, int_rate=0.046),
}
# comps[0] = FY26 ('approximately flat' guide). lev = target net debt / GAAP EBITDA once buybacks resume (from FY27;
# mgmt target 2.75x lease-adjusted EBITDAR ~ 2.6x net debt/EBITDA ex-leases). Bear: no re-levering; buybacks only from
# FCF after dividends. int_rate = average cost of net debt (existing notes ~4%, refinancing at ~5.5-6%).
def scenario(s, iters=3):
    exit_px = PRICE * 1.5
    for _ in range(iters):  # buybacks executed along a geometric price path from today to the exit price
        sales, shares, nd, dps, rows = FY26_SALES, SHARES, NET_DEBT, DPS, []
        for i, yr in enumerate(range(2026, 2032)):
            gr = s['comps'][i] / 100 + s['other']
            if i: sales *= 1 + gr
            ebit = sales * s['m'][i]; ebitda = ebit + sales * DA_PCT
            interest = INTEREST_FY26 if i == 0 else nd * s['int_rate']
            ni = (ebit - interest) * (1 - TAX); eps = ni / shares; adj = eps + AMORT[yr] * (1 - TAX) / shares
            fcf = ni + sales * DA_PCT - sales * CAPEX_PCT - (sales * gr / (1 + gr) * NWC_PCT if i else 0)
            if i == 0: div, bb, new_nd = dps * shares, 0.30, nd       # FY26: Q1 buyback $0.36bn already done; pause otherwise
            else:
                div = dps * shares
                target = s['lev'] * ebitda if (s['lev'] and yr >= 2027) else None
                if yr == 2027 and target: target = (nd + target) / 2   # buybacks restart only after Q2 FY27
                cash_avail = fcf - div
                bb = max(0.0, cash_avail + (target - nd if target else 0)) if target else max(0.0, cash_avail * 0.8)
                new_nd = nd - (cash_avail - bb)
            px_t = PRICE * (exit_px / PRICE) ** (i / 5)
            rows.append(dict(FY=yr, sales=sales, comp=s['comps'][i], ebit_margin=s['m'][i], ebitda=ebitda, interest=interest,
                             net_income=ni, shares=shares, eps_gaap=eps, eps_adj=adj, fcf_equity=fcf, dps=dps, dividends=div,
                             buyback=bb, net_debt=new_nd, nd_ebitda=new_nd / ebitda))
            shares -= bb / px_t if i else 0
            nd = new_nd
            g_eps = (eps / rows[-2]['eps_gaap'] - 1) if len(rows) > 1 else 0.04
            dps *= 1 + min(0.05, max(0.01, g_eps))            # dividend growth floor 1% (52-yr record), cap 5%
        df = pd.DataFrame(rows)
        exit_eps = df.iloc[-1]['eps_adj']; exit_px = exit_eps * s['pe']
    divs = df.iloc[1:]['dps'].sum()                            # ~5 years of dividends (Oct 2026 - Oct 2031), not reinvested
    tot = (exit_px + divs) / PRICE
    return df, dict(fy27_eps_adj=df.iloc[1]['eps_adj'], exit_eps_adj=exit_eps, exit_pe=s['pe'], exit_price=exit_px,
                    dividends=divs, total_return=tot - 1, cagr=tot ** 0.2 - 1,
                    eps_cagr=(exit_eps / df.iloc[0]['eps_adj']) ** 0.2 - 1, share_count_chg=df.iloc[-1]['shares'] / SHARES - 1)

def stress():   # recession / housing double-dip: not in probability set, shown for permanent-loss analysis
    s = dict(p=0, comps=[0.0, -6.0, -2.0, 1.0, 2.0, 2.0], other=0.0, m=[0.112, 0.095, 0.092, 0.098, 0.102, 0.105],
             pe=11.0, lev=None, int_rate=0.055)
    return scenario(s)

sc = {k: scenario(v) for k, v in SCN.items()}
pw_tot = sum(SCN[k]['p'] * (1 + sc[k][1]['total_return']) for k in SCN)
PW = dict(exit_price=sum(SCN[k]['p'] * sc[k][1]['exit_price'] for k in SCN), cagr_of_expected=pw_tot ** 0.2 - 1,
          expected_cagr=sum(SCN[k]['p'] * sc[k][1]['cagr'] for k in SCN))
# value today = probability-weighted (exit price + dividends) discounted at cost of equity 10.15%
COE = 0.1015
PW['pv_today_at_coe'] = sum(SCN[k]['p'] * (sc[k][1]['exit_price'] + sc[k][1]['dividends']) for k in SCN) / (1 + COE) ** 5
for k in SCN: sc[k][1]['pv_today_at_coe'] = (sc[k][1]['exit_price'] + sc[k][1]['dividends']) / (1 + COE) ** 5

def entry_table(prices=(150, 160, 170, 186, 200, 215, 230, 250)):
    t = {}
    for P in prices:
        t[P] = {k: ((sc[k][1]['exit_price'] + sc[k][1]['dividends']) / P) ** 0.2 - 1 for k in SCN}
        t[P]['Expected (prob-wtd)'] = (sum(SCN[k]['p'] * (sc[k][1]['exit_price'] + sc[k][1]['dividends']) for k in SCN) / P) ** 0.2 - 1
    return pd.DataFrame(t).T

def base_cagr(**kw):
    s = copy.deepcopy(SCN['Base']); s.update(kw); return scenario(s)[1]['cagr']
B = SCN['Base']
TORNADO = {
 'Exit P/E 13x / 19x': (base_cagr(pe=13.0), base_cagr(pe=19.0)),
 'EBIT margin path -100bp / +100bp by FY31': (base_cagr(m=[B['m'][0]] + [x - 0.01 * (i + 1) / 5 for i, x in enumerate(B['m'][1:])]),
                                             base_cagr(m=[B['m'][0]] + [x + 0.01 * (i + 1) / 5 for i, x in enumerate(B['m'][1:])])),
 'Comps -1.5pt / +1.5pt p.a. (FY27-31)': (base_cagr(comps=[0.0] + [c - 1.5 for c in B['comps'][1:]]), base_cagr(comps=[0.0] + [c + 1.5 for c in B['comps'][1:]])),
 'No re-levering / 3.0x leverage': (base_cagr(lev=None), base_cagr(lev=3.0)),
 'Cost of net debt 5.75% / 4.0%': (base_cagr(int_rate=0.0575), base_cagr(int_rate=0.04)),
}
# EPS x P/E (value ~12 months out, on FY2027E adjusted EPS)
EPS_CASES = {'Conservative': (11.60, 13.0), 'Base': (12.80, 16.0), 'Optimistic': (13.70, 18.0)}

if __name__ == '__main__':
    pd.set_option('display.width', 220); R = {}
    d = dcf(BASE_G, BASE_M, full=True); R['dcf_base'] = d
    print(f"Mkt cap ${PRICE*SHARES:.1f}bn | net debt ${NET_DEBT:.2f}bn | EV ${PRICE*SHARES+NET_DEBT:.1f}bn")
    print('DCF base:', {k: (round(v, 3) if not isinstance(v, list) else [round(x, 2) for x in v]) for k, v in d.items()})
    s1 = pd.DataFrame({f"g={g:.1%}": {f"WACC {w:.2%}": dcf(BASE_G, BASE_M, w, g) for w in (0.0775, 0.0825, 0.0875, 0.0925, 0.0975)} for g in (0.015, 0.02, 0.025, 0.03)})
    s2 = pd.DataFrame({f"FY30 EBIT {m:.1%}": {f"growth {x:+.1%}/yr vs base": dcf([g + x for g in BASE_G], list(np.linspace(0.112, m, 5)))
                        for x in (-0.02, -0.01, 0.0, 0.01)} for m in (0.100, 0.110, 0.121, 0.130, 0.135)})
    em = {f"{m}x": exit_mult(m) for m in (8, 9, 10, 11, 12)}
    print('\nWACC x g\n', s1.round(0)); print('\nGrowth x margin\n', s2.round(0)); print('\nExit EV/EBITDA cross-check', {k: round(v) for k, v in em.items()})
    for k in SCN:
        df, r = sc[k]; print(f"\n== {k} p={SCN[k]['p']}"); print(df.round(3).to_string(index=False)); print({a: round(float(v), 3) for a, v in r.items()})
    sdf, sr = stress(); print('\n== Stress (not weighted)'); print(sdf[['FY', 'sales', 'eps_adj', 'nd_ebitda']].round(2).to_string(index=False)); print({a: round(float(v), 3) for a, v in sr.items()})
    print('\nProb-weighted:', {k: round(v, 3) for k, v in PW.items()})
    et = entry_table(); print('\nEntry price -> 5y CAGR (%)\n', (et * 100).round(1))
    print('\nTornado, base CAGR %.1f%%' % (sc['Base'][1]['cagr'] * 100)); [print(f"  {k}: {a:.1%} / {b:.1%}") for k, (a, b) in TORNADO.items()]
    ev = {k: dict(eps=e, pe=m, value=e * m, vs_price=e * m / PRICE - 1) for k, (e, m) in EPS_CASES.items()}; print('\nEPS x P/E', ev)
    s1.round(0).to_csv('output/dcf_sens_wacc_g.csv'); s2.round(0).to_csv('output/dcf_sens_growth_margin.csv')
    et.round(4).to_csv('output/entry_price_cagr.csv'); pd.concat({k: sc[k][0] for k in SCN} | {'Stress': sdf}).round(3).to_csv('output/scenarios.csv')
    json.dump({'dcf_base': {k: (v if isinstance(v, list) else float(v)) for k, v in d.items()}, 'exit_mult': em,
               'scenarios': {k: {a: float(v) for a, v in sc[k][1].items()} for k in SCN}, 'stress': {a: float(v) for a, v in sr.items()},
               'prob_weighted': PW, 'tornado': TORNADO, 'eps_val': ev}, open('output/model_results.json', 'w'), indent=1, default=float)
