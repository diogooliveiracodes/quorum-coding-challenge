---
description: "Task list for Legislative Vote Reports implementation"
---

# Tasks: Legislative Vote Reports

**Input**: Design documents from `/specs/001-legislative-vote-reports/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: **Included (TDD mandatory)** per `.cursor/rules/tdd-workflow.mdc` and plan — write failing tests before implementation.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: User story label (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Single project: `src/`, `tests/` at repository root (see plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Package layout for layered architecture (Docker/pytest already exist)

- [x] T001 Create package directories and `__init__.py` files for `src/domain/`, `src/reports/`, and `src/io/` per plan.md structure
- [x] T002 [P] Add empty module stubs `src/domain/models.py`, `src/domain/aggregates.py`, `src/reports/legislators.py`, `src/reports/bills.py`, `src/io/readers.py`, and `src/io/writers.py` ready for TDD

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared domain models and CSV readers that ALL stories need

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 [P] Write failing unit tests for domain models and vote-type constants (`vote_type` `1` = Yea/support, `2` = Nay/oppose) in `tests/test_models.py`
- [x] T004 [P] Write failing unit tests for CSV readers loading legislators, bills (`sponsor_id` required), votes, and vote_results from `data/` in `tests/test_csv_io.py`
- [x] T005 Implement frozen dataclasses `Legislator`, `Bill`, `Vote`, `VoteResult` and vote-type constants in `src/domain/models.py` until T003 passes
- [x] T006 Implement stdlib `csv` loaders in `src/io/readers.py` (paths under `data/`; IDs as integers after parse) until T004 passes
- [x] T007 [P] Implement CSV writers scaffolding in `src/io/writers.py` that only write under `output/` and never mutate `data/` (contracts/csv-reports.md)

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: User Story 1 - Legislator support/oppose counts (Priority: P1) 🎯 MVP

**Goal**: Produce `output/legislators-support-oppose-count.csv` with one row per legislator (`id`, `name`, `num_supported_bills`, `num_opposed_bills`), including legislators with zero votes as `0`/`0`.

**Independent Test**: Run report against sample `data/`; verify one row per legislator and Yea/Nay counts match `vote_results.csv` (spec US1 acceptance scenarios).

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T008 [P] [US1] Write failing unit tests for legislator Yea/Nay aggregation (including zero-vote legislators → counts `0`/`0`) in `tests/test_aggregates.py`
- [x] T009 [P] [US1] Write failing unit tests for legislator report row builder schema/columns in `tests/test_legislator_report.py`
- [x] T010 [US1] Write failing test that writes/reads `output/legislators-support-oppose-count.csv` with required columns from contracts/csv-reports.md in `tests/test_legislator_report.py`

### Implementation for User Story 1

- [x] T011 [US1] Implement pure `count_legislator_votes` (or equivalent) in `src/domain/aggregates.py` until T008 passes
- [x] T012 [US1] Implement `build_legislator_report` in `src/reports/legislators.py` (exactly one row per legislator; columns `id`, `name`, `num_supported_bills`, `num_opposed_bills`) until T009 passes
- [x] T013 [US1] Implement `write_legislator_report` in `src/io/writers.py` targeting `output/legislators-support-oppose-count.csv` until T010 passes
- [x] T014 [US1] Wire legislator report path in `src/main.py` (load → aggregate → write legislator CSV; keep exit codes per contracts/cli.md)

**Checkpoint**: User Story 1 fully functional and independently testable (MVP)

---

## Phase 4: User Story 2 - Bill support/oppose counts and primary sponsor (Priority: P1)

**Goal**: Produce `output/bills-support-oppose-count.csv` with one row per bill (`id`, `title`, `supporter_count`, `opposer_count`, `primary_sponsor`), using `"Unknown"` when sponsor is not in legislators; bills with no vote get supporter/opposer `0`.

**Independent Test**: Verify per-bill counts via `votes.csv` + `vote_results.csv` and sponsor name / `"Unknown"` (spec US2 acceptance scenarios).

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T015 [P] [US2] Write failing unit tests for bill Yea/Nay counts and sponsor resolution (`"Unknown"` when `sponsor_id` unresolved; zero counts when no vote) in `tests/test_aggregates.py`
- [x] T016 [P] [US2] Write failing unit tests for bill report row builder in `tests/test_bill_report.py`
- [x] T017 [US2] Write failing test that writes/reads `output/bills-support-oppose-count.csv` without touching `data/bills.csv` in `tests/test_bill_report.py`

### Implementation for User Story 2

- [x] T018 [US2] Extend `src/domain/aggregates.py` with bill vote counts + `resolve_primary_sponsor` (name or exactly `"Unknown"`) until T015 passes
- [x] T019 [US2] Implement `build_bill_report` in `src/reports/bills.py` (exactly one row per bill; required columns per contracts/csv-reports.md) until T016 passes
- [x] T020 [US2] Implement `write_bill_report` in `src/io/writers.py` targeting `output/bills-support-oppose-count.csv` until T017 passes
- [x] T021 [US2] Complete `src/main.py` orchestration to generate both reports in one run (CLI contract: exit `0` on success; stderr + non-zero on missing inputs)

**Checkpoint**: User Stories 1 AND 2 both work independently via `python -m src.main` / `docker compose run --rm app`

---

## Phase 5: User Story 3 - Submission package with writeup (Priority: P2)

**Goal**: Reviewer-ready package: runnable instructions, both output CSVs, writeup answering complexity/tradeoffs, extensibility, filtered lists, and time spent.

**Independent Test**: Inspect submission contents against spec US3 (source + run steps, both CSVs, writeup with four answers).

### Tests for User Story 3 ⚠️

- [x] T022 [US3] Write failing e2e test regenerating both outputs from `data/` and asserting sample correctness + inputs unchanged in `tests/test_e2e_sample_data.py` (quickstart.md / SC-001–SC-004)

### Implementation for User Story 3

- [x] T023 [US3] Make e2e pass by ensuring `src/main.py` end-to-end path matches contracts; commit generated files under `output/` for submission if required by deliverable policy
- [x] T024 [P] [US3] Write `WRITEUP.md` answering: time complexity/tradeoffs; future columns (e.g. voted-on date, co-sponsors); generating CSVs for a filtered legislator/bill list; time spent
- [x] T025 [P] [US3] Update `README.md` run instructions to match quickstart.md (Compose app/test, expected output filenames, link to WRITEUP.md)

**Checkpoint**: Full submission package reviewable without extra context

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation across stories

- [x] T026 Run full quality gates (`docker compose run --rm test` and `docker compose run --rm app`) and fix any failures
- [x] T027 [P] Walk through `specs/001-legislative-vote-reports/quickstart.md` checklist and note any gaps in `WRITEUP.md` or `README.md`
- [x] T028 Refactor only while tests stay green (keep domain pure; no runtime third-party deps)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Setup — **BLOCKS** all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational — MVP
- **User Story 2 (Phase 4)**: Depends on Foundational; reuses readers/models from Phase 2; can proceed after or in parallel with US1 if staffed (shares `aggregates.py` / `main.py` — prefer sequential after US1 to avoid merge conflicts)
- **User Story 3 (Phase 5)**: Depends on US1 + US2 outputs existing
- **Polish (Phase 6)**: Depends on desired stories complete

### User Story Dependencies

- **US1 (P1)**: After Foundational — no dependency on US2/US3
- **US2 (P1)**: After Foundational — independently testable; shares `src/domain/aggregates.py` and `src/main.py` with US1 (coordinate or sequence after US1)
- **US3 (P2)**: After US1 + US2 deliverable CSVs exist

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Aggregates before report builders before writers before `main` wiring
- Story complete before next priority when working solo

### Parallel Opportunities

- T002 stubs in parallel after T001
- T003 || T004 (different test files)
- T008 || T009 (US1 tests)
- T015 || T016 (US2 tests)
- T024 || T025 (docs)
- US1 and US2 can be parallelized only if `aggregates.py` / `writers.py` / `main.py` ownership is split carefully; default recommendation: sequential US1 → US2

---

## Parallel Example: User Story 1

```bash
# Launch US1 failing tests together:
Task: "T008 unit tests for legislator aggregation in tests/test_aggregates.py"
Task: "T009 unit tests for legislator report rows in tests/test_legislator_report.py"

