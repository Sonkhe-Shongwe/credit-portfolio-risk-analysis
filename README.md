# Credit Portfolio Performance & Risk Analysis

A MySQL and Power BI case study on the early credit performance of US mortgages. It compares the 2022 and 2023 Freddie Mac origination cohorts in their 12th scheduled payment month. The analysis tracks the share of loans 90 or more days in arrears, the share of outstanding principal on those loans, and how many loans paid off or otherwise exited before the comparison.

**Status:** Both sample archives passed the MySQL audit and produced the first month-12 comparison. The next milestone is to build and reconcile the Power BI input.

- [Research plan](docs/RESEARCH_PLAN.md) for the business question, sources, definitions and milestone acceptance checks.
- [Project continuation](docs/CONTINUATION.md) for the latest verified checkpoint, open decisions and exact next task.

## Run the first audit

1. Open the [Freddie Mac dataset page](https://www.freddiemac.com/research/datasets/sf-loanlevel-dataset), follow **Access Historical Data**, and sign in to Clarity. In the sample downloads, select `sample_2022.zip` and `sample_2023.zip`. These are the initial comparison years. The [release notes](https://www.freddiemac.com/fmac-resources/research/pdf/release_notes.pdf) document the reporting cutoff.
2. Put both archives in `local-data/` at the repository root. Keep the source and row-level outputs local. Freddie Mac's [dataset terms](https://capitalmarkets.freddiemac.com/crt/docs/pdfs/fre_terms_conditions_sflld.pdf) govern use and publication.
   The importer accepts either `sample_perf_YYYY.txt` or `sample_svcg_YYYY.txt` for the monthly performance file inside each ZIP.
3. Run the commands below from the repository root. Python 3 uses only the standard library to extract and normalise the required fields. MySQL 8 performs the audit and calculations. Use a trusted local MySQL server with `local_infile` enabled. Create an empty schema named `credit_portfolio`, and replace the username as needed.

```sh
python scripts/prepare_freddie_samples.py local-data/sample_2022.zip local-data/sample_2023.zip
mysql --local-infile=1 -u YOUR_USERNAME -p credit_portfolio
```

At the MySQL prompt, run the files in order. Use the same session for both files so the temporary tables stay available.

```sql
SOURCE sql/01_load_and_audit.sql
```

Check that the imports show no warnings and that SQL row counts reconcile with the extraction counts. Review orphan performance rows and loans without performance before continuing. Duplicate loan IDs or loan-months cause the primary-key checks to fail. Run the second file once the audit is clean or any gaps have been explained.

```sql
SOURCE sql/02_month_12_arrears.sql
```

## How to read the output

- **Cohort:** Origination year and quarter from the published loan ID. Month 12 is the original first scheduled payment month plus 11 months. This keeps the comparison on the original schedule when a modification resets the reported loan age.
- **Account rate:** Loans with a numeric delinquency code of 3 or higher divided by loans observed at month 12 with positive principal and known numeric delinquency status.
- **Principal rate:** Outstanding principal on those 90+ day arrears loans divided by outstanding principal on the same eligible population. The numerator is the full outstanding principal on delinquent loans.
- **Coverage:** The output counts voluntary payoffs, other exits, unobserved month-12 records, REO acquisitions, nonpositive or missing balances, and unknown delinquency separately. Rates are undefined when a cohort has no eligible loans. This is a point-in-time comparison among eligible loans, so exits and observation gaps matter when interpreting differences.

The official sample takes the same number of loans per full year. Use sample counts to show coverage. A lending-volume trend would require a source for population totals.
