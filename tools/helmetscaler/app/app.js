// HelmetScaler web: fit a helmet STL on a scalable reference head, section it, cut print strips.
// All units are millimetres. Port of the Unity HelmetScaler build; see README in this folder.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';
import { STLExporter } from 'three/addons/exporters/STLExporter.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';
import { cutStrip } from './cutter.js';

const $ = (id) => document.getElementById(id);
const DEG = Math.PI / 180;
const PRESET_KEY = 'gca.helmetscaler.presets';

// ---------- scene ----------
const stage = $('stage');
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.localClippingEnabled = true;
stage.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x141416);
const camera = new THREE.PerspectiveCamera(35, 1, 1, 20000);
camera.position.set(420, 180, 620);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.target.set(0, 0, 0);

scene.add(new THREE.HemisphereLight(0xffffff, 0x30323a, 1.6));
const key = new THREE.DirectionalLight(0xffffff, 1.8);
key.position.set(300, 500, 400);
camera.add(key);
scene.add(camera);

const grid = new THREE.GridHelper(800, 40, 0x3a3c43, 0x26272c);
scene.add(grid);

const clipPlanes = { x: new THREE.Plane(new THREE.Vector3(-1, 0, 0), 0), y: new THREE.Plane(new THREE.Vector3(0, -1, 0), 0), z: new THREE.Plane(new THREE.Vector3(0, 0, -1), 0) };
const clippable = new Set();
const mat = (color, extra = {}) => {
  const m = new THREE.MeshStandardMaterial({ color, roughness: 0.6, metalness: 0.05, side: THREE.DoubleSide, ...extra });
  clippable.add(m);
  return m;
};
const headMat = mat(0xd9b49a);
const helmetMat = mat(0x7fd0ff, { roughness: 0.45 });
const stripMat = new THREE.MeshStandardMaterial({ color: 0xffb84d, roughness: 0.5, side: THREE.DoubleSide });

// ---------- state ----------
const S = {
  model: 'male',
  heads: {},           // male/female: { root, size: Vector3 }
  headSize: new THREE.Vector3(), // target size in mm
  scan: null,
  helmet: null,        // { pivot, mesh, name }
  h: { mx: 0, my: 0, mz: 0, rx: 0, ry: 0, rz: 0, sx: 1, sy: 1, sz: 1, su: 1 },
  section: 'off',      // off | x | y | z | all
  cut: { axis: null, pos: 0, tilt: 0, thick: 5 },
  strip: null,
};
const headGroup = new THREE.Group();
scene.add(headGroup);

