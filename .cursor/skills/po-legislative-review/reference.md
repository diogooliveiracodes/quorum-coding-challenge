# PO Reference — Legislative Vote Reports

Quick acceptance checklist for Quorum challenge reviews. Canonical detail: `specs/001-legislative-vote-reports/spec.md`.

## User stories

| ID | Priority | Outcome |
|----|----------|---------|
| US1 | P1 (MVP) | `legislators-support-oppose-count.csv` |
| US2 | P1 | `bills-support-oppose-count.csv` |
| US3 | P2 | Source + README + outputs + writeup (4 questions) |

## Functional requirements (short)

| ID | Check |
|----|--------|
| FR-001 | Reads all four input CSVs |
| FR-002 | Legislator output filename + columns |
| FR-003 | Yea/Nay counts per legislator |
| FR-004 | All legislators, including zero votes |
| FR-005 | Bill output distinct name + columns |
| FR-006 | Yea/Nay counts per bill vote |
| FR-007 | Sponsor name or `Unknown` |
| FR-008 | All bills included |
| FR-009 | `1`=Yea, `2`=Nay |
| FR-010 | Inputs never overwritten |
| FR-011 | Submission package complete |

## Success criteria (short)

| ID | Check |
|----|--------|
| SC-001 | 100% agreement vs sample / proven baseline |
| SC-002 | Exactly one row per legislator and per bill |
| SC-003 | `Unknown` + zero counts handled |
| SC-004 | Regenerable; inputs intact |
| SC-005 | Reviewer needs only the submission package |

## Output contracts

**Legislators** → `output/legislators-support-oppose-count.csv`  
Columns: `id`, `name`, `num_supported_bills`, `num_opposed_bills`

**Bills** → `output/bills-support-oppose-count.csv`  
Columns: `id`, `title`, `supporter_count`, `opposer_count`, `primary_sponsor`

## Writeup questions (US3)

1. Time complexity and tradeoffs  
2. Future columns (voted-on date, co-sponsors)  
3. Filtered list of legislators/bills instead of full CSVs  
4. Time spent  

## PO anti-patterns (flag these)

- Overwriting `data/bills.csv` for the bill report  
- Omitting legislators with no votes  
- Treating sponsor miss as empty string instead of `Unknown`  
- Shipping without tests / skipping TDD  
- Runtime dependencies beyond Python stdlib  
- Scope creep (DB, APIs, UI) without challenge value  
