"""Smoke tests for entrypoint input validation (existing scaffold)."""

from pathlib import Path

from src.main import REQUIRED_INPUTS, ensure_inputs


def test_required_inputs_match_challenge_files() -> None:
    assert REQUIRED_INPUTS == (
        "legislators.csv",
        "bills.csv",
        "votes.csv",
        "vote_results.csv",
    )


def test_ensure_inputs_ok_for_project_data() -> None:
    missing = ensure_inputs(Path("data"))
    assert missing == []


def test_ensure_inputs_reports_missing_files(tmp_path: Path) -> None:
    missing = ensure_inputs(tmp_path)
    assert set(missing) == set(REQUIRED_INPUTS)
