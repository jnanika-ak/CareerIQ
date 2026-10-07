import { useEffect, useState } from 'react'
import { mockRecentActivity } from '../data/mockData'
import { fetchActivityHistory } from '../api/api'
import { Icon } from './Icons'

function getActivityIcon(type) {
  switch (type) {
    case 'resume_analysis':
    case 'analysis':
      return 'resume'
    case 'job_analysis':
    case 'benchmark':
      return 'target'
    case 'job_match':
      return 'briefcase'
    case 'career_analysis':
    case 'gap':
      return 'alertTriangle'
    case 'learning_roadmap':
    case 'roadmap':
      return 'roadmap'
    case 'interview_readiness':
      return 'checkCircle'
    default:
      return 'sparkles'
  }
}

function formatRelativeTime(isoStr) {
  if (!isoStr) return 'Recently'
  try {
    const d = new Date(isoStr)
    if (isNaN(d.getTime())) return isoStr
    const diffSec = Math.floor((Date.now() - d.getTime()) / 1000)
    if (diffSec < 60) return 'Just now'
    if (diffSec < 3600) return `${Math.floor(diffSec / 60)} min ago`
    if (diffSec < 86400) return `${Math.floor(diffSec / 3600)} hr ago`
    return `${Math.floor(diffSec / 86400)} day ago`
  } catch {
    return isoStr
  }
}

export default function RecentActivity({ activities: propActivities }) {
  const [activities, setActivities] = useState(propActivities || null)
  const [loading, setLoading] = useState(!propActivities)

  useEffect(() => {
    if (propActivities) {
      setActivities(propActivities)
      setLoading(false)
      return
    }

    let isMounted = true
    async function loadRecent() {
      try {
        const historyData = await fetchActivityHistory(10)
        if (isMounted) {
          if (Array.isArray(historyData) && historyData.length > 0) {
            setActivities(historyData)
          } else {
            setActivities(mockRecentActivity)
          }
        }
      } catch {
        if (isMounted) {
          setActivities(mockRecentActivity)
        }
      } finally {
        if (isMounted) setLoading(false)
      }
    }

    loadRecent()
    return () => {
      isMounted = false
    }
  }, [propActivities])

  const displayList = activities && activities.length > 0 ? activities : mockRecentActivity

  return (
    <div className="dashboard-card recent-activity-card">
      <div className="card-header-row">
        <div>
          <h2 className="card-title">Recent Activity</h2>
          <p className="card-subtext">Persisted database activity timeline &amp; events</p>
        </div>
      </div>

      <div className="activity-timeline">
        {displayList.map((activity) => {
          const actionText = activity.action || activity.title || 'Copilot Action'
          const detailText = activity.detail || activity.description || ''
          const timeText = activity.created_at || activity.timestamp
            ? formatRelativeTime(activity.timestamp || activity.created_at)
            : 'Recent'
          const iconType = activity.activity_type || activity.type || 'sparkles'

          return (
            <div key={activity.id || `${actionText}-${Math.random()}`} className="activity-item">
              <div className={`activity-icon-badge ${iconType}`}>
                <Icon name={getActivityIcon(iconType)} size={16} />
              </div>

              <div className="activity-content">
                <div className="activity-action-row">
                  <span className="activity-title">{actionText}</span>
                  <span className="activity-time">{timeText}</span>
                </div>
                <p className="activity-detail">{detailText}</p>
                {activity.score !== null && activity.score !== undefined && (
                  <span className="activity-score-pill">
                    Score: <strong>{activity.score}</strong>
                    {typeof activity.score === 'number' && activity.score <= 100 ? '%' : ''}
                  </span>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
