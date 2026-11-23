"""CSV readers for legislative input files (stdlib csv only)."""

from __future__ import annotations

import csv
from pathlib import Path

from src.domain.models import Bill, Legislator, Vote, VoteResult


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_legislators(path: Path) -> list[Legislator]:
    return [
        Legislator(id=int(row["id"]), name=row["name"])
        for row in _read_rows(path)
    ]


def load_bills(path: Path) -> list[Bill]:
    return [
        Bill(
            id=int(row["id"]),
            title=row["title"],
            sponsor_id=int(row["sponsor_id"]),
        )
        for row in _read_rows(path)
    ]


def load_votes(path: Path) -> list[Vote]:
    return [
        Vote(id=int(row["id"]), bill_id=int(row["bill_id"]))
        for row in _read_rows(path)
    ]


def load_vote_results(path: Path) -> list[VoteResult]:
    return [
        VoteResult(
            id=int(row["id"]),
            legislator_id=int(row["legislator_id"]),
            vote_id=int(row["vote_id"]),
            vote_type=int(row["vote_type"]),
        )
        for row in _read_rows(path)
    ]
