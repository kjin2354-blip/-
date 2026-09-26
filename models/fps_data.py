"""Sourced inputs for the Comps and Precedents sheets ($mm unless noted)."""

COMPS_ASOF = "25-Sep-2026 close"

_SA = "Market data: stockanalysis.com/{t}/statistics (25-Sep-2026). Consensus CY26E/CY27E revenue & EBITDA: MarketScreener /finances/ (accessed 26-Sep-2026)."

# price, shares = basic shares outstanding (mm), debt/cash latest reported quarter; LTM EBITDA is unadjusted (stockanalysis)
COMPS = [
    dict(name="Vertiv", ticker="VRT", price=253.28, shares=384.99, debt=3340, cash=3110, ltm_rev=11480, ltm_ebitda=2680,
         rev26=14019, rev27=18239, ebitda26=3488, ebitda27=4817, src=_SA.format(t="stocks/vrt")),
    dict(name="Eaton", ticker="ETN", price=439.98, shares=388.40, debt=21330, cash=695, ltm_rev=30030, ltm_ebitda=6640,
         rev26=32683, rev27=36626, ebitda26=7754, ebitda27=8991, src=_SA.format(t="stocks/etn")),
    dict(name="GE Vernova", ticker="GEV", price=957.63, shares=266.33, debt=3720, cash=12720, ltm_rev=41370, ltm_ebitda=3930,
         rev26=46282, rev27=52740, ebitda26=6359, ebitda27=9574, src=_SA.format(t="stocks/gev") + " LTM EBITDA is GAAP and depressed."),
    dict(name="Powell Industries (FYE Sep)", ticker="POWL", price=189.53, shares=36.43, debt=2.5, cash=633.6, ltm_rev=1160,
         ltm_ebitda=236.2, rev26=1191, rev27=1483, ebitda26=244.1, ebitda27=315,
         src=_SA.format(t="stocks/powl") + " Fiscal years end September (not calendarized)."),
    dict(name="Hubbell", ticker="HUBB", price=466.62, shares=52.83, debt=5560, cash=394.7, ltm_rev=6220, ltm_ebitda=1520,
         rev26=6871, rev27=7572, ebitda26=1688, ebitda27=1923, src=_SA.format(t="stocks/hubb")),
    dict(name="nVent Electric", ticker="NVT", price=164.41, shares=161.86, debt=1630, cash=256, ltm_rev=4830, ltm_ebitda=1050,
         rev26=5460, rev27=6421, ebitda26=1217, ebitda27=1443, src=_SA.format(t="stocks/nvt")),
    dict(name="Schneider Electric (EUR)", ticker="SU FP", price=291.00, shares=562.33, debt=20810, cash=4520, ltm_rev=42040,
         ltm_ebitda=8520, rev26=44918, rev27=49022, ebitda26=9719, ebitda27=11171, src=_SA.format(t="quote/epa/SU")),
    dict(name="Legrand (EUR)", ticker="LR FP", price=134.85, shares=262.14, debt=7720, cash=1970, ltm_rev=10110, ltm_ebitda=2220,
         rev26=11031, rev27=12193, ebitda26=2622, ebitda27=2939, src=_SA.format(t="quote/epa/LR")),
    dict(name="Hammond Power Solutions (CAD, pro forma AEG)", ticker="HPS.A CN", price=279.22, shares=11.90, debt=505,
         cash=33.63, ltm_rev=1060, ltm_ebitda=None, rev26=1409, rev27=1708, ebitda26=215.5, ebitda27=263,
         src=_SA.format(t="quote/tsx/HPS.A") + " Debt = C$94.75mm reported + ~C$410mm (US$300mm term debt) drawn to fund AEG "
             "Power Solutions (closed 29-Jun-2026), pro forma. LTM EBITDA omitted: GAAP figure distorted by deal costs."),
]

COMPS_NOTES = [
    "Notes: (1) LTM EBITDA is stockanalysis GAAP-basis, not company-adjusted; GE Vernova and Hammond LTM figures are distorted - prefer forward multiples.",
    "(2) Powell's fiscal year ends Sep; others calendar. FPS is calendarized from its June FYE (see cell comments).",
    "(3) Consensus from MarketScreener; the consensus date could not be confirmed on the page. FY26 revenue matched stockanalysis consensus as of 25-Sep-2026.",
    "(4) Excluded: ABB (market data CHF vs. estimates USD), Mitsubishi Electric (conglomerate), Siemens Energy (gas turbines/wind dominate mix).",
    "Sources: stockanalysis.com statistics pages; marketscreener.com /finances/ pages for each ticker; Hammond Q2-2026 release and AEG closing release (globenewswire, 29-Jun and 30-Jul-2026).",
]

