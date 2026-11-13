"""Run the MySQL audit and write the quarterly Power BI CSV locally."""

import argparse
import csv
from decimal import Decimal
from pathlib import Path
import subprocess
from tempfile import NamedTemporaryFile


ROOT = Path(__file__).resolve().parents[1]
EXCLUSIONS = (
    "voluntary_payoff_by_month_12", "other_exits_by_month_12",
    "month_12_unobserved", "real_estate_owned", "no_positive_principal",
    "unknown_delinquency",
)
FIELDS = (
    "origination_year", "origination_quarter", "sampled_loans", *EXCLUSIONS,
    "eligible_loans", "loans_in_90_plus_arrears", "eligible_principal",
    "principal_in_90_plus_arrears",
)
SQL_RATE_FIELDS = ("loans_in_90_plus_arrears_pct", "principal_in_90_plus_arrears_pct")


def validate(rows):
    keys = set()
    for row in rows:
        year, quarter = (int(row[field]) for field in FIELDS[:2])
        key = (year, quarter)
        if key in keys or quarter not in range(1, 5):
            raise ValueError(f"duplicate or invalid cohort key: {key}")
        keys.add(key)

        sampled = int(row["sampled_loans"])
        eligible = int(row["eligible_loans"])
        excluded = [int(row[field]) for field in EXCLUSIONS]
        in_arrears = int(row["loans_in_90_plus_arrears"])
        principal = Decimal(row["eligible_principal"])
        arrears_principal = Decimal(row["principal_in_90_plus_arrears"])
        if (any(value < 0 for value in excluded) or sampled != eligible + sum(excluded)
                or not 0 <= in_arrears <= eligible or not 0 <= arrears_principal <= principal):
            raise ValueError(f"counts or principal do not reconcile for cohort {key}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mysql", default="mysql", help="MySQL client executable")
    parser.add_argument("mysql_args", nargs=argparse.REMAINDER, help="MySQL arguments after --")
    args = parser.parse_args()
    mysql_args = args.mysql_args
    if mysql_args[:1] == ["--"]:
        mysql_args = mysql_args[1:]

    sql = "\n".join((ROOT / "sql" / name).read_text(encoding="utf-8") for name in (
        "01_load_and_audit.sql", "02_month_12_arrears.sql",
    ))
    try:
        result = subprocess.run(
            [args.mysql, *mysql_args, "--local-infile=1", "--batch", "--column-names"],
            cwd=ROOT, input=sql, stdout=subprocess.PIPE, text=True, check=True,
        )
        header = "\t".join((*FIELDS, *SQL_RATE_FIELDS))
        audit, separator, values = result.stdout.partition(header + "\n")
        if not separator:
            raise ValueError("MySQL output did not contain the expected cohort columns")
        print(audit, end="")
        rows = list(csv.DictReader([header, *values.splitlines()], delimiter="\t"))
        if not rows or any(None in row or None in row.values() for row in rows):
            raise ValueError("MySQL did not return a complete cohort result")
        validate(rows)
    except subprocess.CalledProcessError as error:
        raise SystemExit(f"MySQL failed (exit {error.returncode}). See the client output above.") from error
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error

    output = ROOT / "local-data" / "month_12_cohorts.csv"
    with NamedTemporaryFile(mode="w", encoding="utf-8", newline="", dir=output.parent,
                            delete=False) as staging:
        staged = Path(staging.name)
        try:
            writer = csv.DictWriter(staging, fieldnames=FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
            staging.close()
            staged.replace(output)
        finally:
            staged.unlink(missing_ok=True)
    print(f"Exported {len(rows)} verified cohort rows to {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
