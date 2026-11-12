// Strip cutter: cuts the part of a mesh that lies inside an oriented box and caps the cut faces.
// Port of HelmetScaler's PerfectBoxCutter, with loop-based caps (earcut) in place of its
// nearest-neighbour stitching so concave and hollow cross-sections close properly.
import * as THREE from 'three';

const AXES = [[1, 0], [1, 1], [0, 0], [0, 1], [2, 0], [2, 1]]; // [axis, side] for +x,-x,+y,-y,+z,-z
const EPS = 1e-9;
const ON_FACE = 1e-7;

// Clips polygon (local box coords) against s*p[a] <= 0.5. Intersection points are computed from a
// fixed endpoint order so neighbouring triangles produce bit-identical points on a shared edge.
function clip(poly, a, s) {
  const out = [];
  const n = poly.length;
  for (let i = 0; i < n; i++) {
    const p = poly[i], q = poly[(i + 1) % n];
    const dp = s * p[a] - 0.5, dq = s * q[a] - 0.5;
    if (dp <= 0) out.push(p);
    if ((dp > 0) !== (dq > 0)) {
      const [u, v, du, dv] = dp < dq ? [p, q, dp, dq] : [q, p, dq, dp];
      const t = du / (du - dv);
      const r = [u[0] + (v[0] - u[0]) * t, u[1] + (v[1] - u[1]) * t, u[2] + (v[2] - u[2]) * t];
      r[a] = 0.5 * s; // snap exactly onto the face
      out.push(r);
    }
  }
  return out;
}

function pointInPoly(pt, poly) {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const a = poly[i], b = poly[j];
    if ((a.y > pt.y) !== (b.y > pt.y) && pt.x < ((b.x - a.x) * (pt.y - a.y)) / (b.y - a.y) + a.x) inside = !inside;
  }
  return inside;
}

// Joins undirected segments (world-space points) into closed loops. Open chains are closed off.
function chainLoops(segs) {
  const key = (p) => `${Math.round(p.x * 1e4)},${Math.round(p.y * 1e4)},${Math.round(p.z * 1e4)}`;
  const pts = new Map();
  const adj = new Map();
  for (const [p, q] of segs) {
    const kp = key(p), kq = key(q);
    if (kp === kq) continue;
    pts.set(kp, p); pts.set(kq, q);
    if (!adj.has(kp)) adj.set(kp, []);
    if (!adj.has(kq)) adj.set(kq, []);
    adj.get(kp).push(kq); adj.get(kq).push(kp);
  }
  const used = new Set();
  const ek = (a, b) => (a < b ? a + '|' + b : b + '|' + a);
  const loops = [];
  // start open chains at their ends first, then closed loops anywhere
  const starts = [...adj.keys()].sort((a, b) => (adj.get(a).length % 2) - (adj.get(b).length % 2)).reverse();
  for (const s of starts) {
    for (const first of adj.get(s)) {
      if (used.has(ek(s, first))) continue;
      const loop = [s];
      let prev = s, cur = first;
      used.add(ek(s, first));
      while (cur !== s) {
        loop.push(cur);
        const nxt = adj.get(cur).find((k) => k !== prev && !used.has(ek(cur, k))) ??
          adj.get(cur).find((k) => !used.has(ek(cur, k)));
        if (nxt === undefined) break;
        used.add(ek(cur, nxt));
        prev = cur; cur = nxt;
      }
      if (loop.length >= 3) loops.push(loop.map((k) => pts.get(k)));
    }
  }
  return loops;
}

/**
 * @param {THREE.BufferGeometry} geometry source mesh geometry
 * @param {THREE.Matrix4} meshWorld source mesh world matrix
 * @param {THREE.Matrix4} boxWorld world matrix of a unit cube (-0.5..0.5) placed as the cutter
 * @param {boolean} cap close the cut faces
 * @returns {THREE.BufferGeometry|null} world-space strip
 */
