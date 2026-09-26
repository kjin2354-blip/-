"""Builds the Forgent Power Solutions (NYSE: FPS) valuation workbook.

Sheets: Cover, Inputs, Historicals, DCF, WACC, Sensitivity, Comps, Precedents, Summary.
All calculations are live Excel formulas; hardcoded inputs are blue and sourced.
Run: python3 models/build_fps_model.py  ->  models/FPS_Valuation_Model.xlsx
"""
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L

from fps_data import COMPS, PRECEDENTS, COMPS_ASOF, COMPS_NOTES, PRECEDENT_NOTES

OUT = Path(__file__).with_name("FPS_Valuation_Model.xlsx")

# ---------- styles ----------
FONT = "Arial"
BLUE, BLACK, GREEN = "0000FF", "000000", "008000"
f_in = Font(name=FONT, size=10, color=BLUE)
f_calc = Font(name=FONT, size=10, color=BLACK)
f_link = Font(name=FONT, size=10, color=GREEN)
f_bold = Font(name=FONT, size=10, bold=True)
f_hdr = Font(name=FONT, size=10, bold=True, color="FFFFFF")
f_title = Font(name=FONT, size=14, bold=True)
f_note = Font(name=FONT, size=9, italic=True, color="595959")
fill_hdr = PatternFill("solid", fgColor="1F3864")
fill_key = PatternFill("solid", fgColor="FFFF00")
fill_sub = PatternFill("solid", fgColor="D9E1F2")
thin = Side(style="thin", color="808080")
top_border = Border(top=thin)
box = Border(top=thin, bottom=thin, left=thin, right=thin)

USD = '$#,##0;($#,##0);"-"'
USD1 = '$#,##0.0;($#,##0.0);"-"'
USD2 = '$#,##0.00;($#,##0.00);"-"'
NUM1 = '#,##0.0;(#,##0.0);"-"'
PCT = '0.0%;(0.0%);"-"'
MULT = '0.0x;(0.0x);"-"'
YRS = '0.00'


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


def header_row(ws, row, labels, start_col=1, width=None):
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=start_col + i, value=lab)
        c.font = f_hdr
        c.fill = fill_hdr
        c.alignment = Alignment(horizontal="center", wrap_text=True, vertical="center")


def section(ws, row, text, ncols=14):
    for col in range(1, ncols + 1):
        ws.cell(row=row, column=col).fill = fill_sub
    put(ws, f"A{row}", text, bold=True)


def widths(ws, first=38, rest=12, n=16):
    ws.column_dimensions["A"].width = first
    for i in range(2, n + 1):
        ws.column_dimensions[L(i)].width = rest


wb = Workbook()

# =====================================================================
# INPUTS
# =====================================================================
inp = wb.active
inp.title = "Inputs"
widths(inp, 46, 11, 14)
put(inp, "A1", "Forgent Power Solutions (NYSE: FPS) - Key Inputs & Scenario Assumptions", f_title)
put(inp, "A2", "$ in millions except per-share. Fiscal year ends June 30. Blue = hardcoded input; black = formula; "
    "green = link to another sheet; yellow = key lever.", f_note)

section(inp, 4, "Market data & capital structure")
mk = [
    # label, cell value, fmt, comment
    ("Valuation date", date(2026, 9, 25), "yyyy-mm-dd", "Last close used for price (Fri 25-Sep-2026)."),
    ("Share price ($)", 38.97, USD2, "Close 25-Sep-2026. Source: stockanalysis.com/stocks/fps/statistics"),
    ("Class A shares outstanding (mm)", 274.527094, NUM1, "10-K cover page, as of 8-Sep-2026 (274,527,094). SEC EDGAR 0002080126-26-000035"),
    ("Class B shares / Opco units (mm)", 29.901795, NUM1, "10-K cover page, as of 8-Sep-2026 (29,901,795). Exchangeable 1:1 into Class A (Up-C), so included in fully diluted count."),
    ("Dilutive RSUs / options, treasury method (mm)", 0.27, NUM1, "FY26 incremental dilutive shares from share-based awards (XBRL IncrementalCommonSharesAttributableToShareBasedPaymentArrangements = 270k). Approximation."),
    ("Total debt - term loan ($mm)", 582.175, USD1, "Balance sheet 30-Jun-2026: current $6.0mm + LT $576.2mm (net of discount). $600mm TL due 2032, ~6.63% effective rate. 10-K FY2026."),
    ("Cash & equivalents ($mm)", 97.477, USD1, "Balance sheet 30-Jun-2026. 10-K FY2026."),
    ("Operating lease liabilities ($mm) - memo, not in bridge", 121.596, USD1, "30-Jun-2026. Excluded from net debt because lease cost sits inside EBITDA (ASC 842 operating leases); including it would double count."),
]
MK = {}
for i, (lab, val, fmt, com) in enumerate(mk):
    r = 5 + i
    put(inp, f"A{r}", lab)
    put(inp, f"B{r}", val, f_in, fmt, comment=com)
    MK[lab] = f"Inputs!$B${r}"
