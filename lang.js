/* Language switch - the saraogee.com pattern, sized for a static site.
   Whole page renders in ONE language; the header button flips it and the
   choice sticks in localStorage. Default is Hindi: the audience is the
   merchant; underwriters can click English. */
(function () {
  var saved = null;
  try { saved = localStorage.getItem('pakka-lang'); } catch (e) {}
  var lang = saved === 'en' ? 'en' : 'hi';
  document.documentElement.setAttribute('data-lang', lang);

  function label() {
    var b = document.getElementById('lang-btn');
    if (b) b.textContent = document.documentElement.getAttribute('data-lang') === 'hi'
      ? 'English' : 'हिंदी';
  }
  document.addEventListener('DOMContentLoaded', function () {
    label();
    var b = document.getElementById('lang-btn');
    if (!b) return;
    b.addEventListener('click', function () {
      var next = document.documentElement.getAttribute('data-lang') === 'hi' ? 'en' : 'hi';
      document.documentElement.setAttribute('data-lang', next);
      try { localStorage.setItem('pakka-lang', next); } catch (e) {}
      label();
    });
  });
})();
