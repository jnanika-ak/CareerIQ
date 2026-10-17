## CareerIQ — AI-Powered Job Intelligence & Career Copilot

**Turn your resume into a personalized career roadmap and get your dream job **

CareerIQ is a full-stack career intelligence platform that helps to analyzes resumes, evaluates job compatibility, identifies skill gaps, recommends career paths, and generates personalized learning roadmaps with interview readiness insights.

### Live Links

- **Live Application:** https://career-iq-ten.vercel.app
- **Backend API:** https://careeriq-rsb5.onrender.com
- **API Documentation:** https://careeriq-rsb5.onrender.com/docs

### Key Features

- **Resume Intelligence:** Upload PDF or DOCX resumes and extract candidate profiles, skills, education, experience, and projects.
- **Job Match Analysis:** Compare candidate skills against job descriptions and identify matched and missing requirements.
- **Career Recommendations:** Explore suitable career paths and role-fit scores.
- **Skill Gap Analysis:** Identify high-priority skills to improve for a target role.
- **Personalized Learning Roadmap:** Organize learning priorities into a structured plan.
- **Interview Readiness:** Assess preparation across technical skills, role alignment, skill coverage, and project readiness.
- **Persistent Data:** Store candidate and analysis records in PostgreSQL.

### Technology Stack

- **Frontend:** React, Vite, JavaScript, CSS
- **Backend:** Python, FastAPI, Uvicorn
- **Resume Processing:** PyMuPDF, python-docx
- **Database:** PostgreSQL, SQLAlchemy, psycopg
- **Deployment:** Vercel, Render, Superbase

## Database Architecture & Requirements

CareerIQ uses **PostgreSQL 18** for relational data persistence.

### Prerequisites
1. **PostgreSQL 18+** running on `localhost:5432`.
2. A database named `careeriq`.
   ```sql
   CREATE DATABASE careeriq;
   ```
3. A superuser or application user (default: `postgres`).

### Database Environment Configuration
Create or update `backend/.env` (using `backend/.env.example` as a template):

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/careeriq
```

> [!NOTE]
> If your password contains special characters (such as `@`, `/`, `#`), ensure it is URL-encoded (e.g. using `urllib.parse.quote_plus`).

---

## Relational Schema (PostgreSQL 18)

When the FastAPI backend starts, it automatically creates any missing tables safely without dropping or overwriting existing data:

| Table Name | Description | Key Fields |
| :--- | :--- | :--- |
| `candidates` | Core candidate identity and profile metadata | `id`, `name`, `email`, `phone`, `summary`, `target_role`, timestamps |
| `candidate_skills` | Extracted competencies associated with a candidate | `id`, `candidate_id` (FK), `skill_name`, `category`, `created_at` |
| `resume_analyses` | Raw resume document logs and text extracts | `id`, `candidate_id` (FK), `filename`, `file_type`, `extracted_text`, `created_at` |
| `job_analyses` | Segmented job descriptions & requirement benchmarks | `id`, `candidate_id` (FK), `job_title`, `job_description`, `created_at` |
| `job_matches` | Quantitative match evaluations against specific jobs | `id`, `candidate_id` (FK), `job_analysis_id` (FK), `match_percentage`, `match_strength`, `created_at` |
| `job_match_skills` | Matched vs. missing skill breakdown per match | `id`, `job_match_id` (FK), `skill_name`, `status` (`matched`/`missing`), `created_at` |
| `career_analyses` | Top career pathways & fit percentages | `id`, `candidate_id` (FK), `strongest_role`, `strongest_role_score`, `created_at` |
| `skill_gaps` | Prioritized competencies required for target career roles | `id`, `career_analysis_id` (FK), `skill_name`, `priority`, `current_level`, `target_level` |
| `learning_roadmaps` | Tailored multi-week milestone curricula | `id`, `candidate_id` (FK), `title`, `total_weeks`, `created_at` |
| `roadmap_weeks` | Weekly learning modules, estimated hours, and status | `id`, `roadmap_id` (FK), `week_number`, `title`, `priority`, `hours_per_week`, `status` |
| `interview_readiness` | Multi-factor weighted interview readiness scores | `id`, `candidate_id` (FK), `score`, `readiness_level`, sub-scores, `created_at` |

