# NSF Award Search Official Sources (Web-Collected)

Last verified: **2026-03-28 (UTC)**

This document captures official web references needed to build and maintain the NSF source pack.

## Canonical official sources

| Source | URL | Why it matters for TNTECheck |
|---|---|---|
| NSF Developer Resources | https://www.nsf.gov/digital/developer | Official NSF developer landing page that links to Award Search API and Open Data context. |
| NSF Award Search API docs (Research.gov resources host) | https://resources.research.gov/common/webapi/awardapisearch-v1.htm | Canonical endpoint patterns, parameter list, sort semantics, output examples, and request notes. |
| NSF Award Search API docs (Research.gov host alias) | https://www.research.gov/common/webapi/awardapisearch-v1.htm | Alternate official host for same API documentation used in NSF pages. |
| NSF Award Search Boolean help | https://www.nsf.gov/awardsearch/boolean-search-help | Official operator semantics used by keyword/simple search (AND/OR/NOT behavior and case-sensitivity). |
| NSF Award Search download page | https://www.nsf.gov/awardsearch/download-awards | Official bulk-download UX and format notes; states XML->JSON transition timing. |
| NSF Award download schema JSON | https://www.nsf.gov/awardsearch/resources/Award.json | Official JSON schema for bulk annual award exports; supports normalization/provenance mapping. |

## Key facts captured from official pages

1. API URL families include:
   - `/services/v1/awards.{format}` for search
   - `/services/v1/awards/{id}.{format}` for single-award lookup
   - `/services/v1/awards/{id}/projectoutcomes.{format}` for project outcomes.
2. Query controls include `rpp`, `offset`, `keyword`, and many domain filters (institution, state, dates, PI, program, CFDA, etc.).
3. API docs note default sorting behavior by `startDate` when `sortBy` is not provided.
4. Boolean help page specifies uppercase operators (`AND`, `OR`, `NOT`) and their behavior.
5. Download page indicates that in **January 2025**, downloadable annual files switched from XML to JSON.
6. The download schema file (`Award.json`) is a draft-04 JSON schema and includes required fields and property-level definitions.

## Retrieval evidence (commands used)

```bash
curl -L -s 'https://resources.research.gov/common/webapi/awardapisearch-v1.htm' -o /tmp/nsf_award_api.html
curl -L -s 'https://www.nsf.gov/digital/developer' -o /tmp/nsf_developer.html
curl -L -s 'https://www.nsf.gov/awardsearch/boolean-search-help' -o /tmp/nsf_boolean_help.html
curl -L -s 'https://www.nsf.gov/awardsearch/download-awards' -o /tmp/nsf_download_awards.html
curl -L -s 'https://www.nsf.gov/awardsearch/resources/Award.json' -o /tmp/nsf_award_schema.json
```

## Notes on source reliability

- All links above are NSF/Research.gov official domains.
- The API doc appears accessible from both `resources.research.gov` and `research.gov`; treat them as mirror entry points and pin one canonical URL in code comments/tests.
