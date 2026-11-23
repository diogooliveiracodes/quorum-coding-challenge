# Writeup — Quorum Coding Challenge (Legislative Data)

## 1. Time complexity and tradeoffs

The solution loads the four CSVs into memory and aggregates with hash maps:

- Build `vote_id → bill_id` and count Yea/Nay while scanning `vote_results` once → **O(R)** where R is the number of vote results.
- Emit legislator and bill rows → **O(L + B)**.

Overall time is **O(R + L + B + V)** (including reading votes). Space is proportional to the loaded rows.

**Tradeoffs:** An in-memory, stdlib-only approach favors clarity and zero runtime dependencies over scalability. For this sample (and datasets of similar size) that is appropriate. A SQL engine would make joins declarative but adds operational complexity the brief advised against. Nested loops without maps would be simpler to sketch but worse complexity and harder to reason about.

## 2. Future columns (e.g. “Bill Voted On Date”, “Co-Sponsors”)

Domain models are frozen dataclasses. New attributes belong on the relevant model (`Bill`, `Vote`, …), readers map the new CSV fields, and report builders/writers extend the row dicts and header lists. Aggregation functions stay unchanged unless the new column changes counting rules (e.g. co-sponsors would be a separate join, not mixed into Yea/Nay counts).

## 3. Generating CSVs for a filtered list of legislators or bills

Because aggregation and report building are pure and accept in-memory collections, a filtered run is an alternate input adapter: load full (or partial) CSVs, then pass `legislators = […subset…]` / `bills = […subset…]` into `build_legislator_report` / `build_bill_report` (optionally filtering vote results to matching ids). The same writers produce the CSV contracts. No change to counting logic is required.

## 4. Time spent

Approximately **2.5–3 hours** of focused work across specification, Docker/TDD scaffolding, implementation, and this writeup (excluding long waits on image pulls).