export function cutStrip(geometry, meshWorld, boxWorld, cap = true) {
  const pos = geometry.attributes.position;
  const index = geometry.index;
  const toLocal = new THREE.Matrix4().copy(boxWorld).invert().multiply(meshWorld);
  const v = new THREE.Vector3();
  const local = new Float64Array(pos.count * 3);
  for (let i = 0; i < pos.count; i++) {
    v.fromBufferAttribute(pos, i).applyMatrix4(toLocal);
    local[i * 3] = v.x; local[i * 3 + 1] = v.y; local[i * 3 + 2] = v.z;
  }
  const triCount = index ? index.count / 3 : pos.count / 3;
  const out = [];
  const faceSegs = AXES.map(() => []);
  const toWorld = (p) => new THREE.Vector3(p[0], p[1], p[2]).applyMatrix4(boxWorld);
  const pushTri = (a, b, c) => out.push(a.x, a.y, a.z, b.x, b.y, b.z, c.x, c.y, c.z);

  for (let t = 0; t < triCount; t++) {
    let poly = [0, 1, 2].map((k) => {
      const i = index ? index.getX(t * 3 + k) : t * 3 + k;
      return [local[i * 3], local[i * 3 + 1], local[i * 3 + 2]];
    });
    // quick reject: all three vertices beyond one face
    let rejected = false;
    for (const [a, side] of AXES) {
      const s = side ? -1 : 1;
      if (poly.every((p) => s * p[a] > 0.5)) { rejected = true; break; }
    }
    if (rejected) continue;
    for (const [a, side] of AXES) {
      poly = clip(poly, a, side ? -1 : 1);
      if (poly.length < 3) break;
    }
    if (poly.length < 3) continue;
    const w = poly.map(toWorld);
    for (let i = 1; i < w.length - 1; i++) pushTri(w[0], w[i], w[i + 1]);
    if (!cap) continue;
    for (let i = 0; i < poly.length; i++) {
      const p = poly[i], q = poly[(i + 1) % poly.length];
      AXES.forEach(([a, side], f) => {
        const s = side ? -1 : 1;
        if (Math.abs(s * p[a] - 0.5) < ON_FACE && Math.abs(s * q[a] - 0.5) < ON_FACE) faceSegs[f].push([w[i], w[(i + 1) % w.length]]);
      });
    }
  }

  if (cap) {
    const inv = new THREE.Matrix4().copy(boxWorld).invert();
    AXES.forEach(([a, side], f) => {
      if (faceSegs[f].length < 3) return;
      const s = side ? -1 : 1;
      const [u, w] = [0, 1, 2].filter((k) => k !== a);
      const loops = chainLoops(faceSegs[f]);
      const flat = loops.map((loop) => loop.map((p) => {
        const l = p.clone().applyMatrix4(inv);
        return new THREE.Vector2(l.getComponent(u), l.getComponent(w));
      }));
      // depth = how many other loops contain this one; even = outer, odd = hole
      const depth = flat.map((poly, i) => flat.reduce((n, other, j) => n + (j !== i && pointInPoly(poly[0], other) ? 1 : 0), 0));
      flat.forEach((outer, i) => {
        if (depth[i] % 2) return;
        const holes = [];
        flat.forEach((h, j) => { if (depth[j] === depth[i] + 1 && pointInPoly(h[0], outer)) holes.push(j); });
        const contour = THREE.ShapeUtils.isClockWise(outer) ? outer.slice().reverse() : outer;
        const holePts = holes.map((j) => (THREE.ShapeUtils.isClockWise(flat[j]) ? flat[j] : flat[j].slice().reverse()));
        const world3 = [loops[i], ...holes.map((j) => loops[j])];
        const all3 = [];
        world3.forEach((loop, k) => {
          const src = k === 0 ? contour : holePts[k - 1];
          const orig = k === 0 ? outer : flat[holes[k - 1]];
          all3.push(...(src === orig ? loop : loop.slice().reverse()));
        });
        let tris;
        try { tris = THREE.ShapeUtils.triangulateShape(contour, holePts); } catch { return; }
        // outward normal in local space is +axis*s; flip triangles whose local normal points inward
        for (const [i0, i1, i2] of tris) {
          const p0 = all3[i0], p1 = all3[i1], p2 = all3[i2];
          const l0 = p0.clone().applyMatrix4(inv), l1 = p1.clone().applyMatrix4(inv), l2 = p2.clone().applyMatrix4(inv);
          const n = new THREE.Vector3().subVectors(l1, l0).cross(new THREE.Vector3().subVectors(l2, l0));
          if (n.getComponent(a) * s >= -EPS) pushTri(p0, p1, p2); else pushTri(p0, p2, p1);
        }
      });
    });
  }

  if (!out.length) return null;
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(out, 3));
  g.computeVertexNormals();
  return g;
}
