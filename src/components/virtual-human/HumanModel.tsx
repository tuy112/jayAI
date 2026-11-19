'use client';

import { useGLTF } from '@react-three/drei';

export default function HumanModel() {
      const { scene } = useGLTF('/models/female.glb');

      return (
            <primitive
                  object={scene}
                  position={[0, 0, 0]}
                  scale={1}
            />
      );
}

useGLTF.preload('/models/female.glb');