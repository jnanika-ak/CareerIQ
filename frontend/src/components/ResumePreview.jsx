import { useState } from 'react'
import { Icon } from './Icons'

export default function ResumePreview({ data, onReset }) {
  const [copied, setCopied] = useState(false)

  if (!data) return null

  const handleCopyText = async () => {
    try {
      await navigator.clipboard.writeText(data.text || '')
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.warn('Failed to copy text to clipboard', err)
    }
  }

  const formatFileType = (type) => {
    if (!type) return 'Document'
    return type.toUpperCase()
  }

  const wordCount = data.text ? data.text.trim().split(/\s+/).filter(Boolean).length : 0

  return (
    <div className="resume-preview-container">
      {/* Extracted Metadata Overview Bar */}
      <div className="extraction-summary-card">
        <div className="summary-left">
          <div className="summary-file-badge">
            <Icon name="fileText" size={20} />
            <span className="summary-filename" title={data.filename}>
              {data.filename}
            </span>
          </div>

          <div className="summary-chips-row">
            <div className="summary-chip">
              <span className="chip-label">Format:</span>
              <span className="chip-value">{formatFileType(data.file_type)}</span>
            </div>

            <div className="summary-chip">
              <span className="chip-label">Characters:</span>
              <span className="chip-value">{data.characters?.toLocaleString() ?? 0}</span>
            </div>

            <div className="summary-chip">
              <span className="chip-label">Words:</span>
              <span className="chip-value">{wordCount.toLocaleString()}</span>
            </div>

            <div className="summary-chip">
              <span className="chip-label">Pages:</span>
              <span className="chip-value">
                {data.pages !== null && data.pages !== undefined ? `${data.pages} page${data.pages > 1 ? 's' : ''}` : 'N/A (Word Doc)'}
              </span>
            </div>
          </div>
        </div>

        <div className="summary-actions">
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={handleCopyText}
            title="Copy extracted text to clipboard"
          >
            <Icon name="checkCircle" size={14} />
            {copied ? 'Copied!' : 'Copy Text'}
          </button>

          <button
            type="button"
            className="btn btn-ghost btn-sm"
            onClick={onReset}
            title="Upload a different resume"
          >
            <Icon name="refresh" size={14} />
            New Upload
          </button>
        </div>
      </div>

      {/* Extracted Text Viewer */}
      <div className="text-preview-card">
        <div className="preview-card-header">
          <div className="preview-title-group">
            <h3 className="preview-heading">Extracted Resume Content</h3>
            <span className="preview-badge">Raw Text Output</span>
          </div>
          <span className="preview-char-count">
            {data.characters?.toLocaleString() ?? 0} characters extracted
          </span>
        </div>

        <div className="preview-content-box" tabIndex={0} role="region" aria-label="Extracted resume text content">
          <pre className="extracted-text-body">{data.text || 'No text extracted from document.'}</pre>
        </div>
      </div>
    </div>
  )
}
