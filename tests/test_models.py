"""Unit tests for domain models and vote-type constants."""

from src.domain.models import (
    VOTE_TYPE_NAY,
    VOTE_TYPE_YEA,
    Bill,
    Legislator,
    Vote,
    VoteResult,
)


def test_vote_type_constants() -> None:
    assert VOTE_TYPE_YEA == 1
    assert VOTE_TYPE_NAY == 2


def test_legislator_dataclass() -> None:
    person = Legislator(id=1, name="Ada")
    assert person.id == 1
    assert person.name == "Ada"


def test_bill_includes_sponsor_id() -> None:
    bill = Bill(id=10, title="Act", sponsor_id=99)
    assert bill.sponsor_id == 99


def test_vote_and_result() -> None:
    vote = Vote(id=5, bill_id=10)
    result = VoteResult(id=1, legislator_id=1, vote_id=5, vote_type=VOTE_TYPE_YEA)
    assert vote.bill_id == 10
    assert result.vote_type == VOTE_TYPE_YEA
