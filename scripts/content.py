"""Contenido del sitio: áreas, equipo, preguntas frecuentes, navegación y trayectoria."""

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


# Trayectoria del despacho (página La firma)
HISTORY = [
    ('1973', 'Fundación', 'El letrado Antonio Cendán Corredoira abre el despacho en Lugo.'),
    ('1992', 'Cendán &amp; Amarelo', 'Se incorpora Jesús A. Amarelo Fernández y juntos dan forma a la firma actual.'),
    ('2007', 'Sociedad profesional', 'El despacho se constituye como Cendán &amp; Amarelo Abogados, S.L.P.'),
    ('Hoy', 'Seis áreas de práctica', 'Un equipo de cinco abogados que asesora a empresas y particulares en toda Galicia.'),
]

# Cómo trabajamos (inicio y La firma)
METHOD = [
    ('Primera valoración', 'Estudiamos su caso sin compromiso y le explicamos con claridad sus opciones.'),
    ('Estrategia coordinada', 'Los departamentos trabajan juntos para abordar el asunto desde todos sus ángulos.'),
    ('Un letrado responsable', 'Un abogado dirige su asunto de principio a fin y le informa en cada paso.'),
]

# Tres puntos clave por área para la vista "de un vistazo" (inicio y listado de áreas)
KEYS = {
    'penal': ['Derecho penal económico', 'Delitos societarios y fiscales', 'Defensa y acusación particular'],
    'mercantil': ['Sociedades y pactos de socios', 'Contratación mercantil', 'Concurso de acreedores'],
    'tributario': ['Planificación fiscal', 'Inspecciones de Hacienda', 'Recursos y reclamaciones'],
    'civil': ['Familia y divorcios', 'Herencias y testamentos', 'Contratos y reclamaciones'],
    'administrativo': ['Urbanismo y licencias', 'Sanciones administrativas', 'Contratación pública'],
    'laboral': ['Despidos y ERE', 'Convenios colectivos', 'Inspección y Seguridad Social'],
}
