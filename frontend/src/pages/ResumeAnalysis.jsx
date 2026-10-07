import { useState } from 'react'
import ResumeUploader from '../components/ResumeUploader'
import ResumePreview from '../components/ResumePreview'
import CandidateProfileView from '../components/CandidateProfileView'
import { analyzeResume } from '../api/api'
import { Icon } from '../components/Icons'

export default function ResumeAnalysis({ onProfileChange, onNavigateToJobMatch }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [errorMessage, setErrorMessage] = useState(null)
  const [activeTab, setActiveTab] = useState('profile') // 'profile' | 'text'

  const handleFileSelect = (file, validationError) => {
    setSelectedFile(file)
    setErrorMessage(validationError || null)
    if (file) {
      setAnalysisResult(null)
    }
  }

  const handleClearFile = () => {
    setSelectedFile(null)
    setAnalysisResult(null)
    setErrorMessage(null)
  }

  const handleAnalyzeResume = async () => {
    if (!selectedFile) {
      setErrorMessage('Please choose or drop a resume file first.')
      return
    }

    setIsAnalyzing(true)
    setErrorMessage(null)

    try {
      const result = await analyzeResume(selectedFile)
      setAnalysisResult(result)
      if (onProfileChange && result.profile) {
        onProfileChange(result.profile)
      }
      setActiveTab('profile')
    } catch (err) {
      console.error('[CareerIQ] Resume analysis error:', err)
      setErrorMessage(
        err.message || 'Failed to analyze resume. Please check the backend connection.'
      )
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleReset = () => {
    setSelectedFile(null)
    setAnalysisResult(null)
    setErrorMessage(null)
  }

  return (
    <div className="resume-analysis-page">
      {/* Page Header */}
      <div className="resume-page-header">
        <div className="page-header-text">
          <div className="page-badge">
            <Icon name="sparkles" size={14} />
            <span>Step 6B: Candidate Profile Intelligence</span>
          </div>
          <h2 className="resume-main-heading">Resume Intelligence</h2>
          <p className="resume-main-description">
            Upload your resume to extract your professional profile.
          </p>
        </div>
      </div>

      {/* Main Content Layout */}
      <div className="resume-content-layout">
        {!analysisResult ? (
          <section className="resume-upload-section" aria-label="Resume Document Uploader">
            <ResumeUploader
              selectedFile={selectedFile}
              onFileSelect={handleFileSelect}
              onClearFile={handleClearFile}
              onAnalyze={handleAnalyzeResume}
              isAnalyzing={isAnalyzing}
              error={errorMessage}
            />
          </section>
        ) : (
          <section className="resume-results-section" aria-label="Extracted Candidate Intelligence">
            {/* Navigation Tabs between Structured Profile and Extracted Text */}
            <div className="results-navigation-bar">
              <div className="results-tab-group">
                <button
                  type="button"
                  className={`results-tab-btn ${activeTab === 'profile' ? 'active' : ''}`}
                  onClick={() => setActiveTab('profile')}
                >
                  <Icon name="sparkles" size={16} />
                  <span>Candidate Profile</span>
                  {analysisResult.profile?.skills?.length > 0 && (
                    <span className="tab-count-badge">
                      {analysisResult.profile.skills.length} skills
                    </span>
                  )}
                </button>

                <button
                  type="button"
                  className={`results-tab-btn ${activeTab === 'text' ? 'active' : ''}`}
                  onClick={() => setActiveTab('text')}
                >
                  <Icon name="fileText" size={16} />
                  <span>Extracted Text</span>
                  {analysisResult.characters > 0 && (
                    <span className="tab-count-badge">
                      {analysisResult.characters.toLocaleString()} chars
                    </span>
                  )}
                </button>
              </div>

              <div className="results-actions">
                {onNavigateToJobMatch && (
                  <button
                    type="button"
                    className="btn btn-primary btn-sm"
                    onClick={onNavigateToJobMatch}
                    title="Match this candidate profile against a job description"
                  >
                    <Icon name="jobMatch" size={14} />
                    Match with Job
                  </button>
                )}
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  onClick={handleReset}
                  title="Upload another resume"
                >
                  <Icon name="upload" size={14} />
                  Upload New Resume
                </button>
              </div>
            </div>

            {/* Active Tab View */}
            {activeTab === 'profile' ? (
              <CandidateProfileView
                profile={analysisResult.profile}
                filename={analysisResult.filename}
              />
            ) : (
              <ResumePreview data={analysisResult} onReset={handleReset} />
            )}
          </section>
        )}
      </div>
    </div>
  )
}
