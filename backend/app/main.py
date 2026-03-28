from __future__ import annotations

import re
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.models import (
    ComparisonGroupMeta,
    DocsMeta,
    EligibilityProfileMeta,
    ErrorBody,
    ErrorResponse,
    IndicatorMeta,
    MetaEnvelope,
    PresetMeta,
    ReportRunRequest,
    ReportRunResult,
    ProgramGroupMeta,
    ProgramGroupPreview,
    ProgramGroupPreviewItem,
    ProgramGroupUpsertRequest,
    SourceMeta,
)
from app.reporting import run_preset_report
from app.registry import BASE_DATA_DIR, RegistryError, load_registry, save_registry


class SourceResponse(BaseModel):
    data: list[SourceMeta]
    meta: MetaEnvelope


class IndicatorResponse(BaseModel):
    data: list[IndicatorMeta]
    meta: MetaEnvelope


class ProgramGroupResponse(BaseModel):
    data: list[ProgramGroupMeta]
    meta: MetaEnvelope


class ComparisonGroupResponse(BaseModel):
    data: list[ComparisonGroupMeta]
    meta: MetaEnvelope


class PresetResponse(BaseModel):
    data: list[PresetMeta]
    meta: MetaEnvelope


class DocsResponse(BaseModel):
    data: list[DocsMeta]
    meta: MetaEnvelope


class EligibilityProfileResponse(BaseModel):
    data: list[EligibilityProfileMeta]
    meta: MetaEnvelope


app = FastAPI(title="TNTECheck Metadata API", version="0.1.0")
CIP_PATTERN = re.compile(r"^\d{2}(\.\d{2}(\d{2})?)?$")


def _envelope(items: list[BaseModel]) -> dict:
    return {
        "data": [item.model_dump(mode="json") for item in items],
        "meta": {"version": "v1", "count": len(items)},
    }


def _load(name: str, model_type: type[BaseModel], *, data_dir: Path | None = None) -> list[BaseModel]:
    resolved_dir = data_dir or BASE_DATA_DIR
    return load_registry(name, model_type, data_dir=resolved_dir)


def _save(name: str, items: list[BaseModel], *, data_dir: Path | None = None) -> None:
    resolved_dir = data_dir or BASE_DATA_DIR
    save_registry(name, items, data_dir=resolved_dir)


def _validate_program_group(payload: ProgramGroupUpsertRequest, *, existing_id: str | None = None) -> None:
    malformed_cips = [value for value in payload.cip_codes if not CIP_PATTERN.match(value)]
    if malformed_cips:
        raise RegistryError(
            code="INVALID_PROGRAM_GROUP_CIP",
            message="Program group contains malformed CIP values.",
            details={"invalid_cip_codes": malformed_cips},
        )

    if not payload.award_levels:
        raise RegistryError(
            code="EMPTY_PROGRAM_GROUP_AWARD_LEVELS",
            message="Program group must include at least one award level.",
            details={"id": payload.id},
        )

    if not payload.cip_codes:
        raise RegistryError(
            code="EMPTY_PROGRAM_GROUP_CIPS",
            message="Program group must include at least one CIP code.",
            details={"id": payload.id},
        )

    existing = {item.id for item in _load("program_groups", ProgramGroupMeta)}
    if payload.id in existing and payload.id != existing_id:
        raise RegistryError(
            code="DUPLICATE_PROGRAM_GROUP_ID",
            message=f"Program group id '{payload.id}' already exists.",
            details={"id": payload.id},
        )


def _preview_program_group(payload: ProgramGroupUpsertRequest) -> ProgramGroupPreview:
    unique_award_levels = sorted(set(payload.award_levels))
    return ProgramGroupPreview(
        requested_scope=payload.scope,
        total_cip_codes=len(payload.cip_codes),
        total_award_levels=len(unique_award_levels),
        total_combinations=len(payload.cip_codes) * len(unique_award_levels),
        items=[
            ProgramGroupPreviewItem(cip_code=cip_code, award_levels=unique_award_levels)
            for cip_code in payload.cip_codes
        ],
    )


@app.exception_handler(RegistryError)
async def handle_registry_error(_: Request, exc: RegistryError) -> JSONResponse:
    payload = ErrorResponse(error=ErrorBody(code=exc.code, message=exc.message, details=exc.details))
    status_map = {
        "PRESET_NOT_FOUND": 404,
        "INVALID_FILTER": 422,
        "PRESET_NOT_IMPLEMENTED": 422,
        "PROGRAM_GROUP_NOT_FOUND": 404,
        "DUPLICATE_PROGRAM_GROUP_ID": 409,
        "INVALID_PROGRAM_GROUP_CIP": 422,
        "EMPTY_PROGRAM_GROUP_CIPS": 422,
        "EMPTY_PROGRAM_GROUP_AWARD_LEVELS": 422,
    }
    return JSONResponse(status_code=status_map.get(exc.code, 500), content=payload.model_dump(mode="json"))


@app.get("/api/meta/sources", response_model=SourceResponse, responses={500: {"model": ErrorResponse}})
def get_sources() -> dict:
    return _envelope(_load("sources", SourceMeta))


@app.get("/api/meta/indicators", response_model=IndicatorResponse, responses={500: {"model": ErrorResponse}})
def get_indicators() -> dict:
    return _envelope(_load("indicators", IndicatorMeta))


