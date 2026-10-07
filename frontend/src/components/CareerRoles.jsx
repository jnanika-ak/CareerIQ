import { mockCareerRoles } from '../data/mockData'
import { Icon } from './Icons'

export default function CareerRoles() {
  return (
    <div className="dashboard-card career-roles-card">
      <div className="card-header-row">
        <div>
          <h2 className="card-title">Recommended Career Roles</h2>
          <p className="card-subtext">Roles matched against your profile &amp; market demand</p>
        </div>
        <span className="demo-indicator">AI Matches</span>
      </div>

      <div className="roles-grid">
        {mockCareerRoles.map((role) => (
          <div key={role.title} className="role-card-item">
            <div className="role-top-row">
              <div className="role-title-wrap">
                <h3 className="role-title">{role.title}</h3>
                <span className="role-salary">{role.salaryRange}</span>
              </div>
              <div className="role-match-badge">
                <span className="match-num">{role.matchPercentage}%</span>
                <span className="match-label">Match</span>
              </div>
            </div>

            <p className="role-fit-detail">{role.primaryFit}</p>

            <div className="role-footer-row">
              <span className="market-demand-badge">
                Demand: <strong>{role.demand}</strong>
              </span>
              <button type="button" className="explore-path-btn">
                <span>Explore Path</span>
                <Icon name="arrowRight" size={14} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
