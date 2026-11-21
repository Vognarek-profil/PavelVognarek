/* ──────────────────────────────────────────────────────────────────────────
   consent.js: cookie lišta, modal s nastavením a window.cookieConsent.
   Sdílené pro všechny stránky (dřív jen inline na homepage, takže kdo přišel
   na podstránku, nemohl dát souhlas). Výchozí stav Consent Mode (denied)
   a obnovení uloženého souhlasu zůstávají inline v <head> PŘED GTM.
   Odkaz s atributem data-cookie-settings otevře nastavení.
   ────────────────────────────────────────────────────────────────────────── */
(function(){
  if (!document.getElementById('cookieBanner')) {
    var wrap = document.createElement('div');
    wrap.innerHTML = `
<!-- COOKIE CONSENT BANNER -->
<div id="cookieBanner" class="cookie-banner hidden" role="dialog" aria-labelledby="cookieTitle" aria-describedby="cookieDesc">
  <div class="cookie-banner-title" id="cookieTitle">Tento web používá cookies</div>
  <p id="cookieDesc">Nezbytné cookies zajišťují chod webu. Analytické cookies (Google Analytics, Microsoft Clarity) mi pomáhají pochopit, jak web používáte, a zlepšovat jej. Více informací v <a href="/zasady-ochrany-osobnich-udaju.html">zásadách ochrany osobních údajů</a>.</p>
  <div class="cookie-buttons">
    <button type="button" class="cookie-btn cookie-btn-reject" onclick="cookieConsent.rejectAll()">Odmítnout vše</button>
    <button type="button" class="cookie-btn cookie-btn-settings" onclick="cookieConsent.openSettings()">Upravit nastavení</button>
    <button type="button" class="cookie-btn cookie-btn-accept" onclick="cookieConsent.acceptAll()">Přijmout vše</button>
  </div>
</div>

<!-- COOKIE SETTINGS MODAL -->
<div id="cookieModal" class="cookie-modal hidden" role="dialog" aria-labelledby="cookieModalTitle" aria-modal="true">
  <div class="cookie-modal-content">
    <button type="button" class="cookie-modal-close" onclick="cookieConsent.closeSettings()" aria-label="Zavřít">×</button>
    <h3 id="cookieModalTitle">Nastavení cookies</h3>
    <p>Vyberte, které kategorie cookies chcete povolit. Své rozhodnutí můžete kdykoli změnit.</p>

    <div class="cookie-category">
      <div class="cookie-cat-head">
        <span class="cookie-cat-name">Nezbytné</span>
        <div class="cookie-toggle locked" role="switch" aria-checked="true" aria-disabled="true" aria-label="Nezbytné cookies jsou vždy povoleny"></div>
      </div>
      <div class="cookie-cat-desc">Nutné pro základní funkce webu (kontaktní formulář, bezpečnost). Nelze vypnout.</div>
    </div>

    <div class="cookie-category">
      <div class="cookie-cat-head">
        <span class="cookie-cat-name">Analytické</span>
        <div class="cookie-toggle" id="toggleAnalytics" onclick="cookieConsent.toggle(this)" role="switch" tabindex="0" aria-label="Analytické cookies"></div>
      </div>
      <div class="cookie-cat-desc">Google Analytics 4 a Microsoft Clarity: anonymní statistiky návštěvnosti, zdroje návštěv, chování na webu a záznam pohybu po stránce.</div>
    </div>

    <div class="cookie-category">
      <div class="cookie-cat-head">
        <span class="cookie-cat-name">Marketingové</span>
        <div class="cookie-toggle" id="toggleMarketing" onclick="cookieConsent.toggle(this)" role="switch" tabindex="0" aria-label="Marketingové cookies"></div>
      </div>
      <div class="cookie-cat-desc">Remarketing a měření reklam (Google Ads, Sklik, Meta), pokud jsou nasazené.</div>
    </div>

    <div class="cookie-modal-buttons">
      <button type="button" class="cookie-btn cookie-btn-reject" onclick="cookieConsent.rejectAll()">Odmítnout vše</button>
      <button type="button" class="cookie-btn cookie-btn-settings" onclick="cookieConsent.saveCustom()">Uložit volbu</button>
      <button type="button" class="cookie-btn cookie-btn-accept" onclick="cookieConsent.acceptAll()">Přijmout vše</button>
    </div>
  </div>
</div>
`;
    while (wrap.firstChild) document.body.appendChild(wrap.firstChild);
  }
  document.addEventListener('click', function(e){
    var a = e.target.closest ? e.target.closest('[data-cookie-settings]') : null;
    if (!a) return;
    e.preventDefault();
    window.cookieConsent.openSettings();
  });
})();

