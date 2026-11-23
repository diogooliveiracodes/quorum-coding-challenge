"""Unit tests for pure aggregation functions."""

from src.domain.aggregates import (
    count_bill_votes,
    count_legislator_votes,
    resolve_primary_sponsor,
)
from src.domain.models import (
    VOTE_TYPE_NAY,
    VOTE_TYPE_YEA,
    Bill,
    Legislator,
    Vote,
    VoteResult,
)


def test_count_legislator_votes_yea_and_nay() -> None:
    results = [
        VoteResult(1, 10, 100, VOTE_TYPE_YEA),
        VoteResult(2, 10, 101, VOTE_TYPE_NAY),
        VoteResult(3, 11, 100, VOTE_TYPE_YEA),
    ]
    counts = count_legislator_votes(results)
    assert counts[10] == (1, 1)
    assert counts[11] == (1, 0)


def test_count_legislator_votes_missing_legislator_not_in_map() -> None:
    counts = count_legislator_votes([])
    assert counts == {}


def test_count_bill_votes_via_vote_map() -> None:
    votes = [Vote(100, 1), Vote(200, 2)]
    results = [
        VoteResult(1, 10, 100, VOTE_TYPE_YEA),
        VoteResult(2, 11, 100, VOTE_TYPE_NAY),
        VoteResult(3, 12, 200, VOTE_TYPE_YEA),
    ]
    counts = count_bill_votes(votes, results)
    assert counts[1] == (1, 1)
    assert counts[2] == (1, 0)


def test_count_bill_votes_no_vote_means_absent_or_zero() -> None:
    votes = [Vote(100, 1)]
    counts = count_bill_votes(votes, [])
    assert counts.get(1, (0, 0)) == (0, 0)


def test_resolve_primary_sponsor_known_and_unknown() -> None:
    legislators = {412211: Legislator(412211, "Rep. John Yarmuth (D-KY-3)")}
    assert resolve_primary_sponsor(412211, legislators) == "Rep. John Yarmuth (D-KY-3)"
    assert resolve_primary_sponsor(400100, legislators) == "Unknown"
