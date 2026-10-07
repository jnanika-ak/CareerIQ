import { useState, useEffect } from 'react'
import { analyzeCareer } from '../api/api'
import { Icon } from '../components/Icons'

export default function CareerInsights({
  candidateProfile,
  jobMatch,
  onNavigateToResume,
  onNavigateToJobMatch,
  onCareerAnalysisComplete,
  onNavigateToPreparation,
}) {
  const [careerResult, setCareerResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState(null)

  // Fetch career intelligence whenever candidateProfile or jobMatch changes
  useEffect(() => {
    if (!candidateProfile || !candidateProfile.skills || candidateProfile.skills.length === 0) {
      setCareerResult(null)
      return
    }

    let isMounted = true
    const fetchData = async () => {
      setIsLoading(true)
      setErrorMessage(null)

      try {
        const data = await analyzeCareer(candidateProfile, jobMatch)
        if (isMounted) {
          setCareerResult(data)
          if (onCareerAnalysisComplete) {
            onCareerAnalysisComplete(data)
          }
        }
      } catch (err) {
        console.error('[CareerIQ] Career analysis error:', err)
        if (isMounted) {
          setErrorMessage(
            err.message || 'Failed to load career intelligence. Please verify the backend is running.'
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
  }, [candidateProfile, jobMatch])

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

  const getStrengthClass = (strength) => {
    switch (strength) {
      case 'Excellent Fit':
        return 'strength-excellent'
      case 'Strong Fit':
        return 'strength-strong'
      case 'Good Potential':
        return 'strength-moderate'
      case 'Developing Fit':
        return 'strength-weak'
      case 'Early Fit':
      default:
        return 'strength-low'
    }
  }

  // 1. Empty State: No Candidate Profile Uploaded
  if (!candidateProfile || !candidateProfile.skills || candidateProfile.skills.length === 0) {
    return (
      <div className="career-insights-page">
        <div className="career-page-header">
          <div className="page-header-text">
            <div className="page-badge">
              <Icon name="sparkles" size={14} />
              <span>Step 8: Skill Gap &amp; Career Intelligence</span>
            </div>
            <h2 className="career-main-heading">Career Intelligence</h2>
            <p className="career-main-description">
              Understand your skill gaps and discover roles that match your current profile.
            </p>
          </div>
        </div>

        <div className="career-empty-card">
          <div className="empty-icon-circle">
            <Icon name="resume" size={32} />
          </div>
          <h3 className="empty-heading">Analyze your resume first to unlock Career Intelligence.</h3>
          <p className="empty-subtext">
            CareerIQ needs your candidate profile skills to calculate personalized role compatibility,
            detect competency gaps, and prioritize learning goals.
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

  return (
    <div className="career-insights-page">
      {/* Page Header */}
      <div className="career-page-header">
        <div className="page-header-text">
          <div className="page-badge">
            <Icon name="sparkles" size={14} />
            <span>Step 8: Skill Gap &amp; Career Intelligence</span>
          </div>
          <h2 className="career-main-heading">Career Intelligence</h2>
          <p className="career-main-description">
            Understand your skill gaps and discover roles that match your current profile.
          </p>
        </div>
      </div>

      {/* Candidate & Job Context Banner */}
      <div className="career-context-banner">
        <div className="context-left">
          <div className="context-avatar-badge">
            <Icon name="checkCircle" size={18} />
          </div>
          <div className="context-info">
            <span className="context-title">
              Candidate: <strong>{candidateProfile.name || 'Alex Morgan'}</strong>
            </span>
            <span className="context-subtext">
              <strong>{candidateProfile.skills.length} skills</strong> active &bull;{' '}
              {jobMatch
                ? `Job Match: ${jobMatch.job_title || 'Target Job'} (${jobMatch.match_percentage}% match)`
                : 'Profile-based Career Benchmark mode'}
            </span>
          </div>
        </div>

        <div className="context-actions">
          {onNavigateToPreparation && (
            <button
              type="button"
              className="btn btn-primary btn-sm"
              onClick={onNavigateToPreparation}
              title="View your 4-week roadmap and interview readiness"
            >
              <Icon name="roadmap" size={14} />
              Preparation Roadmap &rarr;
            </button>
          )}
          {!jobMatch && onNavigateToJobMatch && (
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={onNavigateToJobMatch}
              title="Add a target job for higher precision gap prioritization"
            >
              <Icon name="jobMatch" size={14} />
              Add Target Job
            </button>
          )}
          {onNavigateToResume && (
            <button
              type="button"
              className="btn btn-ghost btn-sm"
              onClick={onNavigateToResume}
              title="Update candidate profile"
            >
              <Icon name="fileText" size={14} />
              Change Resume
            </button>
          )}
        </div>
      </div>

      {/* Error Banner */}
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
        <div className="career-loading-card">
          <span className="spinner-dot" />
          <p>Analyzing skill gaps and calculating career role benchmarks...</p>
        </div>
      )}

      {/* Results Content */}
      {!isLoading && careerResult && (
        <div className="career-content-layout">
          {/* SECTION 4: CURRENT BEST FIT HERO (Placed prominently) */}
          {careerResult.strongest_fit_role && (
            <section className="current-best-fit-card" aria-label="Current Best Fit Role">
              <div className="best-fit-badge-tag">
                <Icon name="award" size={15} />
                <span>Your Strongest Career Direction</span>
              </div>

              <div className="best-fit-hero-content">
                <div className="best-fit-title-group">
                  <h3 className="best-fit-role-title">
                    {careerResult.strongest_fit_role.role}
                  </h3>
                  <div className="best-fit-meta">
                    <span className="best-fit-score-pill">
                      {careerResult.strongest_fit_role.match_percentage}% Match
                    </span>
                    <span className={`match-strength-pill ${getStrengthClass(careerResult.strongest_fit_role.match_strength)}`}>
                      {careerResult.strongest_fit_role.match_strength}
                    </span>
                    <span className="best-fit-demand-pill">
                      {careerResult.strongest_fit_role.demand_level}
                    </span>
                  </div>
                </div>

                <p className="best-fit-explanation">
                  {careerResult.strongest_fit_role.explanation}
                </p>

                <div className="best-fit-skills-preview">
                  <div className="skills-line">
                    <span className="line-label">Matched Competencies:</span>
                    <div className="mini-tags-wrap">
                      {careerResult.strongest_fit_role.matched_skills.map((skill, idx) => (
                        <span key={idx} className="mini-tag matched">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                  {careerResult.strongest_fit_role.missing_skills.length > 0 && (
                    <div className="skills-line">
                      <span className="line-label">Recommended Additions:</span>
                      <div className="mini-tags-wrap">
                        {careerResult.strongest_fit_role.missing_skills.map((skill, idx) => (
                          <span key={idx} className="mini-tag missing">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </section>
          )}

          {/* SECTION 2: SKILL GAP SUMMARY STATS */}
          <section className="skill-gap-summary-section" aria-label="Skill Gap Summary Statistics">
            <div className="gap-stat-card">
              <div className="stat-card-top">
                <span className="stat-title">Total Skill Gaps</span>
                <span className="stat-icon-wrap neutral">
                  <Icon name="analytics" size={16} />
                </span>
              </div>
              <div className="stat-value">{careerResult.total_gaps_count}</div>
              <div className="stat-subtext">
                {careerResult.is_profile_only ? 'Profile benchmark gaps' : 'Target job & role gaps'}
              </div>
            </div>

            <div className="gap-stat-card">
              <div className="stat-card-top">
                <span className="stat-title">High Priority Gaps</span>
                <span className="stat-icon-wrap rose">
                  <Icon name="alertTriangle" size={16} />
                </span>
              </div>
              <div className="stat-value rose">{careerResult.high_priority_count}</div>
              <div className="stat-subtext">
                {careerResult.high_priority_count > 0 ? 'Mandatory for target job' : 'No required job gaps'}
              </div>
            </div>

            <div className="gap-stat-card">
              <div className="stat-card-top">
                <span className="stat-title">Medium Priority Gaps</span>
                <span className="stat-icon-wrap amber">
                  <Icon name="target" size={16} />
                </span>
              </div>
              <div className="stat-value amber">{careerResult.medium_priority_count}</div>
              <div className="stat-subtext">
                {careerResult.is_profile_only ? 'Core role benchmarks' : 'Preferred job competencies'}
              </div>
            </div>
          </section>

          {/* SECTION 1: TOP SKILL GAPS */}
          <section className="top-skill-gaps-section" aria-label="Top Prioritized Skill Gaps">
            <div className="section-header-row">
              <div className="section-title-wrap">
                <Icon name="alertTriangle" size={18} className="section-header-icon" />
                <h3 className="section-heading">Top Priority Skill Gaps</h3>
              </div>
              <span className="section-count-badge">
                {careerResult.top_priority_gaps.length} Actionable Gaps
              </span>
            </div>

            {careerResult.top_priority_gaps.length > 0 ? (
              <div className="skill-gaps-grid">
                {careerResult.top_priority_gaps.map((gap, idx) => (
                  <div key={idx} className="skill-gap-card">
                    <div className="gap-card-header">
                      <span className={`gap-priority-pill ${getPriorityClass(gap.priority)}`}>
                        {gap.priority} PRIORITY
                      </span>
                      {gap.target_level && (
                        <span className="gap-level-tag">Target: {gap.target_level}</span>
                      )}
                    </div>

                    <h4 className="gap-skill-name">{gap.skill}</h4>

                    <div className="gap-field-row">
                      <span className="field-label">Required for:</span>
                      <span className="field-value highlight">{gap.target_role || 'Target Role'}</span>
                    </div>

                    <div className="gap-field-row">
                      <span className="field-label">Why it matters:</span>
                      <span className="field-value">{gap.reason}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="zero-gaps-card">
                <Icon name="checkCircle" size={24} className="zero-icon" />
                <p>No critical skill gaps detected! Your profile satisfies all target requirements.</p>
              </div>
            )}
          </section>

          {/* SECTION 3: RECOMMENDED CAREER ROLES */}
          <section className="career-roles-section" aria-label="Recommended Career Pathways">
            <div className="section-header-row">
              <div className="section-title-wrap">
                <Icon name="careerPaths" size={18} className="section-header-icon" />
                <h3 className="section-heading">Recommended Career Roles</h3>
              </div>
              <span className="section-count-badge">Top 4 Role Matches</span>
            </div>

            <div className="career-roles-grid">
              {careerResult.recommended_roles.map((role, idx) => (
                <div key={idx} className="career-role-card">
                  <div className="role-card-header">
                    <div className="role-title-wrap">
                      <h4 className="role-title">{role.role}</h4>
                      <span className="role-demand-badge">{role.demand_level}</span>
                    </div>
                    <div className="role-score-group">
                      <span className="role-match-score">{role.match_percentage}%</span>
                      <span className={`match-strength-pill ${getStrengthClass(role.match_strength)}`}>
                        {role.match_strength}
                      </span>
                    </div>
                  </div>

                  <p className="role-description-text">{role.description}</p>

                  <div className="role-skills-breakdown">
                    <div className="role-skills-group">
                      <span className="skills-group-title matched">
                        Matched ({role.matched_skills.length}):
                      </span>
                      <div className="role-skills-tags">
                        {role.matched_skills.map((skill, sIdx) => (
                          <span key={sIdx} className="role-skill-pill matched">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>

                    {role.missing_skills.length > 0 && (
                      <div className="role-skills-group">
                        <span className="skills-group-title missing">
                          Missing ({role.missing_skills.length}):
                        </span>
                        <div className="role-skills-tags">
                          {role.missing_skills.map((skill, sIdx) => (
                            <span key={sIdx} className="role-skill-pill missing">
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  <p className="role-explanation-text">
                    &ldquo;{role.explanation}&rdquo;
                  </p>

                  <div className="role-card-footer">
                    <button
                      type="button"
                      className="btn btn-ghost btn-sm explore-role-btn"
                      title="Role exploration feature"
                      disabled
                    >
                      <span>Explore Role</span>
                      <Icon name="arrowRight" size={14} />
                    </button>
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
