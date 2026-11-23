"""CSV writers for report outputs (never writes under data/)."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Mapping, Sequence


def _write_csv(
    path: Path,
    fieldnames: Sequence[str],
    rows: Iterable[Mapping[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_legislator_report(
    rows: Iterable[Mapping[str, object]],
    path: Path,
) -> None:
    _write_csv(
        path,
        ("id", "name", "num_supported_bills", "num_opposed_bills"),
        rows,
    )


def write_bill_report(
    rows: Iterable[Mapping[str, object]],
    path: Path,
) -> None:
    _write_csv(
        path,
        ("id", "title", "supporter_count", "opposer_count", "primary_sponsor"),
        rows,
    )
