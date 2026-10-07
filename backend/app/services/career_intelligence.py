"""
CareerIQ Career Intelligence Service
Provides Skill Gap Analysis, Gap Prioritization, and Curated Career Role Recommendations.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field

from app.services.job_matcher import normalize_skill, get_canonical_display


# ==============================================================================
# Pydantic Schemas
# ==============================================================================

class SkillGap(BaseModel):
    skill: str
    current_level: str = "0"
    target_level: str = "Required"
    gap: str = "Missing"
    priority: str  # "HIGH", "MEDIUM", "LOW"
    reason: str
    target_role: Optional[str] = None


class CareerRole(BaseModel):
    role: str
    match_percentage: int
    match_strength: str  # "Excellent Fit", "Strong Fit", "Good Potential", "Developing Fit", "Early Fit"
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    total_role_skills: int
    description: str
    demand_level: str
    explanation: str


class CareerAnalysisRequest(BaseModel):
    candidate_profile: Optional[Dict[str, Any]] = None
    job_match: Optional[Dict[str, Any]] = None


class CareerAnalysisResult(BaseModel):
    skill_gaps: List[SkillGap] = Field(default_factory=list)
    top_priority_gaps: List[SkillGap] = Field(default_factory=list)
    recommended_roles: List[CareerRole] = Field(default_factory=list)
    strongest_fit_role: Optional[CareerRole] = None
    total_gaps_count: int = 0
    high_priority_count: int = 0
    medium_priority_count: int = 0
    low_priority_count: int = 0
    is_profile_only: bool = False
    candidate_name: Optional[str] = None
    target_job_title: Optional[str] = None


# ==============================================================================
# Curated MVP Career Roles & Skill Definitions
# ==============================================================================

CURATED_ROLES: List[Dict[str, Any]] = [
    {
        "role": "Data Analyst",
        "description": "Transforms structured data into actionable business insights using SQL, statistical analysis, and interactive dashboards.",
        "demand_level": "High Industry Demand",
        "skills": [
            "Python",
            "SQL",
            "Excel",
            "Power BI",
            "Tableau",
            "Statistics",
            "Data Visualization",
            "Pandas",
        ],
    },
    {
        "role": "BI Analyst",
        "description": "Specializes in business intelligence reporting, data modeling, KPI tracking, and enterprise dashboard architecture.",
        "demand_level": "Steady Enterprise Demand",
        "skills": [
            "SQL",
            "Power BI",
            "Excel",
            "Data Visualization",
            "Statistics",
        ],
    },
    {
        "role": "Business Analyst",
        "description": "Bridges business stakeholders and technical teams through requirements gathering, process mapping, and financial/operational data analysis.",
        "demand_level": "High Business Demand",
        "skills": [
            "Excel",
            "SQL",
            "Data Analysis",
            "Power BI",
            "Tableau",
        ],
    },
    {
        "role": "Junior Data Scientist",
        "description": "Applies statistical modeling, exploratory data analysis, and predictive machine learning algorithms to complex datasets.",
        "demand_level": "Rapidly Growing",
        "skills": [
            "Python",
            "SQL",
            "Pandas",
            "NumPy",
            "Statistics",
            "Machine Learning",
            "Scikit-learn",
        ],
    },
    {
        "role": "Data Engineer",
        "description": "Builds robust data pipelines, orchestrates ETL workflows, and designs scalable database architectures for analytical systems.",
        "demand_level": "Critical Infrastructure Role",
        "skills": [
            "Python",
            "SQL",
            "ETL",
            "Docker",
            "PostgreSQL",
            "Git",
            "Linux",
        ],
    },
    {
        "role": "ML Engineer",
        "description": "Designs, trains, deploys, and optimizes machine learning and deep learning models into production environments.",
        "demand_level": "Advanced AI Specialization",
        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "PyTorch",
            "TensorFlow",
            "Docker",
            "Git",
            "NumPy",
        ],
    },
    {
        "role": "Python Developer",
        "description": "Engineers backend microservices, automations, and modern web APIs using Python ecosystems and relational databases.",
        "demand_level": "Core Engineering Demand",
        "skills": [
            "Python",
            "FastAPI",
            "Django",
            "REST APIs",
            "Git",
            "PostgreSQL",
            "Docker",
        ],
    },
    {
        "role": "Backend Developer",
        "description": "Architects server-side logic, data persistence layers, API gateways, and containerized microservices.",
        "demand_level": "High Engineering Demand",
        "skills": [
            "Python",
            "Node.js",
            "REST APIs",
            "PostgreSQL",
            "Docker",
            "Git",
            "FastAPI",
        ],
    },
    {
        "role": "Full-Stack Developer",
        "description": "Builds end-to-end web applications combining intuitive front-end user experiences with robust backend services.",
        "demand_level": "Versatile Product Engineering",
        "skills": [
            "Python",
            "JavaScript",
            "TypeScript",
            "React",
            "Node.js",
            "HTML",
            "CSS",
            "Git",
            "REST APIs",
        ],
    },
]


# ==============================================================================
# Helper Functions
# ==============================================================================

def get_role_match_strength(percentage: int) -> str:
    """
    Classifies numerical match score into transparent fit labels.
    90-100: Excellent Fit
    75-89:  Strong Fit
    60-74:  Good Potential
    40-59:  Developing Fit
    0-39:   Early Fit
    """
    if percentage >= 90:
        return "Excellent Fit"
    elif percentage >= 75:
        return "Strong Fit"
    elif percentage >= 60:
        return "Good Potential"
    elif percentage >= 40:
        return "Developing Fit"
    else:
        return "Early Fit"


def generate_role_explanation(
    role_name: str,
    match_percentage: int,
    matched_skills: List[str],
    missing_skills: List[str],
) -> str:
    """
    Generates a clear, grounded explanation for a recommended role.
    """
    if match_percentage >= 90:
        return (
            f"Outstanding alignment across all core competencies for {role_name}. "
            f"Your skillset strongly covers key requirements."
        )
    elif match_percentage >= 75:
        missing_preview = ", ".join(missing_skills[:2]) if missing_skills else "advanced topics"
        return (
            f"Strong alignment with your current competencies. "
            f"Strengthening {missing_preview} would solidify your readiness for {role_name}."
        )
    elif match_percentage >= 60:
        missing_preview = ", ".join(missing_skills[:3]) if missing_skills else "core tools"
        return (
            f"Good potential with notable crossover in {', '.join(matched_skills[:3])}. "
            f"Targeting gaps in {missing_preview} will significantly enhance compatibility."
        )
    elif match_percentage >= 40:
        matched_preview = ", ".join(matched_skills[:2]) if matched_skills else "foundational concepts"
        missing_preview = ", ".join(missing_skills[:2]) if missing_skills else "specialized tools"
        return (
            f"Developing foundation with transferable skills in {matched_preview}. "
            f"Acquiring {missing_preview} will be essential for this transition."
        )
    else:
        missing_preview = ", ".join(missing_skills[:3]) if missing_skills else "foundational tools"
        return (
            f"Early career alignment. Developing skills in {missing_preview} "
            f"is recommended to establish readiness for this pathway."
        )


# ==============================================================================
# Core Intelligence Engine
# ==============================================================================

def extract_candidate_skills(candidate_profile: Optional[Dict[str, Any]]) -> Tuple[List[str], Set[str], Optional[str]]:
    """
    Extracts raw skills, normalized skill set, and candidate name from candidate profile dict.
    """
    if not candidate_profile:
        return [], set(), None

    name = candidate_profile.get("name")
    raw_skills = candidate_profile.get("skills", [])
    if not isinstance(raw_skills, list):
        raw_skills = []

    normalized_set = {normalize_skill(s) for s in raw_skills if normalize_skill(s)}
    return raw_skills, normalized_set, name


def calculate_career_roles(normalized_candidate_skills: Set[str]) -> List[CareerRole]:
    """
    Matches candidate skills against curated MVP roles and ranks by match percentage.
    Formula: round((matched_skills / total_role_skills) * 100)
    """
    recommended_roles: List[CareerRole] = []

    for role_def in CURATED_ROLES:
        role_name = role_def["role"]
        role_skills = role_def["skills"]
        total_skills = len(role_skills)

        matched: List[str] = []
        missing: List[str] = []

        for skill in role_skills:
            norm = normalize_skill(skill)
            if norm in normalized_candidate_skills:
                matched.append(get_canonical_display(skill))
            else:
                missing.append(get_canonical_display(skill))

        match_pct = round((len(matched) / total_skills) * 100) if total_skills > 0 else 0
        strength_label = get_role_match_strength(match_pct)
        explanation = generate_role_explanation(role_name, match_pct, matched, missing)

        recommended_roles.append(
            CareerRole(
                role=role_name,
                match_percentage=match_pct,
                match_strength=strength_label,
                matched_skills=matched,
                missing_skills=missing,
                total_role_skills=total_skills,
                description=role_def["description"],
                demand_level=role_def["demand_level"],
                explanation=explanation,
            )
        )

    # Sort descending by match_percentage, then by number of matched skills
    recommended_roles.sort(key=lambda r: (r.match_percentage, len(r.matched_skills)), reverse=True)
    return recommended_roles


def analyze_skill_gaps(
    candidate_skills: List[str],
    normalized_candidate_skills: Set[str],
    job_match: Optional[Dict[str, Any]],
    recommended_roles: List[CareerRole],
) -> Tuple[List[SkillGap], List[SkillGap], bool, Optional[str]]:
    """
    Analyzes skill gaps and assigns priority according to transparent rules.
    HIGH:
      - Required by target job, candidate does not have it.
    MEDIUM:
      - Preferred/nice-to-have skill in target job, candidate does not have it.
      - OR if no job match: top competency missing from closest recommended role (profile-based).
    LOW:
      - Useful related skill from recommended role profiles.
    """
    all_gaps: List[SkillGap] = []
    seen_normalized_gaps: Set[str] = set()

    is_profile_only = True
    target_job_title = None

    # Check if job match context is available and contains required/preferred data
    has_job_match = bool(
        job_match
        and isinstance(job_match, dict)
        and (job_match.get("missing_skills") or job_match.get("preferred_skills") or job_match.get("matched_skills"))
    )

    if has_job_match:
        is_profile_only = False
        target_job_title = job_match.get("job_title") or "Target Job"

        # 1. HIGH PRIORITY: Missing required skills from target job
        missing_required = job_match.get("missing_skills", [])
        if isinstance(missing_required, list):
            for skill in missing_required:
                canonical = get_canonical_display(skill)
                norm = normalize_skill(skill)
                if norm not in normalized_candidate_skills and norm not in seen_normalized_gaps:
                    seen_normalized_gaps.add(norm)
                    all_gaps.append(
                        SkillGap(
                            skill=canonical,
                            current_level="0",
                            target_level="Required",
                            gap="Missing",
                            priority="HIGH",
                            reason=f"Required competency identified from your target job ({target_job_title}).",
                            target_role=target_job_title,
                        )
                    )

        # 2. MEDIUM PRIORITY: Missing preferred / nice-to-have skills from target job
        missing_preferred = job_match.get("missing_preferred_skills", [])
        if not missing_preferred:
            # Check preferred_skills minus matched_preferred_skills
            preferred_all = job_match.get("preferred_skills", [])
            matched_pref = {normalize_skill(s) for s in job_match.get("matched_preferred_skills", [])}
            missing_preferred = [s for s in preferred_all if normalize_skill(s) not in matched_pref]

        if isinstance(missing_preferred, list):
            for skill in missing_preferred:
                canonical = get_canonical_display(skill)
                norm = normalize_skill(skill)
                if norm not in normalized_candidate_skills and norm not in seen_normalized_gaps:
                    seen_normalized_gaps.add(norm)
                    all_gaps.append(
                        SkillGap(
                            skill=canonical,
                            current_level="0",
                            target_level="Preferred",
                            gap="Missing",
                            priority="MEDIUM",
                            reason=f"Preferred / nice-to-have competency for {target_job_title}.",
                            target_role=target_job_title,
                        )
                    )

        # 3. LOW PRIORITY: Complementary skills from top recommended role not in target job
        if recommended_roles:
            top_role = recommended_roles[0]
            for skill in top_role.missing_skills:
                canonical = get_canonical_display(skill)
                norm = normalize_skill(skill)
                if norm not in normalized_candidate_skills and norm not in seen_normalized_gaps:
                    seen_normalized_gaps.add(norm)
                    all_gaps.append(
                        SkillGap(
                            skill=canonical,
                            current_level="0",
                            target_level="Role Standard",
                            gap="Missing",
                            priority="LOW",
                            reason=f"Complementary skill that improves fit for {top_role.role}.",
                            target_role=top_role.role,
                        )
                    )

    else:
        # Profile-only mode: calculate gaps transparently from top recommended roles
        is_profile_only = True
        if recommended_roles and len(normalized_candidate_skills) > 0:
            top_role = recommended_roles[0]
            target_job_title = top_role.role

            # MEDIUM: Missing core skills from strongest matched role (Profile-based)
            for skill in top_role.missing_skills:
                canonical = get_canonical_display(skill)
                norm = normalize_skill(skill)
                if norm not in normalized_candidate_skills and norm not in seen_normalized_gaps:
                    seen_normalized_gaps.add(norm)
                    all_gaps.append(
                        SkillGap(
                            skill=canonical,
                            current_level="0",
                            target_level="Role Standard",
                            gap="Missing",
                            priority="MEDIUM",
                            reason=f"Key competency for your highest-matching direction ({top_role.role}). Profile-based gap.",
                            target_role=top_role.role,
                        )
                    )

            # LOW: Useful complementary skills from secondary recommended role
            if len(recommended_roles) > 1:
                second_role = recommended_roles[1]
                for skill in second_role.missing_skills:
                    canonical = get_canonical_display(skill)
                    norm = normalize_skill(skill)
                    if norm not in normalized_candidate_skills and norm not in seen_normalized_gaps:
                        seen_normalized_gaps.add(norm)
                        all_gaps.append(
                            SkillGap(
                                skill=canonical,
                                current_level="0",
                                target_level="Role Standard",
                                gap="Missing",
                                priority="LOW",
                                reason=f"Transferable competency to expand pathway into {second_role.role}.",
                                target_role=second_role.role,
                            )
                        )

    # Sort gaps: HIGH first, then MEDIUM, then LOW
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    all_gaps.sort(key=lambda g: priority_order.get(g.priority, 3))

    # Top priority gaps (first 4-6 most important gaps)
    top_priority = all_gaps[:6]

    return all_gaps, top_priority, is_profile_only, target_job_title


def perform_career_analysis(
    candidate_profile: Optional[Dict[str, Any]] = None,
    job_match: Optional[Dict[str, Any]] = None,
) -> CareerAnalysisResult:
    """
    Main orchestration function for Step 8 Career Intelligence.
    Transforms candidate profile + job matching information into:
    1. Skill Gaps with priority
    2. Top priority gaps
    3. Ranked Career Role Recommendations (top 4)
    4. Strongest fit role summary
    """
    raw_skills, normalized_skills, candidate_name = extract_candidate_skills(candidate_profile)

    # Compute role recommendations across curated roles
    all_role_recommendations = calculate_career_roles(normalized_skills)

    # Top 4 roles
    top_4_roles = all_role_recommendations[:4]

    # Strongest fit role
    strongest_fit = top_4_roles[0] if top_4_roles else None

    # Compute skill gaps and priorities
    skill_gaps, top_priority_gaps, is_profile_only, target_job_title = analyze_skill_gaps(
        candidate_skills=raw_skills,
        normalized_candidate_skills=normalized_skills,
        job_match=job_match,
        recommended_roles=all_role_recommendations,
    )

    high_count = sum(1 for g in skill_gaps if g.priority == "HIGH")
    medium_count = sum(1 for g in skill_gaps if g.priority == "MEDIUM")
    low_count = sum(1 for g in skill_gaps if g.priority == "LOW")

    return CareerAnalysisResult(
        skill_gaps=skill_gaps,
        top_priority_gaps=top_priority_gaps,
        recommended_roles=top_4_roles,
        strongest_fit_role=strongest_fit,
        total_gaps_count=len(skill_gaps),
        high_priority_count=high_count,
        medium_priority_count=medium_count,
        low_priority_count=low_count,
        is_profile_only=is_profile_only,
        candidate_name=candidate_name or "Candidate",
        target_job_title=target_job_title,
    )
