# Power BI setup

## Generate the input

Prepare `local-data/origination.tsv` and `local-data/performance.tsv` using the [README](../README.md#run-the-first-audit). With the MySQL client available, run the following command from the repository root. The `--` separates exporter arguments from MySQL client arguments.

```sh
python scripts/export_power_bi.py -- --user=YOUR_USERNAME -p credit_portfolio
```

The exporter runs the two SQL scripts in one session, prints the audit results and writes `local-data/month_12_cohorts.csv`. Each row is one origination year and quarter. The file includes the base counts and balances used in the report. The directory is ignored by Git.

## Open the Power BI project

1. Pull `main` in GitHub Desktop. From the repository root, make a local working copy of the complete `power-bi` folder under `local-data` so your Windows path and any cached data stay local. For a first-time setup in PowerShell, after generating the CSV, run `Copy-Item -Recurse .\power-bi .\local-data\power-bi`.
2. Open `local-data\power-bi\Credit Portfolio.pbip` in a current version of Power BI Desktop. If the project format is unavailable, enable **Power BI Project (.pbip) save option** under **File > Options and settings > Options > Preview features** and restart Desktop. [Microsoft's Power BI Project guide](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
3. Choose **Transform data > Edit parameters**. Set `CohortCsvPath` to the full Windows path of `local-data\month_12_cohorts.csv`, then apply the change and refresh. A blank path opens the report with empty visuals. The local copy contains both report and model folders and needs both to open.

Power Query loads the fields below using the CSV's `en-US` number format. Counts use whole numbers and principal uses fixed decimal USD amounts. The report includes Year and Quarter dropdowns on both pages.

| Columns | Meaning |
|---|---|
| `origination_year`, `origination_quarter` | Unique cohort key |
| `sampled_loans`, `eligible_loans` | Starting sample and eligible month-12 accounts |
| `loans_in_90_plus_arrears` | Eligible accounts 90 or more days in arrears |
| `eligible_principal`, `principal_in_90_plus_arrears` | Outstanding principal in USD for the eligible population and its 90+ day subset |
| `voluntary_payoff_by_month_12`, `other_exits_by_month_12`, `month_12_unobserved`, `real_estate_owned`, `no_positive_principal`, `unknown_delinquency` | Mutually exclusive reasons a sampled loan falls outside the eligible population |

The model defines the following percentage measures. `DIVIDE` returns blank for a zero denominator.

```dax
Accounts in arrears % =
DIVIDE(SUM(Cohorts[loans_in_90_plus_arrears]), SUM(Cohorts[eligible_loans]))

Principal on arrears loans % =
DIVIDE(SUM(Cohorts[principal_in_90_plus_arrears]), SUM(Cohorts[eligible_principal]))

Month-12 eligibility % =
DIVIDE(SUM(Cohorts[eligible_loans]), SUM(Cohorts[sampled_loans]))

Voluntary payoff % =
DIVIDE(SUM(Cohorts[voluntary_payoff_by_month_12]), SUM(Cohorts[sampled_loans]))
```

## Verify the report

1. On **Arrears comparison**, check that the matrix shows both years, both arrears rates, counts and USD exposure. Confirm the two quarter charts each show Q1 to Q4 and the expected year series.
2. On **Cohort coverage**, check that each matrix row adds back to the sampled count when eligible loans and all exclusion categories are summed. Confirm that voluntary payoff and eligibility appear for each quarter.
3. Compare each year and quarter against the local output of `sql/02_month_12_arrears.sql`. Test both dropdowns, clear them, and check the totals. Totals must recalculate from the underlying counts and balances.
4. Check both pages at Fit to Page and record the Desktop version, refresh outcome and any render or filter issues in [the continuation document](CONTINUATION.md). Use the [publication notes](RESEARCH_PLAN.md#evidence-and-scope) before sharing a data-bearing report.

The export has been reconciled to MySQL, and the checked-in report definition has passed static validation. The refresh, visual rendering and filter checks require Power BI Desktop.