// ---------- helpers ----------
let toastT;
function toast(msg) {
  const t = $('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastT);
  toastT = setTimeout(() => t.classList.remove('show'), 2200);
}
const fmt = (v, d = 1) => (Math.round(v * 10 ** d) / 10 ** d).toFixed(d);
function download(data, name) {
  const url = URL.createObjectURL(new Blob([data], { type: 'model/stl' }));
  const a = Object.assign(document.createElement('a'), { href: url, download: name });
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function sceneBounds() {
  const b = new THREE.Box3();
  if (S.scan) b.expandByObject(S.scan);
  else if (S.heads[S.model]) b.expandByObject(S.heads[S.model].root);
  if (S.helmet) b.expandByObject(S.helmet.pivot);
  if (b.isEmpty()) b.set(new THREE.Vector3(-150, -150, -150), new THREE.Vector3(150, 150, 150));
  return b;
}
function updateGrid() {
  const b = sceneBounds();
  grid.position.y = b.min.y - 2;
}

// Builds a labelled slider + number input + nudge buttons. Returns { set(v) }.
function control(parent, { label, min, max, step, value, digits = 1, nudge = step, onInput }) {
  const row = document.createElement('div');
  row.className = 'ctl';
  row.innerHTML = `<label>${label}</label><button class="nb" aria-label="${label} down">−</button><input type="range"><button class="nb" aria-label="${label} up">+</button><input type="number">`;
  const [lab, down, range, up, num] = row.children;
  const id = 'c' + Math.random().toString(36).slice(2, 8);
  num.id = id; lab.htmlFor = id;
  Object.assign(range, { min, max, step });
  num.step = step;
  const set = (v, fire = false) => {
    range.value = v;
    num.value = fmt(v, digits);
    if (fire) onInput(v);
  };
  range.addEventListener('input', () => set(+range.value, true));
  num.addEventListener('change', () => { const v = parseFloat(num.value); if (Number.isFinite(v)) set(v, true); else set(+range.value); });
  down.addEventListener('click', () => set(+num.value - nudge, true));
  up.addEventListener('click', () => set(+num.value + nudge, true));
  parent.appendChild(row);
  set(value);
  return { set, row, range, num };
}

// ---------- heads ----------
const gltf = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
async function loadHead(name) {
  const g = await gltf.loadAsync(`models/${name}-head.glb`);
  const root = new THREE.Group();
  const inner = g.scene;
  inner.traverse((o) => { if (o.isMesh) { o.material = headMat; o.geometry.computeVertexNormals(); } });
  root.add(inner);
  const box = new THREE.Box3().setFromObject(inner);
  inner.position.sub(box.getCenter(new THREE.Vector3()));
  const size = box.getSize(new THREE.Vector3());
  root.visible = false;
  headGroup.add(root);
  S.heads[name] = { root, size };
}

const headCtl = {};
function applyHeadScale() {
  const h = S.heads[S.model];
  if (!h) return;
  h.root.scale.set(S.headSize.x / h.size.x, S.headSize.y / h.size.y, S.headSize.z / h.size.z);
  $('headDims').textContent = `${fmt(S.headSize.x)} × ${fmt(S.headSize.y)} × ${fmt(S.headSize.z)} mm`;
  updateGrid();
}
function showModel(name, keepSize = false) {
  clearScan();
  S.model = name;
  for (const [n, h] of Object.entries(S.heads)) h.root.visible = n === name;
  const h = S.heads[name];
  if (!keepSize) S.headSize.copy(h.size);
  for (const a of ['x', 'y', 'z']) {
    const def = h.size[a];
    Object.assign(headCtl[a].range, { min: Math.round(def * 0.7), max: Math.round(def * 1.3) });
    headCtl[a].set(S.headSize[a]);
  }
  document.querySelectorAll('[data-model]').forEach((b) => b.setAttribute('aria-pressed', b.dataset.model === name));
  applyHeadScale();
}

// ---------- scan ----------
const stl = new STLLoader();
function loadScan(buf, name) {
  const geo = stl.parse(buf);
  geo.computeBoundingBox();
  geo.translate(...geo.boundingBox.getCenter(new THREE.Vector3()).negate().toArray());
  geo.computeVertexNormals();
  clearScan();
  for (const h of Object.values(S.heads)) h.root.visible = false;
  S.scan = new THREE.Mesh(geo, headMat);
  headGroup.add(S.scan);
  const size = geo.boundingBox.getSize(new THREE.Vector3());
  $('scanInfo').textContent = `${name}: ${fmt(size.x)} × ${fmt(size.y)} × ${fmt(size.z)} mm`;
  $('scanInfo').hidden = false;
  $('bClearScan').hidden = false;
  $('headCtls').classList.add('off');
  updateGrid();
  toast('Scan loaded. Head scaling is off while a scan is shown.');
}
function clearScan() {
  if (!S.scan) return;
  headGroup.remove(S.scan);
  S.scan.geometry.dispose();
  S.scan = null;
  $('scanInfo').hidden = true;
  $('bClearScan').hidden = true;
  $('headCtls').classList.remove('off');
  if (S.heads[S.model]) S.heads[S.model].root.visible = true;
  updateGrid();
}

// ---------- helmet ----------
const helmetCtl = {};
function loadHelmet(buf, name) {
  const geo = stl.parse(buf);
  geo.computeBoundingBox();
  geo.translate(...geo.boundingBox.getCenter(new THREE.Vector3()).negate().toArray());
  if (!geo.attributes.normal) geo.computeVertexNormals();
  if (S.helmet) { scene.remove(S.helmet.pivot); S.helmet.mesh.geometry.dispose(); }
  cancelStrip();
  const pivot = new THREE.Group();
  const mesh = new THREE.Mesh(geo, helmetMat);
  pivot.add(mesh);
  scene.add(pivot);
  S.helmet = { pivot, mesh, name: name.replace(/\.stl$/i, '') };
  resetHelmet();
  $('helmetName').textContent = name;
  document.querySelectorAll('.needs-helmet').forEach((el) => { el.disabled = false; });
  $('helmetCtls').classList.remove('off');
  $('cutCtls').classList.toggle('off', !S.cut.axis);
  toast(`${name}: ${(geo.attributes.position.count / 3).toLocaleString()} triangles`);
}
function applyHelmet() {
  if (!S.helmet) return;
  const { mx, my, mz, rx, ry, rz, sx, sy, sz, su } = S.h;
  const p = S.helmet.pivot;
  p.position.set(mx, my, mz);
  p.rotation.set(rx * DEG, ry * DEG, rz * DEG, 'YXZ');
  p.scale.set(sx * su, sy * su, sz * su);
  p.updateMatrixWorld(true);
  updateGrid();
  if (S.cut.axis) placeCutter();
}
function resetHelmet() {
  Object.assign(S.h, { mx: 0, my: 0, mz: 0, rx: 0, ry: 0, rz: 0, sx: 1, sy: 1, sz: 1, su: 1 });
  for (const [k, c] of Object.entries(helmetCtl)) c.set(S.h[k]);
  applyHelmet();
}

// ---------- section view ----------
function applySection() {
  const b = sceneBounds();
  const planes = [];
  for (const a of ['x', 'y', 'z']) {
    const on = S.section === a || S.section === 'all';
    $('sec_' + a).classList.toggle('off', !on);
    if (!on) continue;
    const t = +$('secr_' + a).value;
    clipPlanes[a].constant = b.min[a] + (b.max[a] - b.min[a]) * t;
    planes.push(clipPlanes[a]);
  }
  for (const m of clippable) { m.clippingPlanes = planes; m.needsUpdate = true; }
  document.querySelectorAll('[data-sec]').forEach((el) => el.setAttribute('aria-pressed', el.dataset.sec === S.section));
}

// ---------- strip cutter ----------
const cutter = new THREE.Mesh(
  new THREE.BoxGeometry(1, 1, 1),
  new THREE.MeshBasicMaterial({ color: 0xffb84d, transparent: true, opacity: 0.12, depthWrite: false, side: THREE.DoubleSide }),
);
cutter.add(new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(1, 1, 1)), new THREE.LineBasicMaterial({ color: 0xffb84d })));
cutter.visible = false;
scene.add(cutter);
const cutCtl = {};
const AXIS_V = { x: new THREE.Vector3(1, 0, 0), y: new THREE.Vector3(0, 1, 0), z: new THREE.Vector3(0, 0, 1) };
const TILT_V = { x: new THREE.Vector3(0, 0, 1), y: new THREE.Vector3(1, 0, 0), z: new THREE.Vector3(0, 1, 0) };

