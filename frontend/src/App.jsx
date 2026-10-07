import { useEffect, useState } from 'react'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import StatCard from './components/StatCard'
import ReadinessCard from './components/ReadinessCard'
import SkillProfile from './components/SkillProfile'
import SkillGap from './components/SkillGap'
import CareerRoles from './components/CareerRoles'
import LearningRoadmap from './components/LearningRoadmap'
import RecentActivity from './components/RecentActivity'
import ResumeAnalysis from './pages/ResumeAnalysis'
import JobMatch from './pages/JobMatch'
import CareerInsights from './pages/CareerInsights'
import Preparation from './pages/Preparation'
import { mockStatCards } from './data/mockData'
import { fetchHistorySummary } from './api/api'
import './App.css'

export default function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [currentView, setCurrentView] = useState('dashboard')
  const [candidateProfile, setCandidateProfile] = useState(null)
  const [jobMatchResult, setJobMatchResult] = useState(null)
  const [careerAnalysisResult, setCareerAnalysisResult] = useState(null)
  const [historySummary, setHistorySummary] = useState(null)

  useEffect(() => {
    let isMounted = true
    async function loadSummary() {
      try {
        const sum = await fetchHistorySummary()
        if (isMounted && sum) {
          setHistorySummary(sum)
        }
      } catch {
        // Graceful fallback to mock data
      }
    }
    loadSummary()
    return () => {
      isMounted = false
    }
  }, [currentView])

  // Derive stat cards from real PostgreSQL metrics if available, otherwise mockData
  const hasDbMetrics =
    historySummary &&
    (historySummary.total_resume_analyses > 0 ||
      historySummary.total_job_matches > 0 ||
      historySummary.total_career_analyses > 0)

  const activeStatCards = hasDbMetrics
    ? [
        {
          id: 'readiness',
          title: 'Job Readiness Score',
          value:
            historySummary.latest_interview_readiness_score !== null
              ? `${historySummary.latest_interview_readiness_score}%`
              : '78%',
          change: historySummary.latest_interview_readiness_level || 'Weighted Evaluation',
          isPositive: true,
          tag: 'Database Metric',
          icon: 'target',
        },
        {
          id: 'job-matches',
          title: 'Job Matches Evaluated',
          value: `${historySummary.total_job_matches || 0}`,
          subtext: `Avg Match: ${historySummary.average_match_score || 0}%`,
          isPositive: true,
          tag: 'Skill Benchmark',
          icon: 'checkCircle',
        },
        {
          id: 'resumes-stored',
          title: 'Resumes Analyzed',
          value: `${historySummary.total_resume_analyses || 0}`,
          subtext: `${historySummary.total_career_analyses || 0} career evaluations`,
          isPositive: true,
          tag: 'Candidate Database',
          icon: 'briefcase',
        },
        {
          id: 'skill-gaps',
          title: 'Skill Gaps Tracked',
          value: `${historySummary.total_skill_gaps || 0}`,
          subtext: 'Identified growth competencies',
          isPositive: false,
          tag: 'Growth Areas',
          icon: 'alertTriangle',
        },
      ]
    : mockStatCards

  return (
    <div className="app-layout">
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        activeView={currentView}
        onSelectView={(view) => setCurrentView(view)}
      />

      <div className="main-wrapper">
        <Header onToggleSidebar={() => setIsSidebarOpen((prev) => !prev)} />

        <main className="dashboard-content">
          {currentView === 'resume' ? (
            <ResumeAnalysis
              onProfileChange={setCandidateProfile}
              onNavigateToJobMatch={() => setCurrentView('job-match')}
            />
          ) : currentView === 'job-match' ? (
            <JobMatch
              candidateProfile={candidateProfile}
              onNavigateToResume={() => setCurrentView('resume')}
              onJobMatchComplete={setJobMatchResult}
              onNavigateToCareerInsights={() => setCurrentView('career-insights')}
            />
          ) : currentView === 'career-insights' || currentView === 'skill-gap' || currentView === 'career-paths' ? (
            <CareerInsights
              candidateProfile={candidateProfile}
              jobMatch={jobMatchResult}
              onNavigateToResume={() => setCurrentView('resume')}
              onNavigateToJobMatch={() => setCurrentView('job-match')}
              onCareerAnalysisComplete={setCareerAnalysisResult}
              onNavigateToPreparation={() => setCurrentView('preparation')}
            />
          ) : currentView === 'preparation' || currentView === 'roadmap' || currentView === 'interview' ? (
            <Preparation
              candidateProfile={candidateProfile}
              careerAnalysis={careerAnalysisResult}
              jobMatch={jobMatchResult}
              onNavigateToResume={() => setCurrentView('resume')}
              onNavigateToCareerInsights={() => setCurrentView('career-insights')}
            />
          ) : (
            <>
              {/* Summary Stat Cards Row */}
              <section className="stats-grid-section" aria-label="Summary Statistics">
                {activeStatCards.map((card) => (
                  <StatCard key={card.id} card={card} />
                ))}
              </section>

              {/* Primary Intelligence Row: Readiness & Skills */}
              <section className="dashboard-grid-two-col">
                <div className="col-stack">
                  <ReadinessCard
                    score={historySummary?.latest_interview_readiness_score}
                    level={historySummary?.latest_interview_readiness_level}
                    isPersisted={Boolean(historySummary?.latest_interview_readiness_score !== null && hasDbMetrics)}
                  />
                  <SkillProfile />
                </div>

                <div className="col-stack">
                  <SkillGap />
                  <RecentActivity />
                </div>
              </section>

              {/* Secondary Intelligence Row: Roles & Roadmap */}
              <section className="dashboard-grid-two-col">
                <div className="col-stack">
                  <CareerRoles />
                </div>

                <div className="col-stack">
                  <LearningRoadmap />
                </div>
              </section>
            </>
          )}

          {/* Clean Dashboard Footer Note */}
          <footer className="dashboard-footer">
            <p>
              <strong>CareerIQ</strong> &mdash; AI-Powered Job Intelligence &amp; Career Copilot &bull; Step 10: PostgreSQL Database &amp; Analytics
            </p>
          </footer>
        </main>
      </div>
    </div>
  )
}
