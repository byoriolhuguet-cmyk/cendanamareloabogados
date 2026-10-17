"""Generador del sitio estático de Cendán & Amarelo Abogados.

Uso:  sh scripts/build.sh        (genera el HTML y minifica CSS/JS)
      python3 scripts/build.py   (sólo HTML, sitemap.xml, llms*.txt, despacho.json y feed RSS)

Contenido editable: scripts/content.py y scripts/legal_content.py. Noticias: data/news.json (scripts/news.py).
Rutas absolutas que conservan las URL de la web anterior.
"""
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

sys.path.insert(0, os.path.dirname(__file__))
from content import AREAS, FAQ, GUIDES, HISTORY, KEYS, LAWYERS, METHOD, PROVINCES, TEAM  # noqa: E402
from icons import ICONS  # noqa: E402
from legal_content import PAGES as LEGAL  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOMAIN = 'https://www.cendanamareloabogados.com'
UPDATED = '2026-10-17'
PHONE_TEL = '+34982223053'
PHONE_HTML = '982&nbsp;223&nbsp;053'
EMAIL = 'despacho@cendanamareloabogados.com'
WHATSAPP = '34982223053'      # cambiar aquí si el WhatsApp es un móvil distinto (formato internacional, sin "+")
WA_URL = f'https://wa.me/{WHATSAPP}?text=Hola,%20quisiera%20hacer%20una%20consulta%20al%20despacho.'
MAPS = 'https://www.google.com/maps/search/?api=1&amp;query=Avenida+de+A+Coru%C3%B1a+10-14+27003+Lugo'
CTA = 'Solicitar consulta'
SITEMAP = []
AREA_BY_ID = {a['id']: a for a in AREAS}
AREA_LABEL = {a['id']: a['name'].replace('Derecho ', '').split(' y ')[0] for a in AREAS}
AREA_LABEL['general'] = 'General'
MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
DAYS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']


