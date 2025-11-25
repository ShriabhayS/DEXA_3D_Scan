# Frontend - DEXA to 3D Avatar

React + Three.js frontend for visualizing and interacting with 3D avatars generated from DEXA scans.

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Three.js** - 3D graphics library
- **React Three Fiber** - React renderer for Three.js
- **@react-three/drei** - Useful helpers for R3F
- **Axios** - HTTP client for API calls

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

4. Preview production build:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── AvatarViewer.jsx    # Three.js 3D viewer
│   │   ├── Controls.jsx        # Morphing controls and actions
│   │   └── UploadForm.jsx      # File upload form
│   ├── App.jsx                 # Main app component
│   ├── main.jsx                # Entry point
│   └── index.css               # Global styles
├── index.html
├── package.json
└── vite.config.js
```

## Components

### AvatarViewer

3D viewer component using React Three Fiber:
- Loads and displays GLB avatar files
- Orbit controls (rotate, zoom, pan)
- Lighting and environment setup
- Morphing support (simplified)

### UploadForm

File upload interface:
- DEXA PDF upload (required)
- Body photo upload (optional)
- Target body fat input (optional)
- Form validation and error handling

### Controls

Avatar interaction controls:
- Morph progress slider
- Download GLB button
- Screenshot button (placeholder)

## API Integration

The frontend communicates with the FastAPI backend:
- `/api/generate-avatar` - Upload DEXA scan and generate avatar
- `/api/avatar/{id}/glb` - Download GLB file
- `/output/{filename}` - Serve generated files

Proxy configuration in `vite.config.js` routes API calls to `http://localhost:8000`.

## Development Notes

- The viewer uses GLTFLoader to load GLB files
- Morphing is currently simplified (scaling only)
- Screenshot functionality is a placeholder
- Mobile responsiveness is basic - needs enhancement for production

## Future Enhancements

- Full morphing animation between states
- Advanced camera controls
- Material customization
- Export options (PNG, GLB variants)
- Performance optimization for large meshes
- Mobile touch controls

