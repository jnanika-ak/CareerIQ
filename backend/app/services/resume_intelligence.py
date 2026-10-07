import re
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

# ==============================================================================
# Pydantic Schemas for Structured Profile Response
# ==============================================================================


class EducationItem(BaseModel):
    degree: Optional[str] = None
    field: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None


class ProjectItem(BaseModel):
    name: str
    description: Optional[str] = None


class ExperienceItem(BaseModel):
    role: Optional[str] = None
    company: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None


class CandidateProfile(BaseModel):
    name: Optional[str] = None
    summary: Optional[str] = None
    education: List[EducationItem] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    experience: List[ExperienceItem] = Field(default_factory=list)


class ResumeAnalysisResponse(BaseModel):
    filename: str
    file_type: Optional[str] = None
    characters: Optional[int] = None
    pages: Optional[int] = None
    text: Optional[str] = None
    profile: CandidateProfile



# ==============================================================================
# Curated Skill Vocabulary
# ==============================================================================

# Categories with canonical display names
SKILL_VOCABULARY = [
    # Programming
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "C", "SQL", "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "R",
    # Data & Analytics
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Power BI", "Tableau", "Excel", "Statistics", "Data Analysis", "Data Visualization",
    "Exploratory Data Analysis", "EDA", "Business Intelligence", "ETL", "Data Mining",
    # AI / Machine Learning
    "Machine Learning", "Deep Learning", "Scikit-learn", "TensorFlow", "PyTorch", "NLP", "Natural Language Processing",
    "Computer Vision", "LLM", "Hugging Face", "Keras", "OpenCV", "Generative AI",
    # Web & Frameworks
    "HTML", "CSS", "React", "Node.js", "FastAPI", "REST API", "Next.js", "Express", "Django", "Flask", "Tailwind CSS",
    "Bootstrap", "GraphQL", "Redux", "Vue.js", "Angular",
    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes", "Git", "GitHub", "CI/CD", "Linux", "Terraform", "Jenkins",
    # Databases
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Cassandra", "Oracle", "Elasticsearch", "DynamoDB"
]

# Section Headers Regex Patterns
SECTION_PATTERNS = {
    "summary": re.compile(
        r"^(professional\s+summary|career\s+objective|profile\s+summary|summary|profile|about\s+me|objective)[\s:]*$",
        re.IGNORECASE,
    ),
    "skills": re.compile(
        r"^(technical\s+skills(\s+&\s+tools)?|technical\s+competencies|core\s+competencies|skills(\s+&\s+technologies)?|key\s+skills|technologies|skills)[\s:]*$",
        re.IGNORECASE,
    ),
    "experience": re.compile(
        r"^(professional\s+experience|work\s+experience|employment\s+history|work\s+history|internships|experience)[\s:]*$",
        re.IGNORECASE,
    ),
    "education": re.compile(
        r"^(academic\s+qualifications|academic\s+background|educational\s+background|education|academics)[\s:]*$",
        re.IGNORECASE,
    ),
    "projects": re.compile(
        r"^(academic\s+projects|personal\s+projects|key\s+projects|relevant\s+projects|technical\s+projects|projects)[\s:]*$",
        re.IGNORECASE,
    ),
    "certifications": re.compile(
        r"^(licenses\s+&\s+certifications|certifications\s+&\s+licenses|courses\s+&\s+certifications|certifications|certificates)[\s:]*$",
        re.IGNORECASE,
    ),
}

# Degree keywords and regular expressions for Education extraction
DEGREE_PATTERNS = [
    (r"\b(B\.?\s?Tech|Bachelor of Technology)\b", "Bachelor of Technology"),
    (r"\b(B\.?\s?E\.?|Bachelor of Engineering)\b", "Bachelor of Engineering"),
    (r"\b(B\.?\s?S\.?|B\.?\s?Sc\.?|Bachelor of Science)\b", "Bachelor of Science"),
    (r"\b(Bachelor of Arts|B\.?\s?A\.?)\b", "Bachelor of Arts"),
    (r"\b(B\.?\s?C\.?\s?A\.?|Bachelor of Computer Applications)\b", "Bachelor of Computer Applications"),
    (r"\b(M\.?\s?Tech|Master of Technology)\b", "Master of Technology"),
    (r"\b(M\.?\s?S\.?|M\.?\s?Sc\.?|Master of Science)\b", "Master of Science"),
    (r"\b(M\.?\s?C\.?\s?A\.?|Master of Computer Applications)\b", "Master of Computer Applications"),
    (r"\b(M\.?\s?B\.?\s?A\.?|Master of Business Administration)\b", "Master of Business Administration"),
    (r"\b(Ph\.?\s?D\.?|Doctor of Philosophy)\b", "Doctor of Philosophy"),
    (r"\b(Diploma|Associate Degree|Higher Secondary|High School)\b", "Diploma"),
]

