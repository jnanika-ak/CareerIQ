import { mockSkillProfile } from '../data/mockData'

export default function SkillProfile() {
  return (
    <div className="dashboard-card skill-profile-card">
      <div className="card-header-row">
        <div>
          <h2 className="card-title">Skill Profile</h2>
          <p className="card-subtext">Verified candidate proficiencies &amp; technical strength</p>
        </div>
        <span className="demo-indicator">Validated</span>
      </div>

      <div className="skills-list">
        {mockSkillProfile.map((skill) => (
          <div key={skill.name} className="skill-item">
            <div className="skill-header">
              <div className="skill-meta">
                <span className="skill-name">{skill.name}</span>
                <span className="skill-category">{skill.category}</span>
              </div>
              <span className="skill-percentage">{skill.level}%</span>
            </div>

            <div className="progress-bar-track">
              <div
                className="progress-bar-fill fill-primary"
                style={{ width: `${skill.level}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
