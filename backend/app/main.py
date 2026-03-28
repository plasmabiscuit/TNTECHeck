from __future__ import annotations

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
    ProgramGroupMeta,
    SourceMeta,
)
from app.registry import BASE_DATA_DIR, RegistryError, load_registry


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


def _envelope(items: list[BaseModel]) -> dict:
    return {
        "data": [item.model_dump(mode="json") for item in items],
        "meta": {"version": "v1", "count": len(items)},
    }


def _load(name: str, model_type: type[BaseModel], *, data_dir: Path = BASE_DATA_DIR) -> list[BaseModel]:
    return load_registry(name, model_type, data_dir=data_dir)


@app.exception_handler(RegistryError)
async def handle_registry_error(_: Request, exc: RegistryError) -> JSONResponse:
    payload = ErrorResponse(error=ErrorBody(code=exc.code, message=exc.message, details=exc.details))
    return JSONResponse(status_code=500, content=payload.model_dump(mode="json"))


@app.get("/api/meta/sources", response_model=SourceResponse, responses={500: {"model": ErrorResponse}})
def get_sources() -> dict:
    return _envelope(_load("sources", SourceMeta))


@app.get("/api/meta/indicators", response_model=IndicatorResponse, responses={500: {"model": ErrorResponse}})
def get_indicators() -> dict:
    return _envelope(_load("indicators", IndicatorMeta))


@app.get("/api/meta/program-groups", response_model=ProgramGroupResponse, responses={500: {"model": ErrorResponse}})
def get_program_groups() -> dict:
    return _envelope(_load("program_groups", ProgramGroupMeta))


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
