from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from backend.registry.models import (
    ComparisonGroupRegistryEntry,
    EligibilityProfileRegistryEntry,
    IndicatorRegistryEntry,
    PresetRegistryEntry,
    ProgramGroupRegistryEntry,
    RegistryBundle,
    SourceDocRegistryEntry,
    SourceRegistryEntry,
)


class RegistryValidationError(ValueError):
    """Raised when a registry file cannot be parsed or validated."""


REGISTRY_FILES = {
    "sources": "sources.json",
    "source_docs": "source_docs.json",
    "presets": "presets.json",
    "program_groups": "program_groups.json",
    "comparison_groups": "comparison_groups.json",
    "eligibility_profiles": "eligibility_profiles.json",
    "indicators": "indicators.json",
}

ENTRY_MODELS = {
    "sources": SourceRegistryEntry,
    "source_docs": SourceDocRegistryEntry,
    "presets": PresetRegistryEntry,
    "program_groups": ProgramGroupRegistryEntry,
    "comparison_groups": ComparisonGroupRegistryEntry,
    "eligibility_profiles": EligibilityProfileRegistryEntry,
    "indicators": IndicatorRegistryEntry,
}


def _read_registry_file(registry_dir: Path, filename: str) -> Any:
    path = registry_dir / filename
    if not path.exists():
        raise RegistryValidationError(f"Missing registry file: {path}")

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RegistryValidationError(
            f"Invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc

    if not isinstance(raw, list):
        raise RegistryValidationError(f"Registry file {path} must contain a JSON array")
    return raw


def _validate_entries(entries: list[dict[str, Any]], key: str, filename: str) -> list[Any]:
    model = ENTRY_MODELS[key]
    validated: list[Any] = []
    seen_ids: set[str] = set()

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise RegistryValidationError(
                f"Registry '{key}' in {filename} must contain objects. Index {index} had type {type(entry).__name__}."
            )

        try:
            validated_entry = model.model_validate(entry)
        except ValidationError as exc:
            raise RegistryValidationError(
                f"Registry '{key}' in {filename} failed validation at index {index}: {exc}"
            ) from exc

        if validated_entry.id in seen_ids:
            raise RegistryValidationError(
                f"Registry '{key}' in {filename} has duplicate id '{validated_entry.id}'"
            )
        seen_ids.add(validated_entry.id)
        validated.append(validated_entry)

    return validated


def load_registries(registry_dir: str | Path) -> RegistryBundle:
    """Load and validate all registry files with fail-fast behavior."""
    base = Path(registry_dir)
    payload: dict[str, Any] = {}

    for key, filename in REGISTRY_FILES.items():
        entries = _read_registry_file(base, filename)
        payload[key] = _validate_entries(entries, key=key, filename=filename)

    return RegistryBundle.model_validate(payload)
