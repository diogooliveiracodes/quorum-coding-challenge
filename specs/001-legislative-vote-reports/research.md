# Research: Legislative Vote Reports

**Feature**: `001-legislative-vote-reports` | **Date**: 2026-11-23

All Technical Context items were already decided by project conventions and prior design discussion. This document records decisions, rationale, and alternatives so Phase 1 can proceed with zero unresolved clarifications.

---

## 1. Language and CSV processing

**Decision**: Python 3.12 + standard library `csv` module only at runtime.

**Rationale**: Challenge brief and evaluators expect a high-level language; stdlib keeps the Docker image dependency-free and the submission trivial to run. Dataset is tiny, so pandas adds little value.

**Alternatives considered**:
- **pandas** — expressive groupby/joins; rejected as unnecessary runtime dependency for this scale.
- **Node/Go** — fine if showcasing fluency; rejected because Python is the agreed stack and already scaffolded.

---

## 2. Architecture style

**Decision**: Lean layered / ports-adapters: `domain` (pure) → `reports` (use cases) → `io` (CSV adapters) → `main` (wiring).

**Rationale**: Supports TDD (pure aggregates), writeup extensibility (new columns, filtered lists via alternate adapters), and readability without enterprise ceremony.

**Alternatives considered**:
- **Single script** — fastest to draft; rejected because it fights TDD and extensibility narrative.
- **Full Clean Architecture / DI container** — overkill for a 2–3 hour challenge.

---

## 3. Testing strategy

**Decision**: pytest (dev-only); Red → Green → Refactor; domain unit tests first, then report builders, CSV I/O, then e2e against `data/`.

**Rationale**: Matches project Cursor rules and quality gates (`docker compose run --rm test`, CI). Pure functions make correctness proofs cheap (SC-001).

**Alternatives considered**:
- **unittest only** — works without pip; rejected because pytest is already in `requirements-dev.txt` and Compose `test` service.
- **Manual-only verification** — insufficient for TDD gate and regression safety.

---

## 4. Aggregation algorithm

**Decision**: Single-pass (or few-pass) in-memory maps: build `vote_id → bill_id`, then count Yea/Nay by `legislator_id` and by `bill_id`; resolve sponsors via `legislator_id → name` with default `"Unknown"`.

**Rationale**: O(N) over vote results + O(L + B) for report rows; clear time-complexity story for the writeup; adequate for sample and modestly larger CSVs.

**Alternatives considered**:
- **SQL / SQLite** — neat joins; rejected by challenge guidance (no DB needed) and simplicity gate.
- **Nested loops without indexes** — simpler to write naively; rejected for unclear complexity and slower mental model.

---

## 5. Output naming and paths

**Decision**: Write to `output/legislators-support-oppose-count.csv` and `output/bills-support-oppose-count.csv`; never modify `data/*`.

**Rationale**: Spec FR-002/FR-005/FR-010 and AGENTS.md; avoids clobbering input `bills.csv` despite the brief’s example name.

**Alternatives considered**: Writing a second `bills.csv` in-place or overwriting inputs — rejected as unsafe for evaluators.

---

## 6. Runtime delivery

**Decision**: Docker Compose service `app` for evaluators; optional local `python -m src.main`; Compose `test` + GitHub Actions for quality gates.

**Rationale**: Already scaffolded and verified; reproducible environment without asking reviewers to manage venvs.

**Alternatives considered**: Poetry/venv-only delivery — acceptable locally, weaker “one command” story than Compose.

---

## 7. Extensibility (writeup alignment)

**Decision**: Keep domain models as dataclasses; new columns = extend models + report builders; filtered legislator/bill lists = alternate input adapter feeding the same aggregates/reports.

**Rationale**: Direct answers for challenge writeup questions 2 and 3 without changing core count logic.

**Alternatives considered**: Hard-coding column lists only in writers — harder to evolve; rejected for writeup/extensibility goals.

---

## Unresolved clarifications

None. Ready for Phase 1 design artifacts.
