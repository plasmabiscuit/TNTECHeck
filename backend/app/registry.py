from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError


class RegistryError(Exception):
    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}


BASE_DATA_DIR = Path(__file__).resolve().parent / "data"


def load_registry(name: str, model_type: type[BaseModel], *, data_dir: Path = BASE_DATA_DIR) -> list[BaseModel]:
    registry_path = data_dir / f"{name}.json"
    if not registry_path.exists():
        raise RegistryError(
            code="REGISTRY_NOT_FOUND",
            message=f"Registry '{name}' is missing.",
            details={"registry": name, "path": str(registry_path)},
        )

    try:
        payload = json.loads(registry_path.read_text())
    except json.JSONDecodeError as exc:
        raise RegistryError(
            code="REGISTRY_PARSE_ERROR",
            message=f"Registry '{name}' is not valid JSON.",
            details={"registry": name, "path": str(registry_path), "error": str(exc)},
        ) from exc

    if not isinstance(payload, list):
        raise RegistryError(
            code="REGISTRY_SHAPE_ERROR",
            message=f"Registry '{name}' must contain a JSON array.",
            details={"registry": name, "path": str(registry_path), "received_type": type(payload).__name__},
        )

    items: list[BaseModel] = []
    for idx, item in enumerate(payload):
        try:
            items.append(model_type.model_validate(item))
        except ValidationError as exc:
            raise RegistryError(
                code="REGISTRY_VALIDATION_ERROR",
                message=f"Registry '{name}' failed item validation.",
                details={
                    "registry": name,
                    "path": str(registry_path),
                    "index": idx,
                    "error": exc.errors(),
                },
            ) from exc

    return items
