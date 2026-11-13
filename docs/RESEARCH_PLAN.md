# Research plan

## Business question

At the same point in the repayment schedule, how did early mortgage arrears differ between Freddie Mac loans originated in 2022 and 2023, and how much outstanding principal sat on the loans that were 90 or more days in arrears?

The audience is a credit portfolio monitoring team. Its decision is which origination quarters warrant a closer review. The report should let that team see the arrears gap, check how much principal it represents and see whether payoff or other exits changed the population being compared. An observed gap supports further investigation into borrower mix, loan purpose, servicing or economic conditions. Establishing any of those as a cause requires separate evidence.

## Evidence and scope

- **Primary data:** Freddie Mac Single-Family Loan-Level Dataset, US Standard Dataset annual samples `sample_2022.zip` and `sample_2023.zip`. Each archive includes origination data and monthly performance. The sample design supports cohort comparisons within Freddie Mac's Standard Dataset. It takes 50,000 loans per full vintage year, so estimating actual year-over-year lending volume requires population totals. The case study concerns US mortgages acquired by Freddie Mac. [Dataset](https://www.freddiemac.com/research/datasets/sf-loanlevel-dataset) · [Sample design](https://www.freddiemac.com/fmac-resources/research/pdf/faq.pdf) · [Release notes](https://www.freddiemac.com/fmac-resources/research/pdf/release_notes.pdf)
- **Method reference:** The CFPB compares 90+ day delinquency across credit card origination vintages at equal account ages. We use the same age-alignment principle with mortgage-specific source definitions. [CFPB vintage analysis](https://www.consumerfinance.gov/archive/blog/credit-card-delinquencies-are-higher-than-in-2019-because-lenders-took-on-more-risk/) · [Freddie Mac data dictionary](https://www.freddiemac.com/fmac-resources/research/pdf/user_guide.pdf)
- **Publication:** Keep source ZIPs and loan-level extracts local. Before sharing a report or export publicly, check the Freddie Mac terms for the intended use and ensure the artifact cannot expose or reconstruct source records. Check the data embedded in any Power BI file as well as what the report displays. [Dataset terms](https://capitalmarkets.freddiemac.com/crt/docs/pdfs/fre_terms_conditions_sflld.pdf)

## Method and measures

1. Load one origination record per loan and one performance record per loan per reporting month. Verify keys, join coverage, row counts and principal completeness. Python extracts and normalises the required fields. MySQL performs the analysis.
2. Assign cohort year and quarter from the source loan ID. Set the target to the first scheduled payment month plus 11 calendar months. This preserves the original schedule when Freddie Mac's reported loan age resets after a modification. Use the published reporting month consistently. Freddie Mac documents a lag for delinquency reporting. [Data dictionary](https://www.freddiemac.com/fmac-resources/research/pdf/user_guide.pdf)
3. Classify each sampled loan once at month 12. Use the first recorded exit, with the effective month where supplied and the reporting month as fallback. A loan is eligible if it has an observation at the target month, no exit by then, positive principal and a known numeric delinquency code. Report voluntary payoffs, other exits, missing observations, REO acquisitions, missing or nonpositive principal, and unknown delinquency as separate groups.
4. Compare years and their origination quarters using these measures. Build year totals by summing the underlying numerators and denominators first.

| Measure | Definition |
|---|---|
| Accounts 90+ days in arrears | Eligible loans with delinquency code 3 or above divided by all eligible loans |
| Outstanding principal on accounts 90+ days in arrears | Outstanding principal on those eligible 90+ day loans divided by total eligible outstanding principal |
| Month-12 eligibility | Eligible loans divided by all sampled loans in the cohort |
| Voluntary payoff by month 12 | Loans whose first recorded exit was a voluntary payoff by the target month divided by all sampled loans |

Both arrears measures describe status at one reporting month. A loan that recovered before that month can be current at the snapshot. The principal numerator is the remaining balance on the delinquent loans. The project makes no estimate of the missed instalment amount or realised credit loss. Different origination quarters also reach month 12 in different calendar periods.

## Milestones and acceptance

| Milestone | Deliverable | Acceptance |
|---|---|---|
| 1. Source and data audit | Reproducible import and MySQL quality checks | Verify unique loan and loan-month keys. Reconcile extraction and load counts, and account for unmatched records. |
| 2. First month-12 comparison | Cohort-level MySQL output with counts, balances and rates | Reconcile all eligibility groups to the sample and verify rates from underlying totals. Record which cohorts merit a closer look and what the exits change about the interpretation. |
| 3. Power BI input and measures | One row per origination year and quarter, a data dictionary and report measures | Verify row count, keys, coverage totals and SQL-to-Power BI reconciliation. Check yearly totals under filters by dividing sums, with a blank rate for a zero denominator. |
| 4. Power BI report and findings | One report with a cohort comparison and a coverage view, plus a short findings brief | Show the two arrears rates alongside denominators and exits. Review claims, units and source terms before publication. |

The report should open with the year comparison, then let the reader check which quarters contribute to the gap and how payoffs and other exclusions affect the comparison. Start with the month-12 snapshot. Extend to other ages or borrower segments if the first report leaves a specific question that the available data can answer.