@app.get("/api/meta/program-groups", response_model=ProgramGroupResponse, responses={500: {"model": ErrorResponse}})
def get_program_groups() -> dict:
    return _envelope(_load("program_groups", ProgramGroupMeta))


@app.get("/api/program-groups", response_model=ProgramGroupResponse, responses={500: {"model": ErrorResponse}})
def list_program_groups() -> dict:
    return _envelope(_load("program_groups", ProgramGroupMeta))


@app.post("/api/program-groups", response_model=ProgramGroupMeta, responses={409: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
def create_program_group(request: ProgramGroupUpsertRequest) -> ProgramGroupMeta:
    _validate_program_group(request)
    items = _load("program_groups", ProgramGroupMeta)
    created = ProgramGroupMeta(
        id=request.id,
        label=request.label,
        scope=request.scope,
        description=request.description,
        cip_codes=request.cip_codes,
        award_levels=request.award_levels,
        notes=request.notes,
        version=1,
    )
    items.append(created)
    _save("program_groups", items)
    return created


@app.put("/api/program-groups/{program_group_id}", response_model=ProgramGroupMeta, responses={404: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
def update_program_group(program_group_id: str, request: ProgramGroupUpsertRequest) -> ProgramGroupMeta:
    items = _load("program_groups", ProgramGroupMeta)
    found_index = next((idx for idx, item in enumerate(items) if item.id == program_group_id), None)
    if found_index is None:
        raise RegistryError(
            code="PROGRAM_GROUP_NOT_FOUND",
            message=f"Program group '{program_group_id}' was not found.",
            details={"id": program_group_id},
        )

    _validate_program_group(request, existing_id=program_group_id)
    current = items[found_index]
    updated = ProgramGroupMeta(
        id=request.id,
        label=request.label,
        scope=request.scope,
        description=request.description,
        cip_codes=request.cip_codes,
        award_levels=request.award_levels,
        notes=request.notes,
        version=current.version + 1,
    )
    items[found_index] = updated
    _save("program_groups", items)
    return updated


@app.delete("/api/program-groups/{program_group_id}", status_code=204, responses={404: {"model": ErrorResponse}})
def delete_program_group(program_group_id: str) -> None:
    items = _load("program_groups", ProgramGroupMeta)
    next_items = [item for item in items if item.id != program_group_id]
    if len(next_items) == len(items):
        raise RegistryError(
            code="PROGRAM_GROUP_NOT_FOUND",
            message=f"Program group '{program_group_id}' was not found.",
            details={"id": program_group_id},
        )

    _save("program_groups", next_items)


@app.post("/api/program-groups/preview", response_model=ProgramGroupPreview, responses={422: {"model": ErrorResponse}})
def preview_program_group(request: ProgramGroupUpsertRequest) -> ProgramGroupPreview:
    _validate_program_group(request, existing_id=request.id)
    return _preview_program_group(request)


@app.get(
    "/api/meta/comparison-groups",
    response_model=ComparisonGroupResponse,
    responses={500: {"model": ErrorResponse}},
)
def get_comparison_groups() -> dict:
    return _envelope(_load("comparison_groups", ComparisonGroupMeta))


@app.get("/api/meta/presets", response_model=PresetResponse, responses={500: {"model": ErrorResponse}})
def get_presets() -> dict:
    return _envelope(_load("presets", PresetMeta))


@app.get("/api/meta/docs", response_model=DocsResponse, responses={500: {"model": ErrorResponse}})
def get_docs() -> dict:
    return _envelope(_load("docs", DocsMeta))


@app.get(
    "/api/meta/eligibility-profiles",
    response_model=EligibilityProfileResponse,
    responses={500: {"model": ErrorResponse}},
)
def get_eligibility_profiles() -> dict:
    return _envelope(_load("eligibility_profiles", EligibilityProfileMeta))


@app.post(
    "/api/report/run",
    response_model=ReportRunResult,
    responses={404: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
)
def run_report(request: ReportRunRequest) -> ReportRunResult:
    presets = {item.id: item for item in _load("presets", PresetMeta)}
    if request.preset_id not in presets:
        raise RegistryError(
            code="PRESET_NOT_FOUND",
            message=f"Preset '{request.preset_id}' was not found.",
            details={"preset_id": request.preset_id},
        )

    known_program_group_ids = {item.id for item in _load("program_groups", ProgramGroupMeta)}
    known_comparison_group_ids = {item.id for item in _load("comparison_groups", ComparisonGroupMeta)}

    for filter_item in request.filters.items:
        if filter_item.field == "program_group_id" and filter_item.operator == "eq":
            if filter_item.value not in known_program_group_ids:
                raise RegistryError(
                    code="INVALID_FILTER",
                    message="Invalid program_group_id filter value.",
                    details={"field": "program_group_id", "value": filter_item.value},
                )

        if filter_item.field == "comparison_group_id" and filter_item.operator == "eq":
            if filter_item.value not in known_comparison_group_ids:
                raise RegistryError(
                    code="INVALID_FILTER",
                    message="Invalid comparison_group_id filter value.",
                    details={"field": "comparison_group_id", "value": filter_item.value},
                )

    try:
        return run_preset_report(request)
    except NotImplementedError as exc:
        raise RegistryError(
            code="PRESET_NOT_IMPLEMENTED",
            message=str(exc),
            details={"preset_id": request.preset_id},
        ) from exc
