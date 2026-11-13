-- Run both SQL files in one MySQL 8 session with an empty scratch schema selected.
CREATE TEMPORARY TABLE origination (
    loan_id VARCHAR(20) NOT NULL,
    origination_year SMALLINT UNSIGNED NOT NULL,
    origination_quarter TINYINT UNSIGNED NOT NULL,
    first_payment_month DATE NOT NULL
);

CREATE TEMPORARY TABLE performance (
    loan_id VARCHAR(20) NOT NULL,
    reporting_month DATE NOT NULL,
    outstanding_principal DECIMAL(14, 2),
    delinquency_code VARCHAR(3),
    zero_balance_code CHAR(2),
    zero_balance_month DATE
);

LOAD DATA LOCAL INFILE 'local-data/origination.tsv' INTO TABLE origination;
SHOW WARNINGS;
LOAD DATA LOCAL INFILE 'local-data/performance.tsv' INTO TABLE performance;
SHOW WARNINGS;

SELECT origination_year, COUNT(*) AS rows_loaded, COUNT(DISTINCT loan_id) AS unique_loans
FROM origination
GROUP BY origination_year
ORDER BY origination_year;

SELECT COUNT(*) AS performance_rows,
       COUNT(DISTINCT loan_id, reporting_month) AS unique_loan_months,
       MIN(reporting_month) AS first_reporting_month,
       MAX(reporting_month) AS last_reporting_month,
       SUM(outstanding_principal IS NULL) AS missing_principal_rows
FROM performance;

-- The primary keys stop duplicate rows from reaching the analysis.
ALTER TABLE origination ADD PRIMARY KEY (loan_id);
ALTER TABLE performance ADD PRIMARY KEY (loan_id, reporting_month);

SELECT COUNT(*) AS orphan_performance_rows
FROM performance AS p
LEFT JOIN origination AS o ON o.loan_id = p.loan_id
WHERE o.loan_id IS NULL;

SELECT COUNT(*) AS loans_with_no_performance
FROM origination AS o
LEFT JOIN performance AS p ON p.loan_id = o.loan_id
WHERE p.loan_id IS NULL;

SELECT delinquency_code, COUNT(*) AS performance_rows
FROM performance
GROUP BY delinquency_code
ORDER BY performance_rows DESC, delinquency_code;