YEAR_PATTERN = re.compile(r"\b((?:19|20)\d{2}\s*(?:[-–—to]+\s*(?:(?:19|20)\d{2}|Present|Current))?|(?:19|20)\d{2})\b", re.IGNORECASE)


# ==============================================================================
# Helper Functions for Parsing Sections
# ==============================================================================


def split_sections(text: str) -> Tuple[List[str], Dict[str, List[str]]]:
    """
    Split resume text into header lines and identified sections.
    """
    lines = [line.strip() for line in text.splitlines()]
    header_lines: List[str] = []
    sections: Dict[str, List[str]] = {}

    current_section: Optional[str] = None

    for line in lines:
        if not line:
            continue

        clean_line = line.strip(" -•*#").strip()
        matched_section = None

        # Check if line matches any section header
        for sec_name, pattern in SECTION_PATTERNS.items():
            if pattern.match(clean_line):
                matched_section = sec_name
                break

        # Check combined sections like "CERTIFICATIONS & PROJECTS"
        if not matched_section and re.match(r"^certifications?\s*(&|\band\b)\s*projects?", clean_line, re.I):
            matched_section = "certifications"

        if matched_section:
            current_section = matched_section
            if current_section not in sections:
                sections[current_section] = []
        else:
            if current_section is None:
                header_lines.append(line)
            else:
                sections[current_section].append(line)

    return header_lines, sections


def extract_name(header_lines: List[str]) -> Optional[str]:
    """
    Attempt to identify the candidate name from the top header lines using heuristics.
    Returns None if not confidently identified.
    """
    # Exclude common non-name tokens
    bad_tokens = ["email", "phone", "github", "linkedin", "http", "@", "+", "resume", "curriculum", "curriculum vitae", "portfolio", "tel:"]

    for line in header_lines[:5]:
        cleaned = line.strip(" -•*|#").strip()
        lower = cleaned.lower()

        # Reject if contains contact info or link
        if any(token in lower for token in bad_tokens):
            continue

        # Reject if contains digits
        if re.search(r"\d", cleaned):
            continue

        # Split into words
        words = cleaned.split()
        if 2 <= len(words) <= 4:
            # Check if all words look like name tokens (letters, optional periods/hyphens)
            if all(w.replace(".", "").replace("-", "").isalpha() for w in words):
                # Ensure each word starts capitalized
                if all(w[0].isupper() for w in words if len(w) > 0):
                    # Check not typical job titles or section words
                    title_words = {"senior", "junior", "lead", "engineer", "developer", "analyst", "manager", "intern", "consultant", "architect"}
                    if not any(w.lower() in title_words for w in words):
                        return cleaned

    return None


def extract_summary(sections: Dict[str, List[str]]) -> Optional[str]:
    """
    Extract professional summary or objective.
    """
    if "summary" in sections and sections["summary"]:
        text = " ".join(sections["summary"]).strip()
        return text if text else None
    return None


def extract_skills(full_text: str, sections: Dict[str, List[str]]) -> List[str]:
    """
    Detect skills from curated vocabulary present in the resume text.
    Prioritizes skills mentioned in the Skills section, then scans full text.
    """
    found_skills = []
    seen = set()

    # If dedicated skills section exists, look there first
    search_texts = []
    if "skills" in sections:
        search_texts.append("\n".join(sections["skills"]))
    search_texts.append(full_text)

    for text in search_texts:
        for skill in SKILL_VOCABULARY:
            if skill.lower() in seen:
                continue

            # Handle single-letter or special character skills
            if skill == "C":
                # Match standalone 'C' surrounded by punctuation or whitespace, but not C++ or C#
                pattern = r"(?<![A-Za-z0-9])C(?![A-Za-z0-9+#])"
                if re.search(pattern, text):
                    found_skills.append(skill)
                    seen.add(skill.lower())
            elif skill in ["C++", "C#"]:
                pattern = re.escape(skill)
                if re.search(pattern, text, re.IGNORECASE):
                    found_skills.append(skill)
                    seen.add(skill.lower())
            elif skill == "R":
                pattern = r"(?<![A-Za-z0-9])R(?![A-Za-z0-9+#])"
                if re.search(pattern, text):
                    found_skills.append(skill)
                    seen.add(skill.lower())
            elif skill in ["EDA", "NLP", "LLM", "ETL", "SQL", "AWS", "GCP", "HTML", "CSS", "CI/CD"]:
                pattern = r"\b" + re.escape(skill) + r"\b"
                if re.search(pattern, text, re.IGNORECASE):
                    found_skills.append(skill)
                    seen.add(skill.lower())
            else:
                pattern = r"\b" + re.escape(skill) + r"\b"
                if re.search(pattern, text, re.IGNORECASE):
                    found_skills.append(skill)
                    seen.add(skill.lower())

    return found_skills


