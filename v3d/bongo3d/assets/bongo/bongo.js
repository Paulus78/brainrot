// Bongo als echtes 3D-Rig (Three.js). Einheiten: Kopfradius ~1, Boden y=0.
// createBongo() -> { root, rig, setPose(pose) }   createBucket() -> { root, setPose }
import * as THREE from 'three';
import { RoundedBoxGeometry } from '../vendor/geometries/RoundedBoxGeometry.js';
import { addFur } from './fur.js';

export const COL = {
  fur: '#7a3f1f', furTip: '#d08850', belly: '#e9b489', earIn: '#e59a8c', skin: '#d99a7e',
  banana: '#f7c52a', bananaIn: '#f3dc8a', bananaTip: '#5a3a1e', bucket: '#ffc414',
  sandal: '#2350e0', ring: '#2455e6', lid: '#b37248', mouth: '#4a1414', tongue: '#d8575f',
};

const V = (x, y, z) => new THREE.Vector3(x, y, z);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, t) => a + (b - a) * t;

function std(color, o = {}) {
  return new THREE.MeshStandardMaterial(Object.assign({ color, roughness: 0.55, metalness: 0 }, o));
}
function phys(color, o = {}) {
  return new THREE.MeshPhysicalMaterial(Object.assign({ color, roughness: 0.35, metalness: 0, clearcoat: 0.6, clearcoatRoughness: 0.25 }, o));
}
function mesh(geo, mat, cast = true) {
  const m = new THREE.Mesh(geo, mat);
  m.castShadow = cast; m.receiveShadow = true;
  return m;
}
function pivot(name, x = 0, y = 0, z = 0) {
  const g = new THREE.Group(); g.name = name; g.position.set(x, y, z); return g;
}

// Getaperte Roehre entlang einer Kurve (fuer den Bananenstiel)
function taperTube(curve, segs, radial, rFn) {
  const geo = new THREE.TubeGeometry(curve, segs, 1, radial, false);
  const pos = geo.attributes.position;
  const frames = curve.computeFrenetFrames(segs, false);
  for (let i = 0; i <= segs; i++) {
    const c = curve.getPointAt(i / segs);
    const r = rFn(i / segs);
    for (let j = 0; j <= radial; j++) {
      const k = i * (radial + 1) + j;
      const p = V(pos.getX(k), pos.getY(k), pos.getZ(k)).sub(c).multiplyScalar(r).add(c);
      pos.setXYZ(k, p.x, p.y, p.z);
    }
  }
  geo.computeVertexNormals();
  return geo;
}

