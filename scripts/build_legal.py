"""Genera las páginas legales reutilizando cabecera y pie de index.html.

Uso: python3 scripts/build_legal.py .
Ejecutar tras modificar la cabecera o el pie de index.html.
"""
import re, sys, os
root = sys.argv[1]
idx = open(os.path.join(root, 'index.html'), encoding='utf-8').read()

def fix(html):
    # Rutas relativas desde /<pagina>/
    html = re.sub(r'href="#', 'href="../#', html)
    html = html.replace('href="aviso-legal/"', 'href="../aviso-legal/"')
    html = html.replace('href="accesibilidad/"', 'href="../accesibilidad/"')
    html = html.replace('href="politica-de-cookies-ue/"', 'href="../politica-de-cookies-ue/"')
    return html

header = fix(re.search(r'  <!-- ============ CABECERA ============ -->.*?</header>', idx, re.S).group(0))
header = header.replace('href="../#top"', 'href="../"')
footer = fix(re.search(r'  <!-- ============ PIE ============ -->.*?</footer>', idx, re.S).group(0))

PAGES = {}

PAGES['aviso-legal'] = ('Aviso legal', 'Aviso legal, condiciones de uso y política de protección de datos de Cendán & Amarelo Abogados, S.L.P., despacho de abogados en Lugo.', '''
        <p class="updated">Condiciones generales</p>
        <p>En este apartado se encuentran establecidas las condiciones generales de la página. Sugerimos al usuario lea atentamente estas condiciones, recordándole que si utiliza nuestro Sitio Web declara la aceptación plena de todos los apartados vigentes en cada momento en que el usuario acceda a esta página.</p>

        <h2 id="datos-contacto">1. Datos de contacto</h2>
        <table>
          <tbody>
          <tr><th scope="row">Responsable</th><td>CENDAN &amp; AMARELO ABOGADOS, S.L.P.</td></tr>
          <tr><th scope="row">NIF</th><td>B27365667</td></tr>
          <tr><th scope="row">Teléfono</th><td><a href="tel:+34982223053">982&nbsp;223&nbsp;053</a></td></tr>
          <tr><th scope="row">Correo electrónico</th><td><a href="mailto:despacho@cendanamareloabogados.com">despacho@cendanamareloabogados.com</a></td></tr>
          <tr><th scope="row">Dirección postal</th><td>Avenida de La Coruña, 10-14, Entreplanta, 27003, Lugo</td></tr>
          </tbody>
        </table>

        <h2 id="terminos">2. Términos de uso</h2>
        <p>El usuario se compromete a hacer un uso adecuado y lícito del Sitio Web y de sus contenidos, de conformidad con la legislación aplicable, los presentes Términos de Uso, la Política de Privacidad, las buenas costumbres generalmente aceptadas y el orden público.</p>
        <p>Este sitio Web contiene materiales preparados por CENDAN &amp; AMARELO ABOGADOS, S.L.P (en adelante el Abogado/Despacho) con fines únicamente informativos por lo que tales materiales podrían no reflejar el estado legislativo o jurisprudencial más reciente sobre las cuestiones analizadas y no deben ser considerados, bajo ningún concepto, como sustitutivos de asesoramiento legal o de otra naturaleza.</p>
        <p>El acceso a estos materiales no establece ni implica relación alguna entre abogado y cliente, ni cualquier otro tipo de relación de confianza o profesional entre el Abogado/Despacho y el usuario de este sitio Web. Por ello, el usuario no debe actuar sobre la base de la información contenida en la misma sin recurrir previamente al correspondiente asesoramiento profesional.</p>
        <p>Asimismo, el usuario no debe enviar al Abogado/Despacho ningún tipo de información confidencial sin haberlo consultado previamente con alguno de nuestros abogados y haber recibido de los mismos autorización para remitir dicha información. Del mismo modo, estos materiales pueden ser modificados, desarrollados o actualizados sin notificación previa.</p>

        <h2 id="proteccion-datos">3. Política de protección de datos</h2>
        <p>Algunos de los servicios incluidos en este sitio Web exigen la recogida de datos personales que se consideran imprescindibles para la prestación de los mismos por el Abogado/Despacho. Durante el proceso de recogida de los datos, el usuario será informado del carácter necesario de los mismos. Si no se facilitan estos datos obligatorios, no será posible la prestación de tales servicios.</p>
        <p>La información que recibe el Abogado/Despacho de los usuarios de este sitio Web, a través de los diferentes formularios (consultas, contacto o contratación de servicios) es objeto de tratamiento automatizado y se incorporan a los registros de actividad de su titularidad, siendo responsable de dichos tratamientos CENDAN and AMARELO ABOGADOS, S.L.P, con domicilio social en Avenida de La Coruña, 10-14, Entreplanta, 27003, Lugo, teléfono 982223053, fax: 982223947, y CIF: B27365667.</p>
        <p>El Abogado/Despacho tratará los datos de forma confidencial y exclusivamente con el objetivo de gestionar la relación con sus clientes, socios, franquiciados y promocionar las actividades de la Firma.</p>
        <p>El envío de correos electrónicos o la cumplimentación de formularios incluidos en el presente sitio Web implica el consentimiento expreso a la inclusión de sus datos de carácter personal en los tratamientos referidos anteriormente y, si así lo autorizase expresamente, su consentimiento a que sus datos sean utilizados para el envío de comunicaciones comerciales por correo electrónico o por cualquier otro medio. Estos consentimientos se solicitarán, explícitamente, mediante la habilitación de los checkbox correspondientes antes de que pueda enviar los datos en cada formulario.</p>
        <h3>Ejercicio de derechos</h3>
        <p>En relación con los datos recabados en la forma prevista en los apartados anteriores, el usuario podrá ejercitar los derechos reconocidos por la ley y, en particular, los derechos de acceso, rectificación o cancelación de datos, portabilidad, limitación, bloqueo y oposición, si resultase pertinente, así como el derecho de revocar el consentimiento prestado para la cesión de sus datos en cualquier momento.</p>
        <p>Tales derechos podrán ser ejercitados por el usuario o, en su caso, por quien lo represente, mediante solicitud escrita y firmada, dirigida a la siguiente dirección: Avenida de La Coruña, 10-14, Entreplanta, 27003, Lugo, o bien mediante correo electrónico a la cuenta <a href="mailto:despacho@cendanamareloabogados.com">despacho@cendanamareloabogados.com</a>. La solicitud referida anteriormente deberá contener los siguientes datos:</p>
        <ul>
          <li>Nombre y apellidos del usuario</li>
          <li>Domicilio a efectos de notificaciones</li>
          <li>Fotocopia del Documento Nacional de Identidad o pasaporte</li>
          <li>Contenido concreto del derecho ejercitado</li>
        </ul>
        <h3>Conservación y seguridad</h3>
        <p>El Abogado/Despacho guardará los datos de carácter personal que haya recabado durante los plazos necesarios para el cumplimiento de la relación contractual o durante los plazos legalmente obligatorios, y adoptará las medidas necesarias para evitar su alteración, pérdida, tratamiento o acceso no autorizados. El Abogado/Despacho cumplirá estos deberes de acuerdo con lo establecido por la normativa aplicable.</p>
        <p>No se contempla la realización de transferencias internacionales de datos a terceros países, ni la existencia de decisiones automatizadas o elaboración de perfiles, ni tampoco la cesión de sus datos a terceros más allá de las cesiones obligadas por la legislación vigente.</p>
        <p><strong>Uso de cookies.</strong> Esta web utiliza cookies en los términos establecidos en nuestra <a href="../politica-de-cookies-ue/">política de cookies</a>.</p>
        <p>Todos los datos facilitados, con independencia de su carácter, están protegidos por el deber de confidencialidad del abogado.</p>

        <h2 id="aviso-legal">4. Aviso legal</h2>
        <p>La página web pertenece a CENDAN &amp; AMARELO ABOGADOS, S.L.P, con NIF nº B27365667 y domicilio en Avenida de La Coruña, 10-14, Entreplanta, 27003, Lugo, inscrita en el Registro Mercantil de Lugo con los siguientes datos de inscripción: Tomo 385 · Libro 0 · Folio 42 · Hoja LU-12246 · Inscripción 2ª, dirección de correo electrónico: <a href="mailto:despacho@cendanamareloabogados.com">despacho@cendanamareloabogados.com</a> y teléfono de contacto: 982223053.</p>
        <p>Los servicios que se prestan a través de esta web se realizan a través de profesionales, Abogados, con el título académico de licenciados en derecho:</p>
        <ul>
          <li>D. Jesús A. Amarelo Fernández, colegiado 864 del Ilustre Colegio de Abogados de Lugo</li>
          <li>D. Francisco González González, colegiado 1.625 del Ilustre Colegio de Abogados de Lugo</li>
          <li>Dña. Ana Belén Rey Vázquez, colegiada 2.062 del Ilustre Colegio de Abogados de Lugo</li>
          <li>D. José Manuel López Fernández, colegiado 2.219 del Ilustre Colegio de Abogados de Lugo</li>
        </ul>
        <p>Las normas profesionales aplicables al ejercicio de la Abogacía están contenidas en el Estatuto General de la Abogacía Española, aprobado por el Real Decreto 135/2021, de 2 de marzo (Boletín Oficial del Estado nº 71, de 24 de marzo de 2021), donde puede ser consultado. También puede serlo en Internet en la página del Boletín Oficial del Estado (<a href="https://www.boe.es/" rel="noopener" target="_blank">www.boe.es</a>) y alternativamente en la del Consejo General de la Abogacía Española (<a href="http://www.cge.es/" rel="noopener" target="_blank">www.cge.es</a>). También el Código Deontológico de la Abogacía Española, aprobado por el Pleno del C.G.A.E. y que puede ser visualizado en su web (<a href="http://www.cgae.es/" rel="noopener" target="_blank">www.cgae.es</a>).</p>
        <p>El propietario del dominio referenciado le informa que la finalidad de la Página Web es publicitaria e informativa; asimismo, se ofrece la posibilidad de contactar o solicitar información más detallada de los servicios del despacho.</p>
        <p>Los datos personales que usted nos facilite quedarán incorporados y serán tratados en los Registros de tratamiento del despacho, titularidad de CENDAN and AMARELO ABOGADOS, S.L.P con la finalidad de poder gestionar su solicitud, así como para mantenerle informado de futuras promociones, noticias y novedades relacionadas con la actividad vía correo electrónico, fax, sms, o cualquier otro medio electrónico o físico, presente o futuro, salvo que no contemos con su consentimiento expreso a tal efecto. El Abogado/Despacho se compromete a no ceder ni utilizar dichos datos más que para los fines para los que han sido recabados.</p>

        <h2 id="responsabilidad">5. Limitación de la responsabilidad</h2>
        <p>El Abogado/Despacho no se responsabiliza de los posibles errores u omisiones que pudieran existir en los contenidos de este sitio. A su vez, estos contenidos pueden ser modificados, desarrollados o actualizados sin notificación previa.</p>
        <p>Este Sitio Web puede contener vínculos a otras páginas de Internet y lo hace en la creencia de buena fe de que tales contenidos cumplen con la ley. Esto no significa que el Abogado/Despacho apruebe o recomiende los contenidos de los mismos. Si el usuario accede a ellos, lo hace bajo su responsabilidad. El Abogado/Despacho no asume garantías sobre la veracidad, exactitud o actualización de los contenidos, servicios, textos, gráficos y vínculos de tales sitios.</p>
        <p>El Abogado/Despacho tampoco se hace responsable de los daños informáticos o de otro tipo que pudiera ocasionar al visitante el acceso a los contenidos de este sitio. Por ello no garantiza la ausencia de virus u otros elementos lesivos que pudieran causar daños o alteraciones en el sistema informático o en los correos electrónicos.</p>
        <p>La violación de la seguridad del sistema o red puede conllevar responsabilidades civiles o penales. El Abogado/Despacho se reserva el derecho a investigar las posibles violaciones de seguridad a este Sitio Web o, a instancia de las autoridades competentes, podrá contribuir en la investigación de posibles violaciones.</p>
''')

