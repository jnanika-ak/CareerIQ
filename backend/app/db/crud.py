"""
CareerIQ Persistence & Data Access Layer (CRUD)
Step 10: Persists and queries candidate profiles, resumes, jobs, matches,
career paths, roadmaps, interview readiness, and history.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import logging

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.db.models import (
    Candidate,
    CandidateSkill,
    CareerAnalysis,
    InterviewReadiness,
    JobAnalysis,
    JobMatch,
    JobMatchSkill,
    LearningRoadmap,
    ResumeAnalysis,
    RoadmapWeek,
    SkillGap,
)

logger = logging.getLogger("careeriq.crud")


def get_latest_candidate(db: Session) -> Optional[Candidate]:
    """Retrieves the most recently created or updated candidate record."""
    try:
        stmt = select(Candidate).order_by(desc(Candidate.updated_at)).limit(1)
        return db.execute(stmt).scalars().first()
    except Exception as exc:
        logger.error(f"Error fetching latest candidate: {exc}")
        return None


def get_or_create_candidate(
    db: Session,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    summary: Optional[str] = None,
    target_role: Optional[str] = None,
) -> Candidate:
    """
    Finds an existing candidate by email or name, or creates a new one.
    Updates profile fields if new details are provided.
    """
    candidate: Optional[Candidate] = None

    if email and email.strip():
        candidate = db.execute(
            select(Candidate).where(Candidate.email == email.strip())
        ).scalars().first()

    if not candidate and name and name.strip() and name.strip() != "Candidate":
        candidate = db.execute(
            select(Candidate).where(Candidate.name == name.strip())
        ).scalars().first()

    if not candidate:
        # Check if there is a single unnamed or default candidate to reuse
        candidate = Candidate(
            name=name.strip() if name else "Candidate",
            email=email.strip() if email else None,
            phone=phone.strip() if phone else None,
            summary=summary.strip() if summary else None,
            target_role=target_role.strip() if target_role else None,
        )
        db.add(candidate)
        db.flush()
    else:
        # Update fields if new data present
        if name and name != "Candidate":
            candidate.name = name
        if email:
            candidate.email = email
        if phone:
            candidate.phone = phone
        if summary:
            candidate.summary = summary
        if target_role:
            candidate.target_role = target_role
        candidate.updated_at = datetime.now(timezone.utc)
        db.flush()

    return candidate


def persist_resume_analysis(
    db: Session,
    filename: str,
    file_type: Optional[str],
    extracted_text: Optional[str],
    profile_data: Optional[Dict[str, Any]] = None,
) -> Optional[ResumeAnalysis]:
    """Persists parsed resume text, candidate profile, and candidate skills."""
    try:
        profile_data = profile_data or {}
        name = profile_data.get("name")
        email = profile_data.get("email")
        phone = profile_data.get("phone")
        summary = profile_data.get("summary")

        candidate = get_or_create_candidate(
            db, name=name, email=email, phone=phone, summary=summary
        )

        # Persist resume analysis log
        resume_record = ResumeAnalysis(
            candidate_id=candidate.id,
            filename=filename,
            file_type=file_type,
            extracted_text=extracted_text,
        )
        db.add(resume_record)

        # Persist candidate skills
        raw_skills = profile_data.get("skills", [])
        if isinstance(raw_skills, list) and raw_skills:
            # Clear previous skills for this candidate to prevent duplicates
            existing_skills = {
                cs.skill_name.lower(): cs
                for cs in db.execute(
                    select(CandidateSkill).where(CandidateSkill.candidate_id == candidate.id)
                ).scalars().all()
            }
            for skill in raw_skills:
                skill_str = str(skill).strip()
                if skill_str and skill_str.lower() not in existing_skills:
                    db.add(CandidateSkill(candidate_id=candidate.id, skill_name=skill_str))

        db.commit()
        db.refresh(resume_record)
        return resume_record
    except Exception as exc:
        db.rollback()
        logger.error(f"Failed to persist resume analysis: {exc}")
        return None


def persist_job_analysis(
    db: Session,
    job_description: str,
    job_title: Optional[str] = None,
    candidate_id: Optional[int] = None,
) -> Optional[JobAnalysis]:
    """Persists a job description analysis record."""
    try:
        if not candidate_id:
            latest = get_latest_candidate(db)
            candidate_id = latest.id if latest else None

        record = JobAnalysis(
            candidate_id=candidate_id,
            job_title=job_title,
            job_description=job_description,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except Exception as exc:
        db.rollback()
        logger.error(f"Failed to persist job analysis: {exc}")
        return None


def persist_job_match(
    db: Session,
    job_description: str,
    match_percentage: float,
    match_strength: Optional[str],
    matched_skills: List[str],
    missing_skills: List[str],
    job_title: Optional[str] = None,
    candidate_id: Optional[int] = None,
) -> Optional[JobMatch]:
    """Persists a job match result along with matched and missing skill items."""
    try:
        if not candidate_id:
            latest = get_latest_candidate(db)
            candidate_id = latest.id if latest else None

        # Create or link job analysis
        job_analysis = JobAnalysis(
            candidate_id=candidate_id,
            job_title=job_title,
            job_description=job_description,
        )
        db.add(job_analysis)
        db.flush()

        match_record = JobMatch(
            candidate_id=candidate_id,
            job_analysis_id=job_analysis.id,
            match_percentage=float(match_percentage),
            match_strength=match_strength,
        )
        db.add(match_record)
        db.flush()

        for s in matched_skills:
            if str(s).strip():
                db.add(JobMatchSkill(job_match_id=match_record.id, skill_name=str(s).strip(), status="matched"))

        for s in missing_skills:
            if str(s).strip():
                db.add(JobMatchSkill(job_match_id=match_record.id, skill_name=str(s).strip(), status="missing"))

        db.commit()
        db.refresh(match_record)
        return match_record
    except Exception as exc:
        db.rollback()
        logger.error(f"Failed to persist job match: {exc}")
        return None


def persist_career_analysis(
    db: Session,
    strongest_role: str,
    strongest_role_score: float,
    skill_gaps: List[Dict[str, Any]],
    candidate_id: Optional[int] = None,
) -> Optional[CareerAnalysis]:
    """Persists career role recommendations and identified skill gaps."""
    try:
        candidate: Optional[Candidate] = None
        if candidate_id:
            candidate = db.get(Candidate, candidate_id)
        if not candidate:
            candidate = get_latest_candidate(db)
        if candidate:
            candidate_id = candidate.id
            candidate.target_role = strongest_role

        record = CareerAnalysis(
            candidate_id=candidate_id,
            strongest_role=strongest_role,
            strongest_role_score=float(strongest_role_score),
        )
        db.add(record)
        db.flush()

        for gap in skill_gaps:
            skill_name = gap.get("skill") or gap.get("skill_name")
            if skill_name:
                db.add(
                    SkillGap(
                        career_analysis_id=record.id,
                        skill_name=str(skill_name).strip(),
                        priority=str(gap.get("priority", "MEDIUM")),
                        current_level=gap.get("current_level"),
                        target_level=gap.get("target_level"),
                    )
                )

        db.commit()
        db.refresh(record)
        return record
    except Exception as exc:
        db.rollback()
        logger.error(f"Failed to persist career analysis: {exc}")
        return None


def persist_learning_interview(
    db: Session,
    target_role: str,
    roadmap_weeks: List[Dict[str, Any]],
    overall_readiness_score: int,
    readiness_level: str,
    technical_score: Optional[int] = None,
    role_alignment_score: Optional[int] = None,
    skill_coverage_score: Optional[int] = None,
    project_readiness_score: Optional[int] = None,
    candidate_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Persists a 4-week learning roadmap and weighted interview readiness score."""
    result = {"roadmap_id": None, "readiness_id": None}
    try:
        if not candidate_id:
            latest = get_latest_candidate(db)
            candidate_id = latest.id if latest else None

        # 1. Persist Roadmap
        roadmap_record = LearningRoadmap(
            candidate_id=candidate_id,
            title=f"{target_role} Learning Roadmap",
            total_weeks=len(roadmap_weeks) if roadmap_weeks else 4,
        )
        db.add(roadmap_record)
        db.flush()

        for w in roadmap_weeks:
            db.add(
                RoadmapWeek(
                    roadmap_id=roadmap_record.id,
                    week_number=int(w.get("week_number", 1)),
                    title=str(w.get("title", f"Week {w.get('week_number', 1)}")),
                    priority=w.get("priority"),
                    hours_per_week=w.get("estimated_hours"),
                    status=w.get("status"),
                )
            )

        # 2. Persist Interview Readiness
        readiness_record = InterviewReadiness(
            candidate_id=candidate_id,
            score=int(overall_readiness_score),
            readiness_level=readiness_level,
            technical_score=technical_score,
            role_alignment_score=role_alignment_score,
            skill_coverage_score=skill_coverage_score,
            project_readiness_score=project_readiness_score,
        )
        db.add(readiness_record)

        db.commit()
        db.refresh(roadmap_record)
        db.refresh(readiness_record)

        result["roadmap_id"] = roadmap_record.id
        result["readiness_id"] = readiness_record.id
        return result
    except Exception as exc:
        db.rollback()
        logger.error(f"Failed to persist learning & interview analysis: {exc}")
        return result


