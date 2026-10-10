# Appendix C — Finance (Modules 8, 11, 14, 17–21) — Evercore Inc. (NYSE: EVR)

Research date: 10-Oct-2026. Price: $271.86 (close 9-Oct-2026, Yahoo chart API). 52-week range: $251.13 intraday low (1-Oct-2026) to $388.71 intraday high (16-Jan-2026). Latest reported period: Q2 2026 (8-K 29-Jul-2026; 10-Q filed 5-Aug-2026). Q3 2026 results are due 28-Oct-2026.

**Conventions.** "GAAP" means U.S. GAAP as reported. "Adj." means Evercore's non-GAAP "Adjusted" basis, which assumes LP units are exchanged, excludes Robey Warshaw acquisition items and special charges, and reports interest expense below operating income. The two bases are never mixed without a label. $mm unless stated. "(est.)" marks my own estimates. "TTM" means Q3'25–Q2'26.

**Primary sources used.**
- 8-K earnings releases: Q2'26 (29-Jul-2026), Q1'26 (29-Apr-2026), Q4'25 (4-Feb-2026), and Q4 releases for FY2013–FY2024.
- 10-Q Q2'26 (accession 0001628280-26-053320).
- 10-K FY2025 (0001628280-26-010273, filed 20-Feb-2026).
- SEC XBRL companyfacts (CIK 1360901).
- Peer 8-K releases: PJT, MC, LAZ, PWP (Q2'26 and Q4'25) and HLI (Q1 FY27 and Q4 FY26).
- Quarterly file `evr_quarterly_data.json` (80 quarters). I spot-checked it against the releases: Q2'26 revenue $990.199mm, comp $641.791mm, GAAP EPS $2.32 and Adj. EPS $2.91 all match; Q4'25 and Q1'26 also match.

**Non-primary sources (labeled where used).**
- Consensus: user-provided FY2027 Adj. EPS $22.19, plus Q3'26 revenue of about $1.02bn and EPS of about $3.11. Both are unverified.
- WallStreetZen (accessed 10-Oct-2026): FY26/27/28 EPS $19.69 / $23.24 / $26.72 (13 analysts).
- Prices and the 10-year UST yield come from Yahoo (10Y close 5.24% on 9-Oct, 5.28% on 2-Oct).

---

## Key numbers at a glance

