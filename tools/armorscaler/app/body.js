// MakeHuman body model: deforms the CC0 base mesh with targets and solves target weights from
// tape measurements. Positions are MakeHuman decimetres internally; every measurement is in mm.

const ARM_TIP = 8274; // shoulder point, shared by the shoulder and upper-arm rulers

export const MEASUREMENTS = [
  // id, label, how it is measured, group
  { id: 'height', label: 'Height', group: 'Overall' },
  { id: 'neck-circ', label: 'Neck', group: 'Upper body' },
  { id: 'shoulder-width', label: 'Shoulder width', group: 'Upper body', tip: 'Shoulder point to shoulder point, straight across' },
  { id: 'shoulder-dist', label: 'Shoulder length', group: 'Upper body', tip: 'Side of the neck to the shoulder point' },
  { id: 'bust-circ', label: 'Chest / bust', group: 'Upper body' },
  { id: 'underbust-circ', label: 'Underbust', group: 'Upper body', sex: 'f' },
  { id: 'frontchest-dist', label: 'Front chest width', group: 'Upper body' },
  { id: 'waist-circ', label: 'Waist', group: 'Upper body' },
  { id: 'hips-circ', label: 'Hips', group: 'Upper body' },
  { id: 'napetowaist-dist', label: 'Nape to waist', group: 'Upper body' },
  { id: 'waisttohip-dist', label: 'Waist to hip', group: 'Upper body' },
  { id: 'neck-height', label: 'Neck length', group: 'Upper body' },
  { id: 'arm-length', label: 'Arm length', group: 'Arms', tip: 'Shoulder point to wrist' },
  { id: 'upperarm-length', label: 'Shoulder to elbow', group: 'Arms' },
  { id: 'lowerarm-length', label: 'Elbow to wrist', group: 'Arms' },
  { id: 'upperarm-circ', label: 'Bicep', group: 'Arms' },
  { id: 'wrist-circ', label: 'Wrist', group: 'Arms' },
  { id: 'inseam', label: 'Inseam', group: 'Legs', tip: 'Crotch to floor' },
  { id: 'upperleg-height', label: 'Crotch to knee', group: 'Legs' },
  { id: 'lowerleg-height', label: 'Knee to ankle', group: 'Legs' },
  { id: 'thigh-circ', label: 'Thigh', group: 'Legs' },
  { id: 'knee-circ', label: 'Knee', group: 'Legs' },
  { id: 'calf-circ', label: 'Calf', group: 'Legs' },
  { id: 'ankle-circ', label: 'Ankle', group: 'Legs' },
];

export async function loadBody(base) {
  const [man, buf] = await Promise.all([
    fetch(base + 'body.json').then((r) => r.json()),
    fetch(base + 'body.bin').then((r) => r.arrayBuffer()),
  ]);
  return new BodyModel(man, buf);
}

export class BodyModel {
  constructor(man, buf) {
    this.n = man.vertexCount;
    this.rulers = man.rulers;
    this.crotch = man.crotch;
    this.faces = new Uint16Array(buf, man.faces.offset, man.faces.count);
    this.bodies = { f: new Float32Array(buf, man.bodies.f, this.n * 3), m: new Float32Array(buf, man.bodies.m, this.n * 3) };
    const T = {};
    for (const t of man.targets) {
      const idx = new Uint16Array(buf, t.indices, t.count);
      const q = new Int16Array(buf, t.deltas, t.count * 3);
      const d = new Float32Array(t.count * 3);
      for (let i = 0; i < d.length; i++) d[i] = q[i] * t.scale;
      T[`${t.name}|${t.sex}`] = { idx, d };
    }
    const pick = (name, sex) => T[`${name}|${sex}`] || T[`${name}|*`];
    // modifiers: weight w in [-1, 1]; w < 0 applies the "low" target, w > 0 the "high" one
    this.modifiers = { f: [], m: [] };
    for (const sex of ['f', 'm']) {
      const add = (key, lo, hi, solved = true, limit = 1.5) => {
        const a = pick(lo, sex), b = pick(hi, sex);
        if (a && b) this.modifiers[sex].push({ key, lo: a, hi: b, solved, limit });
      };
      for (const r of Object.keys(this.rulers)) add(r, `measure-${r}-decr`, `measure-${r}-incr`);
      add('height', 'height-minheight', 'height-maxheight', true, 1);
      if (sex === 'f') add('cup', 'cup-mincup', 'cup-maxcup');
      add('weight', 'weight-minweight', 'weight-maxweight', false);
      add('muscle', 'muscle-minmuscle', 'muscle-maxmuscle', false);
    }
    // vertices any measurement reads: rulers, crotch, arm tip, and the top/bottom candidates for height
    const need = new Set([ARM_TIP, this.crotch.f, this.crotch.m]);
    Object.values(this.rulers).forEach((r) => r.forEach((i) => need.add(i)));
    for (const sex of ['f', 'm']) {
      const ys = [...Array(this.n).keys()].sort((a, b) => this.bodies[sex][a * 3 + 1] - this.bodies[sex][b * 3 + 1]);
      ys.slice(0, 60).forEach((i) => need.add(i));
      ys.slice(-60).forEach((i) => need.add(i));
    }
    this.buildBodysuit();
    this.sub = [...need];
    this.subOf = new Map(this.sub.map((v, k) => [v, k]));
    // dense per-modifier deltas restricted to the measured vertices
    for (const sex of ['f', 'm']) {
      for (const m of this.modifiers[sex]) {
        for (const side of ['lo', 'hi']) {
          const t = m[side];
          const dense = new Float32Array(this.sub.length * 3);
          for (let i = 0; i < t.idx.length; i++) {
            const k = this.subOf.get(t.idx[i]);
            if (k !== undefined) { dense[k * 3] = t.d[i * 3]; dense[k * 3 + 1] = t.d[i * 3 + 1]; dense[k * 3 + 2] = t.d[i * 3 + 2]; }
          }
          t.sub = dense;
        }
      }
    }
  }

