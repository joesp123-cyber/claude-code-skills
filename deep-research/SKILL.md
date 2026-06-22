---
name: deep-research
description: "Multi-source research skill that produces a fully cited, structured research note on any topic. Unlike last-30-days (which is recency-filtered), deep-research casts a wide net across time and produces a formal research output suitable for decisions. Use when the user asks for thorough research on a topic, market, technology, person, or company where historical context matters as much as recency."
---

# Deep Research

Thorough, multi-source research on any topic. Produces a structured, cited research note. Use when you need to understand something fully, not just what happened in the last 30 days.

## When to Use This vs. last-30-days

| Use `deep-research` | Use `last-30-days` |
|---|---|
| Understanding a market, technology, or company fully | Finding out what changed this month |
| Historical context matters | Only current state matters |
| Building a research note for a decision | Quick intelligence check |
| Topic is stable or slow-moving | Topic is fast-moving |

## Research Protocol

### Step 1 — Frame the question
Before searching, state clearly:
- What is the core question?
- What decision does this research inform?
- What would HIGH confidence look like vs. LOW confidence?

### Step 2 — Multi-source search
Run 5–8 searches across different source types:

```
[topic] overview
[topic] site:ft.com OR site:reuters.com OR site:wsj.com
[topic] research report OR whitepaper
[topic] site:reddit.com OR site:hackernews.com
[topic] criticism OR "problems with" OR "failure"
[topic] pricing OR revenue OR market size
[topic] [year] trends
```

### Step 3 — Fetch top sources
For the 5 most relevant results, use WebFetch to get full content — not just snippets. Snippets miss nuance and context.

### Step 4 — Cross-reference
Look for:
- Where sources agree — that's signal
- Where sources conflict — that's the most interesting finding
- What NO source mentions — that's the absence signal

### Step 5 — Produce the research note

Use the standard VektorMark research note format:

```markdown
---
type: research
date: YYYY-MM-DD
valid_until: YYYY-MM-DD
staleness_risk: High/Medium/Low
confidence: HIGH/MEDIUM/LOW
topic: "[topic slug]"
tags: [research, relevant-tags]
status: active
---

# [Topic]

## Question
[What I set out to learn]

## Method
[Searches run, sources consulted]

## Findings
1. [Finding] — [source URL, accessed YYYY-MM-DD]
2. ...

## Implications
- [What this means for the decision at hand]

## Open questions
- [What I still don't know]

## Confidence assessment
HIGH/MEDIUM/LOW — [why]
```

### Step 6 — Confidence labelling
Label every finding:
- `HIGH` — multiple independent sources agree, primary source available
- `MEDIUM` — one strong source, or multiple weak sources
- `LOW` — single source, or inferred from adjacent data

Never present LOW confidence findings as established fact.

## Hard Rules

- Every claim needs a URL and access date.
- If you can't source it, label it a hypothesis.
- No invented statistics.
- If search returns nothing credible, say so.
