# Registry File Structure

The backend loads JSON registries from the `registries/` folder on first access via `get_registry_bundle()` (typically triggered by the first metadata request), then caches the bundle and validates each entry against typed schemas.

## TTU default context

The registry bundle is TTU-first by default:

- `institution_unitid`: `221847`
- `institution_name`: `Tennessee Technological University`

This context is set in code and applies to all metadata payloads unless explicitly changed in future implementation work.

## Required registry files

All files must exist and must contain a JSON array.

- `registries/sources.json`
- `registries/source_docs.json`
- `registries/presets.json`
- `registries/program_groups.json`
- `registries/comparison_groups.json`
- `registries/eligibility_profiles.json`
- `registries/indicators.json`

## Validation behavior

Validation is fail-fast:

1. Files are loaded in a deterministic order.
2. JSON parse errors raise a `RegistryValidationError` with filename, line, and column.
3. Type/schema validation errors raise a `RegistryValidationError` including registry name and failing index.
4. Duplicate IDs in a single registry raise a `RegistryValidationError`.

Any failure prevents the full bundle from being returned.

## Schema highlights

### Source (`sources.json`)

Required fields:

- `id`, `name`, `description`, `adapter`, `base_url`
- `supports_summary_endpoints` (boolean)
- `supports_live_queries` (boolean)
- `status` (`active | degraded | offline`)

### Source docs (`source_docs.json`)

Required fields:

- `id`, `source`, `label`, `url`
- `category` (`api | data_dictionary | download | help | terms`)

### Preset (`presets.json`)

Required fields:

- `id`, `title`, `description`
- optional arrays for `funder_tags`, `required_sources`, `indicators`
- boolean support flags

### Program groups (`program_groups.json`)

Required fields:

- `id`, `name`, `description`
- `mappings[]` with `cip_code` and `label`

### Comparison groups (`comparison_groups.json`)

Required fields:

- `id`, `name`, `description`
- `unitids[]` (non-empty integer array)

### Eligibility profiles (`eligibility_profiles.json`)

Required fields:

- `id`, `name`, `funder`, `program`, `version_label`, `effective_date`
- optional `criteria[]` with `id`, `label`, `comparator`, `threshold`, `indicator_id`
- optional `manual_override_allowed`, `provenance_notes`

### Indicators (`indicators.json`)

Required fields:

- `id`, `name`, `label`, `description`, `domain`
- `source`, `source_topic`, `source_variable`
- `allowed_years`, `allowed_filters`, `aggregation_modes`
- `format`, `unit`, `default_chart`, `provenance`
- boolean support flags (`is_public_source`, `supports_comparison`, `supports_disaggregation`)

## Metadata endpoints

- `GET /api/meta/sources`
- `GET /api/meta/docs`
- `GET /api/meta/presets`
- `GET /api/meta/program-groups`
- `GET /api/meta/comparison-groups`
- `GET /api/meta/indicators`
- `GET /api/eligibility/profiles`

Each endpoint reads from the same validated registry bundle.
