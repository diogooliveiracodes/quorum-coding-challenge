"""Entry point: generate legislative support/oppose CSV reports."""

from __future__ import annotations

import sys
from pathlib import Path

from src.io.readers import (
    load_bills,
    load_legislators,
    load_vote_results,
    load_votes,
)
from src.io.writers import write_bill_report, write_legislator_report
from src.reports.bills import build_bill_report
from src.reports.legislators import build_legislator_report

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")

REQUIRED_INPUTS = (
    "legislators.csv",
    "bills.csv",
    "votes.csv",
    "vote_results.csv",
)

LEGISLATOR_REPORT = "legislators-support-oppose-count.csv"
BILL_REPORT = "bills-support-oppose-count.csv"


def ensure_inputs(data_dir: Path) -> list[str]:
    return [name for name in REQUIRED_INPUTS if not (data_dir / name).is_file()]


def generate_reports(data_dir: Path, output_dir: Path) -> None:
    legislators = load_legislators(data_dir / "legislators.csv")
    bills = load_bills(data_dir / "bills.csv")
    votes = load_votes(data_dir / "votes.csv")
    results = load_vote_results(data_dir / "vote_results.csv")

    legislators_by_id = {leg.id: leg for leg in legislators}

    legislator_rows = build_legislator_report(legislators, results)
    bill_rows = build_bill_report(bills, legislators_by_id, votes, results)

    output_dir.mkdir(parents=True, exist_ok=True)
    write_legislator_report(legislator_rows, output_dir / LEGISLATOR_REPORT)
    write_bill_report(bill_rows, output_dir / BILL_REPORT)


def main() -> int:
    missing = ensure_inputs(DATA_DIR)
    if missing:
        print("Missing required input files:", ", ".join(missing), file=sys.stderr)
        return 1

    try:
        generate_reports(DATA_DIR, OUTPUT_DIR)
    except OSError as exc:
        print(f"Failed to generate reports: {exc}", file=sys.stderr)
        return 1

    print("Wrote:")
    print(f"  {OUTPUT_DIR / LEGISLATOR_REPORT}")
    print(f"  {OUTPUT_DIR / BILL_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
