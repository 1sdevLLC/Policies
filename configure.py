#!/usr/bin/env python3
"""Fill the templates in _template/ from site.config.json and write the finished site to docs/.

Usage:  python3 configure.py
Re-run any time you change site.config.json or a template. Never edit the generated
files in docs/ by hand -- edit _template/ and re-run. GitHub Pages publishes docs/ only,
so this script, your config and the templates are not served on the website.
"""
import datetime
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
TPL = ROOT / "_template"
OUT = ROOT / "docs"          # the folder GitHub Pages publishes
OUT.mkdir(exist_ok=True)
cfg = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
flags = dict(cfg.get("flags", {}))
problems = []


def need(key, obj=cfg, label="site.config.json"):
    v = obj.get(key, "")
    if not v or str(v).strip().upper().startswith("YOUR"):
        problems.append(f'{label}: set "{key}" (still a placeholder)')
    return v


for k in ["llc_name", "brand_name", "tagline", "domain", "contact_email", "support_email",
          "privacy_email", "mailing_address", "county", "effective_date"]:
    need(k)

apps = cfg.get("apps", [])
if not apps:
    problems.append('site.config.json: add at least one entry to "apps"')
for i, a in enumerate(apps):
    for k in ("name", "tagline", "description"):
        need(k, a, f"apps[{i}]")

if flags.get("hipaa_covered"):
    problems.append('flags.hipaa_covered is true: these templates are for non-HIPAA consumer apps. '
                    'Get a healthcare attorney to draft a HIPAA Notice of Privacy Practices instead.')

health = cfg.get("health", {})
flags["phone_present"] = bool(cfg.get("phone"))
if flags.get("accesses_photos"):
    need("photos_description")
if flags.get("has_backend"):
    need("service_providers")
flags["health_any"] = bool(flags.get("has_health_data") or flags.get("include_health_policy"))
if flags["health_any"]:
    for k in ("data_types", "purposes", "third_parties"):
        need(k, health, "health")

if problems:
    print("Fix these first:\n  - " + "\n  - ".join(problems))
    sys.exit(1)

e = lambda s: html.escape(str(s), quote=True)
today = datetime.date.today()
domain = cfg["domain"].strip().lower()

app_cards = ""
for a in apps:
    link = (f'<a class="btn" href="{e(a["app_store_url"])}">View on the App Store</a>'
            if a.get("app_store_url") else '<span class="soon">Coming soon to the App Store</span>')
    app_cards += (f'<article class="card"><h3>{e(a["name"])}</h3><p class="lead">{e(a["tagline"])}</p>'
                  f'<p>{e(a["description"])}</p>{link}</article>\n')

nav = [("/", "Home"), ("/support.html", "Support"), ("/privacy.html", "Privacy Policy"), ("/terms.html", "Terms of Use")]
if flags.get("include_health_policy"):
    nav.append(("/health-privacy.html", "Consumer Health Data Privacy"))

header = ('<header class="site"><a class="brand" href="/">' + e(cfg["brand_name"]) + '</a><nav>'
          + "".join(f'<a href="{h}">{t}</a>' for h, t in nav) + '</nav></header>')
footer = (f'<footer class="site"><p>&copy; {today.year} {e(cfg["llc_name"])}. All rights reserved.</p>'
          f'<p>{e(cfg["mailing_address"]).replace(chr(10), "<br>")}</p>'
          '<p>' + " &middot; ".join(f'<a href="{h}">{t}</a>' for h, t in nav[1:]) + '</p>'
          '<p class="fine">Apple, the Apple logo, iPhone and App Store are trademarks of Apple Inc. '
          'This site is not affiliated with or endorsed by Apple.</p></footer>')

tokens = {
    "LLC_NAME": e(cfg["llc_name"]), "BRAND_NAME": e(cfg["brand_name"]), "TAGLINE": e(cfg["tagline"]),
    "DOMAIN": e(domain), "CONTACT_EMAIL": e(cfg["contact_email"]), "SUPPORT_EMAIL": e(cfg["support_email"]),
    "PRIVACY_EMAIL": e(cfg["privacy_email"]), "MAILING_ADDRESS": e(cfg["mailing_address"]).replace("\n", "<br>"),
    "PHONE": e(cfg.get("phone", "")), "COUNTY": e(cfg["county"]), "EFFECTIVE_DATE": e(cfg["effective_date"]),
    "RESPONSE_TIME": e(cfg.get("response_time", "within 2 business days")),
    "YEAR": str(today.year), "TODAY": today.strftime("%B %-d, %Y"),
    "ANALYTICS_DESCRIPTION": e(cfg.get("analytics_description", "")),
    "HEALTH_DATA_TYPES": e(health.get("data_types", "")), "HEALTH_PURPOSES": e(health.get("purposes", "")),
    "SERVICE_PROVIDERS": e(cfg.get("service_providers", "")),
    "PHOTOS_DESCRIPTION": e(cfg.get("photos_description", "")),
    "HEALTH_THIRD_PARTIES": e(health.get("third_parties", "")),
    "APP_CARDS": app_cards, "APP_NAMES": e(", ".join(a["name"] for a in apps)),
    "HEADER": header, "FOOTER": footer,
}

IF = re.compile(r"\{\{#if (\w+)\}\}((?:(?!\{\{#if ).)*?)\{\{/if\}\}", re.S)


def cond(m):
    body = m.group(2)
    yes, _, no = body.partition("{{else}}")
    return yes if flags.get(m.group(1), False) else no


def render(text):
    prev = None
    while prev != text:
        prev = text
        text = IF.sub(cond, text)
    text = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: tokens.get(m.group(1), m.group(0)), text)
    return text


pages = []
for src in sorted(TPL.iterdir()):
    out = OUT / src.name
    if src.name == "health-privacy.html" and not flags.get("include_health_policy"):
        if out.exists():
            out.unlink()
        continue
    if src.suffix in (".html", ".txt"):
        text = render(src.read_text(encoding="utf-8"))
        for m in re.findall(r"\[[A-Z][A-Z .,/&-]{3,}[^\]]*\]", text):
            problems.append(f"{src.name}: leftover placeholder {m} -- fix it in site.config.json")
        left = set(re.findall(r"\{\{[^}]+\}\}", text))
        if left:
            problems.append(f"{src.name}: unresolved tokens {sorted(left)}")
        out.write_text(text, encoding="utf-8")
        if src.suffix == ".html" and src.name != "404.html":
            pages.append(src.name)
    else:
        out.write_bytes(src.read_bytes())

if problems:
    print("\n".join(problems))
    sys.exit(1)

urls = "".join(
    f"  <url><loc>https://{domain}/{'' if p == 'index.html' else p}</loc><lastmod>{today.isoformat()}</lastmod></url>\n"
    for p in pages)
(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n",
    encoding="utf-8")
(OUT / "CNAME").write_text(domain + "\n", encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")
print(f"Built {len(pages)} pages for https://{domain}/ :")
for p in pages:
    print("  -", p)
