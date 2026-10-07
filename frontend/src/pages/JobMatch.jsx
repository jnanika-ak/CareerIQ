import { useState } from 'react'
import { matchJobDescription } from '../api/api'
import { Icon } from '../components/Icons'

const SAMPLE_DATA_ANALYST_JOB = `Senior Data Analyst
Department: Analytics & Business Intelligence

About the Role:
We are looking for a Senior Data Analyst to join our high-growth analytics team. You will partner with business stakeholders, build enterprise data models, and drive data-backed decision making across the organization.

Requirements:
- Strong proficiency in SQL and Python for data analysis and ETL scripting.
- Advanced experience with Power BI and Excel for executive reporting.
- Experience with Relational Databases (PostgreSQL or MySQL).

Preferred Qualifications:
- Familiarity with Tableau dashboards and cloud data warehouses.
- Solid understanding of Statistics, A/B testing, and Data Visualization best practices.
`

const SAMPLE_FULL_STACK_JOB = `Senior Full-Stack Engineer
Team: Core Platform Engineering

Requirements:
- Strong proficiency in Python, FastAPI, and React.
- Demonstrated experience with TypeScript, Node.js, and REST APIs.
- Experience building scalable services with Docker, Git, and PostgreSQL.

Preferred Qualifications:
- Familiarity with AWS cloud architecture and CI/CD automation pipelines.
- Experience with Redis caching and microservice architecture.
`

