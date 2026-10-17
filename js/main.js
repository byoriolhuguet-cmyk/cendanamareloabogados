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
    else setTimeout(function () { intro.remove(); }, 2800);
  }

  /* Cabecera: transparente sobre la portada oscura, sólida al pasar al contenido */
  var header = document.querySelector('[data-header]');
  var firstDark = document.querySelector('main [data-dark]');
  if (header) {
    if (firstDark && hasIO) {
      var hh = header.offsetHeight;
      new IntersectionObserver(function (e) {
        header.classList.toggle('is-solid', !e[0].isIntersecting);
      }, { rootMargin: '0px 0px -' + Math.max(window.innerHeight - hh, 0) + 'px 0px' }).observe(firstDark);
    } else {
      header.classList.add('is-solid');
    }
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
  var items = document.querySelectorAll('.reveal, .firma-art, .finale');
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

  /* Paralaje del isotipo del hero: se mueve entero (nunca tesela a tesela) */
  var hero = document.querySelector('.hero');
  var art = hero && hero.querySelector('.hero-tiles');
  if (art && finePointer && !reduce) {
    var pend = false, nx = 0, ny = 0;
    hero.addEventListener('pointermove', function (e) {
      nx = e.clientX / window.innerWidth - 0.5; ny = e.clientY / window.innerHeight - 0.5;
      if (pend) return; pend = true;
      requestAnimationFrame(function () {
        art.style.setProperty('--px', (nx * -30).toFixed(1) + 'px');
        art.style.setProperty('--py', (ny * -20).toFixed(1) + 'px');
        pend = false;
      });
    }, { passive: true });
  }

  /* Carril del equipo: arrastrar con el ratón */
  document.querySelectorAll('[data-rail]').forEach(function (rail) {
    if (!finePointer) return;
    var down = false, sx = 0, sl = 0, moved = false;
    rail.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = rail.scrollLeft; });
    window.addEventListener('pointerup', function () { down = false; rail.classList.remove('is-drag'); });
    rail.addEventListener('pointermove', function (e) {
      if (!down) return;
      var dx = e.clientX - sx;
      if (Math.abs(dx) > 4) { moved = true; rail.classList.add('is-drag'); }
      rail.scrollLeft = sl - dx;
    });
    rail.addEventListener('click', function (e) { if (moved) { e.preventDefault(); moved = false; } }, true);
  });

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

  /* Botones magnéticos y cursor (sólo ratón) */
  if (finePointer && !reduce) {
    document.querySelectorAll('.btn-accent, .btn-dark, .wa-float').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.15).toFixed(1) + 'px,' + ((e.clientY - r.top - r.height / 2) * 0.28).toFixed(1) + 'px)';
      }, { passive: true });
      b.addEventListener('pointerleave', function () { b.style.transform = ''; });
    });
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
      doc.classList.toggle('cursor-text', !!e.target.closest('input:not([type=checkbox]), textarea, select'));
      doc.classList.toggle('cursor-link', !!e.target.closest('a, button, summary, label'));
      if (!raf) raf = requestAnimationFrame(loop);
    }, { passive: true });
    doc.addEventListener('mouseleave', function () { doc.classList.remove('cursor-on'); });
  }

  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
