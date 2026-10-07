"""
CareerIQ Career Intelligence Route
POST /api/career/analyze
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import crud
from app.services.career_intelligence import (
    CareerAnalysisRequest,
    CareerAnalysisResult,
    perform_career_analysis,
)

router = APIRouter(prefix="/career", tags=["Career Intelligence & Recommendations"])


@router.post(
    "/analyze",
    response_model=CareerAnalysisResult,
    status_code=status.HTTP_200_OK,
    summary="Analyze candidate skill gaps and career role recommendations",
    description="Transforms candidate profile and optional job match data into prioritized skill gaps and ranked career role recommendations.",
)
async def analyze_career(
    request: CareerAnalysisRequest,
    db: Session = Depends(get_db),
):
    """
    Analyzes skill gaps and recommends career pathways.
    Robustly handles empty candidate profiles, missing job match data, or partial structures.
    Persists career analysis and skill gaps safely.
    """
    candidate_profile = request.candidate_profile or {}
    job_match = request.job_match or None

    result = perform_career_analysis(
        candidate_profile=candidate_profile,
        job_match=job_match,
    )

    # Persist career analysis safely
    try:
        strongest = result.strongest_fit_role or (
            result.recommended_roles[0] if result.recommended_roles else None
        )
        if strongest:
            role_name = getattr(strongest, "role", "Recommended Role")
            role_score = getattr(strongest, "match_percentage", 0.0)
            all_gaps = result.skill_gaps or result.top_priority_gaps or []
            gaps_data = [g.model_dump() for g in all_gaps]
            crud.persist_career_analysis(
                db=db,
                strongest_role=role_name,
                strongest_role_score=role_score,
                skill_gaps=gaps_data,
            )
    except Exception as exc:
        pass

    return result
