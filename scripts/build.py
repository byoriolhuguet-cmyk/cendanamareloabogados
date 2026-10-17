"""Generador del sitio estático de Cendán & Amarelo Abogados.

Uso:  sh scripts/build.sh   (genera el HTML y minifica CSS/JS)
      python3 scripts/build.py   (sólo HTML, sitemap.xml y llms.txt)

Contenido editable: scripts/content.py (áreas, equipo, FAQ...) y scripts/legal_content.py.
Rutas absolutas (/css/..., /contacto/) que conservan las URL de la web anterior.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from content import AREAS, FAQ, GUIDES, HISTORY, KEYS, METHOD, NAV, PROVINCES, TEAM  # noqa: E402
from icons import ICONS  # noqa: E402
from legal_content import PAGES as LEGAL  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOMAIN = 'https://www.cendanamareloabogados.com'
UPDATED = '2026-10-17'
PHONE_TEL = '+34982223053'
PHONE_HTML = '982&nbsp;223&nbsp;053'
EMAIL = 'despacho@cendanamareloabogados.com'
# WhatsApp: número del despacho. Cambiar aquí si se usa un móvil distinto (formato internacional sin "+").
WHATSAPP = '34982223053'
WA_TEXT = 'Hola,%20quisiera%20hacer%20una%20consulta%20al%20despacho.'
WA_URL = f'https://wa.me/{WHATSAPP}?text={WA_TEXT}'
MAPS = 'https://www.google.com/maps/search/?api=1&amp;query=Avenida+de+A+Coru%C3%B1a+10-14+27003+Lugo'
CTA_LABEL = 'Solicitar consulta'   # una sola etiqueta para la intención "contactar por formulario"
SITEMAP = []
AREA_BY_ID = {a['id']: a for a in AREAS}
AREA_LABEL = {a['id']: a['name'].replace('Derecho ', '').replace('Dº ', '').split(' y ')[0] for a in AREAS}
AREA_LABEL['general'] = 'General'
MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']


def load_news():
    path = os.path.join(ROOT, 'data', 'news.json')
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {'updated': None, 'items': []}


NEWS = load_news()


def fecha(iso):
    """'2026-10-17...' -> '17 de octubre de 2026'."""
    y, m, d = int(iso[:4]), int(iso[5:7]), int(iso[8:10])
    return f'{d} de {MONTHS[m - 1]} de {y}'


# ---------------------------------------------------------------- Piezas comunes

def ico(name, cls='ico'):
    box, inner = ICONS[name]
    return f'<svg class="{cls}" viewBox="{box}" aria-hidden="true" focusable="false">{inner}</svg>'


ARROW = ico('arrow_up_right')

# Teselas del isotipo (centro x, centro y, semidiagonal) en el espacio 116x68 del logotipo.
# El orden marca la secuencia de aparición: de la base hacia la cima, como se construye un tejado.
TILES = [(15.5, 63.5, 12.5), (56.5, 56.5, 19.5), (81.5, 66.5, 9.5), (36, 40, 17), (97.5, 49.5, 14.5),
         (77.5, 33, 16.5), (18, 24.5, 11.5), (58, 16, 14), (96.5, 13, 9)]


def tiles_svg(cls, uid):
    """Isotipo reconstruido en SVG con la geometría exacta del logotipo.

    Las teselas sólo cambian de opacidad al animarse (nunca se giran ni escalan),
    así el logotipo conserva siempre su forma.
    """
    polys = ''.join(
        f'<polygon style="--i:{i}" points="{x},{y - r} {x + r},{y} {x},{y + r} {x - r},{y}"/>'
        for i, (x, y, r) in enumerate(TILES))
    return (f'<svg class="{cls}" viewBox="0 0 116 68" aria-hidden="true" focusable="false">'
            f'<defs><linearGradient id="g{uid}" x1="0" y1="0" x2="0" y2="68" gradientUnits="userSpaceOnUse">'
            '<stop offset="0" stop-color="#f8dac4"/><stop offset=".5" stop-color="#f0a479"/><stop offset="1" stop-color="#e8702a"/>'
            f'</linearGradient><clipPath id="c{uid}"><rect width="116" height="67.6"/></clipPath></defs>'
            f'<g fill="url(#g{uid})" clip-path="url(#c{uid})">{polys}</g></svg>')


def picture(slug, alt, cls='', eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture class="{cls}"><source srcset="/assets/img/equipo/{slug}.webp" type="image/webp">'
            f'<img src="/assets/img/equipo/{slug}.jpg" width="375" height="450" {load} decoding="async" alt="{alt}"></picture>')


def logo(cls='brand'):
    return (f'<a class="{cls}" href="/" aria-label="Cendán &amp; Amarelo Abogados, inicio">'
            '<picture><source srcset="/assets/img/logo.webp" type="image/webp">'
            '<img src="/assets/img/logo.png" width="298" height="123" alt=""></picture></a>')


def btn_primary(extra=''):
    return f'<a class="btn btn-dark {extra}" href="/contacto/"><span>{CTA_LABEL}</span><i>{ARROW}</i></a>'


def btn_whatsapp(extra=''):
    return f'<a class="btn btn-line btn-wa {extra}" href="{WA_URL}" rel="noopener" target="_blank">{ico("whatsapp")}<span>WhatsApp</span></a>'


def btn_call(extra=''):
    return f'<a class="btn btn-line {extra}" href="tel:{PHONE_TEL}">{ico("phone")}<span>{PHONE_HTML}</span></a>'


def header(active):
    cur = ' aria-current="page"'
    items = ''.join(f'<li><a href="{h}"{cur if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f'''  <header class="site-header">
    <div class="wrap header-bar">
      {logo()}
      <nav class="nav" id="nav" aria-label="Principal">
        <ul>{items}<li class="nav-only-m"><a href="/contacto/"{cur if active == '/contacto/' else ''}>Contacto</a></li></ul>
        <a class="nav-phone" href="tel:{PHONE_TEL}">{ico('phone')}<span>{PHONE_HTML}</span></a>
        <a class="btn btn-dark btn-sm" href="/contacto/"><span>{CTA_LABEL}</span></a>
        <div class="nav-extra">
          {btn_whatsapp()}
          <p>Avda. de A Coruña 10-14, Entlo. 27003 Lugo<br>Lunes a jueves, de 9:00 a 14:30 y de 16:00 a 19:30. Viernes, de 9:00 a 15:00</p>
        </div>
      </nav>
      <a class="head-call" href="tel:{PHONE_TEL}" aria-label="Llamar al {PHONE_HTML}">{ico('phone')}</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Abrir menú"><span></span><span></span></button>
    </div>
  </header>'''


def whatsapp_float():
    return f'''  <a class="wa-float" href="{WA_URL}" rel="noopener" target="_blank" aria-label="Escríbanos por WhatsApp">
    {ico('whatsapp')}<span>Escríbanos</span>
  </a>'''


def footer():
    areas = ''.join(f'<li><a href="/{a["slug"]}/">{a["name"]}</a></li>' for a in AREAS)
    return f'''  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div class="footer-brand">
        {logo('brand brand-footer')}
        <p>Despacho de abogados en Lugo desde 1973. Asesoramiento a empresas y particulares en toda Galicia.</p>
      </div>
      <div>
        <p class="footer-title">Despacho</p>
        <ul class="footer-list">
          <li><a href="tel:{PHONE_TEL}">{PHONE_HTML}</a></li>
          <li><a href="{WA_URL}" rel="noopener" target="_blank">WhatsApp</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Avda. de A Coruña 10-14, Entlo.<br>27003 Lugo</li>
          <li>L a J: 9:00 a 14:30 y 16:00 a 19:30<br>V: 9:00 a 15:00</li>
        </ul>
      </div>
      <nav aria-label="Áreas de práctica">
        <p class="footer-title">Áreas</p>
        <ul class="footer-list">{areas}</ul>
      </nav>
      <nav aria-label="Enlaces">
        <p class="footer-title">Enlaces</p>
        <ul class="footer-list">
          <li><a href="/despacho-abogados-lugo/">Quiénes somos</a></li>
          <li><a href="/equipo-profesional/">Profesionales</a></li>
          <li><a href="/actualidad-juridica/">Actualidad</a></li>
          <li><a href="/guias-juridicas/">Guías jurídicas</a></li>
          <li><a href="/abogados-galicia/">Galicia y España</a></li>
          <li><a href="/contacto/">Contacto</a></li>
          <li><a href="mailto:{EMAIL}?subject=Curr%C3%ADculum">Envíenos su CV</a></li>
        </ul>
      </nav>
    </div>
    <div class="wrap footer-bottom">
      <p>© <span data-year>2026</span> Cendán &amp; Amarelo Abogados, S.L.P.</p>
      <ul class="footer-legal">
        <li><a href="/aviso-legal/">Aviso legal</a></li>
        <li><a href="/accesibilidad/">Accesibilidad</a></li>
        <li><a href="/politica-de-cookies-ue/">Política de cookies</a></li>
      </ul>
      <p class="social">
        <a href="https://es-es.facebook.com/pages/Cendan-Amarelo-Abogados/226246534135877" rel="noopener" target="_blank" aria-label="Facebook">{ico('facebook')}</a>
        <a href="https://twitter.com/cendanamarelo" rel="noopener" target="_blank" aria-label="X (Twitter)">{ico('x')}</a>
      </p>
    </div>
  </footer>'''


def quickbar():
    """Información esencial de un vistazo: cuatro accesos directos."""
    return f'''    <section class="quick" aria-label="Contacto rápido">
      <div class="wrap">
        <ul class="quick-grid" role="list">
          <li class="reveal"><a href="tel:{PHONE_TEL}">{ico('phone')}<span><small>Llámenos</small>{PHONE_HTML}</span></a></li>
          <li class="reveal" style="--d:70ms"><a href="{WA_URL}" rel="noopener" target="_blank">{ico('whatsapp')}<span><small>WhatsApp</small>Escríbanos ahora</span></a></li>
          <li class="reveal" style="--d:140ms"><a href="{MAPS}" rel="noopener" target="_blank">{ico('map_pin')}<span><small>Oficina</small>Avda. de A Coruña 10-14, Lugo</span></a></li>
          <li class="reveal" style="--d:210ms"><a href="/contacto/">{ico('clock')}<span><small>Horario</small>L a J 9:00 a 19:30 · V 9:00 a 15:00</span></a></li>
        </ul>
      </div>
    </section>'''


def contact_block(title='¿Necesita asesoramiento?',
                  text='Contacte con nosotros sin compromiso y le daremos una primera valoración.', eyebrow=True):
    eb = '<p class="eyebrow reveal">Contacto</p>' if eyebrow else ''
    return f'''    <section class="contact-band" aria-labelledby="cb-title">
      <div class="wrap band-grid">
        <div class="band-copy">
          {eb}
          <h2 id="cb-title" class="reveal">{title}</h2>
          <p class="reveal">{text}</p>
          <div class="actions reveal">{btn_primary()}{btn_whatsapp()}</div>
        </div>
        <dl class="data-list">
          <div class="reveal"><dt>{ico('phone')}Teléfono</dt><dd class="dd-big"><a href="tel:{PHONE_TEL}">{PHONE_HTML}</a></dd></div>
          <div class="reveal" style="--d:80ms"><dt>{ico('envelope_simple')}Correo</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          <div class="reveal" style="--d:160ms"><dt>{ico('map_pin')}Oficina</dt><dd>Avda. de A Coruña 10-14, Entlo. 27003 Lugo<br><a class="u" href="{MAPS}" rel="noopener" target="_blank">Cómo llegar</a></dd></div>
          <div class="reveal" style="--d:240ms"><dt>{ico('clock')}Horario</dt><dd>Lunes a jueves, de 9:00 a 14:30 y de 16:00 a 19:30<br>Viernes, de 9:00 a 15:00</dd></div>
        </dl>
      </div>
      {tiles_svg('band-tiles', 'cb')}
    </section>'''


def areas_bento(heading='h3'):
    """Bento asimétrico: una celda por área, con tres puntos clave visibles de un vistazo."""
    cells = ''
    for i, a in enumerate(AREAS):
        keys = ''.join(f'<li>{k}</li>' for k in KEYS[a['id']])
        cells += f'''
          <li class="bento-cell cell-{a["id"]} reveal" style="--d:{i * 70}ms">
            <a href="/{a["slug"]}/">
              <{heading}>{a["name"]}</{heading}>
              <ul class="keys">{keys}</ul>
              <span class="cell-go">Conocer más {ARROW}</span>
            </a>
          </li>'''
    return f'<ul class="bento" role="list">{cells}\n        </ul>'


def team_grid():
    out = '<ul class="team" role="list">'
    for i, (slug, name, role) in enumerate(TEAM):
        out += f'''
          <li class="member reveal" style="--d:{i * 80}ms" id="{slug}">
            <figure>
              {picture(slug, f'{name}, {role.lower()} de Cendán &amp; Amarelo Abogados')}
              <figcaption><strong>{name}</strong><span>{role}</span></figcaption>
            </figure>
          </li>'''
    return out + '\n        </ul>'


def method_list():
    items = ''.join(f'<li class="reveal" style="--d:{n * 120}ms"><h3>{t}</h3><p>{d}</p></li>' for n, (t, d) in enumerate(METHOD))
    return f'<ol class="method" role="list">{items}</ol>'


def faq_list(items):
    return ''.join(
        f'<details class="reveal" style="--d:{n * 60}ms"><summary><h3>{q}</h3>{ico("ph_caret_down", "ico caret")}</summary><p>{r}</p></details>'
        for n, (q, r) in enumerate(items))


def news_list(items, cls=''):
    """Noticias externas: titular, fuente y fecha, enlazando a la fuente original."""
    out = ''
    for n, it in enumerate(items):
        area = it.get('area', 'general')
        out += (f'<li class="news-item reveal" style="--d:{(n % 6) * 50}ms" data-area="{area}" data-scope="{it.get("scope", "españa")}">'
                f'<a href="{esc(it["url"])}" rel="noopener nofollow" target="_blank">'
                f'<span class="news-meta"><span class="news-tag">{AREA_LABEL.get(area, "General")}</span>'
                f'<time datetime="{it["date"]}">{fecha(it["date"])}</time></span>'
                f'<span class="news-title">{html_escape(it["title"])}</span>'
                f'<span class="news-src">{html_escape(it["source"])} {ARROW}</span></a></li>')
    return f'<ol class="news-list {cls}" role="list">{out}</ol>'


def html_escape(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def marquee():
    words = ''.join(f'<span>{a["name"].replace("Derecho ", "")}</span><i aria-hidden="true"></i>' for a in AREAS)
    return f'''    <div class="marquee" aria-hidden="true">
      <div class="marquee-track"><div>{words}</div><div>{words}</div></div>
    </div>'''


def guide_cards(guides, heading='h3'):
    cards = ''.join(
        f'<li class="guide-card reveal" style="--d:{n * 80}ms"><a href="/guias-juridicas/{g["slug"]}/">'
        f'<span class="news-tag">{AREA_LABEL[g["area"]]}</span><{heading}>{g["title"]}</{heading}><p>{g["desc"]}</p>'
        f'<span class="cell-go">Leer la guía {ARROW}</span></a></li>' for n, g in enumerate(guides))
    return f'<ul class="guides" role="list">{cards}</ul>'


def page_hero(eyebrow, h1, lead, crumbs, ctas=True):
    trail = '<li><a href="/">Inicio</a></li>' + ''.join(
        f'<li><a href="{u}">{n}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{n}</li>'
        for i, (n, u) in enumerate(crumbs))
    actions = f'<div class="actions">{btn_primary()}{btn_call()}</div>' if ctas else ''
    return f'''    <section class="page-hero">
      <div class="wrap page-hero-grid">
        <div>
          <nav class="crumbs" aria-label="Migas de pan"><ol>{trail}</ol></nav>
          <p class="eyebrow">{eyebrow}</p>
          <h1>{h1}</h1>
          {f'<p class="lead">{lead}</p>' if lead else ''}
          {actions}
        </div>
        {tiles_svg('page-tiles', 'ph')}
      </div>
    </section>'''


def aside_contact():
    """Tarjeta de contacto lateral (fija al hacer scroll en escritorio)."""
    return f'''<aside class="aside-card" aria-label="Contacto">
          <p class="aside-title">¿Hablamos de su caso?</p>
          <p>Primera valoración sin compromiso.</p>
          {btn_primary('btn-block')}
          {btn_whatsapp('btn-block')}
          <a class="aside-phone" href="tel:{PHONE_TEL}">{ico('phone')}{PHONE_HTML}</a>
        </aside>'''


# ---------------------------------------------------------------- Plantilla

ORG = {
    '@type': ['LegalService', 'LocalBusiness'], '@id': DOMAIN + '/#despacho',
    'name': 'Cendán & Amarelo Abogados', 'legalName': 'Cendán & Amarelo Abogados, S.L.P.',
    'alternateName': ['Cendán y Amarelo Abogados', 'Cendán & Amarelo, Abogados y Asesores Tributarios'],
    'taxID': 'B27365667',
    'description': 'Despacho de abogados en Lugo fundado en 1973, con servicio en toda Galicia. Derecho penal económico, mercantil y concursal, tributario, civil y procesal, administrativo y laboral.',
    'url': DOMAIN + '/', 'logo': DOMAIN + '/assets/img/logo.png', 'image': DOMAIN + '/assets/img/og-cendan-amarelo.jpg',
    'foundingDate': '1973', 'founder': {'@type': 'Person', 'name': 'Antonio Cendán Corredoira'},
    'telephone': PHONE_TEL, 'faxNumber': '+34982223947', 'email': EMAIL, 'priceRange': '€€',
    'knowsLanguage': ['es', 'gl'],
    'address': {'@type': 'PostalAddress', 'streetAddress': 'Avenida de A Coruña, 10-14, Entresuelo', 'addressLocality': 'Lugo',
                'postalCode': '27003', 'addressRegion': 'Galicia', 'addressCountry': 'ES'},
    'hasMap': MAPS.replace('&amp;', '&'),
    'areaServed': [{'@type': 'City', 'name': 'Lugo'}, {'@type': 'AdministrativeArea', 'name': 'Provincia de Lugo'},
                   {'@type': 'AdministrativeArea', 'name': 'Galicia'}],
    'openingHoursSpecification': [
        {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'], 'opens': '09:00', 'closes': '14:30'},
        {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'], 'opens': '16:00', 'closes': '19:30'},
        {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Friday', 'opens': '09:00', 'closes': '15:00'}],
    'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': PHONE_TEL, 'email': EMAIL,
                      'availableLanguage': ['es', 'gl'], 'areaServed': 'ES-GA'}],
    'sameAs': ['https://twitter.com/cendanamarelo', 'https://es-es.facebook.com/pages/Cendan-Amarelo-Abogados/226246534135877'],
    'knowsAbout': ['Derecho penal económico', 'Derecho penal', 'Derecho mercantil', 'Derecho concursal', 'Derecho tributario',
                   'Derecho civil', 'Derecho procesal', 'Derecho de familia', 'Derecho administrativo', 'Derecho laboral'],
    'employee': [{'@type': 'Person', 'name': n, 'jobTitle': r, 'image': f'{DOMAIN}/assets/img/equipo/{s}.jpg'} for s, n, r in TEAM],
    'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Áreas de práctica', 'itemListElement': [
        {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': a['name'], 'url': f'{DOMAIN}/{a["slug"]}/'}} for a in AREAS]},
}


def esc(s):
    return s.replace('&', '&amp;').replace('&amp;amp;', '&amp;').replace('"', '&quot;')


def page_head(title, desc, path, crumbs=None, extra_schema=None, home=False, robots='index, follow, max-snippet:-1, max-image-preview:large'):
    graph = [ORG] if home else [{'@type': ['LegalService', 'LocalBusiness'], '@id': DOMAIN + '/#despacho', 'name': 'Cendán & Amarelo Abogados'}]
    if crumbs:
        items = [{'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': DOMAIN + '/'}]
        items += [{'@type': 'ListItem', 'position': n, 'name': name, 'item': DOMAIN + url} for n, (name, url) in enumerate(crumbs, 2)]
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': items})
    graph.extend(extra_schema or [])
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    intro_js = ("try{if(!sessionStorage.getItem('ca-intro')){d.classList.add('is-intro');sessionStorage.setItem('ca-intro','1')}}catch(e){}"
                if home else '')
    preload_img = ('\n  <link rel="preload" as="image" type="image/webp" href="/assets/img/equipo/jesus-a-amarelo-fernandez.webp" fetchpriority="high">'
                   if home else '')
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{DOMAIN}{path}">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#fcfbfa">
  <meta name="color-scheme" content="light">
  <meta name="format-detection" content="telephone=yes">
  <meta name="geo.region" content="ES-GA">
  <meta name="geo.placename" content="Lugo">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_ES">
  <meta property="og:site_name" content="Cendán &amp; Amarelo Abogados">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{DOMAIN}{path}">
  <meta property="og:image" content="{DOMAIN}/assets/img/og-cendan-amarelo.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@cendanamarelo">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preload" href="/assets/fonts/cormorant-garamond.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/jost.woff2" as="font" type="font/woff2" crossorigin>{preload_img}
  <link rel="alternate" type="application/rss+xml" title="Actualidad jurídica · Cendán &amp; Amarelo" href="/actualidad-juridica/feed.xml">
  <link rel="alternate" type="text/plain" title="Información para asistentes de IA" href="/llms.txt">
  <link rel="stylesheet" href="/css/styles.min.css">
  <script>(function(d){{d.classList.add('js');{intro_js}}})(document.documentElement)</script>
  <script type="application/ld+json">
{ld}
  </script>
</head>
'''


def page(path, title, desc, main, active='', crumbs=None, extra_schema=None, home=False, intro=''):
    html = page_head(title, desc, path, crumbs, extra_schema, home)
    html += f'''<body>
{intro}  <a class="skip" href="#contenido">Saltar al contenido</a>
  <div class="progress" aria-hidden="true"></div>
  <span class="top-sentinel" aria-hidden="true"></span>
{header(active)}

  <main id="contenido">
{main}
  </main>

{footer()}
{whatsapp_float()}

  <script src="/js/main.min.js" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, 'index.html') if path == '/' else os.path.join(ROOT, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    SITEMAP.append(path)


# ---------------------------------------------------------------- Páginas

def home_news():
    items = NEWS['items'][:4]
    news_html = news_list(items, 'news-compact') if items else '<p class="lead">Cada dos días, los titulares jurídicos más relevantes de Galicia y España.</p>'
    return f'''    <section class="section section-paper" aria-labelledby="h-actualidad">
      <div class="wrap">
        <div class="section-head section-head-row">
          <h2 id="h-actualidad" class="reveal">Actualidad jurídica.</h2>
          <a class="link reveal" href="/actualidad-juridica/">Ver la actualidad {ARROW}</a>
        </div>
        <div class="home-news">
          {news_html}
          {guide_cards(GUIDES[:2])}
        </div>
      </div>
    </section>'''


def build_home():
    intro = f'''  <div class="intro" aria-hidden="true">
    <div class="intro-logo">{tiles_svg('intro-tiles', 'in')}
      <picture><source srcset="/assets/img/logo-texto.webp" type="image/webp"><img class="intro-word" src="/assets/img/logo-texto.png" width="298" height="52" alt=""></picture>
    </div>
  </div>
'''
    facts = [('1973', 'Año de fundación'), ('6', 'Áreas de práctica'), ('5', 'Abogados'), ('+40', 'Años de experiencia')]
    prefix = ' data-prefix="+"'
    facts_html = ''.join(
        f'<div class="reveal" style="--d:{n * 90}ms"><dt>{t}</dt><dd data-count="{v.lstrip("+")}"{prefix if v.startswith("+") else ""}>{v}</dd></div>'
        for n, (v, t) in enumerate(facts))
    main = f'''    <section class="hero" aria-labelledby="h1">
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <p class="eyebrow">Desde 1973</p>
          <h1 id="h1">Despacho de abogados <em>en Lugo</em><span class="dot" aria-hidden="true">.</span></h1>
          <p class="lead">Asesoramiento jurídico a empresas y particulares en toda Galicia, de forma personal e individualizada.</p>
          <div class="actions">{btn_primary()}{btn_call()}</div>
        </div>
        <figure class="hero-art">
          {picture('jesus-a-amarelo-fernandez', 'Jesús A. Amarelo Fernández, socio', 'hero-ph hero-ph-a', eager=True)}
          {picture('francisco-gonzalez-gonzalez', 'Francisco González González, socio', 'hero-ph hero-ph-b')}
          <div class="hero-mark">{tiles_svg('hero-tiles', 'h')}</div>
          <figcaption>Jesús A. Amarelo y Francisco González, socios del despacho</figcaption>
        </figure>
      </div>
    </section>

{quickbar()}

{marquee()}

    <section class="section section-paper" aria-labelledby="h-areas">
      <div class="wrap">
        <div class="section-head section-head-row">
          <div>
            <p class="eyebrow reveal">Áreas de práctica</p>
            <h2 id="h-areas" class="reveal">Seis especialidades, un mismo equipo.</h2>
          </div>
          <a class="link reveal" href="/areas-de-practica/">Ver todas las áreas {ARROW}</a>
        </div>
        {areas_bento()}
      </div>
    </section>

    <section class="section firma" aria-labelledby="h-firma">
      <div class="wrap">
        <h2 id="h-firma" class="statement reveal">Un equipo altamente cualificado, cuyo objetivo es la satisfacción de las necesidades de nuestros clientes.</h2>
        <dl class="facts">{facts_html}</dl>
        <div class="firma-grid">
          <div class="prose">
            <p class="reveal">La firma, fundada en 1973 por el letrado Antonio Cendán Corredoira, ha crecido respondiendo a las demandas de sus clientes, ampliando sus campos de actuación e incorporando abogados especializados en las distintas materias.</p>
            <a class="link reveal" href="/despacho-abogados-lugo/">Conocer la firma {ARROW}</a>
          </div>
          <ul class="values" role="list">
            <li class="reveal">Perseguimos la más alta calidad en el servicio</li>
            <li class="reveal" style="--d:90ms">Especialización y experiencia</li>
            <li class="reveal" style="--d:180ms">Sólido compromiso por la excelencia y la integridad</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section section-team" aria-labelledby="h-equipo">
      <div class="wrap">
        <div class="section-head section-head-row">
          <h2 id="h-equipo" class="reveal">Conozca a nuestros abogados.</h2>
          <a class="link reveal" href="/equipo-profesional/">Ver el equipo {ARROW}</a>
        </div>
        {team_grid()}
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-metodo">
      <div class="wrap">
        <h2 id="h-metodo" class="reveal">Cómo trabajamos.</h2>
        {method_list()}
      </div>
    </section>

{home_news()}

    <section class="section" aria-labelledby="h-faq">
      <div class="wrap faq-grid">
        <div>
          <h2 id="h-faq" class="reveal">Preguntas frecuentes.</h2>
          <a class="link reveal" href="/contacto/#h-faq">Ver todas las preguntas {ARROW}</a>
        </div>
        <div class="faq">{faq_list(FAQ[:4])}</div>
      </div>
    </section>

{contact_block()}'''
    faq_ld = {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': r}} for q, r in FAQ[:4]]}
    speak = {'@type': 'WebPage', 'url': DOMAIN + '/', 'name': 'Despacho de abogados en Lugo', 'inLanguage': 'es-ES',
             'about': {'@id': DOMAIN + '/#despacho'},
             'speakable': {'@type': 'SpeakableSpecification', 'cssSelector': ['#h1', '.hero .lead', '.quick-grid']}}
    page('/', 'Despacho de abogados en Lugo | Cendán & Amarelo Abogados',
         'Cendán & Amarelo, despacho de abogados en Lugo desde 1973. Derecho penal económico, mercantil, tributario, civil, administrativo y laboral para empresas y particulares de Galicia.',
         main, home=True, intro=intro, extra_schema=[faq_ld, speak])


def build_firma():
    crumbs = [('La firma', '/despacho-abogados-lugo/')]
    hist = ''.join(f'<li class="reveal" style="--d:{n * 100}ms"><span class="tl-year">{y}</span><h3>{t}</h3><p>{d}</p></li>'
                   for n, (y, t, d) in enumerate(HISTORY))
    main = f'''{page_hero('La firma', 'Despacho de abogados en Lugo', 'Una trayectoria de más de treinta y cinco años al servicio de empresas y particulares.', crumbs)}

    <section class="section" aria-label="Presentación">
      <div class="wrap narrow">
        <p class="statement reveal">Cendán &amp; Amarelo es un despacho de abogados con una trayectoria de más de treinta y cinco años que cuenta con un equipo altamente cualificado, cuyo objetivo es la satisfacción de las necesidades de nuestros clientes.</p>
        <div class="prose two-col">
          <p class="reveal">La firma, fundada en 1973 por el letrado Antonio Cendán Corredoira, ha crecido desde entonces respondiendo a las demandas de nuestros clientes, ampliando sus campos de actuación e incorporando abogados especializados en las distintas materias.</p>
          <p class="reveal">Por su experiencia y profesionalidad, Cendán &amp; Amarelo cuenta con el respaldo y fidelidad de un gran número de clientes, prestando asesoramiento a empresas y particulares, a quienes asesora en todas las áreas, de forma personal e individualizada, entre las que se encuentran importantes empresas tanto a nivel regional como a nivel nacional.</p>
          <p class="reveal">Para responder adecuadamente a las necesidades de los clientes, otorgamos una especial atención a la formación continuada de nuestros profesionales. El trabajo en equipo y la gestión del conocimiento son herramientas fundamentales para el desarrollo de nuestros servicios.</p>
        </div>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-historia">
      <div class="wrap">
        <h2 id="h-historia" class="reveal">Trayectoria.</h2>
        <ol class="timeline" role="list">{hist}</ol>
      </div>
    </section>

    <section class="section" aria-labelledby="h-valores">
      <div class="wrap firma-grid">
        <h2 id="h-valores" class="reveal">Lo que nos define.</h2>
        <ul class="values values-lg" role="list">
          <li class="reveal">Perseguimos la más alta calidad en el servicio</li>
          <li class="reveal" style="--d:90ms">Especialización y experiencia</li>
          <li class="reveal" style="--d:180ms">Sólido compromiso por la excelencia y la integridad</li>
        </ul>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-metodo">
      <div class="wrap">
        <h2 id="h-metodo" class="reveal">Cómo trabajamos.</h2>
        {method_list()}
        <p class="note reveal">Un compromiso sin fisuras con nuestros clientes, sin más límites que los que impone la ética profesional.</p>
      </div>
    </section>

{contact_block(eyebrow=False)}'''
    page('/despacho-abogados-lugo/', 'La firma · Despacho de abogados en Lugo desde 1973 | Cendán & Amarelo',
         'Cendán & Amarelo, despacho de abogados en Lugo fundado en 1973 por Antonio Cendán Corredoira. Calidad, especialización e integridad al servicio de empresas y particulares.',
         main, '/despacho-abogados-lugo/', crumbs)


def build_areas_index():
    crumbs = [('Áreas de práctica', '/areas-de-practica/')]
    main = f'''{page_hero('Especialidades', 'Áreas de práctica', 'Desarrollamos nuestra actuación, tanto en el ámbito empresarial como en el ámbito personal, desde hace más de cuatro décadas.', crumbs)}

    <section class="section">
      <div class="wrap">
        {areas_bento('h2')}
        <p class="note reveal">Los departamentos trabajan de forma coordinada: cada asunto se estudia desde todas las áreas que le afectan.</p>
      </div>
    </section>

{contact_block(eyebrow=False)}'''
    page('/areas-de-practica/', 'Áreas de práctica · Abogados en Lugo | Cendán & Amarelo',
         'Derecho penal, mercantil y concursal, tributario, civil y procesal, administrativo y laboral. Abogados especialistas en Lugo con servicio en toda Galicia.',
         main, '/areas-de-practica/', crumbs)


def area_related(a):
    news = [i for i in NEWS['items'] if i.get('area') == a['id']][:4]
    guides = [g for g in GUIDES if g['area'] == a['id']]
    if not news and not guides:
        return ''
    news_html = news_list(news) if news else ''
    guide_html = guide_cards(guides) if guides else ''
    return f'''    <section class="section" aria-labelledby="h-act">
      <div class="wrap">
        <div class="section-head section-head-row">
          <h2 id="h-act" class="reveal">Actualidad de {a['name']}.</h2>
          <a class="link reveal" href="/actualidad-juridica/">Toda la actualidad {ARROW}</a>
        </div>
        {guide_html}
        {news_html}
      </div>
    </section>'''


def build_area(a):
    crumbs = [('Áreas de práctica', '/areas-de-practica/'), (a['name'], f'/{a["slug"]}/')]
    lead_p, *rest = a['intro']
    rest_html = ''.join(f'<p class="reveal">{p}</p>' for p in rest)
    services = ''.join(f'<li class="reveal" style="--d:{(n % 2) * 60}ms">{ico("ph_check")}<span>{s}</span></li>' for n, s in enumerate(a['services']))
    others = ''.join(f'<li><a href="/{o["slug"]}/">{o["name"]} {ARROW}</a></li>' for o in AREAS if o is not a)
    main = f'''{page_hero('Áreas de práctica', a['name'], a['short'], crumbs)}

    <section class="section">
      <div class="wrap with-aside">
        <div class="main-col">
          <p class="statement reveal">{lead_p}</p>
          <div class="prose">{rest_html}</div>
          <h2 class="h-sub reveal">Qué hacemos</h2>
          <ul class="services" role="list">{services}</ul>
          <p class="note reveal">{a['note']}</p>
        </div>
        {aside_contact()}
      </div>
    </section>

{area_related(a)}
{contact_block('¿Necesita alguna consulta legal?', eyebrow=False)}

    <section class="section-tight" aria-labelledby="h-otras">
      <div class="wrap">
        <h2 id="h-otras" class="other-title">Otras áreas de práctica</h2>
        <ul class="other-areas" role="list">{others}</ul>
      </div>
    </section>'''
    service = {'@type': 'Service', 'name': a['name'], 'serviceType': a['name'], 'url': f'{DOMAIN}/{a["slug"]}/',
               'provider': {'@id': DOMAIN + '/#despacho'}, 'areaServed': ['Lugo', 'Galicia'], 'description': a['short']}
    page(f'/{a["slug"]}/', f'Abogados de {a["name"]} en Lugo | Cendán & Amarelo',
         f'Abogados especialistas en {a["name"]} en Lugo y Galicia. {a["short"]} Primera valoración sin compromiso.',
         main, '/areas-de-practica/', crumbs, [service])


def build_equipo():
    crumbs = [('Equipo profesional', '/equipo-profesional/')]
    main = f'''{page_hero('Equipo profesional', 'Conozca a nuestros expertos', 'Experimentados profesionales que han ido engrosando nuestro número de socios a medida que asumían responsabilidades y acreditaban sus méritos.', crumbs)}

    <section class="section section-team">
      <div class="wrap">
        {team_grid()}
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-formacion">
      <div class="wrap narrow">
        <h2 id="h-formacion" class="reveal">Formación y experiencia.</h2>
        <div class="prose two-col">
          <p class="reveal">La formación, parte que consideramos fundamental para el ejercicio de esta profesión, ha sido la base sobre la que se han configurado las carreras de nuestros profesionales, completando una formación académica y, en determinados casos, de postgrado en algunas de las más prestigiosas escuelas de negocios y Universidades de los Estados Unidos de América y de Europa.</p>
          <p class="reveal">Nuestro equipo de trabajo, basado en la interrelación departamental y la suma de esfuerzos en el trabajo en equipo, se compone por abogados altamente cualificados para atender a las demandas de las empresas e individuos que requieren de un completo asesoramiento legal.</p>
        </div>
        <p class="note reveal">La experiencia adquirida a lo largo de los años nos ha permitido desarrollar un compromiso sin fisuras con nuestros clientes, sin más límites que los que impone la ética profesional.</p>
      </div>
    </section>

{contact_block('¿Quiere unirse?', f'Si desea formar parte de nuestro equipo, envíenos su currículum a {EMAIL}.', eyebrow=False)}'''
    page('/equipo-profesional/', 'Equipo profesional · Abogados en Lugo | Cendán & Amarelo',
         'Conozca al equipo de abogados de Cendán & Amarelo en Lugo: Jesús A. Amarelo, Francisco González, Ana Belén Rey, Manuel Lugilde y David Couselo.',
         main, '/equipo-profesional/', crumbs)


def build_actualidad():
    crumbs = [('Actualidad jurídica', '/actualidad-juridica/')]
    items = NEWS['items']
    upd = f'Actualizado el {fecha(NEWS["updated"])}. ' if NEWS.get('updated') else ''
    galicia = [i for i in items if i.get('scope') == 'galicia'][:8]
    chips = '<button type="button" class="chip" aria-pressed="true" data-filter="all">Todas</button>' + \
        '<button type="button" class="chip" aria-pressed="false" data-filter="galicia">Galicia</button>' + \
        ''.join(f'<button type="button" class="chip" aria-pressed="false" data-filter="{a["id"]}">{AREA_LABEL[a["id"]]}</button>' for a in AREAS)
    if items:
        news_html = f'''
        <div class="chips" role="group" aria-label="Filtrar noticias">{chips}</div>
        {news_list(items, 'news-filterable')}
        <p class="news-empty" hidden>No hay noticias recientes en esta categoría.</p>'''
    else:
        news_html = '''<div class="empty"><p class="statement">Las noticias se están actualizando.</p><p>Cada dos días recopilamos los titulares jurídicos más relevantes de España y de Galicia. Vuelva en unas horas.</p></div>'''
    gal_html = f'''
    <section class="section section-paper" aria-labelledby="h-galicia">
      <div class="wrap">
        <div class="section-head section-head-row">
          <h2 id="h-galicia" class="reveal">En Galicia.</h2>
          <a class="link reveal" href="/abogados-galicia/">Nuestro ámbito de actuación {ARROW}</a>
        </div>
        {news_list(galicia)}
      </div>
    </section>''' if galicia else ''
    main = f'''{page_hero('Noticias', 'Actualidad jurídica en Galicia y España', f'Los titulares jurídicos más relevantes, seleccionados cada dos días. {upd}Cada noticia enlaza a su fuente original.', crumbs, ctas=False)}

    <section class="section" aria-labelledby="h-ultimas">
      <div class="wrap">
        <h2 id="h-ultimas" class="reveal">Últimas noticias.</h2>
        {news_html}
      </div>
    </section>
{gal_html}

    <section class="section" aria-labelledby="h-guias">
      <div class="wrap">
        <div class="section-head section-head-row">
          <h2 id="h-guias" class="reveal">Guías del despacho.</h2>
          <a class="link reveal" href="/guias-juridicas/">Ver todas las guías {ARROW}</a>
        </div>
        {guide_cards(GUIDES)}
      </div>
    </section>

{contact_block('¿Le afecta alguna novedad?', 'Contacte con nosotros y le explicaremos cómo puede afectarle. Primera valoración sin compromiso.', eyebrow=False)}'''
    schema = [{'@type': 'CollectionPage', 'name': 'Actualidad jurídica en Galicia y España', 'url': f'{DOMAIN}/actualidad-juridica/',
               'dateModified': NEWS.get('updated') or UPDATED, 'inLanguage': 'es-ES', 'publisher': {'@id': DOMAIN + '/#despacho'},
               'mainEntity': {'@type': 'ItemList', 'itemListElement': [
                   {'@type': 'ListItem', 'position': n, 'url': it['url'], 'name': it['title']} for n, it in enumerate(items[:20], 1)]}}]
    page('/actualidad-juridica/', 'Actualidad jurídica en Galicia y España | Cendán & Amarelo Abogados',
         'Noticias jurídicas de Galicia y España actualizadas cada dos días: penal, mercantil, tributario, civil, administrativo y laboral. Cendán & Amarelo Abogados, Lugo.',
         main, '/actualidad-juridica/', crumbs, schema)
    build_feed(items)


def build_feed(items):
    """RSS propio con los titulares seleccionados (enlazan a la fuente original)."""
    def rfc(iso):
        from email.utils import format_datetime
        from datetime import datetime
        return format_datetime(datetime.strptime(iso, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=__import__('datetime').timezone.utc))
    entries = ''.join(
        f'<item><title>{html_escape(i["title"])}</title><link>{html_escape(i["url"])}</link><guid isPermaLink="false">{html_escape(i["url"])}</guid>'
        f'<pubDate>{rfc(i["date"])}</pubDate><category>{AREA_LABEL.get(i["area"], "General")}</category><source url="{DOMAIN}/actualidad-juridica/feed.xml">{html_escape(i["source"])}</source></item>'
        for i in items[:30])
    xml = (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Actualidad jurídica · Cendán &amp; Amarelo Abogados</title>'
           f'<link>{DOMAIN}/actualidad-juridica/</link><description>Titulares jurídicos de Galicia y España seleccionados por Cendán &amp; Amarelo Abogados (Lugo).</description>'
           f'<language>es-ES</language>{entries}</channel></rss>\n')
    os.makedirs(os.path.join(ROOT, 'actualidad-juridica'), exist_ok=True)
    with open(os.path.join(ROOT, 'actualidad-juridica', 'feed.xml'), 'w', encoding='utf-8') as f:
        f.write(xml)


def build_guides():
    crumbs = [('Guías jurídicas', '/guias-juridicas/')]
    main = f'''{page_hero('Guías', 'Guías jurídicas', 'Respuestas claras a las dudas legales más habituales, redactadas por el despacho.', crumbs)}

    <section class="section">
      <div class="wrap">
        {guide_cards(GUIDES, 'h2')}
      </div>
    </section>

{contact_block(eyebrow=False)}'''
    page('/guias-juridicas/', 'Guías jurídicas | Cendán & Amarelo Abogados, Lugo',
         'Guías jurídicas del despacho Cendán & Amarelo: despidos, herencias en Galicia, inspecciones de Hacienda y más.',
         main, '/actualidad-juridica/', crumbs)
    for g in GUIDES:
        area = AREA_BY_ID[g['area']]
        crumbs_g = crumbs + [(g['title'], f'/guias-juridicas/{g["slug"]}/')]
        toc = ''.join(f'<li><a href="#s{n}">{t}</a></li>' for n, (t, _) in enumerate(g['sections'], 1))
        summary = ''.join(f'<li>{ico("ph_check")}<span>{x}</span></li>' for x in g['summary'])
        body = ''.join(f'<h2 id="s{n}" class="reveal">{t}</h2>' + ''.join(f'<p class="reveal">{p}</p>' for p in ps)
                       for n, (t, ps) in enumerate(g['sections'], 1))
        related = [x for x in GUIDES if x is not g]
        main_g = f'''{page_hero(AREA_LABEL[g['area']], g['title'], g['desc'], crumbs_g, ctas=False)}

    <section class="section">
      <div class="wrap with-aside">
        <article class="main-col article">
          <p class="article-meta">Cendán &amp; Amarelo Abogados · <time datetime="{g['date']}">{fecha(g['date'])}</time></p>
          <div class="summary-box reveal">
            <p class="summary-title">En resumen</p>
            <ul role="list">{summary}</ul>
          </div>
          <nav class="toc" aria-label="Contenido de la guía"><p>Contenido</p><ol>{toc}</ol></nav>
          <div class="prose">{body}</div>
          <p class="note reveal">Esta guía ofrece información general y no sustituye al asesoramiento profesional. Cada caso requiere un estudio individual.</p>
          <a class="link reveal" href="/{area['slug']}/">Más sobre {area['name']} {ARROW}</a>
        </article>
        {aside_contact()}
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-mas">
      <div class="wrap">
        <h2 id="h-mas" class="reveal">Otras guías.</h2>
        {guide_cards(related)}
      </div>
    </section>'''
        art = {'@type': 'Article', 'headline': g['title'], 'description': g['desc'], 'datePublished': g['date'], 'dateModified': g['date'],
               'inLanguage': 'es-ES', 'author': {'@id': DOMAIN + '/#despacho'}, 'publisher': {'@id': DOMAIN + '/#despacho'},
               'mainEntityOfPage': f'{DOMAIN}/guias-juridicas/{g["slug"]}/', 'image': DOMAIN + '/assets/img/og-cendan-amarelo.jpg',
               'about': area['name'], 'spatialCoverage': 'Galicia, España'}
        page(f'/guias-juridicas/{g["slug"]}/', f'{g["title"]} | Cendán & Amarelo Abogados', g['desc'], main_g, '/actualidad-juridica/', crumbs_g, [art])


def build_galicia():
    crumbs = [('Galicia y España', '/abogados-galicia/')]
    prov = ''.join(f'<li class="reveal" style="--d:{n * 80}ms"><h3>{p}</h3><p>{t}</p></li>' for n, (p, t) in enumerate(PROVINCES))
    main = f'''{page_hero('Ámbito de actuación', 'Abogados en Galicia y en toda España', 'Desde Lugo, asesoramos y defendemos a empresas y particulares en las cuatro provincias gallegas y ante los tribunales de toda España.', crumbs)}

    <section class="section">
      <div class="wrap narrow">
        <p class="statement reveal">Un despacho gallego, con más de cuarenta años de ejercicio, que acompaña a sus clientes allí donde esté su asunto.</p>
        <div class="prose two-col">
          <p class="reveal">Nuestra sede está en Lugo, en la Avenida de A Coruña. Desde ella atendemos a clientes de toda Galicia, a los que asesoramos de forma presencial, por teléfono o por correo, y representamos ante juzgados, audiencias provinciales y el Tribunal Superior de Xustiza de Galicia.</p>
          <p class="reveal">Muchos de nuestros clientes son empresas con actividad en toda España. Por eso intervenimos también ante órganos de ámbito nacional, como la Audiencia Nacional, el Tribunal Supremo y las administraciones del Estado, coordinando cada asunto desde Lugo.</p>
        </div>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-provincias">
      <div class="wrap">
        <h2 id="h-provincias" class="reveal">Las cuatro provincias gallegas.</h2>
        <ul class="provinces" role="list">{prov}</ul>
      </div>
    </section>

    <section class="section" aria-labelledby="h-espana">
      <div class="wrap firma-grid">
        <h2 id="h-espana" class="reveal">También en el resto de España.</h2>
        <ul class="values" role="list">
          <li class="reveal">Audiencia Nacional y Tribunal Supremo</li>
          <li class="reveal" style="--d:90ms">Administración General del Estado y Agencia Tributaria</li>
          <li class="reveal" style="--d:180ms">Empresas con actividad en varias comunidades</li>
        </ul>
      </div>
    </section>

{contact_block()}'''
    schema = [{'@type': 'Service', 'name': 'Asesoramiento jurídico en Galicia y España', 'provider': {'@id': DOMAIN + '/#despacho'},
               'areaServed': [{'@type': 'AdministrativeArea', 'name': p} for p, _ in PROVINCES] + [{'@type': 'Country', 'name': 'España'}]}]
    page('/abogados-galicia/', 'Abogados en Galicia y España: Lugo, A Coruña, Ourense y Pontevedra | Cendán & Amarelo',
         'Despacho de abogados con sede en Lugo que actúa en toda Galicia (Lugo, A Coruña, Ourense, Pontevedra) y ante los tribunales de toda España.',
         main, '', crumbs, schema)


def build_contacto():
    crumbs = [('Contacto', '/contacto/')]
    options = ''.join(f'<option>{a["name"]}</option>' for a in AREAS)
    main = f'''{page_hero('Contacto', 'Hablemos de su caso', 'Consúltenos sin compromiso y le daremos una primera valoración.', crumbs, ctas=False)}

    <section class="section">
      <div class="wrap contact">
        <div>
          <div class="contact-quick">
            <a class="btn btn-dark btn-block" href="tel:{PHONE_TEL}">{ico('phone')}<span>Llamar&nbsp;al&nbsp;{PHONE_HTML}</span></a>
            {btn_whatsapp('btn-block')}
          </div>
          <dl class="data-list">
            <div class="reveal"><dt>{ico('envelope_simple')}Correo</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
            <div class="reveal"><dt>{ico('map_pin')}Oficina</dt><dd>Avda. de A Coruña 10-14, Entlo.<br>27003 Lugo<br><a class="link" href="{MAPS}" rel="noopener" target="_blank">Cómo llegar {ARROW}</a></dd></div>
            <div class="reveal"><dt>{ico('clock')}Horario</dt><dd>Lunes a jueves, de 9:00 a 14:30 y de 16:00 a 19:30<br>Viernes, de 9:00 a 15:00</dd></div>
          </dl>
        </div>

        <form class="form reveal" id="form" novalidate>
          <h2>Formulario de contacto</h2>
          <p class="help">Le responderemos en el menor plazo posible. Los campos con * son obligatorios.</p>
          <div class="field"><label for="f-name">Nombre y apellidos *</label><input id="f-name" name="nombre" type="text" autocomplete="name" required><p class="err" id="f-name-err">Indique su nombre.</p></div>
          <div class="field-row">
            <div class="field"><label for="f-mail">Email *</label><input id="f-mail" name="email" type="email" autocomplete="email" inputmode="email" required><p class="err">Indique un email válido.</p></div>
            <div class="field"><label for="f-tel">Teléfono</label><input id="f-tel" name="telefono" type="tel" autocomplete="tel" inputmode="tel"></div>
          </div>
          <div class="field"><label for="f-area">Área</label><select id="f-area" name="area"><option value="">Seleccione (opcional)</option>{options}</select></div>
          <div class="field"><label for="f-msg">Mensaje *</label><textarea id="f-msg" name="mensaje" rows="5" required aria-describedby="f-msg-help"></textarea><p class="help" id="f-msg-help">Describa brevemente su asunto. No incluya información confidencial.</p><p class="err">Escriba su consulta.</p></div>
          <label class="check"><input type="checkbox" name="privacidad" required><span>He leído y acepto el <a href="/aviso-legal/">Aviso legal y la política de privacidad</a>. *</span></label>
          <label class="check"><input type="checkbox" name="comunicaciones"><span>Acepto recibir comunicaciones del despacho (opcional).</span></label>
          <button class="btn btn-dark" type="submit"><span>Enviar consulta</span><i>{ARROW}</i></button>
          <p class="form-status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-faq">
      <div class="wrap faq-grid">
        <h2 id="h-faq" class="reveal">Preguntas frecuentes.</h2>
        <div class="faq">{faq_list(FAQ)}</div>
      </div>
    </section>'''
    faq_ld = {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': r}} for q, r in FAQ]}
    page('/contacto/', 'Contacto · Abogados en Lugo | Cendán & Amarelo',
         'Contacte con Cendán & Amarelo Abogados: Avda. de A Coruña 10-14, Lugo. Teléfono y WhatsApp 982 223 053. Primera valoración sin compromiso.',
         main, '/contacto/', crumbs, [ORG, faq_ld])


def build_legal():
    for slug, (title, desc, body) in LEGAL.items():
        crumbs = [(title, f'/{slug}/')]
        main = f'''{page_hero('Información legal', title, '', crumbs, ctas=False)}

    <section class="section legal">
      <div class="wrap">
        <article class="prose">
{body.rstrip()}
        </article>
      </div>
    </section>'''
        page(f'/{slug}/', f'{title} | Cendán & Amarelo Abogados', desc, main, '', crumbs)


def build_404():
    html = page_head('Página no encontrada | Cendán & Amarelo Abogados', 'La página solicitada no existe.', '/404.html', robots='noindex')
    html += f'''<body>
{header('')}
  <main id="contenido">
    <section class="page-hero page-404">
      <div class="wrap page-hero-grid">
        <div>
          <p class="eyebrow">Error 404</p>
          <h1>Esta página no existe</h1>
          <p class="lead">Es posible que la dirección haya cambiado con la nueva web del despacho.</p>
          <div class="actions"><a class="btn btn-dark" href="/"><span>Volver al inicio</span><i>{ARROW}</i></a>{btn_call()}</div>
        </div>
        {tiles_svg('page-tiles', 'ph')}
      </div>
    </section>
  </main>
{whatsapp_float()}
  <script src="/js/main.min.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def build_isotipo():
    polys = ''.join(f'<polygon points="{x},{y - r} {x + r},{y} {x},{y + r} {x - r},{y}"/>' for x, y, r in TILES)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 116 68"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="68" gradientUnits="userSpaceOnUse">'
           '<stop offset="0" stop-color="#f8dac4"/><stop offset=".5" stop-color="#f0a479"/><stop offset="1" stop-color="#e8702a"/></linearGradient>'
           f'<clipPath id="c"><rect width="116" height="67.6"/></clipPath></defs><g fill="url(#g)" clip-path="url(#c)">{polys}</g></svg>')
    with open(os.path.join(ROOT, 'assets', 'img', 'isotipo.svg'), 'w', encoding='utf-8') as f:
        f.write(svg)


def build_sitemap():
    def prio(p):
        return '1.0' if p == '/' else '0.3' if p.strip('/') in LEGAL else '0.8'
    urls = ''.join(f'  <url><loc>{DOMAIN}{p}</loc><lastmod>{UPDATED}</lastmod><priority>{prio(p)}</priority></url>\n' for p in SITEMAP)
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')


def build_llms():
    areas = '\n'.join(f'- [{a["name"]}]({DOMAIN}/{a["slug"]}/): {a["short"]}' for a in AREAS)
    team = '\n'.join(f'- {n}, {r}' for _, n, r in TEAM)
    hist = '\n'.join(f'- {y}: {d}'.replace('&amp;', '&') for y, _, d in HISTORY)
    txt = f'''# Cendán & Amarelo Abogados

> Despacho de abogados en Lugo (Galicia, España), fundado en 1973 por el letrado Antonio Cendán Corredoira. Asesora a empresas y particulares de Lugo y de toda Galicia, de forma personal e individualizada.

- Razón social: Cendán & Amarelo Abogados, S.L.P. (NIF B27365667)
- Registro Mercantil de Lugo: Tomo 385, Libro 0, Folio 42, Hoja LU-12246
- Dirección: Avenida de A Coruña, 10-14, Entresuelo, 27003 Lugo
- Teléfono: +34 982 223 053. Fax: +34 982 223 947
- WhatsApp: https://wa.me/{WHATSAPP}
- Email: {EMAIL}
- Horario: lunes a jueves de 9:00 a 14:30 y de 16:00 a 19:30; viernes de 9:00 a 15:00
- Redes: https://twitter.com/cendanamarelo, https://es-es.facebook.com/pages/Cendan-Amarelo-Abogados/226246534135877

## Áreas de práctica
{areas}

## Equipo
{team}

## Trayectoria
{hist}

## Páginas
- [Inicio]({DOMAIN}/)
- [La firma]({DOMAIN}/despacho-abogados-lugo/)
- [Equipo profesional]({DOMAIN}/equipo-profesional/)
- [Contacto y preguntas frecuentes]({DOMAIN}/contacto/)
- [Galicia y España]({DOMAIN}/abogados-galicia/)
- [Actualidad jurídica]({DOMAIN}/actualidad-juridica/) (RSS: {DOMAIN}/actualidad-juridica/feed.xml)
- [Guías jurídicas]({DOMAIN}/guias-juridicas/)

## Para agentes
- Información completa: {DOMAIN}/llms-full.txt
- Datos estructurados: {DOMAIN}/despacho.json
- [Aviso legal]({DOMAIN}/aviso-legal/)
'''
    with open(os.path.join(ROOT, 'llms.txt'), 'w', encoding='utf-8') as f:
        f.write(txt)


def build_agent_files():
    """Navegación agéntica: versión completa en texto y datos estructurados del despacho."""
    lines = ['# Cendán & Amarelo Abogados: información completa', '',
             'Despacho de abogados en Lugo (Galicia, España), fundado en 1973 por Antonio Cendán Corredoira.',
             f'Teléfono y WhatsApp: +34 982 223 053. Email: {EMAIL}. Dirección: Avenida de A Coruña, 10-14, Entresuelo, 27003 Lugo.',
             'Horario: lunes a jueves de 9:00 a 14:30 y de 16:00 a 19:30; viernes de 9:00 a 15:00.',
             'Primera valoración sin compromiso. Formulario: ' + DOMAIN + '/contacto/', '']
    for a in AREAS:
        lines += [f'## {a["name"]} ({DOMAIN}/{a["slug"]}/)', a['short']]
        lines += [p.replace('&amp;', '&') for p in a['intro']]
        lines += ['Servicios:'] + [f'- {re_tags(x)}' for x in a['services']] + [a['note'], '']
    lines += ['## Equipo'] + [f'- {n}, {r}' for _, n, r in TEAM] + ['']
    lines += ['## Trayectoria'] + [f'- {y}: {d}'.replace('&amp;', '&') for y, _, d in HISTORY] + ['']
    lines += ['## Ámbito'] + [f'- {p}: {t}' for p, t in PROVINCES] + ['- Resto de España: Audiencia Nacional, Tribunal Supremo y administraciones del Estado.', '']
    lines += ['## Preguntas frecuentes'] + [f'P: {q}\nR: {r}' for q, r in FAQ] + ['']
    for g in GUIDES:
        lines += [f'## Guía: {g["title"]} ({DOMAIN}/guias-juridicas/{g["slug"]}/)', g['desc']]
        for t, ps in g['sections']:
            lines += [f'### {t}'] + ps
        lines += ['']
    with open(os.path.join(ROOT, 'llms-full.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    data = {k: v for k, v in ORG.items() if k != 'hasOfferCatalog'}
    data['@context'] = 'https://schema.org'
    data['areas'] = [{'nombre': a['name'], 'url': f'{DOMAIN}/{a["slug"]}/', 'resumen': a['short'], 'servicios': [re_tags(x) for x in a['services']]} for a in AREAS]
    data['whatsapp'] = f'https://wa.me/{WHATSAPP}'
    data['contacto'] = DOMAIN + '/contacto/'
    with open(os.path.join(ROOT, 'despacho.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def re_tags(t):
    import re
    return re.sub(r'<[^>]+>', '', t).replace('&amp;', '&')


if __name__ == '__main__':
    build_home()
    build_firma()
    build_areas_index()
    for area in AREAS:
        build_area(area)
    build_equipo()
    build_actualidad()
    build_guides()
    build_galicia()
    build_contacto()
    build_legal()
    build_404()
    build_isotipo()
    build_sitemap()
    build_llms()
    build_agent_files()
    print(f'{len(SITEMAP)} páginas + 404 generadas')