function helmetBox() { return new THREE.Box3().setFromObject(S.helmet.pivot); }
function placeCutter() {
  const a = S.cut.axis;
  if (!a || !S.helmet) { cutter.visible = false; return; }
  const b = helmetBox();
  const c = b.getCenter(new THREE.Vector3());
  c[a] = S.cut.pos;
  cutter.position.copy(c);
  const base = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), AXIS_V[a]);
  const tilt = new THREE.Quaternion().setFromAxisAngle(TILT_V[a], S.cut.tilt * DEG);
  cutter.quaternion.copy(tilt.multiply(base));
  const span = b.getSize(new THREE.Vector3()).length() * 1.1;
  cutter.scale.set(span, S.cut.thick, span);
  cutter.visible = !S.strip;
  cutter.updateMatrixWorld(true);
}
function setCutAxis(a) {
  cancelStrip();
  S.cut.axis = S.cut.axis === a ? null : a;
  document.querySelectorAll('[data-cut]').forEach((el) => el.setAttribute('aria-pressed', el.dataset.cut === S.cut.axis));
  $('cutCtls').classList.toggle('off', !S.cut.axis);
  if (S.cut.axis && S.helmet) {
    const b = helmetBox();
    const lo = Math.floor(b.min[a]), hi = Math.ceil(b.max[a]);
    Object.assign(cutCtl.pos.range, { min: lo, max: hi });
    S.cut.pos = Math.round((lo + hi) / 2);
    S.cut.tilt = 0;
    cutCtl.pos.set(S.cut.pos);
    cutCtl.tilt.set(0);
  }
  placeCutter();
}
function buildStrip() {
  const { mesh } = S.helmet;
  mesh.updateMatrixWorld(true);
  return cutStrip(mesh.geometry, mesh.matrixWorld, cutter.matrixWorld, true);
}
function previewStrip() {
  if (!S.helmet || !S.cut.axis) return;
  cancelStrip();
  const geo = buildStrip();
  if (!geo) { toast('The cutter does not touch the helmet here.'); return; }
  S.strip = new THREE.Mesh(geo, stripMat);
  scene.add(S.strip);
  S.helmet.pivot.visible = false;
  cutter.visible = false;
  $('bCancelStrip').disabled = false;
}
function cancelStrip() {
  if (S.strip) { scene.remove(S.strip); S.strip.geometry.dispose(); S.strip = null; }
  if (S.helmet) S.helmet.pivot.visible = true;
  if (S.cut.axis && S.helmet) cutter.visible = true;
  $('bCancelStrip').disabled = true;
}
function exportStrip() {
  if (!S.helmet || !S.cut.axis) return;
  const geo = S.strip ? S.strip.geometry : buildStrip();
  if (!geo) { toast('The cutter does not touch the helmet here.'); return; }
  const stamp = new Date().toTimeString().slice(0, 8).replace(/:/g, '');
  download(new STLExporter().parse(new THREE.Mesh(geo), { binary: true }), `${S.helmet.name}_strip_${S.cut.axis}_${stamp}.stl`);
}
function exportHelmet() {
  if (!S.helmet) return;
  S.helmet.mesh.updateMatrixWorld(true);
  download(new STLExporter().parse(S.helmet.mesh, { binary: true }), `${S.helmet.name}_fitted.stl`);
}