  modsFor(sex) { return this.modifiers[sex]; }

  // Bodysuit look: finds patches around the nipples and crotch on the base bodies so deform() can smooth it flat.
  buildBodysuit() {
    const nb = Array.from({ length: this.n }, () => new Set());
    for (let i = 0; i < this.faces.length; i += 3) {
      const [a, b, c] = [this.faces[i], this.faces[i + 1], this.faces[i + 2]];
      nb[a].add(b).add(c); nb[b].add(a).add(c); nb[c].add(a).add(b);
    }
    this.neighbours = nb.map((s) => Uint16Array.from(s));
    this.patches = {};
    for (const sex of ['f', 'm']) {
      const v = this.bodies[sex];
      const bust = this.rulers['bust-circ'];
      const by = bust.reduce((s, i) => s + v[i * 3 + 1], 0) / bust.length;
      const radius = sex === 'f' ? 0.22 : 0.15; // nipple only; breast and pec shape stay
      const patch = [];
      for (const side of [-1, 1]) {
        let tip = -1;
        for (let i = 0; i < this.n; i++) {
          const x = v[i * 3] * side, y = v[i * 3 + 1];
          if (x > 0.3 && x < 1.6 && Math.abs(y - by) < 0.8 && (tip < 0 || v[i * 3 + 2] > v[tip * 3 + 2])) tip = i;
        }
        for (let i = 0; i < this.n; i++) {
          const d = Math.hypot(v[i * 3] - v[tip * 3], v[i * 3 + 1] - v[tip * 3 + 1], v[i * 3 + 2] - v[tip * 3 + 2]);
          if (d < radius) patch.push([i, 1 - (d / radius) ** 2]);
        }
      }
      // crotch: soften the anatomy to a smooth bodysuit seam
      const c = this.crotch[sex];
      for (let i = 0; i < this.n; i++) {
        const d = Math.hypot(v[i * 3] - v[c * 3], v[i * 3 + 1] - v[c * 3 + 1], v[i * 3 + 2] - v[c * 3 + 2]);
        if (d < 0.6) patch.push([i, 1 - (d / 0.6) ** 2]);
      }
      this.patches[sex] = patch;
    }
  }

  smoothPatch(sex, out) {
    const patch = this.patches[sex];
    const tmp = new Float32Array(patch.length * 3);
    for (let it = 0; it < 30; it++) {
      patch.forEach(([i], k) => {
        const nb = this.neighbours[i];
        let x = 0, y = 0, z = 0;
        for (const j of nb) { x += out[j * 3]; y += out[j * 3 + 1]; z += out[j * 3 + 2]; }
        tmp[k * 3] = x / nb.length; tmp[k * 3 + 1] = y / nb.length; tmp[k * 3 + 2] = z / nb.length;
      });
      patch.forEach(([i, f], k) => {
        for (let a = 0; a < 3; a++) out[i * 3 + a] += (tmp[k * 3 + a] - out[i * 3 + a]) * f;
      });
    }
  }

  /** Full mesh in mm, feet on y = 0, with the bodysuit smoothing applied. */
  deform(sex, w, out = new Float32Array(this.n * 3)) {
    out.set(this.bodies[sex]);
    for (const m of this.modifiers[sex]) {
      const v = w[m.key] || 0;
      if (!v) continue;
      const t = v > 0 ? m.hi : m.lo, s = Math.abs(v);
      for (let i = 0; i < t.idx.length; i++) {
        const o = t.idx[i] * 3;
        out[o] += t.d[i * 3] * s; out[o + 1] += t.d[i * 3 + 1] * s; out[o + 2] += t.d[i * 3 + 2] * s;
      }
    }
    this.smoothPatch(sex, out);
    let minY = Infinity;
    for (let i = 1; i < out.length; i += 3) if (out[i] < minY) minY = out[i];
    for (let i = 0; i < out.length; i += 3) { out[i] *= 100; out[i + 1] = (out[i + 1] - minY) * 100; out[i + 2] *= 100; }
    return out;
  }

