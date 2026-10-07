"""
CareerIQ Learning Roadmap & Interview Readiness Route
POST /api/learning-interview/analyze
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import crud
from app.services.learning_interview import (
    LearningInterviewRequest,
    LearningInterviewResult,
    perform_learning_interview_analysis,
)

router = APIRouter(
    prefix="/learning-interview",
    tags=["Learning Roadmap & Interview Readiness"],
)


@router.post(
    "/analyze",
    response_model=LearningInterviewResult,
    status_code=status.HTTP_200_OK,
    summary="Generate personalized learning roadmap and interview readiness score",
    description="Transforms candidate profile, career analysis, and optional job match into a 4-week roadmap, weighted readiness score, and role-specific interview preparation areas.",
)
async def analyze_learning_and_interview(
    request: LearningInterviewRequest,
    db: Session = Depends(get_db),
):
    """
    Robust endpoint that accepts candidate_profile, career_analysis, and optional job_match.
    Persists roadmap and interview readiness records into PostgreSQL.
    """
    candidate_profile = request.candidate_profile or {}
    career_analysis = request.career_analysis or None
    job_match = request.job_match or None

    result = perform_learning_interview_analysis(
        candidate_profile=candidate_profile,
        career_analysis=career_analysis,
        job_match=job_match,
    )

    # Persist learning roadmap & interview readiness safely
    try:
        weeks_data = [w.model_dump() for w in result.learning_roadmap.weeks]
        ir = result.interview_readiness
        crud.persist_learning_interview(
            db=db,
            target_role=result.target_role,
            roadmap_weeks=weeks_data,
            overall_readiness_score=ir.overall_score,
            readiness_level=ir.readiness_level,
            technical_score=ir.technical_skills_score,
            role_alignment_score=ir.role_alignment_score,
            skill_coverage_score=ir.skill_coverage_score,
            project_readiness_score=ir.project_readiness_score,
        )
    except Exception:
        pass

    return result
