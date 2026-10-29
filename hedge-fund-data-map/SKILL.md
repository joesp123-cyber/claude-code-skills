---
name: hedge-fund-data-map
description: "Maps every data source, data point and API used across past projects (Equity Signal Trading Bot, Prediction Market Bot, Vektor AI, MSP Discovery Agent, research skills) plus the free or cheap APIs that extend them, into hedge fund signals. Use when designing a strategy, scoping a data pipeline, answering 'where would I get X data', pitching to a fund, or building a research brief that needs primary-source data. Triggers on: 'data sources', 'alt data', 'signal', 'hedge fund', 'what API for', 'insider trades', '13F', 'congress trades', 'prediction market odds', 'short interest', 'government contracts'."
---

# Hedge Fund Data Map

The full catalog is in `sources.yaml` next to this file. Each entry lists the data points, the endpoint, auth, cost, **lag** and the signals it supports. `status` says whether it is `used` (wired into a past project), `connected` (available as a connector) or `potential` (new, but it extends a signal we already run).

Read `sources.yaml` before you answer. Never quote an endpoint, price or lag from memory when the catalog has it.

## Inventory at a glance

| Category | Used before | Connected | Next to add (free first) |
|---|---|---|---|
| Regulatory filings | EDGAR Form 4, EDGAR 13F, STOCK Act, Companies House | — | XBRL company facts, 8-K / 13D / Form 144 / N-PORT, FCA and ESMA shorts, Swedish FI insider register |
| Market data & execution | Alpaca (data + paper trading), market data APIs, IPO watchlist | — | FINRA short interest and short volume, CFTC COT, Polygon / Databento / Tiingo |
| Prediction markets | Polymarket, Kalshi | — | — (already the strongest edge; deepen instead) |
| Macro | — | — | FRED / ALFRED, BLS, BEA, Treasury Fiscal Data, EIA, USDA, NOAA |
| Government contracts | UK Contracts Finder, Find a Tender, CCS frameworks | — | USAspending, SAM.gov, Senate LDA lobbying |
| Healthcare | FDA, EMA, NICE, MHRA, NHS | — | openFDA API, ClinicalTrials.gov v2 |
| Private markets | PEI, Mergermarket, Reuters, FT, Vektor document extraction | Crunchbase | — |
| Alternative / sentiment | Reddit, X, YouTube, Hacker News, G2, Capterra, Product Hunt, LinkedIn (manual) | Similarweb | GDELT, Wikipedia pageviews, PatentsView, GitHub, licensed job data |

## Signal recipes

Each recipe joins sources we already know how to pull. Build them in this order: the first three reuse code that already exists.

### 1. Informed-flow overlap (extends Equity Signal Trading Bot)
- **Inputs:** Form 4 (code P only), 13F quarter-on-quarter adds, STOCK Act trades by members on the relevant committee.
- **Add:** 13D/13G for activist entry, Form 144 for planned insider supply, FINRA short interest as the opposing signal.
- **Rule of thumb:** score = clustered insider buys within 30 days + top-manager 13F adds + committee-relevant congressional buys − rising days-to-cover.
- **Watch:** 13F is up to 45 days stale and STOCK Act up to 45 days. Weight by disclosure lag, not transaction date.

### 2. Prediction markets vs. priced assets (extends Prediction Market Bot)
- **Inputs:** Kalshi Fed, CPI and payrolls contracts; Polymarket policy and election markets.
- **Compare against:** fed funds futures and consensus forecasts (FRED, BLS calendars), sector ETF moves.
- **Trade:** when the Kalshi-implied CPI distribution diverges from consensus, position rate-sensitive baskets. Map Polymarket policy odds to the sector basket each outcome favours.
- **Reuse:** Kelly sizing and the post-resolution learning loop from the old bot.

### 3. Government contract surprise (extends MSP Discovery Agent)
- **Inputs:** UK Contracts Finder / Find a Tender (already parsed), USAspending.
- **Signal:** award value ÷ trailing-twelve-month revenue (from XBRL company facts). Above 5% for a small or mid cap is material and is often not priced until the next earnings call.
- **Reuse:** entity deduplication and parent-company resolution from the MSP agent.