  subPositions(sex, w) {
    const base = this.bodies[sex];
    const p = new Float64Array(this.sub.length * 3);
    this.sub.forEach((v, k) => { p[k * 3] = base[v * 3]; p[k * 3 + 1] = base[v * 3 + 1]; p[k * 3 + 2] = base[v * 3 + 2]; });
    for (const m of this.modifiers[sex]) {
      const v = w[m.key] || 0;
      if (!v) continue;
      const d = (v > 0 ? m.hi : m.lo).sub, s = Math.abs(v);
      for (let i = 0; i < d.length; i++) p[i] += d[i] * s;
    }
    return p;
  }

  /** Every measurement in mm for weights w. */
  measure(sex, w) {
    const p = this.subPositions(sex, w);
    const at = (v) => { const k = this.subOf.get(v) * 3; return [p[k], p[k + 1], p[k + 2]]; };
    const out = {};
    for (const [id, r] of Object.entries(this.rulers)) {
      let len = 0;
      for (let i = 1; i < r.length; i++) {
        const a = at(r[i - 1]), b = at(r[i]);
        len += Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
      }
      out[id] = len * 100;
    }
    let minY = Infinity, maxY = -Infinity;
    for (let k = 1; k < p.length; k += 3) { if (p[k] < minY) minY = p[k]; if (p[k] > maxY) maxY = p[k]; }
    out.height = (maxY - minY) * 100;
    out.inseam = (at(this.crotch[sex])[1] - minY) * 100;
    out['shoulder-width'] = Math.abs(at(ARM_TIP)[0]) * 200;
    out['arm-length'] = out['upperarm-length'] + out['lowerarm-length'];
    return out;
  }

  /**
   * Finds modifier weights that hit the pinned measurements (mm). Damped, bounded Gauss-Newton (measure targets may extrapolate to ±1.5);
   * weights not needed by any pin stay where they are.
   * @returns {{w: object, residual: object}}
   */
  solve(sex, w0, pins) {
    const ids = Object.keys(pins);
    const w = { ...w0 };
    if (!ids.length) return { w, residual: {} };
    const solvedMods = this.modifiers[sex].filter((m) => m.solved);
    const mods = solvedMods.map((m) => m.key);
    const lim = Object.fromEntries(solvedMods.map((m) => [m.key, m.limit]));
    const h = 1e-3, lambda = 0.5;
    let cur = this.measure(sex, w);
    for (let it = 0; it < 30; it++) {
      const r = ids.map((id) => pins[id] - cur[id]);
      if (Math.max(...r.map(Math.abs)) < 0.2) break;
      // Jacobian by forward differences, stepping inward at the bounds
      const J = mods.map((k) => {
        const step = (w[k] || 0) + h > lim[k] ? -h : h;
        const m = this.measure(sex, { ...w, [k]: (w[k] || 0) + step });
        return ids.map((id) => (m[id] - cur[id]) / step);
      });
      const n = mods.length;
      const A = Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => {
        let s = 0;
        for (let q = 0; q < ids.length; q++) s += J[i][q] * J[j][q];
        return s + (i === j ? lambda : 0);
      }));
      const g = mods.map((_, i) => ids.reduce((s, _, q) => s + J[i][q] * r[q], 0));
      const dx = solveLinear(A, g);
      if (!dx) break;
      mods.forEach((k, i) => { w[k] = Math.max(-lim[k], Math.min(lim[k], (w[k] || 0) + dx[i])); });
      cur = this.measure(sex, w);
    }
    const residual = {};
    ids.forEach((id) => { residual[id] = pins[id] - cur[id]; });
    return { w, residual };
  }
}

function solveLinear(A, b) {
  const n = b.length;
  const M = A.map((row, i) => [...row, b[i]]);
  for (let c = 0; c < n; c++) {
    let piv = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[piv][c])) piv = r;
    if (Math.abs(M[piv][c]) < 1e-12) return null;
    [M[c], M[piv]] = [M[piv], M[c]];
    for (let r = 0; r < n; r++) {
      if (r === c) continue;
      const f = M[r][c] / M[c][c];
      if (f) for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k];
    }
  }
  return M.map((row, i) => row[n] / row[i]);
}

// US bra sizing, traditional method: band = underbust in inches + 4 (+5 if odd), one cup per inch
// of bust over the band.
export const CUPS = ['AA', 'A', 'B', 'C', 'D', 'DD', 'DDD', 'G', 'H', 'I', 'J'];
export function braSize(bustMm, underMm) {
  const under = Math.round(underMm / 25.4);
  const band = under % 2 ? under + 5 : under + 4;
  const cup = Math.max(0, Math.min(CUPS.length - 1, Math.round(bustMm / 25.4 - band)));
  return { band, cup: CUPS[cup] };
}
export function braToMm(band, cup) {
  const under = (band - 4) * 25.4;
  return { under, bust: (band + Math.max(0.5, CUPS.indexOf(cup))) * 25.4 };
}