def get_recent_history(db: Session, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Returns unified chronological activity timeline stored in PostgreSQL.
    Sorted newest first.
    """
    timeline: List[Dict[str, Any]] = []

    try:
        # 1. Resume Analyses
        resumes = db.execute(
            select(ResumeAnalysis).order_by(desc(ResumeAnalysis.created_at)).limit(limit)
        ).scalars().all()
        for r in resumes:
            candidate_name = r.candidate.name if r.candidate and r.candidate.name else "Candidate"
            timeline.append({
                "id": f"resume-{r.id}",
                "activity_type": "resume_analysis",
                "action": f"Resume analyzed: {r.filename}",
                "detail": f"Profile extracted for {candidate_name} ({r.file_type or 'PDF/DOCX'})",
                "timestamp": r.created_at.isoformat() if r.created_at else None,
                "score": None,
                "created_at_dt": r.created_at,
            })

        # 2. Job Analyses
        jobs = db.execute(
            select(JobAnalysis).order_by(desc(JobAnalysis.created_at)).limit(limit)
        ).scalars().all()
        for j in jobs:
            title = j.job_title or "Job Description"
            timeline.append({
                "id": f"job-{j.id}",
                "activity_type": "job_analysis",
                "action": f"Job analyzed: {title}",
                "detail": f"Extracted competency requirements & prerequisites",
                "timestamp": j.created_at.isoformat() if j.created_at else None,
                "score": None,
                "created_at_dt": j.created_at,
            })

        # 3. Job Matches
        matches = db.execute(
            select(JobMatch).order_by(desc(JobMatch.created_at)).limit(limit)
        ).scalars().all()
        for m in matches:
            role_title = m.job_analysis.job_title if m.job_analysis and m.job_analysis.job_title else "Target Job"
            timeline.append({
                "id": f"match-{m.id}",
                "activity_type": "job_match",
                "action": f"Job matched: {role_title}",
                "detail": f"Computed {m.match_percentage:.0f}% match ({m.match_strength or 'Evaluated'})",
                "timestamp": m.created_at.isoformat() if m.created_at else None,
                "score": round(m.match_percentage, 1),
                "created_at_dt": m.created_at,
            })

        # 4. Career Analyses
        careers = db.execute(
            select(CareerAnalysis).order_by(desc(CareerAnalysis.created_at)).limit(limit)
        ).scalars().all()
        for c in careers:
            timeline.append({
                "id": f"career-{c.id}",
                "activity_type": "career_analysis",
                "action": f"Career path analyzed: {c.strongest_role}",
                "detail": f"Role compatibility scored at {c.strongest_role_score:.0f}% with skill gaps identified",
                "timestamp": c.created_at.isoformat() if c.created_at else None,
                "score": round(c.strongest_role_score, 1),
                "created_at_dt": c.created_at,
            })

        # 5. Learning Roadmaps
        roadmaps = db.execute(
            select(LearningRoadmap).order_by(desc(LearningRoadmap.created_at)).limit(limit)
        ).scalars().all()
        for rm in roadmaps:
            timeline.append({
                "id": f"roadmap-{rm.id}",
                "activity_type": "learning_roadmap",
                "action": f"Roadmap generated: {rm.title}",
                "detail": f"{rm.total_weeks}-week curriculum tailored to bridge priority skill gaps",
                "timestamp": rm.created_at.isoformat() if rm.created_at else None,
                "score": None,
                "created_at_dt": rm.created_at,
            })

        # 6. Interview Readiness
        readiness_items = db.execute(
            select(InterviewReadiness).order_by(desc(InterviewReadiness.created_at)).limit(limit)
        ).scalars().all()
        for ir in readiness_items:
            timeline.append({
                "id": f"readiness-{ir.id}",
                "activity_type": "interview_readiness",
                "action": f"Interview readiness: {ir.readiness_level}",
                "detail": f"Weighted evaluation score of {ir.score}/100",
                "timestamp": ir.created_at.isoformat() if ir.created_at else None,
                "score": ir.score,
                "created_at_dt": ir.created_at,
            })

        # Sort combined timeline by created_at_dt newest first
        timeline.sort(
            key=lambda x: x["created_at_dt"] or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )

        # Remove internal datetime object before returning JSON
        result = []
        for item in timeline[:limit]:
            clean_item = dict(item)
            clean_item.pop("created_at_dt", None)
            result.append(clean_item)

        return result
    except Exception as exc:
        logger.error(f"Error querying history timeline: {exc}")
        return []


def get_history_summary(db: Session) -> Dict[str, Any]:
    """
    Computes aggregated summary statistics across all persisted tables.
    """
    try:
        total_resumes = db.scalar(select(func.count(ResumeAnalysis.id))) or 0
        total_jobs = db.scalar(select(func.count(JobAnalysis.id))) or 0
        total_matches = db.scalar(select(func.count(JobMatch.id))) or 0
        avg_match = db.scalar(select(func.avg(JobMatch.match_percentage))) or 0.0
        total_careers = db.scalar(select(func.count(CareerAnalysis.id))) or 0
        total_gaps = db.scalar(select(func.count(SkillGap.id))) or 0

        latest_readiness_record = db.execute(
            select(InterviewReadiness).order_by(desc(InterviewReadiness.created_at)).limit(1)
        ).scalars().first()

        latest_readiness_score = (
            latest_readiness_record.score if latest_readiness_record else None
        )
        latest_readiness_level = (
            latest_readiness_record.readiness_level if latest_readiness_record else None
        )

        return {
            "total_resume_analyses": int(total_resumes),
            "total_job_analyses": int(total_jobs),
            "total_job_matches": int(total_matches),
            "average_match_score": round(float(avg_match), 1),
            "total_career_analyses": int(total_careers),
            "total_skill_gaps": int(total_gaps),
            "latest_interview_readiness_score": latest_readiness_score,
            "latest_interview_readiness_level": latest_readiness_level,
        }
    except Exception as exc:
        logger.error(f"Error computing history summary: {exc}")
        return {
            "total_resume_analyses": 0,
            "total_job_analyses": 0,
            "total_job_matches": 0,
            "average_match_score": 0.0,
            "total_career_analyses": 0,
            "total_skill_gaps": 0,
            "latest_interview_readiness_score": None,
            "latest_interview_readiness_level": None,
        }
