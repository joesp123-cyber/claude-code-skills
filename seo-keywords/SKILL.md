---
name: seo-keywords
description: "Keyword and SERP research for a business or topic. Builds keyword clusters from live search, labels search intent, checks who ranks today, finds competitor content gaps and People-Also-Ask questions, and maps each cluster to a page. Never invents search volumes: it uses volume data only from a tool export the user supplies (Google Search Console, Ahrefs, Semrush, Keyword Planner CSV) or a connected ads/SEO plugin. Use when the user asks 'what keywords should I target', 'keyword research', 'what do people search for', 'content gaps', or 'who's ranking for X'."
---

# SEO Keywords

Find the searches the business can realistically win, and say which page should win each one.

## Input

1. **Business:** what it sells, to whom, and where (the city or region matters for local businesses).
2. **Site:** URL or repo, so existing pages can be mapped.
3. **Data, optional:** a GSC/Ahrefs/Semrush/Keyword Planner CSV. If an installed plugin exposes keyword volume (Adspirer `adspirer-keywords`, Hyper `seo-research`, Marketing with Ahrefs), use it and say so.

## Protocol

### Step 1 — Seeds
Write 5–10 seed terms from how *customers* describe the problem, not how the business describes itself. Include:
- the service + location (e.g. "emergency vet Manchester")
- problem phrasing ("dog ate chocolate what to do")
- comparison phrasing ("X vs Y", "best X for Y")
- price phrasing ("X cost", "X prices UK")

### Step 2 — Expand with live search
For each seed, search and record:
- Google autocomplete-style variants (search the seed plus a–z modifiers when useful)
- the **People Also Ask** questions and **related searches** visible in results
- forum phrasing from Reddit and Quora (`[seed] site:reddit.com`)

### Step 3 — Cluster and label intent
Group terms that one page could satisfy. Label each cluster:
- **Informational** (learn), **Commercial** (compare), **Transactional** (buy or book), **Navigational** (a brand).
- **Local**, if results show a map pack.

### Step 4 — Check the results page for each priority cluster
Search the head term and note the top 5 results:
- **Who ranks:** big brands and directories, or small sites like ours?
- **Content format:** guides, service pages, listicles, tools, videos.
- **Search features:** map pack, featured snippet, PAA, AI Overview, ads count.
- **Winnability:** **High** if small sites are in the top 5, **Low** if it's all big authorities. This is a labelled judgement, not a metric.

### Step 5 — Competitor gaps
Pick 3–5 competitors who actually appear in those results. Use `site:competitor.com [topic]` to list their pages on the topic. Flag the clusters where they have a page and we don't.

### Step 6 — Map to pages
Each cluster gets exactly one target page, either existing or new. Two pages targeting one cluster compete with each other ("cannibalisation"), so flag it.

## Output

```
## Keyword Map — [business]
**Date:** YYYY-MM-DD  **Volume source:** [CSV name / plugin / "none — volumes not shown"]

| Cluster | Example terms | Intent | Volume* | Results check | Winnability | Target page | New/Existing |
|---|---|---|---|---|---|---|---|

### Quick wins (High winnability + commercial/transactional)
### Content gaps vs competitors
### Questions to answer (from PAA / forums) → feed to seo-content
```
*Volume comes only from supplied data. Otherwise the column says "n/a".

## Rules

- **Never fabricate search volume, keyword difficulty or traffic.** Without data, rank by intent and winnability and say that's what you did.
- Cite the searches you ran for SERP claims, with the date.
- Prefer clusters that make money (commercial, transactional, local) over vanity traffic.
