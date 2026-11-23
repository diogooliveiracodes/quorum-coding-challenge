# Feature Specification: Legislative Vote Reports

**Feature Branch**: `001-legislative-vote-reports`

**Created**: 2026-11-23

**Status**: Draft

**Input**: User description: "Quorum Coding Challenge — Working with Legislative Data (docs/Quorum Coding Challenge Legislative Data.md)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Legislator support/oppose counts (Priority: P1)

An analyst needs, for every legislator in the provided dataset, how many bills that legislator supported (voted Yea) and how many they opposed (voted Nay), so they can see each legislator’s voting posture across the dataset.

**Why this priority**: This is the first required deliverable of the challenge and the core per-person aggregation clients rely on for visualization.

**Independent Test**: Run the report against the provided legislative dataset and verify one row per legislator with correct Yea/Nay bill counts (including legislators who cast no votes).

**Acceptance Scenarios**:

1. **Given** the full legislative input dataset, **When** the legislator support/oppose report is produced, **Then** the output contains exactly one row per legislator present in the legislators input, with columns for legislator id, name, number of bills supported, and number of bills opposed.
2. **Given** a legislator who voted Yea on some bills and Nay on others, **When** the report is produced, **Then** `num_supported_bills` equals the count of Yea votes (`vote_type` = support) and `num_opposed_bills` equals the count of Nay votes (`vote_type` = oppose) for that legislator.
3. **Given** a legislator who appears in the legislators list but has no vote results, **When** the report is produced, **Then** that legislator still appears with both supported and opposed counts equal to zero.

---

### User Story 2 - Bill support/oppose counts and primary sponsor (Priority: P1)

An analyst needs, for every bill in the dataset, how many legislators supported it, how many opposed it, and who the primary sponsor was (by name), so they can summarize each bill’s vote outcome and sponsorship.

**Why this priority**: This is the second required deliverable and completes the bill-centric view of the same voting data.

**Independent Test**: Run the bill summary report against the provided dataset and verify per-bill supporter/opposer counts and sponsor name resolution (including `"Unknown"` when the sponsor is missing from the legislators list).

**Acceptance Scenarios**:

1. **Given** the full legislative input dataset, **When** the bill summary report is produced, **Then** the output contains exactly one row per bill present in the bills input, with columns for bill id, title, supporter count, opposer count, and primary sponsor name.
2. **Given** a bill that has an associated vote and vote results, **When** the report is produced, **Then** `supporter_count` equals the number of Yea vote results for that bill’s vote and `opposer_count` equals the number of Nay vote results for that bill’s vote.
3. **Given** a bill whose primary sponsor id matches a legislator in the dataset, **When** the report is produced, **Then** `primary_sponsor` is that legislator’s name.
4. **Given** a bill whose primary sponsor id is missing from the legislators list (or otherwise unavailable), **When** the report is produced, **Then** `primary_sponsor` is `"Unknown"`.

---

### User Story 3 - Submission package with writeup (Priority: P2)

A reviewer receives a complete submission folder: runnable source with instructions, the two output reports, and a short writeup answering the challenge’s reflection questions (complexity/tradeoffs, extensibility for new columns, generating reports for a filtered list of legislators/bills, and time spent).

**Why this priority**: Required for evaluation completeness, but depends on correct reports from the stories above.

**Independent Test**: Inspect the submission folder for source + run steps, both output CSVs, and a writeup that addresses all four reflection questions.

**Acceptance Scenarios**:

1. **Given** a completed implementation, **When** the submission package is reviewed, **Then** it includes source code, clear steps to regenerate the outputs from the provided inputs, both required CSV outputs, and a writeup covering all four requested questions.

---

### Edge Cases

