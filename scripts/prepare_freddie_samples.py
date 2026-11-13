"""Extract the fields needed for the credit audit from annual Freddie Mac samples."""

import argparse
import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
import io
from pathlib import Path, PurePosixPath
import re
from tempfile import TemporaryDirectory
from zipfile import ZipFile


def month(value):
    if not re.fullmatch(r"[0-9]{6}", value):
        raise ValueError(f"invalid YYYYMM value: {value!r}")
    return datetime.strptime(value, "%Y%m").date().isoformat()


def effective_month(value):
    if not value:
        return None
    if re.fullmatch(r"[0-9]{8}", value):
        return datetime.strptime(value, "%Y%m%d").date().replace(day=1).isoformat()
    return month(value)


def loan_quarter(loan_id, year):
    match = re.fullmatch(r"[FA]([0-9]{2})Q([1-4])[0-9]{6,7}", loan_id)
    if match is None or int(match[1]) != year % 100:
        raise ValueError("invalid loan identifier or unexpected origination year")
    return int(match[2])


def principal(value):
    if not value:
        return None
    amount = Decimal(value)
    if not amount.is_finite() or amount < 0 or amount >= 10**12 or amount != round(amount, 2):
        raise ValueError(f"invalid principal balance: {value!r}")
    return format(amount, ".2f")


def origination(row, year):
    loan_id = row[19]
    return loan_id, year, loan_quarter(loan_id, year), month(row[1])


def performance(row, year):
    loan_id = row[0]
    loan_quarter(loan_id, year)
    status, exit_code = row[3], row[8]
    if not re.fullmatch(r"[A-Z0-9]{0,3}", status):
        raise ValueError(f"invalid delinquency code: {status!r}")
    if not re.fullmatch(r"[0-9]{0,2}", exit_code):
        raise ValueError(f"invalid zero-balance code: {exit_code!r}")
    return (
        loan_id, month(row[1]), principal(row[2]), status or None,
        exit_code.zfill(2) if exit_code else None,
        effective_month(row[9]),
    )


def copy_rows(archive, filenames, minimum_fields, convert, year, output):
    members = [name for name in archive.namelist() if PurePosixPath(name).name in filenames]
    if len(members) != 1:
        raise ValueError(f"expected exactly one archive member named {' or '.join(filenames)}")

    filename = members[0]
    count = 0
    with archive.open(filename) as raw:
        reader = csv.reader(io.TextIOWrapper(raw, encoding="utf-8-sig"), delimiter="|")
        for line, fields in enumerate(reader, start=1):
            try:
                if len(fields) < minimum_fields:
                    raise ValueError(f"expected at least {minimum_fields} pipe-delimited fields")
                values = convert([value.strip() for value in fields], year)
            except (ValueError, InvalidOperation) as error:
                raise ValueError(f"{filename}:{line}: {error}") from error
            output.write("\t".join(r"\N" if value is None else str(value) for value in values) + "\n")
            count += 1
    if count == 0:
        raise ValueError(f"{filename} contains no data")
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", nargs="+", type=Path, metavar="sample_YYYY.zip")
    args = parser.parse_args()
    sources = {}
    for path in args.archives:
        match = re.fullmatch(r"sample_([0-9]{4})\.zip", path.name)
        if match is None or int(match[1]) in sources:
            parser.error("use one sample_YYYY.zip archive per origination year")
        sources[int(match[1])] = path

    output_dir = Path("local-data")
    output_dir.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=output_dir) as staging:
        orig_path = Path(staging) / "origination.tsv"
        perf_path = Path(staging) / "performance.tsv"
        with orig_path.open("w", newline="\n", encoding="utf-8") as orig_output, \
                perf_path.open("w", newline="\n", encoding="utf-8") as perf_output:
            for year, path in sorted(sources.items()):
                with ZipFile(path) as archive:
                    loans = copy_rows(archive, (f"sample_orig_{year}.txt",), 20, origination, year, orig_output)
                    performance_files = (f"sample_perf_{year}.txt", f"sample_svcg_{year}.txt")
                    months = copy_rows(archive, performance_files, 10, performance, year, perf_output)
                print(f"{year}: {loans:,} origination rows, {months:,} performance rows")
        orig_path.replace(output_dir / orig_path.name)
        perf_path.replace(output_dir / perf_path.name)


if __name__ == "__main__":
    main()
