// Shell-Fell: N leicht nach aussen versetzte Kopien eines Meshes; jede Schale
// verwirft Pixel, in denen kein Haar so lang ist. Deterministisch (Hash-Noise).
import * as THREE from 'three';

const NOISE = /* glsl */ `
float furHash(vec3 p){ p = fract(p*0.3183099 + vec3(0.71,0.113,0.419)); p *= 17.0;
  return fract(p.x*p.y*p.z*(p.x+p.y+p.z)); }
float furNoise(vec3 x){ vec3 i=floor(x), f=fract(x); f=f*f*(3.0-2.0*f);
  return mix(mix(mix(furHash(i),furHash(i+vec3(1,0,0)),f.x), mix(furHash(i+vec3(0,1,0)),furHash(i+vec3(1,1,0)),f.x),f.y),
             mix(mix(furHash(i+vec3(0,0,1)),furHash(i+vec3(1,0,1)),f.x), mix(furHash(i+vec3(0,1,1)),furHash(i+vec3(1,1,1)),f.x),f.y),f.z); }
`;

/**
 * Erzeugt Fell-Schalen fuer eine Geometrie und haengt sie an `parent`.
 * opts: color, tip, belly {center, radius, color}, length, density, shells, gravity(vec3 objektraum)
 */
export function addFur(parent, geometry, opts = {}) {
  const o = Object.assign({
    color: '#b87a4f', tip: '#e2ad7c', length: 0.07, density: 70, shells: 18,
    gravity: new THREE.Vector3(0, -1, 0), belly: null, clump: 0.35, rootDark: 0.5, dens: null,
  }, opts);
  const meshes = [];
  if (!geometry.attributes.furUv) geometry.setAttribute('furUv', geometry.attributes.uv);
  const dens = o.dens || new THREE.Vector2(o.density * 6.0, o.density * 3.0);
  const base = new THREE.Color(o.color);
  const tip = new THREE.Color(o.tip);
  const bellyC = o.belly ? new THREE.Color(o.belly.color) : new THREE.Color(o.color);

  for (let s = 0; s <= o.shells; s++) {
    const h = s / o.shells;
    const mat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.92, metalness: 0.0 });
    mat.transparent = false;
    mat.alphaToCoverage = s > 0;
    const U = {
      uShell: { value: h }, uLen: { value: o.length }, uDensity: { value: o.density },
      uDens: { value: dens }, uRoot: { value: base }, uTip: { value: tip }, uBelly: { value: bellyC },
      uBellyC: { value: o.belly ? o.belly.center : new THREE.Vector3(0, 0, 99) },
      uBellyR: { value: o.belly ? o.belly.radius : 0.0 },
      uGrav: { value: o.gravity.clone() }, uClump: { value: o.clump }, uRootDark: { value: o.rootDark },
    };
    mat.userData.fur = U;
    mat.onBeforeCompile = (sh) => {
      Object.assign(sh.uniforms, U);
      sh.vertexShader = sh.vertexShader
        .replace('#include <common>', `#include <common>
          uniform float uShell; uniform float uLen; uniform vec3 uGrav;
          attribute vec2 furUv;
          varying vec3 vFurPos; varying float vFurH; varying vec2 vFurUv;`)
        .replace('#include <begin_vertex>', `#include <begin_vertex>
          vFurPos = position; vFurH = uShell; vFurUv = furUv;
          transformed += normalize(objectNormal) * uLen * uShell + uGrav * uLen * uShell * uShell * 0.55;`);
      sh.fragmentShader = sh.fragmentShader
        .replace('#include <common>', `#include <common>
          uniform float uShell; uniform float uDensity; uniform vec3 uRoot; uniform vec3 uTip; uniform vec3 uBelly;
          uniform vec3 uBellyC; uniform float uBellyR; uniform float uClump; uniform float uRootDark; uniform vec2 uDens;
          varying vec3 vFurPos; varying float vFurH; varying vec2 vFurUv;
          ${NOISE}`)
        .replace('#include <color_fragment>', `#include <color_fragment>
          vec2 uvf = vFurUv * uDens;
          vec2 ci = floor(uvf); vec2 cf = fract(uvf);
          float best = 9.0; float hsh = 0.0; vec2 bc = ci;
          for (int j = -1; j <= 1; j++) for (int i = -1; i <= 1; i++) {
            vec2 c = ci + vec2(float(i), float(j));
            vec2 jit = vec2(furHash(vec3(c, 1.3)), furHash(vec3(c, 2.7)));
            float dd = length(vec2(float(i), float(j)) + 0.15 + jit * 0.7 - cf);
            if (dd < best) { best = dd; hsh = furHash(vec3(c, 5.1)); bc = c; }
          }
          float strand = 0.45 + 0.55 * hsh;
          strand *= mix(1.0, 0.6 + 0.8 * furNoise(vec3(vFurUv * uDens * 0.035, 0.5)), uClump);
          float cov = 1.0;
          if (uShell > 0.0) {
            float rad = 0.62 * clamp(1.0 - uShell / max(strand, 0.001), 0.0, 1.0);
            cov = smoothstep(rad + 0.10, rad - 0.10, best);
            cov *= step(uShell, strand);
            if (cov < 0.02) discard;
          }
          vec3 cell = vec3(bc, 0.0);
          float bw = uBellyR > 0.0 ? smoothstep(uBellyR, uBellyR*0.55, length(vFurPos - uBellyC)) : 0.0;
          vec3 rootC = mix(uRoot, uBelly, bw);
          vec3 tipC = mix(uTip, uBelly * 1.08, bw);
          vec3 c = mix(rootC, tipC, pow(uShell, 0.8));
          c *= mix(uRootDark, 1.0, pow(uShell, 0.6));
          c *= 0.9 + 0.2 * furHash(cell + 3.1);
          diffuseColor.rgb = c;
          diffuseColor.a = cov;`);
    };
    mat.customProgramCacheKey = () => 'fur-v2';
    const m = new THREE.Mesh(geometry, mat);
    m.castShadow = s === 0;
    m.receiveShadow = true;
    m.renderOrder = s;
    parent.add(m);
    meshes.push(m);
  }
  return meshes;
}
