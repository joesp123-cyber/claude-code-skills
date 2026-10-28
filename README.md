# Claude Code Skills

Skills and agents for [Claude Code](https://claude.ai/code): general-purpose research and workflow skills, plus a **Growth suite** (SEO, ads, outreach) that runs as a team of agents.

## Skills

### `last-30-days`
Searches Reddit, X/Twitter, YouTube, Polymarket, and the open web filtered to the **last 30 days**. Forces live search before forming any answer — no stale training data. Use for market trends, competitor moves, regulatory updates, news.

**Trigger:** `/last-30-days [topic]`

### `deep-research`
Multi-source research across time — no recency filter. Runs 5–8 searches across source types, fetches full content (not snippets), cross-references for conflicts and absence signals, and produces a structured research note with `HIGH/MEDIUM/LOW` confidence labels.

**Trigger:** `/deep-research [topic]`

### `competitor-matrix`
Builds a structured competitive analysis matrix. Finds 8–12 competitors, maps funding, pricing, target customer, key features, data residency, and weaknesses. Produces a ranked threat table and identifies the clearest differentiation gap.

**Trigger:** `/competitor-matrix [product description] [target market]`

### `transcript-to-proposal`
Takes a call transcript and a proposal template, extracts everything the prospect said (pain, priorities, budget signals, objections, buying signals, key quotes), and fills the template into a ready-to-review first draft. 45-minute task down to 5 minutes. Works for any call type — sales, discovery, partnership, pilot discussion.

**Trigger:** `/transcript-to-proposal` then paste transcript + template

## Growth suite: SEO + marketing + outreach

A team of four agents that grows a business three ways: **get found** (SEO and AI search), **pay to be seen** (Google, Meta and LinkedIn ads), and **go get clients** (targeted LinkedIn and email outreach), plus the brand logo in Gmail (BIMI).

| Agent (`agents/`) | Area | Skills |
|---|---|---|
| `growth-lead` | Profiles the business, runs the other three in parallel, merges into a 90-day plan + client one-pager | `growth` |
| `seo-agent` | Get found | `seo-audit`, `seo-keywords`, `seo-content`, `seo-schema`, `seo-geo` |
| `marketing-agent` | Paid ads + inbox brand | `ads-plan`, `email-brand` |
| `outreach-agent` | Targeted client outreach | `outreach` |

| Skill | Trigger | What it does |
|---|---|---|
| `growth` | `/growth [business] [goal]` | Team lead protocol: profile → dispatch agents in parallel → merged 90-day plan, plus a one-page client PDF (`scripts/one_pager.py`) |
| `seo-audit` | `/seo-audit [url or path]` | Technical audit with a bundled crawler (`scripts/audit.py`, stdlib only) for live sites or static builds; fixes go to file:line |
| `seo-keywords` | `/seo-keywords [business]` | Keyword clusters, intent, SERP winnability, competitor gaps; no invented volumes |
| `seo-content` | `/seo-content brief\|optimise [...]` | Content briefs, and on-page rewrites with internal links and an E-E-A-T check |
| `seo-schema` | `/seo-schema [page]` | JSON-LD per page type, plus a local SEO / Google Business Profile checklist |
| `seo-geo` | `/seo-geo [brand]` | AI-search visibility: baseline, AI-crawler rules, `llms.txt`, quotable content, entity signals |
| `ads-plan` | `/ads-plan [business] [budget]` | Google, Meta and LinkedIn campaign plans; launches only PAUSED via an ads plugin |
| `outreach` | `/outreach [business type] [region]` | ICP → named prospects with a reason-now signal → LinkedIn + email sequences → Gmail drafts (never sent) → CSV tracker |
| `email-brand` | `/email-brand [domain]` | SPF/DKIM/DMARC check (`scripts/email_check.py`), DMARC enforcement path, SVG Tiny PS logo, BIMI record, VMC/CMC, signature |

**Works best with these plugins** (from the Anthropic directory; every skill falls back to web research without them):
- Ads: **Adspirer** (Google, Meta, LinkedIn; campaigns created paused, spend changes need approval), or Hyper Marketing / AdCopilot
- SEO data: **Marketing** by Anthropic (Ahrefs, Similarweb)
- Prospecting: **VibeLeads**, **Sales**, **Cold Email, LinkedIn Outreach & Deliverability**
- **Gmail** connector, for outreach drafts

**Guardrails built into every skill:** no invented metrics, every finding comes with a fix, and nothing is sent, spent or published without your approval.

**Install the suite:**
```bash
cp -r growth seo-* ads-plan outreach email-brand ~/.claude/skills/
mkdir -p ~/.claude/agents && cp agents/*.md ~/.claude/agents/
claude --agent growth-lead      # or /growth inside any session
```

### SEO engine: Claude SEO

The SEO Optimisation Protocol runs on [Claude SEO](https://github.com/AgriciDaniel/claude-seo) by Agrici Daniel (MIT licence): 26 skills and 19 specialist agents covering technical SEO, Core Web Vitals, E-E-A-T, schema, AI search, local and maps, links and weekly change monitoring. Install it alongside this suite:

```bash
/plugin marketplace add AgriciDaniel/claude-seo
/plugin install claude-seo@agricidaniel-claude-seo
/seo setup
```

`seo-agent` uses it first and falls back to the skills here when it isn't installed.

## Installation

Copy any skill folder into your Claude Code skills directory:

- **Global (all projects):** `~/.claude/skills/<skill-name>/SKILL.md`
- **Project-level:** `.claude/skills/<skill-name>/SKILL.md`

Then invoke with `/<skill-name>` in Claude Code.

## Format

Each skill is a single `SKILL.md` file with a YAML frontmatter block (`name`, `description`) and a markdown body defining the research protocol. Claude Code loads them automatically.
