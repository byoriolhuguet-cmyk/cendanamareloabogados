/* Cendán & Amarelo Abogados — interacción mínima, sin dependencias */
(function () {
  'use strict';
  var doc = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* Cortina de carga (sólo inicio, primera visita): se retira al terminar */
  var intro = document.querySelector('.intro');
  if (intro) {
    if (!doc.classList.contains('is-intro') || reduce) intro.remove();
    else setTimeout(function () { intro.remove(); }, 2500);
  }

  /* Cabecera: línea inferior al hacer scroll */
  var header = document.querySelector('.site-header');
  var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* Menú móvil */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    var setMenu = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
      nav.classList.toggle('is-open', open);
      document.body.classList.toggle('menu-open', open);
    };
    toggle.addEventListener('click', function () { setMenu(toggle.getAttribute('aria-expanded') !== 'true'); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  }

  /* Revelado progresivo al entrar en pantalla */
  var items = document.querySelectorAll('.reveal, .cta');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* Paralaje de las teselas del hero con el ratón */
  var hero = document.querySelector('.hero');
  if (hero && finePointer && !reduce) {
    var art = hero.querySelector('.hero-tiles');
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      art.style.setProperty('--mx', ((e.clientX - r.left) / r.width - 0.5).toFixed(3));
      art.style.setProperty('--my', ((e.clientY - r.top) / r.height - 0.5).toFixed(3));
    }, { passive: true });
    hero.addEventListener('pointerleave', function () { art.style.setProperty('--mx', 0); art.style.setProperty('--my', 0); });
  }

  /* Cursor: rombo naranja + anillo con inercia */
  if (finePointer && !reduce) {
    var dot = document.createElement('div'), ring = document.createElement('div');
    dot.className = 'cursor-dot'; ring.className = 'cursor-ring';
    dot.setAttribute('aria-hidden', 'true'); ring.setAttribute('aria-hidden', 'true');
    document.body.append(dot, ring);
    doc.classList.add('has-cursor');
    var mx = -100, my = -100, rx = mx, ry = my, raf = 0;
    var loop = function () {
      rx += (mx - rx) * 0.2; ry += (my - ry) * 0.2;
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
    doc.addEventListener('mouseleave', function () { doc.classList.remove('cursor-on'); });
  }

  /* Formulario de contacto: validación y envío por correo (sin servidor) */
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
        status.textContent = 'Revise los campos obligatorios (*) y acepte el aviso legal.';
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
      status.textContent = 'Se abrirá su programa de correo para enviar la consulta. Gracias por su confianza.';
    });
  }

  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