r = 5 + len(mk)
put(inp, f"A{r}", "Fully diluted shares (mm)", bold=True)
put(inp, f"B{r}", f"=B7+B8+B9", fmt=NUM1, bold=True)
MK["FDSO"] = f"Inputs!$B${r}"
r += 1
put(inp, f"A{r}", "Equity value / market cap ($mm)")
put(inp, f"B{r}", f"=B6*B{r-1}", fmt=USD)
MK["MCAP"] = f"Inputs!$B${r}"
r += 1
put(inp, f"A{r}", "Net debt ($mm)")
put(inp, f"B{r}", "=B10-B11", fmt=USD)
MK["NETDEBT"] = f"Inputs!$B${r}"
r += 1
put(inp, f"A{r}", "Enterprise value at market ($mm)", bold=True)
put(inp, f"B{r}", f"=B{r-2}+B{r-1}", fmt=USD, bold=True)
MK["EV"] = f"Inputs!$B${r}"
r += 1
put(inp, f"A{r}", "Note: TRA liability (Up-C tax receivable agreement) excluded from the bridge - see Cover note on tax treatment.", f_note)

# ---- scenario selector ----
r_sc = r + 2
section(inp, r_sc, "Scenario selector")
put(inp, f"A{r_sc+1}", "Active case (1 = Base, 2 = Bull, 3 = Bear)", bold=True)
put(inp, f"B{r_sc+1}", 1, f_in, "0", fill=fill_key, comment="Change to 2 or 3 to flip the DCF to Bull or Bear.")
SC = f"Inputs!$B${r_sc+1}"
put(inp, f"C{r_sc+1}", f'=CHOOSE(B{r_sc+1},"Base","Bull","Bear")')
SCNAME = f"Inputs!$C${r_sc+1}"

# ---- operating assumptions by scenario ----
YEARS = [f"FY{y}E" for y in range(27, 37)]  # FY27E..FY36E (10 yrs)
NY = len(YEARS)
r0 = r_sc + 3
section(inp, r0, "Operating assumptions by scenario (FY27E = company guidance; FY28E+ = analyst assumption)")
header_row(inp, r0 + 1, ["Driver / case"] + YEARS)

cases = {
    "Base": {
        "rev27": 2500, "growth": [0.35, 0.20, 0.12, 0.08, 0.07, 0.06, 0.05, 0.04, 0.035],
        "margin": [0.240, 0.245, 0.245, 0.240, 0.235, 0.230, 0.225, 0.220, 0.220, 0.220],
    },
    "Bull": {
        "rev27": 2600, "growth": [0.45, 0.28, 0.16, 0.10, 0.08, 0.07, 0.06, 0.05, 0.04],
        "margin": [0.240, 0.255, 0.260, 0.260, 0.255, 0.250, 0.245, 0.240, 0.240, 0.240],
    },
    "Bear": {
        "rev27": 2400, "growth": [0.15, 0.08, -0.05, 0.03, 0.04, 0.04, 0.035, 0.03, 0.03],
        "margin": [0.240, 0.225, 0.210, 0.190, 0.180, 0.180, 0.180, 0.180, 0.180, 0.180],
    },
}
case_comments = {
    "Base": "FY27E = guidance midpoint ($2.4-2.6bn revenue, $575-625mm adj. EBITDA; 8-K 15-Sep-2026). $3.0bn backlog covers >90% of FY27 guide. Growth then fades toward GDP+; FY31E revenue (~$4.9bn) stays inside stated ~$5.8bn revenue capacity. Margin fades to 22% as data-center pricing normalizes.",
    "Bull": "FY27E = top of guidance. Stronger AI data-center build-out; FY29E revenue in line with ~46% 3-yr consensus CAGR (stockanalysis). Margins expand on operating leverage then fade to 24%.",
    "Bear": "FY27E = bottom of guidance. Data-center capex digestion in FY29-FY30 (revenue declines FY30E), price competition compresses margins to 18% (closer to legacy switchgear peers).",
}
rows_case = {}
rr = r0 + 2
for name, cs in cases.items():
    put(inp, f"A{rr}", f"{name}: revenue growth (FY27E cell = revenue $mm)", comment=case_comments[name])
    put(inp, f"B{rr}", cs["rev27"], f_in, USD, comment="FY27E revenue level ($mm), from company guidance range.")
    for j, g in enumerate(cs["growth"]):
        put(inp, f"{L(3+j)}{rr}", g, f_in, PCT)
    put(inp, f"A{rr+1}", f"{name}: adj. EBITDA margin")
    for j, m in enumerate(cs["margin"]):
        put(inp, f"{L(2+j)}{rr+1}", m, f_in, PCT)
    rows_case[name] = (rr, rr + 1)
    rr += 2

