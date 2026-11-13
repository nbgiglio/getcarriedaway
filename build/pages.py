"""Builds the site's shared pages (home, portfolios, Lightbench instructions, 404).

Edit this file, not the generated HTML, then run:  python3 build/pages.py .
The header menu, footer and page bodies all come from here.
"""
import os, sys
root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..')
APP = '/tools/lightbench/app/'
LOGO = '<svg width="36" height="36" viewBox="0 0 36 36" aria-hidden="true"><path d="M6 6h24v24H6z" fill="none" stroke="#ffb84d" stroke-width="2" stroke-dasharray="4 3"/><path d="M18 6v6M18 30v-6M6 18h6M30 18h-6" stroke="#ff86a8" stroke-width="2.5"/></svg>'
LB = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ffb84d" stroke-width="2" aria-hidden="true"><path d="M5 4l15 2-2 14-14-2z"/></svg>'

EXT = [
  ('3D modeling', [
    ('BumpMesh', 'https://bumpmesh.com/', 'Adds surface textures to 3D models, in the browser. By CNC Kitchen.'),
    ('Support Fins', 'https://printfins.com/', 'Adds printable support fins to 3D models, in the browser.'),
  ]),
  ('Pattern making', [
    ('Seamly', 'https://seamly.io/', 'Open-source sewing pattern drafting.'),
    ('Valentina', 'https://smart-pattern.com.ua/en/valentina/download/', 'Open-source pattern design software. Download for Windows, Mac or Linux.'),
  ]),
]
ARROW = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9"/></svg>'
def ext_menu():
    out = ''
    for g, items in EXT:
        out += f'<span class="eyebrow">{g}</span><ul class="ext">'
        out += ''.join(f'<li><a href="{u}" target="_blank" rel="noopener"><span>{n}</span>{ARROW}<span class="visually-hidden"> (opens another site)</span></a></li>' for n, u, d in items)
        out += '</ul>'
    return out
def ext_cards():
    out = ''
    for g, items in EXT:
        out += f'<div class="ext-group"><span class="eyebrow">{g}</span><div class="cards">'
        out += ''.join(f'<a class="card ext-card" href="{u}" target="_blank" rel="noopener"><span class="t">{n} {ARROW}</span><span class="d">{d}</span><span class="host">{u.split("/")[2]}</span></a>' for n, u, d in items)
        out += '</div></div>'
    return out

def head(title, desc):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#17171a" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#f6f1e7" media="(prefers-color-scheme: light)">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/brand/gca-icon-dark-bg.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;700&amp;family=Caveat:wght@600;700&amp;family=Nunito:wght@400;600;700;800&amp;family=IBM+Plex+Mono:wght@500&amp;display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/site.js" defer></script>
</head>
<body>
'''

def header(cur):
    a = lambda k: ' aria-current="page"' if cur == k else ''
    tc = ' current' if cur == 'tools' else ''
    return f'''<header class="site-header">
<div class="wrap">
<a class="brand" href="/" aria-label="Get Carrie’d Away, home"><picture><source srcset="/assets/brand/gca-logo-header-on-light.svg" media="(prefers-color-scheme: light)"><img src="/assets/brand/gca-logo-header.svg" alt="Get Carrie’d Away" width="820" height="345"></picture></a>
<button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav">
<svg class="i-open" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
<svg class="i-close" hidden width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
</button>
<nav class="nav" id="site-nav" aria-label="Main">
<a href="/carrie/"{a('carrie')}>Carrie's Work</a>
<a href="/nick/"{a('nick')}>Nick's Work</a>
<div class="tools">
<button class="tools-btn{tc}" type="button" aria-expanded="false" aria-controls="tools-menu">Tools <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
<div class="menu" id="tools-menu" hidden>
<span class="eyebrow">Our tools</span>
<div class="tool-card">
<span class="name">{LB}Lightbench</span>
<p>Projects sewing patterns at true size onto your cutting mat.</p>
<div class="row"><a class="btn amber" href="{APP}">Launch</a><a class="btn line" href="/tools/lightbench/">Instructions</a></div>
</div>
<div class="tool-card">
<span class="name"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#f7b34c" stroke-width="2" aria-hidden="true"><path d="M4 15a8 8 0 0116 0v2H4z"/><path d="M4 17h16"/></svg>HelmetScaler</span>
<p>Fits a helmet STL to a sized head and cuts test-print strips.</p>
<div class="row"><a class="btn amber" href="/tools/helmetscaler/app/">Launch</a></div>
</div>
<div class="tool-card">
<span class="name"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#f7b34c" stroke-width="2" aria-hidden="true"><circle cx="12" cy="4.5" r="2.5"/><path d="M12 8v7M7 10l5-2 5 2M9 22l3-7 3 7"/></svg>Armor Scaler</span>
<p>Turns tape measurements into a 3D body to fit costumes and armour against.</p>
<div class="row"><a class="btn amber" href="/tools/armorscaler/app/">Launch</a></div>
</div>
{ext_menu()}
</div>
</div>
</nav>
</div>
</header>
'''

def footer():
    return '''<footer class="site-footer">
