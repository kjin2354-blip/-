"""Builds Evercore (NYSE: EVR) quarterly history since IPO (Q3 2006 - Q2 2026).

Revenue, compensation, operating income, net income, GAAP and Adjusted EPS, margins, trailing-twelve-month
(TTM) figures and quarter-end P/E. Raw data lives in evr_quarterly_data.json (each row carries its source);
every ratio, TTM sum and P/E is a live Excel formula.
Run: python3 models/build_evr_quarterly.py  ->  models/EVR_Quarterly_History.xlsx
"""
import json
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.series import SeriesLabel
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter as L

HERE = Path(__file__).parent
OUT = HERE / "EVR_Quarterly_History.xlsx"
ROWS = json.loads((HERE / "evr_quarterly_data.json").read_text())

FONT = "Arial"
f_in = Font(name=FONT, size=10, color="0000FF")
f_calc = Font(name=FONT, size=10, color="000000")
f_bold = Font(name=FONT, size=10, bold=True)
f_hdr = Font(name=FONT, size=10, bold=True, color="FFFFFF")
f_title = Font(name=FONT, size=14, bold=True)
f_note = Font(name=FONT, size=9, italic=True, color="595959")
fill_hdr = PatternFill("solid", fgColor="1F3864")
fill_key = PatternFill("solid", fgColor="FFFF00")
fill_sub = PatternFill("solid", fgColor="D9E1F2")

USD1 = '$#,##0.0;($#,##0.0);"-"'
USD2 = '$#,##0.00;($#,##0.00);"-"'
PCT = '0.0%;(0.0%);"-"'
MULT = '0.0x;(0.0x);"-"'


def put(ws, ref, value, font=f_calc, fmt=None, fill=None, comment=None, align=None):
    c = ws[ref]
    c.value = value
    c.font = font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if comment:
        c.comment = Comment(comment, "Model")
    if align:
        c.alignment = Alignment(horizontal=align)
    return c


wb = Workbook()
ws = wb.active
ws.title = "Quarterly"
put(ws, "A1", "Evercore (EVR) - Quarterly Results, Margins and P/E Since IPO (Aug-2006)", f_title)
put(ws, "A2", "$ in millions except per share. Blue = reported data (source in column W and cell comments); black = "
    "formula. P/E = quarter-end close / sum of last four quarters' EPS; 'n/m' where TTM EPS <= 0 or incomplete.", f_note)

COLS = [  # key, header, width, fmt
    ("q", "Quarter", 9, None), ("end", "Period end", 11, "yyyy-mm-dd"),
    ("rev", "Net revenues", 10, USD1), ("yoy", "Revenue YoY", 9, PCT),
    ("comp", "Comp & benefits", 10, USD1), ("ncomp", "Non-comp opex", 10, USD1),
    ("opex", "Total opex", 10, USD1), ("oi", "Operating income", 10, USD1),
    ("ni", "Net income to EVR", 10, USD1), ("eps", "GAAP diluted EPS", 9, USD2),
    ("adj", "Adjusted diluted EPS", 9, USD2),
    ("cr", "Comp ratio", 8, PCT), ("om", "Operating margin", 9, PCT), ("nm", "Net margin", 8, PCT),
    ("ttmrev", "TTM net revenues", 10, USD1), ("ttmom", "TTM operating margin", 9, PCT),
    ("ttmeps", "TTM GAAP EPS", 9, USD2), ("ttmadj", "TTM Adjusted EPS", 9, USD2),
    ("px", "Quarter-end close ($)", 9, USD2), ("pe", "P/E on TTM GAAP EPS", 9, MULT),
    ("peadj", "P/E on TTM Adjusted EPS", 9, MULT), ("src", "Source / note", 70, None),
]
C = {k: L(i + 1) for i, (k, *_r) in enumerate(COLS)}
HR = 4
for i, (k, h, w, _f) in enumerate(COLS):
    c = ws.cell(row=HR, column=i + 1, value=h)
    c.font, c.fill = f_hdr, fill_hdr
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.column_dimensions[L(i + 1)].width = w
ws.row_dimensions[HR].height = 42
FMT = {k: f for k, _h, _w, f in COLS}

