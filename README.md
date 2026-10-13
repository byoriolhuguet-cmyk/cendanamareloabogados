# Cendán & Amarelo Abogados — web

Sitio estático, sin dependencias ni build. Se sube tal cual a cualquier hosting.

```
index.html                    Inicio (una sola página con anclas)
aviso-legal/                  Aviso legal y protección de datos
politica-de-cookies-ue/       Política de cookies
accesibilidad/                Declaración de accesibilidad
css/styles.css                Estilos (mobile-first)
js/main.js                    Menú, cursor, cortina de carga, revelados, formulario
assets/fonts/                 Cormorant Garamond y Jost autoalojadas (licencia OFL)
assets/img/equipo/            Retratos del equipo (WebP + JPG)
.htaccess                     Compresión, caché y cabeceras (Apache)
robots.txt · sitemap.xml · llms.txt
```

- Lighthouse móvil: 100 / 100 / 100 / 100 (rendimiento, accesibilidad, buenas prácticas, SEO).
- Sin cookies ni peticiones a terceros: las fuentes se sirven desde el propio dominio.
- Animaciones: cortina de carga en la primera visita de la sesión, entrada escalonada, revelado de fotos, líneas que se dibujan, barra de progreso de lectura, transiciones entre páginas (View Transitions) y cursor personalizado en dispositivos con ratón. Todo se desactiva con "reducir movimiento".
- El formulario abre el correo del usuario (`mailto:`). Para envío directo, conectar a un backend o servicio de formularios.
- Las páginas legales comparten cabecera y pie con `index.html`; si se cambian allí, hay que copiarlos también en las tres subpáginas.

Vista local: `python3 -m http.server` y abrir http://localhost:8000