// ---------- presets ----------
function readPresets() {
  try { return JSON.parse(localStorage.getItem(PRESET_KEY)) || {}; } catch { return {}; }
}
function writePresets(p) {
  try { localStorage.setItem(PRESET_KEY, JSON.stringify(p)); return true; } catch { toast('This browser blocked saving.'); return false; }
}
function refreshPresets(select = '') {
  const sel = $('presetSel');
  const names = Object.keys(readPresets()).sort((a, b) => a.localeCompare(b));
  sel.innerHTML = '<option value="">Choose a preset</option>' + names.map((n) => `<option>${n.replace(/</g, '&lt;')}</option>`).join('');
  sel.value = names.includes(select) ? select : '';
}
function savePreset() {
  const name = $('presetName').value.trim();
  if (!name) { toast('Type a name first.'); return; }
  const p = readPresets();
  p[name] = { model: S.model, head: S.headSize.toArray(), helmet: { ...S.h } };
  if (writePresets(p)) { $('presetName').value = ''; refreshPresets(name); toast(`Saved “${name}”`); }
}
function loadPreset() {
  const name = $('presetSel').value;
  const p = readPresets()[name];
  if (!p) return;
  S.headSize.fromArray(p.head);
  showModel(p.model, true);
  if (p.helmet) {
    Object.assign(S.h, p.helmet);
    for (const [k, c] of Object.entries(helmetCtl)) c.set(S.h[k]);
    applyHelmet();
  }
  toast(`Loaded “${name}”`);
}
function deletePreset() {
  const name = $('presetSel').value;
  if (!name || !confirm(`Delete preset “${name}”?`)) return;
  const p = readPresets();
  delete p[name];
  writePresets(p);
  refreshPresets();
}

