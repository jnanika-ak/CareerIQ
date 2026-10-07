"""
CareerIQ History & Analytics Routes
Step 10: GET /api/history and GET /api/history/summary
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db, check_database_connection
from app.db import crud

router = APIRouter(prefix="/history", tags=["History & Analytics"])


@router.get(
    "",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Get recent CareerIQ activity history",
    description="Returns a chronological list of recent automated actions and evaluations stored in PostgreSQL.",
)
def get_activity_history(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Returns recent CareerIQ activity stored in PostgreSQL.
    If database is unavailable, gracefully returns empty list without error.
    """
    is_connected, _ = check_database_connection()
    if not is_connected:
        return []

    return crud.get_recent_history(db=db, limit=limit)


@router.get(
    "/summary",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get aggregated CareerIQ metrics summary",
    description="Returns aggregated metrics across resume analyses, job matches, career analyses, and readiness scores.",
)
def get_metrics_summary(db: Session = Depends(get_db)):
    """
    Returns useful persisted metrics such as:
    - total resume analyses
    - total job analyses
    - total job matches
    - average match score
    - total career analyses
    - total skill gaps
    - latest interview readiness score
    """
    is_connected, _ = check_database_connection()
    if not is_connected:
        return {
            "total_resume_analyses": 0,
            "total_job_analyses": 0,
            "total_job_matches": 0,
            "average_match_score": 0.0,
            "total_career_analyses": 0,
            "total_skill_gaps": 0,
            "latest_interview_readiness_score": None,
            "latest_interview_readiness_level": None,
            "database_connected": False,
        }

    summary = crud.get_history_summary(db=db)
    summary["database_connected"] = True
    return summary