put(inp, f"A{rr}", "Active: revenue growth / FY27E revenue", bold=True)
put(inp, f"A{rr+1}", "Active: adj. EBITDA margin", bold=True)
b, u, e = rows_case["Base"], rows_case["Bull"], rows_case["Bear"]
for j in range(NY):
    col = L(2 + j)
    put(inp, f"{col}{rr}", f"=CHOOSE({SC},{col}{b[0]},{col}{u[0]},{col}{e[0]})", fmt=USD if j == 0 else PCT)
    put(inp, f"{col}{rr+1}", f"=CHOOSE({SC},{col}{b[1]},{col}{u[1]},{col}{e[1]})", fmt=PCT)
ACT_G, ACT_M = rr, rr + 1

# ---- other operating drivers (all cases) ----
rr += 3
section(inp, rr, "Other operating drivers (all cases)")
header_row(inp, rr + 1, ["Driver"] + YEARS)
drv = [
    ("Stock-based comp (% revenue) - treated as a cash cost", [0.010] * NY,
     "Adj. EBITDA adds back SBC. We deduct it as an economic cost. FY26 SBC $10.0mm (0.7%); Q4 FY26 annualized ~1.0% post-IPO."),
    ("Depreciation (% revenue)", [0.015, 0.016, 0.017, 0.018, 0.019, 0.020, 0.021, 0.022, 0.022, 0.022],
     "FY26 depreciation $19.0mm = 1.3% of revenue; rises as the 1.8mm sq ft expansion and Tijuana capacity are placed in service."),
    ("Capex (% revenue)", [0.035, 0.035, 0.030, 0.030, 0.028, 0.026, 0.025, 0.025, 0.025, 0.025],
     "FY27 guide ~$87mm (~3.5% of midpoint revenue). FY26 capex $115.9mm (8.2%) was an expansion peak. Fades to maintenance+growth ~2.5%, above D&A in terminal year."),
    ("Change in NWC (% of change in revenue)", [0.15] * NY,
     "FY26 NWC build (AR +$173mm, inventory +$143mm, prepaid +$66mm, less AP +$69mm, contract liabilities +$153mm, accrued +$43mm) = ~$118mm on +$667mm revenue (~18%). Customer deposits partly fund growth; 15% assumed."),
    ("Cash tax rate on EBITA", [0.25] * NY,
     "21% federal + ~4% state/Mexico blended. Reported FY26 ETR of 16.8% is depressed by pre-IPO LLC pass-through income attributable to NCI; an Up-C consolidated view taxes 100% of Opco."),
]
DRV = {}
for i, (lab, vals, com) in enumerate(drv):
    r_ = rr + 2 + i
    put(inp, f"A{r_}", lab, comment=com)
    for j, v in enumerate(vals):
        put(inp, f"{L(2+j)}{r_}", v, f_in, PCT)
    DRV[lab.split(" (")[0].split(" -")[0]] = r_
rr = rr + 2 + len(drv)

# ---- valuation inputs ----
rr += 1
section(inp, rr, "Valuation inputs")
val_inputs = [
    ("Terminal growth rate (perpetuity)", 0.030, PCT, "Long-run nominal GDP-ish; electrification/grid tailwinds argue for upper end of 2-3.5%."),
    ("Terminal EV / EBITDA exit multiple (cross-check)", 14.0, MULT, "Mid-point of mature electrical-equipment peers (ETN/HUBB/NVT historically ~13-18x forward EBITDA); applied to FY36E, when growth has normalized."),
    ("Mid-year convention (1 = on, 0 = off)", 1, "0", "Cash flows assumed to arrive mid-period."),
    ("Next fiscal year end", date(2027, 6, 30), "yyyy-mm-dd", "FY27 ends 30-Jun-2027."),
]
VAL = {}
for i, (lab, v, fmt, com) in enumerate(val_inputs):
    r_ = rr + 1 + i
    put(inp, f"A{r_}", lab)
    put(inp, f"B{r_}", v, f_in, fmt, fill=fill_key if i < 2 else None, comment=com)
    VAL[i] = f"Inputs!$B${r_}"
