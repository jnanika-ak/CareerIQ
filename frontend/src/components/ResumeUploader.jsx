import { useState, useRef } from 'react'
import { Icon } from './Icons'

const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5 MB
const ALLOWED_EXTENSIONS = ['.pdf', '.docx']

function formatFileSize(bytes) {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${(bytes / Math.pow(k, i)).toFixed(1)} ${sizes[i]}`
}

export default function ResumeUploader({
  selectedFile,
  onFileSelect,
  onClearFile,
  onAnalyze,
  isAnalyzing,
  error,
}) {
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef(null)

  const validateAndSelectFile = (file) => {
    if (!file) return

    const name = file.name.toLowerCase()
    const isSupported = ALLOWED_EXTENSIONS.some((ext) => name.endsWith(ext))

    if (!isSupported) {
      onFileSelect(null, 'Unsupported file format. Please upload a PDF (.pdf) or DOCX (.docx) document.')
      return
    }

    if (file.size === 0) {
      onFileSelect(null, 'The selected file is empty (0 bytes). Please select a valid resume document.')
      return
    }

    if (file.size > MAX_FILE_SIZE) {
      onFileSelect(null, 'File size exceeds 5 MB limit. Please upload a smaller document.')
      return
    }

    onFileSelect(file, null)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndSelectFile(e.dataTransfer.files[0])
    }
  }

  const handleFileInputChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSelectFile(e.target.files[0])
    }
  }

  const getFileExtensionLabel = (filename) => {
    if (!filename) return 'Unknown'
    const ext = filename.split('.').pop()?.toUpperCase()
    return ext || 'FILE'
  }

  return (
    <div className="resume-uploader-card">
      {/* Drag & Drop Area */}
      <div
        className={`upload-dropzone ${isDragging ? 'dragging' : ''} ${selectedFile ? 'has-file' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !selectedFile && fileInputRef.current?.click()}
        role="region"
        aria-label="Resume file upload drop zone"
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          className="hidden-file-input"
          onChange={handleFileInputChange}
          style={{ display: 'none' }}
        />

        {!selectedFile ? (
          <div className="dropzone-content">
            <div className="upload-icon-wrapper">
              <Icon name="upload" size={28} className="upload-icon" />
            </div>

            <div className="dropzone-text">
              <p className="dropzone-primary-text">
                <strong>Click to browse</strong> or drag and drop your resume here
              </p>
              <p className="dropzone-secondary-text">
                Supported formats: <strong>PDF, DOCX</strong> &bull; Max size: <strong>5 MB</strong>
              </p>
            </div>

            <button
              type="button"
              className="btn btn-secondary browse-btn"
              onClick={(e) => {
                e.stopPropagation()
                fileInputRef.current?.click()
              }}
            >
              <Icon name="fileText" size={16} />
              Browse Files
            </button>
          </div>
        ) : (
          <div className="selected-file-preview">
            <div className="file-info-header">
              <div className="file-icon-badge">
                <Icon name="fileText" size={24} />
              </div>

              <div className="file-details">
                <h4 className="file-name" title={selectedFile.name}>
                  {selectedFile.name}
                </h4>
                <div className="file-metadata-chips">
                  <span className="metadata-chip">
                    Type: <strong>{getFileExtensionLabel(selectedFile.name)}</strong>
                  </span>
                  <span className="metadata-chip">
                    Size: <strong>{formatFileSize(selectedFile.size)}</strong>
                  </span>
                </div>
              </div>

              <button
                type="button"
                className="btn-icon-clear"
                onClick={(e) => {
                  e.stopPropagation()
                  if (fileInputRef.current) fileInputRef.current.value = ''
                  onClearFile()
                }}
                disabled={isAnalyzing}
                title="Remove selected file"
                aria-label="Remove selected file"
              >
                <Icon name="close" size={16} />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Error notification banner */}
      {error && (
        <div className="upload-error-banner" role="alert">
          <Icon name="alertTriangle" size={18} className="error-icon" />
          <div className="error-content">
            <strong>Upload Error:</strong> {error}
          </div>
        </div>
      )}

      {/* Action footer when file is ready */}
      {selectedFile && (
        <div className="uploader-actions-bar">
          <button
            type="button"
            className="btn btn-ghost"
            onClick={() => {
              if (fileInputRef.current) fileInputRef.current.value = ''
              onClearFile()
            }}
            disabled={isAnalyzing}
          >
            Choose Different File
          </button>

          <button
            type="button"
            className="btn btn-primary analyze-submit-btn"
            onClick={onAnalyze}
            disabled={isAnalyzing}
          >
            {isAnalyzing ? (
              <>
                <span className="spinner-dot" />
                Analyzing Resume...
              </>
            ) : (
              <>
                <Icon name="sparkles" size={16} />
                Analyze Resume
              </>
            )}
          </button>
        </div>
      )}
    </div>
  )
}
