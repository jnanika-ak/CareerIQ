from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import crud
from app.services.job_matcher import (
    JobMatchRequest,
    JobMatchResult,
    JobRequirementProfile,
    match_resume_to_job,
    segment_job_description,
)

router = APIRouter(prefix="/job", tags=["Job Intelligence & Matching"])


class JobAnalyzeRequest(BaseModel):
    job_title: Optional[str] = None
    job_description: str


@router.post(
    "/analyze",
    response_model=JobRequirementProfile,
    status_code=status.HTTP_200_OK,
    summary="Analyze job description and extract requirements",
    description="Extracts required and preferred technical competencies from a raw job description.",
)
async def analyze_job_description(
    request: JobAnalyzeRequest,
    db: Session = Depends(get_db),
):
    if not request.job_description or not request.job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description text cannot be empty.",
        )

    required_skills, preferred_skills, all_skills = segment_job_description(
        request.job_description
    )

    # Persist job analysis safely
    try:
        crud.persist_job_analysis(
            db=db,
            job_description=request.job_description,
            job_title=request.job_title,
        )
    except Exception:
        pass

    return JobRequirementProfile(
        job_title=request.job_title,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        all_skills=all_skills,
    )


@router.post(
    "/match",
    response_model=JobMatchResult,
    status_code=status.HTTP_200_OK,
    summary="Match candidate skills against job description",
    description="Compares candidate profile skills against extracted job requirements, computing match percentage, matched skills, and missing skill gaps.",
)
async def match_job(
    request: JobMatchRequest,
    db: Session = Depends(get_db),
):
    if not request.job_description or not request.job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description text cannot be empty.",
        )

    try:
        result = match_resume_to_job(
            job_description=request.job_description,
            candidate_skills=request.candidate_skills,
            job_title=request.job_title,
        )

        # Persist job match safely
        try:
            crud.persist_job_match(
                db=db,
                job_description=request.job_description,
                match_percentage=result.match_percentage,
                match_strength=result.match_strength,
                matched_skills=result.matched_skills,
                missing_skills=result.missing_skills,
                job_title=request.job_title,
            )
        except Exception:
            pass

        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while matching job requirements: {str(exc)}",
        ) from exc