// Bananenschalen-Blatt: Bahn ueber die Kopfkugel, oben breit, zur Spitze schmal
function petalGeo(len, halfW, nS = 24, nT = 10) {
  const pos = [], idx = [];
  for (let i = 0; i <= nS; i++) {
    const s = i / nS;
    const th = 0.12 + s * len;
    const R = 1.15 + 0.07 * Math.pow(s, 1.8);
    const w = halfW * (1.0 - 0.85 * Math.pow(s, 1.6)) + 0.015;
    for (let j = 0; j <= nT; j++) {
      const t = -1 + 2 * j / nT;
      const ph = t * w / Math.max(Math.sin(th), 0.2);
      const curl = 0.03 * t * t;                      // Raender leicht nach aussen
      const r = R + curl;
      pos.push(r * Math.sin(th) * Math.sin(ph) * 1.07, r * Math.cos(th) * 0.96, r * Math.sin(th) * Math.cos(ph) * 1.0);
    }
  }
  for (let i = 0; i < nS; i++) for (let j = 0; j < nT; j++) {
    const a = i * (nT + 1) + j, b = a + 1, c = a + nT + 1, d = c + 1;
    idx.push(a, c, b, b, c, d);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setIndex(idx); g.computeVertexNormals();
  // Normalen muessen nach aussen zeigen, sonst Dreiecke umdrehen
  const n = g.attributes.normal, mid = Math.floor(nS / 2) * (nT + 1) + Math.floor(nT / 2);
  const pv = new THREE.Vector3().fromBufferAttribute(g.attributes.position, mid);
  const nv = new THREE.Vector3().fromBufferAttribute(n, mid);
  if (pv.dot(nv) < 0) {
    const ix = g.index.array; for (let q = 0; q < ix.length; q += 3) { const tmp = ix[q + 1]; ix[q + 1] = ix[q + 2]; ix[q + 2] = tmp; }
    g.index.needsUpdate = true; g.computeVertexNormals();
  }
  return g;
}

function makeEye(r, opts = {}) {
  const eye = pivot('eye');
  const white = mesh(new THREE.SphereGeometry(r, 48, 32), phys('#f5f2ee', { roughness: 0.18, clearcoat: 1 }), false);
  eye.add(white);
  const ball = pivot('ball');                       // dreht sich fuer den Blick
  eye.add(ball);
  // Iris-Verlauf als Textur (v = radial)
  const cv = document.createElement('canvas'); cv.width = 8; cv.height = 128;
  const g = cv.getContext('2d');
  const grd = g.createLinearGradient(0, 0, 0, 128);
  grd.addColorStop(0.0, '#2a1308'); grd.addColorStop(0.10, '#4a260f'); grd.addColorStop(0.55, '#8a4d1f');
  grd.addColorStop(0.92, '#b4712e'); grd.addColorStop(1.0, '#c4843a');
  g.fillStyle = grd; g.fillRect(0, 0, 8, 128);
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
  const irisA = opts.iris ?? 0.62;
  const iris = mesh(new THREE.SphereGeometry(r * 1.004, 48, 12, 0, Math.PI * 2, 0, irisA), phys('#ffffff', { map: tex, roughness: 0.2, clearcoat: 1 }), false);
  iris.rotation.x = Math.PI / 2;
  ball.add(iris);
  const pupil = mesh(new THREE.SphereGeometry(r * 1.008, 40, 8, 0, Math.PI * 2, 0, irisA * 0.52), phys('#070505', { roughness: 0.1, clearcoat: 1 }), false);
  pupil.rotation.x = Math.PI / 2;
  ball.add(pupil);
  // Glanzlichter (fest am Auge, drehen nicht mit)
  const hl = mesh(new THREE.SphereGeometry(r * 0.13, 16, 12), new THREE.MeshBasicMaterial({ color: '#ffffff' }), false);
  hl.position.set(-r * 0.32, r * 0.36, r * 0.86); eye.add(hl);
  const hl2 = mesh(new THREE.SphereGeometry(r * 0.06, 12, 8), new THREE.MeshBasicMaterial({ color: '#ffffff' }), false);
  hl2.position.set(r * 0.28, -r * 0.25, r * 0.93); eye.add(hl2);
  // Lider: Halbkugeln, die ueber das Auge rotieren
  const lidMat = std(opts.lidColor || COL.lid, { roughness: 0.8 });
  const upper = pivot('lidU'); const lower = pivot('lidL');
  const hemi = new THREE.SphereGeometry(r * 1.07, 48, 16, 0, Math.PI * 2, 0, Math.PI / 2);
  const um = mesh(hemi, lidMat, false); upper.add(um);
  const lm = mesh(hemi, lidMat, false); lm.rotation.x = Math.PI; lower.add(lm);
  eye.add(upper); eye.add(lower);
  return { eye, ball, pupil, upper, lower, r };
}

export function createBongo() {
  const root = pivot('bongo');
  const rig = {};
  const hips = pivot('hips', 0, 0.62, 0); root.add(hips); rig.hips = hips;

  const furBody = { color: COL.fur, tip: COL.furTip, length: 0.075, density: 64, shells: 16 };

  // ---- Rumpf
  const torso = pivot('torso'); hips.add(torso); rig.torso = torso;
  const bodyGeo = new THREE.SphereGeometry(0.74, 64, 48);
  bodyGeo.scale(1.0, 1.08, 0.9); bodyGeo.translate(0, 0.42, 0);
  addFur(torso, bodyGeo, Object.assign({}, furBody, { belly: { center: V(0, 0.3, 0.72), radius: 0.62, color: COL.belly } }));

  // ---- Beine + Fuesse
  for (const side of [-1, 1]) {
    const leg = pivot('leg' + (side < 0 ? 'L' : 'R'), side * 0.33, 0.02, 0.05); hips.add(leg);
    const lg = new THREE.CapsuleGeometry(0.2, 0.22, 8, 24); lg.translate(0, -0.22, 0);
    addFur(leg, lg, Object.assign({}, furBody, { shells: 12 }));
    const foot = pivot('foot', 0, -0.52, 0.08); leg.add(foot);
    const fg = new THREE.SphereGeometry(0.27, 40, 24); fg.scale(1.0, 0.5, 1.35); fg.translate(0, 0.02, 0.1);
    addFur(foot, fg, Object.assign({}, furBody, { color: COL.skin, tip: '#e8b394', length: 0.035, shells: 8, belly: null }));
    for (let k = -1; k <= 1; k++) {                // Zehen
      const tg = new THREE.SphereGeometry(0.085, 20, 12);
      const toe = mesh(tg, std('#dfa184', { roughness: 0.7 }));
      toe.position.set(k * 0.1, 0.0, 0.43); toe.scale.set(1, 0.8, 1); foot.add(toe);
    }
    rig['leg' + (side < 0 ? 'L' : 'R')] = leg;
    if (side < 0) {                                  // eine blaue Sandale (Bildschirm links)
      const sole = mesh(new RoundedBoxGeometry(0.66, 0.09, 0.98, 4, 0.04), phys(COL.sandal, { roughness: 0.4, clearcoat: 0.3 }));
      sole.position.set(0, -0.11, 0.1); foot.add(sole);
      const strapGeo = new THREE.TorusGeometry(0.27, 0.075, 12, 40, Math.PI);
      const strap = mesh(strapGeo, phys(COL.sandal, { roughness: 0.35, clearcoat: 0.4 }));
      strap.scale.set(1.2, 0.72, 1.0); strap.position.set(0, -0.09, 0.14); foot.add(strap);
    }
  }

  // ---- Arme
  for (const side of [-1, 1]) {
    const sh = pivot('arm' + (side < 0 ? 'L' : 'R'), side * 0.62, 0.78, 0.05); torso.add(sh);
    const ag = new THREE.CapsuleGeometry(0.15, 0.32, 8, 20); ag.translate(0, -0.26, 0);
    addFur(sh, ag, Object.assign({}, furBody, { shells: 12 }));
    const hand = pivot('hand', 0, -0.56, 0.02); sh.add(hand);
    const hg = new THREE.SphereGeometry(0.17, 32, 20); hg.scale(1, 1.05, 0.9);
    addFur(hand, hg, Object.assign({}, furBody, { color: '#c98a64', tip: '#e2ad7c', shells: 10, length: 0.045 }));
    sh.rotation.z = side * 0.28;
    rig['arm' + (side < 0 ? 'L' : 'R')] = sh;
    rig['hand' + (side < 0 ? 'L' : 'R')] = hand;
  }

  // ---- Kopf
  const neck = pivot('neck', 0, 1.18, 0.02); torso.add(neck); rig.neck = neck;
  const head = pivot('head', 0, 0.78, 0); neck.add(head); rig.head = head;
  const headGeo = new THREE.SphereGeometry(1.0, 72, 56); headGeo.scale(1.07, 0.96, 0.94);
  addFur(head, headGeo, Object.assign({}, furBody, { length: 0.08, density: 60, shells: 18,
    belly: { center: V(0, -0.45, 0.85), radius: 0.62, color: '#c98a5c' } }));

  // Ohren
  for (const side of [-1, 1]) {
    const ep = pivot('ear' + (side < 0 ? 'L' : 'R'), side * 0.86, 0.3, -0.12); head.add(ep);
    const inner = pivot('earTilt'); ep.add(inner);
    inner.rotation.set(0.05, side * -0.22, side * -0.5);
    const eg = new THREE.SphereGeometry(0.66, 48, 32); eg.scale(1.0, 1.0, 0.28); eg.translate(side * 0.5, 0.18, 0);
    addFur(inner, eg, Object.assign({}, furBody, { shells: 12, length: 0.05 }));
    const ig = new THREE.SphereGeometry(0.5, 40, 24); ig.scale(1.0, 1.0, 0.14); ig.translate(side * 0.52, 0.18, 0.165);
    const inm = mesh(ig, std(COL.earIn, { roughness: 0.75 }));
    inner.add(inm);
    rig['ear' + (side < 0 ? 'L' : 'R')] = ep;
  }

  // Augen: links (Bildschirm) gross, rechts kleiner mit blauem Ring
  const eL = makeEye(0.4, { iris: 0.66 });
  eL.eye.position.set(-0.38, 0.1, 0.72); head.add(eL.eye);
  const eR = makeEye(0.3, { iris: 0.7 });
  eR.eye.position.set(0.4, -0.02, 0.8); head.add(eR.eye);
  const ringG = new THREE.TorusGeometry(0.335, 0.075, 20, 64);
  const ring = mesh(ringG, phys(COL.ring, { roughness: 0.55, clearcoat: 0.2 }));
  ring.position.set(0.4, -0.02, 0.86); ring.rotation.y = 0.28; head.add(ring);
  const ringTail = mesh(new THREE.ConeGeometry(0.09, 0.26, 16), phys(COL.ring, { roughness: 0.55 }));
  ringTail.position.set(0.76, -0.04, 0.72); ringTail.rotation.z = -Math.PI / 2 - 0.2; head.add(ringTail);
  rig.eyeL = eL; rig.eyeR = eR;

  // Nase
  const nose = mesh(new THREE.SphereGeometry(0.075, 24, 16), std('#9a5a48', { roughness: 0.5 }));
  nose.position.set(0.03, -0.2, 0.94); nose.scale.set(1.25, 0.9, 1); head.add(nose);

  // Mund (Geometrie wird pro Frame neu gebaut) + Zahn
  const mouthG = pivot('mouth', 0.0, -0.42, 0.82); head.add(mouthG);
  const mouthMat = std(COL.mouth, { roughness: 0.9 });
  const mouthMesh = mesh(new THREE.BufferGeometry(), mouthMat, false);
  mouthMesh.renderOrder = 30;
  mouthG.add(mouthMesh);
  const tongue = mesh(new THREE.SphereGeometry(0.12, 24, 12), std(COL.tongue, { roughness: 0.6 }), false);
  tongue.scale.set(1.1, 0.35, 0.6); mouthG.add(tongue);
  const tooth = mesh(new RoundedBoxGeometry(0.19, 0.2, 0.08, 4, 0.03), phys('#fbf8f0', { roughness: 0.2, clearcoat: 0.8 }), false);
  mouthG.add(tooth);
  const toothLine = mesh(new THREE.BoxGeometry(0.008, 0.16, 0.086), std('#cfc7b6'), false);
  tooth.add(toothLine);
  rig.mouth = { g: mouthG, mesh: mouthMesh, tooth, tongue, last: '' };

  // Bananenschale
  const ban = pivot('banana', 0.0, 0.0, 0.0); head.add(ban); rig.banana = ban;
  const banWob = pivot('banWob', 0.06, 0.93, -0.04); ban.add(banWob); rig.banWob = banWob;
  const stemCurve = new THREE.CatmullRomCurve3([V(0, -0.05, 0), V(0.05, 0.25, 0.02), V(0.1, 0.5, 0), V(0.02, 0.7, -0.02), V(-0.14, 0.8, 0)]);
  const stemGeo = taperTube(stemCurve, 40, 18, (t) => lerp(0.2, 0.075, Math.pow(t, 0.8)));
  banWob.add(mesh(stemGeo, phys(COL.banana, { roughness: 0.45, clearcoat: 0.3 })));
  const tipM = mesh(new THREE.SphereGeometry(0.08, 16, 12), std(COL.bananaTip, { roughness: 0.8 }));
  tipM.position.copy(stemCurve.getPointAt(1)); banWob.add(tipM);
  const petalOut = phys(COL.banana, { roughness: 0.45, clearcoat: 0.3, side: THREE.FrontSide });
  const petalIn = std(COL.bananaIn, { roughness: 0.7, side: THREE.BackSide });
  rig.petals = [];
  const lens = [1.05, 0.95, 1.0, 1.1];
  const angs = [0.2, -1.1, 1.2, Math.PI];
  for (let k = 0; k < 4; k++) {
    const pg = petalGeo(lens[k], 0.36);
    const p = pivot('petal' + k); p.rotation.y = angs[k];
    p.add(mesh(pg, petalOut)); p.add(mesh(pg, petalIn));
    ban.add(p); rig.petals.push(p);
  }

  return { root, rig, setPose: (pose) => applyPose(rig, pose) };
}

// ---------------------------------------------------------------------------
function buildMouth(open, width, smile) {
  // flache Form (Oberkante + Unterkante), leicht extrudiert
  const w = 0.2 + 0.1 * width + 0.04 * open;
  const n = 24; const shape = new THREE.Shape();
  const top = [], bot = [];
  for (let i = 0; i <= n; i++) {
    const u = -1 + 2 * i / n;
    const y0 = -smile * 0.07 * (1 - u * u) + smile * 0.02;
    top.push([u * w, 0.02 - smile * 0.06 * u * u + 0.0 * y0]);
    const depth = 0.012 + open * 0.3;
    bot.push([u * w, 0.02 - smile * 0.06 * u * u - depth * Math.pow(1 - u * u, 0.7) - 0.012 * (1 - u * u)]);
  }
  shape.moveTo(top[0][0], top[0][1]);
  for (const p of top) shape.lineTo(p[0], p[1]);
  for (let i = bot.length - 1; i >= 0; i--) shape.lineTo(bot[i][0], bot[i][1]);
  const geo = new THREE.ExtrudeGeometry(shape, { depth: 0.16, bevelEnabled: false, curveSegments: 6 });
  geo.translate(0, 0, -0.08);
  return { geo, topY: 0.02 - smile * 0.0, depth: 0.012 + open * 0.3 };
}

export const DEFAULT_POSE = {
  x: 0, y: 0, z: 0, yaw: 0, lean: 0, tilt: 0, squash: 1, bounce: 0,
  headYaw: 0, headPitch: 0, headRoll: 0,
  earL: 0, earR: 0, earFlap: 0, banana: 0, bananaTwist: 0,
  lookX: 0, lookY: 0, pupil: 1, eyeScaleL: 1, eyeScaleR: 1,
  lidUL: 0.18, lidUR: 0.42, lidLL: 0.08, lidLR: 0.18, lidSlant: 0,
  mouthOpen: 0.12, mouthWide: 0, smile: 0.4, tongue: 0,
  armL: 0, armR: 0, armLfwd: 0, armRfwd: 0, legL: 0, legR: 0,
};

function applyPose(rig, P) {
  const p = Object.assign({}, DEFAULT_POSE, P);
  rig.hips.position.set(0, 0.62 + p.bounce, 0);
  rig.hips.parent.position.set(p.x, p.y, p.z);
  rig.hips.parent.rotation.set(0, p.yaw, 0);
  rig.torso.rotation.set(p.lean, 0, p.tilt);
  rig.torso.scale.set(1 / Math.sqrt(p.squash), p.squash, 1 / Math.sqrt(p.squash));
  rig.neck.rotation.set(p.headPitch * 0.35, p.headYaw * 0.35, p.headRoll * 0.35);
  rig.head.rotation.set(p.headPitch * 0.65, p.headYaw * 0.65, p.headRoll * 0.65);
  rig.earL.rotation.set(0, 0, p.earL + p.earFlap);
  rig.earR.rotation.set(0, 0, -p.earR - p.earFlap);
  rig.banWob.rotation.set(0, p.bananaTwist, p.banana);
  rig.petals.forEach((pt, k) => { pt.children.forEach(c => c.rotation.set(p.banana * 0.06 * (k % 2 ? 1 : -1), 0, 0)); });

  rig.armL.rotation.set(-p.armLfwd, 0, -0.28 - p.armL);
  rig.armR.rotation.set(-p.armRfwd, 0, 0.28 + p.armR);
  rig.legL.rotation.set(p.legL, 0, 0);
  rig.legR.rotation.set(p.legR, 0, 0);

  // Augen
  const look = (e, sc, lu, ll) => {
    e.eye.scale.setScalar(sc);
    e.ball.rotation.set(-p.lookY * 0.45, p.lookX * 0.55, 0);
    e.pupil.scale.set(p.pupil, p.pupil, 1);
    const up = clamp(lu), lo = clamp(ll);
    // offen: Deckel weit hinten; zu: Rand knapp unter der Mitte
    e.upper.rotation.set(lerp(-1.2, 0.14, up), 0, 0);
    e.lower.rotation.set(lerp(1.25, -0.06, lo), 0, 0);
  };
  look(rig.eyeL, p.eyeScaleL, p.lidUL, p.lidLL);
  look(rig.eyeR, p.eyeScaleR, p.lidUR, p.lidLR);
  rig.eyeL.upper.rotation.z = -p.lidSlant;
  rig.eyeR.upper.rotation.z = p.lidSlant;

  // Mund
  const key = [p.mouthOpen, p.mouthWide, p.smile].map(v => v.toFixed(3)).join('|');
  const M = rig.mouth;
  if (M.last !== key) {
    const b = buildMouth(p.mouthOpen, p.mouthWide, p.smile);
    M.mesh.geometry.dispose(); M.mesh.geometry = b.geo; M.last = key;
    M.tooth.position.set(-0.01, b.topY - 0.085, 0.07);
    M.tongue.position.set(0, b.topY - b.depth * 0.8, 0.02);
    M.tongue.visible = p.mouthOpen > 0.25 || p.tongue > 0.05;
  }
}

// ---------------------------------------------------------------------------
export function createBucket() {
  const root = pivot('bucket');
  const body = pivot('bucketBody'); root.add(body);
  const H = 1.08, R0 = 0.62, R1 = 0.84;
  const pts = [V(0, 0, 0), V(R0 - 0.04, 0, 0), V(R0, 0.03, 0), V(R1, H - 0.06, 0), V(R1 + 0.05, H - 0.05, 0),
    V(R1 + 0.06, H, 0), V(R1 + 0.03, H + 0.035, 0), V(R1 - 0.03, H + 0.02, 0), V(R1 - 0.05, H - 0.02, 0),
    V(R0 - 0.06, 0.07, 0), V(0, 0.07, 0)].map(p => new THREE.Vector2(p.x, p.y));
  const lg = new THREE.LatheGeometry(pts, 72);
  const yellow = phys(COL.bucket, { roughness: 0.32, clearcoat: 0.7, clearcoatRoughness: 0.2 });
  body.add(mesh(lg, yellow));
  // Smiley-Decal
  const cv = document.createElement('canvas'); cv.width = 1024; cv.height = 512;
  const g = cv.getContext('2d'); g.clearRect(0, 0, 1024, 512);
  g.fillStyle = '#141010';
  g.beginPath(); g.ellipse(400, 190, 38, 50, 0, 0, Math.PI * 2); g.fill();
  g.beginPath(); g.ellipse(624, 190, 38, 50, 0, 0, Math.PI * 2); g.fill();
  g.lineWidth = 34; g.lineCap = 'round'; g.strokeStyle = '#141010';
  g.beginPath(); g.arc(512, 210, 185, 0.22 * Math.PI, 0.78 * Math.PI); g.stroke();
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const y0 = 0.22, y1 = 1.02;
  const rAt = (y) => R0 + (R1 - R0) * (y - 0.03) / (H - 0.09);
  const dg = new THREE.CylinderGeometry(rAt(y1) + 0.004, rAt(y0) + 0.004, y1 - y0, 64, 1, true, -1.15, 2.3);
  dg.translate(0, (y0 + y1) / 2, 0);
  const decal = mesh(dg, new THREE.MeshPhysicalMaterial({ map: tex, transparent: true, roughness: 0.4, clearcoat: 0.7, depthWrite: false }), false);
  decal.renderOrder = 5;
  body.add(decal);
  // Buegel mit Scharnieren
  const handle = pivot('handle', 0, H - 0.08, 0); body.add(handle);
  const arc = new THREE.EllipseCurve(0, 0, R1 + 0.06, 0.95, 0, Math.PI, false, 0);
  const a3 = new THREE.CurvePath();
  const p2 = arc.getPoints(40).map(p => V(p.x, p.y, 0));
  const hc = new THREE.CatmullRomCurve3(p2);
  handle.add(mesh(new THREE.TubeGeometry(hc, 64, 0.045, 12, false), yellow));
  for (const s of [-1, 1]) {
    const knob = mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.06, 24), yellow);
    knob.rotation.z = Math.PI / 2; knob.position.set(s * (R1 + 0.07), H - 0.08, 0); body.add(knob);
  }
  // dunkler Innenraum
  const inner = mesh(new THREE.CircleGeometry(R0 - 0.07, 48), std('#b58a10', { roughness: 0.8 }), false);
  inner.rotation.x = -Math.PI / 2; inner.position.y = 0.075; body.add(inner);
  const glowL = new THREE.PointLight('#9fe7ff', 0, 3.5, 2); glowL.position.set(0, H + 0.2, 0); root.add(glowL);
  return {
    root, body, handle, glow: glowL, H,
    setPose: (q = {}) => {
      const o = Object.assign({ x: 0, y: 0, z: 0, yaw: 0, tiltX: 0, tiltZ: 0, sx: 1, sy: 1, handle: 0.0, glow: 0 }, q);
      root.position.set(o.x, o.y, o.z); root.rotation.set(o.tiltX, o.yaw, o.tiltZ);
      body.scale.set(o.sx, o.sy, o.sx);
      handle.rotation.x = o.handle;
      glowL.intensity = o.glow;
    },
  };
}