# include=1 -> used in summary statistics (core electrical distribution / modular power / grid equipment)
PRECEDENTS = [
    dict(date="Sep-2026", acquirer="Flex", target="EPC Power", include=1,
         desc="Power conversion (rectifiers, DC-DC, SSTs) for data centers and grid", ev=4400, rev=800, ebitda=336,
         basis="Rev 2026E; EBITDA 2027E derived (~40% growth, ~30% margin)",
         src="investors.flex.com release 3-Sep-2026; mgrid.org 3-Sep-2026"),
    dict(date="Sep-2026", acquirer="Vertiv", target="UtilityInnovation Group", include=1,
         desc="Microgrid switchgear and power controls for data centers", ev=1450, rev=None, ebitda=112,
         basis="2027E EBITDA; ~13x stated; excludes up to $1.15bn earnout",
         src="Vertiv 8-K ex-99.1, SEC 0001193125-26-379306"),
    dict(date="Mar-2026", acquirer="Flex", target="Electrical Power Products (EP2)", include=1,
         desc="Engineered control/relay panels, modular control buildings", ev=1100, rev=323, ebitda=None,
         basis="Rev FY Mar-26; EBITDA not disclosed; ~$100mm tax benefit",
         src="prnewswire, Flex to acquire EP2, 30-Mar-2026"),
    dict(date="Oct-2025", acquirer="GE Vernova", target="Prolec GE (remaining 50%)", include=1,
         desc="Power, distribution and specialty transformers (North America)", ev=10550, rev=3000, ebitda=750,
         basis="2025E; 50% stake price ($5.275bn) scaled to 100%; EBITDA derived at ~25% margin",
         src="gevernova.com press release 21-Oct-2025"),
    dict(date="Aug-2025", acquirer="Hubbell", target="DMC Power", include=1,
         desc="Substation and transmission connector systems", ev=825, rev=130, ebitda=60, basis="2026E",
         src="Hubbell 8-K ex-99.1, SEC 0001193125-25-180835"),
    dict(date="Mar-2025", acquirer="Eaton", target="Fibrebond", include=1,
         desc="Pre-integrated modular power enclosures / skids (data centers, utilities)", ev=1400, rev=378, ebitda=110,
         basis="Rev TTM Feb-25; EBITDA 2025E; excl. $240mm assumed retention awards",
         src="Eaton release; Eaton 10-Q Q2-2025"),
    dict(date="Mar-2025", acquirer="nVent", target="Avail Electrical Products Group", include=1,
         desc="Enclosures, switchgear and bus systems for utilities and data centers", ev=975, rev=375, ebitda=78,
         ev_ebitda=12.5, basis="TTM; 12.5x stated", src="nVent release 10-Mar-2025; switchgear-magazine.com"),
    dict(date="Jun-2024", acquirer="nVent", target="Trachte", include=1,
         desc="Custom-engineered control buildings (utility, data center)", ev=695, rev=250, ebitda=58,
         ev_ebitda=12.0, basis="2024E; ~12x 'effective' stated", src="nVent release 6-Jun-2024"),
    dict(date="Oct-2023", acquirer="Hubbell", target="Systems Control", include=1,
         desc="Substation control and relay panels, control buildings", ev=1100, rev=400, ebitda=91.6, basis="2024E; ~12x stated",
         src="Hubbell 8-K ex-99.1, SEC 0001193125-23-266285"),
    dict(date="Apr-2023", acquirer="nVent", target="ECM Industries", include=1,
         desc="Electrical connectors, tools and consumables", ev=1100, rev=415, ebitda=104, ev_ebitda=10.6,
         basis="TTM adj.; ~10.6x 'effective' stated", src="nVent release 3-Apr-2023"),
    dict(date="Sep-2021", acquirer="Vertiv", target="E&I Engineering / Powerbar Gulf", include=1,
         desc="Switchgear, busway, integrated modular power for data centers", ev=1800, rev=460, ebitda=150,
         basis="Rev 2021E; EBITDA 2022E pre-synergy; excl. up to $200mm earnout",
         src="Vertiv 8-K ex-99.1, SEC 0001193125-21-267213"),
    # ---- adjacent: shown for reference, excluded from statistics ----
    dict(date="Nov-2025", acquirer="Eaton", target="Boyd Thermal", include=0,
         desc="Liquid cooling for AI data centers (thermal, not power)", ev=9500, rev=1700, ebitda=422, ev_ebitda=22.5,
         basis="2026E adj.; 22.5x stated. Excluded: thermal", src="Eaton release 3-Nov-2025"),
    dict(date="Nov-2025", acquirer="Vertiv", target="PurgeRite", include=0,
         desc="Fluid-management services for liquid cooling", ev=1000, rev=None, ebitda=None, ev_ebitda=10.0,
         basis="2026E post-synergy, stated. Excluded: services/thermal", src="Vertiv 8-K ex-99.1, SEC 0001193125-25-261623"),
    dict(date="Jul-2024", acquirer="Quanta Services", target="Cupertino Electric", include=0,
         desc="Electrical contractor for data centers (not a manufacturer)", ev=1540, rev=2150, ebitda=165,
         basis="2024E adj. midpoints. Excluded: contractor", src="Quanta release 18-Jul-2024"),
    dict(date="Apr-2024", acquirer="Prysmian", target="Encore Wire", include=0,
         desc="US building wire and cable", ev=4160, rev=None, ebitda=None, ev_ebitda=8.2,
         basis="2023A, 8.2x stated (6.3x post-synergy). Excluded: commodity cable", src="prysmian.com release 15-Apr-2024"),
]

PRECEDENT_NOTES = [
    "Notes: (1) Most acquirers disclose current- or next-year EBITDA, so the multiples are applied to FPS's calendar-2026E EBITDA/revenue "
    "(blend of FY26A and FY27E), not a pure LTM figure. Bases differ deal by deal - see the Basis column.",
    "(2) Deals flagged 0 in 'In stats' (thermal, services, contractor, cable) are shown for context only.",
    "(3) Forgent's own formation deals under Neos Partners (MGM Transformer $424.7mm, Oct-23; VanTran $432.7mm, Jun-24; PwrQ $103.0mm; "
    "States Manufacturing $68.5mm) disclose price only, so no multiples are available (FPS 424B4).",
    "(4) Precedent multiples include a control premium; FPS trades far above them (~21x FY27E EBITDA at market) because its growth is 3-6x the targets'.",
]
