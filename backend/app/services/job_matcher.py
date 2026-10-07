import re
from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field

from app.services.resume_intelligence import SKILL_VOCABULARY

# ==============================================================================
# Pydantic Schemas for Job Matching
# ==============================================================================


class JobRequirementProfile(BaseModel):
    job_title: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    all_skills: List[str] = Field(default_factory=list)


class JobMatchRequest(BaseModel):
    job_title: Optional[str] = None
    job_description: str
    candidate_skills: List[str] = Field(default_factory=list)
    candidate_name: Optional[str] = None


class JobMatchResult(BaseModel):
    job_title: Optional[str] = None
    match_percentage: int
    match_strength: str  # "Excellent Match", "Strong Match", "Moderate Match", "Weak Match", "Low Match"
    total_required: int
    total_matched: int
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    matched_preferred_skills: List[str] = Field(default_factory=list)
    missing_preferred_skills: List[str] = Field(default_factory=list)
    all_job_skills: List[str] = Field(default_factory=list)
    candidate_skills_count: int = 0


# ==============================================================================
# Skill Normalization Mapping
# ==============================================================================

NORMALIZATION_MAP: Dict[str, str] = {
    # Data & BI
    "powerbi": "power bi",
    "power-bi": "power bi",
    "power bi": "power bi",
    "ms excel": "excel",
    "microsoft excel": "excel",
    "excel": "excel",
    "data analytics": "data analysis",
    "data analysis": "data analysis",
    "data visualization": "data visualization",
    "data visualisation": "data visualization",
    "eda": "eda",
    "exploratory data analysis": "eda",
    # Programming & Web
    "nodejs": "node.js",
    "node js": "node.js",
    "node.js": "node.js",
    "node": "node.js",
    "reactjs": "react",
    "react.js": "react",
    "react": "react",
    "nextjs": "next.js",
    "next.js": "next.js",
    "next": "next.js",
    "vuejs": "vue.js",
    "vue.js": "vue.js",
    "vue": "vue.js",
    "expressjs": "express",
    "express.js": "express",
    "express": "express",
    "fastapi": "fastapi",
    "fast api": "fastapi",
    "restful api": "rest api",
    "restful apis": "rest api",
    "rest api": "rest api",
    "rest apis": "rest api",
    "rest": "rest api",
    "c++": "c++",
    "cpp": "c++",
    "c#": "c#",
    "c sharp": "c#",
    "golang": "go",
    "go": "go",
    # Databases
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "mongo": "mongodb",
    "mongodb": "mongodb",
    "mysql": "mysql",
    "redis": "redis",
    "sqlite": "sqlite",
    # AI & ML
    "machine learning": "machine learning",
    "deep learning": "deep learning",
    "scikit-learn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "tensorflow": "tensorflow",
    "pytorch": "pytorch",
    "nlp": "nlp",
    "natural language processing": "nlp",
    "llm": "llm",
    "large language models": "llm",
    "genai": "generative ai",
    "generative ai": "generative ai",
    # Cloud & DevOps
    "amazon web services": "aws",
    "aws": "aws",
    "google cloud platform": "gcp",
    "google cloud": "gcp",
    "gcp": "gcp",
    "microsoft azure": "azure",
    "azure": "azure",
    "docker": "docker",
    "kubernetes": "kubernetes",
    "k8s": "kubernetes",
    "git": "git",
    "github": "github",
    "ci/cd": "ci/cd",
    "ci cd": "ci/cd",
}

# Pre-generate canonical display names
CANONICAL_DISPLAY: Dict[str, str] = {s.lower(): s for s in SKILL_VOCABULARY}
for raw, norm in NORMALIZATION_MAP.items():
    if norm in CANONICAL_DISPLAY:
        CANONICAL_DISPLAY[raw] = CANONICAL_DISPLAY[norm]


def normalize_skill(skill: str) -> str:
    """
    Normalizes a skill name into a standardized key for accurate matching.
    """
    if not skill:
        return ""
    cleaned = skill.strip().lower()
    # Remove leading/trailing non-alphanumeric chars except #, +, .
    cleaned = re.sub(r"^[^a-z0-9#+.]+|[^a-z0-9#+.]+$", "", cleaned)
    if cleaned in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[cleaned]
    # Replace whitespace and hyphens
    condensed = re.sub(r"[\s_-]+", " ", cleaned)
    return NORMALIZATION_MAP.get(condensed, condensed)


