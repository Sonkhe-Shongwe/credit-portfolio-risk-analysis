# Project continuation

**Last updated:** 2026-11-13  
**Repository:** [Sonkhe-Shongwe/credit-portfolio-risk-analysis](https://github.com/Sonkhe-Shongwe/credit-portfolio-risk-analysis)  
**Start here:** Read [the phase scorecard](PROJECT_STATUS.md) for the current percentages and [the blueprint](PROJECT_BLUEPRINT.md) for the finish line. Use this file to resume the work.

## Current checkpoint

| Area | State and evidence |
|---|---|
| Data acquisition | Both Freddie Mac sample ZIPs were provided in the project conversation and processed locally. Use the [official dataset page](https://www.freddiemac.com/research/datasets/sf-loanlevel-dataset) to reacquire them if needed. Download requires Clarity sign-in. |
| Import | [`prepare_freddie_samples.py`](../scripts/prepare_freddie_samples.py) accepts the current `sample_perf_YYYY.txt` and older `sample_svcg_YYYY.txt` member names. Both current archives passed ingestion. The older member name was verified with a synthetic fixture. |
| MySQL data audit | MySQL 8.4.13 loaded 100,000 origination records and 3,718,918 monthly records. The distinct-key counts matched the load counts, with no unmatched loan IDs on either side. Monthly observations ran from January 2022 through June 2026. [`01_load_and_audit.sql`](../sql/01_load_and_audit.sql) |
| Month-12 calculation | The SQL produced eight quarterly cohort rows. The classification totals reconciled to the sampled loan count for each cohort. The local comparison showed lower observed month-12 arrears by both measures in the 2023 sample and more voluntary payoffs. The dashboard should show coverage alongside rates. [`02_month_12_arrears.sql`](../sql/02_month_12_arrears.sql) |
| Power BI input | [`export_power_bi.py`](../scripts/export_power_bi.py) ran both SQL scripts on the official data in MySQL 8.4.13 and generated `local-data/month_12_cohorts.csv`. All eight quarter rows matched the previous SQL output field for field. The [published summary](../power-bi/month_12_cohorts.csv) and embedded model rows were reconciled to that export. |
| Power BI report | Two-page Power BI Project at `power-bi/Credit Portfolio.pbip`. The semantic model embeds the eight aggregate rows and can refresh without a CSV path. The report has a native KPI row, quarterly comparisons and an annual audit table on each page. Static validation passed. Desktop refresh, rendering and filter checks are pending. [Power BI design](POWER_BI.md#report-design) |
| Windows launcher | `Open Credit Portfolio.cmd` opens the project from the existing checkout using a relative path. Power BI Desktop is needed for acceptance. |

## First Windows Desktop evidence

The owner screenshot shows **Arrears comparison** populated with both years in the quarter charts and Year and Quarter set to All. The visible 2022 row matches the baseline (0.4788% accounts in arrears, 0.5173% principal on arrears loans, 229 loans in arrears and 47,824 eligible). The visible total also matches the aggregate baseline (425 loans in arrears, 94,018 eligible and 100,000 sampled). **Cohort coverage** is visible as a tab and has yet to be opened in the supplied evidence. The annual matrix shows a vertical scrollbar and the 2023 row is outside the visible area at the captured view. Record this for the P4.6 layout check. The screenshot does not establish a separate refresh action, Desktop version or exact local commit.

## Resume here

1. **P4.3:** Pull the redesigned report into the existing checkout and reopen it with **Open Credit Portfolio.cmd**. Check that **Arrears comparison** and **Cohort coverage** both load, and record the tested commit, Desktop version and any refresh action.
2. **P4.4 to P4.6:** Reconcile the displayed values, exercise the slicers and inspect the layout. Use the [acceptance checks and expected values](POWER_BI.md#verify-the-report). Record results against their IDs in the [phase scorecard](PROJECT_STATUS.md#p4-power-bi-report-and-windows-acceptance).
3. **P5:** After Windows acceptance, write the findings brief and prepare the GitHub portfolio entry. Use the published aggregate snapshot to verify the claims. See [Power BI setup](POWER_BI.md#reproduce-the-input-from-source) when reproducing or updating the snapshot.

The local quarter comparison showed that both rates were lower in each corresponding 2023 quarter, with a near tie for the account rate in Q1. Q4 had the highest rate on both measures within each year. Show that variation alongside eligibility and payoffs in the report and keep the interpretation descriptive. See the [research plan](RESEARCH_PLAN.md#evidence-and-scope) for the scope of the published summary.

## Checkpoint history

| Date | Work and evidence |
|---|---|
| 2026-11-13 | Built the importer and initial SQL audit. Hand calculations matched the synthetic MySQL run, and the duplicate-key test failed as expected. [Initial implementation](https://github.com/Sonkhe-Shongwe/credit-portfolio-risk-analysis/commit/081cd151c9ac17ea41590dce774a5ce699a09b77) |
| 2026-11-13 | Ran the audit and first calculation on the official 2022 and 2023 archives. Updated the importer for the current monthly filename. [Importer update](https://github.com/Sonkhe-Shongwe/credit-portfolio-risk-analysis/commit/b8e60876c50745ed64512b778982493df574fd18) |
| 2026-11-13 | Documented the research question, analytical method, milestone acceptance checks and next task. |
| 2026-11-13 | Implemented the local CSV exporter, reconciled the eight quarterly rows and both annual rates on the official samples, and documented report setup. |
| 2026-11-13 | Added the Power BI Project, with arrears comparison and cohort coverage pages, a parameterised CSV connection and measures. Static checks passed. Desktop acceptance is next. |
| 2026-11-13 | Added the in-place Windows launcher and documented the automatic CSV connection. The existing GitHub checkout is the working folder. |
| 2026-11-13 | Made report viewing work from a fresh checkout by embedding the verified quarterly research summary and simplifying the Windows launcher. |
| 2026-11-13 | Established the P1 to P5 roadmap, weighted acceptance criteria and v1 blueprint. Baseline is 67% overall and 40% in P4. No new Desktop evidence was supplied. |
| 2026-11-13 | Recorded the first owner screenshot of the populated report on Windows. P4.3 has partial evidence, and the annual matrix needs a visibility check under P4.6. |
| 2026-11-13 | Redesigned both Power BI pages using native visuals and documented the research references. Added KPI cards, a labelled baseline comparison, consistent arrears chart axes and a larger annual matrix. Static validation passed. Desktop acceptance is pending. |
