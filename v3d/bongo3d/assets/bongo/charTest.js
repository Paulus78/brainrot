// Figuren-Test (8 s): 0-3.2 Drehung, danach Mimik-Parcours. Kamera steht still.
import { anim, K, blink } from './anim.js';

export function characterTest(t, { stage, bongo, bucket }) {
  // Drehung: 0 -> 2pi, weich
  const yaw = K(t, [[0.2, 0], [3.0, Math.PI * 2, 'io']]);
  const breath = Math.sin(t * 2 * Math.PI * 0.45);

  const pose = {
    yaw: yaw + K(t, [[3.2, 0], [3.6, -0.35, 'io']]),
    squash: 1 + 0.012 * breath,
    lookX: K(t, [[3.2, 0], [3.35, -0.8, 'out'], [3.9, -0.8], [4.05, 0, 'out'], [6.1, 0], [6.25, 0.6, 'out'], [7.0, 0.6], [7.15, 0, 'out']]),
    lookY: K(t, [[4.6, 0], [4.7, 0.1, 'out'], [6.0, 0.1], [6.2, 0, 'out']]),
    headYaw: K(t, [[3.25, 0], [3.55, -0.3, 'io'], [3.95, -0.3], [4.25, 0, 'io']]),
    headRoll: K(t, [[4.0, 0], [4.3, 0.14, 'io'], [4.75, 0.14], [4.95, 0, 'io'], [6.1, 0], [6.4, -0.12, 'io'], [7.4, -0.12], [7.7, 0, 'io']]),
    headPitch: K(t, [[4.75, 0], [4.9, -0.12, 'out'], [5.8, -0.12], [6.1, 0.05, 'io']]),
    // Lider: normal -> misstrauisch -> geschockt -> selbstzufrieden
    lidUL: K(t, [[4.0, 0.18], [4.2, 0.52, 'io'], [4.72, 0.52], [4.8, 0.0, 'out'], [5.9, 0.0], [6.2, 0.46, 'io']]),
    lidUR: K(t, [[4.0, 0.42], [4.2, 0.6, 'io'], [4.72, 0.6], [4.8, 0.05, 'out'], [5.9, 0.05], [6.2, 0.55, 'io']]),
    lidLL: K(t, [[4.0, 0.08], [4.2, 0.26, 'io'], [4.72, 0.26], [4.8, 0.0, 'out'], [5.9, 0.0], [6.2, 0.2, 'io']]),
    lidLR: K(t, [[4.0, 0.18], [4.2, 0.3, 'io'], [4.72, 0.3], [4.8, 0.0, 'out'], [5.9, 0.0], [6.2, 0.26, 'io']]),
    lidSlant: K(t, [[4.0, 0], [4.2, 0.25, 'io'], [4.72, 0.25], [4.8, 0, 'out'], [5.9, 0], [6.2, -0.15, 'io']]),
    eyeScaleL: K(t, [[4.72, 1], [4.84, 1.14, 'back'], [5.9, 1.14], [6.1, 1, 'io']]),
    eyeScaleR: K(t, [[4.72, 1], [4.84, 1.18, 'back'], [5.9, 1.18], [6.1, 1, 'io']]),
    pupil: K(t, [[4.72, 1], [4.84, 0.62, 'out'], [5.9, 0.62], [6.1, 1, 'io']]),
    mouthOpen: K(t, [[4.0, 0.12], [4.2, 0.03, 'io'], [4.72, 0.03], [4.86, 0.5, 'out'], [5.8, 0.5], [6.1, 0.1, 'io']]),
    smile: K(t, [[4.0, 0.4], [4.2, -0.4, 'io'], [4.72, -0.4], [4.86, -0.1, 'out'], [5.9, -0.1], [6.2, 0.95, 'io']]),
    mouthWide: K(t, [[5.9, 0], [6.2, 0.55, 'io']]),
    earL: K(t, [[4.72, 0], [4.85, 0.35, 'out'], [5.8, 0.35], [6.1, 0, 'io']]) + 0.08 * anim.ring(t - 4.72, 5, 4),
    earR: K(t, [[4.72, 0], [4.85, 0.35, 'out'], [5.8, 0.35], [6.1, 0, 'io']]) + 0.08 * anim.ring(t - 4.78, 5, 4),
    banana: 0.10 * anim.ring(t - 4.72, 3.2, 3) + 0.05 * anim.ring(t - 3.25, 3, 4),
    bounce: 0.12 * anim.hop(t, 4.72, 0.28),
    lean: K(t, [[6.1, 0], [6.4, -0.06, 'io']]),
    armR: K(t, [[6.1, 0], [6.45, 0.25, 'io']]),
  };
  // Blinzeln
  const b = Math.max(blink(t, 1.2), blink(t, 2.6), blink(t, 3.95), blink(t, 7.5));
  pose.lidUL = Math.max(pose.lidUL, b); pose.lidUR = Math.max(pose.lidUR, b);
  pose.lidLL = Math.max(pose.lidLL, b * 0.35); pose.lidLR = Math.max(pose.lidLR, b * 0.35);

  bongo.setPose(pose);
  bucket.setPose({ x: 1.85, y: 0, z: 0.45, yaw: -0.25 });
}
