import React from 'react'
import './Controls.css'

function Controls({ avatarUrl, morphProgress, onMorphProgressChange }) {
  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = avatarUrl
    link.download = 'avatar.glb'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const handleScreenshot = () => {
    // Get the canvas element from the Three.js renderer
    const canvas = document.querySelector('canvas')
    if (!canvas) {
      alert('Canvas not found. Please wait for the avatar to load.')
      return
    }
    
    // Convert canvas to blob and download
    canvas.toBlob((blob) => {
      if (!blob) {
        alert('Failed to capture screenshot')
        return
      }
      
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `avatar-screenshot-${Date.now()}.png`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    }, 'image/png')
  }

  return (
    <div className="controls">
      <h2>Controls</h2>

      <div className="control-group">
        <label htmlFor="morph-slider">
          Morph Progress: {Math.round(morphProgress * 100)}%
        </label>
        <input
          type="range"
          id="morph-slider"
          min="0"
          max="1"
          step="0.01"
          value={morphProgress}
          onChange={(e) => onMorphProgressChange(parseFloat(e.target.value))}
          className="slider"
        />
        <p className="help-text">Morph between current and target state</p>
      </div>

      <div className="button-group">
        <button onClick={handleDownload} className="control-button">
          Download GLB
        </button>
        <button onClick={handleScreenshot} className="control-button">
          Screenshot
        </button>
      </div>
    </div>
  )
}

export default Controls