def extract_education(sections: Dict[str, List[str]], full_text: str) -> List[EducationItem]:
    """
    Extract education entries (degree, field, institution, year).
    """
    lines = sections.get("education", [])
    if not lines:
        # Fallback: scan full text lines mentioning degree terms
        all_lines = full_text.splitlines()
        lines = [l for l in all_lines if any(re.search(pat, l, re.I) for pat, _ in DEGREE_PATTERNS)]

    education_items: List[EducationItem] = []

    # Group lines by entries or process lines
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        matched_degree = None

        for pattern, canonical_degree in DEGREE_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                matched_degree = canonical_degree
                break

        if matched_degree:
            # Look for field of study e.g. "in Computer Science"
            field = None
            field_match = re.search(r"\b(?:in|of)\s+([A-Za-z\s&,]+?)(?:[-–—|(]|\d{4}|$)", line, re.IGNORECASE)
            if field_match:
                candidate_field = field_match.group(1).strip(" -–—|()")
                # Clean leading degree residue e.g. "Science in Computer Science" -> "Computer Science"
                candidate_field = re.sub(r"^(?:Science|Engineering|Arts|Technology|Applications)\s+in\s+", "", candidate_field, flags=re.I)
                # Ignore if it captured university or institution
                if not any(u in candidate_field.lower() for u in ["university", "college", "institute", "school"]):
                    if len(candidate_field.split()) <= 6:
                        field = candidate_field.strip()

            # Search current line and subsequent lines for institution and year
            institution = None
            year = None

            search_lines = [line]
            if i + 1 < len(lines):
                search_lines.append(lines[i + 1])
            if i + 2 < len(lines):
                search_lines.append(lines[i + 2])

            combined_block = " \n ".join(search_lines)

            # Year extraction
            year_match = YEAR_PATTERN.search(combined_block)
            if year_match:
                year = year_match.group(1).strip()

            # Institution extraction (look for University, College, Institute, Academy, School)
            for s_line in search_lines:
                clean_s = re.sub(YEAR_PATTERN, "", s_line).strip(" ()-–—|")
                inst_match = re.search(r"([-A-Za-z\s&,.]*?(?:University|College|Institute|Academy|School)[-A-Za-z\s&,.]*)", clean_s, re.IGNORECASE)
                if inst_match:
                    inst_cand = inst_match.group(1).strip(" -–—|(),.")
                    if len(inst_cand.split()) <= 8:
                        institution = inst_cand
                        break


            education_items.append(
                EducationItem(
                    degree=matched_degree,
                    field=field if field else None,
                    institution=institution if institution else None,
                    year=year if year else None,
                )
            )
            i += 1
        else:
            i += 1

    return education_items


def extract_projects(sections: Dict[str, List[str]]) -> List[ProjectItem]:
    """
    Extract project entries from projects section or combined certifications/projects section.
    """
    lines = list(sections.get("projects", []))
    # Also check if certifications section contains project lines
    if "certifications" in sections:
        for c_line in sections["certifications"]:
            if re.search(r"\b(built with|developed with|copilot|platform|app|agent|system|ai)\b", c_line, re.I) and (":" in c_line or " - " in c_line):
                lines.append(c_line)

    projects: List[ProjectItem] = []
    seen_names = set()

    for line in lines:
        cleaned = line.strip(" -•*#").strip()
        if not cleaned:
            continue

        # Formats like: "Project Name: Description..." or "Project Name - Description..."
        if ":" in cleaned:
            parts = cleaned.split(":", 1)
            name = parts[0].strip(" -•*#")
            desc = parts[1].strip() if len(parts) > 1 else None
            if 1 <= len(name.split()) <= 7 and name.lower() not in seen_names:
                seen_names.add(name.lower())
                projects.append(ProjectItem(name=name, description=desc))
        elif " - " in cleaned:
            parts = cleaned.split(" - ", 1)
            name = parts[0].strip(" -•*#")
            desc = parts[1].strip()
            if 1 <= len(name.split()) <= 7 and name.lower() not in seen_names:
                seen_names.add(name.lower())
                projects.append(ProjectItem(name=name, description=desc))
        elif "|" in cleaned:
            parts = cleaned.split("|", 1)
            name = parts[0].strip(" -•*#")
            desc = parts[1].strip()
            if 1 <= len(name.split()) <= 7 and name.lower() not in seen_names:
                seen_names.add(name.lower())
                projects.append(ProjectItem(name=name, description=desc))

    return projects



