/* Language switch - the saraogee.com pattern, sized for a static site.
   Whole page renders in ONE language; the header button flips it and the
   choice sticks in localStorage. Default is Hindi: the audience is the
   merchant; underwriters can click English. */
(function () {
  var saved = null;
  try { saved = localStorage.getItem('pakka-lang'); } catch (e) {}
  var lang = saved === 'en' ? 'en' : 'hi';
  document.documentElement.setAttribute('data-lang', lang);

  /* The button never changes size: both words are always in it, CSS just
     highlights the active one. A control that moves under the pointer is a
     broken control. */
  document.addEventListener('DOMContentLoaded', function () {
    var b = document.getElementById('lang-btn');
    if (!b) return;
    b.addEventListener('click', function () {
      var next = document.documentElement.getAttribute('data-lang') === 'hi' ? 'en' : 'hi';
      document.documentElement.setAttribute('data-lang', next);
      try { localStorage.setItem('pakka-lang', next); } catch (e) {}
    });
  });
})();