- Legislator present in the legislators list with zero vote results → included with supported = 0 and opposed = 0.
- Bill sponsor id not found among legislators → primary sponsor shown as `"Unknown"`.
- Bill with no associated vote (or no vote results) → supporter and opposer counts are zero; bill still appears in the bill report.
- Dataset constraint for this challenge: at most one vote per bill; counts are taken from that single vote’s results.
- Input data files must not be overwritten; report outputs use distinct file names from the inputs.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The solution MUST read the provided legislative dataset consisting of legislators, bills, votes, and vote results.
- **FR-002**: The solution MUST produce a legislator report CSV named `legislators-support-oppose-count.csv` with columns: `id`, `name`, `num_supported_bills`, `num_opposed_bills`.
- **FR-003**: For each legislator, `num_supported_bills` MUST equal the number of vote results where that legislator’s `vote_type` indicates Yea (support), and `num_opposed_bills` MUST equal the number where `vote_type` indicates Nay (oppose).
- **FR-004**: The legislator report MUST include every legislator from the legislators input, including those with no votes.
- **FR-005**: The solution MUST produce a bill summary CSV with a distinct output name that does not overwrite the input bills file (e.g. `bills-support-oppose-count.csv`), with columns: `id`, `title`, `supporter_count`, `opposer_count`, `primary_sponsor`.
- **FR-006**: For each bill, `supporter_count` and `opposer_count` MUST reflect the number of Yea and Nay vote results associated with that bill’s vote.
- **FR-007**: `primary_sponsor` MUST be the sponsor’s name when the bill’s sponsor id resolves to a legislator in the dataset; otherwise it MUST be `"Unknown"`.
- **FR-008**: The bill summary MUST include every bill from the bills input.
- **FR-009**: Vote type semantics MUST treat `1` as Yea (support) and `2` as Nay (oppose).
- **FR-010**: Input CSVs MUST remain unchanged; only separately named output files may be written.
- **FR-011**: The submission MUST include source code, run instructions, both output CSVs, and a writeup answering: time complexity and tradeoffs; how to extend for future columns (e.g. bill voted-on date, co-sponsors); how to generate CSVs for a filtered list of legislators or bills; and time spent on the assignment.

### Key Entities

- **Legislator (Person)**: An elected official identified by id and name; may cast many vote results; may sponsor bills.
- **Bill**: A piece of legislation with id, title, and a primary sponsor id referencing a legislator (may be unresolved).
- **Vote**: A recorded vote event on a bill (at most one per bill in this challenge’s dataset), linking vote results to that bill.
- **Vote Result**: A single legislator’s Yea or Nay cast on a specific vote.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Against the provided sample dataset, both output reports match expected support/oppose counts and sponsor names for every legislator and bill (100% row-level agreement with a manually verified baseline or equivalent proof of correctness).
- **SC-002**: Every legislator and every bill from the inputs appears exactly once in the corresponding report (no missing or duplicate entity rows).
- **SC-003**: Missing sponsors are represented as `"Unknown"` in 100% of applicable bill rows; legislators with no votes show zero counts rather than being omitted.
- **SC-004**: Regenerating the reports from the provided inputs via the documented run steps produces the same two output files without modifying the four input files.
- **SC-005**: A reviewer can complete evaluation of correctness, structure, and the writeup using only the submission package contents.

## Assumptions

- The feature description is the Quorum Coding Challenge legislative-data brief; sample inputs live in the project’s data directory (`legislators.csv`, `bills.csv`, `votes.csv`, `vote_results.csv`).
- In the provided bills input, the primary sponsor field is `sponsor_id` (equivalent to the brief’s “Primary Sponsor”).
- Output for the bill summary uses a distinct filename (such as `bills-support-oppose-count.csv`) so the input `bills.csv` is never overwritten, even though the brief’s example suggested reusing `bills.csv`.
- For this dataset, there is at most one vote per bill; if a bill has no vote, supporter and opposer counts are zero.
- “Support” means Yea (`vote_type` = 1); “oppose” means Nay (`vote_type` = 2); other vote types are out of scope for this challenge.
- A simple, correct approach is preferred over heavy infrastructure (no database required); suggested effort is about 2–3 hours.
- Optional git history showing progress is encouraged but not required for acceptance of the functional reports.
- The project constitution file is still a placeholder template and does not add additional governance constraints beyond this specification and project agent conventions.
