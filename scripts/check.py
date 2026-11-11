#!/usr/bin/env python3
"""Checks for Flux76.com. Run locally and in CI: python3 scripts/check.py

1. The committed pages match what scripts/build.py generates.
2. en.json and nl.json have the same keys, every key is used by the template,
   no value is empty, and no value is the same in both languages unless listed
   in SAME_IN_BOTH (a completeness check alone misses untranslated text).
3. Every page is in sitemap.xml and every sitemap entry is a page.
4. In each page: in-page anchors point at an existing id, local files exist,
   and nothing is loaded from another host (fonts, images, scripts, styles).
5. Each page declares the same hreflang alternates.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402

ROOT = build.ROOT
SITE = "https://flux76.com"
# Values that are legitimately identical in English and Dutch.
SAME_IN_BOTH = {"foot_contact"}
errors = []


def fail(msg):
    errors.append(msg)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.anchors, self.local, self.external, self.hreflang = set(), [], [], [], {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.hreflang[a["hreflang"]] = a.get("href")
            return
        loads = []  # URLs the browser fetches without the visitor asking
        if tag in ("img", "script", "source", "iframe", "video", "audio") and a.get("src"):
            loads.append(a["src"])
        if a.get("srcset"):
            loads += [part.strip().split()[0] for part in a["srcset"].split(",")]
        if tag == "link" and a.get("rel") in ("stylesheet", "preload", "icon", "apple-touch-icon", "preconnect", "dns-prefetch"):
            loads.append(a.get("href", ""))
        for url in loads:
            (self.external if re.match(r"(https?:)?//", url) else self.local).append(url)
        href = a.get("href", "")
        if tag == "a":
            if href.startswith("#"):
                self.anchors.append(href[1:])
            elif href.startswith("/"):
                self.local.append(href)


def check_content():
    en, nl = build.load("en"), build.load("nl")
    for key in sorted(set(en) ^ set(nl)):
        fail(f"content: key '{key}' is missing from {'nl' if key in en else 'en'}.json")
    used = build.template_keys()
    for key in sorted(set(en) - used):
        fail(f"content: key '{key}' is not used by the template")
    for key in sorted(set(en) & set(nl)):
        if not en[key].strip() or not nl[key].strip():
            fail(f"content: key '{key}' is empty")
        elif en[key] == nl[key] and not key.startswith("_") and key not in SAME_IN_BOTH:
            fail(f"content: key '{key}' is identical in en and nl (untranslated?)")


def check_sitemap():
    locs = set(re.findall(r"<loc>(.*?)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8")))
    pages = {SITE + "/" + rel.removesuffix("index.html") for rel in build.PAGES.values()}
    for url in sorted(pages - locs):
        fail(f"sitemap: {url} is a page but not in sitemap.xml")
    for url in sorted(locs - pages):
        fail(f"sitemap: {url} is in sitemap.xml but is not a page")
    return pages


def check_pages(pages):
    alternates = []
    for rel in build.PAGES.values():
        p = Page()
        p.feed((ROOT / rel).read_text(encoding="utf-8"))
        for anchor in p.anchors:
            if anchor not in p.ids:
                fail(f"{rel}: link to #{anchor} but no element has that id")
        for url in p.external:
            fail(f"{rel}: loads {url} from another host")
        for url in p.local:
            path = url.split("#")[0].split("?")[0]
            target = ROOT / path.lstrip("/")
            if path.endswith("/"):
                target = target / "index.html"
            if not target.is_file():
                fail(f"{rel}: {url} does not exist")
        alternates.append(p.hreflang)
        for lang, href in p.hreflang.items():
            if href not in pages:
                fail(f"{rel}: hreflang {lang} points at {href}, which is not a page")
    if any(a != alternates[0] or len(a) < 3 for a in alternates):
        fail("hreflang: pages do not declare the same en, nl and x-default alternates")
    for css in (ROOT / "assets" / "css").glob("*.css"):
        for url in re.findall(r"url\(\s*['\"]?([^'\")]+)", css.read_text(encoding="utf-8")):
            if re.match(r"(https?:)?//", url):
                fail(f"{css.name}: loads {url} from another host")
            elif not (ROOT / url.lstrip("/")).is_file():
                fail(f"{css.name}: {url} does not exist")


def main():
    if _stale():
        fail("build: committed pages are out of date. Run: python3 scripts/build.py")
    check_content()
    check_pages(check_sitemap())
    for e in errors:
        print("FAIL " + e)
    print(f"{len(errors)} problem(s)" if errors else "All checks passed")
    return 1 if errors else 0


def _stale():
    return any(
        not (ROOT / rel).exists() or (ROOT / rel).read_text(encoding="utf-8") != build.render(lang)
        for lang, rel in build.PAGES.items()
    )


if __name__ == "__main__":
    sys.exit(main())
