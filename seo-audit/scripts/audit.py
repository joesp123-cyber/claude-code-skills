#!/usr/bin/env python3
"""Technical SEO audit for a live site or a static build folder.

    python audit.py https://example.com            # crawl a live site
    python audit.py out/ --base https://example.com # audit a static export

Standard library only. Prints JSON: {"score", "pages", "findings": [...]}.
Each finding carries a severity, the check that raised it, the page, and the fix,
so the caller can turn it straight into a change instead of re-deriving it.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; seo-audit/1.0)"
WEIGHT = {"high": 10, "medium": 4, "low": 1}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = None
        self.meta = {}
        self.links = {}  # rel -> href
        self.headings = []  # (level, text)
        self.imgs_no_alt = 0
        self.imgs = 0
        self.hrefs = []
        self.jsonld = []
        self._in = None
        self._buf = []
        self._heading = None

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title" and self.title is None:
            self._in, self._buf = "title", []
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta.setdefault(key, a.get("content", ""))
        elif tag == "link" and a.get("rel"):
            for rel in a["rel"].lower().split():
                self.links.setdefault(rel, a.get("href", ""))
        elif re.fullmatch(r"h[1-6]", tag):
            self._heading, self._buf = int(tag[1]), []
        elif tag == "img":
            self.imgs += 1
            if "alt" not in a:
                self.imgs_no_alt += 1
        elif tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._in, self._buf = "jsonld", []

    def handle_endtag(self, tag):
        if tag == "title" and self._in == "title":
            self.title = "".join(self._buf).strip()
            self._in = None
        elif tag == "script" and self._in == "jsonld":
            self.jsonld.append("".join(self._buf))
            self._in = None
        elif re.fullmatch(r"h[1-6]", tag) and self._heading:
            self.headings.append((self._heading, " ".join("".join(self._buf).split())))
            self._heading = None

    def handle_data(self, data):
        if self._in or self._heading:
            self._buf.append(data)


class Source:
    """Fetches paths either over HTTP or from a static build folder."""

    def __init__(self, target, base):
        self.local = os.path.isdir(target)
        self.root = target if self.local else None
        self.base = (base or ("https://localhost" if self.local else target)).rstrip("/")
        self.host = urllib.parse.urlparse(self.base).netloc

    def get(self, path):
        """Return (status, text) for a site path like '/about/'."""
        if self.local:
            rel = urllib.parse.unquote(path.split("?")[0].split("#")[0]).lstrip("/")
            for cand in (rel, os.path.join(rel, "index.html"), rel + ".html"):
                f = os.path.join(self.root, cand)
                if os.path.isfile(f):
                    with open(f, encoding="utf-8", errors="replace") as fh:
                        return 200, fh.read()
            return 404, ""
        req = urllib.request.Request(self.base + path, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception:
            return 0, ""

    def internal_path(self, href, page_path):
        """Map a link to a same-site path, or None if it points elsewhere."""
        if href.startswith(("mailto:", "tel:", "javascript:", "#", "data:")):
            return None
        url = urllib.parse.urljoin(self.base + page_path, href)
        p = urllib.parse.urlparse(url)
        if p.netloc != self.host:
            return None
        return (p.path or "/") + (("?" + p.query) if p.query else "")


def audit(target, base, max_pages):
    src = Source(target, base)
    findings = []

    def add(sev, check, page, msg, fix):
        findings.append({"severity": sev, "check": check, "page": page, "message": msg, "fix": fix})

    # A network failure would otherwise read as "robots.txt missing" and so on,
    # which sends the caller off fixing files that are fine.
    if src.get("/")[0] == 0:
        raise SystemExit(f"could not reach {src.base} (DNS, proxy or TLS failure) - nothing audited")

    # --- site-level files
    status, robots = src.get("/robots.txt")
    if status != 200:
        add("high", "robots", "/robots.txt", "robots.txt missing", "Serve /robots.txt with at least `User-agent: *` and a `Sitemap:` line.")
    else:
        if re.search(r"(?im)^\s*disallow:\s*/\s*$", robots) and not re.search(r"(?im)^\s*allow:", robots):
            add("high", "robots", "/robots.txt", "robots.txt blocks the whole site", "Remove `Disallow: /` unless the site should be hidden.")
        if not re.search(r"(?im)^\s*sitemap:", robots):
            add("medium", "robots", "/robots.txt", "robots.txt does not reference a sitemap", f"Add `Sitemap: {src.base}/sitemap.xml`.")
        bots = [b for b in ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended") if b.lower() in robots.lower()]
        if not bots:
            add("low", "ai-crawlers", "/robots.txt", "No explicit rules for AI crawlers", "Decide whether GPTBot, ClaudeBot, PerplexityBot and Google-Extended may crawl, and state it (see seo-geo).")

    status, sitemap = src.get("/sitemap.xml")
    sitemap_paths = []
    if status != 200:
        add("high", "sitemap", "/sitemap.xml", "sitemap.xml missing", "Generate /sitemap.xml listing every indexable URL.")
    else:
        locs = re.findall(r"<loc>\s*([^<]+?)\s*</loc>", sitemap)
        sitemap_paths = [src.internal_path(u, "/") for u in locs]
        sitemap_paths = [p for p in sitemap_paths if p]
        if not locs:
            add("high", "sitemap", "/sitemap.xml", "sitemap.xml lists no URLs", "Add a <url><loc> entry per page.")
        if "<lastmod>" not in sitemap:
            add("low", "sitemap", "/sitemap.xml", "sitemap entries have no <lastmod>", "Add lastModified/lastmod so crawlers know what changed.")

    status, _ = src.get("/llms.txt")
    if status != 200:
        add("low", "llms-txt", "/llms.txt", "No /llms.txt", "Add an llms.txt summary for AI assistants (see seo-geo).")

    # --- crawl pages
    queue = ["/"] + [p for p in sitemap_paths if p != "/"]
    seen, pages = set(), {}
    broken = {}
    while queue and len(pages) < max_pages:
        path = queue.pop(0)
        if path in seen:
            continue
        seen.add(path)
        status, html = src.get(path)
        if status != 200:
            broken.setdefault(path, set()).add("(sitemap or start)")
            continue
        p = Page()
        try:
            p.feed(html)
        except Exception:
            pass
        pages[path] = p
        for href in p.hrefs:
            ip = src.internal_path(href, path)
            if ip is None:
                continue
            ip_clean = ip.split("#")[0]
            if re.search(r"\.(png|jpe?g|gif|svg|webp|pdf|zip|ico|css|js|xml|txt)$", ip_clean, re.I):
                continue
            if ip_clean not in seen and ip_clean not in queue:
                queue.append(ip_clean)

    # links that failed to resolve
    for path in [q for q in seen if q not in pages]:
        add("high", "broken-link", path, "Page linked or listed but returns an error", "Fix the link target or remove it from the sitemap.")

    titles, descs = {}, {}
    for path, p in pages.items():
        robots_meta = p.meta.get("robots", "").lower()
        if "noindex" in robots_meta:
            add("high", "noindex", path, "Page is set to noindex", "Remove noindex if this page should rank.")
        if not p.title:
            add("high", "title", path, "Missing <title>", "Add a unique 30–60 character title with the main keyword first.")
        else:
            titles.setdefault(p.title, []).append(path)
            if not 10 <= len(p.title) <= 60:
                add("medium", "title", path, f"Title is {len(p.title)} chars: {p.title!r}", "Aim for 30–60 characters so Google shows it in full.")
        d = p.meta.get("description")
        if not d:
            add("high", "meta-description", path, "Missing meta description", "Add a 120–160 character description that sells the click.")
        else:
            descs.setdefault(d, []).append(path)
            if not 50 <= len(d) <= 160:
                add("medium", "meta-description", path, f"Description is {len(d)} chars", "Aim for 120–160 characters.")
        if "canonical" not in p.links:
            add("medium", "canonical", path, "No canonical link", "Add <link rel=\"canonical\"> pointing at the preferred URL.")
        if not p.lang:
            add("medium", "lang", path, "<html> has no lang attribute", "Set lang, e.g. lang=\"en-GB\".")
        if "viewport" not in p.meta:
            add("high", "viewport", path, "No viewport meta tag", "Add <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">.")
        h1s = [t for lvl, t in p.headings if lvl == 1]
        if len(h1s) == 0:
            add("high", "h1", path, "No <h1>", "Give each page exactly one H1 stating what it is about.")
        elif len(h1s) > 1:
            add("medium", "h1", path, f"{len(h1s)} <h1> tags", "Keep one H1; demote the rest to H2.")
        prev = 0
        for lvl, text in p.headings:
            if prev and lvl > prev + 1:
                add("low", "heading-order", path, f"Heading jumps from h{prev} to h{lvl} at {text[:40]!r}", "Don't skip heading levels.")
                break
            prev = lvl
        if p.imgs_no_alt:
            add("medium", "img-alt", path, f"{p.imgs_no_alt} of {p.imgs} images have no alt attribute", "Describe each image in alt; use alt=\"\" for decorative ones.")
        for key, sev in (("og:title", "medium"), ("og:description", "medium"), ("og:image", "medium"), ("twitter:card", "low")):
            if key not in p.meta:
                add(sev, "social-card", path, f"Missing {key}", f"Add <meta property=\"{key}\"> so shared links render a card.")
        if "og:image" in p.meta and "og:image:alt" not in p.meta:
            add("low", "social-card", path, "og:image has no og:image:alt", "Add og:image:alt describing the share image.")
        types = []
        for raw in p.jsonld:
            try:
                data = json.loads(raw)
            except ValueError:
                add("high", "json-ld", path, "Invalid JSON-LD block", "Fix the JSON syntax; Google ignores the whole block.")
                continue
            items = data if isinstance(data, list) else data.get("@graph", [data]) if isinstance(data, dict) else []
            types += [str(i.get("@type")) for i in items if isinstance(i, dict)]
        if not p.jsonld:
            add("medium", "json-ld", path, "No structured data", "Add JSON-LD (Organization/Person/LocalBusiness/WebSite) via seo-schema.")
        elif path == "/" and "WebSite" not in types:
            add("low", "json-ld", path, f"Home page JSON-LD has {types} but no WebSite", "Add a WebSite node so Google can show the site name.")

    for t, ps in titles.items():
        if len(ps) > 1:
            add("medium", "duplicate-title", ", ".join(ps), f"Duplicate title {t!r}", "Give every page its own title.")
    for d, ps in descs.items():
        if len(ps) > 1:
            add("medium", "duplicate-description", ", ".join(ps), "Duplicate meta description", "Give every page its own description.")

    penalty = sum(WEIGHT[f["severity"]] for f in findings)
    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["check"]))
    return {
        "target": target,
        "base": src.base,
        "score": max(0, 100 - penalty),
        "pages": sorted(pages),
        "counts": {s: sum(f["severity"] == s for f in findings) for s in order},
        "findings": findings,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="URL to crawl, or a static build folder")
    ap.add_argument("--base", help="public URL of the site (needed for a folder, so absolute links count as internal)")
    ap.add_argument("--max-pages", type=int, default=50)
    args = ap.parse_args()
    target = args.target if os.path.isdir(args.target) else args.target.rstrip("/")
    json.dump(audit(target, args.base, args.max_pages), sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
