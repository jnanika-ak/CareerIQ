"""
CareerIQ SQLAlchemy Database Models
Step 10: PostgreSQL persistence schema for candidates, resumes, jobs, matches,
skill gaps, career paths, roadmaps, and interview readiness.
"""

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def utc_now() -> datetime:
    """Returns current UTC timestamp with timezone awareness."""
    return datetime.now(timezone.utc)


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    target_role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    # Relationships
    skills: Mapped[List["CandidateSkill"]] = relationship(
        "CandidateSkill", back_populates="candidate", cascade="all, delete-orphan"
    )
    resume_analyses: Mapped[List["ResumeAnalysis"]] = relationship(
        "ResumeAnalysis", back_populates="candidate"
    )
    job_analyses: Mapped[List["JobAnalysis"]] = relationship(
        "JobAnalysis", back_populates="candidate"
    )
    job_matches: Mapped[List["JobMatch"]] = relationship(
        "JobMatch", back_populates="candidate"
    )
    career_analyses: Mapped[List["CareerAnalysis"]] = relationship(
        "CareerAnalysis", back_populates="candidate"
    )
    learning_roadmaps: Mapped[List["LearningRoadmap"]] = relationship(
        "LearningRoadmap", back_populates="candidate"
    )
    interview_readiness_records: Mapped[List["InterviewReadiness"]] = relationship(
        "InterviewReadiness", back_populates="candidate"
    )


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    candidate_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    # Relationship
    candidate: Mapped["Candidate"] = relationship("Candidate", back_populates="skills")


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    candidate_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("candidates.id", ondelete="SET NULL"), nullable=True, index=True
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    extracted_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    # Relationship
    candidate: Mapped[Optional["Candidate"]] = relationship("Candidate", back_populates="resume_analyses")


class JobAnalysis(Base):
    __tablename__ = "job_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    candidate_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("candidates.id", ondelete="SET NULL"), nullable=True, index=True
    )
    job_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    job_description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    # Relationships
    candidate: Mapped[Optional["Candidate"]] = relationship("Candidate", back_populates="job_analyses")
    job_matches: Mapped[List["JobMatch"]] = relationship("JobMatch", back_populates="job_analysis")


class JobMatch(Base):
    __tablename__ = "job_matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    candidate_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("candidates.id", ondelete="SET NULL"), nullable=True, index=True
    )
    job_analysis_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("job_analyses.id", ondelete="SET NULL"), nullable=True, index=True
    )
    match_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    match_strength: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    # Relationships
    candidate: Mapped[Optional["Candidate"]] = relationship("Candidate", back_populates="job_matches")
    job_analysis: Mapped[Optional["JobAnalysis"]] = relationship("JobAnalysis", back_populates="job_matches")
    skills: Mapped[List["JobMatchSkill"]] = relationship(
        "JobMatchSkill", back_populates="job_match", cascade="all, delete-orphan"
    )


class JobMatchSkill(Base):
    __tablename__ = "job_match_skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_match_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("job_matches.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_name: Mapped[str] = mapped_column(String(150), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # "matched" or "missing"
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    # Relationship
    job_match: Mapped["JobMatch"] = relationship("JobMatch", back_populates="skills")


class CareerAnalysis(Base):
    __tablename__ = "career_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    candidate_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("candidates.id", ondelete="SET NULL"), nullable=True, index=True
    )
    strongest_role: Mapped[str] = mapped_column(String(255), nullable=False)
    strongest_role_score: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    # Relationships
    candidate: Mapped[Optional["Candidate"]] = relationship("Candidate", back_populates="career_analyses")
    skill_gaps: Mapped[List["SkillGap"]] = relationship(
        "SkillGap", back_populates="career_analysis", cascade="all, delete-orphan"
    )


class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    career_analysis_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("career_analyses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_name: Mapped[str] = mapped_column(String(150), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False)  # "HIGH", "MEDIUM", "LOW"
    current_level: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    target_level: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    # Relationship
    career_analysis: Mapped["CareerAnalysis"] = relationship("CareerAnalysis", back_populates="skill_gaps")


class LearningRoadmap(Base):
    __tablename__ = "learning_roadmaps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    candidate_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("candidates.id", ondelete="SET NULL"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    total_weeks: Mapped[int] = mapped_column(Integer, default=4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    # Relationships
    candidate: Mapped[Optional["Candidate"]] = relationship("Candidate", back_populates="learning_roadmaps")
    weeks: Mapped[List["RoadmapWeek"]] = relationship(
        "RoadmapWeek", back_populates="roadmap", cascade="all, delete-orphan"
    )


class RoadmapWeek(Base):
    __tablename__ = "roadmap_weeks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    roadmap_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("learning_roadmaps.id", ondelete="CASCADE"), nullable=False, index=True
    )
    week_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    priority: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    hours_per_week: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    # Relationship
    roadmap: Mapped["LearningRoadmap"] = relationship("LearningRoadmap", back_populates="weeks")


class InterviewReadiness(Base):
    __tablename__ = "interview_readiness"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    candidate_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("candidates.id", ondelete="SET NULL"), nullable=True, index=True
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    readiness_level: Mapped[str] = mapped_column(String(100), nullable=False)
    technical_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    role_alignment_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    skill_coverage_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    project_readiness_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    # Relationship
    candidate: Mapped[Optional["Candidate"]] = relationship("Candidate", back_populates="interview_readiness_records")
