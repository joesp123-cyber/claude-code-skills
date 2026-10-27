---
name: seo-geo
description: "Generative Engine Optimisation (GEO): get a business cited by AI answer engines — ChatGPT, Claude, Perplexity, Google AI Overviews/AI Mode, Copilot. Checks how the brand currently appears for target questions, sets AI-crawler rules in robots.txt, writes llms.txt, restructures content to answer-first with citable facts, and strengthens entity signals (sameAs, consistent descriptions, third-party mentions). Use when the user asks about 'AI search', 'GEO', 'AEO', 'show up in ChatGPT', 'AI Overviews', 'llms.txt', or 'LLM visibility'."
---

# SEO GEO — visibility in AI answers

AI assistants answer from what they can crawl and from what the web agrees about you. Make the site easy to quote, and make the brand unambiguous.

## Step 1 — Baseline: how does the brand appear today?

Pick 5–10 questions a buyer would ask an assistant: "best [service] in [city]", "[brand] reviews", "who does [service] for [industry]", "[brand] vs [competitor]".

For each one, search the web the way the engines do (they lean on Bing, Google and their own crawls), and record:
- Is the brand mentioned? Is its site cited?
- Who *is* cited instead, and from which source types (directories, Reddit, review sites, listicles, Wikipedia)?
- If an AI Overview shows in Google results, what does it say?

Say plainly that this is a sample at one point in time. AI answers vary from run to run and by user.

## Step 2 — Let the right crawlers in

Decide with the user, then write it into `robots.txt` (or `app/robots.ts`):

| Bot | Used for | Default |
|---|---|---|
| `OAI-SearchBot`, `ChatGPT-User` | ChatGPT search and browsing | allow |
| `GPTBot` | OpenAI model training | user's choice |
| `ClaudeBot`, `Claude-User`, `Claude-SearchBot` | Anthropic training, user fetches and search | allow for visibility |
| `PerplexityBot`, `Perplexity-User` | Perplexity answers | allow |
| `Google-Extended` | Gemini training (not Search ranking) | user's choice |
| `Bingbot` | Bing, which also feeds Copilot and others | allow |

Blocking a search or user bot removes the site from that engine's answers. Blocking a training bot doesn't.

## Step 3 — `llms.txt`

Serve `/llms.txt` (markdown) in this shape:

```
# [Brand]
> One-sentence description of who you are and who you serve.

[2–4 sentences: what you do, where, for whom, what makes you different.]

## Key pages
- [Services](https://site/services/): what's offered and prices
- [About](https://site/about/): team, credentials, history
- [Contact](https://site/contact/): how to book

## Facts
- Founded: …  Location: …  Contact: …
```

It's a cheap, emerging convention. Present it as useful, not as a ranking guarantee.

## Step 4 — Make content quotable
- **Answer first:** open each key page or section with a 40–60 word direct answer to the question it targets.
- **Facts with sources:** stats, prices, timelines and named examples are what engines cite. Vague claims get skipped.
- **Clear structure:** question-style H2s, short paragraphs, lists and tables, and an FAQ that reflects real questions.
- **Freshness:** a visible updated date, with content that stays current.
- **Server-rendered:** AI crawlers often don't run JavaScript. Confirm the text is in the raw HTML (`curl -s URL | grep "key phrase"`).

## Step 5 — Entity consistency and mentions
- The same one-line description of the brand everywhere: the site, LinkedIn, GBP, directories.
- `sameAs` in the JSON-LD links all official profiles (see `seo-schema`).
- Earn mentions in the sources Step 1 showed are being cited: industry directories, "best X" listicles, Reddit threads (as genuine participation, never spam), podcasts, partner sites. List the 10 best targets.

## Output

```
## AI Search Visibility — [brand]  (YYYY-MM-DD)
### Baseline
| Question | Brand mentioned? | Cited sources instead |
### Changes made / to make
- robots AI rules: …   - llms.txt: …   - pages restructured: …
### Mention targets (top 10)
### Re-check in 30 days: [the same questions]
```

## Rules
- No promises of being cited, and no made-up "AI visibility scores".
- Never create fake reviews, sock-puppet forum posts or spam listicles.
