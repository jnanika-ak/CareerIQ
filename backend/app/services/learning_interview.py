"""
CareerIQ Learning Roadmap & Interview Readiness Service
Step 9: Generates a 4-week personalized learning roadmap, interview readiness score,
and role-specific preparation areas based on candidate profile and career intelligence.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field

from app.services.career_intelligence import (
    CURATED_ROLES,
    SkillGap,
    CareerRole,
    perform_career_analysis,
)
from app.services.job_matcher import normalize_skill, get_canonical_display


# ==============================================================================
# Pydantic Schemas
# ==============================================================================

class RoadmapWeek(BaseModel):
    week_number: int
    title: str
    skills: List[str] = Field(default_factory=list)
    objective: str
    activities: List[str] = Field(default_factory=list)
    priority: str  # "HIGH", "MEDIUM", "LOW"
    estimated_hours: str  # e.g., "6–8 hours"
    status: str  # "Current" or "Upcoming"


class LearningRoadmap(BaseModel):
    target_role: str
    target_role_match_percentage: int
    total_weeks: int = 4
    weeks: List[RoadmapWeek] = Field(default_factory=list)
    summary: str


class InterviewReadinessComponent(BaseModel):
    name: str
    score: int  # 0 to 100
    weight: float
    description: str


class InterviewArea(BaseModel):
    area: str
    priority: str  # "HIGH", "MEDIUM", "LOW"
    is_gap: bool
    description: str


class InterviewReadiness(BaseModel):
    overall_score: int
    readiness_level: str  # "Interview Ready", "Strong Preparation", "Needs Preparation", "Early Preparation", "Not Ready Yet"
    target_role: str
    technical_skills_score: int
    role_alignment_score: int
    skill_coverage_score: int
    project_readiness_score: int
    components: List[InterviewReadinessComponent] = Field(default_factory=list)
    preparation_areas: List[InterviewArea] = Field(default_factory=list)
    project_readiness_note: str


class LearningInterviewRequest(BaseModel):
    candidate_profile: Optional[Dict[str, Any]] = None
    career_analysis: Optional[Dict[str, Any]] = None
    job_match: Optional[Dict[str, Any]] = None


class LearningInterviewResult(BaseModel):
    learning_roadmap: LearningRoadmap
    interview_readiness: InterviewReadiness
    target_role: str
    candidate_name: str


# ==============================================================================
# Curated Skill Roadmap Templates
# Concrete, realistic objectives and beginner-to-intermediate activities
# ==============================================================================

SKILL_ROADMAP_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "statistics": {
        "title": "Statistics Fundamentals",
        "objective": "Build a rigorous foundation in descriptive and inferential statistics for data-driven decisions.",
        "activities": [
            "Mean, median, variance, and standard deviation distributions",
            "Probability fundamentals and common statistical distributions",
            "Hypothesis testing (p-values, null hypothesis, t-tests, z-tests)",
            "Correlation, covariance, and simple linear regression models",
        ],
        "estimated_hours": "6–8 hours",
    },
    "tableau": {
        "title": "Tableau Visual Analytics",
        "objective": "Master interactive dashboard creation, calculated fields, and visual data storytelling.",
        "activities": [
            "Connecting diverse data sources and relationship modeling",
            "Building essential charts: bars, lines, scatter plots, and dual-axis charts",
            "Calculated fields, LOD expressions, and interactive parameters",
            "Designing cohesive executive dashboards with dynamic actions and filters",
        ],
        "estimated_hours": "5–7 hours",
    },
    "power bi": {
        "title": "Power BI & DAX Reporting",
        "objective": "Develop automated business intelligence reporting models and custom DAX calculations.",
        "activities": [
            "Data ingestion and automated transformation in Power Query",
            "Star schema dimensional data modeling and relationship management",
            "DAX measures: CALCULATE, SUMX, RELATED, and Time Intelligence",
            "Publishing interactive workspaces and configuring custom slicers",
        ],
        "estimated_hours": "6–8 hours",
    },
    "sql": {
        "title": "Advanced SQL & Analytical Queries",
        "objective": "Strengthen relational querying, window functions, and data aggregation for analytics.",
        "activities": [
            "Multi-table INNER, LEFT, and FULL joins with index awareness",
            "Window functions: ROW_NUMBER, RANK, DENSE_RANK, LAG, and LEAD",
            "Common Table Expressions (CTEs), subqueries, and temporary tables",
            "Complex aggregations, GROUP BY GROUPING SETS, and query plan optimization",
        ],
        "estimated_hours": "6–8 hours",
    },
    "data visualization": {
        "title": "Data Visualization & Dashboard Architecture",
        "objective": "Apply cognitive visual encoding principles to communicate complex data narratives clearly.",
        "activities": [
            "Visual perception principles: color theory, chart hierarchy, and decluttering",
            "Designing KPI summary cards and comparative benchmark displays",
            "Building interactive drill-down workflows and contextual tooltips",
            "Conducting an end-to-end dashboard usability and accessibility review",
        ],
        "estimated_hours": "5–7 hours",
    },
    "python": {
        "title": "Python for Data & Scripting",
        "objective": "Deepen Python fundamentals, data structures, and automation scripting.",
        "activities": [
            "Core data structures: lists, dicts, sets, and list comprehensions",
            "Modular functions, error handling, and robust file I/O operations",
            "Virtual environments, dependency management, and script automation",
            "Building end-to-end data processing pipelines with clean code principles",
        ],
        "estimated_hours": "6–8 hours",
    },
    "pandas": {
        "title": "Data Manipulation with Pandas & NumPy",
        "objective": "Efficiently clean, reshape, filter, and transform analytical dataframes.",
        "activities": [
            "DataFrame indexing, slicing, and conditional filtering with .loc and .iloc",
            "Handling missing values, outlier imputation, and type coercions",
            "Groupby aggregations, multi-level indexing, and pivot tables",
            "Vectorized array computations and matrix transformations with NumPy",
        ],
        "estimated_hours": "6–8 hours",
    },
    "data analysis": {
        "title": "Exploratory Data Analysis & Business Synthesis",
        "objective": "Conduct structured exploratory data analysis to discover trends, anomalies, and insights.",
        "activities": [
            "Formulating business hypotheses and defining success metrics",
            "Exploratory profiling, distribution checks, and feature correlation",
            "Cohort analysis, trend decomposition, and segment comparisons",
            "Synthesizing quantitative findings into an actionable executive brief",
        ],
        "estimated_hours": "6–8 hours",
    },
    "excel": {
        "title": "Advanced Excel & Financial Modeling",
        "objective": "Leverage advanced lookup functions, pivot tables, and financial modeling best practices.",
        "activities": [
            "XLOOKUP, INDEX-MATCH, and dynamic array formulas (FILTER, UNIQUE)",
            "Building multi-dimensional Pivot Tables and slicer-driven dashboards",
            "What-If analysis using Data Tables, Scenario Manager, and Goal Seek",
            "Validating formulas, auditing precedents/dependents, and error checks",
        ],
        "estimated_hours": "5–7 hours",
    },
    "machine learning": {
        "title": "Machine Learning Foundations",
        "objective": "Understand supervised learning algorithms, evaluation metrics, and validation techniques.",
        "activities": [
            "Feature scaling, categorical encoding, and stratified train-test splits",
            "Linear and logistic regression, decision trees, and ensemble forests",
            "Model evaluation: Precision, Recall, F1-Score, ROC-AUC, and Confusion Matrix",
            "Hyperparameter tuning with GridSearchCV and cross-validation pipelines",
        ],
        "estimated_hours": "8–10 hours",
    },
    "scikit-learn": {
        "title": "Applied Scikit-Learn Pipelines",
        "objective": "Build production-ready machine learning pipelines and transformer workflows.",
        "activities": [
            "Constructing ColumnTransformers for heterogeneous datasets",
            "Chaining preprocessing and estimators using sklearn Pipeline",
            "Custom transformers and feature selection techniques",
            "Model serialization with Joblib and inference latency benchmarks",
        ],
        "estimated_hours": "6–8 hours",
    },
    "docker": {
        "title": "Containerization with Docker",
        "objective": "Package applications and analytical pipelines into reproducible container environments.",
        "activities": [
            "Authoring multi-stage Dockerfiles and optimizing image layers",
            "Building, tagging, and running isolated containers locally",
            "Volume bindings, container networking, and environment configuration",
            "Orchestrating multi-service local environments with Docker Compose",
        ],
        "estimated_hours": "5–7 hours",
    },
    "fastapi": {
        "title": "FastAPI REST API Architecture",
        "objective": "Build high-performance asynchronous RESTful APIs with strict Pydantic validation.",
        "activities": [
            "Designing routing structures, path parameters, and query parameters",
            "Pydantic data validation, response serialization, and error handlers",
            "Dependency injection patterns for authentication and persistence",
            "Testing API endpoints with pytest and interactive Swagger/OpenAPI docs",
        ],
        "estimated_hours": "6–8 hours",
    },
    "postgresql": {
        "title": "PostgreSQL Architecture & Indexing",
        "objective": "Model relational database schemas, transactions, and query performance.",
        "activities": [
            "Schema normalization, constraints, and foreign key cascades",
            "ACID transactions, isolation levels, and concurrency locking",
            "B-Tree and GIN indexing strategies for high-throughput queries",
            "Analyzing slow queries with EXPLAIN ANALYZE and query rewrites",
        ],
        "estimated_hours": "5–7 hours",
    },
    "git": {
        "title": "Version Control & Team Git Workflows",
        "objective": "Master branching strategies, collaborative workflows, and code hygiene.",
        "activities": [
            "Branching models (Git Flow/Trunk-based), rebasing, and merge resolution",
            "Atomic commits, conventional commit syntax, and interactive rebase",
            "Pull request code reviews and collaborative Git best practices",
            "Tagging releases and managing remote repository configurations",
        ],
        "estimated_hours": "4–6 hours",
    },
    "react": {
        "title": "Modern React & Component Design",
        "objective": "Build modular, component-driven user interfaces with clean state flows.",
        "activities": [
            "Component hierarchy design, props contracts, and JSX composition",
            "State and side effect management with useState and useEffect",
            "Authoring reusable custom hooks and UI component libraries",
            "Integrating REST APIs, handling loading spinners, and error boundaries",
        ],
        "estimated_hours": "7–9 hours",
    },
    "node.js": {
        "title": "Node.js & Backend Runtime",
        "objective": "Develop asynchronous server applications and middleware pipelines.",
        "activities": [
            "Event loop architecture, non-blocking I/O, and asynchronous patterns",
            "Building REST endpoints with Express or native HTTP modules",
            "Environment variables, configuration loading, and logging",
            "Database connections and asynchronous connection pooling",
        ],
        "estimated_hours": "6–8 hours",
    },
    "etl": {
        "title": "ETL & Data Pipeline Engineering",
        "objective": "Design robust Extract, Transform, and Load pipelines with automated data checks.",
        "activities": [
            "Extracting data from REST APIs, CSVs, and relational databases",
            "Transformation rules, schema validation, and deduplication",
            "Incremental loading strategies and idempotency patterns",
            "Automated logging, error alerting, and pipeline failure recovery",
        ],
        "estimated_hours": "6–8 hours",
    },
}


# ==============================================================================
# Role-Specific Interview Preparation Categories
# ==============================================================================

ROLE_INTERVIEW_PREPARATION_AREAS: Dict[str, List[str]] = {
    "Data Analyst": [
        "SQL Query Optimization & Joins",
        "Python Data Analysis & Pandas",
        "Statistics & Hypothesis Testing",
        "Data Visualization & Storytelling",
        "Power BI & Tableau Reporting",
        "Business Metrics & Stakeholder Communication",
        "Analytical Case Studies & Projects",
    ],
    "BI Analyst": [
        "SQL & Data Modeling",
        "Power BI & DAX Calculations",
        "Excel & Financial Functions",
        "Data Visualization & UX",
        "Statistics & KPI Tracking",
        "Executive Dashboard Walkthroughs",
    ],
    "Business Analyst": [
        "Excel & Data Manipulation",
        "SQL for Business Queries",
        "Requirements Elicitation & User Stories",
        "Data Analysis & Process Mapping",
        "Business Communication & Case Interviews",
        "Stakeholder Alignment & Prioritization",
    ],
    "Junior Data Scientist": [
        "Python & Vectorized Computing",
        "Applied Statistics & Probability",
        "Machine Learning Algorithms & Intuition",
        "Data Preprocessing & Feature Engineering",
        "Model Evaluation Metrics & Bias-Variance",
        "End-to-End Data Science Project Walkthrough",
    ],
    "Data Engineer": [
        "Advanced SQL & Schema Normalization",
        "Python Data Pipeline Scripting",
        "ETL Design, Orchestration & Batch Processing",
        "PostgreSQL & Database Performance Tuning",
        "Docker Containerization & Environments",
        "Data Modeling (Star/Snowflake Schemas)",
    ],
    "ML Engineer": [
        "Python & Object-Oriented ML Architecture",
        "Machine Learning & Deep Learning Theory",
        "PyTorch / TensorFlow Model Development",
        "Docker & Containerized Model Serving",
        "ML Pipeline Validation & Testing",
        "Production Inference & Latency Optimization",
    ],
    "Python Developer": [
        "Python Core, Data Structures & Concurrency",
        "FastAPI & RESTful Web Service Design",
        "Database Persistence & SQL ORMs",
        "Git Collaboration & Code Review Standards",
        "Docker Containerization",
        "Unit Testing & Error Handling",
    ],
    "Backend Developer": [
        "Server-Side Architecture & REST APIs",
        "Relational Databases (PostgreSQL) & Indexing",
        "Python / Node.js Performance & Asynchrony",
        "Docker & Microservice Deployment",
        "Authentication & Security Fundamentals",
        "System Architecture & API Design Scenarios",
    ],
    "Full-Stack Developer": [
        "Frontend Engineering with React & Modern JavaScript",
        "Backend Architecture with Python / Node.js",
        "REST API Contract Design & Integration",
        "State Management & Component Lifecycle",
        "Database Schema Design & Querying",
        "Version Control, CI/CD & Production Builds",
    ],
}


# ==============================================================================
# Helper Functions
# ==============================================================================

def get_readiness_level(overall_score: int) -> str:
    """
    Classifies interview readiness score into transparent levels:
    90–100: Interview Ready
    75–89:  Strong Preparation
    60–74:  Needs Preparation
    40–59:  Early Preparation
    0–39:   Not Ready Yet
    """
    if overall_score >= 90:
        return "Interview Ready"
    elif overall_score >= 75:
        return "Strong Preparation"
    elif overall_score >= 60:
        return "Needs Preparation"
    elif overall_score >= 40:
        return "Early Preparation"
    else:
        return "Not Ready Yet"


def extract_priority_ordered_gaps(
    career_analysis: Optional[Dict[str, Any]],
    job_match: Optional[Dict[str, Any]],
    target_role: str,
    normalized_candidate_skills: Set[str],
) -> List[Tuple[str, str]]:
    """
    Returns an ordered list of (skill_name, priority) tuples.
    Priority order: HIGH -> MEDIUM -> LOW
    """
    ordered_gaps: List[Tuple[str, str]] = []
    seen_normalized: Set[str] = set()

    # 1. From Career Analysis skill_gaps if available
    if career_analysis and isinstance(career_analysis, dict):
        gaps_list = career_analysis.get("skill_gaps", [])
        if isinstance(gaps_list, list):
            for item in gaps_list:
                if isinstance(item, dict):
                    skill = item.get("skill", "")
                    priority = item.get("priority", "LOW")
                elif hasattr(item, "skill"):
                    skill = item.skill
                    priority = getattr(item, "priority", "LOW")
                else:
                    continue

                norm = normalize_skill(skill)
                if norm and norm not in seen_normalized and norm not in normalized_candidate_skills:
                    seen_normalized.add(norm)
                    ordered_gaps.append((get_canonical_display(skill), priority))

    # 2. From job_match if available and not yet included
    if job_match and isinstance(job_match, dict):
        missing_req = job_match.get("missing_skills", [])
        if isinstance(missing_req, list):
            for skill in missing_req:
                norm = normalize_skill(skill)
                if norm and norm not in seen_normalized and norm not in normalized_candidate_skills:
                    seen_normalized.add(norm)
                    ordered_gaps.append((get_canonical_display(skill), "HIGH"))

        missing_pref = job_match.get("missing_preferred_skills", [])
        if isinstance(missing_pref, list):
            for skill in missing_pref:
                norm = normalize_skill(skill)
                if norm and norm not in seen_normalized and norm not in normalized_candidate_skills:
                    seen_normalized.add(norm)
                    ordered_gaps.append((get_canonical_display(skill), "MEDIUM"))

    # 3. If still fewer than 4 gaps, check target role missing skills
    role_def = next((r for r in CURATED_ROLES if r["role"].lower() == target_role.lower()), None)
    if role_def:
        for skill in role_def["skills"]:
            norm = normalize_skill(skill)
            if norm and norm not in seen_normalized and norm not in normalized_candidate_skills:
                seen_normalized.add(norm)
                ordered_gaps.append((get_canonical_display(skill), "MEDIUM"))

    # Sort so HIGH comes first, then MEDIUM, then LOW
    p_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    ordered_gaps.sort(key=lambda x: p_rank.get(x[1], 3))
    return ordered_gaps


def build_roadmap_week(
    week_num: int,
    skill_name: str,
    priority: str,
    target_role: str,
    status: str,
) -> RoadmapWeek:
    """
    Constructs a detailed, beginner-friendly RoadmapWeek object for a given skill.
    """
    norm = normalize_skill(skill_name)
    template = SKILL_ROADMAP_TEMPLATES.get(norm)

    if template:
        return RoadmapWeek(
            week_number=week_num,
            title=template["title"],
            skills=[skill_name],
            objective=template["objective"],
            activities=template["activities"],
            priority=priority,
            estimated_hours=template["estimated_hours"],
            status=status,
        )

    # Clean generic fallback if skill template is not explicitly in catalog
    return RoadmapWeek(
        week_number=week_num,
        title=f"{skill_name} Fundamentals",
        skills=[skill_name],
        objective=f"Develop practical competency and confidence in {skill_name} for the {target_role} role.",
        activities=[
            f"Core conceptual foundations and syntax of {skill_name}",
            f"Practical exercises and common analytical patterns with {skill_name}",
            f"Integration of {skill_name} into existing workflows and tools",
            f"Hands-on mini-project demonstrating {skill_name} problem-solving",
        ],
        priority=priority,
        estimated_hours="6–8 hours",
        status=status,
    )


# ==============================================================================
# Core Service Logic
# ==============================================================================

def generate_learning_roadmap(
    candidate_skills: List[str],
    normalized_candidate_skills: Set[str],
    target_role: str,
    target_role_match_pct: int,
    ordered_gaps: List[Tuple[str, str]],
) -> LearningRoadmap:
    """
    Constructs a strict 4-week structured roadmap prioritizing HIGH -> MEDIUM -> LOW gaps.
    Fills remaining weeks with portfolio synthesis / reinforcement if fewer than 4 gaps exist.
    """
    weeks: List[RoadmapWeek] = []

    # Map available gaps into weeks
    gap_idx = 0
    for w in range(1, 5):
        status = "Current" if w == 1 else "Upcoming"

        if gap_idx < len(ordered_gaps):
            skill, priority = ordered_gaps[gap_idx]
            week_obj = build_roadmap_week(
                week_num=w,
                skill_name=skill,
                priority=priority,
                target_role=target_role,
                status=status,
            )
            weeks.append(week_obj)
            gap_idx += 1
        elif w == 4:
            # Final Week 4 Capstone / Portfolio Synthesis
            weeks.append(
                RoadmapWeek(
                    week_number=4,
                    title=f"{target_role} Portfolio Synthesis",
                    skills=[g[0] for g in ordered_gaps[:3]] if ordered_gaps else ["Portfolio Project"],
                    objective=f"Synthesize newly acquired competencies into an end-to-end portfolio project demonstrating {target_role} readiness.",
                    activities=[
                        f"Define an end-to-end business problem statement aligned with {target_role}",
                        "Implement solution pipeline incorporating newly learned tools and best practices",
                        "Document architecture, methodology, and metrics in a clean GitHub README",
                        "Prepare a 5-minute technical walkthrough presentation for interview discussions",
                    ],
                    priority="MEDIUM",
                    estimated_hours="8–10 hours",
                    status=status,
                )
            )
        else:
            # Core Reinforcement for intermediate week
            role_def = next((r for r in CURATED_ROLES if r["role"].lower() == target_role.lower()), None)
            anchor_skills = role_def["skills"][:2] if role_def else ["Core Competencies"]
            anchor_title = " & ".join(anchor_skills)
            weeks.append(
                RoadmapWeek(
                    week_number=w,
                    title=f"Advanced {anchor_title} Application",
                    skills=anchor_skills,
                    objective=f"Deepen mastery of core {target_role} tools through advanced scenarios and edge cases.",
                    activities=[
                        f"Complex analytical workflows utilizing {anchor_title}",
                        "Performance profiling and refactoring query/code efficiency",
                        "Handling messy, unstructured, and missing data scenarios",
                        "Creating automated testing and validation assertions",
                    ],
                    priority="LOW",
                    estimated_hours="6–8 hours",
                    status=status,
                )
            )

    summary_text = (
        f"A targeted 4-week progression designed to close high-priority skill gaps and "
        f"maximize compatibility for {target_role}."
    )

    return LearningRoadmap(
        target_role=target_role,
        target_role_match_percentage=target_role_match_pct,
        total_weeks=4,
        weeks=weeks,
        summary=summary_text,
    )


def calculate_interview_readiness(
    candidate_profile: Optional[Dict[str, Any]],
    target_role: str,
    target_role_match_pct: int,
    normalized_candidate_skills: Set[str],
    job_match: Optional[Dict[str, Any]],
    ordered_gaps: List[Tuple[str, str]],
) -> InterviewReadiness:
    """
    Computes an interview readiness score using transparent weighted components:
    1. Technical Skills (30%): percentage of target role skills present
    2. Role Alignment (30%): strongest career role match percentage
    3. Skill Coverage (25%): job match percentage if job present, else role coverage
    4. Project Readiness (15%): conservative profile-based project & experience indicator

    Overall Formula:
    round(technical * 0.30 + role_alignment * 0.30 + skill_coverage * 0.25 + project_readiness * 0.15)
    """
    # 1. Technical Skills Score (30%)
    role_def = next((r for r in CURATED_ROLES if r["role"].lower() == target_role.lower()), None)
    if role_def and len(role_def["skills"]) > 0:
        matched_role_skills = [
            s for s in role_def["skills"] if normalize_skill(s) in normalized_candidate_skills
        ]
        technical_skills_score = round((len(matched_role_skills) / len(role_def["skills"])) * 100)
    else:
        technical_skills_score = target_role_match_pct

    # 2. Role Alignment Score (30%)
    role_alignment_score = max(0, min(100, target_role_match_pct))

    # 3. Skill Coverage Score (25%)
    if job_match and isinstance(job_match, dict) and "match_percentage" in job_match:
        skill_coverage_score = max(0, min(100, int(job_match["match_percentage"])))
    else:
        skill_coverage_score = technical_skills_score

    # 4. Project Readiness Score (15%) - conservative, based strictly on profile data
    profile = candidate_profile or {}
    projects = profile.get("projects", [])
    experience = profile.get("experience", [])
    num_projects = len(projects) if isinstance(projects, list) else 0
    num_exp = len(experience) if isinstance(experience, list) else 0

    if num_projects >= 2 and num_exp >= 1:
        project_readiness_score = 85
        project_readiness_note = f"Verified: {num_projects} portfolio projects and {num_exp} professional experience entry."
    elif num_projects >= 2:
        project_readiness_score = 80
        project_readiness_note = f"Verified: {num_projects} relevant projects in candidate profile."
    elif num_projects == 1 and num_exp >= 1:
        project_readiness_score = 75
        project_readiness_note = "Verified: 1 project and professional experience listed."
    elif num_projects == 1:
        project_readiness_score = 65
        project_readiness_note = "Verified: 1 portfolio project listed in candidate profile."
    elif num_exp >= 1:
        project_readiness_score = 60
        project_readiness_note = f"Work experience present ({num_exp} entries), but dedicated project links not specified."
    elif len(normalized_candidate_skills) > 0:
        project_readiness_score = 30
        project_readiness_note = "No project portfolio or experience records found in profile."
    else:
        project_readiness_score = 0
        project_readiness_note = "No projects or candidate profile skills available."

    # Weighted Overall Calculation:
    # technical * 0.30 + role_alignment * 0.30 + skill_coverage * 0.25 + project_readiness * 0.15
    weighted_calc = (
        (technical_skills_score * 0.30)
        + (role_alignment_score * 0.30)
        + (skill_coverage_score * 0.25)
        + (project_readiness_score * 0.15)
    )
    overall_score = round(weighted_calc)
    overall_score = max(0, min(100, overall_score))
    readiness_level = get_readiness_level(overall_score)

    components = [
        InterviewReadinessComponent(
            name="Technical Skills",
            score=technical_skills_score,
            weight=0.30,
            description="Percentage of core technical competencies present in your candidate profile.",
        ),
        InterviewReadinessComponent(
            name="Role Alignment",
            score=role_alignment_score,
            weight=0.30,
            description=f"Compatibility match percentage for your primary career pathway ({target_role}).",
        ),
        InterviewReadinessComponent(
            name="Skill Coverage",
            score=skill_coverage_score,
            weight=0.25,
            description="Coverage of target job description requirements and prerequisite standards.",
        ),
        InterviewReadinessComponent(
            name="Project Readiness",
            score=project_readiness_score,
            weight=0.15,
            description="Verified hands-on portfolio projects and practical work experience in candidate profile.",
        ),
    ]

    # Generate Role-Specific Interview Preparation Areas
    curated_areas = ROLE_INTERVIEW_PREPARATION_AREAS.get(
        target_role,
        [
            "Core Programming & Problem Solving",
            "Data Modeling & Querying",
            "Domain Knowledge & Best Practices",
            "System Design & Architecture",
            "Behavioral & Project Case Studies",
        ],
    )

    gap_normalized_set = {normalize_skill(g[0]) for g in ordered_gaps}
    prep_areas: List[InterviewArea] = []

    for area_title in curated_areas:
        # Check if this area corresponds to an identified gap
        area_norm = normalize_skill(area_title)
        is_identified_gap = False
        gap_priority = "LOW"

        for gap_skill, p in ordered_gaps:
            if normalize_skill(gap_skill) in area_norm or area_norm in normalize_skill(gap_skill):
                is_identified_gap = True
                gap_priority = p
                break

        if is_identified_gap:
            prep_areas.append(
                InterviewArea(
                    area=area_title,
                    priority=gap_priority,
                    is_gap=True,
                    description=f"Identified competency gap for {target_role}. Prioritize conceptual & hands-on interview questions.",
                )
            )
        else:
            prep_areas.append(
                InterviewArea(
                    area=area_title,
                    priority="LOW",
                    is_gap=False,
                    description=f"Existing capability. Review advanced technical nuances and past project contributions.",
                )
            )

    # Sort prep areas so HIGH priority gaps appear first
    p_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    prep_areas.sort(key=lambda a: p_rank.get(a.priority, 3))

    return InterviewReadiness(
        overall_score=overall_score,
        readiness_level=readiness_level,
        target_role=target_role,
        technical_skills_score=technical_skills_score,
        role_alignment_score=role_alignment_score,
        skill_coverage_score=skill_coverage_score,
        project_readiness_score=project_readiness_score,
        components=components,
        preparation_areas=prep_areas,
        project_readiness_note=project_readiness_note,
    )


def perform_learning_interview_analysis(
    candidate_profile: Optional[Dict[str, Any]] = None,
    career_analysis: Optional[Dict[str, Any]] = None,
    job_match: Optional[Dict[str, Any]] = None,
) -> LearningInterviewResult:
    """
    Main orchestration function for Step 9:
    Coordinates Roadmap Generation and Interview Readiness Scoring.
    """
    candidate_profile = candidate_profile or {}
    candidate_name = candidate_profile.get("name") or "Candidate"

    # Extract skills
    raw_skills = candidate_profile.get("skills", [])
    if not isinstance(raw_skills, list):
        raw_skills = []
    normalized_candidate_skills = {normalize_skill(s) for s in raw_skills if normalize_skill(s)}

    # If career_analysis is not provided or empty, calculate it on the fly
    if not career_analysis or not isinstance(career_analysis, dict) or not career_analysis.get("recommended_roles"):
        career_analysis_obj = perform_career_analysis(candidate_profile, job_match)
        career_analysis = career_analysis_obj.model_dump()

    # Determine strongest career role
    recommended_roles = career_analysis.get("recommended_roles", [])
    strongest_role_obj = career_analysis.get("strongest_fit_role") or (
        recommended_roles[0] if recommended_roles else None
    )

    if strongest_role_obj and isinstance(strongest_role_obj, dict):
        target_role = strongest_role_obj.get("role") or "Data Analyst"
        target_role_match_pct = int(strongest_role_obj.get("match_percentage", 0))
    else:
        target_role = "Data Analyst"
        target_role_match_pct = 0

    # Extract prioritized gaps (HIGH -> MEDIUM -> LOW)
    ordered_gaps = extract_priority_ordered_gaps(
        career_analysis=career_analysis,
        job_match=job_match,
        target_role=target_role,
        normalized_candidate_skills=normalized_candidate_skills,
    )

    # 1. Generate 4-Week Learning Roadmap
    learning_roadmap = generate_learning_roadmap(
        candidate_skills=raw_skills,
        normalized_candidate_skills=normalized_candidate_skills,
        target_role=target_role,
        target_role_match_pct=target_role_match_pct,
        ordered_gaps=ordered_gaps,
    )

    # 2. Calculate Interview Readiness
    interview_readiness = calculate_interview_readiness(
        candidate_profile=candidate_profile,
        target_role=target_role,
        target_role_match_pct=target_role_match_pct,
        normalized_candidate_skills=normalized_candidate_skills,
        job_match=job_match,
        ordered_gaps=ordered_gaps,
    )

    return LearningInterviewResult(
        learning_roadmap=learning_roadmap,
        interview_readiness=interview_readiness,
        target_role=target_role,
        candidate_name=candidate_name,
    )
