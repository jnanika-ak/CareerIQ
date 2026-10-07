import { Icon } from './Icons'

function getInitials(name) {
  if (!name) return 'CP'
  const parts = name.trim().split(/\s+/)
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
}

export default function CandidateProfileView({ profile, filename }) {
  if (!profile) return null

  const {
    name,
    summary,
    education = [],
    skills = [],
    projects = [],
    certifications = [],
    experience = [],
  } = profile

  return (
    <div className="candidate-profile-view">
      {/* Candidate Profile Header Card */}
      <div className="profile-hero-card">
        <div className="hero-avatar-circle">
          <span>{getInitials(name)}</span>
        </div>

        <div className="hero-identity">
          <div className="hero-status-tag">
            <Icon name="checkCircle" size={13} />
            <span>Extracted Profile Intelligence</span>
          </div>

          <h3 className="candidate-name">
            {name || <span className="unspecified-name">Candidate Name Unspecified</span>}
          </h3>

          {summary && <p className="candidate-summary">{summary}</p>}

          <div className="hero-meta-chips">
            {filename && (
              <span className="hero-meta-chip">
                <Icon name="fileText" size={12} />
                {filename}
              </span>
            )}
            <span className="hero-meta-chip">
              <Icon name="code" size={12} />
              {skills.length} Skills Identified
            </span>
            {experience.length > 0 && (
              <span className="hero-meta-chip">
                <Icon name="briefcase" size={12} />
                {experience.length} Role{experience.length > 1 ? 's' : ''}
              </span>
            )}
            {education.length > 0 && (
              <span className="hero-meta-chip">
                <Icon name="bookOpen" size={12} />
                {education.length} Education Record{education.length > 1 ? 's' : ''}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Grid Layout for Profile Sections */}
      <div className="profile-sections-grid">
        {/* Left Column: Experience & Projects */}
        <div className="profile-grid-col">
          {/* Work Experience */}
          <div className="profile-section-card">
            <div className="section-card-header">
              <div className="section-title-wrap">
                <div className="section-icon-badge">
                  <Icon name="briefcase" size={18} />
                </div>
                <h4 className="section-heading">Work & Professional Experience</h4>
              </div>
              <span className="section-counter-badge">{experience.length}</span>
            </div>

            <div className="section-card-body">
              {experience.length > 0 ? (
                <div className="experience-timeline">
                  {experience.map((exp, idx) => (
                    <div key={idx} className="timeline-item">
                      <div className="timeline-marker" />
                      <div className="timeline-content">
                        <div className="exp-header-row">
                          <h5 className="exp-role">{exp.role || 'Role Unspecified'}</h5>
                          {exp.duration && (
                            <span className="exp-duration-badge">{exp.duration}</span>
                          )}
                        </div>
                        {exp.company && <p className="exp-company">{exp.company}</p>}
                        {exp.description && (
                          <p className="exp-description">{exp.description}</p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="empty-section-placeholder">
                  <p>No formal work experience entries identified in this document.</p>
                </div>
              )}
            </div>
          </div>

          {/* Key Projects */}
          <div className="profile-section-card">
            <div className="section-card-header">
              <div className="section-title-wrap">
                <div className="section-icon-badge">
                  <Icon name="code" size={18} />
                </div>
                <h4 className="section-heading">Key Projects</h4>
              </div>
              <span className="section-counter-badge">{projects.length}</span>
            </div>

            <div className="section-card-body">
              {projects.length > 0 ? (
                <div className="projects-list">
                  {projects.map((proj, idx) => (
                    <div key={idx} className="project-item-card">
                      <h5 className="project-title">{proj.name}</h5>
                      {proj.description && (
                        <p className="project-desc">{proj.description}</p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="empty-section-placeholder">
                  <p>No standalone project entries identified in this document.</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Skills, Education, Certifications */}
        <div className="profile-grid-col">
          {/* Skills Section */}
          <div className="profile-section-card">
            <div className="section-card-header">
              <div className="section-title-wrap">
                <div className="section-icon-badge">
                  <Icon name="sparkles" size={18} />
                </div>
                <h4 className="section-heading">Extracted Skills</h4>
              </div>
              <span className="section-counter-badge">{skills.length}</span>
            </div>

            <div className="section-card-body">
              {skills.length > 0 ? (
                <div className="skills-badge-wrap">
                  {skills.map((skill, idx) => (
                    <span key={idx} className="skill-pill">
                      {skill}
                    </span>
                  ))}
                </div>
              ) : (
                <div className="empty-section-placeholder">
                  <p>No matching skills detected from standard vocabulary.</p>
                </div>
              )}
            </div>
          </div>

          {/* Education Section */}
          <div className="profile-section-card">
            <div className="section-card-header">
              <div className="section-title-wrap">
                <div className="section-icon-badge">
                  <Icon name="bookOpen" size={18} />
                </div>
                <h4 className="section-heading">Education & Academics</h4>
              </div>
              <span className="section-counter-badge">{education.length}</span>
            </div>

            <div className="section-card-body">
              {education.length > 0 ? (
                <div className="education-list">
                  {education.map((edu, idx) => (
                    <div key={idx} className="education-item-card">
                      <div className="edu-header-row">
                        <h5 className="edu-degree">
                          {edu.degree}
                          {edu.field ? ` in ${edu.field}` : ''}
                        </h5>
                        {edu.year && <span className="edu-year-badge">{edu.year}</span>}
                      </div>
                      {edu.institution && (
                        <p className="edu-institution">{edu.institution}</p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="empty-section-placeholder">
                  <p>No formal degree entries identified in this document.</p>
                </div>
              )}
            </div>
          </div>

          {/* Certifications Section */}
          <div className="profile-section-card">
            <div className="section-card-header">
              <div className="section-title-wrap">
                <div className="section-icon-badge">
                  <Icon name="award" size={18} />
                </div>
                <h4 className="section-heading">Certifications & Licenses</h4>
              </div>
              <span className="section-counter-badge">{certifications.length}</span>
            </div>

            <div className="section-card-body">
              {certifications.length > 0 ? (
                <div className="certifications-list">
                  {certifications.map((cert, idx) => (
                    <div key={idx} className="certification-item-badge">
                      <Icon name="award" size={15} className="cert-icon" />
                      <span className="cert-text">{cert}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="empty-section-placeholder">
                  <p>No verified certification items found.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
