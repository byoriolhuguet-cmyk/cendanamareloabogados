/* Cendán & Amarelo Abogados — interacción mínima (sin dependencias) */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Cortina de carga: se retira del DOM al terminar su animación */
  var intro = document.querySelector('.intro');
  if (intro) {
    if (!doc.classList.contains('is-intro') || reduce) intro.remove();
    else setTimeout(function () { intro.remove(); doc.classList.remove('is-intro'); }, 2600);
  }

  /* Cabecera: fondo al hacer scroll */
  var header = document.querySelector('.site-header');
  var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 24); };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* Cursor elegante: punto + anillo con inercia (sólo ratón, sin movimiento reducido) */
  if (!reduce && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    var dot = document.createElement('div'), ring = document.createElement('div');
    dot.className = 'cursor-dot'; ring.className = 'cursor-ring';
    dot.setAttribute('aria-hidden', 'true'); ring.setAttribute('aria-hidden', 'true');
    document.body.append(dot, ring);
    doc.classList.add('has-cursor');
    var mx = -100, my = -100, rx = mx, ry = my, raf = 0;
    var loop = function () {
      rx += (mx - rx) * 0.18; ry += (my - ry) * 0.18;
      ring.style.transform = 'translate3d(' + rx + 'px,' + ry + 'px,0)';
      raf = (Math.abs(mx - rx) + Math.abs(my - ry) > 0.1) ? requestAnimationFrame(loop) : 0;
    };
    document.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse') return;
      mx = e.clientX; my = e.clientY;
      dot.style.transform = 'translate3d(' + mx + 'px,' + my + 'px,0)';
      doc.classList.add('cursor-on');
      var t = e.target;
      doc.classList.toggle('cursor-text', !!t.closest('input:not([type=checkbox]), textarea, select'));
      doc.classList.toggle('cursor-link', !!t.closest('a, button, summary, label, .member'));
      if (!raf) raf = requestAnimationFrame(loop);
    }, { passive: true });
    document.addEventListener('pointerdown', function () { doc.classList.add('cursor-down'); });
    document.addEventListener('pointerup', function () { doc.classList.remove('cursor-down'); });
    document.documentElement.addEventListener('mouseleave', function () { doc.classList.remove('cursor-on'); });
  }

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
  var items = document.querySelectorAll('.reveal, .section-head');
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
  if (form) {
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
      'Acepta comunicaciones: ' + (d.get('comunicaciones') ? 'sí' : 'no'),
      '',
      d.get('mensaje')
    ].join('\n');
    window.location.href = 'mailto:despacho@cendanamareloabogados.com' +
      '?subject=' + encodeURIComponent('Consulta web · ' + d.get('nombre')) +
      '&body=' + encodeURIComponent(body);
    status.textContent = 'Se abrirá su correo para enviar la consulta. Gracias por su confianza.';
  });
  }

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