---
## System Architecture of CareerIQ

CareerIQ follows a full-stack architecture with a React frontend, a FastAPI backend, and a PostgreSQL database.

```text
                    ┌─────────────────────┐
                    │        User         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   React + Vite      │
                    │ Frontend (Vercel)   │
                    └──────────┬──────────┘
                               │ HTTP / REST API
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    │      (Render)       │
                    └──────────┬──────────┘
                               │ SQLAlchemy
                               ▼
                    ┌─────────────────────┐
                    │ PostgreSQL Database │
                    │     (Supabase)      │
                    └─────────────────────┘
```

### Architecture Components of CareerIQ

- **Frontend:** React and Vite provide the interactive dashboard and user interface.
- **Backend:** FastAPI exposes REST API endpoints for resume analysis, job matching, career recommendations, and interview preparation.
- **Database:** PostgreSQL stores candidate profiles, resume analysis history, job matches, skill gaps, and learning roadmap records.
- **ORM:** SQLAlchemy manages communication between the backend and the database.
- **Deployment:** Vercel hosts the frontend, while Render hosts the backend and Supabase provides the hosted PostgreSQL database.

## How to Run the Application

### 1. Backend Setup & Startup of this project

```powershell
# Navigate to the backend directory
cd backend

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Ensure backend/.env exists with your DATABASE_URL
# Example: DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/careeriq

# Start FastAPI server with live reloading
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The backend API will be available at:
- API Base: `http://127.0.0.1:8000`
- Interactive Swagger Docs: `http://127.0.0.1:8000/docs`
- Health Endpoint: `http://127.0.0.1:8000/api/health`

### 2. Frontend Setup & Startup

```powershell
# Navigate to the frontend directory
cd frontend

# Install node dependencies
npm install

# Start Vite dev server
npm run dev
```

The frontend dashboard will be available at:
`http://localhost:5173`

---

## Verifying PostgreSQL Persistence

### In pgAdmin 4:
1. Open **pgAdmin 4**.
2. Connect to **Servers** &rarr; **PostgreSQL 18**.
3. Expand **Databases** &rarr; **careeriq** &rarr; **Schemas** &rarr; **public** &rarr; **Tables**.
4. Confirm the presence of the 11 CareerIQ tables.
5. Right-click any table (e.g., `candidates` or `resume_analyses`) &rarr; **View/Edit Data** &rarr; **All Rows** to view persisted records.

### Via Command-Line or Python:
```powershell
cd backend
.\.venv\Scripts\python.exe -c "
from sqlalchemy import text
from app.db.session import engine

with engine.connect() as conn:
    print('Row counts:')
    for t in ['candidates', 'candidate_skills', 'resume_analyses', 'job_analyses', 'job_matches', 'career_analyses', 'learning_roadmaps', 'interview_readiness']:
        cnt = conn.execute(text(f'SELECT count(*) FROM {t}')).scalar()
        print(f'  {t}: {cnt}')
"
```

---

## API Endpoints Reference of the Project

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/` | `GET` | Service identity and status verification. |
| `/api/health` | `GET` | Reports backend health and PostgreSQL connectivity (`connected` / `disconnected`). |
| `/api/history` | `GET` | Returns recent chronological CareerIQ activity timeline persisted in PostgreSQL. |
| `/api/history/summary` | `GET` | Aggregated metrics summary (total resumes, jobs, matches, average score, skill gaps). |
| `/api/resume/upload` | `POST` | In-memory text extraction for `.pdf` and `.docx` files. |
| `/api/resume/analyze` | `POST` | Structured candidate profile extraction + persists to PostgreSQL. |
| `/api/job/analyze` | `POST` | Job requirement & competency segmentation + persists to PostgreSQL. |
| `/api/job/match` | `POST` | Match percentage and missing gap analysis + persists to PostgreSQL. |
| `/api/career/analyze` | `POST` | Multi-role scoring & priority skill gaps + persists to PostgreSQL. |
| `/api/learning-interview/analyze` | `POST` | 4-week learning roadmap & weighted readiness score + persists to PostgreSQL. |
