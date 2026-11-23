# Contract: Output CSV reports

**Feature**: `001-legislative-vote-reports`  
**Encoding**: UTF-8, comma-separated, header row required.

## 1. `output/legislators-support-oppose-count.csv`

| Column | Type | Required | Semantics |
|--------|------|----------|-----------|
| `id` | integer | yes | Legislator id |
| `name` | string | yes | Legislator name |
| `num_supported_bills` | integer | yes | Count of Yea (`vote_type=1`) results |
| `num_opposed_bills` | integer | yes | Count of Nay (`vote_type=2`) results |

**Cardinality**: Exactly one row per row in `data/legislators.csv`.  
**Zeros**: Legislators with no vote results still appear with `0` / `0`.

## 2. `output/bills-support-oppose-count.csv`

| Column | Type | Required | Semantics |
|--------|------|----------|-----------|
| `id` | integer | yes | Bill id |
| `title` | string | yes | Bill title |
| `supporter_count` | integer | yes | Yea results on the bill’s vote |
| `opposer_count` | integer | yes | Nay results on the bill’s vote |
| `primary_sponsor` | string | yes | Sponsor name, or exactly `Unknown` if unresolved |

**Cardinality**: Exactly one row per row in `data/bills.csv`.  
**No vote**: `supporter_count` and `opposer_count` are `0`.  
**Must not** overwrite `data/bills.csv`.

## Vote type semantics

| `vote_type` | Meaning |
|-------------|---------|
| `1` | Yea / support |
| `2` | Nay / oppose |

## Related

- Data model: [../data-model.md](../data-model.md)
- Input schemas: project `data/*.csv` and challenge brief
