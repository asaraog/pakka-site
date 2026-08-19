#!/usr/bin/env python3
"""Build the two language trees from the bilingual masters - the Hugo model,
without Hugo.

  src/*.html   masters: every block carries lang-hi / lang-en markup
  ./*.html     built Hindi pages (the default tree)
  ./en/*.html  built English pages

Each built page contains ONE language only, so switching is plain navigation:
no client JS, no reflow, no flash of the other language. The switch pill is a
link to the same page in the other tree.

Run `python3 build.py` after editing anything in src/, then commit the lot.
"""
import os, re, io

PAGES = ['index.html', 'contact.html', 'terms.html', 'privacy.html', 'refunds.html', 'shipping.html']
VER = 'v5'  # bump to bust cached CSS

# GA4 Measurement ID, from analytics.google.com -> Admin -> Data Streams.
# Left blank on purpose: with no ID, no analytics script is injected at all -
# nothing gets built and shipped half-configured. Fill this in, run
# `python3 build.py`, commit. Also update the "Analytics" line in privacy.html
# once this is set, so the page matches what the site actually does.
GA_ID = 'G-FV2BPPCZ4S'

def analytics_snippet():
    if not GA_ID:
        return ''
    return ('<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
            '<script>window.dataLayer=window.dataLayer||[];'
            'function gtag(){dataLayer.push(arguments);}'
            "gtag('js',new Date());gtag('config','%s');</script>\n"
            % (GA_ID, GA_ID))

def remove_lang(html, drop):
    """Remove every element whose class list contains `drop` (lang-hi/lang-en).
    Stack-walks matching close tags, so nested same-name tags survive."""
    out, i = [], 0
    open_re = re.compile(r'<(\w+)([^>]*)>')
    while i < len(html):
        m = open_re.search(html, i)
        if not m:
            out.append(html[i:])
            break
        cls = re.search(r'class="([^"]*)"', m.group(2))
        if not (cls and drop in cls.group(1).split()):
            out.append(html[i:m.end()])
            i = m.end()
            continue
        # matching close of m.group(1), honouring nesting
        tag, depth, j = m.group(1), 1, m.end()
        pair = re.compile(r'<(/?)' + tag + r'[ >]')
        while depth and (n := pair.search(html, j)):
            depth += -1 if n.group(1) else 1
            j = n.end() if n.group(1) else n.end()
        # swallow trailing newline the element sat on
        k = html.find('>', j - 1) + 1 if html[j - 1] != '>' else j
        out.append(html[i:m.start()].rstrip(' '))
        i = k
        while i < len(html) and html[i] == '\n' and out and out[-1].endswith('\n'):
            i += 1
    return ''.join(out)

def pill(page, lang):
    if lang == 'hi':
        return ('<a class="lang-pill" href="en/%s" hreflang="en">'
                '<span class="on">हिंदी</span><span class="l-sep">·</span>'
                '<span>English</span></a>' % page)
    return ('<a class="lang-pill" href="../%s" hreflang="hi">'
            '<span>हिंदी</span><span class="l-sep">·</span>'
            '<span class="on">English</span></a>' % page)

def build(page, lang):
    s = io.open(os.path.join('src', page), encoding='utf-8').read()
    s = remove_lang(s, 'lang-en' if lang == 'hi' else 'lang-hi')
    # strip the now-empty class hooks
    s = re.sub(r'\s*class="((?:[-\w]+\s+)*)lang-(?:hi|en)((?:\s+[-\w]+)*)"',
               lambda m: (' class="%s"' % (m.group(1) + m.group(2)).strip()
                          if (m.group(1) + m.group(2)).strip() else ''), s)
    s = s.replace('<script src="lang.js"></script>\n', '')
    s = re.sub(r'<button id="lang-btn".*?</button>', pill(page, lang), s, flags=re.S)
    if lang == 'en':
        # asset + internal links live one level up
        s = s.replace('href="style.css', 'href="../style.css')
        for p in PAGES:
            s = s.replace('href="%s"' % p, 'href="%s"' % p)  # en->en stays sibling
        s = s.replace("lang=\"en\"", "lang=\"en\"")
    else:
        s = s.replace('<html lang="en">', '<html lang="hi">')
    s = s.replace('href="style.css"', 'href="style.css?%s"' % VER)
    s = s.replace('href="../style.css"', 'href="../style.css?%s"' % VER)
    s = s.replace('</head>', analytics_snippet() + '</head>')
    return s

os.makedirs('en', exist_ok=True)
for page in PAGES:
    io.open(page, 'w', encoding='utf-8').write(build(page, 'hi'))
    io.open(os.path.join('en', page), 'w', encoding='utf-8').write(build(page, 'en'))
print('built %d pages x 2 languages' % len(PAGES))