R0 = HR + 1
for i, d in enumerate(ROWS):
    r = R0 + i
    y, m, dd = map(int, d["end"].split("-"))
    put(ws, f"{C['q']}{r}", f"Q{m // 3} {y}", align="left")
    put(ws, f"{C['end']}{r}", date(y, m, dd), fmt=FMT["end"])
    for k in ("rev", "comp", "opex", "ni", "eps", "adj"):
        if d[k] is not None:
            put(ws, f"{C[k]}{r}", d[k], f_in, FMT[k])
        else:
            put(ws, f"{C[k]}{r}", "n/m", f_in, align="right")
    put(ws, f"{C['px']}{r}", d["px"], f_in, FMT["px"], comment=f"Yahoo Finance daily close, {d['pxdate']}.")
    put(ws, f"{C['src']}{r}", d["src"], f_note)
    rev, comp, opex, ni = (f"{C[k]}{r}" for k in ("rev", "comp", "opex", "ni"))
    put(ws, f"{C['ncomp']}{r}", f"={opex}-{comp}", fmt=USD1)
    put(ws, f"{C['oi']}{r}", f"={rev}-{opex}", fmt=USD1)
    put(ws, f"{C['cr']}{r}", f"={comp}/{rev}", fmt=PCT)
    put(ws, f"{C['om']}{r}", f"={C['oi']}{r}/{rev}", fmt=PCT)
    put(ws, f"{C['nm']}{r}", f'=IF(ISNUMBER({ni}),{ni}/{rev},"n/m")', fmt=PCT, align="right")
    if i >= 4:
        put(ws, f"{C['yoy']}{r}", f"={rev}/{C['rev']}{r - 4}-1", fmt=PCT)
    if i >= 3:
        a = r - 3
        put(ws, f"{C['ttmrev']}{r}", f"=SUM({C['rev']}{a}:{C['rev']}{r})", fmt=USD1)
        put(ws, f"{C['ttmom']}{r}", f"=SUM({C['oi']}{a}:{C['oi']}{r})/{C['ttmrev']}{r}", fmt=PCT)
        put(ws, f"{C['ttmadj']}{r}", f"=SUM({C['adj']}{a}:{C['adj']}{r})", fmt=USD2)
        put(ws, f"{C['peadj']}{r}", f'=IF({C["ttmadj"]}{r}>0,{C["px"]}{r}/{C["ttmadj"]}{r},"n/m")',
            fmt=MULT, align="right")
        if i >= 4:  # Q3 2006 GAAP EPS is n/m, so the first complete GAAP TTM is Q3 2007
            put(ws, f"{C['ttmeps']}{r}", f"=SUM({C['eps']}{a}:{C['eps']}{r})", fmt=USD2)
            put(ws, f"{C['pe']}{r}", f'=IF({C["ttmeps"]}{r}>0,{C["px"]}{r}/{C["ttmeps"]}{r},"n/m")',
                fmt=MULT, align="right")
RL = R0 + len(ROWS) - 1

# latest-price row
r = RL + 2
put(ws, f"{C['q']}{r}", "Latest", f_bold)
put(ws, f"{C['end']}{r}", date(2026, 10, 6), fmt="yyyy-mm-dd")
put(ws, f"{C['px']}{r}", 268.08, f_in, USD2, comment="Yahoo Finance close, 6-Oct-2026 (matches user-provided price).")
put(ws, f"{C['ttmeps']}{r}", f"={C['ttmeps']}{RL}", fmt=USD2)
put(ws, f"{C['ttmadj']}{r}", f"={C['ttmadj']}{RL}", fmt=USD2)
put(ws, f"{C['pe']}{r}", f"={C['px']}{r}/{C['ttmeps']}{r}", fmt=MULT, fill=fill_key)
put(ws, f"{C['peadj']}{r}", f"={C['px']}{r}/{C['ttmadj']}{r}", fmt=MULT, fill=fill_key)
put(ws, f"{C['src']}{r}", "Price 6-Oct-2026 over TTM EPS through Q2 2026 (latest reported quarter).", f_note)
LATEST = r

# summary statistics on TTM Adjusted P/E and margins
r = LATEST + 2
for col in range(1, len(COLS) + 1):
    ws.cell(row=r, column=col).fill = fill_sub
put(ws, f"A{r}", "Through-cycle statistics (Q1 2010 - Q2 2026; excludes IPO / 2008-09 distortions)", f_bold)
s0 = R0 + next(i for i, d in enumerate(ROWS) if d["end"] == "2010-03-31")
stats = [("Median", "MEDIAN"), ("Minimum", "MIN"), ("Maximum", "MAX"), ("Average", "AVERAGE")]
for j, (lab, fn) in enumerate(stats):
    rr = r + 1 + j
    put(ws, f"{C['q']}{rr}", lab, f_bold)
    for k in ("cr", "om", "ttmom", "pe", "peadj"):
        put(ws, f"{C[k]}{rr}", f"={fn}({C[k]}{s0}:{C[k]}{RL})", fmt=FMT[k])