TG, EXITM, MIDYR, FYE = VAL[0], VAL[1], VAL[2], VAL[3]
r_ = rr + 1 + len(val_inputs)
put(inp, f"A{r_}", "Stub fraction of FY27 remaining after valuation date")
put(inp, f"B{r_}", f"=({FYE}-{MK['Valuation date']})/365", fmt=YRS)
STUB = f"Inputs!$B${r_}"
inp.freeze_panes = "B4"

# =====================================================================
# HISTORICALS
# =====================================================================
hs = wb.create_sheet("Historicals")
widths(hs, 40, 12, 10)
put(hs, "A1", "Forgent - Historical Financials ($mm, FYE June 30)", f_title)
put(hs, "A2", "Source: FY2026 10-K and Q4 FY2026 earnings release (8-K, Sept 2026), SEC EDGAR CIK 0002080126. "
    "FY24 is a partial successor period after the Sept-2023 Neos Partners acquisition and is omitted.", f_note)
header_row(hs, 4, ["Income statement", "FY2025A", "FY2026A", "Q1 FY26A", "Q2 FY26A", "Q3 FY26A", "Q4 FY26A"])
hist = [
    ("Revenue", [753.188, 1420.059, 283.274, 296.404, 378.709, 461.672]),
    ("Gross profit", [278.066, 497.600, None, None, None, 166.695]),
    ("SG&A", [146.270, 262.886, None, None, None, 62.640]),
    ("Operating income", [72.237, 182.489, None, None, None, 91.899]),
    ("Depreciation", [6.188, 19.023, None, None, None, 5.623]),
    ("Amortization of intangibles", [58.676, 47.876, None, None, None, 10.870]),
    ("Interest expense", [54.778, 57.127, None, None, None, 11.423]),
    ("Income tax expense", [5.340, 21.365, None, None, None, 14.427]),
    ("Net income", [17.446, 106.035, None, None, None, 66.094]),
    ("Adjusted EBITDA (company definition)", [169.173, 322.904, None, None, 85.0, 112.736]),
    ("Stock-based compensation", [None, 10.036, None, None, None, 4.490]),
    ("Capex", [84.115, 115.905, None, None, None, 31.0]),
    ("Operating cash flow", [45.022, 109.081, None, None, None, 74.0]),
]
H = {}
for i, (lab, vals) in enumerate(hist):
    r_ = 5 + i
    put(hs, f"A{r_}", lab)
    for j, v in enumerate(vals):
        if v is not None:
            put(hs, f"{L(2+j)}{r_}", v, f_in, USD1)
    H[lab] = r_
put(hs, "D5", 283.274, f_in, USD1, comment="Derived: 1H FY26 revenue $579.678mm (10-Q) less Q2 $296.404mm.")
put(hs, "F14", 85.0, f_in, USD1, comment="Q3 FY26 earnings release: 'Adjusted EBITDA ... $85 million'. Rounded as disclosed.")
put(hs, "G16", 31.0, f_in, USD1, comment="Q4 release narrative, rounded ($31mm).")
put(hs, "G17", 74.0, f_in, USD1, comment="Q4 release narrative, rounded ($74mm).")
r_ = 5 + len(hist) + 1
section(hs, r_, "Ratios", 7)
ratios = [
    ("Revenue growth", "=C5/B5-1", None),
    ("Gross margin", "=B6/B5", "=C6/C5"),
    ("Adj. EBITDA margin", "=B14/B5", "=C14/C5"),
    ("Capex % revenue", "=B16/B5", "=C16/C5"),
    ("Depreciation % revenue", "=B9/B5", "=C9/C5"),
    ("Free cash flow (OCF - capex)", "=B17-B16", "=C17-C16"),
]
for i, (lab, fb, fc) in enumerate(ratios):
    rr_ = r_ + 1 + i
    put(hs, f"A{rr_}", lab)
    fmt = USD1 if "Free" in lab else PCT
    if lab == "Revenue growth":
        put(hs, f"C{rr_}", fb, fmt=fmt)
    else:
        put(hs, f"B{rr_}", fb, fmt=fmt)
        put(hs, f"C{rr_}", fc, fmt=fmt)