| Item | Value | Arithmetic |
|---|---|---|
| TTM Adj. EPS | $19.05 | 3.48 + 5.13 + 7.53 + 2.91 |
| TTM Adj. EPS ex-Q1'26 vesting tax benefit | ~$17.0 | Q1'26 benefit $94.0mm ÷ 44.44mm sh = $2.12; and ($847.9mm − $94.0mm) ÷ ~44.3mm sh |
| TTM GAAP EPS | $17.69 | 3.41 + 4.76 + 7.20 + 2.32 |
| NTM Adj. EPS (consensus-derived, est.) | ~$21.2 | Q4'26E $6.10 (= 19.69 − 10.48 − 3.11) + ~68% × FY27 $22.19 |
| **Mid-cycle Adj. EPS (my est., 2026 basis)** | **$13.00** | $4.0bn revenue × 20.0% Adj. op margin − $27.6mm interest = $772mm pre-tax; × (1 − 26.5%) = $568mm; ÷ 43.6mm sh |
| P/E TTM (Adj.) / ex-tax-benefit / GAAP | 14.3x / 16.0x / 15.4x | 271.86 ÷ 19.05 / 17.0 / 17.69 |
| P/E NTM (Adj., consensus-derived) | ~12.8x | 271.86 ÷ 21.2 |
| **P/E on mid-cycle EPS** | **20.9x** | 271.86 ÷ 13.00 |
| Adjusted diluted shares (Q2'26) | 43.71mm | release p. A-3 |
| Market cap, adjusted diluted / Class A only | $11.88bn / $10.45bn | 43.71 × 271.86; 38.45mm × 271.86 |
| Net cash (gross), 30-Jun-26 | $1,864.9mm ($42.7/sh) | cash 1,256.6 + investments and CDs 1,148.3 − notes 540.0 |
| Net cash after accrued comp | $924.7mm ($21.2/sh) | 1,864.9 − 940.2 |
| Scenario values (FY28 EPS × P/E) | Bull $422 / Base $277 / Bear $165 | 26.40 × 16 / 19.80 × 14 / 8.25 × 20 |
| Probability-weighted value | ~$280 (+3%) | 0.25 × 422 + 0.45 × 277 + 0.30 × 165 |
| Kelly f* at $271.86 | Negative, so 0% | b = 0.048; f* = −5.5 |
| Price at which half-Kelly turns positive | ≤ ~$243 | b ≥ q/p = 0.43 |

---

## Module 8 — Revenue quality

### 8a) Growth split: organic (SMD capacity × productivity), acquisitions, FX

I approximate IB revenue as Advisory plus Underwriting fees (GAAP). IB SMD counts are year-end figures as disclosed. They include committed hires, and before 2024 they were labeled "Advisory SMDs".

| Year | YE IB SMDs | IB revenue ($mm) | Avg SMDs | Revenue per avg SMD ($mm) | YoY IB revenue |
|---|---|---|---|---|---|
| 2020 | 107 | 2,031.5 | — | — | — |
| 2021 | 114 | 2,998.7 | 110.5 | 27.1 | +47.6% |
| 2022 | 130 | 2,515.6 | 122.0 | 20.6 | −16.1% |
| 2023 | 136 | 2,074.9 | 133.0 | 15.6 | −17.5% |
| 2024 | 144 | 2,597.7 | 140.0 | 18.6 | +25.2% |
| 2025 | 171 | 3,446.7 | 157.5 | 21.9 | +32.7% |
| TTM Jun-26 | 188 (Jun-26); 159 (Jun-25) | 4,277.6 | 173.5 | 24.7 | +46% (est.) |

**FY2025 decomposition (+32.7% IB revenue).**
- Capacity: average SMDs +12.5% (140 → 157.5).
- Productivity: revenue per SMD +17.9% (18.6 → 21.9).
- Check: 1.125 × 1.179 = 1.326.

**Acquisitions.** Robey Warshaw closed 1-Oct-2025 and brought 5 SMDs. Its revenue is **not disclosed**. I estimate $60–120mm a year, or about 1.5–2.5% of revenue (est., Low confidence). It contributed one quarter to FY25 and is part of TTM growth.

**FX.** About 24% of 2025 revenue came from non-U.S. clients (10-K). FX was a small effect on growth, roughly ±1pp (est.). Not disclosed / To verify.

**H1'26 vs H1'25.** IB revenue rose +62% (1,341.6 → 2,172.5) while SMDs grew about 18% (159 → 188). Most of the growth was therefore productivity, meaning large-fee completions, which is cyclical rather than structural.

Source: Q4'21–Q4'25 and Q2'26 8-K releases (SMD footnotes, revenue tables); 10-K FY2025.
Confidence: Medium-High for the decomposition (SMD counts include commits); Low for the Robey Warshaw and FX split.

### 8b) Seasonality and lumpiness

Quarterly share of annual GAAP net revenue, 2010–2025 averages: Q1 20.3%, Q2 23.1%, Q3 24.4%, **Q4 32.2%**. The median absolute QoQ revenue change since 2015 is 24%.

2026 breaks the pattern:
- Q1'26 revenue was $1,391.6mm, a record and +100% YoY. It was above Q4'25 ($1,288.3mm), which is historically unusual.
- Q2'26 fell back to $990.2mm.
- Average fee per fee-paying client was ~$6.6mm in Q1'26 (IB revenue $1,299.8mm ÷ 198 fees, derived from H1 minus Q2) and ~$2.9mm in Q2'26 ($872.7mm ÷ 296).

Q1 was driven by a few mega-fees. The mandates named in the releases include WBD's $110bn sale to Paramount Skydance, Devon/Coterra ($58bn) and Jetro/Sysco ($29.1bn). Consensus for Q3'26 (~$1.02bn, unverified) would be about −2% YoY versus Q3'25's $1,038.9mm, which would be the first YoY quarterly revenue decline since Q1'24.

Source: evr_quarterly_data.json; Q1'26 and Q2'26 releases.
Confidence: High (history); Medium (consensus).

### 8c) Revenue recognition

- **Success fees.** Recognized when the transaction completes, or earlier once it is "probable that a significant reversal will not occur". Some year-end fees are booked before the deal closes; Deloitte's FY2025 **critical audit matter** is exactly this year-end success-fee recognition.
- **Retainers and announcement fees.** Recognized over time.
- **Private-fund placement fees.** Often paid in installments. This creates long-term receivables plus long-term contract assets of $179.4mm at 30-Jun-26, up from $115.8mm at YE24 (101.3 + 14.5).
- **Contract assets (current).** $147.4mm at YE25, down to $47.2mm at 30-Jun-26 as year-end accruals reversed. Total contract assets were $79.0mm at Jun-26 versus $175.3mm at YE25.
- **Deferred revenue.** Small, at $12.7mm.
- **Reimbursable client expenses.** Grossed up in revenue (ASC 606 presentation since 2018). Amount not separately disclosed (To verify).

The quality issue is that Q4 and year-end revenue relies on management judgment about deals that have not yet closed. Higher long-term placement receivables also stretch cash conversion.

Source: 10-K FY2025 (auditor report, Notes 2 and 4); 10-Q Q2'26 Note 4.
Confidence: High.

### 8d) Concentration

- "No client accounted for more than 10% of Consolidated Net Revenues" in H1'26 or H1'25 (10-Q Note 19).
- Fees of at least $1mm: 529 in FY25 (+16% YoY), and 280 in H1'26 versus 206 in H1'25.
- Total fee-paying transactions: 806 in FY25 and 494 in H1'26.
- Average IB fee was ~$4.3mm in FY25 (3,446.7 ÷ 806) and ~$4.4mm in H1'26 (2,172.5 ÷ 494).

The largest single fees (for example on WBD) are **not disclosed**. I estimate the top 10 fees at 15–25% of annual advisory revenue (est., Low confidence). Concentration lies in deal timing and a few mega-mandates, not in any one client.

Source: 10-Q Q2'26; Q4'25 and Q2'26 releases.
Confidence: High (disclosed metrics); Low (top-fee estimate).

### 8e) Geographic mix and FX

| Region (ex-other revenue) | 2023 | 2024 | 2025 | 2025 share |
|---|---|---|---|---|
| Americas | 1,826.9 | 2,331.4 | 3,067.3 | 81.2% |
| of which U.S. | 1,719.3 | 2,187.9 | 2,885.7 | 76.4% |
| EMEA | 469.7 | 503.5 | 626.3 | 16.6% |
| Asia-Pacific | 48.1 | 56.4 | 83.2 | 2.2% |
| Total | 2,344.7 | 2,891.3 | 3,776.8 | 100% |

- EMEA total assets jumped to $1.89bn at YE25, from $0.61bn, with Robey Warshaw and UK cash.
- FX translation hit cash by −$12.6mm in H1'26 and added +$31.5mm in FY25.
- Some notes (Series H/J) appear to be non-USD (their carrying values move with FX). To verify.
- FX matters at the margin; the GBP/EUR mix will rise with Robey Warshaw.

Source: 10-K FY2025 segment note (geographic information); 10-Q cash flow statement.
Confidence: High.

**Key judgment (Module 8): revenue quality is good on concentration and auditing but highly lumpy. H1'26 was flattered by mega-fees, so revenue is cyclical and *lagging* the deal cycle. Direction: rising (near-term), uncontrollable.**

---

## Module 11 — Profitability

### 11a) Comp ratio, non-comp ratio, operating margin — history and peers

**Evercore full-year history.**

| FY | Adj. revenue | Adj. comp ratio | Adj. op margin | GAAP comp ratio | GAAP op margin |
|---|---|---|---|---|---|
| 2013 | 760.1 | 59.2% | n/d | 63.5% | 17.0% |
| 2014 | 911.9 | 59.0% | n/d | 60.0% | 18.7% |
| 2015 | 1,216 | 57.8% | 24.0% | 64.4% | 10.5% |
| 2016 | 1,431 | 57.3% | 26.5% | 62.5% | 18.1% |
| 2017 | 1,625.8 | 57.5% (restated) | 26.2% | 56.5% | 25.2% |
| 2018 | 2,083.2 | 56.7% | 28.4% | 58.0% | 26.3% |
| 2019 | 2,032.6 | 58.2% | 24.5% | 59.8% | 21.8% |
| 2020 | 2,327.3 | 58.9% | 27.5% | 60.6% | 23.3% |
| 2021 | 3,316.9 | 55.7% | 34.3% | 56.2% | 33.5% |
| 2022 | 2,785.6 | 60.9% | 25.9% | 61.5% | 25.2% |
| 2023 | 2,449.3 | 67.6% | 15.7% | 68.3% | 14.8% |
| 2024 | 3,002.6 | 65.7% | 18.6% | 66.3% | 17.7% |
| 2025 | 3,884.0 | 64.2% | 21.6% | 64.9% | 20.5% |
| H1'26 | 2,401.0 | 63.8% | 22.7% | 64.9% | 20.0% |
| TTM | 4,746.2 | 63.6% | 23.4% | — | — |

- GAAP op margin for 2013–2016 is computed from the quarterly file. n/d = not disclosed in the headline.
- Adj. non-comp ratio: 2025 = 100 − 64.2 − 21.6 = 14.2%; H1'26 = 13.5%; Q2'26 = 17.5%.
- Adj. non-comp dollars are growing +27% YoY (H1). The TTM run-rate is $619.7mm: FY25 $551.5mm + H1'26 $325.2mm − H1'25 $257.0mm.
- The structural break: the Adj. comp ratio averaged **57.7% in 2015–2020** and **65.8% in 2023–2025**.

**Peers, latest reported period.** Each peer uses its own non-GAAP definition, so the comparison is approximate.

| Firm | Period | Comp ratio | Margin |
|---|---|---|---|
| EVR | H1'26 | 63.8% (Adj.) | 22.7% (Adj. op) |
| PJT | H1'26 | ~66.5% (release "% of revenues"; basis to verify) | 21.0% (Adj. pretax, 189.5 ÷ 904) |
| MC | Q2'26 | 65.8% (GAAP = Adj.: 269.4 ÷ 409.4) | 17.0% (H1 Adj. pretax) |
| HLI | Q1 FY27 (Jun-26) | 64.3% | ~15.3% (GAAP-basis: 100 − 64.3 − 20.4 non-comp) |
| LAZ | Q2'26 (firm-wide) | 69.9% (Adj.) | n/d; Adj. EPS H1 −50% YoY |
| PWP | H1'26 | 70.8% (Adj.: 215.9 ÷ 305) | ~7.5% (Adj. pretax: 23 ÷ 305) |

EVR currently has the best margin in the group, but that reflects its peak revenue.

Source: Q4 8-K releases FY2013–FY2025; Q2'26 release; peer 8-Ks (July 2026).
Confidence: High for EVR; Medium for peer comparability.

### 11b) Revenue sensitivity: ±10% revenue → EPS (empirical)

**Empirical Adj. decremental and incremental margins:**

| Period | Δ Revenue | Δ Adj. op income | Ratio |
|---|---|---|---|
| 2018→19 | −50.6 | −92.5 | 183% (cost growth continued) |
| 2021→22 | −531.3 | −415.7 | **78%** |
| 2022→23 | −336.3 | −337.3 | **100%** |
| 2021→23 cumulative | −867.6 | −753.0 | **87%** |
| 2020→21 (up) | +989.6 | +499.1 | 50% |
| 2023→24 (up) | +553.3 | +171.9 | 31% |
| 2024→25 (up) | +881.4 | +281.3 | 32% |
| H1'25→H1'26 (up) | +862.2 | +270.9 | 31% |

The response is asymmetric. In upcycles about 31% of incremental revenue falls to operating income, because Evercore reinvests in hires and comp. In downcycles 80–100% of lost revenue comes out of operating income, because deferred-comp amortization, base salaries for the larger SMD base, guarantees and non-comp costs are sticky.

**Sensitivity on TTM Adj. revenue of $4,746mm**, using 26.5% tax, 43.7mm shares, and normalized TTM EPS of ~$17.0 ex-tax-benefit:

| Scenario | Δ Adj. op income | Δ EPS | % of ~$17.0 |
|---|---|---|---|
| +10% revenue (+$475mm) | +$147mm (31%) | +$2.47 | +15% |
| −10% revenue (−$475mm) | −$403mm (85%) | −$6.78 | −40% |

For a stock trading on peak-ish earnings, this is the core risk.

Source: Q4 releases FY2018–FY2025; Q2'26 release; my calculations.
Confidence: Medium-High.

### 11c) Comp-ratio trend vs revenue-per-SMD trend

| Year | Revenue per avg IB SMD ($mm) | Adj. comp ratio |
|---|---|---|
| 2021 | 27.1 | 55.7% |
| 2022 | 20.6 | 60.9% |
| 2023 | 15.6 | 67.6% |
| 2024 | 18.6 | 65.7% |
| 2025 | 21.9 | 64.2% |
| TTM Jun-26 | 24.7 | 63.6% |

- Within a cycle, the comp ratio falls by about 1pp per +$1mm of revenue per SMD.
- Across cycles it has drifted up. At ~$21–22mm per SMD the ratio was 60.9% in 2022 but 64.2% in 2025, a structural upshift of about 3–4pp. Likely causes are higher deferred-comp amortization, more junior and support headcount (2,715 employees, +10.6% YoY), and lateral guarantees.
- IB SMDs rose from 144 (YE24) to 188 (Jun-26 including commits), +31% in 18 months. If revenue per SMD returns to the 2021–25 average of ~$20.8mm, the implied Adj. comp ratio at the current structure is **~65–66%** (est.).

Source: releases (SMD counts, comp ratios); my calculations.
Confidence: Medium.

### 11d) Segment margins

| Segment (Adj.) | H1'26 revenue | H1'26 Adj. op margin | H1'25 Adj. op margin | H1'26 Adj. comp ratio |
|---|---|---|---|---|
| Investment Banking & Equities | 2,352.5 | 22.7% | 17.6% | 63.9% |
| Investment Management | 48.5 | 21.1% | 24.3% | 60.6% |

- Investment Management is only about 2% of revenue and is margin-stable. Wealth AUM is $16.2bn (+12%).
- Equities (commissions $126.2mm in H1) sits inside IB&E and is not separately margined. It is likely low-margin (est.).
- The firm's margin is essentially the IB margin.

Source: Q2'26 release pp. A-4 to A-5.
Confidence: High.

### 11e) Mid-cycle margin estimate and basis (mid-cycle EPS method)

I triangulate mid-cycle earnings three ways.

**(1) Mid-cycle revenue = $4.0bn (2026 basis).**
- **Trend method.** A log-linear trend on Adj. revenue gives 2026 trend values of $4,109mm (fit from 2015) and $3,990mm (fit from 2016), with trend growth of 10–11% a year. TTM revenue of $4,746mm is about **1.16x trend**. Previous ratios: 2021 peak 1.33x; 2023 trough 0.81x; 2025 1.05x.
- **Capacity method.** About 178 effective SMDs (188 less a ramp haircut for 2026 joiners) × $20.0mm mid-cycle productivity (2021–25 average $20.8mm, rounded down) = $3.56bn. Adding non-IB revenue of about $0.45bn (commissions ~$250mm, Investment Management ~$95mm, other/interest ~$110mm) gives about **$4.0bn**.

**(2) Mid-cycle Adj. op margin = 20.0% (est.).**
- Comp ratio of 65.0%: from 11c, the current structure at ~$20mm per SMD.
- Non-comp ratio of 15.0%: about $600mm on $4.0bn, versus the $620mm TTM run-rate.
- I deliberately use less than the 2015–2025 average Adj. margin of 24.8% (median 25.8%). The 2015–2020 years had a comp ratio about 8pp lower, which I do not expect to return given the talent market and the SMD build. FY2025 had revenue near trend and reached 21.6% with fewer SMDs, so 20% for the larger cost base is consistent.

**(3) Mid-cycle EPS (est.).**
- 4,000 × 20.0% = $800mm Adj. operating income.
- Less interest of $27.6mm (Q2'26 Adj. interest $6.9mm × 4) = $772.4mm pre-tax.
- Tax at 26.5%: the ex-vesting Adj. ETR is about 29.4% (Q2'26 and Q4'25), less about 3pp for a normal-year vesting benefit. That gives $567.7mm.
- ÷ 43.6mm shares = **$13.02, rounded to $13.00**.
- **Cross-check A:** FY25 actual Adj. pre-tax of about $816mm × 0.735 ÷ 44.38mm = $13.5 at normalized tax.
- **Cross-check B:** the 2021–25 average Adj. EPS of $11.99 (17.50, 12.01, 6.46, 9.42, 14.56), grown 6% a year for three years from its 2023 midpoint, gives $14.3.
- Range: $13.0–14.3. I use **$13.00**, the conservative end, because the cost base has grown faster than revenue capacity.
- Forward: at about 6% trend growth, mid-cycle EPS is about $13.8 for FY27 and about $14.6 for FY28.

Source: Q4 releases FY2013–FY2025; Q2'26 release; my model.
Confidence: Medium.

**Key judgment (Module 11): current margins (Adj. 23.4% TTM) are about 3.4pp above my mid-cycle 20%. The operating leverage is asymmetric (31% on the way up, about 85% on the way down), and comp intensity rises structurally with the SMD build. Direction: margins rising now but cyclical, partly controllable.**

---

## Module 14 — Pre-mortem ("it is Oct-2028 and EVR has lost 40%+ — why?")

### Death 1 (mandatory): The deal cycle turns or stalls

**Scenario.** The 10-year UST holds above 5% and the rate shock stalls sponsor exits and LBO financing. Strategic M&A slows on antitrust and tariff uncertainty, and the mega-deals in the 2026 backlog (for example WBD/Paramount) are delayed or broken. FY2027 Adj. revenue falls about 25% from TTM, matching the 2021→23 drawdown of −26%.

**Trigger.**
- Announced global M&A volume down more than 20% YoY for two quarters.
- HY spreads above 500bp.
- EVR fee count and fees of $1mm+ down YoY.
- Q3/Q4'26 revenue below consensus while the comp ratio rises.

**Current status (evidence of an early turn).**
- The 10Y rose from about 4.5% in July to 5.24–5.28% in early October 2026.
- Peers are already weakening: HLI Corporate Finance revenue −24% YoY in the June quarter; PWP H1 revenue −17%; LAZ H1 Adj. EPS −50%.
- EVR's Q3 consensus (unverified) implies about −11% YoY Adj. EPS (3.11 vs 3.48).
- EVR is down 30% from its high.
- EVR itself still reported record Q2 revenue (+19%), and management cites broad-based strength. The company gives no numeric guidance.
- Management's response options: flex the comp accrual (Q4 true-up), slow lateral hiring, keep buybacks.

**Probability:** 30% over 24 months.
- Base rate: severe revenue drawdowns of 25% or more occurred in 2008 and 2022–23, two episodes in about 19 years, roughly 10% a year or about 20% over two years.
- I raise this to 30% because the upturn is in its third year (2024–26), there is a rate shock, and peers are deteriorating.

**Impact.**
- Revenue: $3.56bn (4,746 × 0.75).
- Margins: Adj. comp ratio 67.5% (the 2023 level), non-comp $640mm (18%), op margin about 14.5%.
- EPS: 3,560 × 14.5% − 27.6 = $488.6mm; × 0.735 ÷ 43.5mm = **$8.25** (−51% vs ~$17 normalized TTM).
- Multiple: about 20x trough EPS, or about 12.7x mid-cycle. In 2023, P/E on TTM EPS ran 14–30x at the trough.
- **Value: about $165 a share (−39%).**

Source: release data, peer 8-Ks, Yahoo 10Y; my scenario.
Confidence: Medium.

### Death 2 (mandatory): Margin mean-reversion as hiring outruns revenue

**Scenario.** Revenue merely plateaus at about $4.8bn, but the 188-SMD base (+31% in 18 months), amortization of 2025–26 RSU grants ($1.1bn unvested grant value; deferred cash $318.5mm through 2030), guarantees for laterals, and non-comp growth (+27% YoY H1; travel, technology, professional fees, credit-loss provisions) push the Adj. comp ratio to about 66% and non-comp to about 17%.

**Trigger.**
- Adj. comp ratio up YoY for two consecutive quarters while revenue per SMD falls.
- Non-comp growth above 15% with flat revenue.
- Q4'26 comp-ratio true-up above 63.5% for FY26.

**Current status.**
- Q2'26 Adj. non-comp ratio was 17.5%, versus 15.9% a year earlier.
- The Q2 Adj. comp ratio of 63.5% was helped by record revenue.
- Seven more IB SMDs committed after the Q2 call. Hiring is still accelerating.
- Management frames this as "continue to invest", with no stated comp-ratio target. To verify on the Q3 call.

**Probability:** 35% (overlaps with Death 1).

**Impact.**
- Margins: op margin about 17%.
- EPS: (4,800 × 17% − 27.6) × 0.735 ÷ 43.5 = **$13.3** (−22% vs ~$17).
- Multiple: about 15x.
- **Value: about $200 (−26%).**

Source: Q2'26 release (deferred comp, headcount, non-comp detail); my scenario.
Confidence: Medium.

### Death 3 (company-specific): Key-banker and franchise erosion

**Scenario.** Senior rainmakers leave, or the founder generation (Chairman/CEO Weinberg; Senior Chairman Altman) transitions badly. Robey Warshaw's UK founders underperform their earn-out or leave after it ends. Rivals (PJT, Centerview, Lazard's growth plan, bulge brackets) poach teams.

**Trigger.**
- Net IB SMD departures of 5 or more in 12 months, excluding retirements.
- Any top-producer exit.
- Robey Warshaw contingent consideration written down.

**Current status.**
- Disclosed departures are small: 2 known departures adjusted in the Jun-26 count.
- Robey Warshaw: contingent consideration fair value $26.9mm; deferred consideration of £74.8mm ($99.2mm) due at the first anniversary on 1-Oct-2026, in shares or cash. It was due as of this writing (verify settlement). Retention and performance awards are being expensed ($14.2mm in H1'26).

**Probability:** 15%.

**Impact.**
- Revenue about −8% versus base.
- FY28 EPS 19.8 → about 16.8.
- Multiple 13x.
- **Value about $218 (−20%).**

Source: Q2'26 10-Q Note 5; releases.
Confidence: Low-Medium.

### Death 4 (company-specific): The counter-cyclical hedge underdelivers (restructuring / private credit / sponsor in-housing)

**Scenario.** In a downturn, Evercore's Liability Management & Restructuring business is smaller than HLI's or PJT's and offsets less. Private credit resolves distress bilaterally and sponsors in-source M&A. Structural fee-pool loss is about 5%, and the bear-case decline deepens to −30%.

**Trigger.**
- Restructuring league-table share down.
- Private-credit share of leveraged finance continues to rise.
- PCA/PFG revenue down YoY.

**Current status.**
- Evercore's LM&R team was named IFR Americas Restructuring Adviser of the Year for 2025.
- Private Funds Group ranked #1 in PEI's 2025 placement-agent ranking.
- Product-line revenue is **not disclosed** (To verify).

**Probability:** 20%, mainly as an amplifier of Death 1.

**Impact.**
- Standalone: EPS −12%, value about $235.
- With Death 1: revenue −30%, EPS about $6.9.

Source: Q4'25 and Q2'26 releases.
Confidence: Low.

### Death 5 (company-specific, mechanical): Earnings-quality headwinds — vesting tax benefit fade and special charges

**Scenario.** The Q1 tax benefit from RSUs vesting above grant price was $94.0mm in 2026 (about $2.12 a share) and $78.0mm in 2025. In Q1'27, the 2026 grant tranche (granted at about $320–345) would vest below grant price at the current $272. That offsets gains on the 2023–2024 tranches (granted at about $125–200). The benefit could fall to about $20–40mm (est.), a hit of about −$1.2 to −$1.7 a share.

A further item: a special charge of $21.3mm (non-U.S. employment taxes for prior periods; liability $24.9mm) was excluded from Adj. results but is a recurring-type operating risk.

**Trigger:** price below about $300 into Feb/March 2027 vesting.

**Current status:** price $271.86.

**Probability:** 60%.

**Impact.** FY27 Adj. EPS about −6 to −9% versus a flat-price assumption. Multiple is unchanged; value about −$15 to −20 a share.

Source: Q1'26 release (tax benefit); Q2'26 10-Q Note 16.
Confidence: Medium.

### Bear-case summary

| Scenario | Probability (24 mo) | Revenue | Adj. EPS | Multiple | Value/sh | vs $271.86 |
|---|---|---|---|---|---|---|
| D1 Deal cycle turns | 30% | $3.56bn | $8.25 | 20x trough (12.7x mid) | **$165** | −39% |
| D2 Comp/margin mean-reversion | 35% | $4.8bn | $13.3 | 15x | $200 | −26% |
| D3 Key-banker / franchise | 15% | −8% vs base | $16.8 (FY28) | 13x | $218 | −20% |
| D4 Restructuring / private credit hedge fails | 20% | −5% structural | −12% | — | $235 | −14% |
| D5 Tax-benefit fade / special charges | 60% | — | −$1.2 to −$1.7 | unchanged | ~$255 | −6% |
| **Compound (D1 + D2 + D5, partly D4)** | **12%** | $3.32bn (−30%) | **$6.2** | 21x trough (~10x mid) | **$130** | **−52%** |

Compound arithmetic:
- Margin: comp ratio 69% plus non-comp $640mm (19.3%) gives 11.7%.
- EPS: (3,320 × 11.7% − 27.6) × 0.75 ÷ 43.5 = $6.2.
- Analogues: the 2021–22 peak-to-trough was −51% ($163 → $80); 2008 was about −75%.

The bear value used in Kelly is **$165** (D1). The compound $130 is a stress case.

**Is the real risk an earnings collapse or multiple compression?**
- **Primarily an earnings collapse.** Multiple compression has largely happened already. The stock fell from $388.71 to $271.86 (−30%) while TTM EPS rose, and NTM P/E fell from roughly 18–20x (January, on forward EPS of about $19–20) to about 12.8x. That is near the 2020–25 median perfect-foresight forward P/E of 11.1x (mean 12.4x).
- Because of the asymmetric decremental (85–100%), a 25% revenue decline halves EPS. History shows the market then prices EVR on mid-cycle earnings, about 10–13x, rather than on trough or peak EPS. On mid-cycle EPS the stock is still at 20.9x, so a mid-cycle re-rating is the second leg of the risk.

Source: as above.
Confidence: Medium.

**Key judgment (Module 14): the dominant risk is an earnings collapse driven by cycle and comp stickiness. Early-warning signals (rates, peer revenue) are already flashing. Direction: rising, uncontrollable.**

---

## Module 17 — Balance sheet (30-Jun-2026 vs 31-Dec-2025)

### 17a) Cash, investments, debt and net cash; accrued comp as offset

| $mm | 30-Jun-26 | 31-Dec-25 |
|---|---|---|
| Cash and equivalents | 1,256.6 | 1,426.0 |
| Investment securities and CDs (mainly U.S. Treasuries) | 1,148.3 | 1,580.6 |
| **Gross liquidity** | **2,404.9** | **3,006.6** |
| Notes payable (incl. current) | 540.0 | 588.2 |
| **Net cash (gross)** | **1,864.9** | **2,418.4** |
| Accrued compensation and benefits | 940.2 | 1,381.3 |
| **Net cash after accrued comp** | **924.7** | **1,037.1** |
| Further: Robey Warshaw deferred consideration (PV) / TRA | 97.8 / 63.4 | 96.5 / 59.6 |
| Net cash after comp, Robey Warshaw and TRA | ~763 ($17.5/sh) | ~881 |

- Liquidity is seasonal. It troughs in Q1 after bonus payments (cash $986mm at 31-Mar-26).
- Current assets exceeded current liabilities by $1.9bn.
- Broker-dealer EGL net capital is $796.1mm against a $0.25mm minimum.

Source: 10-Q Q2'26 balance sheet and Note 17; Q2'26 release (Liquidity).
Confidence: High.

### 17b) Debt maturity ladder — all fixed-rate senior notes

| Maturity | Note | Coupon | Carrying ($mm) |
|---|---|---|---|
| 3/2026 | Series C | 5.48% | repaid ($48.0mm) |
| 3/2028 | Series D | 5.58% | 17.0 |
| 11/2028 | Series J | 4.61% | 66.4 |
| 8/2029 | Series E | 4.34% | 74.7 |
| 7/2030 | Series K | 5.17% | 124.7 |
| 8/2031 | Series F | 4.44% | 59.7 |
| 7/2032 | Series L | 5.47% | 124.7 |
| 8/2033 | Series G / H | 4.54% / 3.33% | 39.8 / 33.0 |
| **Total** | | about 4.9% weighted (est.) | **540.0** |

- No maturity in any single year exceeds $125mm.
- The unsecured PNC revolver was raised to $225mm (July 2025) and was undrawn per the disclosures.
- Covenants are maximum leverage, minimum tangible net worth and minimum interest coverage; the company was in compliance.
- Refinancing risk: negligible.

Source: 10-Q Note 11 (Notes Payable); 10-Q liquidity section.
Confidence: High.

### 17c) Working capital

Receivables (current) were $568.5mm at Jun-26 ($555.8mm at YE25). Current contract assets were $47.2mm ($147.4mm). Long-term receivables plus long-term contract assets were $179.4mm ($157.8mm).

**DSO (GAAP):**
- YE24: 421.5 ÷ 2,979.6 × 365 = 51.6 days.
- YE25: 555.8 ÷ 3,855.8 × 365 = 52.6 days.
- Jun-26: 568.5 ÷ 4,709.0 TTM × 365 = 44.1 days.

DSO is stable to improving. However, AR rose 32% in FY25 (+$134mm) against revenue +29%, and the bad-debt allowance rose to $5.5mm from $3.0mm (Q2'26 credit-loss provision).

The key working-capital item is accrued comp ($1.38bn at YE25), which is paid in Q1. It is effectively an interest-free liability that partly funds the investment portfolio.

Source: 10-Q Note 4; 10-K.
Confidence: High.

### 17d) Goodwill and intangibles

- Goodwill $227.8mm plus intangibles $22.3mm = $250.1mm, about 13% of Evercore stockholders' equity ($1,858.6mm).
- Goodwill rose from $124.5mm (YE24) to $230.8mm (YE25) with Robey Warshaw.
- Intangible amortization is $3.7mm a quarter (excluded from Adj.).
- The 10-K reports no goodwill, intangible or equity-method impairment in 2023–2025; reporting-unit fair values "substantially exceed" carrying values.
- Historical goodwill declines (2015: 218 → 166; 2016–17: 161 → 134) appear tied to Investment Management impairments and divestitures and FX. To verify the ISI-specific history.

Source: 10-K FY2025 (critical accounting estimates); XBRL Goodwill series.
Confidence: Medium-High.

### 17e) Off-balance-sheet and other obligations

| Item | Amount | Note |
|---|---|---|
| Operating lease liabilities | $553.2mm | 65.3 current + 487.9 long-term; right-of-use assets $445.3mm |
| Deferred cash comp, to be paid through 2030 | $318.5mm | expensed over service period |
| Unvested RSUs | 4.4mm units, $1.1bn grant value | future comp expense |
| TRA | $63.4mm | payments ~$11mm a year |
| Robey Warshaw deferred consideration | $97.8mm (£74.8mm) | due 1-Oct-2026 |
| Robey Warshaw contingent consideration | $26.9mm | |
| Non-U.S. employment-tax liability | $24.9mm | |
| Guarantees | n/q | a portion of annual bonuses is guaranteed (not quantified) |
| Litigation | ordinary course | no material accruals disclosed |

Source: 10-Q Notes 5, 10, 15, 16; Q2'26 release.
Confidence: High (amounts); Medium (completeness).

### 17f) Capex

| Period | Capex ($mm) |
|---|---|
| 2023 | 20.0 |
| 2024 | 30.1 |
| 2025 | 74.0 (office build-outs) |
| H1'26 | 13.8 |

Capex runs at 0.5–2% of revenue. The real investment is hiring, expensed through comp (equity-based and deferred comp of $675.1mm in FY25).

Source: 10-K and 10-Q cash flow statements.
Confidence: High.

**Key judgment (Module 17): the balance sheet is a fortress (net cash of $0.9–1.9bn depending on treatment, small fixed-rate laddered debt) and is not a source of risk. Direction: controllable.**

---

## Module 18 — Accounting quality

### 18a) Auditor

Deloitte & Touche LLP has been the auditor since 2003. It gave an unqualified opinion on FY2025 and an unqualified ICFR opinion (20-Feb-2026). No material weakness and no auditor change. The critical audit matter is year-end success-fee recognition.

Source: 10-K FY2025 auditor's report.
Confidence: High.

### 18b) Non-GAAP gap and add-backs

| Period | GAAP EPS | Adj. EPS | Gap | Main drivers |
|---|---|---|---|---|
| FY2015 | 0.98 | 3.23 | +230% | ISI acquisition-related comp and intangibles |
| FY2017 | 2.80 | 5.45 | +95% | Tax Cuts and Jobs Act remeasurement, ISI items |
| FY2021 | 17.08 | 17.50 | +2.5% | LP conversion |
| FY2023 | 6.37 | 6.46 | +1.4% | |
| FY2024 | 9.08 | 9.42 | +3.7% | |
| FY2025 | 14.05 | 14.56 | +3.6% | LP units, Robey Warshaw (Q4) |
| H1'26 | 9.56 | 10.48 | +9.6% | special charge $21.3mm, Robey Warshaw comp $14.2mm, intangibles $7.4mm, contingent consideration $2.8mm, lease impairment $1.8mm |

- In dollars, Adj. net income exceeds GAAP by more (FY25 $646.3mm vs $591.9mm, +9.2%) mainly because noncontrolling interest is added back. The LP units (2.56mm) are added to the share count, so the EPS gap is small.
- The gap is widening again with Robey Warshaw (four-year retention and comp awards).
- The "special charge" for prior-period non-U.S. employment taxes is arguably an operating cost. I treat it as a quality flag.

Source: Q4 releases; Q2'26 release pp. A-2 and A-3.
Confidence: High.

### 18c) Receivables and contract assets vs revenue growth

See 17c. DSO is about 44–53 days and stable. Contract assets swing seasonally: they build at year end and reverse in H1. Long-term placement receivables are growing faster than revenue (+55% since YE24 vs revenue +58% TTM), which is acceptable but worth watching. No red flags.

Source: 10-Q Note 4.
Confidence: Medium-High.

### 18d) Deferred comp accounting, accruals, and the Q1 vesting tax benefit

- Annual bonus awards are granted in Q1, vest over four years, and are amortized subject to retirement eligibility. Intra-year comp is accrued at an estimated full-year ratio and trued up in Q4, so Q4 margins are a management judgment.
- The equity-based plus deferred comp add-back was $675.1mm in FY25, or 17.5% of GAAP revenue.
- The Q1 vesting tax benefit (Adj.) was $78.0mm in 2025 and $94.0mm in 2026. That drove the FY25 Adj. ETR to 19.8% and the Q1'26 Adj. ETR to 3.0%, against about 29–30% in normal quarters.
- Recurrence depends on the share price at Q1 vesting relative to the grant prices of 2022–2025 awards. At $272 the 2026 tranche would be under water (see Death 5). For valuation I normalize tax at 26.5%.

Source: Q1'26 and Q2'26 releases; 10-Q MD&A.
Confidence: Medium-High.

### 18e) Restatements and SEC comment letters

- No restatements identified.
- The last CORRESP/UPLOAD exchange with SEC staff on EDGAR was Dec-2013 to Feb-2014.
- No 10-K/A or 10-Q/A filings in the filing list (2013–2026).
- 2017 Adj. results were recast for ASC 606 (comp ratio 58.5% → 57.5%). That is a presentation change, not an error.

Source: EDGAR submissions (CIK 1360901).
Confidence: High.

**Key judgment (Module 18): accounting is clean and well audited. The main judgment areas are year-end success-fee timing, the Q4 comp true-up and the price-dependent vesting tax benefit, which inflated FY25 and FY26 Adj. EPS by about $1.8–2.1 a year. Direction: controllable, quality stable.**

---

## Module 19 — Cash flow

### 19a) Operating cash flow vs net income

| FY | OCF ($mm) | Net income attributable, GAAP ($mm) | OCF/NI |
|---|---|---|---|
| 2016 | 421.9 | 107.5 | 3.9x |
| 2017 | 507.2 | 125.5 | 4.0x |
| 2018 | 849.6 | 377.2 | 2.3x |
| 2019 | 504.7 | 297.4 | 1.7x |
| 2020 | 978.4 | 350.6 | 2.8x |
| 2021 | 1,384.9 | 740.1 | 1.9x |
| 2022 | 531.4 | 476.5 | 1.1x |
| 2023 | 458.0 | 255.5 | 1.8x |
| 2024 | 988.2 | 378.3 | 2.6x |
| 2025 | 1,256.5 | 591.9 | 2.1x |
| H1'26 / H1'25 | 299.7 / (111.9) | 396.5 / 243.4 | seasonal (Q1 bonus payout −$518.7mm) |

OCF/NI is persistently above 1 because SBC and deferred comp are non-cash ($675mm in FY25), and in up-years the accrued-comp build adds cash. In down-years (2022–23) the comp accrual unwinds; 2023's accrued-comp change was −$325.7mm.

Source: XBRL (NetCashProvidedByUsedInOperatingActivities, NetIncomeLoss); 10-K and 10-Q cash flow statements.
Confidence: High.

### 19b) FCF and FCF yield

- **Reported FCF.** TTM OCF = 1,256.5 + 299.7 − (−111.9) = $1,668.1mm. TTM capex = 74.0 + 13.8 − 45.7 = $42.1mm. **FCF = $1,626mm, a 13.7% yield** on the $11.88bn adjusted-diluted market cap.
- **Economic FCF after SBC.** TTM equity-based and deferred comp = 675.1 + 415.4 − 329.4 = $761.1mm, so FCF − SBC = $865mm, a **7.3% yield**.
- **FY2025.** FCF $1,182.5mm; FCF − SBC $507mm (4.3% at today's cap).

Treat the SBC-adjusted figure as the real owner FCF, because buybacks largely exist to offset SBC (19e).

Source: 10-K and 10-Q cash flow statements; my calculations.
Confidence: Medium-High.

### 19c) Is FCF funding hiring plus capital return?

- **FY2025.** FCF of $1,182.5mm covered dividends $144.4mm + buybacks $661.8mm + NCI distributions $30.7mm + TRA $11.4mm = $848.3mm, or 1.39x. Cash also rose $554mm, helped by $250mm of new notes.
- **H1'26.** Returns of $821.2mm (buybacks $736.5mm + dividends $84.7mm) plus $48mm of note repayment exceeded FCF of $285.9mm by about 2.9x. The gap was funded by running down Treasuries by about $432mm.
- **TTM.** FCF $1,626mm vs returns ~$1,098mm, or 1.48x.

Hiring is already inside OCF as comp. Yes, FCF funds both, but H1'26 buybacks at an average of $324.60 a share were front-loaded near the top of the range.

Source: cash flow statements; releases.
Confidence: High.

### 19d) Dividend coverage

- Current dividend is $0.89 a quarter ($3.56 a year), a 1.31% yield. It was raised 6% in April 2026 and has been raised every year (2009 $0.51 → 2025 $3.32).
- Payout ratio: 18% of TTM Adj. EPS, about 27% of mid-cycle EPS ($13.00), and about 43% of bear EPS ($8.25).
- FY25 cash dividends of $144mm were 8.2x covered by FCF.

The dividend is safe even in the compound bear case ($6.2 EPS, 57% payout).

Source: releases; XBRL dividends-per-share series.
Confidence: High.

### 19e) Buybacks net of SBC dilution

| Year | Weighted diluted shares, GAAP (mm) |
|---|---|
| 2014 | 41.8 |
| 2016 | 44.2 |
| 2018 | 45.3 |
| 2020 | 42.6 |
| 2022 | 41.0 |
| 2023 | 40.1 |
| 2024 | 41.6 |
| 2025 | 42.1 |

- Adjusted diluted shares were 43.55mm in Q2'25 and 43.71mm in Q2'26 (**+0.4% despite about $948mm of TTM repurchases**).
- 51.3mm shares are held in treasury at a cost of $5.30bn.
- Over 2016–2025 the share count fell only about 5% while the company spent roughly $4bn+ on repurchases (est.).
- **Gross buyback yield is about 8.0%** (948 ÷ 11,880). **Net buyback yield is about 0%.**
- The authorization is the lesser of $1.6bn and 8.0mm shares from 29-Apr-2025.

Buybacks are effectively the cash settlement of comp. Valuing EVR on "total shareholder yield" overstates owner returns unless SBC is treated as a cost (Adjusted EPS already does this).

Source: XBRL; Q2'26 10-Q (treasury, authorization); releases.
Confidence: High.

**Key judgment (Module 19): cash generation is strong but flatters reported FCF because about 45% of it offsets SBC. True owner FCF yield is about 4–7%. Capital return is sustainable, and the dividend is very safe. Direction: controllable.**

---

## Module 20 — Valuation

### 20a) P/E (Adjusted, NTM and TTM) vs own history — pre-2020 vs current cycle

Method: quarter-end price ÷ Adj. EPS. The "perfect-foresight forward" is the next four reported quarters and serves as a proxy for historical NTM consensus, which I do not have.

| Measure | 2010–2019 (pre-2020) | 2020–Q2'26 (current cycle) | Now |
|---|---|---|---|
| P/E TTM Adj., mean / median | 18.5x / 17.1x | 16.0x / 12.8x | **14.3x** (16.0x ex-tax-benefit) |
| P/E TTM range | 7.9–35.4x | 5.3–31.7x | |
| P/E forward (perfect foresight), mean / median | 15.1x / 13.3x | 12.4x / 11.1x | **~12.8x** NTM consensus-derived |
| Price ÷ trailing 5-year average EPS | 25.2x median (biased up by fast growth) | 15.7x median (7.6–28.4x) | **21.3x** |
| P/E on my mid-cycle EPS | — | — | **20.9x** |

Two cautions:
- The 2018 tax cut lowered the ETR from about 40% to about 25%, which mechanically raised EPS and cut P/Es after 2018, so the pre/post split partly reflects tax.
- The pattern is classic cyclical. The TTM P/E peaked at 26–32x in the 2023–24 trough (Q3'24 31.7x) and bottomed at 5.3x at the 2022 earnings peak.

On NTM the stock is near its current-cycle average. On mid-cycle it is expensive.

Source: evr_quarterly_data.json; Q4 releases; my calculations.
Confidence: Medium-High.

### 20b) Peer comps (prices 9-Oct-2026; TTM Adj. EPS from primary releases)

| Firm | Price | TTM Adj. EPS (calc) | P/E TTM | P/E NTM | Div yield | Latest revenue growth | Comp ratio | Margin |
|---|---|---|---|---|---|---|---|---|
| **EVR** | 271.86 | 19.05 = 3.48 + 5.13 + 7.53 + 2.91 | **14.3x** | ~12.8x (est.) | 1.3% | H1'26 +56% | 63.8% Adj. | 22.7% Adj. op |
| PJT | 137.28 | 7.91 = 6.98 + 3.51 − 2.58 | 17.4x | To verify | 0.7% | H1'26 +24% | ~66.5% | 21.0% Adj. pretax |
| MC | 57.08 | 2.95 = 2.99 + 1.13 − 1.17 | 19.3x | To verify | 4.6% | H1'26 +9% | 65.8% | 17.0% Adj. pretax |
| HLI (FY Mar) | 130.16 | 6.77 = 7.56 + 1.35 − 2.14 | 19.2x | To verify | 2.2% ($0.70/q) | Q1 FY27 −15.5% | 64.3% | ~15% GAAP op (est.) |
| LAZ | 36.75 | 1.90 = 2.44 + 0.54 − 1.08 | 19.3x | To verify | 5.4% | H1'26 Adj. +3% | 69.9% Adj. | n/d |
| PWP | 15.67 | 0.55 = 0.68 + 0.25 − 0.38 | 28.5x | To verify | 1.8% | H1'26 −17% | 70.8% Adj. | 7.5% Adj. pretax |

- PJT H1'25 Adj. EPS is derived as 3.51 ÷ 1.36 (the release states +36%).
- Peer buyback yields are not computed; LAZ returned $277mm in H1, MC $246mm, PWP $73mm. Peer NTM consensus is not verified from a primary source (information gap).

EVR is the cheapest peer on TTM because it has the most elevated earnings: the highest growth and margin in H1'26. Peers with depressed earnings (HLI, LAZ, PWP) trade at 19–29x TTM. On normalized earnings EVR is not cheap relative to the group. The market is applying a "peak-earnings discount" to EVR.

Source: peer 8-K releases (July 2026; Jan/May 2026); Yahoo prices.
Confidence: Medium.

### 20c) Reverse DCF / implied growth on mid-cycle EPS

**Cost of equity:**
- 10Y UST 5.28% (user; Yahoo 5.24% on 9-Oct).
- EVR 5-year weekly beta vs S&P 500 is **1.49** (2-year 1.99), computed from Yahoo prices.
- ERP 4.5%.
- CAPM: 5.28 + 1.49 × 4.5 = 12.0%. I use **11.5%** as the base, tempered for EVR's net-cash balance sheet, with **10.5%** and **12.5%** as the sensitivity range.

**Single-stage:** P = E₁ × payout ÷ (r − g), with E₀ = mid-cycle $13.00 and E₁ = E₀(1 + g).

| r | Payout 100% | Payout 90% | Two-stage: 10-year growth needed (then 4% terminal) | Implied g on NTM consensus $21.2 |
|---|---|---|---|---|
| 10.5% | 5.5% | 5.9% | 7.6% | 2.5% |
| **11.5%** | **6.4%** | **6.9%** | **9.7%** | **3.4%** |
| 12.5% | 7.4% | 7.9% | 11.6% | 4.4% |

Worked example (r = 11.5%, payout 100%):
- 271.86 × (0.115 − g) = 13.00 × (1 + g)
- → 31.26 − 13.00 = (271.86 + 13.00) × g
- → g = 18.26 ÷ 284.86 = **6.41%**

**Interpretation.**
- On mid-cycle EPS, the price implies about 6.4% perpetual growth, or about 9.7% a year for 10 years before fading to 4%. That would mean Evercore keeps compounding near its 2015–25 trend (10–11%) and keeps gaining share for another decade.
- On consensus NTM EPS (treated as sustainable), the implied growth is only 3.4%, which looks cheap.

**The valuation hinges on whether ~$21 is a normal or a peak earnings level.** My base case is that FY26–27 earnings are about 1.4–1.6x mid-cycle, so the market is not offering a mid-cycle margin of safety at $272.

Source: my calculations; Yahoo prices (beta).
Confidence: Medium.

### 20d) Scenario DCF, including a mid-cycle-margin case

Assumptions: 10-year Adj. EPS paths (Adj. EPS ≈ distributable cash, since SBC is already expensed); terminal growth 4%; values in $ a share at 10-Oct-2026.

| Case | EPS path FY27 / FY28 / FY29 → FY36 | r = 10.5% | **r = 11.5%** | r = 12.5% |
|---|---|---|---|---|
| Consensus extrapolation (no cycle) | 23.24 / 26.72 / +6% a year → 42.6 | 440 | **379** | 333 |
| Base cyclical (my FY27–28, then revert to mid-cycle trend) | 18.5 / 19.8 / 15.5 → 23.3 | 250 | **217** | 191 |
| **Mid-cycle-margin case** (20% Adj. margin from FY27; mid-cycle EPS $13.00 +6% a year) | 13.8 / 14.6 / 15.5 → 23.3 | 241 | **208** | 183 |
| Bear (D1, then 95% of mid-cycle path) | 11.0 / 8.25 / 11.0 / 15.6 → 22.1 | 220 | **189** | 165 |
| Compound (90% of mid-cycle path after trough) | 9.0 / 6.2 / 8.5 / 11.0 → 21.0 | 202 | **172** | 150 |

At an 11.5% cost of equity, only the no-cycle consensus extrapolation justifies today's price. The mid-cycle-margin case is worth about $208, about 24% below the price. At 10.5% the base case reaches $250.

The DCF is highly rate-sensitive. The sell-off from $341 (30-Jun) to $272 coincided with the 10Y rising from about 4.4% to about 5.3%.

Source: my model.
Confidence: Medium.

### 20e) IPO-specific analysis

N/A. Evercore IPO'd in August 2006 and has a 20-year public history, so IPO-specific analysis (lock-ups, IPO pricing) does not apply. The overhang analogue is the LP units and unvested RSUs: 2.56mm LP units and 4.4mm unvested RSUs, already included in the adjusted share count.

Source: Q2'26 release p. A-3.
Confidence: High.

**Key judgment (Module 20): EVR looks cheap on peak-ish NTM earnings (12.8x) and on peer TTM, but expensive on mid-cycle earnings (20.9x; implied perpetual growth about 6.4% at an 11.5% cost of equity). Intrinsic value is about $208–217 under mid-cycle/base assumptions. Direction: valuation risk falling (the de-rating has started) but still leading earnings risk.**

---

## Module 21 — Decision and sizing

### 21a) Three scenarios: FY2028 Adj. EPS × target P/E

| Scenario | Probability | FY28 revenue | Adj. op margin | Shares | FY28 Adj. EPS | Target P/E (NTM at end-2027) | Value/sh | vs $271.86 |
|---|---|---|---|---|---|---|---|---|
| Bull: cycle extends, rates ease, SMD build monetizes | 25% | $6.0bn | 26.0% | 43.0mm | **$26.40** | 16x | **$422** | +55% |
| Base: late-cycle plateau, higher rates, comp intensity up | 45% | $5.2bn | 23.0% | 43.3mm | **$19.80** | 14x | **$277** | +2% |
| Bear: D1, the deal cycle turns | 30% | $3.56bn (FY27–28 trough) | 14.5% | 43.5mm | **$8.25** | 20x trough (12.7x mid) | **$165** | −39% |
| **Probability-weighted** | | | | | | | **~$280** | **+3%** |

EPS arithmetic:
- Bull: (6,000 × 26% − 27.6) × 0.74 ÷ 43.0 = $26.4. This is consistent with WallStreetZen's FY28 consensus of $26.72 (non-primary).
- Base: (5,200 × 23% − 27.6) × 0.735 ÷ 43.3 = $19.8.
- Bear: (3,560 × 14.5% − 27.6) × 0.735 ÷ 43.5 = $8.25.

Bull and base values are undiscounted end-2027 values. Discounting at 11.5% for about 1.2 years would cut them by about 12%.

My base sits about 26% below consensus FY28 because:
- Consensus needs about $27mm+ of revenue per SMD on 195–200 SMDs, a 2021-peak productivity level, sustained for two more years.
- My base assumes about $24mm.

Basis for the target multiples: base 14x sits between the 2020–25 median perfect-foresight forward P/E (11.1x) and the pre-2020 median (13.3x), slightly generous given a 5.3% 10Y; bull 16x requires rates to ease.

Source: my model; consensus non-primary as labeled.
Confidence: Medium (base); Low (bull/bear probabilities).

### 21b) Sizing — Kelly with the deal-cycle factor cap

Kelly: f* = (p × b − q) / b; p = probability the base/bull case plays out, q = 1 − p, b = (base value − price) / (price − bear-case value). Inputs are subjective; f* is halved and then capped by aggregate deal-cycle factor exposure. Not investment advice.

**Inputs:** price $271.86; base value $277; bear value $165 (Module 14, D1).

**p = 0.70.** Basis: 1 − 30% probability of D1 over 24 months. The D1 probability rests on a historical base rate of severe drawdowns (about 20% per two years), raised for a third-year upturn, a 5.3% 10Y and deteriorating peers.

**Calculation:**
- b = (277 − 271.86) / (271.86 − 165) = 5.14 / 106.86 = **0.048**
- f* = (0.70 × 0.048 − 0.30) / 0.048 = (0.034 − 0.30) / 0.048 = **−5.5, so the position is 0%**
- Half-Kelly: 0%.
- Sensitivity: even at p = 0.80, f* = (0.038 − 0.20) / 0.048 < 0. Using the DCF base ($217) instead of $277 makes b negative.

**Price at which Kelly turns positive** (p = 0.70; need b ≥ q/p = 0.4286):

| Price | b | f* | Half-Kelly |
|---|---|---|---|
| $260 | 0.18 | <0 | 0% |
| $250 | 0.32 | <0 | 0% |
| **$243** | 0.44 | 0.01 | **~0.6%** (breakeven) |
| $233 | 0.65 | 0.24 | 11.8% |
| $220 | 1.04 | 0.41 | 20.5% |
| $200 | 2.20 | 0.56 | 28.2% |

Breakeven arithmetic: 277 − P ≥ 0.4286 × (P − 165), so P ≤ (277 + 70.7) ÷ 1.4286 = $243.4.

**Factor cap.** The aggregate deal-cycle basket limit is **15–20% of the portfolio**. It covers EVR plus all names that move with M&A and capital-markets activity: other boutiques (PJT, LAZ, MC, HLI, PWP), bulge-bracket IB (GS, MS), alternative managers, brokers and exchange-volume names. Within that, EVR is capped at **6%** of the portfolio.

**Binding constraint:**
- At today's price: **Kelly itself (f* < 0), so no position.**
- Between about $243 and $235: the half-Kelly result is the constraint (<10%), further limited by the 6% single-name cap.
- Below about $233: the **factor basket cap** binds. Half-Kelly (12–28%) exceeds the single-name cap and any remaining room in the basket.

**Key judgment (21b):** zero allocation at $271.86. The constraint is the poor payoff asymmetry (base value about equal to price, bear −39%), not factor crowding.

Source: Module 14 and 21a inputs; my calculations.
Confidence: Medium (method); Low (p).

### 21c) Buy zones and exit conditions

Anchors: mid-cycle EPS $13.00; NTM Adj. EPS about $21.2 (consensus-derived, est.).

| Tier | P/E on mid-cycle EPS | Price | Implied P/E NTM | Action |
|---|---|---|---|---|
| 1 Deeply undervalued | ≤ 10x | ≤ $130 | ≤ 6.1x | Full position up to cap (compound-bear level; 2008/2022 analogues) |
| 2 Undervalued | 10–12x | $130–156 | 6.1–7.4x | Build to 6% cap (basket permitting) |
| 3 Attractive | 12–14.5x | $156–189 | 7.4–8.9x | Accumulate; half-Kelly far exceeds cap |
| 4 Fair | 14.5–17x | $189–221 | 8.9–10.4x | Starter to half position (DCF base/mid-cycle $208–217 sits here) |
| 5 Full | 17–20x | $221–260 | 10.4–12.3x | Small starter only below ~$243 (Kelly breakeven); otherwise hold, no add |
| 6 Overvalued | > 20x | > $260 | > 12.3x | **Current ($271.86 = 20.9x mid / 12.8x NTM)**: no new money; trim existing above $301 (23x mid) |

**Exit conditions (four categories, numeric):**
1. **Fundamentals.** Any of the following:
   - Adj. comp ratio up YoY **and** advisory revenue down YoY for **2 consecutive quarters**.
   - Net IB SMD departures of **5 or more in 12 months** (excluding retirements), or the exit of any named top producer.
   - TTM Adj. op margin below **17%**.
   - Fees of $1mm+ down more than **15% YoY** for 2 quarters.
2. **Valuation.** Trim at P/E on mid-cycle EPS above **23x (>$300)**; exit above **26x (>$338)** or P/E NTM above 16x, unless mid-cycle EPS is revised up.
3. **Industry turn.** Any of the following:
   - Announced global M&A volume down more than **20% YoY for two consecutive quarters**.
   - HY OAS above **500bp**.
   - 10Y UST above **5.75%** for 1 month.
   - Sponsor-backed exit volume down more than **25% YoY**.
4. **Discipline stop-loss.** Halve the position at **−20%** from average cost; exit at **−30%**, or on a close below the bear value ($165) without a thesis review. Re-underwrite after any quarter where revenue misses consensus by more than 15%.

Source: my framework built on Modules 11, 14 and 20.
Confidence: Medium.

### 21d) Catalysts and headwinds, with timing

| Date | Event | Watch |
|---|---|---|
| 28-Oct-2026 | Q3'26 earnings | Consensus revenue ~$1.02bn, Adj. EPS ~$3.11 (unverified); YoY revenue (Q3'25 was $1,038.9mm); comp ratio trajectory; non-comp growth; SMD commits; backlog tone |
| ~28–29 Oct and ~Dec-2026 | FOMC meetings | Exact dates to verify. With the 10Y at 5.2–5.3%, the curve and term premium matter more than the funds rate for sponsor activity |
| 1-Oct-2026 (just passed) | Robey Warshaw deferred consideration (£74.8mm) due | Settled in cash or shares (verify in the Q3 10-Q) |
| Early Feb-2027 | Q4'26 / FY26 results | FY comp-ratio true-up; FY27 hiring plan |
| Q1-2027 | RSU vesting | Size of the vesting tax benefit (Death 5); FY26 bonus pool |
| 2026–2028 | Leveraged-loan and HY maturity wall | Supports LM&R in a downturn (partial hedge) |
| Ongoing | Mega-deal regulatory approvals (WBD/Paramount Skydance, Devon/Coterra and others) | Closing timing moves success fees between quarters |

Headwinds: rate shock; peer revenue declines (HLI, PWP, LAZ); non-comp inflation; the stock's beta of about 1.5–2.0.

Tailwinds: record H1 fees; 188 SMDs; a Q4 seasonal peak; net cash and buybacks.

Source: releases; peer 8-Ks; Yahoo.
Confidence: Medium (event dates partly to verify).

### 21e) One-sentence thesis

Evercore is a best-in-class, net-cash advisory franchise whose earnings are about 1.5x mid-cycle and whose cost base just grew 30%; at $272 (12.8x peak-ish NTM but 20.9x mid-cycle EPS, about 6.4% implied perpetual growth at an 11.5% cost of equity), the payoff is roughly symmetric to slightly negative (base about $277, bear $165), so I would wait for under about $243, and ideally for the $189–221 fair zone, before taking a size-capped deal-cycle position.

Confidence: Medium.

**Key judgment (Module 21): no position at the current price. The binding constraint is Kelly (unfavorable asymmetry), not the factor cap. Direction: wait for lower prices; leading signals (rates, peers) are deteriorating.**

---

## Information-gap table

| # | Gap | Why it matters | How to close | Status |
|---|---|---|---|---|
| 1 | Consensus FY26/27/28 Adj. EPS and Q3'26 (user $22.19 FY27; WallStreetZen $23.24) | NTM P/E, sentiment | Bloomberg/FactSet/LSEG | To verify |
| 2 | Peer NTM P/E and buyback yields | 20b peer comps | Consensus terminal | To verify |
| 3 | Revenue by product (strategic M&A, LM&R, PCA/PFG, ECM) | Death 4, fee-pool mix | Investor presentations, call transcripts | Not disclosed |
| 4 | Robey Warshaw revenue contribution and settlement of £74.8mm due 1-Oct-2026 | 8a organic growth; Death 3 | Q3'26 10-Q | Not disclosed / To verify |
| 5 | Largest individual fees (e.g., WBD) and top-10 fee share | Lumpiness, 8d | Not disclosed; deal-fee filings (proxy statements of targets) | Not disclosed |
| 6 | Gross SMD departures (not just net) | Death 3 trigger | Press tracking, FINRA BrokerCheck | To verify |
| 7 | Historical goodwill-impairment detail (2015–2017) | 17d | 10-Ks for FY2015–FY2017 | To verify |
| 8 | Future vesting schedule by grant price | Size of Death 5 | 10-K equity note | Partly disclosed |
| 9 | FOMC meeting dates and announced M&A volume data for Q3'26 | 21c/21d triggers | Fed calendar; LSEG/Dealogic | To verify |
| 10 | Notes denominated in foreign currency (Series H/J) | FX exposure of debt | 10-K Notes Payable note | To verify |

---

## Data appendix

### A. Annual core financials — U.S. GAAP

Source: evr_quarterly_data.json (sums of quarters; Q4 releases). Op margin = (net revenue − total opex) ÷ net revenue.

| FY | Net revenue ($mm) | Comp ratio | Op margin | Net income attributable ($mm) | Diluted EPS (sum of quarters) | Year-end price |
|---|---|---|---|---|---|---|
| 2007 | 321.6 | 93.1%* | −17.1%* | −34.5 | −3.60* | 21.55 |
| 2008 | 194.7 | 75.3% | −4.8% | −4.7 | −0.35 | 12.49 |
| 2009 | 313.1 | 67.3% | 6.3% | −1.6 | −0.21 | 30.40 |
| 2010 | 375.9 | 65.9% | 9.8% | 9.0 | 0.39 | 34.00 |
| 2011 | 524.3 | 68.2% | 6.8% | 7.0 | 0.26 | 26.62 |
| 2012 | 642.4 | 67.0% | 10.2% | 28.9 | 0.86 | 30.19 |
| 2013 | 765.4 | 63.5% | 17.0% | 53.3 | 1.38 | 59.78 |
| 2014 | 915.9 | 60.0% | 18.7% | 86.9 | 2.07 | 52.37 |
| 2015 | 1,223.3 | 64.4% | 10.5% | 42.9 | 0.98 (FY) | 54.07 |
| 2016 | 1,440.1 | 62.5% | 18.1% | 107.5 | 2.43 (FY) | 68.70 |
| 2017 | 1,704.3 | 56.5% | 25.2% | 125.5 | 2.80 (FY) | 90.00 |
| 2018 | 2,064.7 | 58.0% | 26.3% | 377.2 | 8.33 (FY) | 71.56 |
| 2019 | 2,008.7 | 59.8% | 21.8% | 297.4 | 6.89 (FY) | 74.76 |
| 2020 | 2,263.9 | 60.6% | 23.3% | 350.6 | 8.22 (FY) | 109.64 |
| 2021 | 3,289.5 | 56.2% | 33.5% | 740.1 | 17.08 (FY) | 135.85 |
| 2022 | 2,762.0 | 61.5% | 25.2% | 476.5 | 11.61 (FY) | 109.08 |
| 2023 | 2,425.9 | 68.3% | 14.8% | 255.5 | 6.37 (FY) | 171.05 |
| 2024 | 2,979.6 | 66.3% | 17.7% | 378.3 | 9.08 (FY) | 277.19 |
| 2025 | 3,855.8 | 64.9% | 20.5% | 591.9 | 14.05 (FY) | 340.25 |
| H1'26 | 2,381.8 | 64.9% | 20.0% | 396.5 | 9.56 | 341.44 (30-Jun) |
| TTM Jun-26 | 4,709.0 | 64.5% | ~21.4% | 745.1 | 17.69 | 271.86 (9-Oct) |

\*2007 includes a $126.0mm non-cash vesting charge tied to the May-2007 offering, and pre-2008 partner pay is not fully comparable. EPS shown as "(FY)" is the full-year reported figure; earlier years are sums of quarterly figures.

### B. Annual core financials — Adjusted (non-GAAP; as reported in each Q4 release)

| FY | Adj. net revenue | Adj. comp ratio | Adj. op margin | Adj. net income ($mm) | Adj. diluted EPS |
|---|---|---|---|---|---|
| 2007–2012 | n/a | n/a | n/a | n/a | 1.56 / 0.12 / 0.85 / 0.96 / 1.49 / 1.78 (sum of quarters as first reported; 2012 per release) |
| 2013 | 760.1 | 59.2% | n/d | 103.7 | 2.25 |
| 2014 | 911.9 | 59.0% | n/d | 124.3 | 2.59 |
| 2015 | 1,216 | 57.8% | 24.0% | 171 | 3.23 |
| 2016 | 1,431 | 57.3% | 26.5% | 223.0 | 4.32 |
| 2017 | 1,625.8 | 57.5% (restated; 58.5% first reported) | 26.2% | n/d | 5.45 |
| 2018 | 2,083.2 | 56.7% | 28.4% | 454.0 | 9.01 |
| 2019 | 2,032.6 | 58.2% | 24.5% | 373.3 | 7.70 |
| 2020 | 2,327.3 | 58.9% | 27.5% | 459.6 | 9.62 |
| 2021 | 3,316.9 | 55.7% | 34.3% | 843.2 | 17.50 |
| 2022 | 2,785.6 | 60.9% | 25.9% | 528.7 | 12.01 |
| 2023 | 2,449.3 | 67.6% | 15.7% | 276.9 | 6.46 |
| 2024 | 3,002.6 | 65.7% | 18.6% | 415.8 | 9.42 |
| 2025 | 3,884.0 | 64.2% | 21.6% | 646.3 | 14.56 |
| H1'26 | 2,401.0 | 63.8% | 22.7% | 461.8 | 10.48 |
| TTM Jun-26 | 4,746.2 | 63.6% | 23.4% | 847.9 | 19.05 (sum of quarters) |

Adj. ETR: 2024 21.8%; 2025 19.8%; Q1'26 3.0% (vesting benefit $94.0mm); Q2'26 29.4%.

### C. Quarterly detail, last 8 quarters

| Quarter | GAAP net revenue | GAAP comp ratio | GAAP EPS | Adj. EPS | Quarter-end price |
|---|---|---|---|---|---|
| Q3'24 | 734.2 | 66.5% | 1.86 | 2.04 | 253.34 |
| Q4'24 | 975.3 | 65.6% | 3.30 | 3.41 | 277.19 |
| Q1'25 | 694.8 | 66.2% | 3.48 | 3.49 | 199.72 |
| Q2'25 | 833.8 | 65.8% | 2.36 | 2.42 | 270.02 |
| Q3'25 | 1,038.9 | 65.5% | 3.41 | 3.48 | 337.32 |
| Q4'25 | 1,288.3 | 63.0% | 4.76 | 5.13 | 340.25 |
| Q1'26 | 1,391.6 | 65.0% | 7.20 | 7.53 | 298.51 |
| Q2'26 | 990.2 | 64.8% | 2.32 | 2.91 | 341.44 |

### D. Valuation snapshot (10-Oct-2026)

| Item | Value | Basis |
|---|---|---|
| Price | $271.86 | close 9-Oct-2026 |
| Class A shares outstanding | 38.45mm | 30-Jun-26 balance sheet |
| Adjusted diluted shares (incl. 2.56mm LP units) | 43.71mm | Q2'26 |
| Market cap | $10.45bn (Class A) / **$11.88bn** (adjusted diluted) | |
| Net cash, gross / after accrued comp / after comp, Robey Warshaw and TRA | $1,864.9mm / $924.7mm / ~$763mm | 30-Jun-26 |
| EV / TTM Adj. op income ($1,109.5mm) | 9.0x (gross net cash) / 9.9x (after accrued comp) | (11.88 − 1.86) ÷ 1.11; (11.88 − 0.92) ÷ 1.11 |
| P/E TTM — Adj. / Adj. ex-tax-benefit / GAAP | 14.3x / 16.0x / 15.4x | |
| P/E NTM (Adj., consensus-derived, est.) | ~12.8x | EPS ~$21.2 |
| P/E FY27 consensus (user $22.19 / WallStreetZen $23.24) | 12.3x / 11.7x | non-primary |
| P/E on mid-cycle EPS ($13.00) | 20.9x | my estimate |
| Dividend yield | 1.31% | $3.56 ÷ 271.86 |
| Gross buyback yield (TTM $948mm) | 8.0% | |
| Net buyback yield (share-count change) | ~0% (adjusted diluted shares +0.4% YoY) | |
| FCF yield — reported / after SBC | 13.7% / 7.3% | TTM |
| Book value (Evercore stockholders' equity) | $1,858.6mm (~$42.5/adj. share); P/B ~6.4x | 30-Jun-26 |
| 52-week range | $251.13 – $388.71 (−30% from high) | |
| Beta (5-year weekly vs S&P 500) | 1.49 | Yahoo-derived |
