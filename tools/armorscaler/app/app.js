// Armor Scaler: a measurement-driven body (MakeHuman base mesh, CC0). Type tape measurements, the
// solver reshapes the body to match, export STL. Units in the scene are mm.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { STLExporter } from 'three/addons/exporters/STLExporter.js';
import { loadBody, MEASUREMENTS, CUPS, braSize, braToMm } from './body.js';

const $ = (id) => document.getElementById(id);
const PRESET_KEY = 'gca.armorscaler.presets';
const UNITS_KEY = 'gca.armorscaler.units';

// ---------- scene ----------
const stage = $('stage');
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
stage.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x141416);
const camera = new THREE.PerspectiveCamera(30, 1, 10, 50000);
camera.position.set(1800, 1300, 3600);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.target.set(0, 900, 0);
scene.add(new THREE.HemisphereLight(0xffffff, 0x30323a, 1.6));
const key = new THREE.DirectionalLight(0xffffff, 1.8);
key.position.set(1000, 2000, 1500);
camera.add(key);
scene.add(camera);
scene.add(new THREE.GridHelper(3000, 30, 0x3a3c43, 0x26272c));

const bodyGeo = new THREE.BufferGeometry();
const bodyMesh = new THREE.Mesh(bodyGeo, new THREE.MeshStandardMaterial({ color: 0x8d96a3, roughness: 0.8, metalness: 0.02 }));
scene.add(bodyMesh);
const ruler = new THREE.Line(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0xffb84d, depthTest: false }));
ruler.renderOrder = 10;
ruler.frustumCulled = false;
ruler.visible = false;
scene.add(ruler);

// ---------- state ----------
let M; // BodyModel
const S = { sex: 'f', w: {}, pins: {}, residual: {}, units: 'cm', positions: null, measured: {} };
try { S.units = localStorage.getItem(UNITS_KEY) || 'cm'; } catch { /* storage blocked */ }

const toUnit = (mm) => (S.units === 'cm' ? mm / 10 : mm / 25.4);
const fromUnit = (v) => (S.units === 'cm' ? v * 10 : v * 25.4);
const fmt = (mm) => toUnit(mm).toFixed(S.units === 'cm' ? 1 : 2);

