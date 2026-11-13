# Portfolio v1 blueprint

## What the finished project does

A reviewer opens the report from the GitHub checkout and compares serious arrears for the 2022 and 2023 Freddie Mac mortgage samples in their 12th scheduled payment month. They can see which origination quarters warrant closer review, how much outstanding principal is on the affected accounts, and how much of each cohort paid off or otherwise fell outside the comparison.

**Audience:** A credit portfolio monitoring team and a portfolio reviewer assessing credit analytics, SQL and Power BI skills. **Decision:** Which quarters should the analyst investigate further, and what should they verify before attributing the observed difference to underwriting, borrower mix, servicing or market conditions?

## What a reviewer will receive

| Deliverable | Final contents |
|---|---|
| **Two-page Power BI report** | **Arrears comparison** presents the annual account and principal rates with eligible counts, then compares the quarters. **Cohort coverage** presents the sample, eligible population, voluntary payoffs and other exclusions. Both pages support Year and Quarter filters. |
| **Verified data and calculations** | Eight quarterly aggregate rows, the embedded Power BI model, the documented measures and the reproducible Python and MySQL workflow that produced the aggregates. The original source archives and row-level extracts stay local. |
| **Findings brief** | One short, evidence-led account of the year and quarter patterns, the eligibility and payoff context, the scope of the data, and the follow-up analysis the findings justify. |
| **GitHub portfolio entry** | A README with the project question, open instructions, accepted visuals and findings, plus source references, the phase scorecard and a current handoff. |

## How to use the project

1. **View the report.** Pull the repo, run **Open Credit Portfolio.cmd**, and refresh in Power BI Desktop if needed. The eight summary rows are embedded. [Power BI setup](POWER_BI.md#open-the-power-bi-project)
2. **Inspect the findings.** Read the annual summary and filter a quarter. Use the coverage page to see how the eligible population was formed. Then read the findings brief and compare its claims with the report.
3. **Reproduce the analysis when needed.** Acquire the official samples, prepare them with Python, run the SQL audit and comparison, then reconcile the export. [Source and run instructions](../README.md#run-the-first-audit)

## Research scope

The first release describes the observed month-12 snapshot for the sampled US mortgages. The data supports an account-based arrears rate, a balance-weighted arrears rate and a comparison of coverage. It does not establish causes, actual lending growth, cumulative delinquency, realised losses or results for a South African credit book. Forecasting, later repayment ages and additional borrower segments are possible follow-ups. [Definitions and limitations](RESEARCH_PLAN.md#method-and-measures)

## Release criteria

Portfolio v1 is complete when every required item in the [phase scorecard](PROJECT_STATUS.md) is verified. The GitHub handoff will identify the accepted commit, the checks that passed in Power BI Desktop, and the final report and findings entry points.
