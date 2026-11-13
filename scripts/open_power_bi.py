"""Open the Power BI report directly from this checkout using its local CSV."""

import argparse
import os
from pathlib import Path
from tempfile import NamedTemporaryFile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-only", action="store_true", help="Set up the local model without launching Desktop")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    csv_path = root / "local-data" / "month_12_cohorts.csv"
    if not csv_path.is_file():
        parser.exit(1, "Missing local-data/month_12_cohorts.csv. Generate it using docs/POWER_BI.md.\n")

    project = root / "power-bi" / "Credit Portfolio.pbip"
    if not project.is_file():
        parser.exit(1, "Power BI project is missing. Pull the latest files in GitHub Desktop.\n")

    definition = project.parent / "Credit Portfolio.SemanticModel" / "definition"
    parameter = definition / "expressions.tmdl"
    path_literal = str(csv_path).replace("#(", "#(#)(").replace('"', '""')
    expression = (
        f'expression CohortCsvPath = "{path_literal}" '
        'meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=false]\n'
    )
    try:
        if not parameter.exists() or parameter.read_text(encoding="utf-8-sig") != expression:
            with NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=definition,
                                    suffix=".tmp", delete=False) as staging:
                staged = Path(staging.name)
                try:
                    staging.write(expression)
                    staging.close()
                    staged.replace(parameter)
                finally:
                    staging.close()
                    staged.unlink(missing_ok=True)
    except OSError as error:
        parser.exit(1, f"Could not write the local Power BI connection: {error}\n")

    print("Connected Power BI to local-data/month_12_cohorts.csv.")
    if args.prepare_only:
        return
    if os.name != "nt":
        parser.exit(1, "Open power-bi/Credit Portfolio.pbip using Power BI Desktop on Windows.\n")
    try:
        os.startfile(project)
    except OSError:
        parser.exit(1, f"Open this project from File > Open in Power BI Desktop:\n{project}\n")


if __name__ == "__main__":
    main()
