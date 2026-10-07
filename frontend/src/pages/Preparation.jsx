import { useState, useEffect } from 'react'
import { analyzeLearningInterview } from '../api/api'
import { Icon } from '../components/Icons'

export default function Preparation({
  candidateProfile,
  careerAnalysis,
  jobMatch,
  onNavigateToResume,
  onNavigateToCareerInsights,
}) {
  const [prepResult, setPrepResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState(null)

  useEffect(() => {
    // If no candidate profile, don't attempt request
    if (!candidateProfile || !candidateProfile.skills || candidateProfile.skills.length === 0) {
      setPrepResult(null)
      return
    }

    let isMounted = true
    const fetchData = async () => {
      setIsLoading(true)
      setErrorMessage(null)

      try {
        const data = await analyzeLearningInterview(
          candidateProfile,
          careerAnalysis,
          jobMatch
        )
        if (isMounted) {
          setPrepResult(data)
        }
      } catch (err) {
        console.error('[CareerIQ] Learning & interview analysis error:', err)
        if (isMounted) {
          setErrorMessage(
            err.message || 'Failed to load preparation data. Please verify the backend is running.'
          )
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    fetchData()

    return () => {
      isMounted = false
    }
  }, [candidateProfile, careerAnalysis, jobMatch])

  const getReadinessLevelClass = (level) => {
    switch (level) {
      case 'Interview Ready':
        return 'strength-excellent'
      case 'Strong Preparation':
        return 'strength-strong'
      case 'Needs Preparation':
        return 'strength-moderate'
      case 'Early Preparation':
        return 'strength-weak'
      case 'Not Ready Yet':
      default:
        return 'strength-low'
    }
  }

  const getPriorityClass = (priority) => {
    switch (priority) {
      case 'HIGH':
        return 'priority-high'
      case 'MEDIUM':
        return 'priority-medium'
      case 'LOW':
      default:
        return 'priority-low'
    }
  }

  // EMPTY STATE 1: No Resume Uploaded
  if (!candidateProfile || !candidateProfile.skills || candidateProfile.skills.length === 0) {
    return (
      <div className="prep-page">
        <div className="prep-page-header">
          <div className="page-header-text">
            <div className="page-badge">
              <Icon name="sparkles" size={14} />
              <span>Step 9: Learning Roadmap &amp; Interview Readiness</span>
            </div>
            <h2 className="prep-main-heading">Career Preparation</h2>
            <p className="prep-main-description">
              Build the skills you need and measure your interview readiness.
            </p>
          </div>
        </div>

        <div className="career-empty-card">
          <div className="empty-icon-circle">
            <Icon name="resume" size={32} />
          </div>
          <h3 className="empty-heading">Analyze your resume first to unlock Career Preparation.</h3>
          <p className="empty-subtext">
            CareerIQ needs your candidate profile skills and target career direction to construct a
            personalized 4-week roadmap and benchmark your interview readiness.
          </p>
          <div className="empty-action-row">
            <button
              type="button"
              className="btn btn-primary"
              onClick={onNavigateToResume}
            >
              <Icon name="upload" size={16} />
              Analyze Resume
            </button>
          </div>
        </div>
      </div>
    )
  }

  // EMPTY STATE 2: Resume uploaded but Career Intelligence not generated and no skills
  if (!careerAnalysis && (!candidateProfile.skills || candidateProfile.skills.length === 0)) {
    return (
      <div className="prep-page">
        <div className="prep-page-header">
          <div className="page-header-text">
            <div className="page-badge">
              <Icon name="sparkles" size={14} />
              <span>Step 9: Learning Roadmap &amp; Interview Readiness</span>
            </div>
            <h2 className="prep-main-heading">Career Preparation</h2>
            <p className="prep-main-description">
              Build the skills you need and measure your interview readiness.
            </p>
          </div>
        </div>

        <div className="career-empty-card">
          <div className="empty-icon-circle">
            <Icon name="careerPaths" size={32} />
          </div>
          <h3 className="empty-heading">Complete Career Intelligence first.</h3>
          <p className="empty-subtext">
            Generate your skill gap analysis and role match rankings in Career Insights to align your
            preparation goals with your target pathway.
          </p>
          <div className="empty-action-row">
            <button
              type="button"
              className="btn btn-primary"
              onClick={onNavigateToCareerInsights}
            >
              <Icon name="careerPaths" size={16} />
              Career Insights
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="prep-page">
      {/* Page Header */}
      <div className="prep-page-header">
        <div className="page-header-text">
          <div className="page-badge">
            <Icon name="sparkles" size={14} />
            <span>Step 9: Learning Roadmap &amp; Interview Readiness</span>
          </div>
          <h2 className="prep-main-heading">Career Preparation</h2>
          <p className="prep-main-description">
            Build the skills you need and measure your interview readiness.
          </p>
        </div>
      </div>

      {/* Candidate Context Banner */}
      <div className="prep-context-banner">
        <div className="context-left">
          <div className="context-avatar-badge">
            <Icon name="checkCircle" size={18} />
          </div>
          <div className="context-info">
            <span className="context-title">
              Candidate: <strong>{prepResult?.candidate_name || candidateProfile.name || 'Candidate'}</strong>
            </span>
            <span className="context-subtext">
              Target Pathway: <strong>{prepResult?.target_role || 'Target Role'}</strong>
              {jobMatch ? ` &bull; Targeted Job: ${jobMatch.job_title || 'Target Job'}` : ''}
            </span>
          </div>
        </div>

        <div className="context-actions">
          {onNavigateToCareerInsights && (
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={onNavigateToCareerInsights}
              title="Review Skill Gaps and Career Insights"
            >
              <Icon name="careerPaths" size={14} />
              Career Insights
            </button>
          )}
        </div>
      </div>

      {/* Error Message */}
      {errorMessage && (
        <div className="upload-error-banner" role="alert">
          <Icon name="alertTriangle" size={18} className="error-icon" />
          <div className="error-content">
            <strong>Error:</strong> {errorMessage}
          </div>
        </div>
      )}

      {/* Loading Skeleton */}
      {isLoading && (
        <div className="prep-loading-card">
          <span className="spinner-dot" />
          <p>Generating your personalized 4-week roadmap and calculating interview readiness...</p>
        </div>
      )}

      {!isLoading && prepResult && (
        <div className="prep-content-layout">
          {/* Top Row: Section 4 (Target Role Callout) & Section 1 (Interview Readiness Hero) */}
          <div className="prep-top-grid">
            {/* SECTION 4: TARGET ROLE CALLOUT */}
            <section className="target-role-callout-card" aria-label="Target Role Information">
              <div className="target-role-badge">
                <Icon name="target" size={14} />
                <span>Preparing For</span>
              </div>
              <h3 className="target-role-heading">{prepResult.target_role}</h3>
              <div className="target-role-stats-row">
                <span className="role-stat-pill">
                  Role Match: <strong>{prepResult.learning_roadmap.target_role_match_percentage}%</strong>
                </span>
                <span className="role-stat-pill">
                  Roadmap Duration: <strong>4 Weeks</strong>
                </span>
              </div>
              <p className="target-role-desc">
                {prepResult.learning_roadmap.summary}
              </p>
            </section>

            {/* SECTION 1: INTERVIEW READINESS SCORE CARD */}
            <section className="interview-readiness-hero-card" aria-label="Interview Readiness Score">
              <div className="readiness-score-header">
                <div className="readiness-title-wrap">
                  <div className="readiness-icon-badge">
                    <Icon name="award" size={18} />
                  </div>
                  <div>
                    <h3 className="readiness-heading">Interview Readiness</h3>
                    <span className="readiness-sub">Weighted Evaluation</span>
                  </div>
                </div>

                <div className="readiness-overall-pill-group">
                  <span className="readiness-number">{prepResult.interview_readiness.overall_score}%</span>
                  <span className={`match-strength-pill ${getReadinessLevelClass(prepResult.interview_readiness.readiness_level)}`}>
                    {prepResult.interview_readiness.readiness_level}
                  </span>
                </div>
              </div>

              {/* Component Progress Bars */}
              <div className="readiness-components-list">
                {prepResult.interview_readiness.components.map((comp, idx) => (
                  <div key={idx} className="readiness-component-item">
                    <div className="component-meta-row">
                      <span className="component-name">
                        {comp.name}{' '}
                        <span className="component-weight">({Math.round(comp.weight * 100)}% weight)</span>
                      </span>
                      <span className="component-score-val">{comp.score}%</span>
                    </div>

                    <div className="progress-bar-track">
                      <div
                        className="progress-bar-fill"
                        style={{ width: `${comp.score}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              {prepResult.interview_readiness.project_readiness_note && (
                <div className="project-readiness-footer-note">
                  <Icon name="fileText" size={13} />
                  <span>{prepResult.interview_readiness.project_readiness_note}</span>
                </div>
              )}
            </section>
          </div>

          {/* SECTION 2: PREPARATION PRIORITIES */}
          <section className="prep-priorities-section" aria-label="Interview Preparation Priorities">
            <div className="section-header-bar">
              <div className="header-title-wrap">
                <Icon name="alertTriangle" size={18} className="header-icon" />
                <h3 className="section-title">Interview Preparation Priorities</h3>
              </div>
              <span className="badge-counter">
                {prepResult.interview_readiness.preparation_areas.length} Focus Areas
              </span>
            </div>

            <div className="prep-areas-grid">
              {prepResult.interview_readiness.preparation_areas.map((area, idx) => (
                <div key={idx} className={`prep-area-card ${area.is_gap ? 'is-gap-card' : ''}`}>
                  <div className="area-card-top">
                    <span className="area-step-number">#{idx + 1}</span>
                    <span className={`gap-priority-pill ${getPriorityClass(area.priority)}`}>
                      {area.priority} PRIORITY
                    </span>
                  </div>

                  <h4 className="area-title">{area.area}</h4>
                  <p className="area-desc">{area.description}</p>

                  <div className="area-status-footer">
                    {area.is_gap ? (
                      <span className="area-tag gap-tag">
                        <Icon name="alertTriangle" size={12} />
                        Skill Gap Focus
                      </span>
                    ) : (
                      <span className="area-tag present-tag">
                        <Icon name="checkCircle" size={12} />
                        Reinforce Strengths
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* SECTION 3: 4-WEEK LEARNING ROADMAP */}
          <section className="learning-roadmap-section" aria-label="4-Week Learning Roadmap">
            <div className="section-header-bar">
              <div className="header-title-wrap">
                <Icon name="roadmap" size={18} className="header-icon" />
                <h3 className="section-title">4-Week Personalized Learning Roadmap</h3>
              </div>
              <span className="badge-counter">Weekly Milestones</span>
            </div>

            <div className="roadmap-timeline-grid">
              {prepResult.learning_roadmap.weeks.map((week) => (
                <div
                  key={week.week_number}
                  className={`roadmap-week-card ${week.status === 'Current' ? 'week-current' : 'week-upcoming'}`}
                >
                  <div className="week-card-header">
                    <div className="week-tag-wrap">
                      <span className="week-number-badge">WEEK {week.week_number}</span>
                      <span className={`week-status-pill ${week.status === 'Current' ? 'current' : 'upcoming'}`}>
                        {week.status.toUpperCase()}
                      </span>
                    </div>

                    <span className="week-hours-tag">
                      <Icon name="target" size={12} />
                      {week.estimated_hours}
                    </span>
                  </div>

                  <h4 className="week-title">{week.title}</h4>

                  <div className="week-skills-pills">
                    {week.skills.map((skill, sIdx) => (
                      <span key={sIdx} className="week-skill-chip">
                        {skill}
                      </span>
                    ))}
                    <span className={`gap-priority-pill ${getPriorityClass(week.priority)}`}>
                      {week.priority}
                    </span>
                  </div>

                  <div className="week-objective-box">
                    <span className="objective-label">Objective:</span>
                    <p className="objective-text">{week.objective}</p>
                  </div>

                  <div className="week-activities-group">
                    <span className="activities-label">Actionable Activities:</span>
                    <ul className="activities-list">
                      {week.activities.map((act, aIdx) => (
                        <li key={aIdx} className="activity-item">
                          <span className="activity-bullet" />
                          <span>{act}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      )}
    </div>
  )
}
