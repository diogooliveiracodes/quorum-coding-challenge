# Quorum Coding Challenge — Legislative Data

Join legislative CSVs and produce support/oppose aggregate reports.

**Stack:** Python 3.12 + standard library (`csv` only). No pip dependencies.  
**Runtime:** Docker Compose (recommended for evaluators).

## Quick start (Docker)

Requires [Docker](https://docs.docker.com/get-docker/) with Compose v2.

```bash
docker compose run --rm app
```

First run builds the image. The container:

1. Reads inputs from `./data` (mounted read-only)
2. Writes outputs to `./output` (mounted on the host)

Rebuild after Dockerfile changes:

```bash
docker compose build
docker compose run --rm app
```

## Inputs

| File | Role |
|------|------|
| `data/legislators.csv` | Legislators (`id`, `name`) |
| `data/bills.csv` | Bills (`id`, `title`, `sponsor_id`) |
| `data/votes.csv` | Votes (`id`, `bill_id`) |
| `data/vote_results.csv` | Casts (`id`, `legislator_id`, `vote_id`, `vote_type`) |

`vote_type`: `1` = Yea (support), `2` = Nay (oppose).

## Expected outputs

Written under `output/` (inputs are never overwritten):

| File | Description |
|------|-------------|
| `legislators-support-oppose-count.csv` | Per-legislator Yea/Nay bill counts |
| `bills-support-oppose-count.csv` | Per-bill supporter/opposer counts + primary sponsor |

## Run without Docker

```bash
python -m src.main
```

Requires Python 3.10+ (developed against 3.12).

## Quality gates (TDD)

Architecture: layered `domain` → `reports` → `io` → `main`. Development is **test-first** (Red → Green → Refactor). Cursor rules under `.cursor/rules/` enforce this.

```bash
# Preferred (Docker)
docker compose run --rm test

# Local
pip install -r requirements-dev.txt
python -m pytest
```

CI runs the same gates on every push/PR (`.github/workflows/ci.yml`).

## Project layout

```
├── data/                 # Input CSVs (do not modify)
├── output/               # Generated report CSVs
├── src/                  # Application source (layered)
│   └── main.py           # Entry point
├── tests/                # pytest suite
├── .cursor/rules/        # Architecture + TDD + quality rules
├── Dockerfile
├── docker-compose.yml    # services: app, test
└── README.md
```

## Spec

Feature specification: [`specs/001-legislative-vote-reports/spec.md`](specs/001-legislative-vote-reports/spec.md)
