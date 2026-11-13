# Project continuation

**Last updated:** 2026-11-13  
**Repository:** [Sonkhe-Shongwe/credit-portfolio-risk-analysis](https://github.com/Sonkhe-Shongwe/credit-portfolio-risk-analysis)  
**Start here:** Read this file, then [the research plan](RESEARCH_PLAN.md) and the [README run instructions](../README.md#run-the-first-audit).

## Current checkpoint

| Area | State and evidence |
|---|---|
| Data acquisition | Both Freddie Mac sample ZIPs were provided in the project conversation and processed locally. Use the [official dataset page](https://www.freddiemac.com/research/datasets/sf-loanlevel-dataset) to reacquire them if needed. Download requires Clarity sign-in. |
| Import | [`prepare_freddie_samples.py`](../scripts/prepare_freddie_samples.py) accepts the current `sample_perf_YYYY.txt` and older `sample_svcg_YYYY.txt` member names. Both current archives passed ingestion. The older member name was verified with a synthetic fixture. |
| MySQL data audit | MySQL 8.4.13 loaded 100,000 origination records and 3,718,918 monthly records. The distinct-key counts matched the load counts, with no unmatched loan IDs on either side. Monthly observations ran from January 2022 through June 2026. [`01_load_and_audit.sql`](../sql/01_load_and_audit.sql) |
| Month-12 calculation | The SQL produced eight quarterly cohort rows. The classification totals reconciled to the sampled loan count for each cohort. The local comparison showed lower observed month-12 arrears by both measures in the 2023 sample and more voluntary payoffs. The dashboard should show coverage alongside rates. [`02_month_12_arrears.sql`](../sql/02_month_12_arrears.sql) |
| Power BI | Pending. The SQL outputs the comparison, but a standalone BI-ready export and report measures still need to be built and verified. |

## Resume here

1. Verify the current default branch and compare it with this checkpoint. If the prepared TSVs are available locally, use them to rerun the audit and calculation. Otherwise, use the attached sample ZIPs if available in the project workspace, or reacquire them using the README. The pipeline runs in a single MySQL session because the tables are temporary.
2. Add a reproducible local export with one row per origination year and quarter. Export the base counts and principal amounts needed for both ratios, plus all exclusion counts. Verify eight unique cohort keys for the current archives and reconcile each cohort's eligibility categories to its sample count.
3. Use the export to build the Power BI measures and report. Recalculate year totals from the underlying counts and balances, and validate those results against SQL. Show voluntary payoffs and eligibility alongside arrears. Use USD for amounts.

The open analytical question is whether the year-level difference appears across most quarters or is concentrated in particular cohorts. Check that before writing the findings brief. The source terms still need to be applied to any specific public report or data-bearing artifact. See the [research plan](RESEARCH_PLAN.md#evidence-and-scope).

## Checkpoint history

| Date | Work and evidence |
|---|---|
| 2026-11-13 | Built the importer and initial SQL audit. Hand calculations matched the synthetic MySQL run, and the duplicate-key test failed as expected. [Initial implementation](https://github.com/Sonkhe-Shongwe/credit-portfolio-risk-analysis/commit/081cd151c9ac17ea41590dce774a5ce699a09b77) |
| 2026-11-13 | Ran the audit and first calculation on the official 2022 and 2023 archives. Updated the importer for the current monthly filename. [Importer update](https://github.com/Sonkhe-Shongwe/credit-portfolio-risk-analysis/commit/b8e60876c50745ed64512b778982493df574fd18) |
| 2026-11-13 | Documented the research question, analytical method, milestone acceptance checks and next task. |
