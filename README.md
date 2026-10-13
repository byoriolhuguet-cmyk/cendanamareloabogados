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

## Editar

- Textos y estructura: `scripts/build.py` (áreas, equipo, FAQ, plantillas). Legales: `scripts/legal_content.py`.
- Estilos: `css/styles.css`. Interacción: `js/main.js`.
- Después de cualquier cambio: `sh scripts/build.sh` (regenera el HTML, el sitemap, `llms.txt` y los `.min`).

## Detalles técnicos

- Diseño minimalista sobre blanco con los colores del logotipo; isotipo reconstruido en SVG para las animaciones (cortina de carga, entrada del hero con paralaje, bloques de contacto).
- Una sola familia tipográfica (Jost, autoalojada y recortada, 25 KB). Sin cookies ni peticiones a terceros.
- Lighthouse 99–100 en rendimiento, accesibilidad, buenas prácticas y SEO (móvil y escritorio).
- Datos estructurados: `LegalService`/`LocalBusiness`, `Service` por área, `FAQPage`, `BreadcrumbList`.
- `vercel.json` / `.htaccess`: caché, cabeceras de seguridad y redirecciones 301 de los perfiles individuales antiguos.
- El formulario abre el correo del usuario (`mailto:`); para envío directo hace falta un servicio de formularios.

Vista local: `python3 -m http.server` y abrir http://localhost:8000