put(hs, f"G{r_+3}", "=G14/G5", fmt=PCT)
put(hs, f"F{r_+3}", "=F14/F5", fmt=PCT)
r_ += len(ratios) + 2
section(hs, r_, "Operating KPIs (30-Jun-2026)", 7)
kpis = [
    ("Backlog ($mm)", 3000, "~$3.0bn; 10-K FY2026. Covers >90% of FY27 revenue guidance (Q4 call)."),
    ("FY26 bookings ($mm)", 1503, "Q4 FY26 earnings release highlights."),
    ("FY26 revenue mix: Data center", 0.59, "10-K FY2026, approximate."),
    ("FY26 revenue mix: Grid", 0.21, "10-K FY2026, approximate."),
    ("FY26 revenue mix: Industrial", 0.10, "10-K FY2026, approximate."),
    ("FY26 revenue mix: Other", 0.10, "10-K FY2026, approximate."),
    ("Stated revenue capacity after Tijuana expansion ($mm)", 5800, "Q4 FY26 call: new 385k sq ft facility online Q4 FY27 raises capacity to ~$5.8bn."),
]
for i, (lab, v, com) in enumerate(kpis):
    put(hs, f"A{r_+1+i}", lab)
    put(hs, f"B{r_+1+i}", v, f_in, PCT if v < 1 else USD, comment=com)

# =====================================================================
# WACC
# =====================================================================
wc = wb.create_sheet("WACC")
widths(wc, 46, 14, 4)
put(wc, "A1", "Weighted Average Cost of Capital", f_title)
put(wc, "A2", "FPS listed Feb-2026: too little trading history for a reliable regression beta, so beta is peer-based.", f_note)
w_rows = [
    ("Risk-free rate (10-yr UST)", 0.0425, PCT, "Assumption: 10-yr US Treasury ~4.25% (Sept 2026). Verify against live yield before use."),
    ("Equity risk premium", 0.055, PCT, "Kroll/Damodaran-style implied ERP range 4.5-6.0%."),
    ("Levered beta (peer-based)", 1.45, "0.00", "Judgment from peer betas: Vertiv ~1.6-1.8, Powell ~1.3-1.5, GE Vernova ~1.2-1.4, Eaton ~1.1. FPS is high-growth, data-center concentrated (~59% of revenue) -> upper half."),
    ("Size / company-specific premium", 0.0, PCT, "Set to 0 by default; FPS ~$12bn market cap. Use to reflect customer concentration if desired."),
    ("Pre-tax cost of debt", 0.0663, PCT, "Effective rate on $600mm term loan due 2032 (10-K FY2026)."),
    ("Tax rate", "=Inputs!B{}".format(DRV["Cash tax rate on EBITA"]), PCT, None),
]
for i, (lab, v, fmt, com) in enumerate(w_rows):
    put(wc, f"A{4+i}", lab)
    put(wc, f"B{4+i}", v, f_link if isinstance(v, str) else f_in, fmt, comment=com)
put(wc, "A11", "Cost of equity (CAPM)", bold=True)
put(wc, "B11", "=B4+B6*B5+B7", fmt=PCT, bold=True)
put(wc, "A12", "After-tax cost of debt")
put(wc, "B12", "=B8*(1-B9)", fmt=PCT)
put(wc, "A14", "Market value of equity ($mm)")
put(wc, "B14", f"={MK['MCAP']}", f_link, USD)
put(wc, "A15", "Debt ($mm)")
put(wc, "B15", f"={MK['Total debt - term loan ($mm)']}", f_link, USD)
put(wc, "A16", "Debt / total capital")
put(wc, "B16", "=B15/(B14+B15)", fmt=PCT)
put(wc, "A17", "Equity / total capital")
put(wc, "B17", "=1-B16", fmt=PCT)
put(wc, "A19", "WACC", bold=True)
put(wc, "B19", "=B17*B11+B16*B12", fmt=PCT, bold=True, fill=fill_key)
put(wc, "A20", "WACC override (leave blank to use calculated)")
put(wc, "B20", None, f_in, PCT, comment="Type a rate here to override the CAPM-derived WACC.")
put(wc, "A21", "WACC used in DCF", bold=True)
put(wc, "B21", '=IF(ISNUMBER(B20),B20,B19)', fmt=PCT, bold=True)
WACC = "WACC!$B$21"

