"""Builds the Evercore (NYSE: EVR) mid-cycle earnings workbook.

Question it answers: what does EVR earn in an average year of the advisory cycle, how fast does
that "average year" grow, and what multiple of it is the market paying today?

Sheets: Summary, Inputs, History, MidCycle, Value, Sources.
Two independent estimates of mid-cycle revenue (trend line; SMD capacity x normal productivity),
one mid-cycle margin (margin regressed on revenue-vs-trend, read at trend), then a fading-growth
distribution model. All calculations are live formulas; hardcoded inputs are blue and sourced.
Run: python3 models/build_evr_midcycle.py  ->  models/EVR_MidCycle_Model.xlsx
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Font, PatternFill, Side, Border
from openpyxl.utils import get_column_letter as L

OUT = Path(__file__).with_name("EVR_MidCycle_Model.xlsx")

# ---------- styles (same conventions as build_fps_model.py) ----------
FONT = "Arial"
BLUE, BLACK, GREEN = "0000FF", "000000", "008000"
f_in = Font(name=FONT, size=10, color=BLUE)
f_calc = Font(name=FONT, size=10, color=BLACK)
f_link = Font(name=FONT, size=10, color=GREEN)
f_hdr = Font(name=FONT, size=10, bold=True, color="FFFFFF")
f_title = Font(name=FONT, size=14, bold=True)
f_note = Font(name=FONT, size=9, italic=True, color="595959")
fill_hdr = PatternFill("solid", fgColor="1F3864")
fill_key = PatternFill("solid", fgColor="FFFF00")
fill_sub = PatternFill("solid", fgColor="D9E1F2")
top_border = Border(top=Side(style="thin", color="808080"))

USD = '$#,##0;($#,##0);"-"'
USD1 = '$#,##0.0;($#,##0.0);"-"'
USD2 = '$#,##0.00;($#,##0.00);"-"'
NUM1 = '#,##0.0;(#,##0.0);"-"'
NUM0 = '#,##0;(#,##0);"-"'
PCT = '0.0%;(0.0%);"-"'
MULT = '0.0x;(0.0x);"-"'
YR = "0"
RATIO = '0.00;(0.00);"-"'


def put(ws, ref, value, font=f_calc, fmt=None, bold=False, fill=None, comment=None, align=None):
    c = ws[ref]
    c.value = value
    c.font = Font(name=FONT, size=font.size, color=font.color, bold=bold or font.bold, italic=font.italic)
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if comment:
        c.comment = Comment(comment, "Model")
    if align:
        c.alignment = Alignment(horizontal=align)
    return c


def section(ws, row, text, ncols=12):
    for col in range(1, ncols + 1):
        ws.cell(row=row, column=col).fill = fill_sub
    put(ws, f"A{row}", text, bold=True)


def widths(ws, first=46, rest=11, n=20):
    ws.column_dimensions["A"].width = first
    for i in range(2, n + 1):
        ws.column_dimensions[L(i)].width = rest


# ---------- source data ----------
SEC = "SEC EDGAR, Evercore Inc. (CIK 1360901)"
XBRL = f"{SEC} XBRL companyfacts, 10-K full-year values (latest restatement)"
# GAAP, $mm: net revenues, comp & benefits, total opex, pretax income, NI attrib. to EVR, diluted EPS, diluted shares (mm)
GAAP = {
    2009: (312.417, 207.592, 288.969, 22.042, -1.570, -0.10, 15.545),
    2010: (375.905, 247.737, 339.045, 36.303, 8.954, 0.39, 22.968),
    2011: (524.264, 357.680, 488.452, 36.731, 6.952, 0.23, 29.397),
    2012: (642.373, 430.415, 576.838, 70.387, 28.889, 0.89, 32.548),
    2013: (765.428, 485.794, 635.253, 138.501, 53.262, 1.38, 38.481),
    2014: (915.858, 549.516, 744.911, 176.127, 86.874, 2.08, 41.843),
    2015: (1223.273, 788.175, 1094.603, 134.720, 42.863, 0.98, 43.699),
    2016: (1440.052, 900.590, 1178.878, 267.815, 107.528, 2.43, 44.193),
    2017: (1704.349, 962.512, 1275.538, 437.649, 125.454, 2.80, 44.826),
    2018: (2064.705, 1197.173, 1522.628, 551.371, 377.240, 8.33, 45.279),
    2019: (2008.698, 1200.977, 1570.987, 448.707, 297.436, 6.89, 43.194),
    2020: (2263.905, 1372.339, 1737.472, 540.831, 350.574, 8.22, 42.623),
    2021: (3289.499, 1848.757, 2187.061, 1116.599, 740.116, 17.08, 43.321),
    2022: (2762.048, 1697.519, 2066.006, 704.041, 476.520, 11.61, 41.037),
    2023: (2425.949, 1656.875, 2066.814, 365.790, 255.479, 6.37, 40.099),
    2024: (2979.593, 1974.036, 2452.679, 533.145, 378.279, 9.08, 41.646),
    2025: (3855.820, 2500.834, 3065.878, 793.814, 591.922, 14.05, 42.131),
}
# Adjusted (company non-GAAP), $mm: net revenues, operating income, NI attrib., diluted EPS; source = Q4 release of year+1
# (2018 onward only: earlier years pre-date the 2018 gross-up of client expenses and the 2017 tax reform, so not comparable)
ADJ = {
    2018: (2083.2, 591.0, 454.0, 9.01, "Q4'19 release (8-K 29-Jan-2020) restated column; EPS from Q4'18 release 30-Jan-2019"),
    2019: (2032.6, 498.5, 373.3, 7.70, "Q4'19 release, 8-K filed 29-Jan-2020"),
    2020: (2327.3, 639.3, 459.6, 9.62, "Q4'20 release, 8-K filed 3-Feb-2021"),
    2021: (3316.9, 1138.4, 843.2, 17.50, "Q4'21 release, 8-K filed 2-Feb-2022"),
    2022: (2785.6, 722.7, 528.7, 12.01, "Q4'22 release, 8-K filed 1-Feb-2023"),
    2023: (2449.3, 385.4, 276.9, 6.46, "Q4'23 release, 8-K filed 31-Jan-2024"),
    2024: (3002.6, 557.3, 415.8, 9.42, "Q4'24 release, 8-K filed 5-Feb-2025"),
    2025: (3884.0, 838.6, 646.3, 14.56, "Q4'25 release, 8-K filed 4-Feb-2026"),
}
# Advisory / Investment Banking SMDs at year end
SMD = {
    2012: (60, "10-K FY2012: 60 SMDs in Investment Banking"),
    2013: (67, "10-K FY2013: 67 SMDs in Investment Banking"),
    2014: (68, "10-K FY2014: 68 advisory SMDs"),
    2015: (79, "10-K FY2015: 79 Advisory SMDs"),
    2016: (81, "10-K FY2016: 81 Advisory SMDs"),
    2017: (87, "10-K FY2017: 87 SMDs in strategic and capital markets advisory"),
    2018: (98, "10-K FY2018: 98 SMDs in strategic and capital markets advisory"),
    2019: (112, "10-K FY2019: 112 SMDs in strategic and capital markets advisory"),
    2020: (107, "Q4'21 release: 107 Advisory SMDs at 31-Dec-2020 (company-adjusted for commits/departures)"),
    2021: (114, "Q4'21 release: 114 Advisory SMDs (adjusted for commits/departures)"),
    2022: (130, "Q4'22 release: 130 Advisory SMDs (adjusted for commits/departures)"),
    2023: (136, "Q4'23 release: 136 Advisory SMDs (adjusted for commits/departures)"),
    2024: (144, "Q4'24 release: 144 Investment Banking SMDs (adjusted for commits/departures)"),
    2025: (171, "Q4'25 release: 171 Investment Banking SMDs (adjusted for commits/departures)"),
}
Y0, Y1 = 2009, 2025
YEARS = list(range(Y0, Y1 + 1))


def col(y):
    return L(2 + y - Y0)


C0, C1 = col(Y0), col(Y1)
A0, A1 = col(2018), col(2025)  # adjusted-data window

wb = Workbook()

# =====================================================================
# INPUTS
# =====================================================================
inp = wb.active
inp.title = "Inputs"
widths(inp, 58, 12, 4)
inp.column_dimensions["C"].width = 90
put(inp, "A1", "Evercore (NYSE: EVR) - Mid-Cycle Earnings Inputs", f_title)
put(inp, "A2", "$ in millions except per-share. Blue = hardcoded input; black = formula; green = link; "
    "yellow = key judgement call. Change any blue cell and the workbook recalculates.", f_note)
IN = {}


def inrow(r, key, label, val, fmt, note, key_fill=False):
    put(inp, f"A{r}", label)
    put(inp, f"B{r}", val, f_in, fmt, fill=fill_key if key_fill else None)
    put(inp, f"C{r}", note, f_note)
    IN[key] = f"Inputs!$B${r}"


section(inp, 4, "Market data", 3)
inrow(5, "PX", "Share price ($)", 268.08, USD2, "Close 6-Oct-2026, as provided by user (not independently re-checked).")
inrow(6, "HI", "52-week high ($)", 388.71, USD2, "As provided by user.")
inrow(7, "CONS27", "Consensus 2027E EPS, adjusted ($)", 22.19, USD2,
      "As provided by user. Consensus is on Evercore's Adjusted basis, so this model uses Adjusted EPS throughout.")
inrow(8, "H1NI", "H1 2026 Adjusted NI attributable to EVR ($mm)", 461.8, USD1, "Q2'26 release, 8-K filed 29-Jul-2026.")
inrow(9, "H1EPS", "H1 2026 Adjusted diluted EPS ($)", 10.48, USD2, "Q2'26 release, 8-K filed 29-Jul-2026.")
put(inp, "A10", "Current Adjusted diluted shares (mm)", bold=True)
put(inp, "B10", "=B8/B9", fmt=NUM1, bold=True)
put(inp, "C10", "Implied: H1'26 Adjusted NI / Adjusted EPS.", f_note)
IN["SH"] = "Inputs!$B$10"

section(inp, 12, "Method 1 - revenue trend line", 3)
inrow(13, "TS", "Trend window start year", 2016, YR,
      "KEY CHOICE. 2009-2015 was a start-up/scale-up phase (revenue +16%/yr) that would bias the trend "
      "upward; 2016 start = post-ISI-acquisition, mature firm, spans 2019/2023 troughs and 2021 peak.", True)
inrow(14, "TE", "Trend window end year", 2025, YR, "Last full fiscal year reported.")
inrow(15, "VY", "Mid-cycle base year", 2026, YR, "Year for which mid-cycle earnings are estimated.")

section(inp, 17, "Method 2 - SMD capacity x normal productivity", 3)
inrow(18, "SMDN", "Investment Banking SMDs now", 188, NUM0,
      "30-Jun-2026, incl. commits, net of known departures. Q2'26 release.")
inrow(19, "SMDP", "Investment Banking SMDs one year earlier", 159, NUM0, "30-Jun-2025, same basis. Q2'26 release.")
inrow(20, "RAMP", "Productivity of SMDs added in last 12m (vs. tenured)", 0.5, PCT,
      "Assumption: lateral/promoted SMDs typically take 2-3 years to reach full productivity. "
      "Also absorbs that the count includes commits not yet on board.", True)

section(inp, 22, "Blend & earnings conversion", 3)
inrow(23, "W1", "Weight on Method 1 (trend) vs Method 2 (capacity)", 0.5, PCT,
      "Assumption. Method 2 reflects today's firm; Method 1 reflects the past path. Equal weight absent a reason to prefer.",
      True)

section(inp, 25, "Growth of mid-cycle earnings  (g = fee-pool growth + share gains)", 3)
inrow(26, "GPOOL", "Industry fee-pool growth, through-cycle (nominal)", 0.045, PCT,
      "Assumption. Over full cycles, advisory fees track deal value, which tracks corporate value / nominal GDP "
      "(~4-5%). No buyback term: value is computed on total company distributions, then divided by today's "
      "shares - adding buyback-driven EPS growth too would double count.", True)
inrow(27, "GSHARE", "Share-gain contribution in year 1", 0.03, PCT,
      "Assumption. Fades linearly to zero by year 10. History: SMDs +8%/yr 2016-25 but revenue/SMD flat in "
      "nominal terms, so headcount growth has not translated 1:1 into share.", True)
inrow(28, "GT", "Terminal growth (after year 10)", 0.04, PCT, "Assumption. At or below nominal GDP.", True)
inrow(29, "ROE", "Return on equity on incremental capital", 0.30, PCT,
      "Assumption. Sets reinvestment = g / ROE; payout = 1 - g/ROE. 2025 Adjusted NI / avg equity was ~35% "
      "at above-mid-cycle earnings. Growth here is funded mostly through comp (already in margins), so payout is high.")

section(inp, 31, "Cost of equity (CAPM)", 3)
inrow(32, "RF", "Risk-free rate (10-year UST)", 0.0528, PCT, "As provided by user (10-year at 5.28%, up ~110bp YTD). Not re-checked.")
inrow(33, "BETA", "Equity beta", 1.40, RATIO,
      "Assumption - verify against a data provider. Advisory boutiques typically screen 1.3-1.6.", True)
inrow(34, "ERP", "Equity risk premium", 0.05, PCT, "Assumption.")
put(inp, "A35", "Cost of equity", bold=True)
put(inp, "B35", "=B32+B33*B34", fmt=PCT, bold=True)
IN["R"] = "Inputs!$B$35"
inrow(36, "RFCHG", "Change in 10-year yield this year (for rate-effect check)", 0.011, PCT,
      "As provided by user (~110bp). Used only on Summary to show how much of the de-rating rates alone explain.")

# =====================================================================
# HISTORY
# =====================================================================
hs = wb.create_sheet("History")
widths(hs, 46, 10, 2 + len(YEARS))
put(hs, "A1", "Evercore - Reported History, 2009-2025", f_title)
put(hs, "A2", "$ in millions except per-share. GAAP from XBRL; Adjusted (non-GAAP) and SMD counts from earnings releases "
    "and 10-Ks. Each blue cell carries its source in a comment. Years are calendar = fiscal.", f_note)
put(hs, "A4", "Year", bold=True)
for y in YEARS:
    c = put(hs, f"{col(y)}4", y, fmt=YR, bold=True, align="center")
    c.fill = fill_hdr
    c.font = f_hdr
hs["A4"].fill = fill_hdr
hs["A4"].font = f_hdr

R = {}
section(hs, 5, "Reported - U.S. GAAP", 2 + len(YEARS))
glabels = [("REV", "Net revenues", USD), ("COMP", "Employee compensation & benefits", USD),
           ("OPEX", "Total operating expenses", USD), ("PTI", "Pre-tax income", USD),
           ("NI", "Net income attributable to Evercore", USD), ("EPS", "Diluted EPS ($)", USD2),
           ("DSH", "Diluted shares (mm)", NUM1)]
for i, (k, lab, fmt) in enumerate(glabels):
    r = 6 + i
    R[k] = r
    put(hs, f"A{r}", lab)
    for y in YEARS:
        put(hs, f"{col(y)}{r}", GAAP[y][i], f_in, fmt,
            comment=f"{XBRL}. Tag: " + ["RevenuesNetOfInterestExpense", "LaborAndRelatedExpense", "OperatingExpenses",
                                        "IncomeLossFromContinuingOperationsBefore...NoncontrollingInterest",
                                        "NetIncomeLoss", "EarningsPerShareDiluted",
                                        "WeightedAverageNumberOfDilutedSharesOutstanding"][i] if y == Y0 else None)
put(hs, f"A{R['REV']}", "Net revenues", bold=True)

section(hs, 14, "Reported - Adjusted (company non-GAAP basis; consensus is on this basis)", 2 + len(YEARS))
alabels = [("AREV", "Adjusted net revenues", USD), ("AOP", "Adjusted operating income", USD),
           ("ANI", "Adjusted net income attributable to Evercore", USD), ("AEPS", "Adjusted diluted EPS ($)", USD2)]
for i, (k, lab, fmt) in enumerate(alabels):
    r = 15 + i
    R[k] = r
    put(hs, f"A{r}", lab)
    for y, v in ADJ.items():
        put(hs, f"{col(y)}{r}", v[i], f_in, fmt, comment=f"{SEC}. {v[4]}." if i == 0 else None)
r = 19
R["SMD"] = r
put(hs, f"A{r}", "Investment Banking / Advisory SMDs, year end")
for y, (v, src) in SMD.items():
    put(hs, f"{col(y)}{r}", v, f_in, NUM0, comment=f"{SEC}. {src}.")

section(hs, 21, "Derived ratios", 2 + len(YEARS))
derived = [
    ("CR", "GAAP compensation ratio", PCT, lambda c: f"={c}{R['COMP']}/{c}{R['REV']}", YEARS),
    ("NCR", "GAAP non-comp opex / revenue", PCT, lambda c: f"=({c}{R['OPEX']}-{c}{R['COMP']})/{c}{R['REV']}", YEARS),
    ("AOPM", "Adjusted operating margin", PCT, lambda c: f"={c}{R['AOP']}/{c}{R['AREV']}", list(ADJ)),
    ("CONV", "Adjusted NI / Adjusted operating income (tax, NCI, other)", PCT,
     lambda c: f"={c}{R['ANI']}/{c}{R['AOP']}", list(ADJ)),
    ("ASH", "Adjusted diluted shares (mm) = Adj NI / Adj EPS", NUM1, lambda c: f"={c}{R['ANI']}/{c}{R['AEPS']}", list(ADJ)),
    ("RPS", "Net revenue per SMD ($mm)", NUM1, lambda c: f"={c}{R['REV']}/{c}{R['SMD']}", list(SMD)),
    ("LN", "LN(net revenue)  [helper for trend regression]", RATIO, lambda c: f"=LN({c}{R['REV']})", YEARS),
    ("TREND", "Trend net revenue (Method 1 line)", USD,
     lambda c: f"=EXP(MidCycle!$C$8+MidCycle!$C$7*{c}$4)", YEARS),
    ("RVT", "Revenue / trend  (>1 = above-trend year)", RATIO, lambda c: f"={c}{R['REV']}/{c}{R['TREND'] if 'TREND' in R else 0}", YEARS),
    ("RVTX", "Revenue / trend - 1  [regressor for margin]", PCT, lambda c: f"={c}{R['RVT'] if 'RVT' in R else 0}-1", list(ADJ)),
    ("MEPS", "Mid-cycle Adjusted EPS at the time (trend rev x mid-cycle margin x conversion / shares)", USD2,
     lambda c: f"={c}{R['TREND']}*MidCycle!$C$22*MidCycle!$C$24/{c}{R['ASH']}", list(ADJ)),
    ("CYC", "Actual Adjusted EPS / mid-cycle EPS  (cycle position)", RATIO,
     lambda c: f"={c}{R['AEPS']}/{c}{R['MEPS']}", list(ADJ)),
]
for i, (k, lab, fmt, fn, yrs) in enumerate(derived):
    R[k] = 22 + i
for k, lab, fmt, fn, yrs in derived:
    r = R[k]
    put(hs, f"A{r}", lab)
    for y in yrs:
        put(hs, f"{col(y)}{r}", fn(col(y)), fmt=fmt)
put(hs, f"A{R['CYC'] + 2}", "Revenue per SMD uses total net revenue (incl. Equities and Wealth Management, ~10-15% of "
    "revenue) over year-end advisory SMDs; before 2015 it is distorted by the ISI acquisition (Oct-2014). "
    "SMD counts from 2020 are company-adjusted to include committed hires.", f_note)
hs.freeze_panes = "B5"

# =====================================================================
# MIDCYCLE
# =====================================================================
mc = wb.create_sheet("MidCycle")
widths(mc, 4, 12, 6)
mc.column_dimensions["B"].width = 64
mc.column_dimensions["D"].width = 80
put(mc, "A1", "Evercore - Mid-Cycle Earnings Estimate", f_title)
put(mc, "A2", "Principle: earnings = revenue x margin. Split each into a cyclical part (average it out) and a structural "
    "part (trend it forward).", f_note)
rng_ln = f"INDEX(History!${C0}${R['LN']}:${C1}${R['LN']},MATCH({IN['TS']},History!${C0}$4:${C1}$4,0)):" \
         f"INDEX(History!${C0}${R['LN']}:${C1}${R['LN']},MATCH({IN['TE']},History!${C0}$4:${C1}$4,0))"
rng_yr = f"INDEX(History!${C0}$4:${C1}$4,MATCH({IN['TS']},History!${C0}$4:${C1}$4,0)):" \
         f"INDEX(History!${C0}$4:${C1}$4,MATCH({IN['TE']},History!${C0}$4:${C1}$4,0))"
rng_rps = f"INDEX(History!${C0}${R['RPS']}:${C1}${R['RPS']},MATCH({IN['TS']},History!${C0}$4:${C1}$4,0)):" \
          f"INDEX(History!${C0}${R['RPS']}:${C1}${R['RPS']},MATCH({IN['TE']},History!${C0}$4:${C1}$4,0))"
rows = [
    (4, None, "1. Mid-cycle REVENUE", None, None),
    (6, "Method 1 - log-linear trend of GAAP net revenue over the chosen window", None, None, None),
    (7, "Trend slope (log points / year)", f"=SLOPE({rng_ln},{rng_yr})", RATIO, "Least-squares fit of LN(revenue) on year."),
    (8, "Trend intercept", f"=INTERCEPT({rng_ln},{rng_yr})", RATIO, None),
    (9, "Trend growth rate", "=EXP(C7)-1", PCT, "Through-cycle revenue growth implied by the window. Very sensitive to the start year (see note)."),
    (10, "Mid-cycle revenue, base year - Method 1", f"=EXP(C8+C7*{IN['VY']})", USD, "Point on the trend line in the base year."),
    (12, "Method 2 - SMD capacity x normal revenue per SMD", None, None, None),
    (13, "Normal revenue per SMD (window average, $mm)", f"=AVERAGE({rng_rps})", NUM1,
     "Average over the same window, so booms and busts net out. Nominal: it has been ~flat since 2016."),
    (14, "SMDs added in last 12 months", f"={IN['SMDN']}-{IN['SMDP']}", NUM0, None),
    (15, "Productive-equivalent SMDs", f"={IN['SMDN']}-C14*(1-{IN['RAMP']})", NUM1, "New SMDs counted at the ramp-productivity input."),
    (16, "Mid-cycle revenue, base year - Method 2", "=C13*C15", USD, None),
    (18, "Blended mid-cycle revenue", f"={IN['W1']}*C10+(1-{IN['W1']})*C16", USD,
     "If Methods 1 and 2 disagree by >15%, one of the inputs is wrong - check before trusting either."),
    (19, "Method 2 / Method 1 - 1", "=C16/C10-1", PCT, None),
    (20, None, "2. Mid-cycle MARGIN and earnings conversion", None, None),
    (21, "Operating leverage: margin change per +100% revenue vs trend",
     f"=SLOPE(History!{A0}{R['AOPM']}:{A1}{R['AOPM']},History!{A0}{R['RVTX']}:{A1}{R['RVTX']})", PCT,
     "Regression of Adjusted operating margin on (revenue/trend - 1), 2018-2025. Sticky comp means margin rises in booms."),
    (22, "Mid-cycle Adjusted operating margin (regression read at trend)",
     f"=INTERCEPT(History!{A0}{R['AOPM']}:{A1}{R['AOPM']},History!{A0}{R['RVTX']}:{A1}{R['RVTX']})", PCT,
     "Margin the firm earns when revenue is exactly on trend. Better than a simple average if the sample is skewed to booms or busts."),
    (23, "Memo: simple average Adjusted operating margin 2018-2025",
     f"=AVERAGE(History!{A0}{R['AOPM']}:{A1}{R['AOPM']})", PCT, "Cross-check on C22."),
    (24, "Adjusted NI / operating income (avg 2018-2025)",
     f"=AVERAGE(History!{A0}{R['CONV']}:{A1}{R['CONV']})", PCT,
     "Captures tax rate (incl. recurring Q1 share-vesting tax benefits), NCI and other items. Post-2017 tax reform only."),
    (26, None, "3. Mid-cycle EARNINGS", None, None),
    (27, "Mid-cycle Adjusted operating income ($mm)", "=C18*C22", USD, None),
    (28, "Mid-cycle Adjusted NI ($mm)", "=C27*C24", USD, None),
    (29, "Mid-cycle Adjusted EPS, base year ($)", f"=C28/{IN['SH']}", USD2, "On today's diluted share count."),
    (30, "Memo: Method 1 only EPS", f"=C10*C22*C24/{IN['SH']}", USD2, None),
    (31, "Memo: Method 2 only EPS", f"=C16*C22*C24/{IN['SH']}", USD2, None),
    (33, None, "4. What the market and consensus imply", None, None),
    (34, "Mid-cycle EPS, base year + 1 ($)", f"=C29*(1+{IN['GPOOL']}+{IN['GSHARE']})", USD2,
     "One year of mid-cycle growth (Value sheet, year 1)."),
    (35, "Consensus next-year EPS ($)", f"={IN['CONS27']}", USD2, None),
    (36, "Consensus vs mid-cycle (same year)", "=C35/C34-1", PCT,
     "How far above an average year consensus sits. Large positive = consensus is a peak-year number."),
    (37, "P/E on consensus", f"={IN['PX']}/C35", MULT, "The headline '12x'."),
    (38, "P/E on mid-cycle EPS (same year)", f"={IN['PX']}/C34", MULT, "The multiple that actually matters for a cyclical."),
    (39, "P/E at 52-week high on mid-cycle EPS", f"={IN['HI']}/C34", MULT, None),
]
for r, lab, f, fmt, note in rows:
    if lab is None and f is not None:  # section header (label passed in f slot)
        section(mc, r, "", 4)
        put(mc, f"B{r}", f, bold=True)
        continue
    if f is None:
        put(mc, f"B{r}", lab, bold=True)
        continue
    put(mc, f"B{r}", lab)
    put(mc, f"C{r}", f, fmt=fmt, bold=r in (10, 16, 18, 22, 29, 38))
    if note:
        put(mc, f"D{r}", note, f_note)
for r in (18, 22, 29, 38):
    mc[f"C{r}"].fill = fill_key

# =====================================================================
# VALUE
# =====================================================================
vs = wb.create_sheet("Value")
widths(vs, 50, 11, 14)
put(vs, "A1", "Evercore - Growth of Mid-Cycle Earnings and Value", f_title)
put(vs, "A2", "Value = present value of the distributable earnings of an AVERAGE year, growing at fee-pool growth plus "
    "fading share gains. Cash flows at year end; valuation as of the base year.", f_note)
N = 10
put(vs, "A4", "Year index (t)", bold=True)
put(vs, "A5", "Calendar year", bold=True)
for t in range(0, N + 1):
    c = L(2 + t)
    put(vs, f"{c}4", t, fmt=YR, align="center")
    put(vs, f"{c}5", f"={IN['VY']}+{t}", fmt=YR, bold=True, align="center")
labels = {6: "Fee-pool growth", 7: "Share-gain contribution (fades to 0)", 8: "Mid-cycle NI growth (g)",
          9: "Mid-cycle Adjusted NI ($mm)", 10: "Payout ratio = 1 - g / ROE", 11: "Distributable earnings ($mm)",
          12: "Discount factor", 13: "PV of distributions ($mm)", 14: "Memo: mid-cycle EPS on today's shares ($)"}
for r, lab in labels.items():
    put(vs, f"A{r}", lab)
put(vs, "B9", "=MidCycle!C28", f_link, USD)
put(vs, "B14", f"=B9/{IN['SH']}", fmt=USD2)
for t in range(1, N + 1):
    c, p = L(2 + t), L(1 + t)
    put(vs, f"{c}6", f"={IN['GPOOL']}", fmt=PCT)
    put(vs, f"{c}7", f"={IN['GSHARE']}*MAX(0,({N}-{c}4)/({N}-1))", fmt=PCT)
    put(vs, f"{c}8", f"={c}6+{c}7", fmt=PCT)
    put(vs, f"{c}9", f"={p}9*(1+{c}8)", fmt=USD)
    put(vs, f"{c}10", f"=1-{c}8/{IN['ROE']}", fmt=PCT)
    put(vs, f"{c}11", f"={c}9*{c}10", fmt=USD)
    put(vs, f"{c}12", f"=1/(1+{IN['R']})^{c}4", fmt=RATIO)
    put(vs, f"{c}13", f"={c}11*{c}12", fmt=USD)
    put(vs, f"{c}14", f"={c}9/{IN['SH']}", fmt=USD2)
LC = L(2 + N)
section(vs, 16, "Valuation", 12)
vrows = [
    (17, "Sum of PV, years 1-10 ($mm)", f"=SUM(C13:{LC}13)", USD),
    (18, "Terminal value at year 10 ($mm)",
     f"={LC}9*(1+{IN['GT']})*(1-{IN['GT']}/{IN['ROE']})/({IN['R']}-{IN['GT']})", USD),
    (19, "PV of terminal value ($mm)", f"=B18*{LC}12", USD),
    (20, "Equity value ($mm)", "=B17+B19", USD),
    (21, "Value per share ($)", f"=B20/{IN['SH']}", USD2),
    (22, "Current price ($)", f"={IN['PX']}", USD2),
    (23, "Upside / (downside)", "=B21/B22-1", PCT),
    (24, "Implied fair P/E on base-year mid-cycle EPS", "=B21/MidCycle!C29", MULT),
    (25, "Terminal value share of equity value", "=B19/B20", PCT),
]
for r, lab, f, fmt in vrows:
    put(vs, f"A{r}", lab, bold=r in (21, 23))
    put(vs, f"B{r}", f, fmt=fmt, bold=r in (21, 23))
vs["B21"].fill = fill_key
put(vs, "A26", "No net-cash adjustment: Evercore's cash largely funds accrued year-end bonuses, so it is treated as "
    "operating. Excess cash would add to value.", f_note)

section(vs, 28, "Reverse test: what perpetual growth in mid-cycle earnings does today's price imply?", 12)
put(vs, "A29", "Next-year mid-cycle EPS (E1)")
put(vs, "B29", "=MidCycle!C34", f_link, USD2)
put(vs, "A30", "Implied perpetual g  [solves P = E1 (1 - g/ROE) / (r - g)]")
put(vs, "B30", f"=({IN['PX']}*{IN['R']}-B29)/({IN['PX']}-B29/{IN['ROE']})", fmt=PCT, bold=True)
vs["B30"].fill = fill_key
put(vs, "A31", "Compare with fee-pool growth input")
put(vs, "B31", f"={IN['GPOOL']}", f_link, PCT)

section(vs, 33, "Sensitivity: single-stage value per share = E1 x (1 - g/ROE) / (r - g)", 12)
put(vs, "A34", "Cost of equity (down) / perpetual g (across)", bold=True)
GS = [0.03, 0.04, 0.05, 0.06, 0.07]
RS = [0.09, 0.10, 0.11, 0.12, 0.13]
for j, g in enumerate(GS):
    put(vs, f"{L(2 + j)}34", g, f_in, PCT, bold=True, align="center")
for i, rr in enumerate(RS):
    r = 35 + i
    put(vs, f"A{r}", rr, f_in, PCT, bold=True, align="right")
    for j in range(len(GS)):
        c = L(2 + j)
        put(vs, f"{c}{r}", f"=IF($A{r}>{c}$34,$B$29*(1-{c}$34/{IN['ROE']})/($A{r}-{c}$34),NA())", fmt=USD)
put(vs, "A41", "Price ($) for comparison")
put(vs, "B41", f"={IN['PX']}", f_link, USD2)

# =====================================================================
# SUMMARY
# =====================================================================
sm = wb.create_sheet("Summary", 0)
widths(sm, 62, 14, 3)
sm.column_dimensions["C"].width = 90
put(sm, "A1", "Evercore (EVR) - What Is an Average Year Worth?", f_title)
put(sm, "A2", "All figures link to the model; change Inputs and this page updates. Adjusted (non-GAAP) EPS basis "
    "to match consensus.", f_note)
srows = [
    (4, "Mid-cycle EPS today", None, None, None),
    (5, "Mid-cycle Adjusted EPS, base year", "=MidCycle!C29", USD2, "Blend of trend-line and SMD-capacity methods."),
    (6, "   Method 1 (trend) only", "=MidCycle!C30", USD2, None),
    (7, "   Method 2 (capacity) only", "=MidCycle!C31", USD2, None),
    (8, "Mid-cycle operating margin", "=MidCycle!C22", PCT, "Read off margin-vs-revenue regression at trend revenue."),
    (9, "Mid-cycle EPS, next year", "=MidCycle!C34", USD2, None),
    (10, "Consensus next-year EPS", f"={IN['CONS27']}", USD2, None),
    (11, "Consensus above mid-cycle by", "=MidCycle!C36", PCT, "Positive = consensus assumes an above-average year continues."),
    (13, "Multiples", None, None, None),
    (14, "P/E on consensus", "=MidCycle!C37", MULT, "Looks cheap..."),
    (15, "P/E on mid-cycle EPS", "=MidCycle!C38", MULT, "...the cyclical-correct read."),
    (16, "P/E on mid-cycle EPS at the 52-week high", "=MidCycle!C39", MULT, "How rich the peak was."),
    (17, "Fair P/E on mid-cycle EPS (model)", "=Value!B24", MULT, None),
    (19, "Value", None, None, None),
    (20, "Value per share (fading-growth model)", "=Value!B21", USD2, None),
    (21, "Upside / (downside) vs price", "=Value!B23", PCT, None),
    (22, "Perpetual growth in mid-cycle earnings implied by price", "=Value!B30", PCT,
     "Compare with ~4-5% fee-pool growth. Higher = price already pays for continued share gains."),
    (24, "Rate effect (how much of the de-rating rates alone explain)", None, None, None),
    (25, "Single-stage fair P/E at current cost of equity",
     f"=(1-{IN['GT']}/{IN['ROE']})/({IN['R']}-{IN['GT']})", MULT, "At terminal growth input."),
    (26, "Same, with risk-free rate lower by the YTD rise",
     f"=(1-{IN['GT']}/{IN['ROE']})/({IN['R']}-{IN['RFCHG']}-{IN['GT']})", MULT, None),
    (27, "Multiple compression from rates alone", "=B25/B26-1", PCT,
     "Compare with the ~31% peak-to-now price fall."),
    (28, "Peak-to-now price change", f"={IN['PX']}/{IN['HI']}-1", PCT, None),
]
for r, lab, f, fmt, note in srows:
    if f is None:
        section(sm, r, lab, 3)
        continue
    put(sm, f"A{r}", lab)
    put(sm, f"B{r}", f, f_link if "!" in f else f_calc, fmt, bold=r in (5, 15, 20, 22))
    if note:
        put(sm, f"C{r}", note, f_note)
for r in (5, 15, 22):
    sm[f"B{r}"].fill = fill_key

# chart: actual vs mid-cycle EPS
ch = LineChart()
ch.title = "Adjusted EPS: actual vs mid-cycle (trend method)"
ch.y_axis.title = "$ / share"
ch.height, ch.width = 7.5, 16
data = Reference(hs, min_col=2 + 2018 - Y0, max_col=2 + 2025 - Y0, min_row=R["AEPS"], max_row=R["AEPS"])
ch.add_data(data, from_rows=True, titles_from_data=False)
ch.add_data(Reference(hs, min_col=2 + 2018 - Y0, max_col=2 + 2025 - Y0, min_row=R["MEPS"], max_row=R["MEPS"]),
            from_rows=True, titles_from_data=False)
ch.set_categories(Reference(hs, min_col=2 + 2018 - Y0, max_col=2 + 2025 - Y0, min_row=4, max_row=4))
ch.series[0].tx = None
from openpyxl.chart.series import SeriesLabel
ch.series[0].tx = SeriesLabel(v="Actual Adjusted EPS")
ch.series[1].tx = SeriesLabel(v="Mid-cycle EPS")
sm.add_chart(ch, "A31")

ch2 = LineChart()
ch2.title = "Net revenue vs trend line ($mm)"
ch2.height, ch2.width = 7.5, 16
ch2.add_data(Reference(hs, min_col=2, max_col=1 + len(YEARS), min_row=R["REV"], max_row=R["REV"]),
             from_rows=True, titles_from_data=False)
ch2.add_data(Reference(hs, min_col=2, max_col=1 + len(YEARS), min_row=R["TREND"], max_row=R["TREND"]),
             from_rows=True, titles_from_data=False)
ch2.set_categories(Reference(hs, min_col=2, max_col=1 + len(YEARS), min_row=4, max_row=4))
ch2.series[0].tx = SeriesLabel(v="Net revenue")
ch2.series[1].tx = SeriesLabel(v="Trend (window per Inputs)")
sm.add_chart(ch2, "C31")

# =====================================================================
# SOURCES
# =====================================================================
so = wb.create_sheet("Sources")
so.column_dimensions["A"].width = 150
notes = [
    "SOURCES",
    "GAAP history: SEC EDGAR XBRL companyfacts API, CIK 0001360901 (https://data.sec.gov/api/xbrl/companyfacts/CIK0001360901.json), "
    "10-K full-year durations; latest filed value used where restated.",
    "Adjusted results: Evercore Q4 earnings releases (Exhibit 99.1 to 8-K, Item 2.02) filed 29-Jan-2020, 3-Feb-2021, 2-Feb-2022, "
    "1-Feb-2023, 31-Jan-2024, 5-Feb-2025, 4-Feb-2026; H1 2026 from the Q2'26 release filed 29-Jul-2026.",
    "SMD counts: 10-K Item 1 (2012-2019) and earnings-release headcount footnotes (2020-2026). Definitions drift slightly "
    "('Advisory' -> 'Investment Banking'; company-adjusted for commits from 2020).",
    "User-provided (not independently re-checked): share price 268.08 (6-Oct-2026), 52-week high 388.71, 2027E consensus EPS "
    "22.19, 10-year UST 5.28% and ~110bp YTD rise.",
    "",
    "KNOWN LIMITATIONS",
    "1. Trend line is sensitive to the window: 2009-2025 gives ~16%/yr growth (start-up phase), 2016-2025 ~9.5%, 2018-2025 ~8%. "
    "Default is 2016.",
    "2. Margin regression has only 8 observations (2018-2025), roughly one cycle. Treat the mid-cycle margin as +/- 2pp.",
    "3. Adjusted NI conversion includes Q1 share-vesting tax benefits, which scale with the share price (Q1'26: $94mm "
    "Adjusted). Lower prices shrink this benefit - a small reflexive effect not modelled.",
    "4. Revenue per SMD uses total firm revenue; Equities and Wealth Management are not driven by advisory SMDs.",
    "5. Pre-2018 adjusted figures are excluded (client-expense gross-up and the 2017 tax reform break comparability).",
]
for i, t in enumerate(notes):
    put(so, f"A{i + 1}", t, bold=t.isupper() and len(t) < 30)

for ws in wb.worksheets:
    ws.sheet_view.showGridLines = False
wb.save(OUT)
print(f"wrote {OUT}")
