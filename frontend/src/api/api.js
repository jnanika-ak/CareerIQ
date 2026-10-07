/**
 * CareerIQ Frontend API Client
 * Centralized API utility for communicating with the CareerIQ FastAPI backend.
 */

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

/**
 * Health check response object
 * @typedef {Object} HealthCheckResponse
 * @property {string} status - e.g. "healthy"
 * @property {string} service - e.g. "CareerIQ Backend"
 */

/**
 * Fetches the backend health status.
 * Target endpoint: GET http://127.0.0.1:8000/api/health
 *
 * @returns {Promise<HealthCheckResponse>} The backend health payload.
 * @throws {Error} If request fails or HTTP status is non-2xx.
 */
export async function getBackendHealth() {
  const url = `${API_BASE_URL}/api/health`;

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(
      `Backend health check failed with HTTP ${response.status} (${response.statusText})`
    );
  }

  const data = await response.json();
  return data;
}

/**
 * Uploads a resume file (PDF or DOCX) to the backend for text extraction.
 * Target endpoint: POST http://127.0.0.1:8000/api/resume/upload
 *
 * @param {File} file - The resume file object to upload
 * @returns {Promise<{ filename: string, file_type: string, characters: number, pages: number|null, text: string }>}
 * @throws {Error} If upload fails, backend offline, or validation rejects the file
 */
export async function uploadResume(file) {
  if (!file) {
    throw new Error('Please select a resume file to upload.');
  }

  const formData = new FormData();
  formData.append('file', file);

  const url = `${API_BASE_URL}/api/resume/upload`;

  let response;
  try {
    response = await fetch(url, {
      method: 'POST',
      body: formData,
    });
  } catch {
    throw new Error(
      'Unable to connect to the CareerIQ backend. Please verify the backend server is running.'
    );
  }

  if (!response.ok) {
    let errorMessage = `Server error (${response.status})`;
    try {
      const errorData = await response.json();
      if (errorData && errorData.detail) {
        errorMessage = errorData.detail;
      }
    } catch {
      errorMessage = response.statusText || errorMessage;
    }
    throw new Error(errorMessage);
  }

  return response.json();
}

/**
 * Analyzes a resume file (PDF or DOCX) to extract raw text and a structured candidate profile.
 * Target endpoint: POST http://127.0.0.1:8000/api/resume/analyze
 *
 * @param {File} file - The resume file to analyze
 * @returns {Promise<{
 *   filename: string,
 *   file_type?: string,
 *   characters?: number,
 *   pages?: number|null,
 *   text?: string,
 *   profile: {
 *     name: string|null,
 *     summary: string|null,
 *     education: Array<{ degree?: string, field?: string, institution?: string, year?: string }>,
 *     skills: string[],
 *     projects: Array<{ name: string, description?: string }>,
 *     certifications: string[],
 *     experience: Array<{ role?: string, company?: string, duration?: string, description?: string }>
 *   }
 * }>}
 */
export async function analyzeResume(file) {
  if (!file) {
    throw new Error('Please select a resume file to analyze.');
  }

  const formData = new FormData();
  formData.append('file', file);

  const url = `${API_BASE_URL}/api/resume/analyze`;

  let response;
  try {
    response = await fetch(url, {
      method: 'POST',
      body: formData,
    });
  } catch {
    throw new Error(
      'Unable to connect to the CareerIQ backend. Please verify the backend server is running.'
    );
  }

  if (!response.ok) {
    let errorMessage = `Server error (${response.status})`;
    try {
      const errorData = await response.json();
      if (errorData && errorData.detail) {
        errorMessage = errorData.detail;
      }
    } catch {
      errorMessage = response.statusText || errorMessage;
    }
    throw new Error(errorMessage);
  }

  return response.json();
}

/**
 * Analyzes a job description and matches it against candidate skills.
 * Target endpoint: POST http://127.0.0.1:8000/api/job/match
 *
 * @param {Object} payload
 * @param {string} payload.job_description - Pasted job description text
 * @param {string} [payload.job_title] - Optional job title
 * @param {string[]} [payload.candidate_skills] - Array of candidate skills
 * @param {string} [payload.candidate_name] - Candidate name
 * @returns {Promise<{
 *   job_title: string|null,
 *   match_percentage: number,
 *   match_strength: string,
 *   total_required: number,
 *   total_matched: number,
 *   matched_skills: string[],
 *   missing_skills: string[],
 *   preferred_skills: string[],
 *   matched_preferred_skills: string[],
 *   missing_preferred_skills: string[],
 *   all_job_skills: string[],
 *   candidate_skills_count: number
 * }>}
 */
export async function matchJobDescription({
  job_description,
  job_title,
  candidate_skills = [],
  candidate_name,
}) {
  if (!job_description || !job_description.trim()) {
    throw new Error('Please enter or paste a job description.');
  }

  const url = `${API_BASE_URL}/api/job/match`;

  let response;
  try {
    response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({
        job_description,
        job_title,
        candidate_skills,
        candidate_name,
      }),
    });
  } catch {
    throw new Error(
      'Unable to connect to the CareerIQ backend. Please verify the backend server is running.'
    );
  }

  if (!response.ok) {
    let errorMessage = `Server error (${response.status})`;
    try {
      const errorData = await response.json();
      if (errorData && errorData.detail) {
        errorMessage = errorData.detail;
      }
    } catch {
      errorMessage = response.statusText || errorMessage;
    }
    throw new Error(errorMessage);
  }

  return response.json();
}

