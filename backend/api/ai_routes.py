from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from ai.inference import get_inference_engine

router = APIRouter(prefix="/ai", tags=["AI"])


class ClassifyTitleRequest(BaseModel):
    title: str


class DetectDuplicateRequest(BaseModel):
    recordA: Dict[str, Any]
    recordB: Dict[str, Any]


class DetectAnomalyRequest(BaseModel):
    field: str
    value: str


class SuggestFixRequest(BaseModel):
    field_type: str
    value: str


class QualityScoreRequest(BaseModel):
    stats: Dict[str, int]


@router.post("/classify-title")
async def classify_job_title(request: ClassifyTitleRequest):
    return get_inference_engine().classify_job_title(request.title)


@router.post("/detect-duplicate")
async def detect_duplicate(request: DetectDuplicateRequest):
    return get_inference_engine().detect_duplicate_probability(request.recordA, request.recordB)


@router.post("/detect-anomaly")
async def detect_anomaly(request: DetectAnomalyRequest):
    return get_inference_engine().detect_anomaly(request.field, request.value)


@router.post("/suggest-fix")
async def suggest_correction(request: SuggestFixRequest):
    return get_inference_engine().suggest_correction(request.field_type, request.value)


@router.post("/quality-score")
async def compute_quality_score(request: QualityScoreRequest):
    return get_inference_engine().compute_quality_score(request.stats)


@router.get("/health")
async def ai_health_check():
    engine = get_inference_engine()
    return {
        "status": "ok" if engine.models_loaded else "models_not_loaded",
        "models_loaded": engine.models_loaded,
        "available_models": {
            "job_title_classifier": engine.job_title_classifier is not None,
            "duplicate_detector": engine.duplicate_detector is not None,
            "anomaly_detectors": engine.anomaly_detectors is not None,
            "references": list(engine.references.keys()),
        },
    }
