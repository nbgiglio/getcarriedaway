"""Portfolio grids and project write-up pages, built from build/projects.py."""
import html, re


def _md(t):
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html.escape(t, quote=False))


def _slug(n):
    return re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')


ALIASES = {'the-never-ending-story': 'neverending-story'}


def portfolio(head, header, footer, key, who, intro, names, docs):
    by = {}
    for d in docs:
        by[d['slug']] = d
        by[_slug(d['title'])] = d
    cards = []
    for n in names:
        s = _slug(n)
        d = by.get(s) or by.get(ALIASES.get(s, ''))
        if d:
            img = (f'<img src="/{key}/{d["slug"]}/img/{d["cover"]}-sm.jpg" alt="" loading="lazy">' if d['cover']
                   else '<span class="label">[PHOTO]</span>')
            ev = f'<span class="ev">{html.escape(d["event"])}</span>' if d['event'] else ''
            cards.append(
                f'<a class="project" href="/{key}/{d["slug"]}/"><div class="ph">{img}</div>'
                f'<div class="top"><span class="display">{html.escape(d["title"])}</span></div>{ev}'
                f'<span class="muted" style="font-size:14px">{html.escape(d["card"])}</span>'
                f'<span class="read">Read the build →</span></a>')
        else:
            cards.append(
                f'<article class="project"><div class="ph"><span class="label">[PHOTO]</span></div>'
                f'<div class="top"><span class="display">{html.escape(n)}</span><span class="yr">[Year]</span></div>'
                f'<span class="muted" style="font-size:14px">[Character · one line about the build]</span></article>')
    other = ('/nick/', 'Nick\'s Work →') if key == 'carrie' else ('/carrie/', 'Carrie\'s Work →')
    count = f'{len(names)} project{"s" if len(names) != 1 else ""}'
    return (head(f"{who}'s Work · Get Carrie’d Away", f'Cosplay and costume builds by {who}.') + header(key) +
            '<main class="wrap">\n<section class="page-head">\n'
            f'<div><span class="eyebrow accent">Portfolio</span><h1>{who}\'s Work</h1><p class="lead">{intro}</p></div>\n'
            f'<span class="eyebrow">{count}</span>\n</section>\n'
            '<section class="projects" aria-label="Projects">\n' + '\n'.join(cards) + '\n</section>\n'
            f'<p style="padding-bottom:48px"><a href="{other[0]}" style="color:var(--accent);font-weight:600;text-decoration:none">{other[1]}</a></p>\n'
            '</main>\n' + footer())


def project_page(head, header, footer, key, who, d):
    base = f'/{key}/{d["slug"]}/img/'

    def fig(stem, cap):
        c = html.escape(cap)
        return (f'<figure><a href="{base}{stem}.jpg" target="_blank" rel="noopener">'
                f'<img src="{base}{stem}-sm.jpg" alt="{c}" loading="lazy"></a><figcaption>{c}</figcaption></figure>')

    if d['cover']:
        cover = f'<figure class="proj-cover"><img src="{base}{d["cover"]}.jpg" alt="{html.escape(d["title"])}"></figure>'
    else:
        cover = '<div class="ph dashed proj-cover"><span class="label">[PHOTO · THE FINISHED COSTUME]</span></div>'
    facts = ''.join(f'<div><dt>{html.escape(a)}</dt><dd>{html.escape(b)}</dd></div>' for a, b in d['facts'])
    secs = []
    for s in d['sections']:
        body = ''.join(f'<p>{_md(x)}</p>' for x in s.get('paras', []))
        if s.get('table'):
            hd, rows = s['table']
            body += ('<div class="table-wrap"><table><thead><tr>' + ''.join(f'<th scope="col">{html.escape(h)}</th>' for h in hd) +
                     '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{html.escape(c)}</td>' for c in r) + '</tr>' for r in rows) +
                     '</tbody></table></div>')
        if s.get('tags'):
            body += '<ul class="tags">' + ''.join(f'<li>{html.escape(t)}</li>' for t in s['tags']) + '</ul>'
        if s.get('steps'):
            body += '<ol class="steps">' + ''.join(f'<li>{html.escape(t)}</li>' for t in s['steps']) + '</ol>'
        gal = ('<div class="gallery">' + ''.join(fig(a, b) for a, b in s['images']) + '</div>') if s.get('images') else ''
        secs.append(f'<section class="proj-sec"><h2>{html.escape(s["title"])}</h2><div class="prose">{body}</div>{gal}</section>')
    quote = f'<blockquote>“{html.escape(d["quote"])}”</blockquote>' if d.get('quote') else ''
    event = f'<span class="chip">{html.escape(d["event"])}</span>' if d['event'] else ''
    intro = ''.join(f'<p class="lead">{_md(x)}</p>' for x in d['intro'])
    return (head(f"{d['title']} · {who}'s Work · Get Carrie’d Away", f"{d['title']}: {d['card']}. A costume build by {who}.") + header(key) +
            '<main>\n'
            f'<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/{key}/">{who.upper()}\'S WORK</a><span>/</span>'
            f'<span class="here" aria-current="page">{html.escape(d["title"].upper())}</span></nav></div>\n'
            f'<section class="wrap proj-hero">\n<div class="proj-intro"><span class="eyebrow accent">{html.escape(d["subtitle"])}</span>'
            f'<h1>{html.escape(d["title"])}</h1>{event}{intro}{quote}</div>\n{cover}\n</section>\n'
            f'<section class="wrap" aria-label="At a glance"><dl class="facts">{facts}</dl></section>\n'
            '<div class="wrap">\n' + '\n'.join(secs) + '\n</div>\n'
            f'<p class="wrap" style="padding-block:40px 56px"><a href="/{key}/" style="color:var(--accent);font-weight:700;text-decoration:none">← All of {who}\'s work</a></p>\n'
            '</main>\n' + footer())
