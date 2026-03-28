# Metadata API Endpoints

All metadata endpoints return a stable envelope:

```json
{
  "data": ["...typed records..."],
  "meta": {
    "version": "v1",
    "count": 0
  }
}
```

Error responses are explicit and debuggable:

```json
{
  "error": {
    "code": "REGISTRY_NOT_FOUND",
    "message": "Registry 'sources' is missing.",
    "details": {
      "registry": "sources",
      "path": ".../sources.json"
    }
  }
}
```

## `GET /api/meta/sources`
Returns source adapter metadata used by source-status and data-source selectors.

`data[]` fields:
- `id` (string)
- `name` (string)
- `kind` (`public_api | download | manual_import`)
- `capabilities` (string[])
- `default_enabled` (boolean)
- `docs_url` (URL, optional)

## `GET /api/meta/indicators`
Returns normalized indicator registry metadata for query and preset builders.

`data[]` fields:
- `id`, `label`, `category`, `unit`, `default_aggregation`
- `source_ids` (string[])
- `description` (optional string)

## `GET /api/meta/program-groups`
Returns TTU-local program group mappings (CIP-driven).

`data[]` fields:
- `id`, `label`, `description` (optional)
- `cip_codes` (string[])

## `GET /api/meta/comparison-groups`
Returns named institution comparison groups for benchmark workflows.

`data[]` fields:
- `id`, `label`, `description` (optional)
- `institution_unitids` (integer[])

## `GET /api/meta/presets`
Returns preset catalog entries used to render report launcher cards and setup defaults.

`data[]` fields:
- `id`, `label`, `sponsor_context` (string[]), `description`
- `sections[]`:
  - `indicator_ids` (string[])
  - `program_group_ids` (string[])
  - `comparison_group_id` (string, optional)

## `GET /api/meta/docs`
Returns external documentation links keyed to sources.

`data[]` fields:
- `id`, `label`, `url`
- `source_id` (optional)
- `tags` (string[])

## `GET /api/meta/eligibility-profiles`
Returns editable eligibility profile templates.

`data[]` fields:
- `id`, `label`, `description`, `provenance_notes` (optional)
- `criteria[]`:
  - `id`, `label`, `indicator_id`
  - `operator` (`> | >= | < | <= | == | != | between`)
  - `threshold` (number | number[] | string)
  - `editable` (boolean)
