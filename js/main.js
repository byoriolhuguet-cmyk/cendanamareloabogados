/* Cendán & Amarelo Abogados: interacción sin dependencias ni escuchas de scroll */
(function () {
  'use strict';
  var doc = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var desktop = window.matchMedia('(min-width: 1024px)');
  var hasIO = 'IntersectionObserver' in window;

  /* Cortina de carga (sólo inicio, primera visita) */
  var intro = document.querySelector('.intro');
  if (intro) {
    if (!doc.classList.contains('is-intro') || reduce) intro.remove();
    else setTimeout(function () { intro.remove(); }, 2400);
  }

  /* Cabecera: blanca siempre; línea inferior en cuanto se hace scroll */
  var header = document.querySelector('[data-header]');
  if (header && hasIO) {
    var sentinel = document.createElement('div');
    sentinel.setAttribute('aria-hidden', 'true');
    sentinel.style.cssText = 'position:absolute;top:0;left:0;width:1px;height:8px;pointer-events:none';
    document.body.prepend(sentinel);
    new IntersectionObserver(function (e) { header.classList.toggle('is-scrolled', !e[0].isIntersecting); }).observe(sentinel);
  }

  /* Menús desplegables: hover en escritorio, clic en todos; Escape y clic fuera los cierran */
  var megas = Array.prototype.slice.call(document.querySelectorAll('.has-mega'));
  var closeTimer;
  var setMega = function (li, open) {
    megas.forEach(function (m) {
      var on = m === li && open;
      m.classList.toggle('open', on);
      m.querySelector('.nav-drop').setAttribute('aria-expanded', String(on));
    });
    if (header) header.classList.toggle('mega-open', desktop.matches && megas.some(function (m) { return m.classList.contains('open'); }));
  };
  megas.forEach(function (li) {
    var b = li.querySelector('.nav-drop');
    b.addEventListener('click', function () { setMega(li, !li.classList.contains('open')); });
    li.addEventListener('pointerenter', function (e) {
      if (e.pointerType !== 'mouse' || !desktop.matches) return;
      clearTimeout(closeTimer); setMega(li, true);
    });
    li.addEventListener('pointerleave', function (e) {
      if (e.pointerType !== 'mouse' || !desktop.matches) return;
      closeTimer = setTimeout(function () { setMega(li, false); }, 180);
    });
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('.has-mega') && desktop.matches) setMega(null, false); });

  /* Menú móvil */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  var setMenu = function (open) {
    if (!toggle) return;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    nav.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
  };
  if (toggle) {
    toggle.addEventListener('click', function () { setMenu(toggle.getAttribute('aria-expanded') !== 'true'); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) { setMenu(false); setMega(null, false); } });
    desktop.addEventListener('change', function () { setMenu(false); setMega(null, false); });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = megas.filter(function (m) { return m.classList.contains('open'); })[0];
    setMega(null, false); setMenu(false);
    if (open) open.querySelector('.nav-drop').focus();
  });

  /* Titulares palabra a palabra (h2 de texto plano; el texto sigue accesible por aria-label) */
  if (!reduce) {
    document.querySelectorAll('h2.reveal').forEach(function (h) {
      if (h.children.length) return;
      var txt = h.textContent.trim();
      h.setAttribute('aria-label', txt);
      h.innerHTML = txt.split(/\s+/).map(function (w, i) {
        return '<span class="w" aria-hidden="true"><span style="--wi:' + i + '">' + w + '</span></span>';
      }).join(' ');
      h.classList.add('split');
    });
  }

  /* Cifras que cuentan */
  var countUp = function (el) {
    var end = parseInt(el.getAttribute('data-count'), 10), prefix = el.getAttribute('data-prefix') || '';
    if (!end || reduce) return;
    var start = end > 1000 ? end - 60 : 0, t0 = null;
    var step = function (t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / 1600, 1);
      el.textContent = prefix + Math.round(start + (end - start) * (1 - Math.pow(1 - p, 4)));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  /* Revelado al entrar en pantalla */
  var items = document.querySelectorAll('.reveal, .firma-art, .tess');
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

  /* Formularios: validación en línea; envío a /api/contact y, si no está disponible, por correo */
  document.querySelectorAll('[data-form]').forEach(function (form) {
    var status = form.querySelector('.f-status');
    var check = function (f) {
      if (!f.willValidate || f.name === 'web') return false;
      var bad = !f.checkValidity();
      f.classList.toggle('is-invalid', bad);
      f.setAttribute('aria-invalid', String(bad));
      return bad;
    };
    form.addEventListener('blur', function (e) { if (e.target.matches('input, textarea')) check(e.target); }, true);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = Array.prototype.filter.call(form.elements, check);
      if (bad.length) { status.textContent = 'Revise los campos marcados y acepte el aviso legal.'; bad[0].focus(); return; }
      var d = new FormData(form), data = {};
      d.forEach(function (v, k) { data[k] = v; });
      var btn = form.querySelector('button[type=submit]');
      btn.disabled = true; status.classList.remove('is-ok'); status.textContent = 'Enviando…';
      var mailto = function () {
        var body = ['Nombre: ' + data.nombre, 'Teléfono: ' + data.telefono, 'Email: ' + (data.email || '-'), 'Área: ' + (data.area || '-'), '', data.mensaje].join('\n');
        window.location.href = 'mailto:despacho@cendanamareloabogados.com?subject=' + encodeURIComponent('Consulta web: ' + data.nombre) + '&body=' + encodeURIComponent(body);
        status.textContent = 'Se abrirá su correo para enviar la consulta. Si lo prefiere, llámenos al 982 223 053.';
      };
      fetch('/api/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          status.classList.add('is-ok');
          status.textContent = 'Gracias. Hemos recibido su consulta y le llamaremos en breve.';
          form.reset();
        })
        .catch(mailto)
        .then(function () { btn.disabled = false; });
    });
  });

  /* Cursor minimalista: un punto que sigue al ratón y se abre en aro sobre enlaces (sólo ratón) */
  if (finePointer && !reduce) {
    var dot = document.createElement('div');
    dot.className = 'cursor-dot';
    dot.setAttribute('aria-hidden', 'true');
    document.body.append(dot);
    doc.classList.add('has-cursor');
    var mx = 0, my = 0, pending = false;
    document.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse') return;
      mx = e.clientX; my = e.clientY;
      doc.classList.add('cursor-on');
      doc.classList.toggle('cursor-text', !!e.target.closest('input:not([type=checkbox]), textarea, select'));
      doc.classList.toggle('cursor-link', !!e.target.closest('a, button, summary, label'));
      if (pending) return;
      pending = true;
      requestAnimationFrame(function () { dot.style.transform = 'translate3d(' + mx + 'px,' + my + 'px,0)'; pending = false; });
    }, { passive: true });
    doc.addEventListener('mouseleave', function () { doc.classList.remove('cursor-on'); });
  }

  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
