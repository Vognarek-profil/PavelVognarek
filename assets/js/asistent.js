/* ──────────────────────────────────────────────────────────────────────────
   Asistent Diagnostika: průvodce s tlačítky, bez AI.

   Otázky, volby a doporučení bere z assets/js/diagnostika-data.js
   (window.DIAGNOSTIKA). Odpovědi posílá na /api/diagnostika, server je ověří
   proti stejnému souboru a pošle Pavlovi e-mail.

   Otevírá se:
     - plovoucím tlačítkem vpravo dole (ukáže se až po zavření cookie lišty),
     - libovolným prvkem s atributem data-asistent="<zdroj>"; volitelně
       data-asistent-problem="<id volby>" rovnou předvyplní první otázku.
   Bez JavaScriptu vedou tyhle prvky na #kontakt, takže nic nechybí.

   Texty se vkládají přes textContent, nikdy přes innerHTML.
   ────────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';
  var D = window.DIAGNOSTIKA;
  if (!D || !document.querySelector) return;

  var KLIC = 'pvDiagnostika_v' + D.verze;
  var stav = novyStav();
  var ui = null;          // prvky okna, vznikne při prvním otevření
  var opener = null;      // prvek, na který se po zavření vrátí fokus
  var launcher = null;

  function novyStav() {
    return { odpovedi: {}, poradi: [], text: '', textHotovo: false, hotovo: false, zdroj: '' };
  }

  // ── uložení rozpracované diagnostiky v rámci návštěvy ─────────────────────
  function uloz() {
    try { sessionStorage.setItem(KLIC, JSON.stringify(stav)); } catch (e) { /* soukromé okno */ }
  }
  function nacti() {
    try {
      var s = JSON.parse(sessionStorage.getItem(KLIC) || 'null');
      if (s && s.odpovedi && Array.isArray(s.poradi)) stav = s;
    } catch (e) { /* nic */ }
  }

  function dl(obj) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(obj);
  }

  // ── pomocník na stavbu DOM ────────────────────────────────────────────────
  function h(tag, attrs, deti) {
    var el = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (!Object.prototype.hasOwnProperty.call(attrs, k) || attrs[k] == null || attrs[k] === false) continue;
      if (k === 'text') el.textContent = attrs[k];
      else if (k === 'class') el.className = attrs[k];
      else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), attrs[k]);
      else el.setAttribute(k, attrs[k] === true ? '' : attrs[k]);
    }
    (deti || []).forEach(function (d) { if (d) el.appendChild(typeof d === 'string' ? document.createTextNode(d) : d); });
    return el;
  }

  // ── průchod otázkami ─────────────────────────────────────────────────────
  function aktivni() { return D.aktivniOtazky(stav.odpovedi); }

  function dalsiKrok() {
    if (stav.hotovo) return { typ: 'hotovo' };
    var ots = aktivni();
    for (var i = 0; i < ots.length; i++) {
      if (stav.poradi.indexOf(ots[i].id) === -1) return { typ: 'otazka', o: ots[i] };
    }
    if (!stav.textHotovo) return { typ: 'text' };
    return { typ: 'kontakt' };
  }

  function popisOdpovedi(o) {
    var v = stav.odpovedi[o.id];
    var ids = Array.isArray(v) ? v : [v];
    return ids.map(function (id) {
      var volba = o.volby.filter(function (x) { return x.id === id; })[0];
      return volba ? D.popisekVolby(volba, stav.odpovedi) : id;
    }).join(', ');
  }

  function odpovez(o, hodnota) {
    stav.odpovedi[o.id] = hodnota;
    if (stav.poradi.indexOf(o.id) === -1) stav.poradi.push(o.id);
    // Slovensko: Sklik se nenabízí, případnou dřívější volbu zahodit.
    if (o.id === 'trh' && Array.isArray(stav.odpovedi.kanaly)) {
      stav.odpovedi.kanaly = stav.odpovedi.kanaly.filter(function (id) {
        return D.volby(D.otazka('kanaly'), stav.odpovedi).some(function (x) { return x.id === id; });
      });
    }
    dl({ event: 'asistent_krok', asistent_krok: o.id, asistent_krok_cislo: stav.poradi.length });
    uloz();
    vykresli(true);
  }

  function zpet() {
    if (stav.hotovo) return;
    var krok = dalsiKrok();
    if (krok.typ === 'kontakt') { stav.textHotovo = false; }
    else if (krok.typ === 'text' && stav.poradi.length) { smazPosledni(); }
    else if (stav.poradi.length) { smazPosledni(); }
    uloz();
    vykresli(true);
  }

  function smazPosledni() {
    var id = stav.poradi.pop();
    delete stav.odpovedi[id];
  }

  function znovu() {
    stav = novyStav();
    uloz();
    vykresli(true);
  }

  // ── vykreslení ───────────────────────────────────────────────────────────
  function bublinaBot(text, extra) {
    return h('div', { class: 'pv-as-msg is-bot' }, [h('p', { text: text })].concat(extra || []));
  }
  function bublinaJa(text) {
    return h('div', { class: 'pv-as-msg is-me' }, [h('p', { text: text })]);
  }

  function vykresli(presunFokus) {
    if (!ui) return;
    var krok = dalsiKrok();
    var log = ui.log, ovl = ui.ovladani;
    log.textContent = '';
    ovl.textContent = '';

    log.appendChild(bublinaBot(D.texty.uvod));
    stav.poradi.forEach(function (id) {
      var o = D.otazka(id);
      if (!o || D.preskocit(o, stav.odpovedi)) return;
      log.appendChild(bublinaBot(o.text));
      log.appendChild(bublinaJa(popisOdpovedi(o)));
    });
    if (stav.textHotovo) {
      log.appendChild(bublinaBot(D.texty.doplneni));
      log.appendChild(bublinaJa(stav.text || 'Bez doplnění'));
    }

    var hlaska = '', kotva = null;
    if (krok.typ === 'otazka') {
      kotva = log.appendChild(bublinaBot(krok.o.text));
      hlaska = krok.o.text;
      ovl.appendChild(krok.o.typ === 'vice' ? ovladaniVice(krok.o) : ovladaniJedna(krok.o));
    } else if (krok.typ === 'text') {
      kotva = log.appendChild(bublinaBot(D.texty.doplneni));
      hlaska = D.texty.doplneni;
      ovl.appendChild(ovladaniText());
    } else if (krok.typ === 'kontakt') {
      kotva = log.appendChild(shrnuti());
      log.appendChild(bublinaBot(D.texty.dalsiKrok));
      hlaska = D.texty.shrnuti;
      ovl.appendChild(formular());
    } else {
      kotva = log.appendChild(bublinaBot(D.texty.hotovo));
      hlaska = D.texty.hotovo;
      ovl.appendChild(h('div', { class: 'pv-as-row' }, [
        h('button', { type: 'button', class: 'pv-as-btn', text: 'Zavřít', onclick: zavri }),
        h('button', { type: 'button', class: 'pv-as-link', text: 'Nová diagnostika', onclick: znovu })
      ]));
    }

    // Zpět jde jen během otázek, po odeslání už ne.
    ui.zpet.hidden = stav.hotovo || (stav.poradi.length === 0 && !stav.textHotovo);
    var ots = aktivni().length + 2;
    var hotovych = Math.min(ots, stav.poradi.length + (stav.textHotovo ? 1 : 0) + (stav.hotovo ? 1 : 0));
    ui.progress.style.width = Math.round(hotovych / ots * 100) + '%';
    ui.progressText.textContent = stav.hotovo ? 'Odesláno' : (krok.typ === 'kontakt' ? 'Poslední krok' : 'Krok ' + (hotovych + 1) + ' z ' + ots);
    ui.zive.textContent = hlaska;

    // Aktuální otázka nahoře v okně, pod ní volby. Starší průběh jde odscrollovat nahoru.
    // Nad otázkou je vidět i předchozí bublina (úvod nebo poslední odpověď), ať je jasná souvislost.
    if (kotva && kotva.previousSibling) kotva = kotva.previousSibling;
    ui.telo.scrollTop = kotva ? Math.max(0, kotva.offsetTop - 8) : ui.telo.scrollHeight;
    if (presunFokus) {
      var prvni = ovl.querySelector('button, input, textarea');
      if (prvni) prvni.focus({ preventScroll: true });
    }
  }

  function ovladaniJedna(o) {
    var box = h('div', { class: 'pv-as-opts', role: 'group', 'aria-label': o.text });
    D.volby(o, stav.odpovedi).forEach(function (v) {
      box.appendChild(h('button', {
        type: 'button', class: 'pv-as-opt', text: D.popisekVolby(v, stav.odpovedi),
        onclick: function () { odpovez(o, v.id); }
      }));
    });
    return box;
  }

  function ovladaniVice(o) {
    var vybrane = (stav.odpovedi[o.id] || []).slice();
    var box = h('div', { class: 'pv-as-opts', role: 'group', 'aria-label': o.text });
    var dal = h('button', { type: 'button', class: 'pv-as-btn', text: 'Pokračovat', disabled: !vybrane.length,
      onclick: function () { if (vybrane.length) odpovez(o, vybrane.slice()); } });
    var tlacitka = [];
    var volby = D.volby(o, stav.odpovedi);
    function obnov() {
      tlacitka.forEach(function (b, i) { b.setAttribute('aria-pressed', vybrane.indexOf(volby[i].id) !== -1 ? 'true' : 'false'); });
      dal.disabled = !vybrane.length;
    }
    volby.forEach(function (v) {
      var b = h('button', { type: 'button', class: 'pv-as-opt is-check', text: D.popisekVolby(v, stav.odpovedi),
        onclick: function () {
          var i = vybrane.indexOf(v.id);
          if (i !== -1) vybrane.splice(i, 1);
          else if (v.vylucna) vybrane = [v.id];
          else {
            vybrane = vybrane.filter(function (id) { return !volby.some(function (x) { return x.id === id && x.vylucna; }); });
            vybrane.push(v.id);
          }
          obnov();
        } });
      tlacitka.push(b);
      box.appendChild(b);
    });
    obnov();
    return h('div', null, [box, h('div', { class: 'pv-as-row' }, [dal])]);
  }

  function ovladaniText() {
    var ta = h('textarea', { class: 'pv-as-input', id: 'pvAsText', rows: '3', maxlength: '2000',
      'aria-label': 'Doplnění vlastními slovy', placeholder: 'Nepovinné' });
    ta.value = stav.text || '';
    function hotovo(text) {
      stav.text = text;
      stav.textHotovo = true;
      dl({ event: 'asistent_krok', asistent_krok: 'text', asistent_krok_cislo: stav.poradi.length + 1 });
      uloz();
      vykresli(true);
    }
    return h('div', null, [ta, h('div', { class: 'pv-as-row' }, [
      h('button', { type: 'button', class: 'pv-as-btn', text: 'Pokračovat', onclick: function () { hotovo(ta.value.trim().slice(0, 2000)); } }),
      h('button', { type: 'button', class: 'pv-as-link', text: 'Přeskočit', onclick: function () { hotovo(''); } })
    ])]);
  }

  function shrnuti() {
    var dop = D.doporuc(stav.odpovedi);
    var seznam = h('ul', { class: 'pv-as-cards' });
    dop.sluzby.forEach(function (s) {
      seznam.appendChild(h('li', null, [
        h('a', { href: s.url, class: 'pv-as-card' }, [h('strong', { text: s.nazev }), h('span', { text: s.popis })])
      ]));
    });
    return bublinaBot(D.texty.shrnuti, [seznam]);
  }

  function pole(id, label, typ, attrs) {
    var vstup = h('input', Object.assign({ id: id, name: id.replace('pvAs-', ''), type: typ, class: 'pv-as-input' }, attrs || {}));
    return h('div', { class: 'pv-as-field' }, [h('label', { for: id, text: label }), vstup]);
  }

  function formular() {
    var f = h('form', { class: 'pv-as-form', novalidate: true });
    f.appendChild(h('div', { class: 'pv-as-hp', 'aria-hidden': 'true' }, [
      h('label', { for: 'pvAs-website', text: 'Website' }),
      h('input', { id: 'pvAs-website', name: 'website', type: 'text', tabindex: '-1', autocomplete: 'off' })
    ]));
    f.appendChild(pole('pvAs-jmeno', 'Jméno', 'text', { autocomplete: 'name', required: true, maxlength: '200' }));
    f.appendChild(pole('pvAs-email', 'E-mail', 'email', { autocomplete: 'email', required: true, maxlength: '200' }));
    f.appendChild(pole('pvAs-telefon', 'Telefon (nepovinné)', 'tel', { autocomplete: 'tel', maxlength: '50' }));
    f.appendChild(pole('pvAs-web', 'Web nebo e-shop (nepovinné)', 'text', { autocomplete: 'url', inputmode: 'url', maxlength: '300', placeholder: 'mujeshop.cz' }));
    var souhlas = h('p', { class: 'pv-as-consent' });
    var cast = D.texty.souhlas.split('zásad ochrany osobních údajů');
    souhlas.appendChild(document.createTextNode(cast[0]));
    souhlas.appendChild(h('a', { href: '/zasady-ochrany-osobnich-udaju.html', target: '_blank', rel: 'noopener', text: 'zásad ochrany osobních údajů' }));
    souhlas.appendChild(document.createTextNode(cast[1] || ''));
    var btn = h('button', { type: 'submit', class: 'pv-as-btn is-wide', text: 'Odeslat a domluvit konzultaci' });
    var status = h('p', { class: 'pv-as-status', role: 'alert' });
    f.appendChild(btn);
    f.appendChild(souhlas);
    f.appendChild(status);

    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = {};
      Array.prototype.forEach.call(f.elements, function (el) { if (el.name) data[el.name] = el.value.trim(); });
      status.textContent = '';
      if (!data.jmeno || !data.email) { status.textContent = 'Vyplňte prosím jméno a e-mail.'; return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) { status.textContent = 'Zkontrolujte prosím e-mail.'; return; }
      btn.disabled = true;
      btn.textContent = 'Odesílám…';
      var platne = {};
      aktivni().forEach(function (o) { platne[o.id] = stav.odpovedi[o.id]; });
      fetch('/api/diagnostika', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          odpovedi: platne, text: stav.text, jmeno: data.jmeno, email: data.email,
          telefon: data.telefon, web: data.web, website: data.website,
          stranka: window.location.pathname, zdroj: stav.zdroj
        })
      }).then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (json) {
          if (!res.ok || !json.ok) throw new Error(json.error || '');
          stav.hotovo = true;
          uloz();
          dl({ event: 'form_submit', form_id: 'asistent', form_location: window.location.pathname });
          vykresli(true);
        });
      }).catch(function (err) {
        btn.disabled = false;
        btn.textContent = 'Odeslat a domluvit konzultaci';
        status.textContent = (err && err.message ? err.message + ' ' : 'Odeslání se nepovedlo. ')
          + 'Případně napište přímo na pavogppc@gmail.com.';
      });
    });
    return f;
  }

  // ── okno ─────────────────────────────────────────────────────────────────
  function postav() {
    var zavrit = h('button', { type: 'button', class: 'pv-as-x', 'aria-label': 'Zavřít diagnostiku', onclick: zavri }, ['×']);
    var zpetBtn = h('button', { type: 'button', class: 'pv-as-back', text: '← Zpět', onclick: zpet });
    var bar = h('span');
    var barText = h('span', { class: 'pv-as-steps' });
    var log = h('div', { class: 'pv-as-log' });
    var ovl = h('div', { class: 'pv-as-ctrl' });
    var telo = h('div', { class: 'pv-as-body' }, [log, ovl]);
    var zive = h('div', { class: 'pv-as-sr', 'aria-live': 'polite' });
    var panel = h('div', { class: 'pv-as-panel', role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'pvAsTitle' }, [
      h('div', { class: 'pv-as-head' }, [
        h('span', { class: 'pv-as-ava', 'aria-hidden': 'true', text: 'PV' }),
        h('div', { class: 'pv-as-titles' }, [
          h('strong', { id: 'pvAsTitle', text: 'Diagnostika' }),
          h('span', { text: 'Pavel Vognárek · automatický průvodce' })
        ]),
        zavrit
      ]),
      h('div', { class: 'pv-as-meta' }, [zpetBtn, barText]),
      h('div', { class: 'pv-as-bar', 'aria-hidden': 'true' }, [bar]),
      telo, zive
    ]);
    var root = h('div', { class: 'pv-as', hidden: true }, [
      h('div', { class: 'pv-as-backdrop', onclick: zavri }), panel
    ]);
    panel.addEventListener('keydown', pastFokusu);
    document.body.appendChild(root);
    ui = { root: root, panel: panel, telo: telo, log: log, ovladani: ovl, zpet: zpetBtn, progress: bar, progressText: barText, zive: zive };
  }

  function pastFokusu(e) {
    if (e.key === 'Escape') { e.preventDefault(); zavri(); return; }
    if (e.key !== 'Tab') return;
    var f = Array.prototype.filter.call(
      ui.panel.querySelectorAll('button, [href], input, textarea, [tabindex]:not([tabindex="-1"])'),
      function (el) { return !el.disabled && !el.hidden && el.offsetParent !== null && el.getAttribute('tabindex') !== '-1'; });
    if (!f.length) return;
    var prvni = f[0], posledni = f[f.length - 1];
    if (e.shiftKey && document.activeElement === prvni) { e.preventDefault(); posledni.focus(); }
    else if (!e.shiftKey && document.activeElement === posledni) { e.preventDefault(); prvni.focus(); }
  }

  function otevri(volby) {
    volby = volby || {};
    if (!ui) postav();
    if (stav.hotovo) stav = novyStav();
    // Předvyplněný problém z karty: jen když diagnostika ještě nezačala dál než první otázkou.
    var problem = volby.problem && D.otazka('problem').volby.some(function (v) { return v.id === volby.problem; });
    if (problem && stav.poradi.length <= 1 && !stav.textHotovo) {
      stav.odpovedi = { problem: volby.problem };
      stav.poradi = ['problem'];
    }
    if (volby.zdroj) stav.zdroj = volby.zdroj;
    uloz();
    opener = document.activeElement;
    ui.root.hidden = false;
    document.documentElement.classList.add('pv-as-open');
    ukazLauncher();
    vykresli(true);
    dl({ event: 'asistent_open', asistent_zdroj: stav.zdroj || 'neznamy' });
  }

  function zavri() {
    if (!ui || ui.root.hidden) return;
    ui.root.hidden = true;
    document.documentElement.classList.remove('pv-as-open');
    ukazLauncher();
    if (opener && opener.focus) opener.focus();
  }

  // ── plovoucí tlačítko: ne přes cookie lištu, ne při otevřeném okně ────────
  function ukazLauncher() {
    if (!launcher) return;
    var lista = document.getElementById('cookieBanner');
    var listaVidet = lista && !lista.classList.contains('hidden');
    var otevreno = ui && !ui.root.hidden;
    launcher.hidden = !!(listaVidet || otevreno);
  }

  function init() {
    nacti();
    document.addEventListener('click', function (e) {
      var el = e.target.closest ? e.target.closest('[data-asistent]') : null;
      if (!el) return;
      e.preventDefault();
      otevri({ zdroj: el.getAttribute('data-asistent'), problem: el.getAttribute('data-asistent-problem') });
    });
    launcher = h('button', { type: 'button', class: 'pv-as-launch', 'aria-haspopup': 'dialog', hidden: true,
      onclick: function () { otevri({ zdroj: 'plovouci' }); } }, [
      h('span', { class: 'pv-as-launch-ico', 'aria-hidden': 'true' }),
      h('span', { text: 'S čím vám pomůžu?' })
    ]);
    document.body.appendChild(launcher);
    var lista = document.getElementById('cookieBanner');
    if (lista && window.MutationObserver) {
      new MutationObserver(ukazLauncher).observe(lista, { attributes: true, attributeFilter: ['class'] });
    }
    ukazLauncher();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
