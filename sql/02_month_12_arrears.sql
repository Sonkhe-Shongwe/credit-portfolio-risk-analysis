-- Payment month 1 is the original first scheduled payment month.
-- Use the original schedule because the source loan age can reset after modification.
CREATE TEMPORARY TABLE first_exit (
    loan_id VARCHAR(20) PRIMARY KEY,
    exit_month DATE NOT NULL,
    zero_balance_code CHAR(2) NOT NULL
);

INSERT INTO first_exit (loan_id, exit_month, zero_balance_code)
SELECT loan_id,
       exit_month,
       zero_balance_code
FROM (
    SELECT loan_id, zero_balance_code,
           COALESCE(zero_balance_month, reporting_month) AS exit_month,
           ROW_NUMBER() OVER (
               PARTITION BY loan_id
               ORDER BY COALESCE(zero_balance_month, reporting_month), reporting_month
           ) AS exit_order
    FROM performance
    WHERE zero_balance_code IS NOT NULL
) AS exits
WHERE exit_order = 1;

WITH month_12 AS (
    SELECT loan_id, origination_year, origination_quarter,
           DATE_ADD(first_payment_month, INTERVAL 11 MONTH) AS target_month
    FROM origination
),
classified AS (
    SELECT m.origination_year, m.origination_quarter, p.outstanding_principal,
           CASE
               WHEN e.exit_month <= m.target_month AND e.zero_balance_code = '01'
                   THEN 'voluntary_payoff_by_month_12'
               WHEN e.exit_month <= m.target_month THEN 'exited_by_month_12'
               WHEN p.loan_id IS NULL THEN 'month_12_unobserved'
               WHEN p.delinquency_code = 'RA' THEN 'real_estate_owned'
               WHEN p.outstanding_principal IS NULL OR p.outstanding_principal <= 0
                   THEN 'no_positive_principal'
               WHEN NOT COALESCE(REGEXP_LIKE(p.delinquency_code, '^[0-9]{1,2}$'), 0)
                   THEN 'unknown_delinquency'
               WHEN CAST(p.delinquency_code AS UNSIGNED) >= 3 THEN 'arrears_90_plus'
               ELSE 'under_90_days'
           END AS month_12_status
    FROM month_12 AS m
    LEFT JOIN performance AS p
        ON p.loan_id = m.loan_id AND p.reporting_month = m.target_month
    LEFT JOIN first_exit AS e ON e.loan_id = m.loan_id
),
cohorts AS (
    SELECT origination_year, origination_quarter, COUNT(*) AS sampled_loans,
           SUM(month_12_status = 'voluntary_payoff_by_month_12') AS voluntary_payoff_by_month_12,
           SUM(month_12_status = 'exited_by_month_12') AS other_exits_by_month_12,
           SUM(month_12_status = 'month_12_unobserved') AS month_12_unobserved,
           SUM(month_12_status = 'real_estate_owned') AS real_estate_owned,
           SUM(month_12_status = 'no_positive_principal') AS no_positive_principal,
           SUM(month_12_status = 'unknown_delinquency') AS unknown_delinquency,
           SUM(month_12_status IN ('arrears_90_plus', 'under_90_days')) AS eligible_loans,
           SUM(month_12_status = 'arrears_90_plus') AS loans_in_90_plus_arrears,
           SUM(CASE WHEN month_12_status IN ('arrears_90_plus', 'under_90_days')
                    THEN outstanding_principal ELSE 0 END) AS eligible_principal,
           SUM(CASE WHEN month_12_status = 'arrears_90_plus'
                    THEN outstanding_principal ELSE 0 END) AS principal_in_90_plus_arrears
    FROM classified
    GROUP BY origination_year, origination_quarter
)
SELECT *,
       ROUND(100.0 * loans_in_90_plus_arrears / NULLIF(eligible_loans, 0), 4)
           AS loans_in_90_plus_arrears_pct,
       ROUND(100.0 * principal_in_90_plus_arrears / NULLIF(eligible_principal, 0), 4)
           AS principal_in_90_plus_arrears_pct
FROM cohorts
ORDER BY origination_year, origination_quarter;
