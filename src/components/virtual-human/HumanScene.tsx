'use client';

import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import HumanModel from './HumanModel';

export default function HumanScene() {
      return (
            <Canvas
                  camera={{
                        position: [0, 0.9, 3],
                        fov: 40
                  }}
                  style={{ height: '700px' }}
            >
                  <ambientLight intensity={1.5} />

                  <directionalLight
                        position={[3, 5, 4]}
                        intensity={2}
                  />

                  <HumanModel />

                  <OrbitControls
                        target={[0, 0.8, 0]}
                        minDistance={1.5}
                        maxDistance={6}
                  />
            </Canvas>
      );
}
