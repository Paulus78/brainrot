// Renderer, Kamera, Licht, Studio-Hintergrund. Deterministisch.
import { RoomEnvironment } from '../vendor/environments/RoomEnvironment.js';

export function setupStage(THREE, canvas, opts = {}) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, alpha: false });
  renderer.setPixelRatio(opts.pixelRatio || 1.5);
  renderer.setSize(1080, 1920, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(opts.bg || '#cbc3be');
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.45;

  const camera = new THREE.PerspectiveCamera(28, 1080 / 1920, 0.1, 200);
  camera.position.set(0.3, 2.6, 17.5);
  camera.lookAt(0.3, 2.05, 0);

  // Studio: Hohlkehle (Boden geht weich in die Wand ueber)
  const sweepShape = [];
  for (let i = 0; i <= 24; i++) {
    const a = (i / 24) * Math.PI / 2;
    sweepShape.push(new THREE.Vector2(-6 - 0 + 0, 0));
  }
  const floorMat = new THREE.MeshStandardMaterial({ color: opts.floor || '#d8d0cb', roughness: 0.95 });
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(60, 60), floorMat);
  floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(60, 40), new THREE.MeshStandardMaterial({ color: opts.wall || '#c9c0bb', roughness: 1 }));
  wall.position.set(0, 20, -8); wall.receiveShadow = true; scene.add(wall);

  const hemi = new THREE.HemisphereLight('#fff4ea', '#8a7a70', 0.55); scene.add(hemi);
  const key = new THREE.DirectionalLight('#fff1e0', 2.6);
  key.position.set(-5, 9, 8); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.camera.left = -5; key.shadow.camera.right = 5; key.shadow.camera.top = 7; key.shadow.camera.bottom = -2;
  key.shadow.radius = 6; key.shadow.bias = -0.0004; key.shadow.normalBias = 0.02;
  scene.add(key);
  const fill = new THREE.DirectionalLight('#dfe8ff', 0.8); fill.position.set(7, 4, 6); scene.add(fill);
  const rim = new THREE.DirectionalLight('#ffe6cc', 1.6); rim.position.set(3, 6, -8); scene.add(rim);

  return { renderer, scene, camera, lights: { hemi, key, fill, rim }, floor, wall };
}
