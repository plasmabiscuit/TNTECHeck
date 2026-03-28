from __future__ import annotations

from typing import Any

from .models import TTU_NAME, TTU_UNITID


def normalize_institution_identity(record: dict[str, Any]) -> dict[str, Any]:
    """Placeholder institution identity normalization hook."""

    normalized = dict(record)
    normalized.setdefault("institution_id", TTU_UNITID)
    normalized.setdefault("institution_name", TTU_NAME)
    return normalized


def normalize_time(record: dict[str, Any]) -> dict[str, Any]:
    """Placeholder year/date normalization hook."""

    normalized = dict(record)
    if "fiscal_year" in normalized and "year" not in normalized:
        normalized["year"] = normalized["fiscal_year"]
    return normalized


def normalize_program_cip(record: dict[str, Any]) -> dict[str, Any]:
    """Placeholder program/CIP normalization hook."""

    normalized = dict(record)
    if "cip" in normalized and "cip_code" not in normalized:
        normalized["cip_code"] = normalized["cip"]
    return normalized


def normalize_funding(record: dict[str, Any]) -> dict[str, Any]:
    """Placeholder funding/currency normalization hook."""

    normalized = dict(record)
    if "amount" in normalized and "value" not in normalized:
        normalized["value"] = normalized["amount"]
    return normalized
