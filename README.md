# Claude Code Skills

Four general-purpose skills for [Claude Code](https://claude.ai/code).

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

## Installation

Copy any skill folder into your Claude Code skills directory:

- **Global (all projects):** `~/.claude/skills/<skill-name>/SKILL.md`
- **Project-level:** `.claude/skills/<skill-name>/SKILL.md`

Then invoke with `/<skill-name>` in Claude Code.

## Format

Each skill is a single `SKILL.md` file with a YAML frontmatter block (`name`, `description`) and a markdown body defining the research protocol. Claude Code loads them automatically.
