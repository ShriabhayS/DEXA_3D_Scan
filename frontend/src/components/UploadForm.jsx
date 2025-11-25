import React, { useState } from 'react'
import axios from 'axios'
import './UploadForm.css'

function UploadForm({ onAvatarGenerated, onLoadingChange, onError }) {
  const [dexaFile, setDexaFile] = useState(null)
  const [bodyPhoto, setBodyPhoto] = useState(null)
  const [targetBodyFat, setTargetBodyFat] = useState('')

  const handleDexaFileChange = (e) => {
    const file = e.target.files[0]
    if (file && file.type === 'application/pdf') {
      setDexaFile(file)
    } else {
      alert('Please select a PDF file for the DEXA scan')
    }
  }

  const handleBodyPhotoChange = (e) => {
    const file = e.target.files[0]
    if (file && (file.type.startsWith('image/'))) {
      setBodyPhoto(file)
    } else {
      alert('Please select an image file')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!dexaFile) {
      alert('Please select a DEXA scan PDF')
      return
    }

    onLoadingChange(true)
    onError(null)

    try {
      const formData = new FormData()
      formData.append('dexa_file', dexaFile)
      if (bodyPhoto) {
        formData.append('body_photo', bodyPhoto)
      }
      if (targetBodyFat) {
        formData.append('target_body_fat_percent', parseFloat(targetBodyFat))
      }

      const response = await axios.post('/api/generate-avatar', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      const avatarId = response.data.avatar_id
      const glbUrl = `/output/${avatarId}.glb`
      onAvatarGenerated(glbUrl)
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to generate avatar'
      onError(errorMessage)
      console.error('Error generating avatar:', error)
    } finally {
      onLoadingChange(false)
    }
  }

  return (
    <form className="upload-form" onSubmit={handleSubmit}>
      <h2>Upload DEXA Scan</h2>

      <div className="form-group">
        <label htmlFor="dexa-file">DEXA Scan PDF *</label>
        <input
          type="file"
          id="dexa-file"
          accept=".pdf"
          onChange={handleDexaFileChange}
          required
        />
        {dexaFile && <p className="file-name">{dexaFile.name}</p>}
      </div>

      <div className="form-group">
        <label htmlFor="body-photo">Body Photo (Optional)</label>
        <input
          type="file"
          id="body-photo"
          accept="image/*"
          onChange={handleBodyPhotoChange}
        />
        {bodyPhoto && <p className="file-name">{bodyPhoto.name}</p>}
        <p className="help-text">Upload a full-body photo for personalization</p>
      </div>

      <div className="form-group">
        <label htmlFor="target-fat">Target Body Fat % (Optional)</label>
        <input
          type="number"
          id="target-fat"
          min="0"
          max="100"
          step="0.1"
          value={targetBodyFat}
          onChange={(e) => setTargetBodyFat(e.target.value)}
          placeholder="e.g., 20.0"
        />
        <p className="help-text">Set a target body fat percentage for morphing</p>
      </div>

      <button type="submit" className="submit-button" disabled={!dexaFile}>
        Generate Avatar
      </button>
    </form>
  )
}

export default UploadForm