PAGES['politica-de-cookies-ue'] = ('Política de cookies', 'Política de cookies de la web de Cendán & Amarelo Abogados: qué tecnologías de almacenamiento utiliza el sitio y cómo gestionarlas.', '''
        <p class="updated">Última actualización: 13 de octubre de 2026</p>
        <p>En cumplimiento del artículo 22.2 de la Ley 34/2002, de servicios de la sociedad de la información y de comercio electrónico (LSSI), y del Reglamento (UE) 2016/679 (RGPD), CENDAN &amp; AMARELO ABOGADOS, S.L.P. informa al usuario sobre el uso de cookies y tecnologías similares en este sitio web.</p>

        <h2 id="que-son">1. ¿Qué son las cookies?</h2>
        <p>Las cookies son pequeños archivos que un sitio web almacena en el navegador del usuario cuando lo visita. Existen otras tecnologías de funcionamiento similar, como el almacenamiento local del navegador (<i>localStorage</i> o <i>sessionStorage</i>), a las que se aplica esta misma política.</p>

        <h2 id="que-usamos">2. Cookies que utiliza este sitio</h2>
        <p>Esta web <strong>no instala cookies propias ni de terceros</strong> con fines analíticos, publicitarios o de seguimiento. No utilizamos herramientas de analítica, píxeles de redes sociales ni contenidos incrustados de terceros. Las tipografías se sirven desde nuestro propio servidor, por lo que no se envían datos a proveedores externos al cargar la página.</p>
        <p>Únicamente se emplea el siguiente elemento técnico, estrictamente necesario y exento de consentimiento conforme al artículo 22.2 de la LSSI:</p>
        <table>
          <thead><tr><th scope="col">Nombre</th><th scope="col">Tipo</th><th scope="col">Finalidad</th><th scope="col">Duración</th></tr></thead>
          <tbody><tr><td>ca-intro</td><td>Propia · técnica (<i>sessionStorage</i>)</td><td>Recordar que la animación de bienvenida ya se mostró, para no repetirla en cada página.</td><td>Hasta cerrar la pestaña</td></tr></tbody>
        </table>
        <p>Este elemento no contiene datos personales ni permite identificar al usuario. Por este motivo, la web no muestra un aviso de consentimiento de cookies.</p>

        <h2 id="terceros">3. Enlaces a sitios de terceros</h2>
        <p>La web contiene enlaces a servicios externos (Facebook, X/Twitter, Google Maps e Iberley). Al pulsarlos, el usuario abandona este sitio y dichos servicios pueden instalar sus propias cookies, de las que son responsables con arreglo a sus respectivas políticas:</p>
        <ul>
          <li>Meta (Facebook): <a href="https://www.facebook.com/policies/cookies/" rel="noopener" target="_blank">facebook.com/policies/cookies</a></li>
          <li>X (Twitter): <a href="https://help.x.com/es/rules-and-policies/x-cookies" rel="noopener" target="_blank">help.x.com</a></li>
          <li>Google: <a href="https://policies.google.com/technologies/cookies?hl=es" rel="noopener" target="_blank">policies.google.com</a></li>
          <li>Iberley: <a href="https://www.iberley.es/" rel="noopener" target="_blank">iberley.es</a></li>
        </ul>

        <h2 id="gestion">4. Cómo gestionar o eliminar las cookies</h2>
        <p>El usuario puede permitir, bloquear o eliminar las cookies y el almacenamiento local desde la configuración de su navegador:</p>
        <ul>
          <li><a href="https://support.google.com/chrome/answer/95647?hl=es" rel="noopener" target="_blank">Google Chrome</a></li>
          <li><a href="https://support.mozilla.org/es/kb/Borrar%20cookies" rel="noopener" target="_blank">Mozilla Firefox</a></li>
          <li><a href="https://support.apple.com/es-es/guide/safari/sfri11471/mac" rel="noopener" target="_blank">Safari</a></li>
          <li><a href="https://support.microsoft.com/es-es/microsoft-edge" rel="noopener" target="_blank">Microsoft Edge</a></li>
        </ul>
        <p>Bloquear el elemento técnico descrito no impide navegar por la web; únicamente hará que la animación de bienvenida pueda mostrarse de nuevo.</p>

        <h2 id="cambios">5. Cambios en esta política</h2>
        <p>Si en el futuro se incorporan nuevas cookies (por ejemplo, de analítica), esta política se actualizará y, cuando la ley lo exija, se solicitará el consentimiento previo del usuario antes de instalarlas. Para cualquier consulta puede escribir a <a href="mailto:despacho@cendanamareloabogados.com">despacho@cendanamareloabogados.com</a>.</p>
''')

