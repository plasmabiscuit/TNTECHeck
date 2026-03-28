# NSF Award Search Source Pack TODO

Updated: 2026-03-28

## Completed in this pass

- [x] Collected official NSF/Research.gov source links for API + Award Search help + download/schema pages.
- [x] Documented canonical endpoint patterns and core request parameters.
- [x] Added TTU-first query templates for adapter validation and reporting workflows.

## Remaining documentation tasks

- [ ] Build a full field catalog crosswalk from API response fields to TNTECheck normalized output keys.
- [ ] Add explicit partial-failure and retry/backoff guidance based on adapter behavior.
- [ ] Add examples of known institution-name variants for TTU matching to reduce false positives/negatives.
- [ ] Add a refresh SOP for periodic verification of official docs and schema changes.
- [ ] Validate if NSF publishes explicit rate-limit guidance; if absent, document observed safe client behavior and caveats.

## Validation checklist before marking source pack "Strong"

- [ ] Top-level docs index updated with final file list and status.
- [ ] At least one adapter-facing implementation note checked into source docs.
- [ ] Regression tests reference canonical docs for parameter/date constraints.
