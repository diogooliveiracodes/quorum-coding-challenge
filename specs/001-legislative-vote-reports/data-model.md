# Data Model: Legislative Vote Reports

**Feature**: `001-legislative-vote-reports` | **Date**: 2026-11-23  
**Source**: [spec.md](./spec.md), input CSVs under `data/`

## Entities

### Legislator (Person)

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `id` | int | `legislators.csv` | Primary key |
| `name` | string | `legislators.csv` | Display name |

**Rules**: Every legislator appears in the legislator report even with zero vote results (counts = 0).

### Bill

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `id` | int | `bills.csv` | Primary key |
| `title` | string | `bills.csv` | Bill title |
| `sponsor_id` | int | `bills.csv` (`sponsor_id`) | FK → Legislator; may be unresolved |

**Rules**: Every bill appears in the bill report. Unresolved `sponsor_id` → primary sponsor name `"Unknown"`.

### Vote

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `id` | int | `votes.csv` | Primary key |
| `bill_id` | int | `votes.csv` | FK → Bill |

**Rules**: For this challenge dataset, at most one Vote per Bill. Missing vote ⇒ bill supporter/opposer counts = 0.

### VoteResult

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `id` | int | `vote_results.csv` | Primary key |
| `legislator_id` | int | `vote_results.csv` | FK → Legislator |
| `vote_id` | int | `vote_results.csv` | FK → Vote |
| `vote_type` | int | `vote_results.csv` | `1` = Yea (support), `2` = Nay (oppose) |

**Rules**: Only `1` and `2` are in scope. Each result contributes to both legislator-level and bill-level aggregates via `vote_id → bill_id`.

## Relationships

```text
Legislator 1──* VoteResult *──1 Vote *──1 Bill
Bill *──? Legislator   (via sponsor_id; optional / may be Unknown)
```

## Derived report rows (not persisted as entities)

### LegislatorSupportOpposeRow

| Field | Type | Derivation |
|-------|------|------------|
| `id` | int | Legislator.id |
| `name` | string | Legislator.name |
| `num_supported_bills` | int | Count VoteResult where legislator + vote_type=1 |
| `num_opposed_bills` | int | Count VoteResult where legislator + vote_type=2 |

### BillSupportOpposeRow

| Field | Type | Derivation |
|-------|------|------------|
| `id` | int | Bill.id |
| `title` | string | Bill.title |
| `supporter_count` | int | Yea results on the bill’s vote (0 if none) |
| `opposer_count` | int | Nay results on the bill’s vote (0 if none) |
| `primary_sponsor` | string | Legislator.name for `sponsor_id`, else `"Unknown"` |

## Validation rules

1. Input files required: `legislators.csv`, `bills.csv`, `votes.csv`, `vote_results.csv`.
2. IDs treated as integers after CSV parse.
3. Legislator report cardinality = number of legislators.
4. Bill report cardinality = number of bills.
5. Outputs must not mutate input files.

## State transitions

N/A — batch, read-only aggregation (no entity lifecycle beyond load → compute → write).
