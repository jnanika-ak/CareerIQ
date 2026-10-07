import { mockRoadmap } from '../data/mockData'
import { Icon } from './Icons'

export default function LearningRoadmap() {
  return (
    <div className="dashboard-card roadmap-card">
      <div className="card-header-row">
        <div>
          <h2 className="card-title">Learning Roadmap Preview</h2>
          <p className="card-subtext">Structured 4-week sprint to bridge priority gaps</p>
        </div>
        <span className="roadmap-active-badge">Sprint 1</span>
      </div>

      <div className="roadmap-timeline">
        {mockRoadmap.map((item, index) => (
          <div key={item.week} className="roadmap-step">
            <div className="step-indicator-col">
              <div className={`step-dot ${item.status === 'In Progress' ? 'active-dot' : ''}`}>
                {index + 1}
              </div>
              {index < mockRoadmap.length - 1 && <div className="step-connector-line" />}
            </div>

            <div className="step-content">
              <div className="step-header">
                <div className="step-week-topic">
                  <span className="step-week">{item.week}</span>
                  <span className="step-arrow">→</span>
                  <span className="step-topic">{item.topic}</span>
                </div>
                <span className={`step-status-tag ${item.status === 'In Progress' ? 'in-progress' : 'upcoming'}`}>
                  {item.status}
                </span>
              </div>
              <p className="step-detail">{item.detail}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="roadmap-footer">
        <button type="button" className="roadmap-action-btn">
          <span>View Full Roadmap</span>
          <Icon name="arrowRight" size={16} />
        </button>
      </div>
    </div>
  )
}
