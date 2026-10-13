# Cendán & Amarelo Abogados — web

Sitio estático, sin dependencias ni build. Se sube tal cual a cualquier hosting.

```
index.html                    Inicio (una sola página con anclas)
aviso-legal/                  Aviso legal y protección de datos
politica-de-cookies-ue/       Política de cookies
accesibilidad/                Declaración de accesibilidad
404.html                      Página de error
css/styles.css → .min.css     Estilos (mobile-first); se sirve la versión minificada
js/main.js → .min.js          Menú, cursor, cortina de carga, revelados, formulario
scripts/build.sh              Regenera los .min y las páginas legales
scripts/build_legal.py        Genera las páginas legales con la cabecera y el pie de index.html
assets/fonts/                 Cormorant Garamond y Jost autoalojadas (licencia OFL)
assets/img/equipo/            Retratos del equipo (WebP + JPG)
vercel.json                   Caché, cabeceras de seguridad y redirecciones 301 (Vercel)
.htaccess                     Lo mismo para hosting Apache
site.webmanifest · apple-touch-icon.png · assets/img/og-*.jpg (imagen para redes)
robots.txt · sitemap.xml · llms.txt
```

- Lighthouse móvil: 100 / 100 / 100 / 100 (rendimiento, accesibilidad, buenas prácticas, SEO).
- Sin cookies ni peticiones a terceros: las fuentes se sirven desde el propio dominio.
- Animaciones: cortina de carga en la primera visita de la sesión, entrada escalonada, revelado de fotos, líneas que se dibujan, barra de progreso de lectura, transiciones entre páginas (View Transitions) y cursor personalizado en dispositivos con ratón. Todo se desactiva con "reducir movimiento".
- El formulario abre el correo del usuario (`mailto:`). Para envío directo, conectar a un backend o servicio de formularios.
- Tras editar `css/styles.css`, `js/main.js` o la cabecera/pie de `index.html`, ejecutar `sh scripts/build.sh`.
- Las URL de la web anterior (`/despacho-abogados-lugo/`, `/abogados-derecho-penal-lugo/`, `/equipo-profesional/...`, `/contacto/`…) redirigen con 301 a su sección para conservar el posicionamiento.
- Fuentes recortadas al subconjunto latino (70 KB en total) con `pyftsubset`.

Vista local: `python3 -m http.server` y abrir http://localhost:8000
