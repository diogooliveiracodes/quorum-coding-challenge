"""Build bill support/oppose report rows."""

from __future__ import annotations

from typing import Any

from src.domain.aggregates import count_bill_votes, resolve_primary_sponsor
from src.domain.models import Bill, Legislator, Vote, VoteResult


def build_bill_report(
    bills: list[Bill],
    legislators_by_id: dict[int, Legislator],
    votes: list[Vote],
    results: list[VoteResult],
) -> list[dict[str, Any]]:
    counts = count_bill_votes(votes, results)
    rows: list[dict[str, Any]] = []
    for bill in bills:
        supporters, opposers = counts.get(bill.id, (0, 0))
        rows.append(
            {
                "id": bill.id,
                "title": bill.title,
                "supporter_count": supporters,
                "opposer_count": opposers,
                "primary_sponsor": resolve_primary_sponsor(
                    bill.sponsor_id,
                    legislators_by_id,
                ),
            }
        )
    return rows