# =====================================================================
# DCF
# =====================================================================
d = wb.create_sheet("DCF")
widths(d, 44, 11, 13)
put(d, "A1", "Unlevered DCF - Forgent Power Solutions", f_title)
put(d, "A2", '="Active case: "&' + SCNAME + '&"   |   $mm, FYE June 30"', f_note)
header_row(d, 4, ["($mm)", "FY26A"] + YEARS)
C0 = 3  # column index of FY27E (C)
cols = [L(C0 + j) for j in range(NY)]
labels = [
    "Revenue", "  growth %", "Adj. EBITDA", "  margin %", "(-) Stock-based comp", "(-) Depreciation",
    "EBITA (EBIT excl. acquired-intangible amortization)", "(-) Cash taxes", "NOPAT", "(+) Depreciation",
    "(-) Capex", "(-) Increase in NWC", "Unlevered free cash flow", "  UFCF margin %", "",
    "Fraction of year in forecast", "Discount period (years)", "Discount factor", "PV of UFCF",
]
R = {lab.strip(): 5 + i for i, lab in enumerate(labels)}
for lab, r_ in zip(labels, range(5, 5 + len(labels))):
    if lab:
        put(d, f"A{r_}", lab, bold=lab in ("Revenue", "Adj. EBITDA", "NOPAT", "Unlevered free cash flow", "PV of UFCF"))
# FY26A column
put(d, f"B{R['Revenue']}", "=Historicals!C5", f_link, USD)
put(d, f"B{R['Adj. EBITDA']}", "=Historicals!C14", f_link, USD)
put(d, f"B{R['margin %']}", f"=B{R['Adj. EBITDA']}/B{R['Revenue']}", fmt=PCT)
put(d, f"B{R['growth %']}", "=Historicals!C20", f_link, PCT)

for j, c in enumerate(cols):
    ic = L(2 + j)  # matching column on Inputs (FY27E = B)
    prev = L(C0 + j - 1)
    if j == 0:
        put(d, f"{c}{R['Revenue']}", f"=Inputs!{ic}{ACT_G}", f_link, USD)
        put(d, f"{c}{R['growth %']}", f"={c}{R['Revenue']}/{prev}{R['Revenue']}-1", fmt=PCT)
    else:
        put(d, f"{c}{R['Revenue']}", f"={prev}{R['Revenue']}*(1+{c}{R['growth %']})", fmt=USD)
        put(d, f"{c}{R['growth %']}", f"=Inputs!{ic}{ACT_G}", f_link, PCT)
    put(d, f"{c}{R['margin %']}", f"=Inputs!{ic}{ACT_M}", f_link, PCT)
    put(d, f"{c}{R['Adj. EBITDA']}", f"={c}{R['Revenue']}*{c}{R['margin %']}", fmt=USD)
    put(d, f"{c}{R['(-) Stock-based comp']}", f"=-{c}{R['Revenue']}*Inputs!{ic}{DRV['Stock-based comp']}", fmt=USD)
    put(d, f"{c}{R['(-) Depreciation']}", f"=-{c}{R['Revenue']}*Inputs!{ic}{DRV['Depreciation']}", fmt=USD)
    ebita = R["EBITA (EBIT excl. acquired-intangible amortization)"]
    put(d, f"{c}{ebita}", f"={c}{R['Adj. EBITDA']}+{c}{R['(-) Stock-based comp']}+{c}{R['(-) Depreciation']}", fmt=USD)
    put(d, f"{c}{R['(-) Cash taxes']}", f"=-MAX(0,{c}{ebita})*Inputs!{ic}{DRV['Cash tax rate on EBITA']}", fmt=USD)
    put(d, f"{c}{R['NOPAT']}", f"={c}{ebita}+{c}{R['(-) Cash taxes']}", fmt=USD)
    put(d, f"{c}{R['(+) Depreciation']}", f"=-{c}{R['(-) Depreciation']}", fmt=USD)
    put(d, f"{c}{R['(-) Capex']}", f"=-{c}{R['Revenue']}*Inputs!{ic}{DRV['Capex']}", fmt=USD)
    put(d, f"{c}{R['(-) Increase in NWC']}", f"=-({c}{R['Revenue']}-{prev}{R['Revenue']})*Inputs!{ic}{DRV['Change in NWC']}", fmt=USD)
    uf = R["Unlevered free cash flow"]
    put(d, f"{c}{uf}", f"={c}{R['NOPAT']}+{c}{R['(+) Depreciation']}+{c}{R['(-) Capex']}+{c}{R['(-) Increase in NWC']}", fmt=USD, bold=True)
    put(d, f"{c}{R['UFCF margin %']}", f"={c}{uf}/{c}{R['Revenue']}", fmt=PCT)
    fr = R["Fraction of year in forecast"]
    put(d, f"{c}{fr}", f"={STUB}" if j == 0 else 1, f_link if j == 0 else f_in, YRS)
    dp = R["Discount period (years)"]
    # end-of-period = cumulative fractions; mid-year pulls back half of the current fraction
    put(d, f"{c}{dp}", f"=SUM(${cols[0]}${fr}:{c}{fr})-{MIDYR}*{c}{fr}/2", fmt=YRS)
    put(d, f"{c}{R['Discount factor']}", f"=1/(1+{WACC})^{c}{dp}", fmt="0.000")
    put(d, f"{c}{R['PV of UFCF']}", f"={c}{uf}*{c}{fr}*{c}{R['Discount factor']}", fmt=USD, bold=True)
