---
name: transcript-to-proposal
description: "Takes a call transcript and a proposal template, extracts everything the prospect said (pain points, priorities, budget signals, objections, buying signals), and fills the template into a ready-to-review first draft. Cuts proposal writing from 45 minutes to 5. Works for any call type — sales, discovery, design partner, pilot discussion."
---

# Transcript to Proposal

One call transcript in. One filled proposal draft out. Ready to review in under a minute.

## What it does

Reads a call transcript, extracts what matters (prospect pain, stated priorities, budget signals, objections, buying signals, key quotes), and fills a proposal template with that information. You review and adjust before sending — but the heavy lifting is done.

## Input Required

Before starting, confirm:
1. **The transcript** — paste it directly or provide a file path
2. **The template** — paste it, provide a file path, or name an existing proposal template in the repo (e.g. `proposals/2026-06-23_summa-pilot-framework.md`)
3. **Your role on the call** — so the skill knows which speaker is you vs. the prospect

## Protocol

### Step 1 — Parse the transcript

Identify speakers. Label them:
- **YOU** — the seller / founder / account manager
- **PROSPECT** — the person or people on the other side

If there are multiple prospect speakers, note their names and roles where identifiable.

### Step 2 — Extract prospect intelligence

Read every line from PROSPECT. Pull out:

| Signal type | What to look for |
|---|---|
| **Pain points** | Problems they described, friction they mentioned, things that "take too long" or "keep getting missed" |
| **Stated priorities** | What they said matters most right now — in their words |
| **Current process** | How they do this today, what tools they use |
| **Budget signals** | Any mention of spend, budget cycles, approval processes, "what we normally pay" |
| **Timeline signals** | When they need a solution, upcoming deadlines, decision timelines |
| **Buying signals** | Positive language — "that's exactly what we need", "who else is using this", "how do we get started" |
| **Objections** | Hesitations, concerns, "the problem with that is...", "I'd need to check with..." |
| **Key quotes** | Verbatim lines that capture their pain or enthusiasm — use these in the proposal |
| **Named stakeholders** | Anyone else mentioned who needs to be involved in a decision |

### Step 3 — Extract your positioning

Read every line from YOU. Pull out:
- What you promised or committed to
- What you said the product does
- What pricing or terms you mentioned (if any)
- What next steps you proposed

### Step 4 — Fill the template

Take the template and fill every section using the extracted intelligence. Rules:
- Use the prospect's own words where possible — especially for pain points
- Don't invent specifics that weren't discussed — mark gaps as `[TO CONFIRM]`
- If the template has a section that wasn't covered on the call, note `[Not discussed — add before sending]`
- Pricing: use what was discussed. If nothing was discussed, use the template default and flag it
- Testimonials / social proof: keep template defaults unless you mentioned specific ones on the call

### Step 5 — Add a call summary header

At the top of the filled proposal, add:

```
## Call Summary
**Date:** [date from transcript or today]
**Participants:** [names and roles]
**Call duration:** [if available]

### What they care about most
[3 bullet points — their top pain points in their own words]

### Their buying signal
[The strongest positive signal from the call]

### Their main concern
[The biggest objection or hesitation raised]

### Agreed next steps
[What was agreed at the end of the call]
```

### Step 6 — Flag what needs review

At the bottom of the filled proposal, add a **Before You Send** checklist:

```
## Before You Send
- [ ] [Any section marked [TO CONFIRM] — verify before sending]
- [ ] Pricing — is this what you want to quote?
- [ ] Named stakeholders — do you need to address the proposal to anyone else?
- [ ] Next steps — are they reflected accurately?
- [ ] Remove this checklist before sending
```

### Step 7 — Save output

Save to `proposals/YYYY-MM-DD_[prospect-name]-proposal.md`.

## Hard Rules

- Never invent specifics the prospect didn't say. Mark gaps clearly.
- Use their words, not yours — proposals land better when they echo what the prospect said.
- If the transcript is unclear or a speaker is unidentified, say so rather than guessing.
- Don't include anything confidential from your side (internal pricing rationale, margin, internal notes) in the output file.
- If no template is provided, use this default structure:
  - Executive Summary
  - The Problem (their words)
  - The Solution
  - Scope of Work
  - Timeline
  - Pricing
  - Next Steps
  - About Us / Social Proof

## Example Invocation

```
/transcript-to-proposal

Transcript: [paste transcript here]
Template: proposals/2026-06-23_summa-pilot-framework.md
My speaker label: Joe
```
