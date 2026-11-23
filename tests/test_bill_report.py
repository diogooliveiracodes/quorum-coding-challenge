"""Tests for bill report builder and CSV writer."""

from pathlib import Path

from src.domain.models import (
    VOTE_TYPE_NAY,
    VOTE_TYPE_YEA,
    Bill,
    Legislator,
    Vote,
    VoteResult,
)
from src.io.writers import write_bill_report
from src.reports.bills import build_bill_report


def test_build_bill_report_unknown_sponsor_and_counts() -> None:
    bills = [
        Bill(1, "Known Sponsor Bill", 10),
        Bill(2, "Unknown Sponsor Bill", 999),
        Bill(3, "No Vote Bill", 10),
    ]
    legislators = {10: Legislator(10, "Sponsor Name")}
    votes = [Vote(100, 1), Vote(200, 2)]
    results = [
        VoteResult(1, 1, 100, VOTE_TYPE_YEA),
        VoteResult(2, 2, 100, VOTE_TYPE_NAY),
        VoteResult(3, 3, 200, VOTE_TYPE_YEA),
    ]
    rows = build_bill_report(bills, legislators, votes, results)
    by_id = {r["id"]: r for r in rows}
    assert by_id[1]["supporter_count"] == 1
    assert by_id[1]["opposer_count"] == 1
    assert by_id[1]["primary_sponsor"] == "Sponsor Name"
    assert by_id[2]["primary_sponsor"] == "Unknown"
    assert by_id[3]["supporter_count"] == 0
    assert by_id[3]["opposer_count"] == 0
    assert set(rows[0]) == {
        "id",
        "title",
        "supporter_count",
        "opposer_count",
        "primary_sponsor",
    }


def test_write_bill_report_does_not_use_data_bills_name(tmp_path: Path) -> None:
    rows = [
        {
            "id": 1,
            "title": "Act",
            "supporter_count": 3,
            "opposer_count": 2,
            "primary_sponsor": "Unknown",
        }
    ]
    out = tmp_path / "bills-support-oppose-count.csv"
    write_bill_report(rows, out)
    assert out.name == "bills-support-oppose-count.csv"
    text = out.read_text(encoding="utf-8")
    assert "id,title,supporter_count,opposer_count,primary_sponsor" in text
    assert "Unknown" in text