for rr_ in (R["Unlevered free cash flow"], R["PV of UFCF"]):
    for j in range(NY + 1):
        d.cell(row=rr_, column=2 + j).border = top_border
put(d, f"A{R['Fraction of year in forecast']+5}",
    "FY27E UFCF is pro-rated by the stub fraction (Q1 FY27 is already partly elapsed at the valuation date). "
    "Acquired-intangible amortization is excluded from EBITA; its tax shield is conservatively ignored.", f_note)

LAST = cols[-1]
UF = R["Unlevered free cash flow"]
PVR = R["PV of UFCF"]
FRR = R["Fraction of year in forecast"]
b0 = R["PV of UFCF"] + 3
section(d, b0, "Valuation", 13)
put(d, f"B{b0}", "Perpetuity growth", bold=True, align="center")
put(d, f"C{b0}", "Exit multiple", bold=True, align="center")
rows_v = [
    ("WACC", f"={WACC}", f"={WACC}", PCT),
    ("Terminal growth / exit EV/EBITDA", f"={TG}", f"={EXITM}", None),
    ("Terminal-year UFCF / EBITDA", f"={LAST}{UF}", f"={LAST}{R['Adj. EBITDA']}", USD),
    ("Terminal value (at FY36 year-end)", f"=B{{r3}}*(1+B{{r2}})/(B{{r1}}-B{{r2}})", f"=C{{r3}}*C{{r2}}", USD),
    ("Discount period for TV (years)", f"=SUM({cols[0]}{FRR}:{LAST}{FRR})", f"=SUM({cols[0]}{FRR}:{LAST}{FRR})", YRS),
    ("PV of terminal value", "=B{r4}/(1+B{r1})^B{r5}", "=C{r4}/(1+C{r1})^C{r5}", USD),
    ("Sum of PV of UFCF", f"=SUM({cols[0]}{PVR}:{LAST}{PVR})", f"=SUM({cols[0]}{PVR}:{LAST}{PVR})", USD),
    ("Enterprise value", "=B{r6}+B{r7}", "=C{r6}+C{r7}", USD),
    ("  PV of TV as % of EV", "=B{r6}/B{r8}", "=C{r6}/C{r8}", PCT),
    ("(-) Debt", f"=-{MK['Total debt - term loan ($mm)']}", f"=-{MK['Total debt - term loan ($mm)']}", USD),
    ("(+) Cash", f"={MK['Cash & equivalents ($mm)']}", f"={MK['Cash & equivalents ($mm)']}", USD),
    ("Equity value", "=B{r8}+B{r10}+B{r11}", "=C{r8}+C{r10}+C{r11}", USD),
    ("Fully diluted shares (mm)", f"={MK['FDSO']}", f"={MK['FDSO']}", NUM1),
    ("Implied share price ($)", "=B{r12}/B{r13}", "=C{r12}/C{r13}", USD2),
    ("Current share price ($)", f"={MK['Share price ($)']}", f"={MK['Share price ($)']}", USD2),
    ("Upside / (downside)", "=B{r14}/B{r15}-1", "=C{r14}/C{r15}-1", PCT),
    ("Implied EV / FY27E EBITDA", f"=B{{r8}}/{cols[0]}{R['Adj. EBITDA']}", f"=C{{r8}}/{cols[0]}{R['Adj. EBITDA']}", MULT),
    ("Implied terminal EV/EBITDA  |  implied perpetuity growth",
     f"=B{{r4}}/{LAST}{R['Adj. EBITDA']}", f"=(C{{r4}}*C{{r1}}-{LAST}{UF})/(C{{r4}}+{LAST}{UF})", None),
]
rmap = {f"r{i+1}": b0 + 1 + i for i in range(len(rows_v))}
for i, (lab, fb, fc, fmt) in enumerate(rows_v):
    r_ = b0 + 1 + i
    bold = lab in ("Enterprise value", "Equity value", "Implied share price ($)")
    put(d, f"A{r_}", lab, bold=bold)
    fb_, fc_ = fb.format(**rmap), fc.format(**rmap)
    link = lambda s: s.startswith("=Inputs") or s.startswith("=WACC") or s.startswith("=-Inputs")
    if lab == "Terminal growth / exit EV/EBITDA":
        put(d, f"B{r_}", fb_, f_link, PCT); put(d, f"C{r_}", fc_, f_link, MULT)
    elif lab.startswith("Implied terminal"):
        put(d, f"B{r_}", fb_, fmt=MULT); put(d, f"C{r_}", fc_, fmt=PCT)
    else:
        put(d, f"B{r_}", fb_, f_link if link(fb_) else f_calc, fmt, bold=bold,
            fill=fill_key if lab == "Implied share price ($)" else None)
        put(d, f"C{r_}", fc_, f_link if link(fc_) else f_calc, fmt, bold=bold,
            fill=fill_key if lab == "Implied share price ($)" else None)