PAGES['accesibilidad'] = ('Accesibilidad', 'Declaración de accesibilidad de la web de Cendán & Amarelo Abogados: nivel de conformidad, medidas adoptadas y canal de comunicación.', '''
        <p class="updated">Declaración elaborada el 13 de octubre de 2026</p>
        <p>CENDAN &amp; AMARELO ABOGADOS, S.L.P. se compromete a que su sitio web sea accesible para todas las personas, con independencia de su capacidad o de la tecnología que utilicen. Esta declaración se aplica al sitio www.cendanamareloabogados.com.</p>

        <h2 id="conformidad">1. Nivel de conformidad</h2>
        <p>El sitio se ha diseñado y desarrollado con el objetivo de cumplir el nivel <strong>AA</strong> de las Pautas de Accesibilidad para el Contenido Web (<a href="https://www.w3.org/TR/WCAG22/" rel="noopener" target="_blank">WCAG 2.2</a>) del W3C y la norma europea EN 301 549. La conformidad se ha valorado mediante una autoevaluación realizada por el propio despacho y sus desarrolladores.</p>

        <h2 id="medidas">2. Medidas adoptadas</h2>
        <ul>
          <li>Estructura semántica con encabezados jerárquicos, regiones (cabecera, navegación, contenido principal y pie) y enlace para saltar al contenido.</li>
          <li>Navegación completa con teclado y foco visible en todos los elementos interactivos.</li>
          <li>Contraste de color mínimo de 4,5:1 en los textos.</li>
          <li>Áreas táctiles de al menos 44 × 44 píxeles en dispositivos móviles.</li>
          <li>Textos alternativos en todas las fotografías.</li>
          <li>Formularios con etiquetas asociadas, campos obligatorios señalados y mensajes de estado anunciados a los lectores de pantalla.</li>
          <li>Respeto de la preferencia de movimiento reducido del sistema: con ella activa se desactivan las animaciones y el cursor decorativo.</li>
          <li>Diseño adaptable que permite ampliar el texto hasta el 200 % sin pérdida de contenido.</li>
          <li>Idioma de la página declarado para una correcta lectura por síntesis de voz.</li>
        </ul>

        <h2 id="limitaciones">3. Contenido no accesible</h2>
        <p>No se tiene constancia de contenidos que incumplan los requisitos indicados. Los sitios de terceros enlazados desde esta web (redes sociales, mapas o noticias) quedan fuera del alcance de esta declaración.</p>

        <h2 id="contacto">4. Comunicaciones y sugerencias</h2>
        <p>Si encuentra alguna barrera de accesibilidad o necesita la información de esta web en otro formato, puede comunicarlo por cualquiera de estos medios. Le responderemos en el menor plazo posible.</p>
        <ul>
          <li>Teléfono: <a href="tel:+34982223053">982&nbsp;223&nbsp;053</a></li>
          <li>Correo electrónico: <a href="mailto:despacho@cendanamareloabogados.com">despacho@cendanamareloabogados.com</a></li>
          <li>Presencialmente: Avda. de A Coruña 10-14, Entlo. 27003 Lugo</li>
        </ul>

        <h2 id="revision">5. Revisión</h2>
        <p>Esta declaración se revisará cada vez que se introduzcan cambios relevantes en el sitio y, en todo caso, una vez al año.</p>
''')

