"""Entry point: generate legislative support/oppose CSV reports.

Reads CSVs from data/ and writes reports to output/.
Report generation logic will be implemented in follow-up work.
"""

from __future__ import annotations

import sys
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")

REQUIRED_INPUTS = (
    "legislators.csv",
    "bills.csv",
    "votes.csv",
    "vote_results.csv",
)


def ensure_inputs(data_dir: Path) -> list[str]:
    missing = [name for name in REQUIRED_INPUTS if not (data_dir / name).is_file()]
    return missing


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    missing = ensure_inputs(DATA_DIR)
    if missing:
        print("Missing required input files:", ", ".join(missing), file=sys.stderr)
        return 1

    print("Quorum legislative reports — environment ready.")
    print(f"  data:   {DATA_DIR.resolve()}")
    print(f"  output: {OUTPUT_DIR.resolve()}")
    print("  inputs:", ", ".join(REQUIRED_INPUTS))
    print("Report generation not implemented yet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