DCF_PRICE_PG = f"DCF!$B${rmap['r14']}"
DCF_PRICE_EX = f"DCF!$C${rmap['r14']}"
d.freeze_panes = "B5"

# =====================================================================
# SENSITIVITY (explicit formulas, no Excel data tables)
# =====================================================================
s = wb.create_sheet("Sensitivity")
widths(s, 30, 11, 9)
put(s, "A1", "DCF Sensitivities - implied share price ($)", f_title)
put(s, "A2", "Each cell recomputes the full DCF with SUMPRODUCT across the DCF sheet's UFCF row (active case).", f_note)
fcf_rng = f"DCF!${cols[0]}${UF}:${LAST}${UF}"
frac_rng = f"DCF!${cols[0]}${FRR}:${LAST}${FRR}"
per_rng = f"DCF!${cols[0]}${R['Discount period (years)']}:${LAST}${R['Discount period (years)']}"
tvper = f"DCF!$B${rmap['r5']}"
last_fcf = f"DCF!${LAST}${UF}"
last_ebitda = f"DCF!${LAST}${R['Adj. EBITDA']}"
netcash = f"(-{MK['Total debt - term loan ($mm)']}+{MK['Cash & equivalents ($mm)']})"
wacc_vals = [-0.02, -0.01, 0, 0.01, 0.02]
tg_vals = [0.02, 0.025, 0.03, 0.035, 0.04]
ex_vals = [10, 12, 14, 16, 18]


def grid(top, title, col_vals, col_fmt, tv_expr):
    put(s, f"A{top}", title, bold=True)
    put(s, f"A{top+1}", "WACC  \\  " + ("terminal growth" if col_fmt == PCT else "exit multiple"), f_note)
    for k, v in enumerate(col_vals):
        put(s, f"{L(3+k)}{top+1}", v, f_in, col_fmt, bold=True)
    for i, dw in enumerate(wacc_vals):
        r_ = top + 2 + i
        put(s, f"B{r_}", f"={WACC}+({dw})", fmt=PCT, bold=True)
        for k in range(len(col_vals)):
            cc = L(3 + k)
            w = f"$B{r_}"
            x = f"{cc}${top+1}"
            pv = f"SUMPRODUCT({fcf_rng},{frac_rng},1/(1+{w})^{per_rng})"
            tv = tv_expr(w, x)
            put(s, f"{cc}{r_}", f"=({pv}+({tv})/(1+{w})^{tvper}+{netcash})/{MK['FDSO']}", fmt=USD2,
                fill=fill_key if (dw == 0 and k == 2) else None)


grid(4, "Perpetuity-growth method", tg_vals, PCT, lambda w, x: f"{last_fcf}*(1+{x})/({w}-{x})")
grid(12, "Exit-multiple method", ex_vals, MULT, lambda w, x: f"{last_ebitda}*{x}")
put(s, "A20", "Base-case scenario table: flip Inputs!B" + SC.split("$")[-1] + " (1/2/3) to see Bull / Bear on every sheet.", f_note)

from build_fps_rest import build_rest  # noqa: E402

build_rest(wb, dict(MK=MK, DCF_PRICE_PG=DCF_PRICE_PG, DCF_PRICE_EX=DCF_PRICE_EX, WACC=WACC,
                    SC=SC, SCNAME=SCNAME, DCF_R=R, DCF_COLS=cols, sens_rows=(6, 10, 14, 18)),
           put, header_row, section, widths,
           dict(f_in=f_in, f_calc=f_calc, f_link=f_link, f_bold=f_bold, f_title=f_title, f_note=f_note,
                fill_key=fill_key, fill_sub=fill_sub, USD=USD, USD1=USD1, USD2=USD2, NUM1=NUM1, PCT=PCT, MULT=MULT))

for ws in wb.worksheets:
    ws.sheet_view.showGridLines = False
wb.calculation.fullCalcOnLoad = True  # openpyxl writes no cached values; Excel computes on open
wb.save(OUT)
print("saved", OUT)
