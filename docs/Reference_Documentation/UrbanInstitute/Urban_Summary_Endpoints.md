# Urban Summary Endpoints

## 1. Why summary endpoints matter

Urban's summary endpoints exist so users can request aggregated results directly from the API rather than downloading large raw tables and summarizing them locally.

Urban's engineering writeup explains the motivation plainly: the raw endpoints can require millions of rows for some summaries, while summary endpoints can return equivalent high-level results in seconds.

For TNTECHeck, this means summary endpoints should be the **default choice** for:
- KPI tiles
- trend lines
- peer-group comparisons
- breakdown summaries used in proposal narratives
- report tables that do not require record-level detail

## 2. Syntax

Urban's summary endpoint repository and engineering writeup describe the general form as:

```text
https://educationdata.urban.org/api/v1/{section}/{source}/{topic}/summaries?var={var}&stat={stat}&by={by}
```

Where:

- `{section}` is one of:
  - `college-university`
  - `school-districts`
  - `schools`
- `{source}` is the data source:
  - such as `ipeds`, `scorecard`, `ccd`, `crdc`, `saipe`, etc.
- `{topic}` is the endpoint/topic
- `var` is the **numeric, nonfilter** variable to summarize
- `stat` is the summary statistic
- `by` is one or more grouping variables

## 3. Supported statistics

Urban's summary endpoint docs list these statistics:

- `sum`
- `count`
- `avg`
- `min`
- `max`
- `variance`
- `stddev`
- `median`

## 4. Grouping behavior

The docs note that:
- `by` can contain one or more comma-separated grouping variables
- queries are automatically grouped by **year** by default

Example pattern:

```text
.../summaries?var=enrollment&stat=sum&by=fips,race
```

For TNTECHeck, that default year grouping is useful, because many institutional reports need time series without extra work.

## 5. Filters

Summary endpoints also accept additional query-string filters in the same request.

Example from Urban's writeup pattern:

```text
.../summaries?var=enrollment&stat=sum&by=sex&fips=6&race=1,2
```

Implications:
- you can aggregate and filter in one call
- multiple filter values can be passed as comma-separated strings
- the same filter logic should be modeled in TNTECHeck's adapter layer for both raw and summary calls

## 6. Joined directory/context variables

Urban's writeup notes an important optimization: where applicable, summary tables have been **prejoined** against associated `directory` files, which allows extra `by` and `filter` variables that may live outside the raw fact table.

This is more important than it looks.

For TNTECHeck, it means you may be able to group or filter a summary by institutional attributes that come from directory-like context tables without building your own joins first.

That is one of the main reasons Urban is attractive for dashboard/report work.

## 7. When TNTECHeck should prefer summary endpoints

Prefer summary endpoints when:
- the result is an aggregate, not a record-level table
- the frontend needs fast rendering
- the chart is a trend or grouped breakdown
- the dashboard only needs totals, averages, medians, or counts
- peer/institution comparisons are being computed from large source tables

Prefer raw endpoints when:
- you need row-level detail for export
- you need fields not supported in summary mode
- you need custom calculations beyond the supported summary stats
- you need to inspect specific institutions/program records before summarizing

## 8. Practical college examples for TNTECHeck

### Example A: completions by CIP family over time
Use a college-university IPEDS completions endpoint and summarize the relevant completions variable by:
- year
- CIP grouping
- institution or state filter

### Example B: enrollment by race/sex
Use `college-university/ipeds/fall-enrollment/...` in summary mode to get proposal-ready demographic slices without pulling the full raw detail set for multiple years.

### Example C: tuition or net price trends
Use summary mode for:
- annual institutional trend
- state benchmark
- peer-group median/average

### Example D: faculty capacity context
Use summary endpoints for institution-level staffing/salary measures when you need quick benchmarking or trend summaries.

## 9. TNTECHeck implementation pattern

Recommended adapter logic:

1. Maintain a registry of endpoints that support summary mode.
2. For each indicator, specify:
   - raw endpoint
   - summary-compatible numeric variable
   - supported group-by variables
   - supported filters
3. Default to summary mode for charts/KPIs.
4. Fall back to raw mode when summary mode is not available or too restrictive.
5. Cache summary requests aggressively, because these are likely to power repeated report views.

## 10. Hard truth

If you ignore summary endpoints and build TNTECHeck around raw pulls only, you will recreate a slower, clumsier version of functionality Urban already solved.

Use raw endpoints where they are necessary. Do not make them your default when the output is obviously aggregate.
