import { Icon } from './Icons'

export default function StatCard({ card }) {
  const { title, value, change, subtext, isPositive, tag, icon } = card

  return (
    <div className="stat-card">
      <div className="stat-card-header">
        <span className="stat-tag">{tag}</span>
        <div className="stat-icon-wrapper">
          <Icon name={icon} size={18} />
        </div>
      </div>

      <div className="stat-body">
        <div className="stat-title">{title}</div>
        <div className="stat-value">{value}</div>
      </div>

      <div className="stat-footer">
        {change && (
          <span className={`stat-trend ${isPositive ? 'trend-positive' : 'trend-negative'}`}>
            {change}
          </span>
        )}
        {subtext && <span className="stat-subtext">{subtext}</span>}
      </div>
    </div>
  )
}