put(ws, f"{C['src']}{r + 1}", "Text 'n/m' cells are ignored by MEDIAN/MIN/MAX/AVERAGE.", f_note)
ws.freeze_panes = ws[f"C{R0}"]

# ---------- charts ----------
ch = ws.parent.create_sheet("Charts")
put(ch, "A1", "Evercore - Quarterly History Charts", f_title)
cats = Reference(ws, min_col=2, min_row=R0 + 3, max_row=RL)


def line(title, keys, labels, anchor, fmt):
    c = LineChart()
    c.title = title
    c.height, c.width = 9, 26
    for k, lab in zip(keys, labels):
        col = list(C).index(k) + 1
        c.add_data(Reference(ws, min_col=col, min_row=R0 + 3, max_row=RL), titles_from_data=False)
        c.series[-1].tx = SeriesLabel(v=lab)
    c.set_categories(cats)
    c.x_axis.number_format = "yyyy"
    c.y_axis.number_format = fmt
    ch.add_chart(c, anchor)


line("P/E on TTM Adjusted EPS (quarter-end)", ["peadj"], ["P/E (TTM Adjusted)"], "A3", "0x")
line("TTM operating margin and quarterly comp ratio (GAAP)", ["ttmom", "cr"],
     ["TTM operating margin", "Comp ratio"], "A22", "0%")
line("TTM net revenues ($mm) ", ["ttmrev"], ["TTM net revenues"], "A41", "#,##0")
line("TTM Adjusted vs GAAP EPS ($)", ["ttmadj", "ttmeps"], ["TTM Adjusted EPS", "TTM GAAP EPS"], "A60", "0.00")

# ---------- notes ----------
nt = wb.create_sheet("Notes")
nt.column_dimensions["A"].width = 150
notes = [
    "SOURCES",
    "Q1 2010 - Q2 2026 GAAP: SEC EDGAR XBRL companyfacts (CIK 0001360901), latest filed value per quarter; Q4 = full year "
    "less nine months where no discrete Q4 fact exists. Q4 2021-2025 GAAP EPS taken from the Q4 earnings releases.",
    "Q3 2006 - Q4 2009 GAAP: condensed consolidated statements of operations in Evercore's earnings releases (8-K Ex. 99.1).",
    "Adjusted EPS: company's 'Adjusted' / 'Adjusted Pro Forma' diluted EPS as first reported in each quarter's earnings "
    "release (79 releases, Nov-2006 to Jul-2026). Q1 2007 = six-month figure less Q2 (no Q1 2007 release; first "
    "release after IPO covered Q3 2006). Q2 2009 = $0.10 as reported (company also showed $0.30 excluding one-time costs).",
    "Prices: Yahoo Finance daily closes (not dividend-adjusted; EVR has had no splits).",
    "",
    "CAVEATS",
    "1. The IPO was 10-Aug-2006. Q3 2006 combines predecessor and successor periods; before the IPO, partners' pay was a "
    "distribution, not compensation expense, so Q3 2006 margins are not comparable.",
    "2. GAAP EPS and GAAP P/E are distorted by one-offs: Q2 2007 IPO-related vesting charge ($126mm), 2009 special charges, "
    "Q4 2017 tax-reform remeasurement, and (through ~2016) the LP-unit structure that pushed earnings to noncontrolling "
    "interests. Adjusted P/E is the usable series; it is also the basis of consensus.",
    "3. Adjusted definitions changed over time (e.g. 2018 gross-up of client expenses, 2016 removal of 'Pro Forma'). Values "
    "are as first reported, not restated.",
    "4. TTM EPS = sum of four quarterly EPS figures, which differs slightly from a full-year EPS because share counts vary.",
    "5. GAAP revenue/expense figures for some early XBRL quarters were later reclassified; latest filed values are used, "
    "so they can differ by ~1% from the original release.",
    "6. Comp ratio for Q1 2010 is from the Q1 2010 release (no XBRL fact).",
]
for i, t in enumerate(notes):
    put(nt, f"A{i + 1}", t, f_bold if t.isupper() and len(t) < 20 else f_calc)

for s in wb.worksheets:
    s.sheet_view.showGridLines = False
wb.save(OUT)
print(f"wrote {OUT}")
