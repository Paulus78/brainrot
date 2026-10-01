// Kleine Animations-Helfer: Keyframes mit Easing, Blinzeln, Nachschwingen, Hopser.
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const ease = {
  lin: (x) => x,
  io: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  in: (x) => x * x * x,
  out: (x) => 1 - Math.pow(1 - x, 3),
  back: (x) => { const s = 1.7, c = s + 1; return 1 + c * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2); },
  step: (x) => (x >= 1 ? 1 : 0),
};

// K(t, [[t0, v0], [t1, v1, ease], ...]) - Ease gilt fuer das Segment, das am Key endet.
export function K(t, keys) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    const [t1, v1, e = 'io'] = keys[i];
    if (t <= t1) {
      const [t0, v0] = keys[i - 1];
      const u = ease[e](clamp((t - t0) / Math.max(t1 - t0, 1e-6)));
      return v0 + (v1 - v0) * u;
    }
  }
  return keys[keys.length - 1][1];
}

export function blink(t, t0, dur = 0.16) {
  const u = (t - t0) / dur;
  if (u < 0 || u > 1) return 0;
  return u < 0.4 ? u / 0.4 : 1 - (u - 0.4) / 0.6;
}

export const anim = {
  ring: (dt, f = 4, d = 4) => (dt <= 0 ? 0 : Math.exp(-d * dt) * Math.sin(2 * Math.PI * f * dt)),
  hop: (t, t0, dur) => { const u = (t - t0) / dur; return u < 0 || u > 1 ? 0 : 4 * u * (1 - u); },
};