### 4. Biotech event calendar
- **Inputs:** FDA PDUFA and AdCom dates, EMA CHMP opinions, NICE decisions, ClinicalTrials.gov primary completion dates and status changes.
- **Overlay:** options implied volatility (Polygon / Databento) to find events the market under-prices.
- **Watch:** silent changes to trial endpoints or enrolment are the early tell.

### 5. Filing change detection (reuses Vektor AI)
- **Inputs:** 10-K / 10-Q risk factors, MD&A, 8-K text, earnings call transcripts.
- **Method:** run the Vektor extraction and recency-weighted retrieval stack. Diff each section against the prior filing and flag new risks, removed guidance language and changed KPI definitions.
- **Reuse:** provenance linter from the Holiday Chain Validator, so every flagged change carries its source passage.

### 6. Attention and sentiment
- **Inputs:** Reddit, X, YouTube, Hacker News, Wikipedia pageviews, GDELT tone.
- **Use:** contrarian or confirmatory, never standalone. Wikipedia pageviews are the hardest to game. Reddit and X are the fastest.
- **Watch:** commercial-use terms for Reddit and X data.

### 7. Positioning and crowding
- **Inputs:** 13F concentration, FINRA short interest, FCA/ESMA named shorts, CFTC COT managed-money extremes.
- **Use:** as a risk overlay on recipes 1 to 6. Cut size when a long is crowded or a short is over-borrowed.

### 8. Private-to-public read-across
- **Inputs:** Crunchbase rounds, PEI / Mergermarket deals, Companies House filings, Similarweb traffic.
- **Use:** private competitors raising at high multiples pressure listed incumbents. Sponsor activity in a niche flags take-private candidates.

### 9. Nordic port
- **Inputs:** Finansinspektionen insider register, Nasdaq Nordic prices.
- **Use:** recipe 1 on Nordic small caps, where analyst coverage is thinner.

## Reusable components from past builds

| Component | From | Hedge fund use |
|---|---|---|
| Multi-model ensemble with disagreement as signal | Equity Signal Trading Bot | Confidence score on every trade idea |
| Kelly sizing + post-resolution learning loop | Prediction Market Bot (47.1% ROI over its run) | Position sizing; a trade journal that learns |
| Document ingestion, extraction, pgvector, recency-weighted retrieval | Vektor AI, PE Knowledge System | Filings and transcript NLP |
| Entity dedup + enrichment, safe concurrent writes | MSP Discovery Agent | Mapping contract recipients to tickers |
| Provenance linter (no unsourced number ships) | Holiday Chain Validator | Compliance-grade research notes |
| Modular per-source agents | Morning Intelligence Agent | One failing feed never blocks the morning book |
| `last-30-days`, `deep-research`, `competitor-matrix` skills | this repo | Qualitative overlay on quantitative screens |

## Rules

- **Point-in-time only.** Backtest on the date the data became public (filing date, release vintage via ALFRED), never the event date. Look-ahead bias is the most common way these signals fake an edge.
- **Every figure carries source, URL and fetch time.** If it can't be sourced, label it an estimate.
- **Respect terms of use.** No LinkedIn scraping. Get a commercial agreement for Reddit and X at scale. Paywalled sources (FT, Mergermarket) are read, not redistributed.
- **No MNPI.** Expert-network or private-document data stays out of the public-markets book unless compliance has cleared it.
- **Paper first.** A new signal runs in Alpaca paper mode across enough resolved cases before any capital goes in. This is the same rule the Equity Signal Bot follows.

## Output format when asked for data for a strategy

```
## Data plan: [strategy]
| Need | Source (catalog id) | Endpoint | Lag | Cost | Status |
### Join keys
[CIK ↔ ticker ↔ CUSIP ↔ LEI ↔ Companies House number — say which mapping table is used]
### Gaps
[what the catalog lacks, and the cheapest way to fill it]
```
