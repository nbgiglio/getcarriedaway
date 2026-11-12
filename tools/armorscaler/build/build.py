"""Bakes MakeHuman's CC0 base mesh and modelling targets into one binary file for Armor Scaler.

Run: python3 build.py   (downloads from the makehumancommunity/makehuman repo, writes ../app/data/)
Output: body.json (manifest) + body.bin (little-endian buffers). Units stay MakeHuman decimetres;
the app converts to mm.
"""
import json, os, struct, urllib.request, numpy as np

SRC = 'https://raw.githubusercontent.com/makehumancommunity/makehuman/master/makehuman/data/'
CACHE = os.path.join(os.path.dirname(__file__), '.cache')
OUT = os.path.join(os.path.dirname(__file__), '..', 'app', 'data')

MEASURES = ['neck-circ', 'neck-height', 'upperarm-circ', 'upperarm-length', 'lowerarm-length', 'wrist-circ',
            'frontchest-dist', 'bust-circ', 'underbust-circ', 'waist-circ', 'napetowaist-dist', 'waisttohip-dist',
            'shoulder-dist', 'hips-circ', 'upperleg-height', 'thigh-circ', 'lowerleg-height', 'calf-circ',
            'knee-circ', 'ankle-circ']

# Vertex rulers from MakeHuman plugins/0_modeling_a_measurement.py (CC0 data, AGPL code; indices only).
RULERS = {
 'neck-circ': [7514,10358,7631,7496,7488,7489,7474,7475,7531,7537,7543,7549,7555,7561,7743,7722,856,1030,1051,850,844,838,832,826,820,756,755,770,769,777,929,3690,804,800,808,801,799,803,7513,7515,7521,7514],
 'neck-height': [853,854,855,856,857,858,1496,1491],
 'upperarm-circ': [8383,8393,8392,8391,8390,8394,8395,8399,10455,10516,8396,8397,8398,8388,8387,8386,10431,8385,8384,8389],
 'upperarm-length': [8274,10037],
 'lowerarm-length': [10040,10548],
 'wrist-circ': [10208,10211,10212,10216,10471,10533,10213,10214,10215,10205,10204,10203,10437,10202,10201,10206,10200,10210,10209,10208],
 'frontchest-dist': [1437,8125],
 'bust-circ': [8439,8455,8462,8446,8478,8494,8557,8510,8526,8542,10720,10601,10603,10602,10612,10611,10610,10613,10604,10605,10606,3942,3941,3940,3950,3947,3948,3949,3938,3939,3937,4065,1870,1854,1838,1885,1822,1806,1774,1790,1783,1767,1799,8471],
 'underbust-circ': [10750,10744,10724,10725,10748,10722,10640,10642,10641,10651,10650,10649,10652,10643,10644,10645,10646,10647,10648,3988,3987,3986,3985,3984,3983,3982,3992,3989,3990,3991,3980,3981,3979,4067,4098,4073,4072,4094,4100,4082,4088,4088],
 'waist-circ': [4121,10760,10757,10777,10776,10779,10780,10778,10781,10771,10773,10772,10775,10774,10814,10834,10816,10817,10818,10819,10820,10821,4181,4180,4179,4178,4177,4176,4175,4196,4173,4131,4132,4129,4130,4128,4138,4135,4137,4136,4133,4134,4108,4113,4118,4121],
 'napetowaist-dist': [1491,4181],
 'waisttohip-dist': [4121,4341],
 'shoulder-dist': [7478,8274],
 'hips-circ': [4341,10968,10969,10971,10970,10967,10928,10927,10925,10926,10923,10924,10868,10875,10861,10862,4228,4227,4226,4242,4234,4294,4293,4296,4295,4297,4298,4342,4345,4346,4344,4343,4361,4341],
 'upperleg-height': [10970,11230],
 'thigh-circ': [11071,11080,11081,11086,11076,11077,11074,11075,11072,11073,11069,11070,11087,11085,11084,12994,11083,11082,11079,11071],
 'lowerleg-height': [11225,12820],
 'calf-circ': [11339,11336,11353,11351,11350,13008,11349,11348,11345,11337,11344,11346,11347,11352,11342,11343,11340,11341,11338,11339],
 'ankle-circ': [11460,11464,11458,11459,11419,11418,12958,12965,12960,12963,12961,12962,12964,12927,13028,12957,11463,11461,11457,11460],
 'knee-circ': [11223,11230,11232,11233,11238,11228,11229,11226,11227,11224,11225,11221,11222,11239,11237,11236,13002,11235,11234,11223],
}