# Then implement in order:
Task: "T011 aggregates in src/domain/aggregates.py"
Task: "T012 report builder in src/reports/legislators.py"
Task: "T013 writer in src/io/writers.py"
Task: "T014 wire src/main.py"
```

---

## Parallel Example: User Story 2

```bash
# Launch US2 failing tests together:
Task: "T015 bill aggregation + Unknown sponsor in tests/test_aggregates.py"
Task: "T016 bill report rows in tests/test_bill_report.py"

# Then implement in order:
Task: "T018 extend src/domain/aggregates.py"
Task: "T019 src/reports/bills.py"
Task: "T020 write_bill_report in src/io/writers.py"
Task: "T021 complete src/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: legislator CSV correct for sample data
5. Demo MVP if needed

### Incremental Delivery

1. Setup + Foundational → shared models/readers ready
2. US1 → legislator report → MVP
3. US2 → bill report → both CSVs
4. US3 → writeup + package polish
5. Polish → quickstart + quality gates green

### Parallel Team Strategy

1. Pair on Setup + Foundational
2. After Foundational: Dev A on US1, Dev B prepares US2 tests only; merge US1 before US2 implementation touching shared files
3. US3 docs can start in parallel once CSV contracts are stable

---

## Notes

- [P] = different files, no incomplete-task dependencies
- [USn] maps to spec user stories
- Runtime remains Python stdlib only; pytest is dev-only
- Verify tests fail before implementing; commit after each task or logical group
- Avoid overwriting `data/*.csv`; outputs only under `output/`
