---
name: ads-plan
description: "Plans paid campaigns on Google Ads (Search, Performance Max, Local Services), Meta (Facebook/Instagram) and LinkedIn for a specific business: objective, audiences, keywords and negatives, ad copy variants, landing-page match, budget split, tracking setup and a 30-day test plan. Researches competitors' live ads in the Meta Ad Library and Google Ads Transparency Center. Hands launch to an installed ads plugin (Adspirer, Hyper Marketing, AdCopilot) with campaigns created PAUSED and every spend change approved by the user. Use when the user asks for 'Google Ads', 'Facebook ads', 'Meta ads', 'LinkedIn ads', 'PPC', 'paid social', 'ad campaign', or 'ad budget'."
---

# Ads Plan

The fastest route onto page one is paying for it. This skill plans campaigns that don't waste the money.

## Input
1. **Business, offer, location, price/margin.** What's one new customer worth? Without that, there's no sensible cost per lead.
2. **Goal:** calls, bookings, form leads, sales, or awareness.
3. **Monthly budget**, or ask for it. Give a minimum viable test budget when they're unsure.
4. **Landing page** URL or repo.

## Step 1 — Pick channels by intent

| Channel | Use when | Typical format |
|---|---|---|
| Google Search | People already search for the service | Exact and phrase keywords, responsive search ads |
| Google Local Services Ads | An eligible local trade or professional service (US, UK, CA and more) | Pay-per-lead, "Google Guaranteed/Screened" badge |
| Performance Max | E-commerce, or once Search has conversion data | Asset groups + product feed |
| Meta (FB/IG) | Visual or impulse offers, local awareness, retargeting, B2C | Lead forms, Advantage+ audiences, Reels creative |
| LinkedIn | B2B with a high deal value. Target by job title, industry and company size | Lead Gen Forms, Document ads, Conversation ads |

Small budgets (under ~£/$1,000 a month) go into **one** channel, matched to intent. Spreading thin teaches the algorithms nothing.

## Step 2 — Competitor ad research
- **Meta Ad Library** (`facebook.com/ads/library`): search competitors and record their active ads, the angles that repeat, and how long the longest-running ad has been live (long-running usually means it works).
- **Google Ads Transparency Center** (`adstransparency.google.com`): their search and display ads.
- **LinkedIn:** a company page → "Ads" tab.
- Summarise: 3 angles that work, 1 angle nobody uses.

If Hyper (`meta-ads-library`) or AdWhispr is installed, use it for this step.

## Step 3 — Build the plan

**Google Search**
- Campaign split by service (and location), not one catch-all.
- Keywords: from `seo-keywords` clusters with commercial or transactional intent, in exact and phrase match.
- **Negatives list:** jobs, free, DIY, course, salary, plus competitors' names unless bidding on them deliberately.
- Responsive search ads: 15 headlines (≤30 chars) and 4 descriptions (≤90). Include the keyword, the offer, proof, location and a call to action. Assets: sitelinks, callouts, call, location.
- Volume and CPC: only from a connected plugin (Adspirer `adspirer-keywords`) or Keyword Planner. Otherwise write "estimate from Keyword Planner before launch".

**Meta**
- Objective: Leads or Sales (never Traffic for a conversion goal).
- Audiences: location radius plus broad/Advantage+, a lookalike of customers (if a list exists), and retargeting of site visitors.
- Creative: 3 concepts × 2 formats (square image, 9:16 video). Hook in the first 2 seconds, the offer, proof, a call to action. Primary text variants.

**LinkedIn**
- Targeting: job titles or functions × seniority × industry × company size. Keep the audience at 50k–500k.
- Lead Gen Form with 3–5 fields. A Document ad offering a useful guide beats "book a demo" for cold audiences.

**Tracking (required before spend)**
- GA4 plus conversion tracking: the Google Ads tag or conversions via GA4, the Meta Pixel plus Conversions API, the LinkedIn Insight Tag. Use Google Tag Manager if present.
- Call tracking for phone-led businesses.
- With a repo: add the tags in code (consent-aware under UK/EU rules: no marketing tags before consent).

**Budget and test plan**
- Split, daily caps, and the 30-day test: weeks 1–2 learning (don't touch), week 3 cut the losers, week 4 scale the winners by ≤20% every few days.
- Target cost per lead = (customer value × acceptable share) ÷ close rate. Show the maths.

## Step 4 — Launch (only with approval)
- If an ads plugin is installed (Adspirer, Hyper or AdCopilot), create the campaigns **PAUSED** and show the user the summary.
- Only enable or change budgets after an explicit "yes", every time.
- No plugin: export the plan as a step-by-step build sheet for Ads Manager and Google Ads.

## Output
```
## Ads Plan — [business]  (YYYY-MM-DD)
Goal · Budget · Target CPL (with maths)
### Channel choice & why
### Competitor angles
### Campaigns (structure, targeting, keywords/negatives, copy)
### Tracking checklist
### 30-day test plan
### Launch status: PAUSED / build sheet
```

## Rules
- Never spend, enable, or raise a budget without explicit approval.
- No made-up CPCs, conversion rates or "expected leads". Give ranges only from supplied or plugin data, labelled as estimates.
- Ad copy must follow platform policies: no personal-attribute targeting language on Meta ("Are you overweight?"), and follow the special ad category rules for housing, employment, credit and politics.
