# Quickstart validation: Legislative Vote Reports

**Feature**: `001-legislative-vote-reports`  
Prove the feature end-to-end against the sample dataset. Contracts: [contracts/cli.md](./contracts/cli.md), [contracts/csv-reports.md](./contracts/csv-reports.md). Model: [data-model.md](./data-model.md).

## Prerequisites

- Docker with Compose v2 **or** Python 3.12+
- Repository checked out with `data/*.csv` present and unmodified

## 1. Quality gate (TDD)

```bash
docker compose run --rm test
```

**Expect**: pytest exits 0 (all tests green), including domain, report, I/O, and e2e coverage once implemented.

Local alternative:

```bash
pip install -r requirements-dev.txt
python -m pytest
```

## 2. Generate reports

```bash
docker compose run --rm app
```

**Expect**:
- Exit code 0
- Creates/updates:
  - `output/legislators-support-oppose-count.csv`
  - `output/bills-support-oppose-count.csv`
- Files under `data/` unchanged (same content as before the run)

## 3. Manual spot checks (SC-001–SC-003)

1. Open `output/legislators-support-oppose-count.csv` — row count equals `data/legislators.csv` (minus header); spot-check a known legislator’s Yea/Nay totals against `vote_results.csv`.
2. Open `output/bills-support-oppose-count.csv` — one row per bill; supporter/opposer counts match Yea/Nay casts linked via `votes.csv`; unresolved sponsors show `Unknown`.
3. Re-run step 2 — outputs regenerate identically; inputs still unchanged (SC-004).

## 4. Submission package check (User Story 3)

Confirm the folder includes:

- Source under `src/` + run instructions in `README.md`
- Both output CSVs
- Writeup answering complexity/tradeoffs, extensibility, filtered lists, and time spent

## Failure signals

| Symptom | Likely cause |
|---------|----------------|
| pytest red | Domain/report regression — fix before shipping |
| Missing input error | Incomplete `data/` mount or working directory |
| Overwritten `data/bills.csv` | Writer targeting wrong path — must use `output/` |
| Missing legislator with 0 votes | Report builder filtered empty counts — violate FR-004 |
