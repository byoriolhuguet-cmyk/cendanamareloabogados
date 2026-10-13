/* Cendán & Amarelo Abogados — interacción mínima (sin dependencias) */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');

  /* Cabecera: fondo al hacer scroll */
  var header = document.querySelector('.site-header');
  var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 24); };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* Menú móvil */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  var setMenu = function (open) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    nav.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
    if (open) header.classList.add('is-scrolled'); else onScroll();
  };
  toggle.addEventListener('click', function () { setMenu(toggle.getAttribute('aria-expanded') !== 'true'); });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  /* Revelado progresivo */
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* Formulario: validación y envío por correo (sin backend) */
  var form = document.getElementById('form');
  var status = form.querySelector('.form-status');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var invalid = Array.prototype.filter.call(form.elements, function (f) {
      var bad = f.willValidate && !f.checkValidity();
      f.classList.toggle('is-invalid', bad);
      return bad;
    });
    if (invalid.length) {
      status.textContent = 'Revise los campos marcados y acepte la política de privacidad.';
      invalid[0].focus();
      return;
    }
    var d = new FormData(form);
    var body = [
      'Nombre: ' + d.get('nombre'),
      'Email: ' + d.get('email'),
      'Teléfono: ' + (d.get('telefono') || '-'),
      'Área: ' + (d.get('area') || '-'),
      '',
      d.get('mensaje')
    ].join('\n');
    window.location.href = 'mailto:despacho@cendanamareloabogados.com' +
      '?subject=' + encodeURIComponent('Consulta web · ' + d.get('nombre')) +
      '&body=' + encodeURIComponent(body);
    status.textContent = 'Se abrirá su correo para enviar la consulta. Gracias por su confianza.';
  });

  document.getElementById('year').textContent = new Date().getFullYear();
})();
