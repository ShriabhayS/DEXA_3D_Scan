import React, { Suspense, useRef } from 'react'
import { Canvas, useLoader } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera, Environment } from '@react-three/drei'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import './AvatarViewer.css'

function AvatarModel({ glbUrl, morphProgress }) {
  const gltf = useLoader(GLTFLoader, glbUrl)
  const meshRef = useRef()

  // Apply morphing if needed (simplified - in production, interpolate between meshes)
  React.useEffect(() => {
    if (meshRef.current && morphProgress > 0) {
      // Morphing logic would go here
      // For MVP, we'll just scale based on progress
      const scale = 1 + morphProgress * 0.1
      meshRef.current.scale.set(scale, scale, scale)
    }
  }, [morphProgress])

  return (
    <primitive
      ref={meshRef}
      object={gltf.scene}
      position={[0, 0, 0]}
      scale={[1, 1, 1]}
    />
  )
}

function AvatarViewer({ glbUrl, morphProgress }) {
  return (
    <div className="avatar-viewer">
      <Canvas>
        <Suspense fallback={null}>
          <PerspectiveCamera makeDefault position={[0, 1.5, 5]} fov={50} />
          <ambientLight intensity={0.5} />
          <directionalLight position={[10, 10, 5]} intensity={1} />
          <pointLight position={[-10, -10, -5]} intensity={0.5} />
          <Environment preset="sunset" />
          <AvatarModel glbUrl={glbUrl} morphProgress={morphProgress} />
          <OrbitControls
            enablePan={true}
            enableZoom={true}
            enableRotate={true}
            minDistance={2}
            maxDistance={10}
          />
          <gridHelper args={[10, 10, '#444', '#222']} />
        </Suspense>
      </Canvas>
      <div className="viewer-info">
        <p>Use mouse to rotate, scroll to zoom, right-click to pan</p>
      </div>
    </div>
  )
}

export default AvatarViewer

