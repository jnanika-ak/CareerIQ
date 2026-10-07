import { mockReadinessData } from '../data/mockData'

export default function ReadinessCard({
  score: propScore,
  level: propLevel,
  isPersisted = false,
}) {
  const baseData = mockReadinessData
  const score = propScore !== undefined && propScore !== null ? propScore : baseData.score
  const total = baseData.total
  const label = baseData.label
  const description = isPersisted
    ? 'Calculated from weighted profile readiness, role alignment, and verified project evidence.'
    : baseData.description
  const level = propLevel || baseData.level
  const breakdown = baseData.breakdown

  // SVG Gauge calculations
  const radius = 54
  const strokeWidth = 10
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (score / total) * circumference

  return (
    <div className="dashboard-card readiness-card">
      <div className="card-header-row">
        <div>
          <h2 className="card-title">{label}</h2>
          <span className="card-badge-status">{level}</span>
        </div>
        <span className={isPersisted ? 'db-connected-tag' : 'demo-indicator'}>
          {isPersisted ? '● Live DB Metric' : 'Demo Score'}
        </span>
      </div>

      <div className="readiness-visual-container">
        <div className="circular-gauge-wrapper">
          <svg className="circular-gauge-svg" width="140" height="140" viewBox="0 0 140 140">
            <defs>
              <linearGradient id="readinessGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#3b82f6" />
                <stop offset="100%" stopColor="#10b981" />
              </linearGradient>
            </defs>

            {/* Background Track */}
            <circle
              className="gauge-bg-track"
              cx="70"
              cy="70"
              r={radius}
              strokeWidth={strokeWidth}
            />

            {/* Progress Arc */}
            <circle
              className="gauge-progress-arc"
              cx="70"
              cy="70"
              r={radius}
              strokeWidth={strokeWidth}
              stroke="url(#readinessGradient)"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              transform="rotate(-90 70 70)"
            />
          </svg>

          <div className="gauge-center-content">
            <div className="gauge-score-value">{score}</div>
            <div className="gauge-score-total">/ {total}</div>
          </div>
        </div>

        <div className="readiness-details">
          <p className="readiness-description">{description}</p>
          <div className="readiness-metrics-list">
            {breakdown.map((item) => (
              <div key={item.label} className="readiness-metric-item">
                <div className="metric-item-info">
                  <span className="metric-item-label">{item.label}</span>
                  <span className="metric-item-val">{item.score}%</span>
                </div>
                <div className="mini-progress-track">
                  <div
                    className="mini-progress-fill"
                    style={{ width: `${item.score}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