def fetch(rel):
    path = os.path.join(CACHE, rel.replace('/', '__'))
    if not os.path.exists(path):
        os.makedirs(CACHE, exist_ok=True)
        with urllib.request.urlopen(SRC + rel) as r, open(path, 'wb') as f:
            f.write(r.read())
    return open(path, encoding='utf-8').read()

def read_target(rel, n):
    d = np.zeros((n, 3), np.float64)
    for line in fetch('targets/' + rel + '.target').splitlines():
        p = line.split()
        if len(p) == 4 and not line.startswith('#'):
            i = int(p[0])
            if i < n:
                d[i] = [float(p[1]), float(p[2]), float(p[3])]
    return d

# --- base mesh: body group only
verts, faces, group = [], [], None
for line in fetch('3dobjs/base.obj').splitlines():
    if line.startswith('v '):
        verts.append([float(x) for x in line.split()[1:4]])
    elif line.startswith('g '):
        group = line.split()[1]
    elif line.startswith('f ') and group == 'body':
        idx = [int(p.split('/')[0]) - 1 for p in line.split()[1:]]
        for k in range(1, len(idx) - 1):
            faces.append((idx[0], idx[k], idx[k + 1]))
faces = np.array(faces, np.int64)
n = int(faces.max()) + 1          # body vertices are the first n
base = np.array(verts[:n])
print('body verts', n, 'tris', len(faces))

targets = []   # (name, sex, delta)
for m in MEASURES:
    for side in ('decr', 'incr'):
        targets.append((f'measure-{m}-{side}', '*', read_target(f'measure/measure-{m}-{side}', n)))
bodies = {}
for sex, g in (('f', 'female'), ('m', 'male')):
    uni = read_target(f'macrodetails/universal-{g}-young-averagemuscle-averageweight', n)
    # MakeHuman's default human mixes the three ethnic targets equally; the universal targets are near-empty.
    eth = sum(read_target(f'macrodetails/{e}-{g}-young', n) for e in ('african', 'asian', 'caucasian')) / 3
    bodies[sex] = base + uni + eth
    for side in ('minheight', 'maxheight'):
        targets.append((f'height-{side}', sex, read_target(f'macrodetails/height/{g}-young-averagemuscle-averageweight-{side}', n)))
    for kind, a, b in (('weight', 'minweight', 'maxweight'), ('muscle', 'minmuscle', 'maxmuscle')):
        for side in (a, b):
            parts = ('averagemuscle', side) if kind == 'weight' else (side, 'averageweight')
            full = read_target(f'macrodetails/universal-{g}-young-{parts[0]}-{parts[1]}', n)
            targets.append((f'{kind}-{side}', sex, full - uni))
for side in ('mincup', 'maxcup'):
    targets.append((f'cup-{side}', 'f', read_target(f'breast/female-young-averagemuscle-averageweight-{side}-averagefirmness', n)))

# crotch: lowest midline vertex above the knees, on the female and male base
def crotch(v):
    knee_y = v[11230, 1]
    mid = np.where((np.abs(v[:, 0]) < 0.02) & (v[:, 1] > knee_y))[0]
    return int(mid[np.argmin(v[mid, 1])])

blob = bytearray()
def put(arr):
    off = len(blob)
    blob.extend(arr.tobytes())
    while len(blob) % 4:
        blob.append(0)
    return off

man = {'source': 'MakeHuman 1.x base mesh and targets (CC0)', 'units': 'dm', 'vertexCount': n,
       'faces': {'offset': put(faces.astype('<u2')), 'count': int(faces.size)},
       'bodies': {s: put(v.astype('<f4')) for s, v in bodies.items()},
       'rulers': RULERS, 'crotch': {s: crotch(v) for s, v in bodies.items()}, 'targets': []}
for name, sex, d in targets:
    idx = np.where(np.abs(d).max(axis=1) > 1e-7)[0]
    vals = d[idx]
    scale = float(np.abs(vals).max()) / 32767 if len(idx) else 1.0
    q = np.round(vals / scale).astype('<i2')
    man['targets'].append({'name': name, 'sex': sex, 'count': int(len(idx)), 'scale': scale,
                           'indices': put(idx.astype('<u2')), 'deltas': put(q)})
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'body.bin'), 'wb').write(blob)
json.dump(man, open(os.path.join(OUT, 'body.json'), 'w'), separators=(',', ':'))
print('wrote', len(blob), 'bytes,', len(targets), 'targets; crotch', man['crotch'])