(function(){
  var KEY = 'cookieConsent_v1';
  var MAX_AGE = 31536000000; // 12 měsíců

  function gtag(){ dataLayer.push(arguments); }

  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return null;
      var p = JSON.parse(raw);
      if (Date.now() - p.timestamp > MAX_AGE) { localStorage.removeItem(KEY); return null; }
      return p;
    } catch(e) { return null; }
  }

  function save(settings) {
    localStorage.setItem(KEY, JSON.stringify({ settings: settings, timestamp: Date.now() }));
    gtag('consent', 'update', settings);
  }

  function apply(analytics, marketing) {
    var settings = {
      ad_storage: marketing ? 'granted' : 'denied',
      ad_user_data: marketing ? 'granted' : 'denied',
      ad_personalization: marketing ? 'granted' : 'denied',
      analytics_storage: analytics ? 'granted' : 'denied'
    };
    save(settings);
    hide();
  }

  function hide() {
    document.getElementById('cookieBanner').classList.add('hidden');
    document.getElementById('cookieModal').classList.add('hidden');
  }

  function showBanner() { document.getElementById('cookieBanner').classList.remove('hidden'); }

  function closeModal(){ document.getElementById('cookieModal').classList.add('hidden'); }

  function setSwitch(el, on){
    if (!el) return;
    el.classList.toggle('on', on);
    el.setAttribute('aria-checked', on ? 'true' : 'false');
  }

  window.cookieConsent = {
    acceptAll: function(){ apply(true, true); },
    rejectAll: function(){ apply(false, false); },
    openSettings: function(){
      var saved = load();
      var a = saved && saved.settings.analytics_storage === 'granted';
      var m = saved && saved.settings.ad_storage === 'granted';
      setSwitch(document.getElementById('toggleAnalytics'), !!a);
      setSwitch(document.getElementById('toggleMarketing'), !!m);
      document.getElementById('cookieModal').classList.remove('hidden');
    },
    closeSettings: closeModal,
    toggle: function(el){
      var on = el.classList.toggle('on');
      el.setAttribute('aria-checked', on ? 'true' : 'false');
    },
    saveCustom: function(){
      apply(
        document.getElementById('toggleAnalytics').classList.contains('on'),
        document.getElementById('toggleMarketing').classList.contains('on')
      );
    }
  };

  // Zavřít modal kliknutím na pozadí
  document.getElementById('cookieModal').addEventListener('click', function(e){
    if (e.target === this) closeModal();
  });
  // Zavřít modal klávesou ESC
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape' && !document.getElementById('cookieModal').classList.contains('hidden')) closeModal();
  });

  // Přepínače musí jít ovládat klávesnicí, ne jen myší (role="switch" + tabindex bez keydown je past).
  ['toggleAnalytics', 'toggleMarketing'].forEach(function(id){
    var el = document.getElementById(id);
    if (!el) return;
    el.setAttribute('aria-checked', el.classList.contains('on') ? 'true' : 'false');
    el.addEventListener('keydown', function(e){
      if (e.key === ' ' || e.key === 'Enter' || e.key === 'Spacebar') {
        e.preventDefault();
        window.cookieConsent.toggle(el);
      }
    });
  });

  if (!load()) showBanner();
})();
  
