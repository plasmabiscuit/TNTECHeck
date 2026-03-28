# TNTECheck Documentation Gaps and Next Additions

This backlog lists missing or weak documentation needed to keep source adapters and reporting features maintainable.

## Priority 1 (create immediately)

### NSF Award Search source pack

Initial source pack now exists under `docs/Reference_Documentation/NSFAwardSearch/` with official-source links, query/field notes, templates, and TODO tracking.

Next additions to reach strong coverage:

- full API field -> TNTECheck normalized crosswalk
- explicit retry/backoff and partial-failure adapter notes
- refresh SOP for schema/doc change monitoring

### NIFA Data Gateway source pack

Create `docs/Reference_Documentation/NIFADataGateway/` with:

- `README.md` (scope, adapter use, required pre-dev checks)
- endpoint/filter inventory
- field definitions used in TNTECheck outputs
- project/award status and fiscal-year handling notes
- known inconsistencies + fallback behavior guidance

## Priority 2 (high-value structure improvements)

### Source-to-indicator crosswalk

Add a single crosswalk doc showing, for each indicator registry metric:

- source of record
- upstream field(s)
- transform/aggregation rule
- caveats/data-year limitations

### Adapter implementation notes per source

For each source folder, add a short `Implementation_Notes.md` capturing:

- request strategy (batching/pagination)
- normalization assumptions
- expected null patterns
- retry/backoff behavior
- provenance fields included in outputs

### Data refresh SOPs

Per source, add a `Refresh_SOP.md` with:

- where updates are published
- update cadence
- validation checks to run after refresh
- expected breaking-change signals

## Priority 3 (quality-of-life)

### Known issues and decision logs

For each source folder, optionally add:

- `Known_Issues.md`
- `Decision_Log.md`

to preserve historical context for debugging and prevent repeated investigation.

---

## Maintenance rule

When adding a new data source adapter, do not mark it production-ready until:

1. The source folder and `README.md` exist in `docs/Reference_Documentation/`.
2. Endpoint/field docs are linked from the top-level index.
3. At least one adapter-facing implementation note is written.
