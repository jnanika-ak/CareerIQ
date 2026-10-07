import { Icon } from './Icons'
import { mockUserData } from '../data/mockData'

const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: 'dashboard', active: true },
  { id: 'resume', label: 'Resume Analysis', icon: 'resume' },
  { id: 'job-match', label: 'Job Match', icon: 'jobMatch' },
  { id: 'career-insights', label: 'Career Insights', icon: 'careerPaths' },
  { id: 'preparation', label: 'Preparation', icon: 'roadmap' },
  { id: 'skill-gap', label: 'Skill Gap', icon: 'skillGap' },
  { id: 'career-paths', label: 'Career Paths', icon: 'target' },
  { id: 'roadmap', label: 'Learning Roadmap', icon: 'roadmap' },
  { id: 'interview', label: 'Interview Prep', icon: 'interview' },
  { id: 'analytics', label: 'Career Analytics', icon: 'analytics' },
]

export default function Sidebar({
  isOpen,
  onClose,
  activeView = 'dashboard',
  onSelectView,
}) {
  return (
    <>
      {/* Mobile Backdrop Overlay */}
      {isOpen && (
        <div 
          className="sidebar-backdrop" 
          onClick={onClose} 
          aria-hidden="true"
        />
      )}

      <aside className={`app-sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <div className="brand">
            <div className="brand-icon">
              <Icon name="sparkles" size={18} />
            </div>
            <div className="brand-info">
              <span className="brand-name">CareerIQ</span>
              <span className="brand-tag">AI Copilot</span>
            </div>
          </div>

          <button 
            type="button" 
            className="sidebar-close-btn" 
            onClick={onClose}
            aria-label="Close navigation"
          >
            <Icon name="close" size={18} />
          </button>
        </div>

        <nav className="sidebar-nav">
          <div className="nav-section-label">Main Navigation</div>
          <ul>
            {navItems.map((item) => {
              const isActive = activeView === item.id
              return (
                <li key={item.id}>
                  <a
                    href={`#${item.id}`}
                    className={`nav-link ${isActive ? 'active' : ''}`}
                    onClick={(e) => {
                      e.preventDefault()
                      if (onSelectView) onSelectView(item.id)
                      if (onClose) onClose()
                    }}
                  >
                    <Icon name={item.icon} size={18} className="nav-icon" />
                    <span className="nav-label">{item.label}</span>
                    {isActive && <span className="active-indicator" />}
                  </a>
                </li>
              )
            })}
          </ul>
        </nav>


        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="avatar-circle">
              {mockUserData.avatar}
            </div>
            <div className="user-details">
              <div className="user-name">{mockUserData.name}</div>
              <div className="user-role">{mockUserData.title}</div>
            </div>
            <div className="user-badge-status" title={mockUserData.status} />
          </div>
        </div>
      </aside>
    </>
  )
}
