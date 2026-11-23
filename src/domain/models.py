"""Domain models for legislative voting data."""

from __future__ import annotations

from dataclasses import dataclass

VOTE_TYPE_YEA = 1
VOTE_TYPE_NAY = 2

UNKNOWN_SPONSOR = "Unknown"


@dataclass(frozen=True)
class Legislator:
    id: int
    name: str


@dataclass(frozen=True)
class Bill:
    id: int
    title: str
    sponsor_id: int


@dataclass(frozen=True)
class Vote:
    id: int
    bill_id: int


@dataclass(frozen=True)
class VoteResult:
    id: int
    legislator_id: int
    vote_id: int
    vote_type: int
