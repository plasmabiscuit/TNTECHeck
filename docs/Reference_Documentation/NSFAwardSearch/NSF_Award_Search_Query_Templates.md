# NSF Award Search Query Templates (TTU-first)

These templates are based on official endpoint/parameter documentation and are intended as adapter smoke-test and analyst-starting queries.

## 1) TTU institution history (broad)

```http
GET https://api.nsf.gov/services/v1/awards.json?awardeeName="tennessee+tech+university"&rpp=25&offset=0
```

Use when validating institution matching and pagination.

## 2) TTU + Tennessee filter

```http
GET https://api.nsf.gov/services/v1/awards.json?awardeeName="tennessee+tech+university"&awardeeStateCode=TN&rpp=25&offset=0
```

Use when reducing false positives for similarly named non-TN organizations.

## 3) TTU within an award date range

```http
GET https://api.nsf.gov/services/v1/awards.json?awardeeName="tennessee+tech+university"&dateStart=01/01/2020&dateEnd=12/31/2020&rpp=25&offset=0
```

Use for fiscal/period slices in reporting.

## 4) Keyword + institution query

```http
GET https://api.nsf.gov/services/v1/awards.json?awardeeName="tennessee+tech+university"&keyword="cybersecurity"&rpp=25&offset=0
```

Use for topical trend subsets.

## 5) Single award lookup by ID

```http
GET https://api.nsf.gov/services/v1/awards/1052893.json
```

Use for deterministic unit tests around field normalization.

## 6) Project outcomes for one award

```http
GET https://api.nsf.gov/services/v1/awards/1052893/projectoutcomes.json
```

Use to validate optional narrative-enrichment behavior.

## 7) Boolean keyword usage

```http
GET https://api.nsf.gov/services/v1/awards.json?keyword="materials+AND+quantum+NOT+biology"&rpp=25&offset=0
```

Use only with uppercase boolean operators per official help.

## 8) Pagination follow-up page

```http
GET https://api.nsf.gov/services/v1/awards.json?awardeeName="tennessee+tech+university"&rpp=25&offset=25
```

Use to verify continuous retrieval without duplicates.

---

## Practical adapter conventions

- Always set `rpp` and `offset` explicitly.
- Keep template query parameters URL-encoded in production calls.
- Capture response metadata (`totalCount`, `offset`, `rpp`) for restartable ingestion.
