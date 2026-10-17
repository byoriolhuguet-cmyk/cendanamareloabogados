# Cendán & Amarelo Abogados — web

Sitio estático generado con un script de Python (sin dependencias de ejecución). Se publica tal cual en Vercel o en cualquier hosting.

## Páginas (mantienen las URL de la web anterior)

| URL | Página |
|---|---|
| `/` | Inicio |
| `/despacho-abogados-lugo/` | La firma |
| `/areas-de-practica/` | Áreas de práctica |
| `/abogados-derecho-penal-lugo/` … `/abogados-derecho-laboral-lugo/` | Una página por área (6) |
| `/equipo-profesional/` | Equipo |
| `/actualidad-juridica/` | Actualidad |
| `/contacto/` | Contacto, formulario y preguntas frecuentes |
| `/aviso-legal/`, `/politica-de-cookies-ue/`, `/accesibilidad/` | Legales |

## Actualidad jurídica automática (diaria)

- `.github/workflows/noticias.yml` se ejecuta cada día a las 05:17 UTC (y a mano desde la pestaña Actions).
- `scripts/news.py` descarga RSS de fuentes jurídicas de España y Galicia, puntúa la importancia de cada noticia y guarda en `data/news.json` sólo titular, fuente, fecha, enlace, área y puntuación (no copia el cuerpo de las noticias).
- La web muestra "Hoy" (las seis más importantes) y un archivo de dos semanas filtrable por área.
- Fuentes y criterios: listas `FEEDS` y `WEIGHTS` en `scripts/news.py`.

## Formulario de contacto

- Está en el hero, al final de cada página y en /contacto/. Envía a `api/contact.js` (función de Vercel con Resend).
- Para activarlo: en Vercel, Settings > Environment Variables, añadir `RESEND_API_KEY` (y opcionalmente `CONTACT_TO`, `CONTACT_FROM`). Sin clave, el formulario abre el correo del usuario.

## Navegación agéntica y SEO

- `llms.txt` (resumen), `llms-full.txt` (todo el contenido en texto), `despacho.json` (datos estructurados), `actualidad-juridica/feed.xml` (RSS).
- `robots.txt` permite explícitamente a los rastreadores de IA.
- Guías propias en `/guias-juridicas/` (contenido en `scripts/content.py`, revisar por un letrado) y página `/abogados-galicia/` para posicionar en Galicia y España.

## Editar

- Textos: `scripts/content.py` (áreas, equipo, FAQ, trayectoria, método). Legales: `scripts/legal_content.py`.
- Plantillas: `scripts/build.py`. Iconos: `scripts/icons.py` (Phosphor, MIT; Simple Icons, CC0).
- Estilos: `css/styles.css`. Interacción: `js/main.js`.
- Después de cualquier cambio: `sh scripts/build.sh` (regenera el HTML, el sitemap, `llms.txt` y los `.min`).

## Detalles técnicos

- Diseño minimalista sobre blanco con los colores del logotipo. El isotipo está reconstruido en SVG con la geometría exacta del logotipo y sólo se anima por opacidad (nunca se gira ni se escala), para no deformarlo.
- Contacto en todas las páginas: botón «Solicitar consulta», teléfono, WhatsApp flotante y tarjeta lateral fija en las áreas. El número de WhatsApp se cambia en `WHATSAPP` dentro de `scripts/build.py`.
- Tipografía: Bodoni Moda (titulares) y Hanken Grotesk (texto), autoalojadas y recortadas. Sin cookies ni peticiones a terceros.
- Concepto "Noche en Lugo": portada y cierre en negro cálido, cuerpo marfil y el naranja del logotipo como único acento. Sobre fondo oscuro el logotipo se compone con el isotipo vectorial y las letras en marfil, con las proporciones exactas del original.
- Lighthouse 99–100 en rendimiento, accesibilidad, buenas prácticas y SEO (móvil y escritorio).
- Datos estructurados: `LegalService`/`LocalBusiness`, `Service` por área, `FAQPage`, `BreadcrumbList`.
- `vercel.json` / `.htaccess`: caché, cabeceras de seguridad y redirecciones 301 de los perfiles individuales antiguos.
- El formulario abre el correo del usuario (`mailto:`); para envío directo hace falta un servicio de formularios.

Vista local: `python3 -m http.server` y abrir http://localhost:8000
