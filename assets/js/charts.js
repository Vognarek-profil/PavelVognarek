// Tooltipy pro grafy v sekci Jak vyhodnocuji (HTML generuje tools/build_charts.py).
// Tooltip je jen pohodlnější cesta k hodnotě, nikdy jediná: všechna čísla jsou
// i v tabulce pod grafem. Texty se vkládají přes textContent, ne innerHTML.
(function () {
  var groups = document.querySelectorAll('[data-viz-group]');
  var cells = document.querySelectorAll('[data-tip]');
  if (!groups.length && !cells.length) return;

  var tip = document.createElement('div');
  tip.className = 'viz-tip';
  tip.hidden = true;
  document.body.appendChild(tip);

  // rows: [["záhlaví"], ["popisek", "hodnota", "#barva"], ...]
  function render(rows) {
    tip.textContent = '';
    rows.forEach(function (r, k) {
      var line = document.createElement('div');
      if (k === 0 && r.length === 1) {
        line.className = 'viz-tip-h';
        line.textContent = r[0];
      } else {
        line.className = 'viz-tip-r';
        if (r[2]) {
          var key = document.createElement('i');
          key.style.background = r[2];
          line.appendChild(key);
        }
        var b = document.createElement('strong');
        b.textContent = r[1];
        line.appendChild(b);
        line.appendChild(document.createTextNode(' ' + r[0]));
      }
      tip.appendChild(line);
    });
    tip.hidden = false;
  }

  function place(e) {
    var w = tip.offsetWidth, h = tip.offsetHeight;
    var x = e.clientX + 14, y = e.clientY - h - 12;
    if (x + w > window.innerWidth - 8) x = e.clientX - w - 14;
    if (y < 8) y = e.clientY + 18;
    tip.style.left = Math.max(8, x) + 'px';
    tip.style.top = Math.max(8, y) + 'px';
  }

  var active = null;
  function hide() {
    tip.hidden = true;
    if (!active) return;
    active.classList.remove('has-hot');
    active.querySelectorAll('.is-hot').forEach(function (el) { el.classList.remove('is-hot'); });
    active.querySelectorAll('.viz-cross').forEach(function (c) { c.style.display = 'none'; });
    active = null;
  }

  groups.forEach(function (g) {
    var tips = JSON.parse(g.getAttribute('data-tips'));
    var n = tips.length;
    var cross = g.hasAttribute('data-cross');
    g.classList.add('viz-group');

    g.querySelectorAll('.viz-plot').forEach(function (p) {
      if (cross) {
        var c = document.createElement('div');
        c.className = 'viz-cross';
        p.appendChild(c);
      }
      function move(e) {
        var r = p.getBoundingClientRect();
        var i = Math.min(n - 1, Math.max(0, Math.floor((e.clientX - r.left) / r.width * n)));
        if (active && active !== g) hide();
        active = g;
        g.classList.add('has-hot');
        g.querySelectorAll('[data-i]').forEach(function (el) {
          el.classList.toggle('is-hot', +el.getAttribute('data-i') === i);
        });
        if (cross) {
          g.querySelectorAll('.viz-cross').forEach(function (cc) {
            cc.style.left = ((i + 0.5) / n * 100) + '%';
            cc.style.display = 'block';
          });
        }
        render(tips[i]);
        place(e);
      }
      p.addEventListener('pointermove', move);
      p.addEventListener('pointerdown', move);
      // Na dotyku pointerleave přijde hned po zvednutí prstu, tooltip by zmizel dřív, než se přečte.
      p.addEventListener('pointerleave', function (e) { if (e.pointerType !== 'touch') hide(); });
    });
  });

  cells.forEach(function (el) {
    function show(e) { render(JSON.parse(el.getAttribute('data-tip'))); place(e); }
    el.addEventListener('pointermove', show);
    el.addEventListener('pointerdown', show);
    el.addEventListener('pointerleave', function (e) { if (e.pointerType !== 'touch') hide(); });
  });

  document.addEventListener('pointerdown', function (e) {
    if (!e.target.closest('.viz-plot, [data-tip]')) hide();
  });
  window.addEventListener('scroll', hide, { passive: true });
})();