def get_canonical_display(skill: str) -> str:
    """
    Returns canonical casing for a skill if known, otherwise original cleaned string.
    """
    norm = normalize_skill(skill)
    # Check if a display name exists for the normalized key
    for s in SKILL_VOCABULARY:
        if normalize_skill(s) == norm:
            return s
    return skill.strip()


# ==============================================================================
# Job Description Requirement Extraction
# ==============================================================================

# Regex patterns to segment Required vs Preferred qualifications
REQUIRED_HEADER_PATTERNS = [
    re.compile(r"\b(minimum\s+qualifications|basic\s+qualifications|required\s+skills|requirements|what\s+you'?ll\s+need|must\s+have|qualifications|technical\s+requirements)\b", re.I),
]

PREFERRED_HEADER_PATTERNS = [
    re.compile(r"\b(preferred\s+qualifications|desired\s+qualifications|nice\s+to\s+have|bonus\s+points|good\s+to\s+have|plus|preferred\s+skills|preferred)\b", re.I),
]


def extract_skills_from_text(text: str) -> List[str]:
    """
    Detects curated skills present in the text with boundary matching.
    """
    detected: List[str] = []
    seen_normalized: Set[str] = set()

    for skill in SKILL_VOCABULARY:
        norm = normalize_skill(skill)
        if norm in seen_normalized:
            continue

        # Single-letter or special skills matching
        if skill == "C":
            pattern = r"(?<![A-Za-z0-9])C(?![A-Za-z0-9+#])"
            if re.search(pattern, text):
                detected.append(skill)
                seen_normalized.add(norm)
        elif skill in ["C++", "C#"]:
            pattern = re.escape(skill)
            if re.search(pattern, text, re.IGNORECASE):
                detected.append(skill)
                seen_normalized.add(norm)
        elif skill == "R":
            pattern = r"(?<![A-Za-z0-9])R(?![A-Za-z0-9+#])"
            if re.search(pattern, text):
                detected.append(skill)
                seen_normalized.add(norm)
        elif skill in ["EDA", "NLP", "LLM", "ETL", "SQL", "AWS", "GCP", "HTML", "CSS", "CI/CD"]:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text, re.IGNORECASE):
                detected.append(skill)
                seen_normalized.add(norm)
        else:
            # Word boundary search
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text, re.IGNORECASE):
                detected.append(skill)
                seen_normalized.add(norm)

    return detected


def segment_job_description(job_description: str) -> Tuple[List[str], List[str], List[str]]:
    """
    Attempts to distinguish required vs preferred skills from job description text.
    If reliable distinction cannot be determined, all detected skills are categorized as required.
    """
    lines = job_description.splitlines()

    required_text_parts: List[str] = []
    preferred_text_parts: List[str] = []
    current_state = "neutral"  # "required" | "preferred" | "neutral"

    has_required_section = False
    has_preferred_section = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Check for Preferred headers
        if any(pat.search(stripped) for pat in PREFERRED_HEADER_PATTERNS):
            current_state = "preferred"
            has_preferred_section = True
            continue

        # Check for Required headers
        if any(pat.search(stripped) for pat in REQUIRED_HEADER_PATTERNS):
            current_state = "required"
            has_required_section = True
            continue

        if current_state == "required":
            required_text_parts.append(stripped)
        elif current_state == "preferred":
            preferred_text_parts.append(stripped)

    # If both or either section was found, parse each section
    if has_required_section or has_preferred_section:
        req_text = " \n ".join(required_text_parts)
        pref_text = " \n ".join(preferred_text_parts)

        req_skills = extract_skills_from_text(req_text)
        pref_skills = extract_skills_from_text(pref_text)

        # Remove duplicate skills between required and preferred (required takes precedence)
        req_norm_set = {normalize_skill(s) for s in req_skills}
        pref_skills_deduped = [s for s in pref_skills if normalize_skill(s) not in req_norm_set]

        # In case some skills were mentioned in general intro, include them in required
        all_skills = extract_skills_from_text(job_description)
        known_norm_set = req_norm_set.union({normalize_skill(s) for s in pref_skills_deduped})
        extra_skills = [s for s in all_skills if normalize_skill(s) not in known_norm_set]

        # Extra general skills default to required
        req_skills.extend(extra_skills)

        return req_skills, pref_skills_deduped, all_skills
    else:
        # No clear section distinction: treat all detected skills as required (per specification)
        all_skills = extract_skills_from_text(job_description)
        return all_skills, [], all_skills


