"""E2E correctness against sample data/ (SC-001–SC-004)."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from src.main import generate_reports

DATA = Path("data")
INPUT_FILES = (
    "legislators.csv",
    "bills.csv",
    "votes.csv",
    "vote_results.csv",
)


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_e2e_sample_reports_and_inputs_unchanged(tmp_path: Path) -> None:
    before = {name: _file_hash(DATA / name) for name in INPUT_FILES}

    out = tmp_path / "output"
    generate_reports(DATA, out)

    after = {name: _file_hash(DATA / name) for name in INPUT_FILES}
    assert before == after

    legislator_rows = _read_csv(out / "legislators-support-oppose-count.csv")
    bill_rows = _read_csv(out / "bills-support-oppose-count.csv")

    assert len(legislator_rows) == 20
    assert len(bill_rows) == 2

    by_leg = {int(r["id"]): r for r in legislator_rows}
    # John Yarmuth sponsors BBB but cast no votes in sample
    assert by_leg[412211]["num_supported_bills"] == "0"
    assert by_leg[412211]["num_opposed_bills"] == "0"
    # Don Bacon: Yea on infrastructure, Nay on BBB
    assert by_leg[904789]["num_supported_bills"] == "1"
    assert by_leg[904789]["num_opposed_bills"] == "1"

    by_bill = {int(r["id"]): r for r in bill_rows}
    bbb = by_bill[2952375]
    infra = by_bill[2900994]
    assert bbb["supporter_count"] == "6"
    assert bbb["opposer_count"] == "13"
    assert "Yarmuth" in bbb["primary_sponsor"]
    assert infra["supporter_count"] == "13"
    assert infra["opposer_count"] == "6"
    assert infra["primary_sponsor"] == "Unknown"
