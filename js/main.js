/* Cendán & Amarelo Abogados: interacción mínima, sin dependencias ni escuchas de scroll */
(function () {
  'use strict';
  var doc = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var hasIO = 'IntersectionObserver' in window;

  /* Cortina de carga (sólo inicio, primera visita): se retira al terminar */
  var intro = document.querySelector('.intro');
  if (intro) {
    if (!doc.classList.contains('is-intro') || reduce) intro.remove();
    else setTimeout(function () { intro.remove(); }, 2400);
  }

  /* Cabecera: sombra al salir de la parte superior (IntersectionObserver, sin escuchar el scroll) */
  var header = document.querySelector('.site-header');
  var sentinel = document.querySelector('.top-sentinel');
  if (header && sentinel && hasIO) {
    new IntersectionObserver(function (e) { header.classList.toggle('is-scrolled', !e[0].isIntersecting); }).observe(sentinel);
  }

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
    window.matchMedia('(min-width: 1024px)').addEventListener('change', function (m) { if (m.matches) setMenu(false); });
  }


  /* Titulares palabra a palabra: sólo h2 de texto plano (el texto sigue siendo legible para lectores de pantalla) */
  if (!reduce) {
    document.querySelectorAll('h2.reveal').forEach(function (h) {
      if (h.children.length || h.classList.contains('statement')) return;
      var words = h.textContent.trim().split(/\s+/);
      h.setAttribute('aria-label', h.textContent.trim());
      h.innerHTML = words.map(function (w, i) {
        return '<span class="w" aria-hidden="true"><span style="--wi:' + i + '">' + w + '</span></span>';
      }).join(' ');
      h.classList.add('split');
    });
  }

  /* Cifras: cuentan hasta su valor al entrar en pantalla */
  var countUp = function (el) {
    var end = parseInt(el.getAttribute('data-count'), 10);
    var prefix = el.getAttribute('data-prefix') || '';
    if (!end || reduce) return;
    var start = end > 1000 ? end - 60 : 0;
    var t0 = null, dur = 1400;
    var step = function (t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 4);
      el.textContent = prefix + Math.round(start + (end - start) * eased);
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  /* Revelado progresivo al entrar en pantalla */
  var items = document.querySelectorAll('.reveal, .contact-band');
  if (hasIO && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-in');
        var n = en.target.querySelector && en.target.querySelector('[data-count]');
        if (n) countUp(n);
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* Paralaje del isotipo: se mueve entero, nunca tesela a tesela (no deforma el logotipo) */
  var hero = document.querySelector('.hero');
  var mark = hero && hero.querySelector('.hero-mark');
  if (mark && finePointer && !reduce) {
    var pending = false, nx = 0, ny = 0;
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      nx = (e.clientX - r.left) / r.width - 0.5;
      ny = (e.clientY - r.top) / r.height - 0.5;
      if (pending) return;
      pending = true;
      requestAnimationFrame(function () {
        mark.style.setProperty('--px', (nx * 18).toFixed(1) + 'px');
        mark.style.setProperty('--py', (ny * 14).toFixed(1) + 'px');
        pending = false;
      });
    }, { passive: true });
    hero.addEventListener('pointerleave', function () { mark.style.setProperty('--px', '0px'); mark.style.setProperty('--py', '0px'); });
  }


  /* Filtros de noticias */
  var chips = document.querySelectorAll('.chip');
  if (chips.length) {
    var list = document.querySelectorAll('.news-filterable .news-item');
    var empty = document.querySelector('.news-empty');
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        var f = c.getAttribute('data-filter'), shown = 0;
        chips.forEach(function (o) { o.setAttribute('aria-pressed', String(o === c)); });
        list.forEach(function (li) {
          var ok = f === 'all' || li.getAttribute('data-area') === f || (f === 'galicia' && li.getAttribute('data-scope') === 'galicia');
          li.hidden = !ok; if (ok) { shown++; li.classList.add('is-in'); }
        });
        if (empty) empty.hidden = shown > 0;
      });
    });
  }

  /* Foco de luz en las celdas y botones magnéticos (sólo ratón) */
  if (finePointer && !reduce) {
    document.querySelectorAll('.bento-cell').forEach(function (cell) {
      cell.addEventListener('pointermove', function (e) {
        var r = cell.getBoundingClientRect();
        cell.style.setProperty('--sx', (e.clientX - r.left) + 'px');
        cell.style.setProperty('--sy', (e.clientY - r.top) + 'px');
      }, { passive: true });
    });
    document.querySelectorAll('.btn-dark, .wa-float').forEach(function (b) {
      b.classList.add('magnetic');
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.setProperty('--mx', ((e.clientX - r.left - r.width / 2) * 0.18).toFixed(1) + 'px');
        b.style.setProperty('--my', ((e.clientY - r.top - r.height / 2) * 0.3).toFixed(1) + 'px');
      }, { passive: true });
      b.addEventListener('pointerleave', function () { b.style.setProperty('--mx', '0px'); b.style.setProperty('--my', '0px'); });
    });
  }

  /* Cursor: rombo naranja + anillo con inercia (petición expresa del cliente) */
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

  /* Formulario de contacto: errores en línea y envío por correo (sin servidor) */
  var form = document.getElementById('form');
  if (form) {
    var status = form.querySelector('.form-status');
    var check = function (f) {
      var bad = f.willValidate && !f.checkValidity();
      f.classList.toggle('is-invalid', bad);
      f.setAttribute('aria-invalid', String(bad));
      return bad;
    };
    form.addEventListener('blur', function (e) { if (e.target.matches('input, textarea')) check(e.target); }, true);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var invalid = Array.prototype.filter.call(form.elements, check);
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
        '?subject=' + encodeURIComponent('Consulta web: ' + d.get('nombre')) +
        '&body=' + encodeURIComponent(body);
      status.textContent = 'Se abrirá su programa de correo para enviar la consulta. Gracias por su confianza.';
    });
  }

  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
