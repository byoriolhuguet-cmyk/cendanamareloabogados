"""Generador del sitio estático de Cendán & Amarelo Abogados.

Uso:  python3 scripts/build.py
Escribe todas las páginas HTML, sitemap.xml y llms.txt en la raíz del repositorio.
Las rutas son absolutas (/css/..., /contacto/) y conservan las URL de la web anterior.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from legal_content import PAGES as LEGAL  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOMAIN = 'https://www.cendanamareloabogados.com'
UPDATED = '2026-10-13'
PHONE_HTML = '982&nbsp;223&nbsp;053'
EMAIL = 'despacho@cendanamareloabogados.com'
ADDRESS = 'Avda. de A Coruña 10-14, Entlo. 27003 Lugo'
MAPS = 'https://www.google.com/maps/search/?api=1&amp;query=Avenida+de+A+Coru%C3%B1a+10-14+27003+Lugo'

# ---------------------------------------------------------------- Contenido

AREAS = [
    {
        'slug': 'abogados-derecho-penal-lugo', 'id': 'penal', 'name': 'Derecho Penal',
        'short': 'Defensa y acusación, con especial experiencia en Derecho penal económico.',
        'intro': [
            'Cendán &amp; Amarelo Abogados cuenta con una gran experiencia, principalmente, en Derecho penal económico.',
            'Asumimos la defensa y la acusación particular de empresas, directivos y particulares en todas las fases del procedimiento: desde la investigación y la asistencia en dependencias policiales y judiciales hasta el juicio oral y los recursos.',
        ],
        'services': [
            'Delitos societarios, estafas, apropiación indebida y administración desleal',
            'Delitos contra la Hacienda Pública y la Seguridad Social',
            'Insolvencias punibles y alzamiento de bienes',
            'Responsabilidad penal de la persona jurídica y programas de cumplimiento (<i>compliance</i>)',
            'Delitos contra el patrimonio y el orden socioeconómico',
            'Acusación particular y defensa de víctimas',
            'Recursos de apelación y casación',
        ],
        'note': 'El área penal trabaja coordinada con los departamentos mercantil y tributario, imprescindibles en los asuntos de Derecho penal económico.',
    },
    {
        'slug': 'abogados-derecho-mercantil-concursal-lugo', 'id': 'mercantil', 'name': 'Derecho Mercantil y Concursal',
        'short': 'Asesoramiento a empresas, desde su constitución hasta las situaciones de insolvencia.',
        'intro': [
            'Acompañamos a empresas y empresarios a lo largo de toda su vida societaria, con un asesoramiento continuado y preventivo que evita conflictos y protege el patrimonio de la compañía y de sus socios.',
            'Cuando surgen dificultades, intervenimos en la reestructuración de la deuda y en los procedimientos concursales, tanto en defensa del deudor como de los acreedores.',
        ],
        'services': [
            'Constitución de sociedades, modificaciones estatutarias y operaciones societarias',
            'Pactos de socios y protocolos familiares',
            'Contratación mercantil',
            'Conflictos entre socios e impugnación de acuerdos sociales',
            'Responsabilidad de administradores',
            'Planes de reestructuración y refinanciación',
            'Concurso de acreedores y exoneración del pasivo (segunda oportunidad)',
        ],
        'note': 'Trabajamos de forma coordinada con las áreas laboral y tributaria para ofrecer una visión completa de cada operación.',
    },
    {
        'slug': 'abogados-derecho-tributario-lugo', 'id': 'tributario', 'name': 'Derecho Tributario',
        'short': 'Planificación fiscal y defensa del contribuyente ante la Administración.',
        'intro': [
            'Asesoramos a particulares, profesionales y empresas en el cumplimiento de sus obligaciones fiscales y en la planificación de su tributación, siempre dentro del marco legal.',
            'Defendemos a nuestros clientes en los procedimientos de la Agencia Tributaria y de las haciendas autonómica y local, en vía administrativa, económico-administrativa y contencioso-administrativa.',
        ],
        'services': [
            'Planificación fiscal de empresas y patrimonios familiares',
            'Procedimientos de inspección, comprobación y gestión',
            'Procedimientos de recaudación y embargos',
            'Procedimientos sancionadores',
            'Reclamaciones económico-administrativas y recursos contencioso-administrativos',
            'Fiscalidad de sucesiones, donaciones y operaciones societarias',
        ],
        'note': 'El área tributaria colabora estrechamente con los departamentos mercantil y penal.',
    },
    {
        'slug': 'abogados-derecho-civil-procesal-lugo', 'id': 'civil', 'name': 'Derecho Civil y Procesal',
        'short': 'Familia, sucesiones, contratos y litigación civil.',
        'intro': [
            'Asesoramos y defendemos a particulares y empresas en todos los ámbitos del Derecho civil, con especial dedicación al Derecho de familia y sucesiones.',
            'Siempre que es posible buscamos una solución negociada; cuando no lo es, defendemos los intereses de nuestros clientes ante los juzgados y tribunales.',
        ],
        'services': [
            'Separaciones y divorcios, de mutuo acuerdo y contenciosos',
            'Guarda y custodia, régimen de visitas y pensiones',
            'Herencias, testamentos y particiones',
            'Contratos, obligaciones y responsabilidad civil',
            'Arrendamientos urbanos y rústicos',
            'Propiedad, comunidades y derechos reales',
            'Reclamaciones de cantidad y ejecuciones',
        ],
        'note': 'Cada asunto lo dirige un único letrado, que informa al cliente en cada fase del procedimiento.',
    },
    {
        'slug': 'abogados-derecho-adminitrativo-lugo', 'id': 'administrativo', 'name': 'Derecho Administrativo',
        'short': 'Defensa de particulares y empresas frente a las administraciones públicas.',
        'intro': [
            'Representamos a particulares y empresas en sus relaciones con la Administración del Estado, la Xunta de Galicia, las diputaciones y los ayuntamientos.',
            'Intervenimos tanto en vía administrativa como ante la jurisdicción contencioso-administrativa.',
        ],
        'services': [
            'Urbanismo, licencias y disciplina urbanística',
            'Expedientes sancionadores',
            'Contratación pública',
            'Responsabilidad patrimonial de la Administración',
            'Expropiación forzosa',
            'Función pública',
            'Recursos administrativos y contencioso-administrativos',
        ],
        'note': 'El área administrativa trabaja coordinada con la tributaria en los procedimientos con trascendencia fiscal.',
    },
    {
        'slug': 'abogados-derecho-laboral-lugo', 'id': 'laboral', 'name': 'Derecho Laboral',
        'short': 'Asesoramiento laboral integral a empresas y trabajadores.',
        'intro': [
            'El Derecho Laboral ha cobrado una extraordinaria importancia en el ámbito empresarial, convirtiéndose en una de las especialidades del Derecho con mayor prestigio de esta firma.',
            'Así, nuestro equipo de laboral cuenta con una dilatada experiencia y proporciona un asesoramiento laboral integral:',
        ],
        'services': [
            'Reestructuraciones de plantillas y Expedientes de Regulación de Empleo (ERE)',
            'Negociación de convenios colectivos y acuerdos de empresa',
            'Asesoramiento en la contratación',
            'Despidos y extinciones de contratos',
            'Arbitrajes laborales',
            'Incapacidades laborales y jubilaciones',
            'Relaciones laborales con altos directivos',
            '<i>Due diligence</i> laboral',
            'Actas de liquidación y/o infracción en materia de Seguridad Social o motivadas por accidentes de trabajo',
            'Manuales sobre políticas y protocolos de conducta',
            'Prevención de riesgos laborales',
        ],
        'note': 'Y, como no podía ser de otra forma, este departamento actúa coordinadamente con otras áreas de especialización, como la mercantil y tributaria, con el fin de alcanzar el mayor grado de eficiencia en el asesoramiento a nuestros clientes.',
    },
]

TEAM = [
    ('jesus-a-amarelo-fernandez', 'Jesús A. Amarelo Fernández', 'Socio'),
    ('francisco-gonzalez-gonzalez', 'Francisco González González', 'Socio'),
    ('ana-belen-rey-vazquez', 'Ana Belén Rey Vázquez', 'Abogada'),
    ('manuel-lugilde-valin', 'Manuel Lugilde Valín', 'Abogado'),
    ('david-couselo-cortegoso', 'David Couselo Cortegoso', 'Abogado'),
]

FAQ = [
    ('¿Dónde está el despacho?', 'En la Avenida de A Coruña, 10-14, Entresuelo, 27003 Lugo. Atendemos a clientes de Lugo y de toda Galicia.'),
    ('¿En qué áreas del Derecho trabajan?', 'Derecho penal (especialmente penal económico), mercantil y concursal, tributario, civil y procesal, administrativo y laboral.'),
    ('¿Desde cuándo ejerce el despacho?', 'Desde 1973, cuando lo fundó en Lugo el letrado Antonio Cendán Corredoira.'),
    ('¿Cuál es el horario de atención?', 'De lunes a jueves de 9:00 a 14:30 y de 16:00 a 19:30; los viernes de 9:00 a 15:00. Le recomendamos concertar cita previa.'),
    ('¿Atienden asuntos fuera de la provincia de Lugo?', 'Sí. Asesoramos y representamos a particulares y empresas ante juzgados, tribunales y administraciones de toda Galicia.'),
    ('¿Cómo solicito una primera consulta?', 'Llamando al 982 223 053, escribiendo a despacho@cendanamareloabogados.com o mediante el formulario de esta página. Le daremos una primera valoración sin compromiso.'),
]

NAV = [
    ('/despacho-abogados-lugo/', 'La firma'),
    ('/areas-de-practica/', 'Áreas de práctica'),
    ('/equipo-profesional/', 'Equipo'),
    ('/actualidad-juridica/', 'Actualidad'),
]

# ---------------------------------------------------------------- Piezas comunes

ARROW = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>'

# Teselas del logotipo (centro x, centro y, semidiagonal) en el espacio 116×68.
TILES = [(15.5, 63.5, 12.5), (36, 40, 17), (18, 24.5, 11.5), (56.5, 56.5, 19.5), (58, 16, 14),
         (77.5, 33, 16.5), (81.5, 66.5, 9.5), (97.5, 49.5, 14.5), (96.5, 13, 9)]


def tiles_svg(cls, uid):
    """Isotipo de Cendán & Amarelo reconstruido en SVG; cada tesela se anima por separado."""
    polys = ''
    for i, (x, y, r) in enumerate(TILES):
        z = round(0.4 + (i % 4) * 0.35, 2)
        polys += (f'<polygon style="--i:{i};--z:{z}" '
                  f'points="{x},{y - r} {x + r},{y} {x},{y + r} {x - r},{y}"/>')
    return (f'<svg class="{cls}" viewBox="0 0 116 68" aria-hidden="true" focusable="false">'
            f'<defs><linearGradient id="g{uid}" x1="0" y1="0" x2="0" y2="68" gradientUnits="userSpaceOnUse">'
            '<stop offset="0" stop-color="#f8dac4"/><stop offset=".5" stop-color="#f0a479"/>'
            '<stop offset="1" stop-color="#e8702a"/></linearGradient>'
            f'<clipPath id="c{uid}"><rect width="116" height="67.6"/></clipPath></defs>'
            f'<g fill="url(#g{uid})" clip-path="url(#c{uid})">{polys}</g></svg>')


def logo(cls='brand'):
    return (f'<a class="{cls}" href="/">'
            '<picture><source srcset="/assets/img/logo.webp" type="image/webp">'
            '<img src="/assets/img/logo.png" width="298" height="123" alt="Cendán &amp; Amarelo Abogados"></picture></a>')


def header(active):
    cur = ' aria-current="page"'
    items = ''.join(f'<li><a href="{h}"{cur if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f'''  <header class="site-header">
    <div class="wrap header-bar">
      {logo()}
      <nav class="nav" id="nav" aria-label="Principal">
        <ul>{items}</ul>
        <a class="nav-phone" href="tel:+34982223053">{PHONE_HTML}</a>
        <a class="btn btn-dark btn-sm" href="/contacto/"{cur if active == '/contacto/' else ''}><span>Contacto</span></a>
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
        <p class="kicker">Contacto</p>
        <ul class="footer-list">
          <li><a href="tel:+34982223053">{PHONE_HTML}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{ADDRESS}</li>
        </ul>
      </div>
      <nav aria-label="Áreas de práctica">
        <p class="kicker">Áreas</p>
        <ul class="footer-list">{areas}</ul>
      </nav>
      <nav aria-label="Enlaces">
        <p class="kicker">Enlaces</p>
        <ul class="footer-list">
          <li><a href="/despacho-abogados-lugo/">Quiénes somos</a></li>
          <li><a href="/equipo-profesional/">Profesionales</a></li>
          <li><a href="/actualidad-juridica/">Actualidad</a></li>
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
        <a href="https://es-es.facebook.com/pages/Cendan-Amarelo-Abogados/226246534135877" rel="noopener" target="_blank" aria-label="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7.5h2.5l.4-3h-2.9V8.6c0-.9.3-1.5 1.5-1.5h1.5V4.4c-.3 0-1.2-.1-2.2-.1-2.2 0-3.7 1.3-3.7 3.8v2.4H8v3h2.6V21h2.9z"/></svg></a>
        <a href="https://twitter.com/cendanamarelo" rel="noopener" target="_blank" aria-label="X (Twitter)"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.8 3h3.1l-6.8 7.7L22 21h-6.2l-4.9-6.4L5.3 21H2.2l7.2-8.3L1.8 3h6.4l4.4 5.8L17.8 3zm-1.1 16.2h1.7L7.4 4.7H5.6l11.1 14.5z"/></svg></a>
      </p>
    </div>
  </footer>'''


def cta(title='¿Necesita asesoramiento?', text='Contacte con nosotros sin compromiso y le daremos una primera valoración.'):
    return f'''    <section class="cta" aria-labelledby="cta-title">
      <div class="wrap cta-inner">
        {tiles_svg('cta-tiles', 'cta')}
        <div>
          <h2 id="cta-title" class="reveal">{title}</h2>
          <p class="reveal">{text}</p>
        </div>
        <div class="cta-actions reveal">
          <a class="btn btn-dark" href="/contacto/"><span>Consúltenos</span><i>{ARROW}</i></a>
          <a class="cta-phone" href="tel:+34982223053">{PHONE_HTML}</a>
        </div>
      </div>
    </section>'''


def page_head(title, desc, path, crumbs=None, extra_schema=None, home=False):
    graph = [{'@type': ['LegalService', 'LocalBusiness'], '@id': DOMAIN + '/#despacho', 'name': 'Cendán & Amarelo Abogados'}]
    if home:
        graph = [ORG]
    if crumbs:
        items = [{'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': DOMAIN + '/'}]
        for n, (name, url) in enumerate(crumbs, 2):
            items.append({'@type': 'ListItem', 'position': n, 'name': name, 'item': DOMAIN + url})
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': items})
    if extra_schema:
        graph.extend(extra_schema)
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    intro_js = ("try{if(!sessionStorage.getItem('ca-intro')){d.classList.add('is-intro');sessionStorage.setItem('ca-intro','1')}}catch(e){}"
                if home else '')
    esc = lambda s: s.replace('&', '&amp;').replace('&amp;amp;', '&amp;').replace('"', '&quot;')
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{DOMAIN}{path}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
  <meta name="theme-color" content="#ffffff">
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
  <link rel="preload" href="/assets/fonts/jost.woff2" as="font" type="font/woff2" crossorigin>
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
    out = os.path.join(ROOT, path.strip('/'), 'index.html') if path != '/' else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    SITEMAP.append(path)


def page_hero(eyebrow, h1, lead, crumbs):
    trail = '<li><a href="/">Inicio</a></li>' + ''.join(
        f'<li><a href="{u}">{n}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{n}</li>'
        for i, (n, u) in enumerate(crumbs))
    return f'''    <section class="page-hero">
      <div class="wrap">
        <nav class="crumbs" aria-label="Migas de pan"><ol>{trail}</ol></nav>
        <p class="eyebrow">{eyebrow}</p>
        <h1>{h1}<span class="dot" aria-hidden="true">.</span></h1>
        {f'<p class="lead">{lead}</p>' if lead else ''}
      </div>
      {tiles_svg('page-tiles', 'ph')}
    </section>'''


def team_grid():
    out = '<ul class="team" role="list">'
    for i, (slug, name, role) in enumerate(TEAM):
        out += f'''
          <li class="member reveal" style="--d:{i * 80}ms" id="{slug}">
            <figure>
              <picture><source srcset="/assets/img/equipo/{slug}.webp" type="image/webp">
              <img src="/assets/img/equipo/{slug}.jpg" width="375" height="450" loading="lazy" decoding="async" alt="{name}, {role.lower()} de Cendán &amp; Amarelo Abogados"></picture>
              <figcaption><strong>{name}</strong><span>{role}</span></figcaption>
            </figure>
          </li>'''
    return out + '\n        </ul>'


# ---------------------------------------------------------------- Datos estructurados

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

SITEMAP = []

# ---------------------------------------------------------------- Páginas


def build_home():
    intro = f'''  <div class="intro" aria-hidden="true">
    <div class="intro-logo">{tiles_svg('intro-tiles', 'in')}
      <picture><source srcset="/assets/img/logo-texto.webp" type="image/webp"><img class="intro-word" src="/assets/img/logo-texto.png" width="298" height="52" alt=""></picture>
    </div>
  </div>
'''
    areas = ''.join(f'''
          <li class="reveal" style="--d:{i * 60}ms"><a class="area-row" href="/{a["slug"]}/">
            <span class="area-n">0{i + 1}</span><span class="area-t">{a["name"]}</span><span class="area-s">{a["short"]}</span>{ARROW}
          </a></li>''' for i, a in enumerate(AREAS))
    main = f'''    <section class="hero" aria-labelledby="h1">
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <p class="eyebrow">Despacho de abogados · Lugo · Galicia</p>
          <h1 id="h1">Abogados en Lugo desde 1973<span class="dot" aria-hidden="true">.</span></h1>
          <p class="lead">Asesoramiento jurídico a empresas y particulares en toda Galicia, de forma personal e individualizada.</p>
          <div class="actions">
            <a class="btn btn-dark" href="/contacto/"><span>Solicitar consulta</span><i>{ARROW}</i></a>
            <a class="btn btn-line" href="/areas-de-practica/"><span>Áreas de práctica</span></a>
          </div>
        </div>
        <div class="hero-art">{tiles_svg('hero-tiles', 'h')}</div>
      </div>
      <div class="wrap">
        <dl class="stats">
          <div><dt>años de experiencia</dt><dd><sup>+</sup>40</dd></div>
          <div><dt>áreas de práctica</dt><dd>6</dd></div>
          <div><dt>abogados</dt><dd>5</dd></div>
        </dl>
      </div>
    </section>

    <section class="section" aria-labelledby="h-firma">
      <div class="wrap split">
        <p class="eyebrow reveal">La firma</p>
        <div>
          <h2 id="h-firma" class="statement reveal">Un equipo altamente cualificado, cuyo objetivo es la satisfacción de las necesidades de nuestros clientes.</h2>
          <p class="reveal">La firma, fundada en 1973, ha crecido respondiendo a las demandas de sus clientes, ampliando sus campos de actuación e incorporando abogados especializados en las distintas materias.</p>
          <a class="link reveal" href="/despacho-abogados-lugo/">Conocer la firma {ARROW}</a>
        </div>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-areas">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow reveal">Áreas de práctica</p>
          <h2 id="h-areas" class="reveal">Más de cuatro décadas en el ámbito empresarial y personal.</h2>
        </div>
        <ul class="area-list" role="list">{areas}
        </ul>
      </div>
    </section>

    <section class="section" aria-labelledby="h-equipo">
      <div class="wrap">
        <div class="section-head section-head-row">
          <div>
            <p class="eyebrow reveal">Equipo profesional</p>
            <h2 id="h-equipo" class="reveal">Conozca a nuestros abogados.</h2>
          </div>
          <a class="link reveal" href="/equipo-profesional/">Ver el equipo {ARROW}</a>
        </div>
        {team_grid()}
      </div>
    </section>

{cta()}'''
    page('/', 'Despacho de abogados en Lugo | Cendán & Amarelo Abogados',
         'Cendán & Amarelo, despacho de abogados en Lugo desde 1973. Derecho penal económico, mercantil, tributario, civil, administrativo y laboral para empresas y particulares de Galicia.',
         main, home=True, intro=intro)


def build_firma():
    crumbs = [('La firma', '/despacho-abogados-lugo/')]
    main = f'''{page_hero('La firma', 'Despacho de abogados en Lugo', 'Una trayectoria de más de treinta y cinco años al servicio de empresas y particulares.', crumbs)}

    <section class="section" aria-label="Presentación">
      <div class="wrap split">
        <p class="eyebrow reveal">Bienvenidos</p>
        <div class="prose">
          <p class="statement reveal">Cendán &amp; Amarelo es un despacho de abogados con una trayectoria de más de treinta y cinco años que cuenta con un equipo altamente cualificado, cuyo objetivo es la satisfacción de las necesidades de nuestros clientes.</p>
          <p class="reveal">La firma, fundada en 1973 por el letrado Antonio Cendán Corredoira, ha crecido desde entonces respondiendo a las demandas de nuestros clientes, ampliando sus campos de actuación e incorporando abogados especializados en las distintas materias.</p>
          <p class="reveal">Por su experiencia y profesionalidad, Cendán &amp; Amarelo cuenta con el respaldo y fidelidad de un gran número de clientes, prestando asesoramiento a empresas y particulares, a quienes asesora en todas las áreas, de forma personal e individualizada, entre las que se encuentran importantes empresas tanto a nivel regional como a nivel nacional.</p>
          <p class="reveal">Para responder adecuadamente a las necesidades de los clientes, otorgamos una especial atención a la formación continuada de nuestros profesionales. El trabajo en equipo y la gestión del conocimiento son herramientas fundamentales para el desarrollo de nuestros servicios.</p>
        </div>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-valores">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow reveal">Nuestros valores</p>
          <h2 id="h-valores" class="reveal">Lo que nos define.</h2>
        </div>
        <ul class="cards" role="list">
          <li class="card reveal"><span class="card-n">01</span><h3>Calidad</h3><p>Perseguimos la más alta calidad en el servicio.</p></li>
          <li class="card reveal" style="--d:80ms"><span class="card-n">02</span><h3>Especialización</h3><p>Especialización y experiencia en cada materia.</p></li>
          <li class="card reveal" style="--d:160ms"><span class="card-n">03</span><h3>Integridad</h3><p>Sólido compromiso por la excelencia y la integridad.</p></li>
        </ul>
      </div>
    </section>

    <section class="section" aria-labelledby="h-metodo">
      <div class="wrap split">
        <p class="eyebrow reveal">Cómo trabajamos</p>
        <div>
          <h2 id="h-metodo" class="reveal">Un compromiso sin fisuras con nuestros clientes, sin más límites que los que impone la ética profesional.</h2>
          <dl class="steps">
            <div class="reveal"><dt>Formación continuada</dt><dd>Formación académica y, en determinados casos, de postgrado en prestigiosas escuelas de negocios y universidades de Estados Unidos y de Europa.</dd></div>
            <div class="reveal"><dt>Trabajo en equipo</dt><dd>Interrelación departamental y suma de esfuerzos para un completo asesoramiento legal.</dd></div>
            <div class="reveal"><dt>Atención personal</dt><dd>Asesoramiento personal e individualizado, con un letrado responsable de cada asunto.</dd></div>
          </dl>
        </div>
      </div>
    </section>

{cta()}'''
    page('/despacho-abogados-lugo/', 'La firma · Despacho de abogados en Lugo desde 1973 | Cendán & Amarelo',
         'Cendán & Amarelo, despacho de abogados en Lugo fundado en 1973 por Antonio Cendán Corredoira. Calidad, especialización e integridad al servicio de empresas y particulares.',
         main, '/despacho-abogados-lugo/', crumbs)


def build_areas_index():
    crumbs = [('Áreas de práctica', '/areas-de-practica/')]
    rows = ''.join(f'''
          <li class="reveal" style="--d:{i * 60}ms"><a class="area-row" href="/{a["slug"]}/">
            <span class="area-n">0{i + 1}</span><span class="area-t">{a["name"]}</span><span class="area-s">{a["short"]}</span>{ARROW}
          </a></li>''' for i, a in enumerate(AREAS))
    main = f'''{page_hero('Áreas de práctica', 'Áreas de práctica', 'Desarrollamos nuestra actuación, tanto en el ámbito empresarial como en el ámbito personal, desde hace más de cuatro décadas.', crumbs)}

    <section class="section">
      <div class="wrap">
        <ul class="area-list" role="list">{rows}
        </ul>
      </div>
    </section>

{cta()}'''
    page('/areas-de-practica/', 'Áreas de práctica · Abogados en Lugo | Cendán & Amarelo',
         'Derecho penal, mercantil y concursal, tributario, civil y procesal, administrativo y laboral. Abogados especialistas en Lugo con servicio en toda Galicia.',
         main, '/areas-de-practica/', crumbs)


def build_area(i, a):
    crumbs = [('Áreas de práctica', '/areas-de-practica/'), (a['name'], f'/{a["slug"]}/')]
    intro = ''.join(f'<p class="reveal{" statement" if n == 0 else ""}">{p}</p>' for n, p in enumerate(a['intro']))
    services = ''.join(f'<li class="reveal" style="--d:{n * 40}ms">{s}</li>' for n, s in enumerate(a['services']))
    others = ''.join(f'<li><a href="/{o["slug"]}/">{o["name"]} {ARROW}</a></li>' for o in AREAS if o is not a)
    main = f'''{page_hero('Áreas de práctica · Lugo', a['name'], a['short'], crumbs)}

    <section class="section">
      <div class="wrap split">
        <p class="eyebrow reveal">0{i + 1}</p>
        <div class="prose">
          {intro}
          <ul class="checklist" role="list">{services}</ul>
          <p class="note reveal">{a['note']}</p>
        </div>
      </div>
    </section>

{cta('Necesita alguna consulta legal', 'Contacte con nosotros sin compromiso y le daremos una primera valoración.')}

    <section class="section section-tight" aria-labelledby="h-otras">
      <div class="wrap">
        <h2 id="h-otras" class="eyebrow">Otras áreas de práctica</h2>
        <ul class="other-areas" role="list">{others}</ul>
      </div>
    </section>'''
    service = {'@type': 'Service', 'name': a['name'], 'serviceType': a['name'], 'url': f'{DOMAIN}/{a["slug"]}/',
               'provider': {'@id': DOMAIN + '/#despacho'}, 'areaServed': ['Lugo', 'Galicia'],
               'description': a['short']}
    page(f'/{a["slug"]}/', f'Abogados de {a["name"]} en Lugo | Cendán & Amarelo',
         f'Abogados especialistas en {a["name"]} en Lugo y Galicia. {a["short"]} Primera valoración sin compromiso.',
         main, '/areas-de-practica/', crumbs, [service])


def build_equipo():
    crumbs = [('Equipo profesional', '/equipo-profesional/')]
    main = f'''{page_hero('Equipo profesional', 'Conozca a nuestros expertos', 'Nuestra firma está formada por experimentados profesionales que han ido engrosando nuestro número de socios a medida que asumían responsabilidades y acreditaban sus méritos.', crumbs)}

    <section class="section">
      <div class="wrap">
        {team_grid()}
      </div>
    </section>

    <section class="section section-paper" aria-label="Nuestro equipo">
      <div class="wrap split">
        <p class="eyebrow reveal">Formación y experiencia</p>
        <div class="prose">
          <p class="reveal">La formación, parte que consideramos fundamental para el ejercicio de esta profesión, ha sido la base sobre la que se han configurado las carreras de nuestros profesionales, completando una formación académica y, en determinados casos, de postgrado en algunas de las más prestigiosas escuelas de negocios y Universidades de los Estados Unidos de América y de Europa.</p>
          <p class="reveal">Nuestro equipo de trabajo, basado en la interrelación departamental y la suma de esfuerzos en el trabajo en equipo, se compone por abogados altamente cualificados para atender a las demandas de las empresas e individuos que requieren de un completo asesoramiento legal.</p>
          <p class="reveal">La experiencia adquirida a lo largo de los años por nuestro equipo nos ha permitido desarrollar un compromiso sin fisuras con nuestros clientes, sin más límites que los que impone la ética profesional.</p>
        </div>
      </div>
    </section>

{cta('¿Quiere unirse?', 'Si desea formar parte de nuestro equipo, envíenos su currículum a despacho@cendanamareloabogados.com.')}'''
    page('/equipo-profesional/', 'Equipo profesional · Abogados en Lugo | Cendán & Amarelo',
         'Conozca al equipo de abogados de Cendán & Amarelo en Lugo: Jesús A. Amarelo, Francisco González, Ana Belén Rey, Manuel Lugilde y David Couselo.',
         main, '/equipo-profesional/', crumbs)


def build_actualidad():
    crumbs = [('Actualidad jurídica', '/actualidad-juridica/')]
    main = f'''{page_hero('Noticias', 'Actualidad jurídica', 'Seguimos a diario las novedades normativas y jurisprudenciales que afectan a nuestros clientes.', crumbs)}

    <section class="section">
      <div class="wrap split">
        <p class="eyebrow reveal">Fuente</p>
        <div class="prose">
          <p class="statement reveal">Novedades en materia fiscal, laboral, mercantil, penal y administrativa.</p>
          <p class="reveal">Recomendamos las noticias jurídicas de Iberley, actualizadas cada día. Si alguna novedad le afecta, contacte con nosotros y le asesoraremos.</p>
          <a class="btn btn-line reveal" href="https://www.iberley.es/noticias" rel="noopener" target="_blank"><span>Noticias jurídicas en Iberley</span><i>{ARROW}</i></a>
        </div>
      </div>
    </section>

{cta()}'''
    page('/actualidad-juridica/', 'Actualidad jurídica | Cendán & Amarelo Abogados',
         'Actualidad jurídica: novedades fiscales, laborales, mercantiles, penales y administrativas. Cendán & Amarelo Abogados, Lugo.',
         main, '/actualidad-juridica/', crumbs)


def build_contacto():
    crumbs = [('Contacto', '/contacto/')]
    options = ''.join(f'<option>{a["name"]}</option>' for a in AREAS)
    faq = ''.join(f'<details class="reveal"><summary><h3>{q}</h3></summary><p>{r}</p></details>' for q, r in FAQ)
    main = f'''{page_hero('Contacto', 'Contacto', '¿Necesita asesoramiento? Consúltenos sin compromiso y le daremos una primera valoración.', crumbs)}

    <section class="section">
      <div class="wrap contact">
        <div class="contact-data">
          <div class="cd reveal"><p class="kicker">Llámenos</p><p class="cd-big"><a href="tel:+34982223053">{PHONE_HTML}</a></p></div>
          <div class="cd reveal"><p class="kicker">Envíe un mensaje</p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
          <div class="cd reveal"><p class="kicker">Oficina</p><p>Avda. de A Coruña 10-14, Entlo.<br>27003 Lugo</p><a class="link" href="{MAPS}" rel="noopener" target="_blank">Cómo llegar {ARROW}</a></div>
          <div class="cd reveal"><p class="kicker">Horario</p><p>Lunes a jueves: 9:00 – 14:30 y 16:00 – 19:30<br>Viernes: 9:00 – 15:00</p></div>
        </div>

        <form class="form reveal" id="form" novalidate>
          <h2>Formulario de contacto</h2>
          <div class="field"><label for="f-name">Nombre y apellidos *</label><input id="f-name" name="nombre" type="text" autocomplete="name" required></div>
          <div class="field"><label for="f-mail">Email *</label><input id="f-mail" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="f-tel">Teléfono</label><input id="f-tel" name="telefono" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="f-area">Área</label><select id="f-area" name="area"><option value="">Seleccione (opcional)</option>{options}</select></div>
          <div class="field"><label for="f-msg">Mensaje *</label><textarea id="f-msg" name="mensaje" rows="5" required></textarea></div>
          <label class="check"><input type="checkbox" name="privacidad" required><span>He leído y acepto el <a href="/aviso-legal/">Aviso legal y la política de privacidad</a>. *</span></label>
          <label class="check"><input type="checkbox" name="comunicaciones"><span>Acepto recibir comunicaciones del despacho (opcional).</span></label>
          <button class="btn btn-dark" type="submit"><span>Enviar consulta</span><i>{ARROW}</i></button>
          <p class="form-status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-faq">
      <div class="wrap split">
        <div>
          <p class="eyebrow reveal">Preguntas frecuentes</p>
          <h2 id="h-faq" class="reveal">Resolvemos sus dudas.</h2>
        </div>
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
    html = page_head('Página no encontrada | Cendán & Amarelo Abogados', 'La página solicitada no existe.', '/404.html')
    html = html.replace('index, follow, max-snippet:-1, max-image-preview:large', 'noindex')
    html += f'''<body>
{header('')}
  <main id="contenido">
    <section class="hero hero-404">
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <p class="eyebrow">Error 404</p>
          <h1>Esta página no existe<span class="dot" aria-hidden="true">.</span></h1>
          <p class="lead">Es posible que la dirección haya cambiado con la nueva web del despacho.</p>
          <div class="actions">
            <a class="btn btn-dark" href="/"><span>Volver al inicio</span><i>{ARROW}</i></a>
            <a class="btn btn-line" href="/contacto/"><span>Contacto</span></a>
          </div>
        </div>
        <div class="hero-art">{tiles_svg('hero-tiles', 'h')}</div>
      </div>
    </section>
  </main>
  <script src="/js/main.min.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def build_sitemap():
    urls = ''.join(
        f'  <url><loc>{DOMAIN}{p}</loc><lastmod>{UPDATED}</lastmod><priority>{"1.0" if p == "/" else "0.3" if p.strip("/") in LEGAL else "0.8"}</priority></url>\n'
        for p in SITEMAP)
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')


def build_llms():
    areas = '\n'.join(f'- [{a["name"]}]({DOMAIN}/{a["slug"]}/): {a["short"]}' for a in AREAS)
    team = '\n'.join(f'- {n} — {r}' for _, n, r in TEAM)
    txt = f'''# Cendán & Amarelo Abogados

> Despacho de abogados en Lugo (Galicia, España), fundado en 1973 por el letrado Antonio Cendán Corredoira. Asesora a empresas y particulares de Lugo y de toda Galicia, de forma personal e individualizada.

- Razón social: Cendán & Amarelo Abogados, S.L.P. (NIF B27365667)
- Registro Mercantil de Lugo: Tomo 385 · Libro 0 · Folio 42 · Hoja LU-12246
- Dirección: Avenida de A Coruña, 10-14, Entresuelo, 27003 Lugo
- Teléfono: +34 982 223 053 · Fax: +34 982 223 947
- Email: {EMAIL}
- Horario: lunes a jueves 9:00–14:30 y 16:00–19:30; viernes 9:00–15:00
- Redes: https://twitter.com/cendanamarelo · https://es-es.facebook.com/pages/Cendan-Amarelo-Abogados/226246534135877

## Áreas de práctica
{areas}

## Equipo
{team}

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
    for n, area in enumerate(AREAS):
        build_area(n, area)
    build_equipo()
    build_actualidad()
    build_contacto()
    build_legal()
    build_404()
    build_sitemap()
    build_llms()
    print(f'{len(SITEMAP)} páginas + 404 generadas')
