# Project status and phase scorecard

**Baseline:** 13 November 2026  
**Portfolio v1 completion:** **67%**  
**Active phase:** **P4 Power BI report and Windows acceptance**, **40%**  
**Next action:** Pull the redesigned report, reopen it in Power BI Desktop and check that both pages display. [Resume here](CONTINUATION.md#resume-here)

| Phase | Project weight | Phase completion | Points earned | What remains |
|---|---:|---:|---:|---|
| P1. Business question and research design | 10% | **100%** | 10.0 | Baseline verified |
| P2. Source acquisition and data quality | 20% | **100%** | 20.0 | Baseline verified |
| P3. SQL analysis and Power BI input | 25% | **100%** | 25.0 | Baseline verified |
| P4. Power BI report and Windows acceptance | 30% | **40%** | 12.0 | Open and refresh on Windows, reconcile displayed values, exercise filters, and inspect both pages |
| P5. Findings and portfolio handoff | 15% | **0%** | 0.0 | Findings brief, report evidence, reviewer walkthrough and v1 checkpoint |
| **Portfolio v1** | **100%** | | **67.0** | |

## How the percentages work

Each phase has a checklist of weighted acceptance criteria. An item earns its points when its stated evidence is recorded. Break a partially complete item into explicit subchecks if finer tracking is needed. The overall percentage is the sum of each phase's project weight multiplied by its verified completion. At this baseline that is `10 + 20 + 25 + (30 × 0.40) + (15 × 0) = 67`.

The weights are a planning baseline for this portfolio project. They measure verified completion against the scope below. Use **Verified**, **Pending**, **Blocked**, or **Failed** for individual checks. Record evidence for the relevant commit, environment and inputs. Keep earlier failures in the checkpoint history and record the result of any retest. Update the scorecard and [continuation document](CONTINUATION.md) together when acceptance evidence or scope changes. Record the reason for any change to the weights or scope.

## P1. Business question and research design

| ID | Points | Acceptance criterion | Status and evidence |
|---|---:|---|---|
| P1.1 | 30 | State the business question, audience and decision the report supports | Verified. [Business question](RESEARCH_PLAN.md#business-question) |
| P1.2 | 40 | Define the years, source, loan and cohort grain, month-12 convention, eligibility and measures | Verified. [Research method](RESEARCH_PLAN.md#method-and-measures) |
| P1.3 | 30 | Record limitations and define the intended portfolio deliverables | Verified. [Research plan](RESEARCH_PLAN.md) and [v1 blueprint](PROJECT_BLUEPRINT.md) |

## P2. Source acquisition and data quality

| ID | Points | Acceptance criterion | Status and evidence |
|---|---:|---|---|
| P2.1 | 25 | Obtain both official annual samples and document source, file layout and data handling | Verified. [Source and run instructions](../README.md#run-the-first-audit) |
| P2.2 | 25 | Import the supplied archive format and confirm that the older monthly member name still works | Verified. Both official archives and a legacy-name fixture processed. [Importer update](https://github.com/Sonkhe-Shongwe/credit-portfolio-risk-analysis/commit/b8e60876c50745ed64512b778982493df574fd18) |
| P2.3 | 50 | Reconcile extraction and load counts, verify unique keys, and check match coverage | Verified. MySQL 8.4.13 loaded 100,000 loans and 3,718,918 monthly rows with zero duplicate keys and zero unmatched loans. [Audit checkpoint](CONTINUATION.md#current-checkpoint) |

## P3. SQL analysis and Power BI input

| ID | Points | Acceptance criterion | Status and evidence |
|---|---:|---|---|
| P3.1 | 35 | Implement month-12 cohort classification and both arrears rates with reproducible SQL | Verified. Hand-checked fixture and duplicate-key rejection recorded. [Analysis SQL](../sql/02_month_12_arrears.sql) · [Initial implementation](https://github.com/Sonkhe-Shongwe/credit-portfolio-risk-analysis/commit/081cd151c9ac17ea41590dce774a5ce699a09b77) |
| P3.2 | 35 | Reconcile the eight quarterly cohorts and the annual ratios from the real sample export | Verified. Every sampled loan reconciled to eligibility or an exclusion. [Export checkpoint](https://github.com/Sonkhe-Shongwe/credit-portfolio-risk-analysis/commit/fffebad1e57d3617a3d6f205ab6d4b319859ad78) |
| P3.3 | 30 | Reconcile the checked-in summary and model input to the verified export. Document field meanings and source boundaries | Verified. The eight embedded rows match the aggregate CSV and MySQL export. [Published summary](../power-bi/month_12_cohorts.csv) · [Input setup](POWER_BI.md#reproduce-the-input-from-source) |

## P4. Power BI report and Windows acceptance

| ID | Points | Acceptance criterion | Status and evidence |
|---|---:|---|---|
| P4.1 | 25 | Build both report pages, model measures and slicers, with the report available directly from the checkout | Verified at source level. [Power BI project](../power-bi) · [Pull-and-open change](https://github.com/Sonkhe-Shongwe/credit-portfolio-risk-analysis/commit/dbe072cf81664bd92e2ccdecf81c2caee26c8263) |
| P4.2 | 15 | Verify schemas, visual and model bindings, and measure definitions against the known data | Verified by static validation of the redesigned source and reconciliation of the existing measures against the same aggregate input. [Report checkpoint](CONTINUATION.md#current-checkpoint) |
| P4.3 | 20 | Open the project from the existing Windows checkout, load the embedded data, and confirm both pages open | Pending with partial evidence. The original populated Arrears comparison page opened in Windows. Both redesigned pages, the tested commit, Desktop version and refresh outcome remain to be recorded. [First Windows evidence](CONTINUATION.md#first-windows-desktop-evidence) |
| P4.4 | 15 | Reconcile both displayed annual arrears rates, loan counts and coverage totals to the MySQL baseline | Pending with partial evidence. The visible 2022 row and selected totals match the baseline. The 2023 row and coverage totals still need checking. [Expected values](POWER_BI.md#expected-values-for-desktop-acceptance) |
| P4.5 | 15 | Exercise Year and Quarter on both pages, verify the 2023 Q4 result, and clear the filters to restore totals | Pending. [Expected values](POWER_BI.md#expected-values-for-desktop-acceptance) |
| P4.6 | 10 | Inspect both pages at Fit to Page for readable labels, titles, legends and units, and retest any corrected issues | Pending. The first screenshot showed the 2023 row outside the visible area. The redesigned matrix has dedicated room for both years and the total. Verify this and inspect both pages at Fit to Page before capturing the accepted views for P5. |

**P4 reaches 100%** when P4.3 through P4.6 pass in Power BI Desktop and the results are recorded. The next session starts with P4.3 only.

## P5. Findings and portfolio handoff

| ID | Points | Acceptance criterion | Status |
|---|---:|---|---|
| P5.1 | 35 | Write a short findings brief with the annual comparison, quarter-level evidence, payoff context, limitations and an actionable follow-up | Pending |
| P5.2 | 25 | Link the accepted report views and findings from the GitHub README, with source attribution and publication scope | Pending |
| P5.3 | 25 | Walk through the project from a fresh checkout, confirming the viewer can open the report and the optional reproduction steps are clear | Pending |
| P5.4 | 15 | Record the accepted v1 commit, completion evidence and any follow-up ideas in the handoff | Pending |
