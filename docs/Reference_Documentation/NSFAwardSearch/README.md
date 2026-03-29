# NSF Award Search Reference Pack Index

This folder contains official-source documentation needed to support the `nsf_award_search` adapter and source-backed reporting in TNTECheck.

## Required pre-dev workflow for this source

1. Start with `NSF_Award_Search_Official_Sources.md` to confirm canonical NSF endpoints and platform context.
2. Use `NSF_Award_Search_API_Query_and_Field_Notes.md` for request/response behavior and parameter constraints.
3. Use `NSF_Award_Search_Query_Templates.md` for TTU-first query patterns.
4. Use `NSF_Open_GitHub_Repos_Implementation_Notes.md` for official NSF Open reference-architecture patterns and caveats.
5. Check `TODO.md` for open validation and normalization tasks before shipping adapter changes.

## Files in this pack

- `NSF_Award_Search_Official_Sources.md` — curated list of official NSF pages and what each contributes.
- `NSF_Award_Search_API_Query_and_Field_Notes.md` — request URL patterns, key search parameters, pagination, sorting, and response notes.
- `NSF_Award_Search_Query_Templates.md` — practical API calls for TTU institution-level award history and sampling.
- `NSF_Open_GitHub_Repos_Implementation_Notes.md` — extracted patterns from `nsf-open` repositories and TNTECheck adaptation guidance.
- `TODO.md` — unresolved documentation tasks and implementation follow-ups.

## Scope notes

- This pack focuses on **official NSF/Research.gov materials** for Award Search API usage and Award Search data downloads.
- Eligibility decisions still require separate Grants.gov and program guidance; NSF award records are award-history evidence, not NOFO eligibility truth.
