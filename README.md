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

- Sistema visual «Retícula», derivado del logotipo: titulares en Cinzel (capitales romanas de la familia de la Trajan del logotipo), texto en EB Garamond (el «&» naranja del logotipo es una cursiva garamond, y así se repite en el nombre y en los énfasis) y teselas a 45° con el degradado del isotipo.
- Teselas: `tess()` en `scripts/build.py` genera para cada página una composición propia (la semilla es la ruta), apoyada en una línea base como el isotipo sobre el nombre. Aparecen sobre los formularios, en la cabecera de las páginas interiores y en el pie. El rombo se usa también como viñeta, flecha y cursor, y las fotos llevan una esquina cortada a 45°.
- Logotipo: se usa el archivo ORIGINAL (`assets/img/logo-original.png/.webp`, 300x128) sin redibujar ni recolorear, siempre sobre fondo blanco, con anchura fija y altura automática para que nunca se deforme. Para máxima nitidez conviene sustituirlo por la versión vectorial (SVG) cuando el despacho la facilite.
- Cortina de carga (sólo primera visita a la portada): el nombre con la tipografía y la composición del logotipo (capitales romanas, «&» romano naranja, ABOGADOS al 44 %) y una barra fina con una tesela. Dura 1,7 s.
- Diseño «Piedra y luz», versión clara: fondos blancos y gris piedra con una retícula de líneas naranjas a 45°. Portada con el formulario como protagonista y teselas geométricas apoyadas en su borde. Las fotografías (despacho, Muralla de Lugo y empresas) tienen su propio apartado, «El despacho», bajo la presentación de la firma. La frase de la firma se rellena palabra a palabra al hacer scroll y las seis áreas avanzan en un carril horizontal ligado al scroll (en móvil, deslizando). Banda de cifras (los años se calculan solos desde 1973).
- Herramientas de accesibilidad (abajo a la izquierda): tamaño de texto, escala de grises, alto contraste, contraste negativo, fondo claro, subrayar enlaces y fuente legible; se recuerdan en el navegador.
- Navegación agéntica: `llms.txt`, `llms-full.txt`, `despacho.json`, `openapi.json` (acción «solicitar consulta» en `/api/contact`), noticias en JSON Feed (`/actualidad-juridica/noticias.json`) y RSS, acciones `CommunicateAction` en schema.org.
- El CSS minificado se incrusta en cada página (sin petición que bloquee el renderizado): `build.sh` minifica primero y después genera el HTML.
- Foto del despacho (`assets/img/despacho-lugo.*`) en la portada, en «La firma» y en «Contacto».
- Contacto en todas las páginas: botón flotante «Solicitar consulta» (se oculta cuando hay un formulario a la vista), teléfono y formularios en la portada y en el cierre de cada página. El despacho no usa WhatsApp.
- Cursor (sólo ratón): una tesela negra que se abre en un rombo naranja sobre los enlaces y muestra «Ver perfil» o «Ver el área» sobre el equipo y las áreas. Todo el movimiento se desactiva con «reducir movimiento».
- Lighthouse 96–100 (móvil) y 98–100 (escritorio) en rendimiento, accesibilidad, buenas prácticas y SEO (móvil y escritorio).
- Datos estructurados: `LegalService`/`LocalBusiness`, `Service` por área, `FAQPage`, `BreadcrumbList`.
- `vercel.json` / `.htaccess`: caché, cabeceras de seguridad y redirecciones 301 de los perfiles individuales antiguos.
- El formulario envía a `/api/contact` (Vercel + Resend, variables `RESEND_API_KEY`, `CONTACT_TO`, `CONTACT_FROM`); si no está configurado, abre el correo del usuario.

Vista local: `python3 -m http.server` y abrir http://localhost:8000