export default function JobMatch({
  candidateProfile,
  onNavigateToResume,
  onJobMatchComplete,
  onNavigateToCareerInsights,
}) {
  const [jobTitle, setJobTitle] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [matchResult, setMatchResult] = useState(null)
  const [errorMessage, setErrorMessage] = useState(null)

  // Use candidate skills from active analyzed profile, or fallback to default skillset
  const activeSkills = candidateProfile?.skills?.length
    ? candidateProfile.skills
    : ['Python', 'SQL', 'Power BI', 'Excel', 'Pandas', 'Machine Learning']

  const candidateName = candidateProfile?.name || 'Alex Morgan'

  const handleAnalyzeJob = async () => {
    if (!jobDescription.trim()) {
      setErrorMessage('Please paste or type a job description to analyze.')
      return
    }

    setIsAnalyzing(true)
    setErrorMessage(null)

    try {
      const result = await matchJobDescription({
        job_description: jobDescription,
        job_title: jobTitle.trim() || undefined,
        candidate_skills: activeSkills,
        candidate_name: candidateName,
      })
      setMatchResult(result)
      if (onJobMatchComplete) {
        onJobMatchComplete(result)
      }
    } catch (err) {
      console.error('[CareerIQ] Job matching failed:', err)
      setErrorMessage(
        err.message || 'Failed to analyze job description. Please ensure backend is running.'
      )
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleClear = () => {
    setJobTitle('')
    setJobDescription('')
    setMatchResult(null)
    setErrorMessage(null)
  }

  const getStrengthClass = (strength) => {
    switch (strength) {
      case 'Excellent Match':
        return 'strength-excellent'
      case 'Strong Match':
        return 'strength-strong'
      case 'Moderate Match':
        return 'strength-moderate'
      case 'Weak Match':
        return 'strength-weak'
      case 'Low Match':
      default:
        return 'strength-low'
    }
  }

  return (
    <div className="job-match-page">
      {/* Page Header */}
      <div className="job-page-header">
        <div className="page-header-text">
          <div className="page-badge">
            <Icon name="sparkles" size={14} />
            <span>Step 7: Resume-to-Job Match Engine</span>
          </div>
          <h2 className="job-main-heading">Job Match Analyzer</h2>
          <p className="job-main-description">
            Compare target job descriptions against your candidate profile to measure compatibility and uncover key skill gaps.
          </p>
        </div>
      </div>

      {/* Candidate Profile Context Banner */}
      <div className="candidate-context-banner">
        <div className="context-left">
          <div className="context-avatar-badge">
            <Icon name="checkCircle" size={18} />
          </div>
          <div className="context-info">
            <span className="context-title">
              Target Candidate: <strong>{candidateName}</strong>
            </span>
            <span className="context-subtext">
              Active profile loaded with <strong>{activeSkills.length} skills</strong>
              {candidateProfile?.skills?.length ? ' (from analyzed resume)' : ' (default profile)'}
            </span>
          </div>
        </div>

        {onNavigateToResume && (
          <button
            type="button"
            className="btn btn-ghost btn-sm"
            onClick={onNavigateToResume}
            title="Update resume profile"
          >
            <Icon name="fileText" size={14} />
            Change Resume
          </button>
        )}
      </div>

      {/* Main Grid: Input Card & Results Card */}
      <div className="job-match-layout">
        {/* Input Form Section */}
        <section className="job-input-card">
          <div className="card-header-bar">
            <div className="card-title-group">
              <Icon name="briefcase" size={18} className="card-header-icon" />
              <h3 className="card-heading">Target Job Description</h3>
            </div>

            <div className="sample-buttons-group">
              <span className="sample-label">Try sample:</span>
              <button
                type="button"
                className="btn-sample"
                onClick={() => {
                  setJobTitle('Senior Data Analyst')
                  setJobDescription(SAMPLE_DATA_ANALYST_JOB)
                  setErrorMessage(null)
                }}
              >
                Data Analyst
              </button>
              <button
                type="button"
                className="btn-sample"
                onClick={() => {
                  setJobTitle('Senior Full-Stack Engineer')
                  setJobDescription(SAMPLE_FULL_STACK_JOB)
                  setErrorMessage(null)
                }}
              >
                Full-Stack
              </button>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="job-title-input" className="form-label">
              Job Title <span className="label-optional">(Optional)</span>
            </label>
            <input
              id="job-title-input"
              type="text"
              className="form-input"
              placeholder="e.g. Senior Data Analyst or Full-Stack Developer"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              disabled={isAnalyzing}
            />
          </div>

          <div className="form-group">
            <label htmlFor="job-desc-input" className="form-label">
              Paste Job Description <span className="label-required">*</span>
            </label>
            <textarea
              id="job-desc-input"
              className="form-textarea"
              rows={9}
              placeholder="Paste the full job posting requirements here (responsibilities, required skills, preferred qualifications)..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              disabled={isAnalyzing}
            />
          </div>

          {errorMessage && (
            <div className="upload-error-banner" role="alert">
              <Icon name="alertTriangle" size={18} className="error-icon" />
              <div className="error-content">
                <strong>Error:</strong> {errorMessage}
              </div>
            </div>
          )}

          <div className="card-actions-row">
            <button
              type="button"
              className="btn btn-ghost"
              onClick={handleClear}
              disabled={isAnalyzing || (!jobTitle && !jobDescription && !matchResult)}
            >
              Clear
            </button>

            <button
              type="button"
              className="btn btn-primary analyze-job-btn"
              onClick={handleAnalyzeJob}
              disabled={isAnalyzing}
            >
              {isAnalyzing ? (
                <>
                  <span className="spinner-dot" />
                  Analyzing Job Requirements...
                </>
              ) : (
                <>
                  <Icon name="sparkles" size={16} />
                  Analyze Job Match
                </>
              )}
            </button>
          </div>
        </section>

        {/* Results Section */}
        {matchResult && (
          <section className="job-results-card">
            {/* Match Score Hero Card */}
            <div className="match-score-hero">
              <div className="score-visual-circle">
                <span className="score-number">{matchResult.match_percentage}%</span>
                <span className="score-sub">Match</span>
              </div>

              <div className="score-details">
                <div className="strength-badge-row">
                  <span className={`match-strength-pill ${getStrengthClass(matchResult.match_strength)}`}>
                    {matchResult.match_strength}
                  </span>
                  {matchResult.job_title && (
                    <span className="matched-job-title">{matchResult.job_title}</span>
                  )}
                </div>

                <p className="score-summary-text">
                  Your candidate profile satisfies{' '}
                  <strong>
                    {matchResult.total_matched} of {matchResult.total_required} required competencies
                  </strong>{' '}
                  identified in this job description.
                </p>

                <div className="match-stats-pills">
                  <span className="stat-pill">
                    Required Skills: <strong>{matchResult.total_required}</strong>
                  </span>
                  <span className="stat-pill">
                    Matched: <strong>{matchResult.total_matched}</strong>
                  </span>
                  <span className="stat-pill">
                    Missing: <strong>{matchResult.missing_skills.length}</strong>
                  </span>
                  {matchResult.preferred_skills.length > 0 && (
                    <span className="stat-pill">
                      Preferred: <strong>{matchResult.preferred_skills.length}</strong>
                    </span>
                  )}
                </div>

                {onNavigateToCareerInsights && (
                  <div className="hero-action-row" style={{ marginTop: '12px' }}>
                    <button
                      type="button"
                      className="btn btn-primary btn-sm"
                      onClick={onNavigateToCareerInsights}
                      title="View Career Intelligence & Skill Gap recommendations"
                    >
                      <Icon name="careerPaths" size={15} />
                      View Career Intelligence &amp; Skill Gaps &rarr;
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Skills Breakdown Grid */}
            <div className="match-skills-breakdown">
              {/* Matched Required Skills */}
              <div className="skills-column-card matched-card">
                <div className="column-header">
                  <div className="column-title-wrap">
                    <span className="dot-indicator green" />
                    <h4 className="column-title">Matched Required Skills</h4>
                  </div>
                  <span className="count-tag green">{matchResult.matched_skills.length}</span>
                </div>

                <div className="column-body">
                  {matchResult.matched_skills.length > 0 ? (
                    <div className="skill-tags-flow">
                      {matchResult.matched_skills.map((skill, idx) => (
                        <span key={idx} className="skill-match-tag matched">
                          <Icon name="checkCircle" size={13} />
                          {skill}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="empty-subtext">No required skills were matched.</p>
                  )}
                </div>
              </div>

              {/* Missing Skills (Skill Gaps) */}
              <div className="skills-column-card missing-card">
                <div className="column-header">
                  <div className="column-title-wrap">
                    <span className="dot-indicator red" />
                    <h4 className="column-title">Missing Required Skills (Gaps)</h4>
                  </div>
                  <span className="count-tag red">{matchResult.missing_skills.length}</span>
                </div>

                <div className="column-body">
                  {matchResult.missing_skills.length > 0 ? (
                    <div className="skill-tags-flow">
                      {matchResult.missing_skills.map((skill, idx) => (
                        <span key={idx} className="skill-match-tag missing">
                          <Icon name="alertTriangle" size={13} />
                          {skill}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="empty-subtext success">
                      All required skills matched! Zero required gaps.
                    </p>
                  )}
                </div>
              </div>

              {/* Preferred Skills (if detected) */}
              {matchResult.preferred_skills.length > 0 && (
                <div className="skills-column-card preferred-card">
                  <div className="column-header">
                    <div className="column-title-wrap">
                      <span className="dot-indicator blue" />
                      <h4 className="column-title">Preferred / Nice-to-Have Skills</h4>
                    </div>
                    <span className="count-tag blue">{matchResult.preferred_skills.length}</span>
                  </div>

                  <div className="column-body">
                    <div className="skill-tags-flow">
                      {matchResult.matched_preferred_skills.map((skill, idx) => (
                        <span key={`pref-m-${idx}`} className="skill-match-tag preferred-matched">
                          <Icon name="checkCircle" size={13} />
                          {skill} (Bonus Match)
                        </span>
                      ))}
                      {matchResult.missing_preferred_skills.map((skill, idx) => (
                        <span key={`pref-u-${idx}`} className="skill-match-tag preferred-missing">
                          {skill} (Optional)
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </section>
        )}
      </div>
    </div>
  )
}
