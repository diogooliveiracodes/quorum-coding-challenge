# Implementation Plan: Legislative Vote Reports

**Branch**: `001-legislative-vote-reports` | **Date**: 2026-11-23 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-legislative-vote-reports/spec.md`

## Summary

Produce two CSV aggregate reports from four legislative input CSVs: (1) per-legislator Yea/Nay bill counts, (2) per-bill supporter/opposer counts plus primary sponsor name (`"Unknown"` when unresolved). Implementation uses Python 3.12 + stdlib `csv`, a lean layered architecture (`domain` → `reports` → `io` → `main`), TDD with pytest, and Docker Compose for reproducible runs.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: Runtime — stdlib only (`csv`, `pathlib`, `dataclasses`). Dev — `pytest` via `requirements-dev.txt`.

**Storage**: Flat CSV files under `data/` (input) and `output/` (reports). No database.

**Testing**: pytest; Red → Green → Refactor. Unit tests for domain/reports; CSV/e2e tests against sample `data/`. Quality gates: `docker compose run --rm test`, CI `.github/workflows/ci.yml`.

**Target Platform**: Cross-platform CLI via Docker Compose (Python 3.12-slim) or local `python -m src.main`.

**Project Type**: Single-package CLI / batch report generator.

**Performance Goals**: Correctness on the provided sample dataset in well under a few seconds; linear-time joins/aggregations over input rows.

**Constraints**: No overwrite of input CSVs; no runtime third-party deps; keep solution simple (challenge target ~2–3 hours); at most one vote per bill in this dataset.

**Scale/Scope**: Small sample dataset (dozens of legislators/vote results, two bills); two output CSVs + README/writeup deliverables.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Official `.specify/memory/constitution.md` is still a **placeholder template** (no ratified principles). Effective gates come from `AGENTS.md` and `.cursor/rules/`:

| Gate | Status |
|------|--------|
| Layered architecture (`domain` / `reports` / `io` / `main`) | PASS — planned structure matches rules |
| TDD mandatory (failing test before production behavior) | PASS — plan requires domain → reports → io → e2e test order |
| Runtime stdlib only; pytest is dev-only | PASS |
| Do not overwrite inputs; distinct output names | PASS — `output/legislators-support-oppose-count.csv`, `output/bills-support-oppose-count.csv` |
| Prefer simple, readable solution over heavy frameworks | PASS — no DB, no DI container |
| Quality gates (`pytest` + app smoke) before done | PASS — Compose `test`/`app` + CI |

**Initial Constitution Check: PASS** (no violations to track).

**Post–Phase 1 Constitution Check: PASS** — `data-model.md`, `contracts/`, and `quickstart.md` preserve layered boundaries, TDD-first validation, stdlib-only runtime, and distinct `output/` paths; no new complexity introduced.

## Project Structure

### Documentation (this feature)

```text
specs/001-legislative-vote-reports/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py                 # CLI entry: load → aggregate → write
├── domain/
│   ├── __init__.py
│   ├── models.py           # Legislator, Bill, Vote, VoteResult, constants
│   └── aggregates.py       # Pure count + sponsor resolution
├── reports/
│   ├── __init__.py
│   ├── legislators.py      # Build legislator report rows
│   └── bills.py            # Build bill report rows
└── io/
    ├── __init__.py
    ├── readers.py          # Load the four input CSVs
    └── writers.py          # Write the two output CSVs

tests/
├── test_main_inputs.py     # Existing smoke (input validation)
├── test_aggregates.py      # Domain unit tests
├── test_legislator_report.py
├── test_bill_report.py
├── test_csv_io.py
└── test_e2e_sample_data.py # Golden / sample correctness

data/                       # Input CSVs (immutable for the app)
output/                     # Generated reports
Dockerfile
docker-compose.yml          # services: app, test
```

**Structure Decision**: Single Python package with explicit layers (not a monorepo/web split). Matches agreed architecture and Cursor rules; keeps evaluators’ mental model small.

## Complexity Tracking

> No constitution/rule violations requiring justification.
