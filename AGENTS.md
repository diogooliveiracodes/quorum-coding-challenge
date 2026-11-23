# AGENTS.md — Quorum Coding Challenge (Legislative Data)

## Project

Take-home coding challenge: join legislative CSVs and produce two aggregate reports, plus a short writeup. Prefer a simple, correct solution (suggested time: 2–3 hours). Any language is fine; Python is a natural fit.

## Data (input)

| File | Columns | Notes |
|------|---------|--------|
| `legislators.csv` | `id`, `name` | Person / legislator |
| `bills.csv` | `id`, `title`, `sponsor_id` | Bill; `sponsor_id` → legislator `id` |
| `votes.csv` | `id`, `bill_id` | At most one Vote per Bill in this dataset |
| `vote_results.csv` | `id`, `legislator_id`, `vote_id`, `vote_type` | `1` = Yea (support), `2` = Nay (oppose) |

Relationships: Legislator → VoteResult → Vote → Bill; Bill.sponsor_id → Legislator (may be missing → `"Unknown"`).

## Deliverables

### 1. `legislators-support-oppose-count.csv`

| Column | Description |
|--------|-------------|
| `id` | Legislator id |
| `name` | Legislator name |
| `num_supported_bills` | Count of Yea (`vote_type=1`) |
| `num_opposed_bills` | Count of Nay (`vote_type=2`) |

One row per legislator in the dataset (include legislators with zero votes if present).

### 2. Bills summary CSV (e.g. do **not** overwrite input `bills.csv` — use a distinct name such as `bills-support-oppose-count.csv`)

| Column | Description |
|--------|-------------|
| `id` | Bill id |
| `title` | Bill title |
| `supporter_count` | Legislators who voted Yea on that bill’s vote |
| `opposer_count` | Legislators who voted Nay |
| `primary_sponsor` | Sponsor name, or `"Unknown"` if sponsor not in `legislators.csv` |

### 3. Submission package

- Source code + run instructions (README)
- Output CSVs
- Writeup answering: time complexity/tradeoffs; extensibility for new columns; generating CSVs for a filtered list of legislators/bills instead of full CSVs; time spent
- Optional: git history showing progress

## Evaluation focus

Correctness (prove against sample data), structure/readability/extensibility, idiomatic use of the chosen language. No database required.

## Architecture & TDD

Follow Cursor rules in `.cursor/rules/` (always applied):

- **Layers:** `src/domain` (pure) → `src/reports` (use cases) → `src/io` (CSV) → `src/main` (wiring).
- **TDD:** Red → Green → Refactor; no production behavior without a failing test first.
- **Runtime:** Python 3.12 + stdlib `csv` only; `pytest` is dev-only.

## Quality gates

Must pass before considering work done:

```bash
docker compose run --rm test   # or: pip install -r requirements-dev.txt && python -m pytest
docker compose run --rm app    # smoke
```

CI: `.github/workflows/ci.yml` (pytest + app smoke on push/PR).

## Agent conventions

- Do not overwrite input CSVs; write outputs to clearly named files (`output/`).
- Keep the solution simple and well-tested against the provided dataset before optimizing.
- Prefer a small readable layered module over heavy frameworks.
- When changing join/count logic, verify both output CSVs and edge cases (missing sponsor, legislators with no votes).
- Never skip TDD or quality gates to “finish faster.”