# ==============================================================================
# Matching Engine & Scoring
# ==============================================================================


def calculate_match_strength(score: int) -> str:
    """
    Translates percentage score to match strength interpretation:
    90–100: Excellent Match
    75–89: Strong Match
    60–74: Moderate Match
    40–59: Weak Match
    0–39: Low Match
    """
    if score >= 90:
        return "Excellent Match"
    elif score >= 75:
        return "Strong Match"
    elif score >= 60:
        return "Moderate Match"
    elif score >= 40:
        return "Weak Match"
    else:
        return "Low Match"


def match_resume_to_job(
    job_description: str,
    candidate_skills: List[str],
    job_title: Optional[str] = None,
) -> JobMatchResult:
    """
    Performs full job requirement extraction and resume-to-job matching.

    Formula:
    match_percentage = (number of matched required skills / number of required skills) * 100
    Round to nearest whole number.
    Only required skills in denominator.
    """
    if not job_description or not job_description.strip():
        return JobMatchResult(
            job_title=job_title,
            match_percentage=0,
            match_strength="Low Match",
            total_required=0,
            total_matched=0,
            matched_skills=[],
            missing_skills=[],
            preferred_skills=[],
            matched_preferred_skills=[],
            missing_preferred_skills=[],
            all_job_skills=[],
            candidate_skills_count=len(candidate_skills),
        )

    # 1. Segment job requirements
    required_skills, preferred_skills, all_job_skills = segment_job_description(job_description)

    # 2. Normalize candidate skills set
    normalized_candidate_set: Set[str] = {
        normalize_skill(s) for s in candidate_skills if s and s.strip()
    }

    # 3. Compare required skills
    matched_required: List[str] = []
    missing_required: List[str] = []

    for req_skill in required_skills:
        req_norm = normalize_skill(req_skill)
        if req_norm in normalized_candidate_set:
            matched_required.append(req_skill)
        else:
            missing_required.append(req_skill)

    # 4. Compare preferred skills
    matched_preferred: List[str] = []
    missing_preferred: List[str] = []

    for pref_skill in preferred_skills:
        pref_norm = normalize_skill(pref_skill)
        if pref_norm in normalized_candidate_set:
            matched_preferred.append(pref_skill)
        else:
            missing_preferred.append(pref_skill)

    # 5. Compute match score
    total_required = len(required_skills)
    total_matched = len(matched_required)

    if total_required > 0:
        raw_percentage = (total_matched / total_required) * 100
        match_percentage = int(round(raw_percentage))
    elif len(preferred_skills) > 0:
        # Fallback if only preferred skills were present
        raw_percentage = (len(matched_preferred) / len(preferred_skills)) * 100
        match_percentage = int(round(raw_percentage))
    else:
        # No skills mentioned in job description
        match_percentage = 0

    # Ensure bounded 0 - 100
    match_percentage = max(0, min(100, match_percentage))
    match_strength = calculate_match_strength(match_percentage)

    # Attempt to extract job title if not provided
    inferred_title = job_title
    if not inferred_title:
        first_line = job_description.strip().splitlines()[0].strip()
        if len(first_line.split()) <= 6 and not any(c in first_line for c in [":", ".", "?"]):
            inferred_title = first_line

    return JobMatchResult(
        job_title=inferred_title,
        match_percentage=match_percentage,
        match_strength=match_strength,
        total_required=total_required,
        total_matched=total_matched,
        matched_skills=matched_required,
        missing_skills=missing_required,
        preferred_skills=preferred_skills,
        matched_preferred_skills=matched_preferred,
        missing_preferred_skills=missing_preferred,
        all_job_skills=all_job_skills,
        candidate_skills_count=len(candidate_skills),
    )
