import React, { useState } from 'react'
import AvatarViewer from './components/AvatarViewer'
import UploadForm from './components/UploadForm'
import Controls from './components/Controls'
import './App.css'

function App() {
  const [avatarUrl, setAvatarUrl] = useState(null)
  const [morphProgress, setMorphProgress] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAvatarGenerated = (glbPath) => {
    setAvatarUrl(glbPath)
    setError(null)
  }

  const handleLoadingChange = (loading) => {
    setIsLoading(loading)
  }

  const handleError = (err) => {
    setError(err)
    setIsLoading(false)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>DEXA to 3D Avatar</h1>
        <p>Convert your DEXA scan into a personalized 3D avatar</p>
      </header>

      <div className="app-content">
        <div className="sidebar">
          <UploadForm
            onAvatarGenerated={handleAvatarGenerated}
            onLoadingChange={handleLoadingChange}
            onError={handleError}
          />
          {error && (
            <div className="error-message">
              <p>Error: {error}</p>
            </div>
          )}
          {avatarUrl && (
            <Controls
              avatarUrl={avatarUrl}
              morphProgress={morphProgress}
              onMorphProgressChange={setMorphProgress}
            />
          )}
        </div>

        <div className="viewer-container">
          {isLoading ? (
            <div className="loading">
              <div className="spinner"></div>
              <p>Processing DEXA scan and generating avatar...</p>
            </div>
          ) : avatarUrl ? (
            <AvatarViewer
              glbUrl={avatarUrl}
              morphProgress={morphProgress}
            />
          ) : (
            <div className="placeholder">
              <p>Upload a DEXA scan PDF to get started</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App

