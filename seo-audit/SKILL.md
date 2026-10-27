---
name: seo-audit
description: "Technical SEO audit of a live website or a codebase/static build. Runs a bundled crawler (scripts/audit.py) for titles, meta descriptions, canonicals, robots.txt, sitemap.xml, noindex, H1s and heading order, image alt text, broken internal links, Open Graph/Twitter cards, html lang, viewport and JSON-LD, then adds page-speed and source-code checks. Produces a scored report where every finding has an exact fix (file:line when a repo is present). Use when the user says 'SEO audit', 'why isn't my site on Google', 'technical SEO', 'check my site's SEO', or before any other SEO work."
---

# SEO Audit

Find every technical reason a site can't be found, then say exactly how to fix each one. Facts before opinions: run the crawler first, reason about the results second.

## Input

- **Target:** a live URL, a repo, or both. With a repo, the fixes go to source files, not generic advice.
- **Scope:** the whole site (default), or the pages the user names.

## Protocol

### Step 1 — Run the crawler

```bash
# live site
python3 -I <skill-dir>/scripts/audit.py https://example.com
# static build (Next.js `out/`, Astro `dist/`, Hugo `public/`, plain HTML)
python3 -I <skill-dir>/scripts/audit.py out/ --base https://example.com
```

`<skill-dir>` is the folder holding this SKILL.md. The script uses only the standard library and prints JSON: `score`, `pages`, `counts` and `findings[]` (`severity`, `check`, `page`, `message`, `fix`).

If it exits with "could not reach", say so plainly. Don't report the site's files as missing. Ask for the repo, or build the site locally and audit the build.

For a repo with no build: find the build command in `package.json` (or the framework's equivalent), run it, and audit the output folder. If it can't be built, read the source directly (step 3) and say the crawler was skipped.

### Step 2 — Page speed (Core Web Vitals)

Try the PageSpeed Insights API, which needs no key for light use:

```
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<URL>&strategy=mobile
```

Report LCP, INP and CLS, plus the performance score, from `lighthouseResult` (lab data) and `loadingExperience` (real-user data, when Google has it). If the API can't be reached, run Lighthouse locally (`npx lighthouse <url> --output=json --quiet --chrome-flags=--headless`). If neither works, say page speed wasn't measured. Never guess the numbers.

### Step 3 — Source checks (repo only)

The crawler sees what was shipped; the source shows why. For each crawler finding, find where it comes from:

| Framework | Where SEO lives |
|---|---|
| Next.js (app router) | `export const metadata` / `generateMetadata` in `layout.tsx`/`page.tsx`, `app/robots.ts`, `app/sitemap.ts`, `opengraph-image.*` |
| Next.js (pages) | `next/head` in pages, `next-sitemap.config.js` |
| Astro | `<head>` in layouts, `@astrojs/sitemap` |
| WordPress | theme `header.php`, Yoast/RankMath settings |
| Plain HTML | each file's `<head>` |

Also check things the crawler can't see:
- Content that only renders client-side, so crawlers get an empty shell.
- Links that work only via `onClick`.
- Images with no `width`/`height`, which cause layout shift.
- Fonts with no `display: swap`.
- Huge unoptimised images in `public/`.
- `trailingSlash` and canonical settings that disagree.

### Step 4 — Prioritise

Rank by **impact × effort**:
- **P0 — blocks indexing:** noindex, robots blocking, missing or broken sitemap, 404s, empty client-rendered HTML.
- **P1 — weakens every page:** titles, descriptions, H1s, canonicals, structured data, Core Web Vitals failures.
- **P2 — polish:** social cards, alt text, heading order, llms.txt, AI-crawler rules.

## Output

```
## SEO Audit — [site]
**Date:** YYYY-MM-DD   **Crawler score:** NN/100   **Pages crawled:** N
**Page speed (mobile):** LCP x.xs · INP xxxms · CLS 0.xx  (or "not measured — why")

### P0 — fix first
| # | Issue | Page | Fix | Where (file:line) |

### P1
...

### P2
...

### What's already right
[short list, so nobody "fixes" working things]
```

If the user asks for fixes, or a repo is present and they asked for the audit "and fix", apply P0 and P1 directly. Then re-run the crawler and show the before/after score.

## Rules

- Every finding needs a concrete fix. "Improve your titles" is not a fix; the new title is.
- Never invent rankings, traffic or search volumes. The audit is about the site, not the market; that's `seo-keywords`.
- Don't touch design or copy tone while fixing SEO, beyond the title, description and heading text you were asked to change.
