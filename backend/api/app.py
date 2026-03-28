from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI

from backend.registry.loader import load_registries

REGISTRY_DIR = Path(__file__).resolve().parents[2] / "registries"

app = FastAPI(title="TNTECheck Metadata API", version="0.1.0")


@lru_cache(maxsize=1)
def get_registry_bundle():
    return load_registries(REGISTRY_DIR)


@app.get("/api/meta/sources")
def get_sources():
    return get_registry_bundle().sources


@app.get("/api/meta/docs")
def get_source_docs():
    return get_registry_bundle().source_docs


@app.get("/api/meta/presets")
def get_presets():
    return get_registry_bundle().presets


@app.get("/api/meta/program-groups")
def get_program_groups():
    return get_registry_bundle().program_groups


@app.get("/api/meta/comparison-groups")
def get_comparison_groups():
    return get_registry_bundle().comparison_groups


@app.get("/api/meta/indicators")
def get_indicators():
    return get_registry_bundle().indicators


@app.get("/api/eligibility/profiles")
def get_eligibility_profiles():
    return get_registry_bundle().eligibility_profiles
