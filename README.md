# Cendán & Amarelo Abogados — web

Sitio estático, sin dependencias ni build: `index.html`, `css/styles.css`, `js/main.js`.

- Mobile-first (360–430px), sin imágenes: monograma SVG, tipografía (Cormorant Garamond + Jost) y retícula.
- SEO local: H1/H2/H3 estrictos, JSON-LD `LegalService` + `LocalBusiness`, `Person`, `FAQPage`; `robots.txt`, `sitemap.xml`, `llms.txt` para motores de respuesta.
- El formulario abre el correo del usuario (`mailto:`). Para envío directo, conectar a un backend o servicio de formularios.

Vista local: `python3 -m http.server` y abrir http://localhost:8000

Pendiente: migrar las páginas `/aviso-legal/`, `/accesibilidad/` y `/politica-de-cookies-ue/` (el sitio enlaza a ellas); confirmar el horario; completar las listas de servicios de penal, mercantil, tributario, civil y administrativo con el texto de cada página de área (solo laboral es literal).
