"""Tests for CSV readers against sample data/."""

from pathlib import Path

from src.io.readers import load_bills, load_legislators, load_vote_results, load_votes


DATA = Path("data")


def test_load_legislators_from_sample() -> None:
    legislators = load_legislators(DATA / "legislators.csv")
    assert len(legislators) == 20
    assert legislators[0].id == 904789
    assert "Don Bacon" in legislators[0].name


def test_load_bills_includes_sponsor_id() -> None:
    bills = load_bills(DATA / "bills.csv")
    assert len(bills) == 2
    by_id = {b.id: b for b in bills}
    assert by_id[2952375].sponsor_id == 412211
    assert by_id[2900994].sponsor_id == 400100


def test_load_votes_and_results() -> None:
    votes = load_votes(DATA / "votes.csv")
    results = load_vote_results(DATA / "vote_results.csv")
    assert len(votes) == 2
    assert len(results) == 38
    assert votes[0].bill_id == 2900994