<div class="wrap">
<div><picture><source srcset="/assets/brand/gca-logo-on-light.svg" media="(prefers-color-scheme: light)"><img class="footer-logo" src="/assets/brand/gca-logo.svg" alt="Get Carrie’d Away: the adventure starts here" width="820" height="345" loading="lazy"></picture><span>Carrie &amp; Nick · getcarriedaway.art</span></div>
<nav aria-label="Footer"><a href="/carrie/">Carrie's Work</a><a href="/nick/">Nick's Work</a><a href="/tools/lightbench/">Lightbench</a></nav>
</div>
</footer>
</body>
</html>
'''

SHOT = '''<svg viewBox="0 0 560 400" preserveAspectRatio="xMidYMid slice" role="img" aria-label="A pattern piece projected over a cutting mat grid">
<g stroke="#fff" stroke-opacity=".13"><path d="M0 40H560M0 80H560M0 120H560M0 160H560M0 200H560M0 240H560M0 280H560M0 320H560M0 360H560"/><path d="M40 0V400M80 0V400M120 0V400M160 0V400M200 0V400M240 0V400M280 0V400M320 0V400M360 0V400M400 0V400M440 0V400M480 0V400M520 0V400"/></g>
<path d="M150 70Q200 66 214 34L276 26Q282 106 318 146L330 362H150Z" fill="none" stroke="#f1f0ec" stroke-width="2.5"/>
<path d="M150 70Q100 66 86 34L24 26Q18 106-18 146" fill="none" stroke="#f1f0ec" stroke-opacity=".35" stroke-width="2" stroke-dasharray="6 6"/>
<path d="M150 40V380" stroke="#b48cff" stroke-width="2" stroke-dasharray="10 6"/>
<path d="M240 120V300" stroke="#7fd0ff" stroke-width="2.5"/><path d="M240 120l-6 12h12zM240 300l-6-12h12z" fill="#7fd0ff"/>
<path d="M420 40l100 6-6 92-100-6z" fill="none" stroke="#ffb84d" stroke-width="2"/>
</svg>'''

home = head('Get Carrie’d Away', "Cosplay and costuming by Carrie and Nick, plus the tools we build to make it.") + header('home') + f'''<main>
<section class="wrap hero" id="about-carrie" aria-labelledby="about-carrie-h">
<div>
<span class="eyebrow accent">About Carrie</span>
<h1 id="about-carrie-h">Carrie</h1>
<p class="lead">[Carrie's bio, first paragraph: who she is, how she got into costuming, what she loves to build.]</p>
<p class="lead">[Second paragraph: favourite materials and techniques, where she wears her builds, what she's working on now.]</p>
<div class="row"><a class="btn accent" href="/carrie/">See Carrie's work</a><a class="btn line accent" href="/nick/">Nick's work</a></div>
</div>
<div class="ph dashed portrait"><span class="label">[PHOTO · CARRIE]</span><span class="notch t"></span><span class="notch b"></span><span class="notch l"></span><span class="notch r"></span><span class="tag">CUT 1 · PLACE ON FOLD</span></div>
</section>
<section class="wrap section">
<div class="sec-head"><h2>Cosplay, costuming and the tools to make them</h2><span class="eyebrow">Portfolios</span></div>
<div class="makers">
<a class="maker" href="/carrie/"><div class="ph"><span class="label">[PHOTO · CARRIE IN COSTUME]</span></div><div class="top"><span class="display">Carrie's Work</span><span class="see">See all →</span></div><span class="muted">[One line about Carrie: what she builds, favourite materials, characters.]</span></a>
<a class="maker" href="/nick/"><div class="ph"><span class="label">[PHOTO · NICK IN COSTUME]</span></div><div class="top"><span class="display">Nick's Work</span><span class="see">See all →</span></div><span class="muted">[One line about Nick: armour, props, electronics, whatever he's known for.]</span></a>
</div>
</section>
<section class="band">
<div class="wrap feature">
<div>
<span class="eyebrow amber">From the workshop · Tools</span>
<h2 style="font-size:clamp(40px,4.6vw,56px);line-height:1">Lightbench</h2>
<p class="lead">Projects your sewing pattern at true size onto the cutting mat. Calibrate once, mark the pieces, open out folds, line up the grain and tick each piece off as you cut.</p>
<div class="row"><a class="btn amber" href="{APP}">Launch Lightbench</a><a class="btn line" href="/tools/lightbench/">Instructions</a></div>
<span class="muted" style="font-size:14px">Runs in the browser on a tablet or laptop connected to a projector. Your patterns stay on your device.</span>
</div>
<div class="shot">{SHOT}<span class="tag">TRUE SIZE · GRID MATCHES THE MAT</span></div>
</div>
</section>
<section class="wrap section" style="padding-top:72px;padding-bottom:40px">
<div class="sec-head" style="border:0;padding:0"><h2 style="font-size:32px">Other tools we use</h2><span class="eyebrow">Hosted elsewhere</span></div>
{ext_cards()}
</section>
<section class="wrap section" style="padding-top:40px">
<div class="sec-head"><h2 style="font-size:32px">Patterns to use with it</h2><span class="eyebrow">Coming soon</span></div>
<div class="cards">
<div class="card dashed"><span class="t">[Pattern name]</span><span class="d">[What it makes · sizes]</span></div>
<div class="card dashed"><span class="t">[Pattern name]</span><span class="d">[What it makes · sizes]</span></div>
<div class="card dashed"><span class="t">[Pattern name]</span><span class="d">[What it makes · sizes]</span></div>
</div>
</section>
</main>
''' + footer()

def portfolio(key, who, intro, projects):
    import html
    cards = ''.join(f'''<article class="project"><div class="ph"><span class="label">[PHOTO]</span></div><div class="top"><span class="display">{html.escape(n)}</span><span class="yr">[Year]</span></div><span class="muted" style="font-size:14px">[Character · one line about the build]</span></article>
''' for n in projects)
    other = ('/nick/', "Nick's Work →") if key == 'carrie' else ('/carrie/', "Carrie's Work →")
    return head(f"{who}'s Work · Get Carrie’d Away", f"Cosplay and costume builds by {who}.") + header(key) + f'''<main class="wrap">
<section class="page-head">
<div><span class="eyebrow accent">Portfolio</span><h1>{who}'s Work</h1><p class="lead">{intro}</p></div>
<span class="eyebrow">{len(projects)} project{'s' if len(projects) != 1 else ''}</span>
</section>
<section class="projects" aria-label="Projects">
{cards}</section>
<p style="padding-bottom:48px"><a href="{other[0]}" style="color:var(--accent);font-weight:600;text-decoration:none">{other[1]}</a></p>
</main>
''' + footer()

steps = [
 ('Calibrate to your mat', 'On the Mat tab, type the size of your mat or of a rectangle printed on it. Tap Match the corners and drag A, B, C and D onto its corners. Use the arrows for the last few pixels, then Save the setup so you only do this once.', 'PHOTO · CORNERS ON MAT'),
 ('Open your pattern', "On the Pattern tab, tap Open PDF. Untick sizes you aren't using. For print-at-home pages, use Put pages together and set the trim until the lines meet.", 'SCREENSHOT · SIZES LIST'),
 ('Mark the pieces', "Tap Mark pieces, then Find for me, or tap inside each piece. Shape takes the whole outline; Fill stops at the nearest line. Unmark anything that isn't a piece, then tap Done.", 'SCREENSHOT · MARKED PIECES'),
 ('Open folds and line up the grain', 'Choose Line and draw along a place-on-fold line; it snaps onto the pattern. Tap Mirror on fold to see the whole piece. Draw along the grainline and tap Make this the grain to turn the piece square to the mat.', 'SCREENSHOT · MIRRORED PIECE'),
 ('Cut and tick off', "Untick Show the PDF sheet, then turn on Show one piece at a time. Drag the piece onto your fabric, turn it with two fingers or the 1° buttons, and tick it once it's cut. Press Q to black out the projector while you check your fabric.", 'PHOTO · CUTTING ON THE MAT'),
]
need = [
 ('A tablet or laptop', 'iPad works best. In Safari, tap Share, then Add to Home Screen, for full screen.'),
 ('A projector above the mat', 'Send the picture by screen mirroring or USB-C to HDMI. Bluetooth carries sound only.'),
 ('A gridded cutting mat', 'Its printed grid is what Lightbench calibrates against.'),
 ('A projector PDF', 'A0 or projector files work best. Print-at-home pages can be put together.'),
]
keys = [('V L M','Move · Line · Mark'),('[ ]','Turn 1° (Shift 0.1°)'),('Arrows','Nudge 1 mm'),('R','Turn 90°'),('Q','Quiet (black screen)'),('H','Hide controls'),('G T','Grid · Bias strips'),('0','Back to true size')]
instr = head('Lightbench · Get Carrie’d Away', 'How to project sewing patterns at true size onto your cutting mat with Lightbench.') + header('tools') + f'''<main>
<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">HOME</a><span>/</span><span>TOOLS</span><span>/</span><span class="here" aria-current="page">LIGHTBENCH</span></nav></div>
<section class="wrap page-head" style="padding-top:40px">
<div><h1 style="font-size:clamp(48px,7vw,96px);line-height:.95">Lightbench</h1><p class="lead">Project a sewing pattern at true size onto your cutting mat, one piece at a time, and keep track of what you've cut.</p></div>
<a class="btn amber" href="{APP}" style="font-size:18px;padding:16px 28px">Launch Lightbench</a>
</section>
<section class="wrap" style="padding-bottom:64px"><div class="cards">
{''.join(f'<div class="card"><span class="eyebrow" style="font-size:11px">You need</span><span class="t">{t}</span><span class="d">{d}</span></div>' for t,d in need)}
</div></section>
<section style="border-top:1px solid var(--line)"><div class="wrap" style="padding-block:64px">
<h2 style="margin-bottom:24px">How to use it</h2>
{''.join(f'<div class="step"><span class="n">{i}</span><div><h3>{t}</h3><p>{d}</p></div><div class="ph dashed"><span class="label">[{ph}]</span></div></div>' for i,(t,d,ph) in enumerate(steps,1))}
</div></section>
<section class="band"><div class="wrap twocol">
<div><h2 style="font-size:28px">Keyboard shortcuts</h2><div class="keys">{''.join(f'<span><kbd>{k}</kbd>{v}</span>' for k,v in keys)}</div></div>
<div><h2 style="font-size:28px">Good to know</h2>
<p><b>Your patterns stay on your device.</b> Projects and calibration are saved in this browser only. Clearing website data clears them.</p>
<p><b>Screen changed size?</b> Lightbench asks you to recheck the corners, since the grid may no longer match the mat.</p>
<p><b>Zoomed out?</b> A red note at the bottom means you're not at true size. Tap it to go back.</p></div>
</div></section>
</main>
''' + footer()

files = {
 'index.html': home,
 'carrie/index.html': portfolio('carrie', 'Carrie', "[A short intro from Carrie: how she got into costuming, what she loves to build, where she wears it.]",
   ['Snow White', 'Little Mermaid', 'Great Comet of 1812', 'Creaturess from the Black Lagoon', 'Percy Jackson & The Lightning Thief', 'The Never Ending Story', 'Beetlejuice', 'Bunny the Clown']),
 'nick/index.html': portfolio('nick', 'Nick', "[A short intro from Nick: how he got into costuming, what he loves to build, where he wears it.]", ['Vidar', 'Spartan Warrior', 'Juggernaut', 'Turok Dinosaur Hunter', 'Nappa', 'Rocketeer', 'Mr. Clean']),
 'tools/lightbench/index.html': instr,
 '404.html': head('Not found · Get Carrie’d Away', 'Page not found.') + header('') + '<main class="wrap page-head"><div><span class="eyebrow accent">404</span><h1>That page wandered off.</h1><p class="lead">Try the menu, or go back to the <a href="/" style="color:var(--accent)">home page</a>.</p></div></main>\n' + footer(),
}
for p, s in files.items():
    os.makedirs(os.path.join(root, os.path.dirname(p)), exist_ok=True)
    open(os.path.join(root, p), 'w').write(s)
print('\n'.join(files))
