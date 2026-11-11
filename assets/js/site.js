/* Flux76.com — progressive enhancement only. The page is complete without it. */
(function () {
  'use strict';

  // Old links used ?lang=xx on a single URL. Languages now have their own pages.
  var m = /[?&]lang=([a-z]{2})\b/.exec(location.search);
  if (m) {
    var isNl = document.documentElement.lang === 'nl';
    if (m[1] === 'nl' && !isNl) { location.replace('/nl/' + location.hash); return; }
    if (m[1] !== 'nl' && isNl) { location.replace('/' + location.hash); return; }
  }

  // Light or dark: follows the device until the visitor chooses, then remembers the choice.
  var root = document.documentElement;
  var themeBtn = document.querySelector('.theme-btn');
  var system = window.matchMedia('(prefers-color-scheme: dark)');
  function chosen() { var t = root.getAttribute('data-theme'); return t === 'light' || t === 'dark' ? t : null; }
  function current() { return chosen() || (system.matches ? 'dark' : 'light'); }
  function paint() {
    var forced = chosen(), theme = current();
    // <picture> sources and theme-color follow the device by media query; pin them when a choice is made.
    document.querySelectorAll('picture source[data-scheme], picture source[media*="prefers-color-scheme"]').forEach(function (s) {
      s.setAttribute('data-scheme', 'dark');
      s.media = forced ? (forced === 'dark' ? 'all' : 'not all') : '(prefers-color-scheme: dark)';
    });
    document.querySelectorAll('meta[data-theme-color]').forEach(function (m) {
      var scheme = m.getAttribute('data-theme-color');
      m.media = forced ? (forced === scheme ? 'all' : 'not all') : '(prefers-color-scheme: ' + scheme + ')';
    });
    if (themeBtn) {
      var label = theme === 'dark' ? themeBtn.dataset.toLight : themeBtn.dataset.toDark;
      themeBtn.querySelector('span').textContent = label;
      themeBtn.setAttribute('aria-label', label);
      themeBtn.querySelector('use').setAttribute('href', theme === 'dark' ? '#i-sun' : '#i-moon');
    }
  }
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('flux76_theme', next); } catch (e) { /* choice lasts for this page only */ }
      paint();
    });
  }
  if (system.addEventListener) system.addEventListener('change', paint);
  paint();

  // Mobile menu
  var nav = document.querySelector('.nav');
  var toggle = document.querySelector('.nav-toggle');
  function setOpen(open) {
    nav.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
  }
  if (nav && toggle) {
    toggle.addEventListener('click', function () { setOpen(!nav.classList.contains('open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('.nav-main a')) setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { setOpen(false); toggle.focus(); }
    });
  }

  // Copy the email address
  var status = document.getElementById('copy-status');
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    var label = btn.querySelector('span');
    var original = label.textContent;
    var timer;
    btn.addEventListener('click', function () {
      var done = function () {
        label.textContent = btn.dataset.copied;
        if (status) status.textContent = btn.dataset.copied + ': ' + btn.dataset.copy;
        clearTimeout(timer);
        timer = setTimeout(function () { label.textContent = original; if (status) status.textContent = ''; }, 2400);
      };
      var fallback = function () {
        // Clipboard unavailable: show the address so it can be selected by hand.
        var addr = document.querySelector('.contact-addr');
        if (addr) addr.style.display = 'block';
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(btn.dataset.copy).then(done, fallback);
      } else { fallback(); }
    });
  });

  // Reveal the two case-study visuals as they enter the viewport
  var targets = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -12% 0px' });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add('in'); });
  }
})();