def load_news():
    try:
        with open(os.path.join(ROOT, 'data', 'news.json'), encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {'updated': None, 'items': []}


NEWS = load_news()


def parse_iso(iso):
    return datetime.strptime(iso[:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)


def fecha(iso, weekday=False):
    d = parse_iso(iso) if len(iso) > 10 else datetime.strptime(iso, '%Y-%m-%d')
    out = f'{d.day} de {MONTHS[d.month - 1]} de {d.year}'
    return f'{DAYS[d.weekday()]}, {out}' if weekday else out


def top_news(n=5, hours=48):
    """Las más importantes de las últimas horas (puntuación calculada por scripts/news.py)."""
    items = NEWS['items']
    if not items:
        return []
    newest = max(parse_iso(i['date']) for i in items)
    recent = [i for i in items if parse_iso(i['date']) >= newest - timedelta(hours=hours)] or items
    return sorted(recent, key=lambda i: (i.get('score', 0), i['date']), reverse=True)[:n]


def esc(s):
    return s.replace('&', '&amp;').replace('&amp;amp;', '&amp;').replace('"', '&quot;')


def h(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def strip_tags(t):
    return re.sub(r'<[^>]+>', '', t).replace('&amp;', '&')


# ---------------------------------------------------------------- Piezas

def ico(name, cls='ico'):
    box, inner = ICONS[name]
    return f'<svg class="{cls}" viewBox="{box}" aria-hidden="true" focusable="false">{inner}</svg>'


ARROW = ico('arrow_up_right')

def logo_img(cls=''):
    """Logotipo ORIGINAL del despacho (300x128 px, fondo blanco), sin modificar ni redibujar.
    Siempre sobre fondo blanco, con altura automática (nunca se deforma) y como máximo a la mitad
    de su tamaño para que se vea nítido en pantallas de alta densidad."""
    return (f'<picture class="logo {cls}"><source srcset="/assets/img/logo-original.webp" type="image/webp">'
            f'<img src="/assets/img/logo-original.png" width="300" height="128" alt="Cendán &amp; Amarelo Abogados"></picture>')


def office(cls='', eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture class="office {cls}"><source media="(max-width: 700px)" srcset="/assets/img/despacho-lugo-760.webp" type="image/webp">'
            '<source srcset="/assets/img/despacho-lugo.webp" type="image/webp">'
            f'<img src="/assets/img/despacho-lugo.jpg" width="1200" height="769" {load} decoding="async" '
            'alt="Entrada del despacho Cendán &amp; Amarelo Abogados en Lugo, con el logotipo en la mampara de cristal"></picture>')


def picture(slug, alt, cls='', eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture class="{cls}"><source srcset="/assets/img/equipo/{slug}.webp" type="image/webp">'
            f'<img src="/assets/img/equipo/{slug}.jpg" width="375" height="450" {load} decoding="async" alt="{alt}"></picture>')


def btn(label, href, kind='dark', extra='', arrow=True):
    tail = f'<i>{ARROW}</i>' if arrow else ''
    return f'<a class="btn btn-{kind} {extra}" href="{href}"><span>{label}</span>{tail}</a>'


def wa_link(cls='btn btn-line', label='WhatsApp'):
    return f'<a class="{cls}" href="{WA_URL}" rel="noopener" target="_blank">{ico("whatsapp")}<span>{label}</span></a>'


def contact_form(uid, compact=False):
    """Formulario de contacto (hero y cierre). Envía a /api/contact; si no está configurado, abre el correo."""
    options = ''.join(f'<option>{a["name"]}</option>' for a in AREAS)
    extra = '' if compact else f'''
          <div class="f-field f-wide"><label for="{uid}-mail">Email</label><input id="{uid}-mail" name="email" type="email" autocomplete="email" inputmode="email"><p class="f-err">Revise el email.</p></div>'''
    rows = 3 if compact else 5
    comms = '' if compact else '<label class="f-check"><input type="checkbox" name="comunicaciones"><span>Acepto recibir comunicaciones del despacho (opcional).</span></label>'
    return f'''<form class="cform{' cform-compact' if compact else ''}" id="{uid}" novalidate data-form>
        <div class="f-grid">
          <div class="f-field"><label for="{uid}-name">Nombre *</label><input id="{uid}-name" name="nombre" type="text" autocomplete="name" required><p class="f-err">Indique su nombre.</p></div>
          <div class="f-field"><label for="{uid}-tel">Teléfono *</label><input id="{uid}-tel" name="telefono" type="tel" autocomplete="tel" inputmode="tel" required minlength="9"><p class="f-err">Indique un teléfono de contacto.</p></div>{extra}
          <div class="f-field f-wide"><label for="{uid}-area">Área</label><select id="{uid}-area" name="area"><option value="">Seleccione (opcional)</option>{options}</select></div>
          <div class="f-field f-wide"><label for="{uid}-msg">Su consulta *</label><textarea id="{uid}-msg" name="mensaje" rows="{rows}" required></textarea><p class="f-err">Cuéntenos brevemente su caso.</p></div>
        </div>
        <div class="f-hp" aria-hidden="true"><label>Web <input type="text" name="web" tabindex="-1" autocomplete="off"></label></div>
        <label class="f-check"><input type="checkbox" name="privacidad" required><span>Acepto el <a href="/aviso-legal/">aviso legal y la política de privacidad</a>.&nbsp;*</span></label>
        {comms}
        <button class="btn btn-accent btn-block" type="submit"><span>Enviar consulta</span><i>{ARROW}</i></button>
        <p class="f-status" role="status" aria-live="polite"></p>
      </form>'''


# ---------------------------------------------------------------- Cabecera con menús desplegables

def header(active):
    cur = ' aria-current="page"'
    areas = ''.join(f'<li><a href="/{a["slug"]}/"><strong>{a["name"]}</strong><span>{a["short"]}</span></a></li>' for a in AREAS)
    team = ''.join(f'<li><a href="/equipo-profesional/{s}/">{picture(s, "", "mm-ph")}<span><strong>{n}</strong><small>{r}</small></span></a></li>'
                   for s, n, r in TEAM)

    def top(href, label, key):
        return f'<a class="nav-link" href="{href}"{cur if active == key else ""}>{label}</a>'

    def drop(key, label, panel):
        mark = ' data-current="true"' if active == key else ''
        return (f'<button class="nav-link nav-drop" type="button" aria-expanded="false" aria-controls="{panel}"{mark}>'
                f'{label}{ico("ph_caret_down", "ico caret")}</button>')
    return f'''  <header class="site-header" data-header>
    <div class="wrap header-bar">
      <a class="brand" href="/">{logo_img()}</a>
      <nav class="nav" id="nav" aria-label="Principal">
        <ul class="nav-list">
          <li>{top('/despacho-abogados-lugo/', 'La firma', 'firma')}</li>
          <li class="has-mega">{drop('areas', 'Áreas de práctica', 'mm-areas')}
            <div class="mega" id="mm-areas">
              <div class="mega-inner">
                <div class="mega-intro"><p class="mega-title">Áreas de práctica</p><p>Seis especialidades coordinadas para empresas y particulares.</p>{btn('Ver todas', '/areas-de-practica/', 'line', 'btn-sm')}</div>
                <ul class="mega-areas">{areas}</ul>
              </div>
            </div>
          </li>
          <li class="has-mega">{drop('equipo', 'Equipo profesional', 'mm-team')}
            <div class="mega" id="mm-team">
              <div class="mega-inner">
                <div class="mega-intro"><p class="mega-title">Equipo profesional</p><p>Abogados colegiados en el Ilustre Colegio de la Abogacía de Lugo.</p>{btn('Ver el equipo', '/equipo-profesional/', 'line', 'btn-sm')}</div>
                <ul class="mega-team">{team}</ul>
              </div>
            </div>
          </li>
          <li class="has-mega">{drop('actualidad', 'Actualidad', 'mm-news')}
            <div class="mega mega-sm" id="mm-news">
              <div class="mega-inner">
                <ul class="mega-links">
                  <li><a href="/actualidad-juridica/"><strong>Noticias del día</strong><span>Lo más importante del mundo jurídico, cada mañana.</span></a></li>
                  <li><a href="/guias-juridicas/"><strong>Guías jurídicas</strong><span>Despidos, herencias en Galicia, Hacienda.</span></a></li>
                  <li><a href="/abogados-galicia/"><strong>Galicia y España</strong><span>Nuestro ámbito de actuación.</span></a></li>
                </ul>
              </div>
            </div>
          </li>
          <li>{top('/contacto/', 'Contacto', 'contacto')}</li>
        </ul>
        <div class="nav-aside">
          <a class="nav-phone" href="tel:{PHONE_TEL}">{ico('phone')}<span>{PHONE_HTML}</span></a>
          {btn(CTA, '#consulta-final', 'accent', 'btn-sm nav-cta', arrow=False)}
          <div class="nav-mobile-extra">
            {wa_link('btn btn-line btn-block')}
            <p>Avda. de A Coruña 10-14, Entlo. 27003 Lugo<br>Lunes a jueves, 9:00 a 14:30 y 16:00 a 19:30. Viernes, 9:00 a 15:00</p>
          </div>
        </div>
      </nav>
      <a class="head-call" href="tel:{PHONE_TEL}" aria-label="Llamar al despacho">{ico('phone')}</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Abrir menú"><span></span><span></span></button>
    </div>
  </header>'''


def footer():
    areas = ''.join(f'<li><a href="/{a["slug"]}/">{a["name"]}</a></li>' for a in AREAS)
    team = ''.join(f'<li><a href="/equipo-profesional/{s}/">{n}</a></li>' for s, n, _ in TEAM)
    return f'''  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-top">
        <a class="footer-brand" href="/">{logo_img()}</a>
        <p class="footer-claim">Despacho de abogados en Lugo desde 1973. Asesoramiento a empresas y particulares en Galicia y en toda España.</p>
      </div>
      <div class="footer-grid">
        <div>
          <p class="footer-title">Despacho</p>
          <ul class="footer-list">
            <li><a href="tel:{PHONE_TEL}">{PHONE_HTML}</a></li>
            <li><a href="{WA_URL}" rel="noopener" target="_blank">WhatsApp</a></li>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><a href="{MAPS}" rel="noopener" target="_blank">Avda. de A Coruña 10-14, Entlo.<br>27003 Lugo</a></li>
            <li>L a J: 9:00 a 14:30 y 16:00 a 19:30<br>V: 9:00 a 15:00</li>
          </ul>
        </div>
        <nav aria-label="Áreas de práctica"><p class="footer-title">Áreas</p><ul class="footer-list">{areas}</ul></nav>
        <nav aria-label="Equipo"><p class="footer-title">Equipo</p><ul class="footer-list">{team}</ul></nav>
        <nav aria-label="El despacho">
          <p class="footer-title">El despacho</p>
          <ul class="footer-list">
            <li><a href="/despacho-abogados-lugo/">Quiénes somos</a></li>
            <li><a href="/actualidad-juridica/">Actualidad jurídica</a></li>
            <li><a href="/guias-juridicas/">Guías jurídicas</a></li>
            <li><a href="/abogados-galicia/">Galicia y España</a></li>
            <li><a href="/contacto/">Contacto</a></li>
            <li><a href="mailto:{EMAIL}?subject=Curr%C3%ADculum">Envíenos su CV</a></li>
          </ul>
        </nav>
      </div>
      <div class="footer-bottom">
        <p>© <span data-year>2026</span> Cendán &amp; Amarelo Abogados, S.L.P. NIF B27365667</p>
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
    </div>
  </footer>
  <a class="wa-float" href="{WA_URL}" rel="noopener" target="_blank" aria-label="Escríbanos por WhatsApp">{ico('whatsapp')}<span>Escríbanos</span></a>'''


def finale(title='Hablemos de su caso.', text='Primera valoración sin compromiso. Le respondemos en el menor plazo posible.'):
    """Cierre de cada página: formulario completo y datos de contacto."""
    return f'''    <section class="finale" id="consulta-final" aria-labelledby="fin-title">
      <div class="wrap finale-grid">
        <div class="finale-copy">
          <p class="eyebrow">Contacto</p>
          <h2 id="fin-title" class="display-lg reveal">{title}</h2>
          <p class="reveal">{text}</p>
          <dl class="finale-data">
            <div class="reveal"><dt>{ico('phone')}Teléfono</dt><dd><a href="tel:{PHONE_TEL}">{PHONE_HTML}</a></dd></div>
            <div class="reveal"><dt>{ico('whatsapp')}WhatsApp</dt><dd><a href="{WA_URL}" rel="noopener" target="_blank">Escríbanos ahora</a></dd></div>
            <div class="reveal"><dt>{ico('envelope_simple')}Correo</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
            <div class="reveal"><dt>{ico('map_pin')}Oficina</dt><dd><a href="{MAPS}" rel="noopener" target="_blank">Avda. de A Coruña 10-14, Entlo. 27003 Lugo</a></dd></div>
            <div class="reveal"><dt>{ico('clock')}Horario</dt><dd>Lunes a jueves, de 9:00 a 14:30 y de 16:00 a 19:30. Viernes, de 9:00 a 15:00</dd></div>
          </dl>
        </div>
        <div class="finale-form reveal">
          <p class="form-title">Escríbanos</p>
          {contact_form('form-fin')}
        </div>
      </div>
    </section>'''


def page_hero(eyebrow, title, lead, crumbs, art=''):
    trail = '<li><a href="/">Inicio</a></li>' + ''.join(
        f'<li><a href="{u}">{n}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{n}</li>'
        for i, (n, u) in enumerate(crumbs))
    return f'''    <section class="phero">
      <div class="wrap phero-grid">
        <div class="phero-copy">
          <nav class="crumbs" aria-label="Migas de pan"><ol>{trail}</ol></nav>
          <p class="eyebrow">{eyebrow}</p>
          <h1 class="display-xl">{title}</h1>
          {f'<p class="lead">{lead}</p>' if lead else ''}
          <div class="actions">{btn(CTA, '#consulta-final', 'accent')}<a class="btn btn-line" href="tel:{PHONE_TEL}">{ico('phone')}<span>{PHONE_HTML}</span></a></div>
        </div>
        {art}
      </div>
    </section>'''


def news_list(items, cls=''):
    out = ''
    for n, it in enumerate(items):
        area = it.get('area', 'general')
        out += (f'<li class="news-item reveal" style="--d:{(n % 6) * 50}ms" data-area="{area}" data-scope="{it.get("scope", "españa")}">'
                f'<a href="{h(it["url"])}" rel="noopener nofollow" target="_blank">'
                f'<span class="news-meta"><span class="tag">{AREA_LABEL.get(area, "General")}</span>'
                f'<time datetime="{it["date"]}">{fecha(it["date"])}</time></span>'
                f'<span class="news-title">{h(it["title"])}</span>'
                f'<span class="news-src">{h(it["source"])} {ARROW}</span></a></li>')
    return f'<ol class="news-list {cls}" role="list">{out}</ol>'


def guide_cards(guides, level='h3'):
    return '<ul class="guides" role="list">' + ''.join(
        f'<li class="guide reveal" style="--d:{n * 80}ms"><a href="/guias-juridicas/{g["slug"]}/"><span class="tag">{AREA_LABEL[g["area"]]}</span>'
        f'<{level}>{g["title"]}</{level}><p>{g["desc"]}</p><span class="go">Leer la guía {ARROW}</span></a></li>'
        for n, g in enumerate(guides)) + '</ul>'


def areas_rows(level='h3'):
    """Lista editorial de áreas: nombre, resumen y tres claves de un vistazo; la fila completa enlaza al área."""
    rows = ''
    for i, a in enumerate(AREAS):
        keys = ''.join(f'<li>{k}</li>' for k in KEYS[a['id']])
        rows += f'''
          <li class="arow reveal" style="--d:{i * 60}ms"><a href="/{a["slug"]}/">
            <{level} class="arow-name">{a["name"]}</{level}>
            <p class="arow-short">{a["short"]}</p>
            <ul class="arow-keys">{keys}</ul>
            <span class="arow-go">{ARROW}</span>
          </a></li>'''
    return f'<ol class="arows" role="list">{rows}\n        </ol>'


def tcard(i, s, n, r, level):
    areas = ', '.join(AREA_LABEL[x] for x in LAWYERS[s]['areas']) or 'Equipo jurídico'
    return f'''
          <li class="tcard reveal" style="--d:{i * 80}ms"><a href="/equipo-profesional/{s}/">
            {picture(s, f'{n}, {r.lower()} de Cendán &amp; Amarelo Abogados', 'tcard-ph')}
            <div class="tcard-body"><{level}>{n}</{level}><span class="tcard-role">{r}</span><span class="tcard-areas">{areas}</span></div>
          </a></li>'''


def team_rail(level='h3'):
    return '<ul class="team-grid" role="list">' + ''.join(tcard(i, s, n, r, level) for i, (s, n, r) in enumerate(TEAM)) + '\n        </ul>'


def faq_list(items):
    return ''.join(
        f'<details class="faq-item reveal" style="--d:{n * 50}ms"><summary><h3>{q}</h3>{ico("ph_caret_down", "ico caret")}</summary><p>{r}</p></details>'
        for n, (q, r) in enumerate(items))


def timeline():
    return '<ol class="timeline" role="list">' + ''.join(
        f'<li class="reveal" style="--d:{n * 90}ms"><span class="tl-year">{y}</span><h3>{t}</h3><p>{d}</p></li>'
        for n, (y, t, d) in enumerate(HISTORY)) + '</ol>'


def method_stack():
    nums = ['01', '02', '03']
    return '<ol class="mstack" role="list">' + ''.join(
        f'<li class="mcard" style="--n:{n}"><span class="mcard-n" aria-hidden="true">{nums[n]}</span><h3>{t}</h3><p>{d}</p></li>'
        for n, (t, d) in enumerate(METHOD)) + '</ol>'


def aside_card():
    return f'''<aside class="aside-card" aria-label="Contacto">
          <p class="aside-title">¿Hablamos de su caso?</p>
          <p>Primera valoración sin compromiso.</p>
          {btn(CTA, '#consulta-final', 'accent', 'btn-block')}
          {wa_link('btn btn-line btn-block')}
          <a class="aside-phone" href="tel:{PHONE_TEL}">{ico('phone')}{PHONE_HTML}</a>
        </aside>'''


# ---------------------------------------------------------------- Plantilla

ORG = {
    '@type': ['LegalService', 'LocalBusiness'], '@id': DOMAIN + '/#despacho',
    'name': 'Cendán & Amarelo Abogados', 'legalName': 'Cendán & Amarelo Abogados, S.L.P.',
    'alternateName': ['Cendán y Amarelo Abogados', 'Cendán & Amarelo, Abogados y Asesores Tributarios'],
    'taxID': 'B27365667',
    'description': 'Despacho de abogados en Lugo fundado en 1973. Asesoramiento a empresas y particulares en Galicia y en toda España: Derecho penal económico, mercantil y concursal, tributario, civil y procesal, administrativo y laboral.',
    'url': DOMAIN + '/', 'logo': DOMAIN + '/assets/img/logo-original.png', 'image': DOMAIN + '/assets/img/og-cendan-amarelo.jpg',
    'foundingDate': '1973', 'founder': {'@type': 'Person', 'name': 'Antonio Cendán Corredoira'},
    'telephone': PHONE_TEL, 'faxNumber': '+34982223947', 'email': EMAIL, 'priceRange': '€€', 'knowsLanguage': ['es', 'gl'],
    'address': {'@type': 'PostalAddress', 'streetAddress': 'Avenida de A Coruña, 10-14, Entresuelo', 'addressLocality': 'Lugo',
                'postalCode': '27003', 'addressRegion': 'Galicia', 'addressCountry': 'ES'},
    'hasMap': MAPS.replace('&amp;', '&'),
    'areaServed': [{'@type': 'City', 'name': 'Lugo'}] + [{'@type': 'AdministrativeArea', 'name': p} for p, _ in PROVINCES]
                  + [{'@type': 'AdministrativeArea', 'name': 'Galicia'}, {'@type': 'Country', 'name': 'España'}],
    'openingHoursSpecification': [
        {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'], 'opens': '09:00', 'closes': '14:30'},
        {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'], 'opens': '16:00', 'closes': '19:30'},
        {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Friday', 'opens': '09:00', 'closes': '15:00'}],
    'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': PHONE_TEL, 'email': EMAIL,
                      'availableLanguage': ['es', 'gl'], 'areaServed': 'ES'}],
    'sameAs': ['https://twitter.com/cendanamarelo', 'https://es-es.facebook.com/pages/Cendan-Amarelo-Abogados/226246534135877'],
    'knowsAbout': ['Derecho penal económico', 'Derecho penal', 'Derecho mercantil', 'Derecho concursal', 'Derecho tributario',
                   'Derecho civil', 'Derecho procesal', 'Derecho de familia', 'Derecho civil de Galicia', 'Derecho administrativo', 'Derecho laboral'],
    'employee': [{'@type': 'Person', '@id': f'{DOMAIN}/equipo-profesional/{s}/#persona', 'name': n, 'jobTitle': r,
                  'url': f'{DOMAIN}/equipo-profesional/{s}/', 'image': f'{DOMAIN}/assets/img/equipo/{s}.jpg'} for s, n, r in TEAM],
    'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Áreas de práctica', 'itemListElement': [
        {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': a['name'], 'url': f'{DOMAIN}/{a["slug"]}/'}} for a in AREAS]},
}


def page(path, title, desc, main, active='', crumbs=None, schema=None, home=False, intro='',
         robots='index, follow, max-snippet:-1, max-image-preview:large'):
    graph = [ORG] if home or path == '/contacto/' else [{'@type': ['LegalService', 'LocalBusiness'], '@id': DOMAIN + '/#despacho', 'name': 'Cendán & Amarelo Abogados'}]
    if crumbs:
        items = [{'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': DOMAIN + '/'}]
        items += [{'@type': 'ListItem', 'position': n, 'name': strip_tags(nm), 'item': DOMAIN + u} for n, (nm, u) in enumerate(crumbs, 2)]
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': items})
    graph += schema or []
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    intro_js = ("try{if(!sessionStorage.getItem('ca-intro')){d.classList.add('is-intro');sessionStorage.setItem('ca-intro','1')}}catch(e){}" if home else '')
    html = f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{DOMAIN}{path}">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#ffffff">
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
  <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="icon" href="/favicon-48.png" type="image/png" sizes="48x48">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="alternate" type="application/rss+xml" title="Actualidad jurídica · Cendán &amp; Amarelo" href="/actualidad-juridica/feed.xml">
  <link rel="alternate" type="text/plain" title="Información para asistentes de IA" href="/llms.txt">
  <link rel="preload" href="/assets/fonts/hanken.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/css/styles.min.css">
  <script>(function(d){{d.classList.add('js');{intro_js}}})(document.documentElement)</script>
  <script type="application/ld+json">
{ld}
  </script>
</head>
<body>
{intro}  <a class="skip" href="#contenido">Saltar al contenido</a>
  <div class="progress" aria-hidden="true"></div>
{header(active)}

  <main id="contenido">
{main}
  </main>

{footer()}

  <script src="/js/main.min.js" defer></script>
</body>
</html>
'''
    if path == '/404.html':
        out = os.path.join(ROOT, '404.html')
    elif path == '/':
        out = os.path.join(ROOT, 'index.html')
    else:
        out = os.path.join(ROOT, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    if robots.startswith('index'):
        SITEMAP.append(path)


# ---------------------------------------------------------------- Páginas

def build_home():
    intro = '''  <div class="intro" aria-hidden="true"><div class="intro-box"><p class="intro-name">Cendán &amp; Amarelo</p><p class="intro-sub">Abogados</p><span class="intro-bar"><span></span></span></div></div>
'''
    facts = [('1973', 'Año de fundación'), ('6', 'Áreas de práctica'), ('5', 'Abogados'), ('+40', 'Años de experiencia')]
    pre = ' data-prefix="+"'
    facts_html = ''.join(
        f'<div class="reveal" style="--d:{n * 90}ms"><dt>{t}</dt><dd data-count="{v.lstrip("+")}"{pre if v.startswith("+") else ""}>{v}</dd></div>'
        for n, (v, t) in enumerate(facts))
    words = ''.join(f'<span>{a["name"].replace("Derecho ", "")}</span><i aria-hidden="true"></i>' for a in AREAS)
    top = top_news(5)
    news_block = news_list(top, 'news-compact') if top else '<p class="lead">Cada mañana, lo más importante del mundo jurídico en Galicia y España.</p>'
    upd = f'<p class="news-date">{fecha(NEWS["updated"], weekday=True).capitalize()}</p>' if NEWS.get('updated') else ''
    main = f'''    <section class="hero" aria-labelledby="h1" id="consulta">
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <p class="eyebrow">Abogados en Lugo · Desde 1973</p>
          <h1 id="h1" class="display-hero">Despacho de abogados <em>en Lugo</em><span class="dot">.</span></h1>
          <p class="lead">Asesoramiento jurídico a empresas y particulares en Galicia y en toda España, de forma personal e individualizada.</p>
          <ul class="hero-facts" role="list">
            <li><strong>6</strong> áreas de práctica</li>
            <li><strong>5</strong> abogados</li>
            <li><strong>+40</strong> años de ejercicio</li>
          </ul>
          <div class="hero-links">
            <a href="tel:{PHONE_TEL}">{ico('phone')}<span>{PHONE_HTML}</span></a>
            <a href="{WA_URL}" rel="noopener" target="_blank">{ico('whatsapp')}<span>WhatsApp</span></a>
          </div>
        </div>
        <div class="hero-form">
          <p class="form-title">Primera valoración sin compromiso</p>
          <p class="form-sub">Déjenos sus datos y le llamamos.</p>
          {contact_form('form-hero', compact=True)}
        </div>
      </div>
    </section>

    <div class="marquee" aria-hidden="true"><div class="marquee-track"><div>{words}</div><div>{words}</div></div></div>

    <section class="section firma" aria-labelledby="h-firma">
      <div class="wrap">
        <div class="firma-grid">
          <div class="firma-copy">
            <p class="eyebrow">La firma</p>
            <h2 id="h-firma" class="display-lg reveal">Un equipo altamente cualificado al servicio de sus clientes.</h2>
            <p class="firma-text reveal">Fundada en 1973 por el letrado Antonio Cendán Corredoira, la firma ha crecido respondiendo a las demandas de sus clientes, ampliando sus campos de actuación e incorporando abogados especializados en las distintas materias. Asesora a empresas y particulares, entre ellos importantes compañías de ámbito regional y nacional.</p>
            <ul class="values" role="list">
              <li class="reveal">Perseguimos la más alta calidad en el servicio</li>
              <li class="reveal" style="--d:90ms">Especialización y experiencia</li>
              <li class="reveal" style="--d:180ms">Compromiso por la excelencia y la integridad</li>
            </ul>
            {btn('Conocer la firma', '/despacho-abogados-lugo/', 'line')}
          </div>
          <figure class="firma-art">
            {office('firma-ph')}
            <figcaption>Nuestro despacho en la Avenida de A Coruña, Lugo</figcaption>
          </figure>
        </div>
        <dl class="facts">{facts_html}</dl>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-areas">
      <div class="wrap">
        <div class="head-row">
          <h2 id="h-areas" class="display-lg reveal">Áreas de práctica.</h2>
          <a class="link reveal" href="/areas-de-practica/">Todas las áreas {ARROW}</a>
        </div>
        {areas_rows()}
      </div>
    </section>

    <section class="section method" aria-labelledby="h-metodo">
      <div class="wrap method-grid">
        <div class="method-head">
          <h2 id="h-metodo" class="display-lg reveal">Cómo trabajamos.</h2>
          <p class="reveal">Un compromiso sin fisuras con nuestros clientes, sin más límites que los que impone la ética profesional.</p>
        </div>
        {method_stack()}
      </div>
    </section>

    <section class="section section-team" aria-labelledby="h-equipo">
      <div class="wrap">
        <div class="head-row">
          <h2 id="h-equipo" class="display-lg reveal">El equipo.</h2>
          <a class="link reveal" href="/equipo-profesional/">Conocer al equipo {ARROW}</a>
        </div>
        {team_rail()}
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-tray">
      <div class="wrap">
        <h2 id="h-tray" class="display-lg reveal">Trayectoria.</h2>
        {timeline()}
      </div>
    </section>

    <section class="section" aria-labelledby="h-actualidad">
      <div class="wrap">
        <div class="head-row">
          <div><p class="eyebrow">Hoy en el mundo jurídico</p><h2 id="h-actualidad" class="display-lg reveal">Actualidad.</h2>{upd}</div>
          <a class="link reveal" href="/actualidad-juridica/">Todas las noticias {ARROW}</a>
        </div>
        <div class="home-news">{news_block}{guide_cards(GUIDES[:2])}</div>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-faq">
      <div class="wrap faq-grid">
        <div><h2 id="h-faq" class="display-lg reveal">Preguntas frecuentes.</h2><a class="link reveal" href="/contacto/#preguntas">Más preguntas {ARROW}</a></div>
        <div class="faq">{faq_list(FAQ[:4])}</div>
      </div>
    </section>

{finale()}'''
    faq_ld = {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': r}} for q, r in FAQ[:4]]}
    speak = {'@type': 'WebPage', 'url': DOMAIN + '/', 'name': 'Despacho de abogados en Lugo', 'inLanguage': 'es-ES',
             'about': {'@id': DOMAIN + '/#despacho'}, 'speakable': {'@type': 'SpeakableSpecification', 'cssSelector': ['#h1', '.hero .lead', '.hero-facts']}}
    page('/', 'Despacho de abogados en Lugo · Galicia y España | Cendán & Amarelo Abogados',
         'Cendán & Amarelo, despacho de abogados en Lugo desde 1973. Derecho penal económico, mercantil, tributario, civil, administrativo y laboral para empresas y particulares de Galicia y toda España.',
         main, home=True, intro=intro, schema=[faq_ld, speak])


def build_firma():
    crumbs = [('La firma', '/despacho-abogados-lugo/')]
    main = f'''{page_hero('La firma', 'Despacho de abogados en Lugo', 'Una trayectoria iniciada en 1973 al servicio de empresas y particulares.', crumbs, f'<figure class="phero-photo">{office(eager=True)}</figure>')}

    <section class="section">
      <div class="wrap narrow">
        <p class="statement reveal">Cendán &amp; Amarelo es un despacho de abogados con una trayectoria de más de treinta y cinco años que cuenta con un equipo altamente cualificado, cuyo objetivo es la satisfacción de las necesidades de nuestros clientes.</p>
        <ul class="values" role="list">
          <li class="reveal">Perseguimos la más alta calidad en el servicio</li>
          <li class="reveal" style="--d:90ms">Especialización y experiencia</li>
          <li class="reveal" style="--d:180ms">Sólido compromiso por la excelencia y la integridad</li>
        </ul>
        <div class="prose two-col">
          <p class="reveal">La firma, fundada en 1973 por el letrado Antonio Cendán Corredoira, ha crecido desde entonces respondiendo a las demandas de nuestros clientes, ampliando sus campos de actuación e incorporando abogados especializados en las distintas materias.</p>
          <p class="reveal">Por su experiencia y profesionalidad, Cendán &amp; Amarelo cuenta con el respaldo y fidelidad de un gran número de clientes, prestando asesoramiento a empresas y particulares, a quienes asesora en todas las áreas, de forma personal e individualizada, entre las que se encuentran importantes empresas tanto a nivel regional como a nivel nacional.</p>
          <p class="reveal">Para responder adecuadamente a las necesidades de los clientes, otorgamos una especial atención a la formación continuada de nuestros profesionales. El trabajo en equipo y la gestión del conocimiento son herramientas fundamentales para el desarrollo de nuestros servicios.</p>
        </div>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-tray">
      <div class="wrap"><h2 id="h-tray" class="display-lg reveal">Trayectoria.</h2>{timeline()}</div>
    </section>

    <section class="section method" aria-labelledby="h-metodo">
      <div class="wrap method-grid">
        <div class="method-head">
          <h2 id="h-metodo" class="display-lg reveal">Cómo trabajamos.</h2>
          <p class="reveal">Un compromiso sin fisuras con nuestros clientes, sin más límites que los que impone la ética profesional.</p>
        </div>
        {method_stack()}
      </div>
    </section>

    <section class="section section-paper section-team" aria-labelledby="h-equipo">
      <div class="wrap"><div class="head-row"><h2 id="h-equipo" class="display-lg reveal">El equipo.</h2><a class="link reveal" href="/equipo-profesional/">Ver el equipo {ARROW}</a></div>
        {team_rail()}
      </div>
    </section>

{finale()}'''
    page('/despacho-abogados-lugo/', 'La firma · Despacho de abogados en Lugo desde 1973 | Cendán & Amarelo',
         'Cendán & Amarelo, despacho de abogados en Lugo fundado en 1973 por Antonio Cendán Corredoira. Calidad, especialización e integridad al servicio de empresas y particulares.',
         main, 'firma', crumbs)


def build_areas_index():
    crumbs = [('Áreas de práctica', '/areas-de-practica/')]
    main = f'''{page_hero('Especialidades', 'Áreas de práctica', 'Desarrollamos nuestra actuación, tanto en el ámbito empresarial como en el ámbito personal, desde hace más de cuatro décadas.', crumbs)}

    <section class="section">
      <div class="wrap">
        {areas_rows('h2')}
        <p class="note reveal">Los departamentos trabajan de forma coordinada: cada asunto se estudia desde todas las áreas que le afectan.</p>
      </div>
    </section>

{finale()}'''
    page('/areas-de-practica/', 'Áreas de práctica · Abogados en Lugo y Galicia | Cendán & Amarelo',
         'Derecho penal, mercantil y concursal, tributario, civil y procesal, administrativo y laboral. Abogados especialistas en Lugo con servicio en Galicia y toda España.',
         main, 'areas', crumbs)


def build_area(a):
    crumbs = [('Áreas de práctica', '/areas-de-practica/'), (a['name'], f'/{a["slug"]}/')]
    lead_p, *rest = a['intro']
    rest_html = ''.join(f'<p class="reveal">{p}</p>' for p in rest)
    services = ''.join(f'<li class="reveal" style="--d:{(n % 2) * 60}ms">{ico("ph_check")}<span>{s}</span></li>' for n, s in enumerate(a['services']))
    lawyers = [(s, n, r) for s, n, r in TEAM if a['id'] in LAWYERS[s]['areas']]
    law_html = ''.join(f'<li><a href="/equipo-profesional/{s}/">{picture(s, n, "mini-ph")}<span><strong>{n}</strong><small>{r}</small></span></a></li>' for s, n, r in lawyers)
    news = [i for i in NEWS['items'] if i.get('area') == a['id']][:4]
    guides = [g for g in GUIDES if g['area'] == a['id']]
    related = ''
    if news or guides:
        related = f'''
    <section class="section section-paper" aria-labelledby="h-act">
      <div class="wrap">
        <div class="head-row"><h2 id="h-act" class="display-md reveal">Actualidad de {a['name']}.</h2><a class="link reveal" href="/actualidad-juridica/">Toda la actualidad {ARROW}</a></div>
        {guide_cards(guides) if guides else ''}
        {news_list(news) if news else ''}
      </div>
    </section>'''
    others = ''.join(f'<li><a href="/{o["slug"]}/">{o["name"]} {ARROW}</a></li>' for o in AREAS if o is not a)
    team_block = f'<h2 class="display-md sub reveal">Abogados del área.</h2><ul class="mini-team" role="list">{law_html}</ul>' if law_html else ''
    main = f'''{page_hero('Áreas de práctica', a['name'], a['short'], crumbs)}

    <section class="section">
      <div class="wrap with-aside">
        <div class="main-col">
          <p class="statement reveal">{lead_p}</p>
          <div class="prose">{rest_html}</div>
          <h2 class="display-md sub reveal">Qué hacemos.</h2>
          <ul class="services" role="list">{services}</ul>
          <p class="note reveal">{a['note']}</p>
          {team_block}
        </div>
        {aside_card()}
      </div>
    </section>
{related}

    <section class="section-tight" aria-labelledby="h-otras">
      <div class="wrap">
        <h2 id="h-otras" class="mini-title">Otras áreas de práctica</h2>
        <ul class="pills" role="list">{others}</ul>
      </div>
    </section>

{finale('¿Necesita alguna consulta legal?')}'''
    service = {'@type': 'Service', 'name': a['name'], 'serviceType': a['name'], 'url': f'{DOMAIN}/{a["slug"]}/',
               'provider': {'@id': DOMAIN + '/#despacho'}, 'areaServed': ['Lugo', 'Galicia', 'España'], 'description': a['short']}
    page(f'/{a["slug"]}/', f'Abogados de {a["name"]} en Lugo y Galicia | Cendán & Amarelo',
         f'Abogados especialistas en {a["name"]} en Lugo, Galicia y toda España. {a["short"]} Primera valoración sin compromiso.',
         main, 'areas', crumbs, [service])


def build_equipo():
    crumbs = [('Equipo profesional', '/equipo-profesional/')]
    grid = ''.join(tcard(i, s, n, r, 'h2') for i, (s, n, r) in enumerate(TEAM))
    main = f'''{page_hero('Equipo profesional', 'Conozca a nuestros expertos', 'Experimentados profesionales que han ido engrosando nuestro número de socios a medida que asumían responsabilidades y acreditaban sus méritos.', crumbs)}

    <section class="section">
      <div class="wrap"><ul class="team-grid" role="list">{grid}</ul></div>
    </section>

    <section class="section section-paper" aria-labelledby="h-form">
      <div class="wrap narrow">
        <h2 id="h-form" class="display-lg reveal">Formación y experiencia.</h2>
        <div class="prose two-col">
          <p class="reveal">La formación, parte que consideramos fundamental para el ejercicio de esta profesión, ha sido la base sobre la que se han configurado las carreras de nuestros profesionales, completando una formación académica y, en determinados casos, de postgrado en algunas de las más prestigiosas escuelas de negocios y Universidades de los Estados Unidos de América y de Europa.</p>
          <p class="reveal">Nuestro equipo de trabajo, basado en la interrelación departamental y la suma de esfuerzos en el trabajo en equipo, se compone por abogados altamente cualificados para atender a las demandas de las empresas e individuos que requieren de un completo asesoramiento legal.</p>
        </div>
        <p class="note reveal">¿Quiere formar parte del equipo? Envíenos su currículum a <a class="u" href="mailto:{EMAIL}?subject=Curr%C3%ADculum">{EMAIL}</a>.</p>
      </div>
    </section>

{finale()}'''
    page('/equipo-profesional/', 'Equipo profesional · Abogados en Lugo | Cendán & Amarelo',
         'Conozca al equipo de abogados de Cendán & Amarelo en Lugo: Jesús A. Amarelo, Francisco González, Ana Belén Rey, Manuel Lugilde y David Couselo.',
         main, 'equipo', crumbs)
    for s, n, r in TEAM:
        info = LAWYERS[s]
        crumbs_l = crumbs + [(n, f'/equipo-profesional/{s}/')]
        areas = ''.join(f'<li><a href="/{AREA_BY_ID[x]["slug"]}/">{AREA_BY_ID[x]["name"]} {ARROW}</a></li>' for x in info['areas'])
        col = f'<div><dt>Colegiado</dt><dd>Nº {info["colegiado"]} del Ilustre Colegio de la Abogacía de Lugo</dd></div>' if info['colegiado'] else ''
        others = ''.join(f'<li><a href="/equipo-profesional/{o}/">{on} {ARROW}</a></li>' for o, on, _ in TEAM if o != s)
        art = f'<figure class="phero-portrait">{picture(s, f"{n}, {r.lower()} de Cendán &amp; Amarelo Abogados", eager=True)}</figure>'
        areas_block = f'<h2 class="display-md sub reveal">Áreas de práctica.</h2><ul class="pills" role="list">{areas}</ul>' if areas else ''
        main_l = f'''{page_hero(r, n, '', crumbs_l, art)}

    <section class="section">
      <div class="wrap with-aside">
        <div class="main-col">
          <p class="statement reveal">{info['text']}</p>
          <dl class="profile-data">
            <div><dt>Cargo</dt><dd>{r}</dd></div>
            {col}
            <div><dt>Despacho</dt><dd>Avda. de A Coruña 10-14, Entlo. 27003 Lugo</dd></div>
          </dl>
          {areas_block}
        </div>
        {aside_card()}
      </div>
    </section>

    <section class="section-tight" aria-labelledby="h-otros">
      <div class="wrap"><h2 id="h-otros" class="mini-title">Resto del equipo</h2><ul class="pills" role="list">{others}</ul></div>
    </section>

{finale()}'''
        person = {'@type': 'Person', '@id': f'{DOMAIN}/equipo-profesional/{s}/#persona', 'name': n, 'jobTitle': r,
                  'image': f'{DOMAIN}/assets/img/equipo/{s}.jpg', 'worksFor': {'@id': DOMAIN + '/#despacho'},
                  'knowsAbout': [AREA_BY_ID[x]['name'] for x in info['areas']], 'workLocation': {'@type': 'Place', 'name': 'Lugo'}}
        if info['colegiado']:
            person['memberOf'] = {'@type': 'Organization', 'name': 'Ilustre Colegio de la Abogacía de Lugo'}
        page(f'/equipo-profesional/{s}/', f'{n}, {r.lower()} · Cendán & Amarelo Abogados, Lugo',
             f'{n}, {r.lower()} de Cendán & Amarelo Abogados en Lugo. ' + strip_tags(info['text'])[:110],
             main_l, 'equipo', crumbs_l, [person])


def build_actualidad():
    crumbs = [('Actualidad jurídica', '/actualidad-juridica/')]
    items = NEWS['items']
    top = top_news(6)
    chips = ('<button type="button" class="chip" aria-pressed="true" data-filter="all">Todas</button>'
             '<button type="button" class="chip" aria-pressed="false" data-filter="galicia">Galicia</button>'
             + ''.join(f'<button type="button" class="chip" aria-pressed="false" data-filter="{a["id"]}">{AREA_LABEL[a["id"]]}</button>' for a in AREAS))
    by_day = {}
    for i in items:
        by_day.setdefault(i['date'][:10], []).append(i)
    days = ''.join(f'<section class="news-day" aria-label="{fecha(d)}"><h3 class="news-day-title">{fecha(d, weekday=True).capitalize()}</h3>{news_list(v, "news-filterable")}</section>'
                   for d, v in sorted(by_day.items(), reverse=True))
    upd = fecha(NEWS['updated'], weekday=True) if NEWS.get('updated') else ''
    top_html = ''.join(
        f'<li class="reveal" style="--d:{n * 70}ms"><a href="{h(i["url"])}" rel="noopener nofollow" target="_blank"><span class="top-n">{n + 1:02d}</span>'
        f'<span class="top-body"><span class="tag">{AREA_LABEL.get(i["area"], "General")}</span><span class="news-title">{h(i["title"])}</span>'
        f'<span class="news-src">{h(i["source"])} {ARROW}</span></span></a></li>' for n, i in enumerate(top))
    if items:
        body = f'''
    <section class="section" aria-labelledby="h-hoy">
      <div class="wrap">
        <p class="eyebrow">Lo más importante</p>
        <h2 id="h-hoy" class="display-lg reveal">Hoy, {upd}.</h2>
        <ol class="top-news" role="list">{top_html}</ol>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-archivo">
      <div class="wrap">
        <h2 id="h-archivo" class="display-lg reveal">Últimos días.</h2>
        <div class="chips" role="group" aria-label="Filtrar noticias">{chips}</div>
        {days}
        <p class="news-empty" hidden>No hay noticias recientes en esta categoría.</p>
      </div>
    </section>'''
    else:
        body = '''
    <section class="section"><div class="wrap narrow"><p class="statement">Las noticias se publican cada mañana.</p><p class="lead">Vuelva en unas horas para ver la selección del día.</p></div></section>'''
    main = f'''{page_hero('Noticias diarias', 'Actualidad jurídica en Galicia y España', 'Cada mañana seleccionamos las noticias jurídicas más importantes de España y de Galicia. Cada titular enlaza a su fuente original.', crumbs)}
{body}

    <section class="section" aria-labelledby="h-guias">
      <div class="wrap">
        <div class="head-row"><h2 id="h-guias" class="display-lg reveal">Guías del despacho.</h2><a class="link reveal" href="/guias-juridicas/">Todas las guías {ARROW}</a></div>
        {guide_cards(GUIDES)}
      </div>
    </section>

{finale('¿Le afecta alguna novedad?', 'Le explicamos cómo puede afectarle. Primera valoración sin compromiso.')}'''
    schema = [{'@type': 'CollectionPage', 'name': 'Actualidad jurídica en Galicia y España', 'url': f'{DOMAIN}/actualidad-juridica/',
               'dateModified': NEWS.get('updated') or UPDATED, 'inLanguage': 'es-ES', 'publisher': {'@id': DOMAIN + '/#despacho'},
               'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': n, 'url': i['url'], 'name': i['title']}
                                                                        for n, i in enumerate(top or items[:10], 1)]}}]
    page('/actualidad-juridica/', 'Actualidad jurídica hoy: noticias de Galicia y España | Cendán & Amarelo Abogados',
         'Noticias jurídicas diarias de Galicia y España: lo más importante en penal, mercantil, tributario, civil, administrativo y laboral, seleccionado cada mañana.',
         main, 'actualidad', crumbs, schema)
    entries = ''.join(
        f'<item><title>{h(i["title"])}</title><link>{h(i["url"])}</link><guid isPermaLink="false">{h(i["url"])}</guid>'
        f'<pubDate>{format_datetime(parse_iso(i["date"]))}</pubDate><category>{AREA_LABEL.get(i["area"], "General")}</category></item>' for i in items[:40])
    os.makedirs(os.path.join(ROOT, 'actualidad-juridica'), exist_ok=True)
    with open(os.path.join(ROOT, 'actualidad-juridica', 'feed.xml'), 'w', encoding='utf-8') as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Actualidad jurídica · Cendán &amp; Amarelo Abogados</title>'
                f'<link>{DOMAIN}/actualidad-juridica/</link><description>Noticias jurídicas de Galicia y España seleccionadas cada día por Cendán &amp; Amarelo Abogados (Lugo).</description>'
                f'<language>es-ES</language>{entries}</channel></rss>\n')


def build_guides():
    crumbs = [('Guías jurídicas', '/guias-juridicas/')]
    main = f'''{page_hero('Guías', 'Guías jurídicas', 'Respuestas claras a las dudas legales más habituales, redactadas por el despacho.', crumbs)}

    <section class="section"><div class="wrap">{guide_cards(GUIDES, 'h2')}</div></section>

{finale()}'''
    page('/guias-juridicas/', 'Guías jurídicas | Cendán & Amarelo Abogados, Lugo',
         'Guías jurídicas de Cendán & Amarelo: despidos, herencias en Galicia, inspecciones de Hacienda y más.', main, 'actualidad', crumbs)
    for g in GUIDES:
        area = AREA_BY_ID[g['area']]
        crumbs_g = crumbs + [(g['title'], f'/guias-juridicas/{g["slug"]}/')]
        toc = ''.join(f'<li><a href="#s{n}">{t}</a></li>' for n, (t, _) in enumerate(g['sections'], 1))
        summary = ''.join(f'<li>{ico("ph_check")}<span>{x}</span></li>' for x in g['summary'])
        body = ''.join(f'<h2 id="s{n}" class="reveal">{t}</h2>' + ''.join(f'<p class="reveal">{p}</p>' for p in ps) for n, (t, ps) in enumerate(g['sections'], 1))
        main_g = f'''{page_hero(AREA_LABEL[g['area']], g['title'], g['desc'], crumbs_g)}

    <section class="section">
      <div class="wrap with-aside">
        <article class="main-col article">
          <p class="article-meta">Cendán &amp; Amarelo Abogados · <time datetime="{g['date']}">{fecha(g['date'])}</time></p>
          <div class="summary reveal"><p class="summary-title">En resumen</p><ul role="list">{summary}</ul></div>
          <nav class="toc" aria-label="Contenido de la guía"><p>Contenido</p><ol>{toc}</ol></nav>
          <div class="prose">{body}</div>
          <p class="note reveal">Esta guía ofrece información general y no sustituye al asesoramiento profesional. Cada caso requiere un estudio individual.</p>
          {btn(f'Más sobre {area["name"]}', f'/{area["slug"]}/', 'line')}
        </article>
        {aside_card()}
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="h-mas">
      <div class="wrap"><h2 id="h-mas" class="display-md reveal">Otras guías.</h2>{guide_cards([x for x in GUIDES if x is not g])}</div>
    </section>

{finale()}'''
        art = {'@type': 'Article', 'headline': g['title'], 'description': g['desc'], 'datePublished': g['date'], 'dateModified': g['date'],
               'inLanguage': 'es-ES', 'author': {'@id': DOMAIN + '/#despacho'}, 'publisher': {'@id': DOMAIN + '/#despacho'},
               'mainEntityOfPage': f'{DOMAIN}/guias-juridicas/{g["slug"]}/', 'image': DOMAIN + '/assets/img/og-cendan-amarelo.jpg',
               'about': area['name'], 'spatialCoverage': 'Galicia, España'}
        page(f'/guias-juridicas/{g["slug"]}/', f'{g["title"]} | Cendán & Amarelo Abogados', g['desc'], main_g, 'actualidad', crumbs_g, [art])


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

    <section class="section section-paper" aria-labelledby="h-prov">
      <div class="wrap"><h2 id="h-prov" class="display-lg reveal">Las cuatro provincias gallegas.</h2><ul class="provinces" role="list">{prov}</ul></div>
    </section>

    <section class="section" aria-labelledby="h-esp">
      <div class="wrap narrow">
        <h2 id="h-esp" class="display-lg reveal">También en el resto de España.</h2>
        <ul class="values" role="list">
          <li class="reveal">Audiencia Nacional y Tribunal Supremo</li>
          <li class="reveal" style="--d:90ms">Administración General del Estado y Agencia Tributaria</li>
          <li class="reveal" style="--d:180ms">Empresas con actividad en varias comunidades autónomas</li>
        </ul>
      </div>
    </section>

{finale()}'''
    schema = [{'@type': 'Service', 'name': 'Asesoramiento jurídico en Galicia y España', 'provider': {'@id': DOMAIN + '/#despacho'},
               'areaServed': [{'@type': 'AdministrativeArea', 'name': p} for p, _ in PROVINCES] + [{'@type': 'Country', 'name': 'España'}]}]
    page('/abogados-galicia/', 'Abogados en Galicia y España: Lugo, A Coruña, Ourense y Pontevedra | Cendán & Amarelo',
         'Despacho de abogados con sede en Lugo que actúa en toda Galicia (Lugo, A Coruña, Ourense, Pontevedra) y ante los tribunales de toda España.',
         main, '', crumbs, schema)


def build_contacto():
    crumbs = [('Contacto', '/contacto/')]
    main = f'''{page_hero('Contacto', 'Hablemos de su caso', 'Consúltenos sin compromiso: por teléfono, por WhatsApp, por correo o con el formulario.', crumbs)}

    <section class="section">
      <div class="wrap contact-grid">
        <div>
          <div class="contact-quick">
            <a class="btn btn-dark btn-block" href="tel:{PHONE_TEL}">{ico('phone')}<span>Llamar&nbsp;al&nbsp;{PHONE_HTML}</span></a>
            {wa_link('btn btn-line btn-block')}
          </div>
          <figure class="contact-photo reveal">{office()}</figure>
          <dl class="data-list">
            <div class="reveal"><dt>{ico('envelope_simple')}Correo</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
            <div class="reveal"><dt>{ico('map_pin')}Oficina</dt><dd>Avda. de A Coruña 10-14, Entlo.<br>27003 Lugo<br><a class="link" href="{MAPS}" rel="noopener" target="_blank">Cómo llegar {ARROW}</a></dd></div>
            <div class="reveal"><dt>{ico('clock')}Horario</dt><dd>Lunes a jueves, de 9:00 a 14:30 y de 16:00 a 19:30<br>Viernes, de 9:00 a 15:00</dd></div>
          </dl>
        </div>
        <div class="contact-form reveal" id="consulta-final"><p class="form-title">Formulario de contacto</p>{contact_form('form-contacto')}</div>
      </div>
    </section>

    <section class="section section-paper" aria-labelledby="preguntas">
      <div class="wrap faq-grid">
        <h2 id="preguntas" class="display-lg reveal">Preguntas frecuentes.</h2>
        <div class="faq">{faq_list(FAQ)}</div>
      </div>
    </section>'''
    faq_ld = {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': r}} for q, r in FAQ]}
    page('/contacto/', 'Contacto · Abogados en Lugo | Cendán & Amarelo',
         'Contacte con Cendán & Amarelo Abogados: Avda. de A Coruña 10-14, Lugo. Teléfono y WhatsApp 982 223 053. Primera valoración sin compromiso.',
         main, 'contacto', crumbs, [faq_ld])


def build_legal():
    for slug, (title, desc, body) in LEGAL.items():
        crumbs = [(title, f'/{slug}/')]
        main = f'''{page_hero('Información legal', title, '', crumbs)}

    <section class="section legal"><div class="wrap"><article class="prose">
{body.rstrip()}
    </article></div></section>'''
        page(f'/{slug}/', f'{title} | Cendán & Amarelo Abogados', desc, main, '', crumbs)


def build_404():
    main = f'''{page_hero('Error 404', 'Esta página no existe', 'Es posible que la dirección haya cambiado con la nueva web del despacho.', [('Página no encontrada', '/404.html')])}

    <section class="section"><div class="wrap">{areas_rows()}</div></section>'''
    page('/404.html', 'Página no encontrada | Cendán & Amarelo Abogados', 'La página solicitada no existe.', main, robots='noindex')


def build_sitemap():
    def prio(p):
        return '1.0' if p == '/' else '0.3' if p.strip('/') in LEGAL else '0.9' if p == '/actualidad-juridica/' else '0.8'

    def freq(p):
        return 'daily' if p in ('/', '/actualidad-juridica/') else 'monthly'
    today = (NEWS.get('updated') or UPDATED)[:10]
    urls = ''.join(f'  <url><loc>{DOMAIN}{p}</loc><lastmod>{today if freq(p) == "daily" else UPDATED}</lastmod><changefreq>{freq(p)}</changefreq><priority>{prio(p)}</priority></url>\n'
                   for p in SITEMAP)
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')


def build_agent_files():
    """Navegación agéntica: resumen (llms.txt), texto completo (llms-full.txt) y datos (despacho.json)."""
    areas = '\n'.join(f'- [{a["name"]}]({DOMAIN}/{a["slug"]}/): {a["short"]}' for a in AREAS)
    team = '\n'.join(f'- [{n}]({DOMAIN}/equipo-profesional/{s}/), {r}' for s, n, r in TEAM)
    hist = '\n'.join(f'- {y}: {strip_tags(d)}' for y, _, d in HISTORY)
    llms = f'''# Cendán & Amarelo Abogados

> Despacho de abogados en Lugo (Galicia, España), fundado en 1973 por el letrado Antonio Cendán Corredoira. Asesora a empresas y particulares de Galicia y de toda España, de forma personal e individualizada. Primera valoración sin compromiso.

- Razón social: Cendán & Amarelo Abogados, S.L.P. (NIF B27365667). Registro Mercantil de Lugo, Tomo 385, Folio 42, Hoja LU-12246
- Dirección: Avenida de A Coruña, 10-14, Entresuelo, 27003 Lugo
- Teléfono: +34 982 223 053. WhatsApp: https://wa.me/{WHATSAPP}. Email: {EMAIL}
- Horario: lunes a jueves de 9:00 a 14:30 y de 16:00 a 19:30; viernes de 9:00 a 15:00
- Formulario de contacto: {DOMAIN}/contacto/

## Áreas de práctica
{areas}

## Equipo
{team}

## Trayectoria
{hist}

## Páginas
- [Inicio]({DOMAIN}/)
- [La firma]({DOMAIN}/despacho-abogados-lugo/)
- [Galicia y España]({DOMAIN}/abogados-galicia/)
- [Actualidad jurídica diaria]({DOMAIN}/actualidad-juridica/) (RSS: {DOMAIN}/actualidad-juridica/feed.xml)
- [Guías jurídicas]({DOMAIN}/guias-juridicas/)
- [Contacto y preguntas frecuentes]({DOMAIN}/contacto/)
- [Aviso legal]({DOMAIN}/aviso-legal/)

## Para agentes
- Información completa en texto: {DOMAIN}/llms-full.txt
- Datos estructurados (JSON): {DOMAIN}/despacho.json
'''
    with open(os.path.join(ROOT, 'llms.txt'), 'w', encoding='utf-8') as f:
        f.write(llms)
    lines = ['# Cendán & Amarelo Abogados: información completa', '', llms.split('\n', 2)[2], '']
    for a in AREAS:
        lines += [f'## {a["name"]} ({DOMAIN}/{a["slug"]}/)', a['short']] + [strip_tags(p) for p in a['intro']]
        lines += ['Servicios:'] + [f'- {strip_tags(x)}' for x in a['services']] + [strip_tags(a['note']), '']
    for s, n, r in TEAM:
        lines += [f'## {n} ({r})', strip_tags(LAWYERS[s]['text']), '']
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
    data['areas'] = [{'nombre': a['name'], 'url': f'{DOMAIN}/{a["slug"]}/', 'resumen': a['short'], 'servicios': [strip_tags(x) for x in a['services']]} for a in AREAS]
    data['whatsapp'] = f'https://wa.me/{WHATSAPP}'
    data['contacto'] = DOMAIN + '/contacto/'
    data['actualidad'] = {'url': DOMAIN + '/actualidad-juridica/', 'rss': DOMAIN + '/actualidad-juridica/feed.xml', 'actualizado': NEWS.get('updated')}
    with open(os.path.join(ROOT, 'despacho.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


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
    build_sitemap()
    build_agent_files()
    print(f'{len(SITEMAP)} páginas indexables + 404 generadas')
