/* TherapOS docs: scrollspy, search, review-due flags. Progressive enhancement: all content works without JS. */
(function () {
  'use strict';
  var d = document;
  // 1. Scrollspy for the on-page TOC
  var links = [].slice.call(d.querySelectorAll('.page-toc a[href^="#"]'));
  var targets = links.map(function (a) { return d.getElementById(decodeURIComponent(a.getAttribute('href').slice(1))); });
  if (links.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var i = targets.indexOf(e.target);
        if (i < 0) return;
        links.forEach(function (a) { a.classList.remove('active'); a.removeAttribute('aria-current'); });
        links[i].classList.add('active'); links[i].setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '-80px 0px -70% 0px' });
    targets.forEach(function (t) { if (t) io.observe(t); });
  }
  // 2. Review-due flags: elements with data-next-verify="YYYY-MM-DD"
  var today = new Date().toISOString().slice(0, 10);
  [].forEach.call(d.querySelectorAll('[data-next-verify]'), function (el) {
    var n = el.getAttribute('data-next-verify');
    if (n && n < today) { var s = d.createElement('span'); s.className = 'due'; s.textContent = 'Review due'; el.appendChild(d.createTextNode(' ')); el.appendChild(s); }
  });
  // 3. Search
  var btn = d.querySelector('.nav-search'); if (!btn) return;
  var overlay = d.createElement('div'); overlay.className = 'search-overlay'; overlay.setAttribute('role', 'dialog'); overlay.setAttribute('aria-label', 'Search documentation');
  overlay.innerHTML = '<div class="search-box"><input type="search" placeholder="Search the docs…" aria-label="Search the docs" autocomplete="off"><ul></ul></div>';
  d.body.appendChild(overlay);
  var input = overlay.querySelector('input'), list = overlay.querySelector('ul'), index = null, last = null;
  function load(cb) { if (index) return cb(); fetch('/search-index.json').then(function (r) { return r.json(); }).then(function (j) { index = j; cb(); }).catch(function () { list.innerHTML = '<li class="search-empty">Search index unavailable.</li>'; }); }
  function open() { last = d.activeElement; overlay.classList.add('open'); input.value = ''; list.innerHTML = ''; load(run); input.focus(); }
  function close() { overlay.classList.remove('open'); if (last) last.focus(); }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function run() {
    var q = input.value.trim().toLowerCase(); if (!q || !index) { list.innerHTML = ''; return; }
    var words = q.split(/\s+/), res = [];
    index.forEach(function (e) {
      var score = 0, hay = (e.t + ' ' + e.h).toLowerCase();
      words.forEach(function (w) { if (e.h.toLowerCase().indexOf(w) > -1) score += 5; if (e.t.toLowerCase().indexOf(w) > -1) score += 2; if (e.x.toLowerCase().indexOf(w) > -1) score += 1; });
      if (words.every(function (w) { return (hay + ' ' + e.x.toLowerCase()).indexOf(w) > -1; })) res.push([score, e]);
    });
    res.sort(function (a, b) { return b[0] - a[0]; });
    list.innerHTML = res.length ? res.slice(0, 12).map(function (r) { var e = r[1]; return '<li><a href="' + e.u + '">' + esc(e.h || e.t) + '<small>' + esc(e.t) + (e.h ? '' : '') + '</small></a></li>'; }).join('') : '<li class="search-empty">No matches.</li>';
  }
  btn.addEventListener('click', open);
  input.addEventListener('input', run);
  overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });
  d.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && overlay.classList.contains('open')) close();
    if ((e.key === '/' || (e.key === 'k' && (e.ctrlKey || e.metaKey))) && !/INPUT|TEXTAREA/.test(d.activeElement.tagName)) { e.preventDefault(); open(); }
  });
})();
