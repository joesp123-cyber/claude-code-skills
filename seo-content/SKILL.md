---
name: seo-content
description: "SEO content in two modes. BRIEF: turns a keyword cluster into a writer-ready content brief (intent, angle, H2/H3 outline, entities and questions to cover, length from the live SERP, internal links, CTA). OPTIMISE: rewrites an existing page's title, meta description, H1, intro and headings for its target query, adds internal links, and runs an E-E-A-T check, editing source files directly when a repo is present. Use when the user asks for a 'content brief', 'blog post outline', 'optimise this page', 'rewrite my title/meta', 'on-page SEO', or 'internal linking'."
---

# SEO Content

Content that answers the search better than what ranks now, and says who's answering.

## Mode A — Brief (`/seo-content brief [keyword or cluster]`)

1. **Read the results page.** Search the head term. For the top 5 results, note format, rough length, H2s, and what they all cover (table stakes) vs. what none cover (the gap).
2. **Pick the angle:** the one thing this page will do better (first-hand data, a calculator, local specifics, a clearer answer, a fresher date).
3. **Write the brief:**

```
## Content Brief — [working title]
**Target query:** …   **Intent:** …   **Target page/URL:** …
**Title (≤60 chars):** …   **Meta description (120–160):** …
**Angle / why we win:** …
**Length:** ~N words (top-5 range: a–b)
**Answer first:** the 40–60 word direct answer that opens the page
**Outline:**
  H2 … (covers: …)
    H3 …
**Must mention (entities/terms):** …
**Questions to answer (PAA/forums):** …
**Proof to include:** stats with sources, examples, photos, quotes, author credentials
**Internal links:** from [pages] → this page; this page → [pages]
**Schema:** Article / FAQPage / HowTo / Service → see seo-schema
**CTA:** …
```

4. If the user wants the draft too, write it from the brief, in the brand's voice, with sources for every claim.

## Mode B — Optimise (`/seo-content optimise [page]`)

1. Get the page: a URL, or the source file in the repo. Identify its target query, or ask for it; `seo-keywords` can supply one.
2. Score against the checklist:
   - Title: has the query near the front, ≤60 chars, gives a reason to click.
   - Meta description: 120–160 chars, matches the intent, ends with a call to action.
   - One H1 that matches the query's meaning.
   - The first 100 words answer the query directly.
   - H2s cover the subtopics the top results cover.
   - At least 3 relevant internal links in and out, with descriptive anchor text (not "click here").
   - Images: descriptive alt text and file names, sized, lazy-loaded below the fold.
   - Freshness: a visible updated date if the topic changes.
   - **E-E-A-T:** a named author or business with credentials, first-hand experience shown, sources cited, contact/about pages reachable, reviews or testimonials where relevant.
3. Rewrite. Give before → after for title, meta, H1 and intro, plus a list of the heading and link changes. With a repo, edit the file and show the diff.
4. **Internal linking pass:** list the existing pages that should link to this one, each with the sentence to add the link in.

## Rules

- Keep the brand's voice. Optimising is for clarity and relevance, not keyword stuffing; never repeat the query unnaturally.
- No invented stats, reviews or credentials. Mark placeholders `[NEEDS SOURCE]` or `[CLIENT TO CONFIRM]`.
- One page, one primary query.
