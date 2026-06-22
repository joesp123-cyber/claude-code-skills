---
name: competitor-matrix
description: "Builds a structured competitive analysis matrix for any product or market. Takes a product description and target market, finds 8–12 competitors, and produces a ranked threat table with differentiation gaps. Use when the user asks to map a competitive landscape, compare competitors, or understand where a product sits in a market."
---

# Competitor Matrix

Build a competitive analysis for any product and market. Finds real competitors, maps features and pricing, identifies threats and gaps.

## Input Required

Before starting, confirm:
1. **The product** — what does it do, in one sentence?
2. **The target market** — who buys it and why?
3. **The key differentiators** — what is the product's claimed edge?

## Research Protocol

### Step 1 — Find competitors
Search for competitors across multiple angles:

```
[product category] software [target market] 2026
best [product category] tools [target market]
[product category] alternatives
[product category] site:g2.com
[product category] site:producthunt.com
[product category] "pricing" site:reddit.com
VC-backed [product category] startups 2025 2026
```

Find minimum 8 competitors. Include:
- Direct competitors (same product, same market)
- Adjacent competitors (similar product, different market or vice versa)
- Potential future competitors (adjacent players who could expand)

### Step 2 — For each competitor, research

| Field | Where to find it |
|---|---|
| Name + URL | Direct |
| Founded / HQ | Crunchbase, LinkedIn |
| Funding | Crunchbase |
| Pricing | Pricing page, G2, Capterra |
| Target customer | Homepage copy, case studies |
| Key features | Product pages, demo videos |
| Data residency | Privacy policy, trust page |
| AI features | Product pages, changelog |
| Weakness | G2/Capterra negative reviews, Reddit complaints |

### Step 3 — Build the matrix

| Competitor | Founded | Funding | Pricing | Target | Key Feature | Weakness | Threat (1–5) |
|---|---|---|---|---|---|---|---|

### Step 4 — Threat analysis

For each competitor rated 4–5 threat:
- What specifically makes them dangerous?
- What do they have that the subject product doesn't?
- What does the subject product have that they don't?
- Who wins a head-to-head sales conversation and why?

### Step 5 — Positioning gaps

Answer: given this competitive landscape, what is the single clearest differentiation the subject product should lead with?

What does the market NOT have that the product uniquely provides?

### Step 6 — Output

```
## Competitor Matrix — [Product Name]
**Date:** YYYY-MM-DD
**Market:** [description]
**Competitors found:** N

### Full Matrix
[table]

### Top Threats
[2–3 paragraphs on the highest-threat competitors]

### Differentiation Gaps
[What the market is missing that this product provides]

### Recommended Positioning
[One clear sentence the product should lead with in a sales conversation]
```

## Hard Rules

- Prices must be sourced, not estimated — mark `(estimated)` if not confirmed.
- Threat level must be justified, not assigned arbitrarily.
- Include at least one negative review source per high-threat competitor.
