"""Generador del sitio estático de Cendán & Amarelo Abogados.

Uso:  python3 scripts/build.py   (o sh scripts/build.sh, que además minifica)
Escribe todas las páginas HTML, sitemap.xml y llms.txt en la raíz del repositorio.
Las rutas son absolutas (/css/..., /contacto/) y conservan las URL de la web anterior.

Contenido editable: scripts/content.py (áreas, equipo, FAQ...) y scripts/legal_content.py.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from content import AREAS, FAQ, HISTORY, METHOD, NAV, TEAM  # noqa: E402
from icons import ICONS  # noqa: E402
from legal_content import PAGES as LEGAL  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOMAIN = 'https://www.cendanamareloabogados.com'
UPDATED = '2026-10-16'
PHONE_HTML = '982&nbsp;223&nbsp;053'
EMAIL = 'despacho@cendanamareloabogados.com'
MAPS = 'https://www.google.com/maps/search/?api=1&amp;query=Avenida+de+A+Coru%C3%B1a+10-14+27003+Lugo'
CTA_LABEL = 'Solicitar consulta'   # una sola etiqueta para la intención "contactar"
SITEMAP = []


# ---------------------------------------------------------------- Piezas comunes

def ico(name, cls='ico'):
    box, inner = ICONS[name]
    return f'<svg class="{cls}" viewBox="{box}" aria-hidden="true" focusable="false">{inner}</svg>'


ARROW = ico('arrow_up_right')

# Teselas del isotipo (centro x, centro y, semidiagonal) en el espacio 116x68 del logotipo.
TILES = [(15.5, 63.5, 12.5), (36, 40, 17), (18, 24.5, 11.5), (56.5, 56.5, 19.5), (58, 16, 14),
         (77.5, 33, 16.5), (81.5, 66.5, 9.5), (97.5, 49.5, 14.5), (96.5, 13, 9)]


def tiles_svg(cls, uid):
    """Isotipo de Cendán & Amarelo reconstruido en SVG; cada tesela se anima por separado."""
    polys = ''.join(
        f'<polygon style="--i:{i};--z:{round(0.4 + (i % 4) * 0.35, 2)}" points="{x},{y - r} {x + r},{y} {x},{y + r} {x - r},{y}"/>'
        for i, (x, y, r) in enumerate(TILES))
    return (f'<svg class="{cls}" viewBox="0 0 116 68" aria-hidden="true" focusable="false">'
            f'<defs><linearGradient id="g{uid}" x1="0" y1="0" x2="0" y2="68" gradientUnits="userSpaceOnUse">'
            '<stop offset="0" stop-color="#f8dac4"/><stop offset=".5" stop-color="#f0a479"/><stop offset="1" stop-color="#e8702a"/>'
            f'</linearGradient><clipPath id="c{uid}"><rect width="116" height="67.6"/></clipPath></defs>'
            f'<g fill="url(#g{uid})" clip-path="url(#c{uid})">{polys}</g></svg>')


def picture(slug, alt, cls='', eager=False, w=375, h=450):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture class="{cls}"><source srcset="/assets/img/equipo/{slug}.webp" type="image/webp">'
            f'<img src="/assets/img/equipo/{slug}.jpg" width="{w}" height="{h}" {load} decoding="async" alt="{alt}"></picture>')


def logo(cls='brand'):
    return (f'<a class="{cls}" href="/" aria-label="Cendán &amp; Amarelo Abogados, inicio">'
            '<picture><source srcset="/assets/img/logo.webp" type="image/webp">'
            '<img src="/assets/img/logo.png" width="298" height="123" alt=""></picture></a>')


def header(active):
    cur = ' aria-current="page"'
    items = ''.join(f'<li><a href="{h}"{cur if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f'''  <header class="site-header">
    <div class="wrap header-bar">
      {logo()}
      <nav class="nav" id="nav" aria-label="Principal">
        <ul>{items}</ul>
        <a class="nav-phone" href="tel:+34982223053">{ico('phone')}<span>{PHONE_HTML}</span></a>
        <a class="btn btn-dark btn-sm" href="/contacto/"{cur if active == '/contacto/' else ''}><span>{CTA_LABEL}</span></a>
      </nav>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Abrir menú"><span></span><span></span></button>
    </div>
  </header>'''


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
          <li><a href="tel:+34982223053">{PHONE_HTML}</a></li>
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


def contact_block(title='¿Necesita asesoramiento?',
                  text='Contacte con nosotros sin compromiso y le daremos una primera valoración.', eyebrow=True):
    """Bloque de contacto con toda la información práctica (mismo tema claro que el resto)."""
    eb = '<p class="eyebrow reveal">Contacto</p>' if eyebrow else ''
    return f'''    <section class="contact-band" aria-labelledby="cb-title">
      {tiles_svg('band-tiles', 'cb')}
      <div class="wrap band-grid">
        <div class="band-copy">
          {eb}
          <h2 id="cb-title" class="reveal">{title}</h2>
          <p class="reveal">{text}</p>
          <a class="btn btn-dark reveal" href="/contacto/"><span>{CTA_LABEL}</span><i>{ARROW}</i></a>
        </div>
        <dl class="band-data">
          <div class="reveal"><dt>{ico('phone')}Teléfono</dt><dd><a href="tel:+34982223053">{PHONE_HTML}</a></dd></div>
          <div class="reveal" style="--d:80ms"><dt>{ico('envelope_simple')}Correo</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          <div class="reveal" style="--d:160ms"><dt>{ico('map_pin')}Oficina</dt><dd>Avda. de A Coruña 10-14, Entlo.<br>27003 Lugo · <a class="u" href="{MAPS}" rel="noopener" target="_blank">Cómo llegar</a></dd></div>
          <div class="reveal" style="--d:240ms"><dt>{ico('clock')}Horario</dt><dd>Lunes a jueves, de 9:00 a 14:30 y de 16:00 a 19:30<br>Viernes, de 9:00 a 15:00</dd></div>
        </dl>
      </div>
    </section>'''


def areas_bento(heading_level='h3'):
    """Bento asimétrico: exactamente una celda por área (6)."""
    cells = ''
    for i, a in enumerate(AREAS):
        cells += f'''
          <li class="bento-cell cell-{a["id"]} reveal" style="--d:{i * 70}ms">
            <a href="/{a["slug"]}/">
              <{heading_level}>{a["name"]}</{heading_level}>
              <p>{a["short"]}</p>
              <span class="cell-go">Ver área {ARROW}</span>
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
    items = ''.join(
        f'<li class="reveal" style="--d:{n * 100}ms"><h3>{t}</h3><p>{d}</p></li>' for n, (t, d) in enumerate(METHOD))
    return f'<ol class="method" role="list">{items}</ol>'


def page_hero(eyebrow, h1, lead, crumbs):
    trail = '<li><a href="/">Inicio</a></li>' + ''.join(
        f'<li><a href="{u}">{n}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{n}</li>'
        for i, (n, u) in enumerate(crumbs))
    return f'''    <section class="page-hero">
      <div class="wrap">
        <nav class="crumbs" aria-label="Migas de pan"><ol>{trail}</ol></nav>
        <p class="eyebrow">{eyebrow}</p>
        <h1>{h1}</h1>
        {f'<p class="lead">{lead}</p>' if lead else ''}
      </div>
      {tiles_svg('page-tiles', 'ph')}
    </section>'''


# ---------------------------------------------------------------- Plantilla de página

ORG = {
    '@type': ['LegalService', 'LocalBusiness'], '@id': DOMAIN + '/#despacho',
    'name': 'Cendán & Amarelo Abogados', 'legalName': 'Cendán & Amarelo Abogados, S.L.P.',
    'alternateName': ['Cendán y Amarelo Abogados', 'Cendán & Amarelo, Abogados y Asesores Tributarios'],
    'taxID': 'B27365667',
    'description': 'Despacho de abogados en Lugo fundado en 1973, con servicio en toda Galicia. Derecho penal económico, mercantil y concursal, tributario, civil y procesal, administrativo y laboral.',
    'url': DOMAIN + '/', 'logo': DOMAIN + '/assets/img/logo.png', 'image': DOMAIN + '/assets/img/og-cendan-amarelo.jpg',
    'foundingDate': '1973', 'founder': {'@type': 'Person', 'name': 'Antonio Cendán Corredoira'},
    'telephone': '+34982223053', 'faxNumber': '+34982223947', 'email': EMAIL, 'priceRange': '€€',
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
{header(active)}

  <main id="contenido">
{main}
  </main>

{footer()}

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

def build_home():
    intro = f'''  <div class="intro" aria-hidden="true">
    <div class="intro-logo">{tiles_svg('intro-tiles', 'in')}
      <picture><source srcset="/assets/img/logo-texto.webp" type="image/webp"><img class="intro-word" src="/assets/img/logo-texto.png" width="298" height="52" alt=""></picture>
    </div>
  </div>
'''
    main = f'''    <section class="hero" aria-labelledby="h1">
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <p class="eyebrow">Desde 1973</p>
          <h1 id="h1">Despacho de abogados <em>en Lugo</em><span class="dot" aria-hidden="true">.</span></h1>
          <p class="lead">Asesoramiento jurídico a empresas y particulares en toda Galicia, de forma personal e individualizada.</p>
          <div class="actions">
            <a class="btn btn-dark" href="/contacto/"><span>{CTA_LABEL}</span><i>{ARROW}</i></a>
            <a class="btn btn-line" href="/areas-de-practica/"><span>Áreas de práctica</span></a>
          </div>
        </div>
        <figure class="hero-art">
          {tiles_svg('hero-tiles', 'h')}
          {picture('jesus-a-amarelo-fernandez', 'Jesús A. Amarelo Fernández, socio', 'hero-ph hero-ph-a', eager=True)}
          {picture('francisco-gonzalez-gonzalez', 'Francisco González González, socio', 'hero-ph hero-ph-b')}
          <figcaption>Jesús A. Amarelo y Francisco González, socios</figcaption>
        </figure>
      </div>
    </section>

    <section class="facts" aria-label="El despacho en cifras">
      <div class="wrap">
        <dl class="facts-row">
          <div class="reveal"><dt>Año de fundación</dt><dd>1973</dd></div>
          <div class="reveal" style="--d:90ms"><dt>Áreas de práctica</dt><dd>6</dd></div>
          <div class="reveal" style="--d:180ms"><dt>Abogados en el equipo</dt><dd>5</dd></div>
          <div class="reveal" style="--d:270ms"><dt>Ámbito de actuación</dt><dd>Galicia</dd></div>
        </dl>
      </div>
    </section>

    <section class="section firma" aria-labelledby="h-firma">
      <div class="wrap">
        <h2 id="h-firma" class="statement reveal">Un equipo altamente cualificado, cuyo objetivo es la satisfacción de las necesidades de nuestros clientes.</h2>
        <div class="firma-grid">
          <div class="prose">
            <p class="reveal">La firma, fundada en 1973, ha crecido respondiendo a las demandas de sus clientes, ampliando sus campos de actuación e incorporando abogados especializados en las distintas materias.</p>
            <p class="reveal">Asesoramos a empresas y particulares en todas las áreas, entre ellos importantes empresas a nivel regional y nacional.</p>
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

    <section class="section section-paper" aria-labelledby="h-areas">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow reveal">Áreas de práctica</p>
          <h2 id="h-areas" class="reveal">Seis especialidades, un mismo equipo.</h2>
        </div>
        {areas_bento()}
      </div>
    </section>

    <section class="section" aria-labelledby="h-metodo">
      <div class="wrap">
        <h2 id="h-metodo" class="reveal">Cómo trabajamos.</h2>
        {method_list()}
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

{contact_block()}'''
    page('/', 'Despacho de abogados en Lugo | Cendán & Amarelo Abogados',
         'Cendán & Amarelo, despacho de abogados en Lugo desde 1973. Derecho penal económico, mercantil, tributario, civil, administrativo y laboral para empresas y particulares de Galicia.',
         main, home=True, intro=intro)


def build_firma():
    crumbs = [('La firma', '/despacho-abogados-lugo/')]
    hist = ''.join(f'<li class="reveal" style="--d:{n * 90}ms"><span class="tl-year">{y}</span><h3>{t}</h3><p>{d}</p></li>'
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


def build_area(a):
    crumbs = [('Áreas de práctica', '/areas-de-practica/'), (a['name'], f'/{a["slug"]}/')]
    lead_p, *rest = a['intro']
    rest_html = ''.join(f'<p class="reveal">{p}</p>' for p in rest)
    services = ''.join(f'<li class="reveal" style="--d:{(n % 2) * 60}ms">{s}</li>' for n, s in enumerate(a['services']))
    others = ''.join(f'<li><a href="/{o["slug"]}/">{o["name"]} {ARROW}</a></li>' for o in AREAS if o is not a)
    main = f'''{page_hero('Áreas de práctica', a['name'], a['short'], crumbs)}

    <section class="section">
      <div class="wrap narrow">
        <p class="statement reveal">{lead_p}</p>
        <div class="prose">{rest_html}</div>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-servicios">
      <div class="wrap">
        <h2 id="h-servicios" class="reveal">Qué hacemos.</h2>
        <ul class="services" role="list">{services}</ul>
        <p class="note reveal">{a['note']}</p>
      </div>
    </section>

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
    main = f'''{page_hero('Noticias', 'Actualidad jurídica', 'Seguimos a diario las novedades normativas y jurisprudenciales que afectan a nuestros clientes.', crumbs)}

    <section class="section">
      <div class="wrap narrow">
        <p class="statement reveal">Novedades en materia fiscal, laboral, mercantil, penal y administrativa.</p>
        <div class="prose">
          <p class="reveal">Recomendamos las noticias jurídicas de Iberley, actualizadas cada día. Si alguna novedad le afecta, contacte con nosotros y le asesoraremos.</p>
        </div>
        <a class="btn btn-line reveal" href="https://www.iberley.es/noticias" rel="noopener" target="_blank"><span>Noticias en Iberley</span><i>{ARROW}</i></a>
      </div>
    </section>

{contact_block(eyebrow=False)}'''
    page('/actualidad-juridica/', 'Actualidad jurídica | Cendán & Amarelo Abogados',
         'Actualidad jurídica: novedades fiscales, laborales, mercantiles, penales y administrativas. Cendán & Amarelo Abogados, Lugo.',
         main, '/actualidad-juridica/', crumbs)


def build_contacto():
    crumbs = [('Contacto', '/contacto/')]
    options = ''.join(f'<option>{a["name"]}</option>' for a in AREAS)
    faq = ''.join(f'<details class="reveal"><summary><h3>{q}</h3></summary><p>{r}</p></details>' for q, r in FAQ)
    main = f'''{page_hero('Contacto', 'Hablemos de su caso', 'Consúltenos sin compromiso y le daremos una primera valoración.', crumbs)}

    <section class="section">
      <div class="wrap contact">
        <dl class="contact-data">
          <div class="reveal"><dt>{ico('phone')}Teléfono</dt><dd class="cd-big"><a href="tel:+34982223053">{PHONE_HTML}</a></dd></div>
          <div class="reveal"><dt>{ico('envelope_simple')}Correo</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          <div class="reveal"><dt>{ico('map_pin')}Oficina</dt><dd>Avda. de A Coruña 10-14, Entlo.<br>27003 Lugo<br><a class="link" href="{MAPS}" rel="noopener" target="_blank">Cómo llegar {ARROW}</a></dd></div>
          <div class="reveal"><dt>{ico('clock')}Horario</dt><dd>Lunes a jueves, de 9:00 a 14:30 y de 16:00 a 19:30<br>Viernes, de 9:00 a 15:00</dd></div>
        </dl>

        <form class="form reveal" id="form" novalidate>
          <h2>Formulario de contacto</h2>
          <div class="field"><label for="f-name">Nombre y apellidos *</label><input id="f-name" name="nombre" type="text" autocomplete="name" required></div>
          <div class="field-row">
            <div class="field"><label for="f-mail">Email *</label><input id="f-mail" name="email" type="email" autocomplete="email" required></div>
            <div class="field"><label for="f-tel">Teléfono</label><input id="f-tel" name="telefono" type="tel" autocomplete="tel"></div>
          </div>
          <div class="field"><label for="f-area">Área</label><select id="f-area" name="area"><option value="">Seleccione (opcional)</option>{options}</select></div>
          <div class="field"><label for="f-msg">Mensaje *</label><textarea id="f-msg" name="mensaje" rows="5" required aria-describedby="f-msg-help"></textarea><p class="help" id="f-msg-help">Describa brevemente su asunto. No incluya información confidencial.</p></div>
          <label class="check"><input type="checkbox" name="privacidad" required><span>He leído y acepto el <a href="/aviso-legal/">Aviso legal y la política de privacidad</a>. *</span></label>
          <label class="check"><input type="checkbox" name="comunicaciones"><span>Acepto recibir comunicaciones del despacho (opcional).</span></label>
          <button class="btn btn-dark" type="submit"><span>Enviar consulta</span><i>{ARROW}</i></button>
          <p class="form-status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-faq">
      <div class="wrap firma-grid">
        <h2 id="h-faq" class="reveal">Preguntas frecuentes.</h2>
        <div class="faq">{faq}</div>
      </div>
    </section>'''
    faq_ld = {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': r}} for q, r in FAQ]}
    page('/contacto/', 'Contacto · Abogados en Lugo | Cendán & Amarelo',
         'Contacte con Cendán & Amarelo Abogados: Avda. de A Coruña 10-14, Lugo. Teléfono 982 223 053. Primera valoración sin compromiso.',
         main, '/contacto/', crumbs, [ORG, faq_ld])


def build_legal():
    for slug, (title, desc, body) in LEGAL.items():
        crumbs = [(title, f'/{slug}/')]
        main = f'''{page_hero('Información legal', title, '', crumbs)}

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
      <div class="wrap">
        <p class="eyebrow">Error 404</p>
        <h1>Esta página no existe</h1>
        <p class="lead">Es posible que la dirección haya cambiado con la nueva web del despacho.</p>
        <div class="actions">
          <a class="btn btn-dark" href="/"><span>Volver al inicio</span><i>{ARROW}</i></a>
          <a class="btn btn-line" href="/areas-de-practica/"><span>Áreas de práctica</span></a>
        </div>
      </div>
      {tiles_svg('page-tiles', 'ph')}
    </section>
  </main>
  <script src="/js/main.min.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8') as f:
        f.write(html)


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
- [Aviso legal]({DOMAIN}/aviso-legal/)
'''
    with open(os.path.join(ROOT, 'llms.txt'), 'w', encoding='utf-8') as f:
        f.write(txt)


if __name__ == '__main__':
    build_home()
    build_firma()
    build_areas_index()
    for area in AREAS:
        build_area(area)
    build_equipo()
    build_actualidad()
    build_contacto()
    build_legal()
    build_404()
    build_sitemap()
    build_llms()
    print(f'{len(SITEMAP)} páginas + 404 generadas')