def extract_certifications(sections: Dict[str, List[str]]) -> List[str]:
    """
    Extract certification titles from certifications section.
    """
    lines = sections.get("certifications", [])
    certifications: List[str] = []

    for line in lines:
        cleaned = line.strip(" -•*#").strip()
        if not cleaned:
            continue

        # Check if line looks like a project rather than cert in combined sections
        if re.search(r"\b(built with|developed with|github\.com)\b", cleaned, re.I):
            continue

        cert_words = ["certified", "certificate", "certification", "aws", "azure", "google", "meta", "ibm", "cisco", "comptia", "oracle"]
        if any(w in cleaned.lower() for w in cert_words) or len(cleaned.split()) <= 8:
            # Clean trailing punctuation
            cert_name = cleaned.strip(" :.-")
            if cert_name and cert_name not in certifications:
                certifications.append(cert_name)

    return certifications


def extract_experience(sections: Dict[str, List[str]]) -> List[ExperienceItem]:
    """
    Extract work or internship experience entries.
    """
    lines = sections.get("experience", [])
    experience_items: List[ExperienceItem] = []

    current_role: Optional[str] = None
    current_company: Optional[str] = None
    current_duration: Optional[str] = None
    current_descriptions: List[str] = []

    def commit_item():
        nonlocal current_role, current_company, current_duration, current_descriptions
        if current_role or current_company:
            desc = " ".join(current_descriptions).strip() if current_descriptions else None
            experience_items.append(
                ExperienceItem(
                    role=current_role,
                    company=current_company,
                    duration=current_duration,
                    description=desc,
                )
            )
            current_role = None
            current_company = None
            current_duration = None
            current_descriptions = []

    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue

        # Check if this line is an experience header e.g. "Senior Software Engineer | TechCorp Inc. (2022 - Present)"
        is_bullet = line.startswith("-") or line.startswith("•") or line.startswith("*")

        if not is_bullet and ("|" in cleaned or " - " in cleaned or any(w in cleaned.lower() for w in ["intern", "engineer", "developer", "analyst", "manager", "specialist"])):
            # Check for duration
            duration = None
            dur_match = YEAR_PATTERN.search(cleaned)
            if dur_match:
                duration = dur_match.group(1).strip()

            # Parse role & company
            # E.g. "Senior Software Engineer | TechCorp Inc. (2022 - Present)"
            cleaned_no_dates = re.sub(YEAR_PATTERN, "", cleaned).strip(" ()-–—|")
            parts = [p.strip() for p in cleaned_no_dates.split("|") if p.strip()]

            if len(parts) >= 2:
                commit_item()
                current_role = parts[0]
                current_company = parts[1]
                current_duration = duration
                continue
            elif len(parts) == 1 and not is_bullet:
                # Could be "Role at Company"
                at_parts = re.split(r"\s+at\s+", parts[0], flags=re.I)
                if len(at_parts) == 2:
                    commit_item()
                    current_role = at_parts[0].strip()
                    current_company = at_parts[1].strip()
                    current_duration = duration
                    continue

        if is_bullet or (current_role is not None):
            bullet_text = cleaned.strip(" -•*").strip()
            if bullet_text:
                current_descriptions.append(bullet_text)

    commit_item()
    return experience_items


# ==============================================================================
# Main Intelligence Entrypoint
# ==============================================================================


def analyze_resume_text(text: str) -> CandidateProfile:
    """
    Main rule-based NLP extraction pipeline converting raw resume text
    into a structured CandidateProfile.
    """
    if not text or not text.strip():
        return CandidateProfile()

    # 1. Segment text into header and sections
    header_lines, sections = split_sections(text)

    # 2. Extract components
    name = extract_name(header_lines)
    summary = extract_summary(sections)
    skills = extract_skills(text, sections)
    education = extract_education(sections, text)
    projects = extract_projects(sections)
    certifications = extract_certifications(sections)
    experience = extract_experience(sections)

    return CandidateProfile(
        name=name,
        summary=summary,
        education=education,
        skills=skills,
        projects=projects,
        certifications=certifications,
        experience=experience,
    )
