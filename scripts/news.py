"""Recolector de actualidad jurídica para Cendán & Amarelo Abogados.

Lo ejecuta GitHub Actions cada dos días (.github/workflows/noticias.yml):
  1. descarga los RSS/Atom de fuentes jurídicas de España y de Galicia,
  2. guarda en data/news.json titular, fuente, fecha, enlace y área (sin copiar el
     cuerpo de las noticias: sólo se enlaza a la fuente original),
  3. después build.py regenera /actualidad-juridica/, su feed RSS y los bloques
     de noticias de cada área.

Sólo usa la biblioteca estándar de Python. Uso: python3 scripts/news.py
"""
import email.utils
import html
import json
import os
import re
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'data', 'news.json')
MAX_ITEMS = 60          # noticias que se conservan
MAX_AGE_DAYS = 30       # antigüedad máxima
PER_FEED = 15           # máximo por fuente y ejecución

# Fuentes: (nombre visible, URL, ámbito). Si una falla, se ignora y el resto sigue.
GN = 'https://news.google.com/rss/search?hl=es&gl=ES&ceid=ES:es&q='
FEEDS = [
    ('Confilegal', 'https://confilegal.com/feed/', 'españa'),
    ('Noticias Jurídicas', 'https://noticias.juridicas.com/rss/', 'españa'),
    ('Iberley', 'https://www.iberley.es/rss/noticias', 'españa'),
    ('Legal Today', 'https://www.legaltoday.com/feed/', 'españa'),
    ('Economist & Jurist', 'https://www.economistjurist.es/feed/', 'españa'),
    ('Lawyerpress', 'https://www.lawyerpress.com/feed/', 'españa'),
    ('Galicia', GN + '%22Tribunal+Superior+de+Xustiza+de+Galicia%22+OR+TSXG', 'galicia'),
    ('Galicia', GN + 'abogados+Galicia+sentencia+OR+juzgado', 'galicia'),
    ('Lugo', GN + 'juzgado+Lugo+OR+%22Audiencia+Provincial+de+Lugo%22', 'galicia'),
]

# Clasificación por área (palabras clave sin tildes, en minúsculas)
AREAS = {
    'penal': ['penal', 'delito', 'fiscalia', 'condena', 'prision', 'estafa', 'blanqueo', 'compliance', 'imputad', 'investigad', 'fraude', 'mulero', 'ciberdelinc', 'juicio oral'],
    'mercantil': ['mercantil', 'concurso', 'concursal', 'sociedad', 'societari', 'insolvencia', 'acreedores', 'empresa', 'administradores'],
    'tributario': ['hacienda', 'tributari', 'fiscal', 'irpf', 'iva', 'impuesto', 'aeat', 'dgt', 'teac', 'sucesiones'],
    'civil': ['civil', 'herencia', 'divorcio', 'custodia', 'arrendamiento', 'alquiler', 'hipoteca', 'consumidor', 'familia', 'testamento', 'indemnizacion', 'vivienda', 'banco', 'clausula'],
    'administrativo': ['administrativ', 'contencioso', 'urbanismo', 'licencia', 'contratacion publica', 'sancion', 'funcion publica', 'expropiacion'],
    'laboral': ['laboral', 'despid', 'finiquito', 'trabajador', 'seguridad social', 'convenio', ' erte', 'jornada', 'salari', 'pension', 'incapacidad', 'vacaciones', 'sindicat', 'inspeccion de trabajo'],
}
GALICIA_WORDS = ['galicia', 'galleg', 'xunta', 'tsxg', 'lugo', 'coruna', 'santiago', 'ourense', 'pontevedra', 'vigo', 'ferrol', 'monforte']


def norm(s):
    s = unicodedata.normalize('NFKD', s.lower())
    return ''.join(c for c in s if not unicodedata.combining(c))


def clean(text):
    text = html.unescape(re.sub(r'<[^>]+>', ' ', text or ''))
    return re.sub(r'\s+', ' ', text).strip()


def parse_date(s):
    if not s:
        return None
    try:
        d = email.utils.parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(s.strip().replace('Z', '+00:00'))
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; CendanAmareloNews/1.0; +https://www.cendanamareloabogados.com)'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def items_from(xml_bytes):
    root = ET.fromstring(xml_bytes)
    atom = '{http://www.w3.org/2005/Atom}'
    if root.tag == atom + 'feed':
        for e in root.findall(atom + 'entry'):
            link = e.find(atom + 'link')
            yield (e.findtext(atom + 'title'), link.get('href') if link is not None else '',
                   e.findtext(atom + 'updated') or e.findtext(atom + 'published'), None)
    else:
        for e in root.iter('item'):
            src = e.find('source')
            yield (e.findtext('title'), e.findtext('link'), e.findtext('pubDate') or e.findtext('{http://purl.org/dc/elements/1.1/}date'),
                   src.text if src is not None else None)


def classify(title):
    t = norm(title)
    for area, words in AREAS.items():
        if any(w in t for w in words):
            return area
    return 'general'


def main():
    now = datetime.now(timezone.utc)
    old = []
    if os.path.exists(OUT):
        with open(OUT, encoding='utf-8') as f:
            old = json.load(f).get('items', [])
    seen = {norm(i['title']) for i in old}
    fresh, ok = [], 0
    for name, url, scope in FEEDS:
        try:
            data = fetch(url)
            n = 0
            for title, link, date, src in items_from(data):
                title = clean(title)
                link = (link or '').strip()
                if not title or not link.startswith('http'):
                    continue
                source = name
                # Google News añade " - Medio" al titular: lo separamos como fuente
                if 'news.google.com' in url:
                    m = re.match(r'^(.*)\s+-\s+([^-]{2,60})$', title)
                    if m:
                        title, source = m.group(1).strip(), m.group(2).strip()
                    elif src:
                        source = clean(src)
                key = norm(title)
                if key in seen:
                    continue
                d = parse_date(date) or now
                if d < now - timedelta(days=MAX_AGE_DAYS):
                    continue
                seen.add(key)
                t = norm(title)
                fresh.append({
                    'title': title[:220], 'url': link, 'source': source[:60],
                    'date': d.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'area': classify(title),
                    'scope': 'galicia' if scope == 'galicia' or any(w in t for w in GALICIA_WORDS) else 'españa',
                })
                n += 1
                if n >= PER_FEED:
                    break
            ok += 1
            print(f'ok   {name}: {n}')
        except Exception as exc:  # una fuente caída no detiene el resto
            print(f'fallo {name}: {exc}', file=sys.stderr)
    for i in old:
        i['area'] = classify(i['title'])
    items = [i for i in fresh + old if parse_date(i['date']) and parse_date(i['date']) >= now - timedelta(days=MAX_AGE_DAYS)]
    items.sort(key=lambda i: i['date'], reverse=True)
    items = items[:MAX_ITEMS]
    if ok == 0 and old:
        print('Ninguna fuente respondió; se conservan las noticias anteriores.')
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump({'updated': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'items': items}, f, ensure_ascii=False, indent=1)
    print(f'{len(items)} noticias guardadas ({len(fresh)} nuevas)')


if __name__ == '__main__':
    main()
