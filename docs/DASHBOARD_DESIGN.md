# Credit Portfolio dashboard design specification

**Design proposal · 13 November 2026**  
**Source reviewed:** [Power BI report at `9afbfa7`](https://github.com/Sonkhe-Shongwe/credit-portfolio-risk-analysis/tree/9afbfa7761378f0ae96dafd03fcbbe48647cc03b/power-bi)  
**Audience:** Credit portfolio monitoring team and GitHub portfolio reviewers.

The report should let a reviewer see the month-12 arrears position, identify a quarter worth investigating, and verify how many loans qualified for the comparison. The desktop composition should read clearly at Fit to Page and in a GitHub screenshot. The design uses a compact navy header, a light canvas, an aligned KPI row and a large evidence area. The two pages share a navigation and filter layout.

## Reference review

| Reference and access | What to study | Adaptation for this report |
|---|---|---|
| [Numerro Finance](https://www.numerro.io/use-cases/power-bi-finance-template) · public light and dark screenshots | Reusable KPI, chart and table treatments across a finance report. | Use the light composition as the visual starting point. Repeat spacing, typography and panel treatment across both pages. |
| [Briqlab Banking Loan Portfolio](https://www.briqlab.io/power-bi/templates/banking-loan-portfolio-power-bi-dashboard) · public previews and sign-in for the advertised PBIX | The top row gives a compact view of the key loan metrics and puts filters near the analysis. | Borrow the banking layout. Omit the geographic and disbursement visuals because the published summary has eight quarter cohorts. |
| [ZoomCharts Credit Risk Analysis](https://zoomcharts.com/en/microsoft-power-bi-custom-visuals/dashboard-and-report-examples/view/credit-risk-analysis-dashboard) · public preview and account-gated PBIX | Credit-risk overview and a route into more detailed analysis. | Keep that progression with two native Power BI report pages and a single path from arrears to coverage. |
| [Omar Rezk, Bank Loan Portfolio Analysis](https://omarrez2.github.io/projects/bank-loan-analysis) · public screenshot and repository link | A portfolio case study connects the landing view, decision brief and detailed evidence. | Give our opening screenshot the headline metrics and enough supporting evidence to stand alone in the README. |
| [CFPB, Mortgages 90 or more days delinquent](https://www.consumerfinance.gov/data-research/mortgage-performance-trends/mortgages-90-or-more-days-delinquent/) · public interactive charts | Precise delinquency wording, visible scope, explicit comparison and source attribution. | Show the 90-day threshold, observation age and sample source near the numbers. The CFPB figures use a different population and time basis, so the report uses its own cohort comparison. |
| [Microsoft Corporate Spend sample](https://learn.microsoft.com/en-us/power-bi/create-reports/sample-corporate-spend) · downloadable sample PBIX | An editable reference for inspecting Power BI interactions, page transitions and matrix settings in Desktop. | Inspect native behavior before building. Use the sample for mechanics and apply the credit report's own visual system. |

Microsoft's [dashboard design guidance](https://learn.microsoft.com/en-us/power-bi/create-reports/service-dashboards-design-tips) supports the top-left priority, context for cards and consistent scales. [Nielsen Norman Group](https://www.nngroup.com/articles/principles-visual-design/) explains how relative size and contrast establish hierarchy. [IBCS](https://www.ibcs.com/ibcs-version-2-0/) informs consistent notation and comparisons. The [Financial Times Visual Vocabulary](https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary) helps select visuals by the analytical question. The proposed dimensions, palette and component choices below are project decisions.

## Current report review

The two 1280 × 768 report pages already have a shared theme, native visuals, a four-card row, a full-sample comparison, two quarter charts and an annual matrix. The arrears charts already use the same 0% to 0.8% scale. The redesign should improve how those elements relate on the page.

- The 118 px navy block contains title, subtitle and both filters. Use a shallower title area and place navigation and filters together on the next row so controls are visibly distinct from the report title.
- Four 294 × 111 px cards have equal footprints. Give the primary measure more typographic weight and a quiet surface tint, and put its numerator and denominator underneath it. Treat the other three cards as context.
- The fixed comparison currently reads as a broad strip between the KPIs and charts. Use one short baseline insight per page with a clear scope label. Keep the selection state alongside the controls.
- The current matrices occupy the bottom 171 px. Give rows a dedicated fit check so the annual totals can be seen at a glance. The original owner screenshot clipped the 2023 row. The most recent redesign still needs Windows rendering evidence.

## Canvas and hierarchy

Use a 1280 × 768 starting canvas, 24 px outer gutters, 16 px column gaps, 12–16 px panel padding and 8 px corner radii where Power BI supports them. Measure layout against the displayed report at Fit to Page. These positions are starting allocations for implementation.

| Region | Vertical allocation | Design |
|---|---:|---|
| Title | 0–80 px | Navy header with report title and one line of scope, such as “Freddie Mac U.S. mortgage samples · 12th scheduled payment month”. |
| Controls | 92–140 px | Two labelled page tabs on the left. Year, Quarter and Clear filters on the right. Indicate the selected tab with an underline and weight. |
| KPI row | 156–268 px | Four 296 px cards with aligned labels, values and context. The leftmost card carries the primary measure. |
| Baseline | 284–332 px | Short text on a quiet surface. Prefix with “Full sample” so its scope stays clear after filtering. |
| Quarterly evidence | 348–580 px | Two aligned chart areas. On Arrears comparison, use equal widths and a common scale. On Cohort coverage, give the payoff chart more width for the focal Q4 comparison. |
| Reconciliation | 596–732 px | One full-width matrix with visible headers, annual rows and total. Right-align amounts and counts. |
| Source line | 744–764 px | Freddie Mac source, month-12 basis and USD where relevant. |

Use Segoe UI throughout for the first Power BI pass. Start with 24–26 pt for the title, 28–32 pt for the primary value, 23–26 pt for supporting values, 13–15 pt for chart titles and 10–12 pt for labels, axes and reference text. Verify at Fit to Page and adjust the layout if labels shrink or truncate. Use sentence case and consistent decimal alignment in tables.

## Colour, icons and shapes

| Role | Value | Use |
|---|---|---|
| Page and surfaces | `#F3F6FA` canvas, `#FFFFFF` surfaces | Separate the report background from its data regions. |
| Ink and header | `#10243A` | Main text, numbers and navy header. Use white text on the header. |
| Secondary text | `#52647A` | Context, secondary labels and axis text. |
| Cohort series | `#254B86` for 2022, `#00766D` for 2023 | Keep series order, labelled legends and grouped-bar positions stable on both pages. Both colours represent identity. |
| Primary KPI background | `#E9F5F2` | One quiet fill. Keep the value dark. |
| Structural rules | `#D9E2EC` | Gridlines and surface separators. A control boundary that needs to be visible against white can use `#8293A9`. |
| Status | `#91541A` on `#FFF6E8` for review, `#9F3434` on `#FFF2F2` for an actual alert | Use only for a defined status with text, such as “Review”. This snapshot has no breach threshold. |

The proposed text pairs meet the WCAG normal-text target of 4.5:1 in calculation. For example, dark ink on white is 15.72:1, secondary text on the canvas is 5.60:1, and white on navy is 15.72:1. Essential graphical or control boundaries should reach 3:1 where applicable. Recheck the final report after formatting. Supply explicit series labels and a tabular alternative, and use selection text or shape as well as colour for states. [W3C text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) · [Non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) · [Use of colour](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html).

Use one outline icon style at about 16 px, paired with the action name, for actions such as clearing filters and opening definitions if those actions need icons. A chevron communicates a dropdown, a small swatch identifies a cohort and a selected-tab underline communicates location. The card shape groups a label, value and denominator. A delta can include a signed value and explicit comparison period. Skip illustrations, emojis, oversized circular icon backgrounds, ornamental gradients, heavy shadows and coloured borders around every KPI. [Carbon icon guidance](https://www.carbondesignsystem.com/building-blocks/foundations/icons/guidelines) · [Carbon chart palettes](https://www.carbondesignsystem.com/building-blocks/data-visualization/color-palettes).

## Page content

### Arrears comparison

- **KPI order:** Accounts 90+ days in arrears → Principal on arrears loans, share → Loans 90+ days in arrears → Principal on arrears loans, USD. At the full-sample default the four display values are `0.452%`, `0.467%`, `425` and `USD 129.43m`. The account rate reads “425 of 94,018 eligible loans”. The principal rate uses outstanding principal on the affected loans divided by all eligible outstanding principal.
- **Baseline callout:** “Full sample · 2023 account arrears fell 5.45 bps vs 2022. Q4 had the highest account arrears rate in both cohorts.” A basis point is 0.01 percentage points. Use cohort-specific copy if the product later switches to a dynamic callout, and test its behavior under both filters.
- **Charts:** Two clustered column charts, accounts on the left and principal share on the right. Keep Q1–Q4 in order and use 0.0% to 0.8% on both axes. Each bar is an origination quarter measured at the same repayment age. Put exact rates, numerator and denominator in the tooltip and matrix. The annual matrix shows 2022, 2023 and total in the unfiltered view.

### Cohort coverage

- **KPI order:** Month-12 eligibility → Voluntary payoff rate → Eligible loans → Sampled loans. At the full-sample default the values are `94.02%`, `5.64%`, `94,018` and `100,000`. Pair the rate cards with `94,018 of 100,000 sampled loans` and `5,640 of 100,000 sampled loans` respectively.
- **Baseline callout:** “Full sample · Voluntary payoff reached 13.58% in 2023 Q4, compared with 5.52% in 2022 Q4.”
- **Charts:** Payoff share on the left and eligibility on the right. Show the same quarters and year encoding as on the arrears page. Both start at zero. Label their independent scales clearly, initially 0–16% for payoffs and 0–100% for eligibility. Show exact counts and rates in tooltips. Keep the eligibility and all six mutually exclusive exclusion categories in the annual matrix, including true zero counts.

Use three decimal places for headline arrears rates, two for coverage rates, whole numbers for counts, and USD millions for exposure cards. Use four decimals for exact rates in the matrix and tooltips, and full USD to cents where the underlying balance is shown for reconciliation. Aggregate as sums of numerators divided by sums of denominators. Display a blank or `N/A` for a missing denominator. Use a visible empty-state message if the filters yield no rows.

## Interactions and Power BI build

1. Use native Page Navigator or page navigation buttons, slicers, a Clear all slicers button, cards with reference labels, clustered columns and matrices. Use the report theme JSON for shared formatting and explicit overrides for chart scales, series mappings and card roles.
2. Keep Year and Quarter visible at the same location on both pages. Sync their selection across pages so a user moving from 2023 Q4 arrears to coverage keeps the same slice. Verify that Clear filters restores the full-sample selection and the expected matrices on both pages.
3. Filter cards, charts and matrices through the two slicers. Keep the labelled baseline callout fixed. Disable chart-driven cross-filtering in the first implementation so the report's scope always matches the visible slicer state. Verify that keyboard navigation goes from page controls to KPIs, charts, then matrix. Supply alt text and remove purely decorative shapes from tab order.
4. Use the repo's [Power BI setup](POWER_BI.md) to preserve its embedded summary and pull-and-open workflow. Check the native implementation against Microsoft's [cards](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-card), [navigators](https://learn.microsoft.com/en-us/power-bi/create-reports/button-navigators), [slicers](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicers), [clear filters](https://learn.microsoft.com/en-us/power-bi/create-reports/buttons-apply-all-clear-all-slicers), [themes](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-report-themes) and [accessibility guidance](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports).

## Acceptance evidence

| Existing check | Design acceptance evidence |
|---|---|
| P4.3 | Record commit, Desktop version and refresh outcome. Open both pages through the existing launcher. |
| P4.4 | Reconcile both annual rates, counts and USD exposure, and both annual coverage rows. Confirm combined rates use weighted denominators. |
| P4.5 | Select 2023 and Q4 on Arrears comparison. Verify account arrears `0.5856%` (63 of 10,759) and principal arrears `0.5626%`. Open Cohort coverage, verify `86.0720%` eligibility and `13.5840%` payoff share, then clear filters and confirm the default on both pages. |
| P4.6 | Capture both pages at Fit to Page. Both annual rows and totals fit without scrolling, primary numbers lead the reading order, controls show selection and focus, text and marks retain contrast, and charts and matrices stay legible without tooltips. |

This specification is a research and design deliverable. The phase scorecard records the Power BI Desktop acceptance evidence once each check passes.