let toastT;
function toast(msg) {
  const t = $('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastT);
  toastT = setTimeout(() => t.classList.remove('show'), 2400);
}

// ---------- model ----------
function rebuild() {
  const solved = M.solve(S.sex, S.w, S.pins);
  S.w = solved.w;
  S.residual = solved.residual;
  S.measured = M.measure(S.sex, S.w);
  S.positions = M.deform(S.sex, S.w, S.positions || undefined);
  const attr = bodyGeo.getAttribute('position');
  if (!attr) {
    bodyGeo.setAttribute('position', new THREE.BufferAttribute(S.positions, 3));
    bodyGeo.setIndex(new THREE.BufferAttribute(M.faces, 1));
  } else attr.needsUpdate = true;
  bodyGeo.computeVertexNormals();
  bodyGeo.computeBoundingBox();
  refreshRows();
  if (activeRuler) showRuler(activeRuler);
}

// ---------- measurement rows ----------
const rows = {};
function buildRows() {
  const box = $('measures');
  box.innerHTML = '';
  let group = '';
  for (const m of MEASUREMENTS) {
    if (m.group !== group) {
      group = m.group;
      box.appendChild(Object.assign(document.createElement('h3'), { textContent: group }));
    }
    const row = document.createElement('div');
    row.className = 'mrow';
    row.dataset.only = m.sex || '';
    const id = 'm_' + m.id;
    row.innerHTML = `<label for="${id}" title="${m.tip || ''}">${m.label}</label><input id="${id}" type="number" step="0.1" inputmode="decimal"><button class="unpin" type="button" aria-label="Clear ${m.label}" title="Clear">×</button><span class="warn"></span>`;
    const [, input, unpin] = row.children;
    input.addEventListener('change', () => {
      const v = parseFloat(input.value);
      if (Number.isFinite(v) && v > 0) S.pins[m.id] = fromUnit(v); else delete S.pins[m.id];
      rebuild();
    });
    input.addEventListener('focus', () => showRuler(m.id));
    input.addEventListener('blur', () => hideRuler(m.id));
    row.addEventListener('mouseenter', () => showRuler(m.id));
    row.addEventListener('mouseleave', () => { if (document.activeElement !== input) hideRuler(m.id); });
    unpin.addEventListener('click', () => { delete S.pins[m.id]; rebuild(); });
    box.appendChild(row);
    rows[m.id] = { row, input, def: m };
  }
}
function refreshRows() {
  for (const [id, r] of Object.entries(rows)) {
    const show = !r.def.sex || r.def.sex === S.sex;
    r.row.hidden = !show;
    const pinned = id in S.pins;
    r.row.classList.toggle('pinned', pinned);
    if (document.activeElement !== r.input) r.input.value = fmt(S.measured[id]);
    const miss = pinned ? Math.abs(S.residual[id] || 0) : 0;
    r.row.classList.toggle('bad', miss > 5);
    r.row.lastChild.textContent = miss > 5 ? `Out of range. Closest: ${fmt(S.measured[id])}` : '';
  }
  document.querySelectorAll('.unit').forEach((el) => { el.textContent = S.units; });
  const pinCount = Object.keys(S.pins).length;
  $('pinCount').textContent = pinCount ? `${pinCount} measurement${pinCount > 1 ? 's' : ''} set` : 'Type any measurement to set it';
  if (S.sex === 'f') {
    const b = braSize(S.measured['bust-circ'], S.measured['underbust-circ']);
    $('braNow').textContent = `${b.band}${b.cup}`;
  }
  $('braBox').hidden = S.sex !== 'f';
  $('weight').value = S.w.weight || 0;
  $('muscle').value = S.w.muscle || 0;
}

// ---------- ruler overlay ----------
let activeRuler = null;
function vtx(i) { const p = S.positions; return new THREE.Vector3(p[i * 3], p[i * 3 + 1], p[i * 3 + 2]); }
function showRuler(id) {
  activeRuler = id;
  let pts = [];
  if (M.rulers[id]) pts = M.rulers[id].map(vtx);
  else if (id === 'arm-length') pts = [...M.rulers['upperarm-length'], ...M.rulers['lowerarm-length']].map(vtx);
  else if (id === 'shoulder-width') { const a = vtx(8274); pts = [a, new THREE.Vector3(-a.x, a.y, a.z)]; }
  else if (id === 'inseam') { const c = vtx(M.crotch[S.sex]); pts = [c, new THREE.Vector3(c.x, 0, c.z)]; }
  else if (id === 'height') {
    const b = bodyGeo.boundingBox;
    const x = b.max.x + 80;
    pts = [new THREE.Vector3(x, 0, 0), new THREE.Vector3(x, b.max.y, 0)];
  }
  ruler.geometry.dispose();
  ruler.geometry = new THREE.BufferGeometry().setFromPoints(pts);
  ruler.visible = pts.length > 1;
}
function hideRuler(id) { if (activeRuler === id) { activeRuler = null; ruler.visible = false; } }

// ---------- presets ----------
function readPresets() { try { return JSON.parse(localStorage.getItem(PRESET_KEY)) || {}; } catch { return {}; } }
function writePresets(p) { try { localStorage.setItem(PRESET_KEY, JSON.stringify(p)); return true; } catch { toast('This browser blocked saving.'); return false; } }
function refreshPresets(select = '') {
  const names = Object.keys(readPresets()).sort((a, b) => a.localeCompare(b));
  $('presetSel').innerHTML = '<option value="">Choose a body</option>' + names.map((n) => `<option>${n.replace(/</g, '&lt;')}</option>`).join('');
  $('presetSel').value = names.includes(select) ? select : '';
}

// ---------- wiring ----------
function setSex(sex) {
  S.sex = sex;
  if (sex === 'm') delete S.pins['underbust-circ'];
  S.w = { weight: S.w.weight || 0, muscle: S.w.muscle || 0 };
  document.querySelectorAll('button[data-sex]').forEach((b) => b.setAttribute('aria-pressed', b.dataset.sex === sex));
  rebuild();
}
function setUnits(u) {
  S.units = u;
  try { localStorage.setItem(UNITS_KEY, u); } catch { /* ignore */ }
  document.querySelectorAll('[data-units]').forEach((b) => b.setAttribute('aria-pressed', b.dataset.units === u));
  refreshRows();
}

function wire() {
  document.querySelectorAll('button[data-sex]').forEach((b) => b.addEventListener('click', () => setSex(b.dataset.sex)));
  document.querySelectorAll('[data-units]').forEach((b) => b.addEventListener('click', () => setUnits(b.dataset.units)));
  for (const k of ['weight', 'muscle']) $(k).addEventListener('input', () => { S.w[k] = +$(k).value; rebuild(); });
  $('bClearAll').addEventListener('click', () => { S.pins = {}; S.w = {}; rebuild(); });
  $('band').innerHTML = Array.from({ length: 13 }, (_, i) => 26 + i * 2).map((b) => `<option>${b}</option>`).join('');
  $('band').value = '34';
  $('cup').innerHTML = CUPS.map((c) => `<option>${c}</option>`).join('');
  $('cup').value = 'B';
  $('bBra').addEventListener('click', () => {
    const { under, bust } = braToMm(+$('band').value, $('cup').value);
    S.pins['underbust-circ'] = under;
    S.pins['bust-circ'] = bust;
    rebuild();
  });
  $('bExport').addEventListener('click', () => {
    const name = ($('presetSel').value || 'body').replace(/[^\w-]+/g, '_');
    const data = new STLExporter().parse(bodyMesh, { binary: true });
    const url = URL.createObjectURL(new Blob([data], { type: 'model/stl' }));
    Object.assign(document.createElement('a'), { href: url, download: `${name}.stl` }).click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  $('bSave').addEventListener('click', () => {
    const name = $('presetName').value.trim();
    if (!name) { toast('Type a name first.'); return; }
    const p = readPresets();
    p[name] = { sex: S.sex, pins: S.pins, w: S.w };
    if (writePresets(p)) { $('presetName').value = ''; refreshPresets(name); toast(`Saved “${name}”`); }
  });
  $('bLoad').addEventListener('click', () => {
    const p = readPresets()[$('presetSel').value];
    if (!p) return;
    S.sex = p.sex; S.pins = { ...p.pins }; S.w = { ...p.w };
    document.querySelectorAll('button[data-sex]').forEach((b) => b.setAttribute('aria-pressed', b.dataset.sex === S.sex));
    rebuild();
  });
  $('bDelete').addEventListener('click', () => {
    const name = $('presetSel').value;
    if (!name || !confirm(`Delete “${name}”?`)) return;
    const p = readPresets();
    delete p[name];
    writePresets(p);
    refreshPresets();
  });
  $('bView').addEventListener('click', frame);
}

function frame() {
  const b = bodyGeo.boundingBox;
  const c = b.getCenter(new THREE.Vector3());
  const r = b.getSize(new THREE.Vector3()).length() / 2;
  const dir = camera.position.clone().sub(controls.target).normalize();
  controls.target.copy(c);
  camera.position.copy(c).addScaledVector(dir, (r / Math.tan((camera.fov * Math.PI) / 360)) * 1.05);
}

function resize() {
  const w = stage.clientWidth, h = stage.clientHeight;
  renderer.setSize(w, h);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(stage);
resize();
renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });

loadBody('data/')
  .then((model) => {
    M = model;
    buildRows();
    wire();
    refreshPresets();
    setUnits(S.units);
    setSex('f');
    frame();
    $('loading').hidden = true;
  })
  .catch((err) => { console.error(err); $('loading').textContent = 'Could not load the body model.'; });

window.__bs = { S, get M() { return M; } };
