# Power BI setup

## Open the Power BI project

1. Pull `main` in GitHub Desktop and use **Show in Explorer** to open your existing Credit Portfolio checkout.
2. Double-click **Open Credit Portfolio.cmd**. It opens `power-bi\Credit Portfolio.pbip` in place. You can also open that `.pbip` through **File > Open** in Power BI Desktop. [Microsoft's Power BI Project guide](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
3. If the visuals are empty on first open, select **Home > Refresh** to load the summary already embedded in the semantic model.

The report works from any checkout location. The eight aggregate rows are also available as [`power-bi/month_12_cohorts.csv`](../power-bi/month_12_cohorts.csv) for inspection. The model embeds the same rows so Power BI can load them without a machine-specific connection.

## Reproduce the input from source

Prepare `local-data/origination.tsv` and `local-data/performance.tsv` using the [README](../README.md#run-the-first-audit). With the MySQL client available, run the following command from the repository root. The `--` separates exporter arguments from MySQL client arguments.

```sh
python scripts/export_power_bi.py -- --user=YOUR_USERNAME -p credit_portfolio
```

The exporter runs the two SQL scripts in one session and writes `local-data/month_12_cohorts.csv`. When updating the report to a new verified snapshot, update both the checked-in CSV and the `Source = #table(...)` rows in the model's `Cohorts.tmdl`, and reconcile the two before committing. Each row is one origination year and quarter.

Power Query loads the fields below using `en-US` number formats. Counts use whole numbers and principal uses fixed decimal USD amounts. The report includes Year and Quarter dropdowns on both pages.

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

1. **P4.3:** Use the launcher from the existing Windows checkout. Refresh if the visuals are empty and check that **Arrears comparison** and **Cohort coverage** both load. Record the commit, Desktop version and refresh outcome.
2. **P4.4:** Clear both filters. On **Arrears comparison**, reconcile the annual counts, rates and USD exposure. On **Cohort coverage**, reconcile the eligible loans and exclusions to the sample. Confirm the quarter charts show Q1 to Q4 and both year series.
3. **P4.5:** Select **2023** and **Q4** on each page, compare the values to the row below, then clear both filters and confirm the annual values return. Totals use the underlying counts and balances.
4. **P4.6:** Inspect both pages at Fit to Page. Record any clipped labels, illegible legends, ambiguous titles or missing units, and capture both accepted views for the portfolio handoff. Record results in [the phase scorecard](PROJECT_STATUS.md#p4-power-bi-report-and-windows-acceptance) and [continuation document](CONTINUATION.md). See the [publication notes](RESEARCH_PLAN.md#evidence-and-scope) before sharing screenshots.

The export has been reconciled to MySQL, and the checked-in report definition has passed static validation. The refresh, visual rendering and filter checks require Power BI Desktop.

### Expected values for Desktop acceptance

These values are calculated from the checked-in eight-row summary. Compare percentages at the report's displayed precision.

| Selection | Sampled loans | Eligible loans | Loans 90+ days in arrears | Account rate | Principal rate | Principal on arrears loans (USD) | Voluntary payoffs | Eligibility rate | Voluntary payoff rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022, all quarters | 50,000 | 47,824 | 229 | 0.4788% | 0.5173% | $71,906,651.11 | 1,998 | 95.6480% | 3.9960% |
| 2023, all quarters | 50,000 | 46,194 | 196 | 0.4243% | 0.4167% | $57,522,660.23 | 3,642 | 92.3880% | 7.2840% |
| 2023 Q4 | 12,500 | 10,759 | 63 | 0.5856% | 0.5626% | $17,477,672.96 | 1,698 | 86.0720% | 13.5840% |

For the 2023 Q4 coverage check, the remaining 43 loans consist of 42 other exits and one real-estate-owned (REO) acquisition.
