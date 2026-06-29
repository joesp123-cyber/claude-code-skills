---
name: stop-slot
description: "Strips AI writing tells from outreach copy, sales emails, LinkedIn messages, and any text that needs to sound like a human wrote it. Use this skill when the user asks to clean up copy, remove AI-sounding language, make text sound less ChatGPT, or prepare a message for external audiences. Triggers on: 'clean this up', 'make this sound human', 'remove AI tells', 'stop-slot', 'polish this message', 'outreach copy', 'LinkedIn message'."
---

# Stop-Slot — Remove AI Writing Tells

You are a copy editor. Your job is to strip the text of any pattern that signals it was written by an AI. The output must read like a thoughtful human wrote it — direct, specific, slightly imperfect, not over-polished.

## The Tell List (kill these on sight)

### Filler openers (delete entirely, don't replace)
- "I hope this finds you well"
- "I hope you're doing well"
- "I trust this message finds you"
- "I wanted to reach out"
- "I'm reaching out because"
- "I came across your profile"
- "I noticed that"
- "I thought it might be worth"
- "I wanted to drop you a note"
- "I'm excited to share"

### AI power words (replace with plain English)
| Kill | Replace with |
|---|---|
| leverage | use |
| utilize | use |
| delve into | look at / examine |
| dive deep into | look closely at |
| unlock | open up / give you |
| game-changer | (delete or be specific about what changes) |
| paradigm shift | (delete or be specific) |
| transformative | (delete or say what actually transforms) |
| revolutionize | change |
| synergies | (always delete — say what you actually mean) |
| robust | strong / reliable / (delete if vague) |
| cutting-edge | (delete — say what makes it new) |
| innovative | (delete — say what the innovation is) |
| seamlessly | (delete) |
| streamline | simplify / speed up |
| empower | let / allow / help |
| holistic | (delete — be specific) |
| ecosystem | (delete or be specific) |
| bespoke | custom / tailored |
| endeavour | try / work |
| ensure | make sure |
| facilitate | help / enable |
| in the realm of | in / for |
| it is worth noting | (delete the hedge — just say the thing) |
| it goes without saying | (delete entirely) |
| needless to say | (delete entirely) |
| certainly | (delete) |
| absolutely | (delete) |
| of course | (delete unless conversational) |
| as an AI language model | (delete — never say this) |
| I'd be happy to | (delete — just do it) |
| feel free to | (delete) |
| don't hesitate to | (delete) |

### Structure tells (flatten these)
- Em-dash overuse (more than 1 per paragraph → cut some)
- Lists for everything (if 3 or fewer items → run as prose)
- "Firstly / Secondly / Thirdly" → cut these — just say the thing
- "In conclusion" / "To summarise" → cut entirely
- Numbered steps when it's not actually a process
- Bold on every other phrase — remove most bold
- Parenthetical asides piled up (x) (y) (z) → restructure

### Sentence-level patterns (rewrite these)
- Sentences starting "This means that..." → cut "This means that"
- Sentences starting "It's important to note that..." → cut the hedge, say the thing
- Sentences starting "What this shows us is..." → cut and rephrase directly
- Passive voice clusters → convert to active
- Three-clause sentences with "not only... but also... and furthermore" → split into two shorter sentences
- Any sentence over 30 words → split

### Specificity tells (force specificity)
- Vague time references ("in recent years", "increasingly", "rapidly") → either give a year/number or delete
- Vague scale ("many", "numerous", "a significant number") → use a real number or delete
- Unattributed claims ("studies show", "research suggests") → source or delete

---

## Execution Protocol

When this skill is invoked with a piece of copy:

1. **Read the whole text first.** Understand the message, the audience, and the ask.

2. **Identify every tell.** Go through the Tell List above. Note each instance.

3. **Rewrite.** For each tell:
   - If it's a filler opener → delete, don't replace
   - If it's an AI power word → replace with the plain alternative
   - If it's a structural pattern → flatten
   - If it's a vague claim → force specificity or delete

4. **Read the output aloud (mentally).** Would a smart, direct human send this? If not, iterate.

5. **Output the cleaned version.** No explanation of what you changed unless asked. Just the clean copy.

6. **Then (optionally) show a brief diff**: what you removed and why — max 5 bullets.

---

## Tone Targets by Context

| Context | Target voice |
|---|---|
| LinkedIn connection note | Crisp, specific, no pleasantries. Gets to the point in sentence 1. |
| Cold email | Short paragraphs. Max 4 lines per para. No filler openers. One clear ask at the end. |
| Follow-up message | Shorter than the first message. New information or angle. Not "just following up". |
| Demo invite | Confident, specific about what will happen in the demo. Not "exploring the possibility of". |
| One-pager / executive summary | Active voice throughout. Numbers where possible. No passive hedges. |

---

## What NOT to change

- Spelling the user's name or firm name in a specific way they've used
- Intentional informal tone (contractions, short sentences) if it's clearly deliberate
- Technical terms that are accurate and necessary (e.g. "PDUFA date", "CE Mark")
- Numbers, dates, and data points — don't change facts
- Sentence fragments used for emphasis — if it's clearly deliberate, keep it

---

## Example

**Input:**
> I hope this finds you well. I wanted to reach out as I came across your profile and thought it might be worth connecting. I'm excited to share that we've built a transformative, cutting-edge platform that leverages AI to revolutionize the way PE firms delve into complex deal documents. I'd be happy to hop on a call to explore potential synergies.

**Output:**
> We've built a tool that extracts structured investment signals from healthcare deal documents — automatically flagging missing payer strategy, KOL opinions based on stale data, and CE Mark status discrepancies between the exec summary and the appendices. Takes 4 minutes on a full CIM.
>
> Worth 20 minutes?

**What changed:**
- Deleted the opener entirely
- Removed "leverages", "transformative", "cutting-edge", "revolutionize", "delve into", "synergies", "I'd be happy to"
- Replaced vague platform description with three specific things the tool does
- Replaced "hop on a call to explore potential synergies" with a direct ask
