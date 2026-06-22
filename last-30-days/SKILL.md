---
name: last-30-days
description: "Searches Reddit, X/Twitter, YouTube, Polymarket, and the open web filtered to the last 30 days, then answers using only that fresh information. Use this skill when the user asks about anything recent, current, or time-sensitive — market trends, competitor moves, regulatory updates, deal activity, news, pricing changes. Triggers on: 'what's happening with', 'latest on', 'recent', 'current state of', 'last 30 days', 'this month', 'news on', or any question where stale training data would give a wrong answer."
---

# Last 30 Days — Recency-Filtered Research

You are operating in recency-first mode. Your training data has a cutoff. For anything the user asks in this skill, **do not answer from memory** — search first, answer second.

## The Problem This Solves

LLMs confidently answer questions about "current" situations using data that is 12–24 months old. This skill forces a live search before any answer is formed. The result is information that is true *today*, not last year.

## Execution Protocol

When this skill is invoked with a topic, run ALL of the following searches before forming any response:

### Step 1 — Web search (last 30 days)

Run 3–5 web searches using recency filters. Use the `after:` operator and current date to constrain results:

```
[topic] after:2026-05-19
[topic] site:reddit.com after:2026-05-19
[topic] site:twitter.com OR site:x.com after:2026-05-19
[topic] news after:2026-05-19
[topic] [relevant domain e.g. site:gov.uk OR site:fda.gov OR site:ema.europa.eu] after:2026-05-19
```

Adjust the `after:` date to be exactly 30 days before today's date. Today is always available from the system context.

### Step 2 — Source-specific searches

Search each of these explicitly:

| Source | Search format |
|---|---|
| Reddit | `site:reddit.com [topic] after:2026-05-19` |
| X / Twitter | `site:x.com [topic] after:2026-05-19` |
| YouTube | `site:youtube.com [topic] after:2026-05-19` |
| Polymarket | `site:polymarket.com [topic]` (Polymarket is forward-looking; no date filter needed) |
| News | `[topic] news 2026` |

### Step 3 — Fetch top results

For the 3–5 most relevant results, use WebFetch to get the actual content — not just the snippet. Snippets are often incomplete or misleading.

### Step 4 — Synthesise and answer

Only after completing Steps 1–3:

1. State the date range searched (e.g. "Searched: May 19 – June 19, 2026")
2. List sources used (title + URL)
3. Answer the question using *only* what was found in steps 1–3
4. If something was not found in the last 30 days, say so explicitly — do not fill the gap with training data
5. Flag any finding that contradicts what you would have said from training data alone — these are the most valuable signals

## For Vektor AI Research

When the topic relates to healthcare PE, extend the search to these domain-specific sources:

- `site:ema.europa.eu` — EMA drug approvals and opinions
- `site:fda.gov` — FDA approvals, CRLs, PDUFA decisions
- `site:companieshouse.gov.uk` — UK company filings
- `site:gov.uk` — NHS, NICE, MHRA regulatory updates
- `site:pei.media` OR `site:peinsights.com` — PE deal news
- `site:mergermarket.com` — M&A intelligence
- `site:linkedin.com` — hiring signals, firm announcements
- Healthcare PE deal activity: `healthcare PE deal [year] site:reuters.com OR site:ft.com`

Save findings to `research/YYYY-MM-DD_[topic].md` using the standard research note format from CLAUDE.md § 8.

## Output Format

```
## Last 30 Days: [Topic]
**Date range searched:** [start] – [end]
**Sources checked:** [list]

### What's actually happening (as of [date])
[Answer using only live search findings]

### Key sources
1. [Title](URL) — [one-line summary, date]
2. ...

### Contradicts training data?
[Yes/No + what specifically differs, if anything]

### Open questions (not found in last 30 days)
- [What the search didn't surface]
```

## Important Rules

- Never blend training data into the answer without flagging it as such
- If search results are thin, say "limited signal in last 30 days" and explain what you did find
- Date-stamp every source
- If a source is paywalled and WebFetch returns a login wall, note it and move on — don't invent content
