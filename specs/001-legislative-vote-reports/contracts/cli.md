# Contract: CLI entrypoint

**Feature**: `001-legislative-vote-reports`  
**Invocation**: `python -m src.main` or `docker compose run --rm app`

## Interface

| Aspect | Contract |
|--------|----------|
| Working directory | Project root (`/app` in container) |
| Inputs | `data/legislators.csv`, `data/bills.csv`, `data/votes.csv`, `data/vote_results.csv` |
| Outputs | `output/legislators-support-oppose-count.csv`, `output/bills-support-oppose-count.csv` |
| Exit code `0` | Reports written successfully |
| Exit code `≠0` | Missing/invalid required inputs or I/O failure; message on stderr |
| Side effects | Must not modify files under `data/` |

## Evaluator commands

```bash
docker compose run --rm app
# or
python -m src.main
```

See also: [csv-reports.md](./csv-reports.md), [quickstart.md](../quickstart.md).
