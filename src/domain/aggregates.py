"""Pure aggregation helpers for support/oppose counts."""

from __future__ import annotations

from src.domain.models import (
    UNKNOWN_SPONSOR,
    VOTE_TYPE_NAY,
    VOTE_TYPE_YEA,
    Legislator,
    Vote,
    VoteResult,
)


def count_legislator_votes(
    results: list[VoteResult],
) -> dict[int, tuple[int, int]]:
    """Return legislator_id -> (num_supported, num_opposed)."""
    counts: dict[int, list[int]] = {}
    for result in results:
        bucket = counts.setdefault(result.legislator_id, [0, 0])
        if result.vote_type == VOTE_TYPE_YEA:
            bucket[0] += 1
        elif result.vote_type == VOTE_TYPE_NAY:
            bucket[1] += 1
    return {lid: (vals[0], vals[1]) for lid, vals in counts.items()}


def count_bill_votes(
    votes: list[Vote],
    results: list[VoteResult],
) -> dict[int, tuple[int, int]]:
    """Return bill_id -> (supporter_count, opposer_count)."""
    vote_to_bill = {vote.id: vote.bill_id for vote in votes}
    counts: dict[int, list[int]] = {
        vote.bill_id: [0, 0] for vote in votes
    }
    for result in results:
        bill_id = vote_to_bill.get(result.vote_id)
        if bill_id is None:
            continue
        bucket = counts.setdefault(bill_id, [0, 0])
        if result.vote_type == VOTE_TYPE_YEA:
            bucket[0] += 1
        elif result.vote_type == VOTE_TYPE_NAY:
            bucket[1] += 1
    return {bid: (vals[0], vals[1]) for bid, vals in counts.items()}


def resolve_primary_sponsor(
    sponsor_id: int,
    legislators_by_id: dict[int, Legislator],
) -> str:
    legislator = legislators_by_id.get(sponsor_id)
    if legislator is None:
        return UNKNOWN_SPONSOR
    return legislator.name