// ---------- UI wiring ----------
function buildControls() {
  for (const a of ['x', 'y', 'z']) {
    headCtl[a] = control($('headCtls'), {
      label: { x: 'Width', y: 'Height', z: 'Length' }[a] + ' (mm)', min: 100, max: 300, step: 0.5, value: 200, nudge: 1,
      onInput: (v) => { S.headSize[a] = Math.max(1, v); applyHeadScale(); },
    });
  }
  const H = $('helmetCtls');
  const defs = [
    ['mx', 'Move X', -300, 300, 0.5, 1, 1], ['my', 'Move Y', -300, 300, 0.5, 1, 1], ['mz', 'Move Z', -300, 300, 0.5, 1, 1],
    ['rx', 'Tilt X°', -180, 180, 0.5, 1, 1], ['ry', 'Turn Y°', -180, 180, 0.5, 1, 1], ['rz', 'Roll Z°', -180, 180, 0.5, 1, 1],
    ['sx', 'Scale X', 0.5, 1.5, 0.001, 3, 0.01], ['sy', 'Scale Y', 0.5, 1.5, 0.001, 3, 0.01], ['sz', 'Scale Z', 0.5, 1.5, 0.001, 3, 0.01],
    ['su', 'Scale all', 0.5, 1.5, 0.001, 3, 0.01],
  ];
  for (const [k, label, min, max, step, digits, nudge] of defs) {
    if (k === 'rx' || k === 'sx' || k === 'su') H.appendChild(Object.assign(document.createElement('div'), { className: 'gap' }));
    helmetCtl[k] = control(H, {
      label, min, max, step, digits, nudge, value: S.h[k],
      onInput: (v) => { S.h[k] = k.startsWith('s') ? Math.max(0.01, v) : v; applyHelmet(); },
    });
  }
  const C = $('cutCtls');
  cutCtl.pos = control(C, { label: 'Position (mm)', min: -200, max: 200, step: 0.5, value: 0, nudge: 1, onInput: (v) => { S.cut.pos = v; cancelStrip(); placeCutter(); } });
  cutCtl.tilt = control(C, { label: 'Tilt°', min: -180, max: 180, step: 0.5, value: 0, nudge: 1, onInput: (v) => { S.cut.tilt = v; cancelStrip(); placeCutter(); } });
  cutCtl.thick = control(C, { label: 'Thickness (mm)', min: 1, max: 10, step: 0.1, value: 5, nudge: 0.5, onInput: (v) => { S.cut.thick = Math.max(0.1, v); cancelStrip(); placeCutter(); } });

  document.querySelectorAll('[data-model]').forEach((b) => b.addEventListener('click', () => showModel(b.dataset.model)));
  $('bResetHead').addEventListener('click', () => showModel(S.model));
  $('bXray').addEventListener('click', (e) => {
    const on = e.currentTarget.getAttribute('aria-pressed') !== 'true';
    e.currentTarget.setAttribute('aria-pressed', on);
    Object.assign(headMat, { transparent: on, opacity: on ? 0.35 : 1, depthWrite: !on });
    headMat.needsUpdate = true;
  });
  const pick = (input, fn) => input.addEventListener('change', async () => {
    const f = input.files[0];
    if (f) { try { fn(await f.arrayBuffer(), f.name); } catch (err) { console.error(err); toast('Could not read that STL.'); } }
    input.value = '';
  });
  $('bScan').addEventListener('click', () => $('fScan').click());
  pick($('fScan'), loadScan);
  $('bClearScan').addEventListener('click', clearScan);
  $('bHelmet').addEventListener('click', () => $('fHelmet').click());
  pick($('fHelmet'), loadHelmet);
  $('bResetHelmet').addEventListener('click', resetHelmet);
  $('bExportHelmet').addEventListener('click', exportHelmet);
  document.querySelectorAll('[data-sec]').forEach((b) => b.addEventListener('click', () => {
    S.section = S.section === b.dataset.sec && b.dataset.sec !== 'off' ? 'off' : b.dataset.sec;
    for (const a of ['x', 'y', 'z']) $('secr_' + a).value = 0.5;
    applySection();
  }));
  for (const a of ['x', 'y', 'z']) $('secr_' + a).addEventListener('input', applySection);
  document.querySelectorAll('[data-cut]').forEach((b) => b.addEventListener('click', () => setCutAxis(b.dataset.cut)));
  $('bPreviewStrip').addEventListener('click', previewStrip);
  $('bCancelStrip').addEventListener('click', cancelStrip);
  $('bExportStrip').addEventListener('click', exportStrip);
  $('bSavePreset').addEventListener('click', savePreset);
  $('presetName').addEventListener('keydown', (e) => { if (e.key === 'Enter') savePreset(); });
  $('bLoadPreset').addEventListener('click', loadPreset);
  $('bDeletePreset').addEventListener('click', deletePreset);
  $('bView').addEventListener('click', frameAll);

  // drop an STL anywhere: loads as the helmet
  addEventListener('dragover', (e) => { e.preventDefault(); document.body.classList.add('dragging'); });
  addEventListener('dragleave', (e) => { if (!e.relatedTarget) document.body.classList.remove('dragging'); });
  addEventListener('drop', async (e) => {
    e.preventDefault();
    document.body.classList.remove('dragging');
    const f = [...e.dataTransfer.files].find((x) => /\.stl$/i.test(x.name));
    if (f) loadHelmet(await f.arrayBuffer(), f.name); else toast('Drop an .stl file.');
  });
}

function frameAll() {
  const b = sceneBounds();
  const c = b.getCenter(new THREE.Vector3());
  const r = b.getSize(new THREE.Vector3()).length() / 2;
  const dir = camera.position.clone().sub(controls.target).normalize();
  controls.target.copy(c);
  camera.position.copy(c).addScaledVector(dir, r / Math.tan((camera.fov * DEG) / 2) * 1.1);
}

function resize() {
  const w = stage.clientWidth, h = stage.clientHeight;
  renderer.setSize(w, h);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(stage);

buildControls();
refreshPresets();
resize();
renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });

Promise.all([loadHead('male'), loadHead('female')])
  .then(() => { showModel('male'); applySection(); frameAll(); $('loading').hidden = true; })
  .catch((err) => { console.error(err); $('loading').textContent = 'Could not load the head models.'; });

window.__hs = { S, scene, camera, cutStrip };
