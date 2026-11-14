/* Sleep Centre site — small, dependency-free enhancements. */
(function () {
  var d = document, root = d.documentElement;
  root.classList.remove('js-off');

  // Header: solid on scroll
  var header = d.querySelector('.site-header');
  function onScroll() { header && header.classList.toggle('scrolled', window.scrollY > 24); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu
  var btn = d.querySelector('.menu-btn');
  if (btn) btn.addEventListener('click', function () {
    var open = root.classList.toggle('nav-open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  d.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && root.classList.contains('nav-open')) { root.classList.remove('nav-open'); btn && btn.setAttribute('aria-expanded', 'false'); btn && btn.focus(); }
  });

  // Hypnogram path length for the draw-on animation
  d.querySelectorAll('.hypno .trace').forEach(function (p) {
    try { p.style.setProperty('--len', Math.ceil(p.getTotalLength())); } catch (e) {}
  });

  // Reveal on scroll
  var els = d.querySelectorAll('.reveal, .bars');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add('in'); }); }

  // Symptom checker
  var chips = d.querySelectorAll('.chip');
  var out = d.querySelector('[data-verdict]');
  var count = d.querySelector('[data-count]');
  var msgs = [
    ['Tap anything that sounds like you.', 'Your answers stay on this page.'],
    ['One sign is worth keeping an eye on.', 'If it is affecting your days or your partner\'s nights, talk to us.'],
    ['Two or more signs: a sleep assessment is worth booking.', 'Many of these point to sleep apnoea, which is very treatable once diagnosed.'],
    ['Several signs together: please book an assessment soon.', 'Untreated sleep disorders raise the risk of high blood pressure, heart disease and road accidents.']
  ];
  function update() {
    var n = d.querySelectorAll('.chip[aria-pressed="true"]').length;
    var m = msgs[n === 0 ? 0 : n === 1 ? 1 : n < 4 ? 2 : 3];
    if (count) count.textContent = n;
    if (out) out.innerHTML = m[0] + '<small>' + m[1] + '</small>';
  }
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      c.setAttribute('aria-pressed', c.getAttribute('aria-pressed') === 'true' ? 'false' : 'true'); update();
    });
  });

  // Booking form -> WhatsApp message (no patient data stored on a server)
  var form = d.querySelector('[data-book]');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    var f = new FormData(form), lines = ['Hello, I would like to book an appointment.'];
    [['name', 'Name'], ['phone', 'Phone'], ['email', 'Email'], ['service', 'For'], ['date', 'Preferred date'], ['time', 'Preferred time'], ['message', 'Notes']].forEach(function (k) {
      var v = (f.get(k[0]) || '').toString().trim(); if (v) lines.push(k[1] + ': ' + v);
    });
    var url = 'https://wa.me/' + form.getAttribute('data-wa') + '?text=' + encodeURIComponent(lines.join('\n'));
    window.open(url, '_blank', 'noopener');
    var ok = d.querySelector('[data-book-ok]'); if (ok) { ok.hidden = false; ok.focus(); }
  });
  var dateIn = d.querySelector('input[type="date"]');
  if (dateIn) dateIn.min = new Date().toISOString().slice(0, 10);

  var y = d.querySelector('[data-year]'); if (y) y.textContent = new Date().getFullYear();
})();