head_tpl = '''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title} · Cendán &amp; Amarelo Abogados</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://www.cendanamareloabogados.com/{slug}/">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#121211">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="../apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_ES">
  <meta property="og:site_name" content="Cendán &amp; Amarelo Abogados">
  <meta property="og:title" content="{title} · Cendán &amp; Amarelo Abogados">
  <meta property="og:url" content="https://www.cendanamareloabogados.com/{slug}/">
  <meta property="og:image" content="https://www.cendanamareloabogados.com/assets/img/og-cendan-amarelo.jpg">
  <link rel="preload" href="../assets/fonts/cormorant-garamond.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="../assets/fonts/jost.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="../css/styles.min.css">
  <script>document.documentElement.classList.add('js')</script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Inicio","item":"https://www.cendanamareloabogados.com/"}},{{"@type":"ListItem","position":2,"name":"{title}","item":"https://www.cendanamareloabogados.com/{slug}/"}}]}}
  </script>
</head>

<body class="page-legal">
  <div class="progress" aria-hidden="true"></div>
  <a class="skip" href="#contenido">Saltar al contenido</a>

{header}

  <main id="contenido" class="legal">
    <article class="wrap">
      <a class="back" href="../">← Volver al inicio</a>
      <h1>{title}</h1>
{body}
    </article>
  </main>

{footer}

  <script src="../js/main.min.js" defer></script>
</body>
</html>
'''
for slug, (title, desc, body) in PAGES.items():
    os.makedirs(os.path.join(root, slug), exist_ok=True)
    html = head_tpl.format(title=title, desc=desc.replace('&', '&amp;'), slug=slug, header=header, footer=footer, body=body.rstrip())
    open(os.path.join(root, slug, 'index.html'), 'w', encoding='utf-8').write(html)
    print('ok', slug)
