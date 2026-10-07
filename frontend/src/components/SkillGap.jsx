import { mockSkillGaps } from '../data/mockData'
import { Icon } from './Icons'

export default function SkillGap() {
  return (
    <div className="dashboard-card skill-gap-card">
      <div className="card-header-row">
        <div>
          <h2 className="card-title">Skill Gap Analysis</h2>
          <p className="card-subtext">Areas flagged for target role alignment</p>
        </div>
        <div className="gap-alert-tag">
          <Icon name="alertTriangle" size={14} />
          <span>4 Gaps Flagged</span>
        </div>
      </div>

      <div className="gap-items-list">
        {mockSkillGaps.map((gap) => (
          <div key={gap.name} className="gap-item">
            <div className="gap-header">
              <div>
                <span className="gap-name">{gap.name}</span>
                <span className="gap-notes">{gap.notes}</span>
              </div>
              <div className="gap-values">
                <span className="gap-current-level">{gap.currentLevel}%</span>
                <span className={`priority-tag ${gap.priority.toLowerCase().replace(' ', '-')}`}>
                  {gap.priority}
                </span>
              </div>
            </div>

            <div className="gap-bar-container">
              <div className="progress-bar-track gap-track">
                {/* Target Level marker background */}
                <div
                  className="gap-target-indicator"
                  style={{ width: `${gap.targetLevel}%` }}
                  title={`Target Level: ${gap.targetLevel}%`}
                />
                {/* Current level fill */}
                <div
                  className="progress-bar-fill fill-warning"
                  style={{ width: `${gap.currentLevel}%` }}
                />
              </div>

              <div className="gap-subtext-row">
                <span className="gap-delta">
                  Needs +{gap.targetLevel - gap.currentLevel}% to hit benchmark
                </span>
                <span className="gap-target-label">Target: {gap.targetLevel}%</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
