"""Tests for legislator report builder and CSV writer."""

from pathlib import Path

from src.domain.models import Legislator, VoteResult, VOTE_TYPE_NAY, VOTE_TYPE_YEA
from src.io.writers import write_legislator_report
from src.reports.legislators import build_legislator_report


def test_build_legislator_report_includes_zero_vote_legislators() -> None:
    legislators = [
        Legislator(1, "A"),
        Legislator(2, "B"),
    ]
    results = [VoteResult(1, 1, 10, VOTE_TYPE_YEA)]
    rows = build_legislator_report(legislators, results)
    assert len(rows) == 2
    by_id = {r["id"]: r for r in rows}
    assert by_id[1]["num_supported_bills"] == 1
    assert by_id[1]["num_opposed_bills"] == 0
    assert by_id[2]["num_supported_bills"] == 0
    assert by_id[2]["num_opposed_bills"] == 0
    assert set(rows[0]) == {
        "id",
        "name",
        "num_supported_bills",
        "num_opposed_bills",
    }


def test_write_legislator_report_csv(tmp_path: Path) -> None:
    rows = [
        {
            "id": 1,
            "name": "A",
            "num_supported_bills": 2,
            "num_opposed_bills": 1,
        }
    ]
    out = tmp_path / "legislators-support-oppose-count.csv"
    write_legislator_report(rows, out)
    text = out.read_text(encoding="utf-8")
    assert "id,name,num_supported_bills,num_opposed_bills" in text
    assert "1,A,2,1" in text