/**
 * Step 8: Analyzes candidate profile and optional job match to compute skill gaps
 * and ranked career role recommendations.
 * Target endpoint: POST http://127.0.0.1:8000/api/career/analyze
 *
 * @param {Object} [candidateProfile] - Active candidate profile
 * @param {Object} [jobMatch] - Optional job match result
 * @returns {Promise<{
 *   skill_gaps: Array<{ skill: string, current_level: string, target_level: string, gap: string, priority: string, reason: string, target_role: string|null }>,
 *   top_priority_gaps: Array<{ skill: string, current_level: string, target_level: string, gap: string, priority: string, reason: string, target_role: string|null }>,
 *   recommended_roles: Array<{ role: string, match_percentage: number, match_strength: string, matched_skills: string[], missing_skills: string[], total_role_skills: number, description: string, demand_level: string, explanation: string }>,
 *   strongest_fit_role: Object|null,
 *   total_gaps_count: number,
 *   high_priority_count: number,
 *   medium_priority_count: number,
 *   low_priority_count: number,
 *   is_profile_only: boolean,
 *   candidate_name: string,
 *   target_job_title: string|null
 * }>}
 */
export async function analyzeCareer(candidateProfile, jobMatch) {
  const url = `${API_BASE_URL}/api/career/analyze`;

  let response;
  try {
    response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({
        candidate_profile: candidateProfile || null,
        job_match: jobMatch || null,
      }),
    });
  } catch {
    throw new Error(
      'Unable to connect to the CareerIQ backend. Please verify the backend server is running.'
    );
  }

  if (!response.ok) {
    let errorMessage = `Server error (${response.status})`;
    try {
      const errorData = await response.json();
      if (errorData && errorData.detail) {
        errorMessage = errorData.detail;
      }
    } catch {
      errorMessage = response.statusText || errorMessage;
    }
    throw new Error(errorMessage);
  }

  return response.json();
}

/**
 * Step 9: Analyzes candidate profile, career analysis, and optional job match
 * to generate a 4-week personalized learning roadmap and interview readiness score.
 * Target endpoint: POST http://127.0.0.1:8000/api/learning-interview/analyze
 *
 * @param {Object} [candidateProfile] - Active candidate profile
 * @param {Object} [careerAnalysis] - Active career intelligence analysis
 * @param {Object} [jobMatch] - Optional job match result
 * @returns {Promise<{
 *   learning_roadmap: {
 *     target_role: string,
 *     target_role_match_percentage: number,
 *     total_weeks: number,
 *     weeks: Array<{
 *       week_number: number,
 *       title: string,
 *       skills: string[],
 *       objective: string,
 *       activities: string[],
 *       priority: string,
 *       estimated_hours: string,
 *       status: string
 *     }>,
 *     summary: string
 *   },
 *   interview_readiness: {
 *     overall_score: number,
 *     readiness_level: string,
 *     target_role: string,
 *     technical_skills_score: number,
 *     role_alignment_score: number,
 *     skill_coverage_score: number,
 *     project_readiness_score: number,
 *     components: Array<{ name: string, score: number, weight: number, description: string }>,
 *     preparation_areas: Array<{ area: string, priority: string, is_gap: boolean, description: string }>,
 *     project_readiness_note: string
 *   },
 *   target_role: string,
 *   candidate_name: string
 * }>}
 */
export async function analyzeLearningInterview(candidateProfile, careerAnalysis, jobMatch) {
  const url = `${API_BASE_URL}/api/learning-interview/analyze`;

  let response;
  try {
    response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({
        candidate_profile: candidateProfile || null,
        career_analysis: careerAnalysis || null,
        job_match: jobMatch || null,
      }),
    });
  } catch {
    throw new Error(
      'Unable to connect to the CareerIQ backend. Please verify the backend server is running.'
    );
  }

  if (!response.ok) {
    let errorMessage = `Server error (${response.status})`;
    try {
      const errorData = await response.json();
      if (errorData && errorData.detail) {
        errorMessage = errorData.detail;
      }
    } catch {
      errorMessage = response.statusText || errorMessage;
    }
    throw new Error(errorMessage);
  }

  return response.json();
}

/**
 * Fetches recent activity history stored in PostgreSQL.
 * Target endpoint: GET http://127.0.0.1:8000/api/history
 *
 * @param {number} [limit=20] - Maximum number of recent events to retrieve
 * @returns {Promise<Array<Object>>} List of chronological activity items
 */
export async function fetchActivityHistory(limit = 20) {
  const url = `${API_BASE_URL}/api/history?limit=${limit}`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    });

    if (!response.ok) {
      return [];
    }

    return await response.json();
  } catch (err) {
    console.warn('Failed to fetch activity history from backend:', err);
    return [];
  }
}

/**
 * Fetches aggregated statistics and history metrics summary.
 * Target endpoint: GET http://127.0.0.1:8000/api/history/summary
 *
 * @returns {Promise<Object>} Aggregated metrics summary
 */
export async function fetchHistorySummary() {
  const url = `${API_BASE_URL}/api/history/summary`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    });

    if (!response.ok) {
      return null;
    }

    return await response.json();
  } catch (err) {
    console.warn('Failed to fetch history summary from backend:', err);
    return null;
  }
}

