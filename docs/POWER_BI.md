# Power BI setup

## Generate the input

Prepare `local-data/origination.tsv` and `local-data/performance.tsv` using the [README](../README.md#run-the-first-audit). With the MySQL client available, run the following command from the repository root. The `--` separates exporter arguments from MySQL client arguments.

```sh
python scripts/export_power_bi.py -- --user=YOUR_USERNAME -p credit_portfolio
```

The exporter runs the two SQL scripts in one session, prints the audit results and writes `local-data/month_12_cohorts.csv`. Each row is one origination year and quarter. The file includes the base counts and balances used in the report. The directory is ignored by Git.

## Import and define the measures

In Power BI Desktop, use **Get data > Text/CSV**, choose the exported CSV, and name the table `Cohorts`. In Power Query, use **Whole Number** for the year, quarter and count columns and **Fixed Decimal Number** for the two principal columns. The CSV uses a decimal point and USD. Use an English (United States) locale for the principal columns if needed.

| Columns | Meaning |
|---|---|
| `origination_year`, `origination_quarter` | Unique cohort key |
| `sampled_loans`, `eligible_loans` | Starting sample and eligible month-12 accounts |
| `loans_in_90_plus_arrears` | Eligible accounts 90 or more days in arrears |
| `eligible_principal`, `principal_in_90_plus_arrears` | Outstanding principal in USD for the eligible population and its 90+ day subset |
| `voluntary_payoff_by_month_12`, `other_exits_by_month_12`, `month_12_unobserved`, `real_estate_owned`, `no_positive_principal`, `unknown_delinquency` | Mutually exclusive reasons a sampled loan falls outside the eligible population |

Create each formula as a separate measure and format it as a percentage. `DIVIDE` returns blank for a zero denominator.

```dax
Accounts 90+ Days in Arrears % =
DIVIDE(SUM(Cohorts[loans_in_90_plus_arrears]), SUM(Cohorts[eligible_loans]))

Principal on 90+ Day Accounts % =
DIVIDE(SUM(Cohorts[principal_in_90_plus_arrears]), SUM(Cohorts[eligible_principal]))

Month-12 Eligibility % =
DIVIDE(SUM(Cohorts[eligible_loans]), SUM(Cohorts[sampled_loans]))

Voluntary Payoff by Month 12 % =
DIVIDE(SUM(Cohorts[voluntary_payoff_by_month_12]), SUM(Cohorts[sampled_loans]))
```

## Build and verify the report

1. Build a year comparison for the two arrears rates. Place the eligible and sampled counts next to the rates. Add a quarter comparison to show how the year-level result varies across origination quarters.
2. Build a coverage view for eligibility, voluntary payoff and the other exclusions. Include counts so a reader can reconcile each cohort back to its original sample.
3. Compare each year and quarter against `sql/02_month_12_arrears.sql`. Test the year and quarter filters. Verify that totals recalculate from the underlying counts and balances and that principal amounts display as USD.

The export has been reconciled to MySQL. These measures and report instructions still need verification in Power BI Desktop.
