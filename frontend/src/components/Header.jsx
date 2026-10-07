import { Icon } from './Icons'
import { mockUserData } from '../data/mockData'
import { useBackendHealth } from '../hooks/useBackendHealth'

export default function Header({ onToggleSidebar }) {
  const { status } = useBackendHealth({ pollInterval: 5000 })

  const getStatusText = () => {
    switch (status) {
      case 'connected':
        return 'Backend Connected'
      case 'offline':
        return 'Backend Offline'
      case 'connecting':
      default:
        return 'Connecting...'
    }
  }

  return (
    <header className="app-header">
      <div className="header-left">
        <button
          type="button"
          className="mobile-menu-btn"
          onClick={onToggleSidebar}
          aria-label="Open navigation menu"
        >
          <Icon name="menu" size={20} />
        </button>

        <div className="header-titles">
          <h1 className="header-title">Career Dashboard</h1>
          <p className="header-subtitle">
            Welcome back, <span className="highlight-name">{mockUserData.name.split(' ')[0]}</span>. Here is your AI career intelligence overview.
          </p>
        </div>
      </div>

      <div className="header-right">
        <div
          className={`system-status-pill status-${status}`}
          role="status"
          aria-live="polite"
          title={`Backend status: ${getStatusText()}`}
        >
          <span className={`status-dot-pulse status-${status}`} />
          <span className="status-text">{getStatusText()}</span>
        </div>

        <button type="button" className="icon-action-btn" aria-label="Notifications">
          <Icon name="bell" size={18} />
          <span className="notification-badge">3</span>
        </button>

        <div className="header-user-avatar" title={`${mockUserData.name} - ${mockUserData.title}`}>
          <span>{mockUserData.avatar}</span>
        </div>
      </div>
    </header>
  )
}

