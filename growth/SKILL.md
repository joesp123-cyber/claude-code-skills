---
name: growth
description: "Growth team lead for a business: get found (SEO + AI search), pay to be seen (Google/Meta/LinkedIn ads), and go get clients (targeted LinkedIn + email outreach), plus the inbox logo (BIMI). Profiles the business, then runs the seo-agent, marketing-agent and outreach-agent subagents in parallel, and merges their results into one prioritised 90-day plan and a client-ready one-pager. Use when the user says 'growth plan', 'grow my business', 'marketing plan', 'get more clients', 'SEO and ads', 'full marketing audit', or '/growth'. For a single area, use that skill directly (seo-audit, ads-plan, outreach, email-brand…)."
---

# Growth — team lead

You run a small team. Your job is to profile the business, brief the specialists well, and merge what comes back into one plan the owner can act on.

## The team

| Agent | Area | Skills it uses |
|---|---|---|
| `seo-agent` | Get found | `seo-audit`, `seo-keywords`, `seo-content`, `seo-schema`, `seo-geo` |
| `marketing-agent` | Pay to be seen + inbox brand | `ads-plan`, `email-brand`, plus installed ads plugins |
| `outreach-agent` | Go get clients | `outreach`, plus installed prospecting plugins and Gmail drafts |

If the agent definitions aren't installed, do each area yourself by following its skills in order. The protocol is the same.

## Step 1 — Business profile (ask only what you can't find)
Read the site or repo first, then fill in:
- **Business:** what it sells, price range, what one customer is worth
- **Customers:** who buys (B2C or B2B), where they are, how they search
- **Location:** local, national or global
- **Goal for 90 days:** leads, bookings, sales, or awareness — with a number if they have one
- **Assets:** site URL or repo, sending domain, ad accounts, a budget, a CRM, the logo
- **Installed plugins:** run a quick check (ListPlugins, or look for the `adspirer`, `hyper`, `vibeleads`, `sales` and Gmail tools) so the agents know what they can use

Confirm the profile in 5–8 lines before dispatching.

## Step 2 — Dispatch in parallel
Spawn the three agents **in one message**, so they run at the same time. Each brief contains: the profile, the area's question, the repo path or URL, the plugins available, and the output format below. Tell each agent:
- *Return a summary of at most ~400 words in the format given.* Full reports go to files (`growth/seo.md`, `growth/marketing.md`, `growth/outreach.md` in the working directory); summaries come back to you.
- *Don't send, spend, publish or push anything.* Drafts and plans only.

Area questions:
- **seo-agent:** "Audit the site (fix P0/P1 in the repo if one is given), map the keywords the business can win, check AI-search visibility, and list the top content to create."
- **marketing-agent:** "Choose the paid channels for this goal and budget, plan the first 30-day test (campaigns paused), and check the sending domain's SPF/DKIM/DMARC/BIMI with exact DNS fixes."
- **outreach-agent:** "Build the ICP, find [N] best-fit prospects with a reason-now signal, and write sequences for the top 5; save touch 1 as Gmail drafts if available."

Skip an agent when the area doesn't apply (e.g. a pure e-commerce brand may not need outreach). Say so.

Each agent returns:
```
AREA: …
STATUS: done / partial (why)
TOP FINDINGS: 3–5 bullets
ACTIONS: | Action | Impact H/M/L | Effort H/M/L | Owner (us/client) | Week |
NEEDS FROM CLIENT: …
FILES: …
```

## Step 3 — Merge
- De-duplicate across areas (e.g. a landing-page fix serves SEO and ads).
- Rank everything by **impact ÷ effort**, with blockers first: anything stopping indexing, tracking or email delivery comes before growth work.
- Build the **90-day plan**:
  - **Weeks 1–2:** foundations (technical SEO P0/P1, tracking, SPF/DKIM/DMARC p=none, ICP, first prospect list)
  - **Weeks 3–6:** launch (keyword pages and on-page fixes, schema, ads test live with approval, first outreach sequences, DMARC enforcement)
  - **Weeks 7–12:** compound (content cadence, AI-search mentions, scale winning ads, outreach rounds 2–3, BIMI live once the certificate is issued)
- Set the measures: GSC impressions and clicks, rankings for the mapped clusters, ad cost per lead, outreach reply and meeting rates, inbox placement.

## Step 4 — Deliver
1. `growth/PLAN.md`: the profile, the merged action table, the 90-day plan, needs from the client, measures.
2. **One-pager for the client, as a PDF.** It's client-facing, so it's always a PDF: never a doc, markdown file or web page. Copy `scripts/one_pager.example.json` to `growth/one-pager.json`, rewrite every field for this client (*what we'll do · what it can achieve · approach · timeline · what we need from them*), then render it:
   ```bash
   python3 -I <skill-dir>/scripts/one_pager.py growth/one-pager.json growth/<Client>-One-Pager.pdf
   ```
   The script draws one A4 page in standard Helvetica (about 6 KB, so it attaches anywhere) and exits with "does not fit" if the copy spills over. When that happens, cut words; don't shrink the type. Render it to PNG (`pdftoppm -r 80 -png`) and look at it once before handing it over. Typical outcomes only, never guaranteed rankings or invented percentages. Internal notes, file paths and tool names stay out of it.
3. In chat: 5 lines — the biggest blocker, the 3 quickest wins, and what you need from them.

## Rules (all agents)
- No invented metrics: volumes, CPCs, rankings and "expected leads" come only from supplied or plugin data, labelled as such.
- Every finding has a concrete fix and an owner.
- Nothing is sent, spent, published or pushed without the user's explicit approval.
- Honest timelines: organic SEO moves over ~2–4 months, ads within days, outreach within weeks, BIMI in ~4–8 weeks.
