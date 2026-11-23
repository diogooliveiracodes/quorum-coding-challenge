"""Build legislator support/oppose report rows."""

from __future__ import annotations

from typing import Any

from src.domain.aggregates import count_legislator_votes
from src.domain.models import Legislator, VoteResult


def build_legislator_report(
    legislators: list[Legislator],
    results: list[VoteResult],
) -> list[dict[str, Any]]:
    counts = count_legislator_votes(results)
    rows: list[dict[str, Any]] = []
    for legislator in legislators:
        supported, opposed = counts.get(legislator.id, (0, 0))
        rows.append(
            {
                "id": legislator.id,
                "name": legislator.name,
                "num_supported_bills": supported,
                "num_opposed_bills": opposed,
            }
        )
    return rows
