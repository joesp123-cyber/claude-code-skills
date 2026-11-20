---
name: shift-briefing
description: "Writes the AM or PM shift briefing email that summarises what the autonomous Jira shifts did and what Joe has to decide. Built to be read on a phone in under 30 seconds: decisions first, under 20 lines, no paths or commands. Use when a shift run ends and the briefing is due, or when the user says 'shift briefing', 'write the briefing' or 'send the briefing'."
---

# Shift Briefing

You write the email Joe reads on his phone after a shift. Its job is to tell him what he has to decide and what he can merge. Everything else belongs on the Jira ticket or in the run log.

**Test: can Joe read it on a phone in under 30 seconds and know what to do next? If not, cut it.**

---

## Inputs

Gather these before writing:

1. Jira tickets touched this shift: status, branch, and whether tests pass
2. Open questions from the shift log, and any ticket with `shift_hold: true`
3. Tickets still To Do and what each is waiting on
4. Problems from the run log

## Format

Subject: `Shift briefing: <Ddd DD Mon> <AM|PM>`

Body, in this order. Leave out any section with nothing in it.

```
Shift briefing · <Ddd DD Mon> <AM|PM>

<N> decisions waiting
1. <KEY>: <one yes/no or either/or question>?
2. ...

Ready to merge (in this order)
<KEY> → <KEY> → <KEY>. Tests all pass. Nothing pushed.
Also from this morning: <KEY>, <KEY>.

Blocked
<KEY>, <KEY> wait on <KEY>.
<KEY>, <KEY> wait on <KEY> (yours).

Problems
<only problems Joe has to act on, one line each>
```

## Rules

- Under 20 lines in total. One idea per line, under 70 characters.
- Decisions come first, as a numbered list. Each one is a single yes/no or either/or question that starts with the ticket key. If a decision needs context, put it on the ticket and keep the email to the question.
- Ready to merge: ticket keys in merge order on one line, then one line saying whether tests pass and whether anything is pushed. If any tests fail, say which ticket and stop it from being listed as ready.
- "Also from this morning" appears only in the PM briefing, for tickets from the AM briefing that are still waiting to merge.
- Blocked: group tickets by what they wait on. Mark the blocker "(yours)" when only Joe can clear it.
- Problems: only ones Joe has to act on. If there are none, write "None that need you." Model fallbacks, credit limits, tool outages, connector failures and duplicate runs go in the run log, not the email, unless they stopped a ticket from being done.
- Leave out file paths, git commands, branch names, test counts, memory figures and line numbers. Joe can't act on them from a phone, and they are already on the ticket.
- Plain British English. Short sentences. No em dashes or en dashes in prose.

## Example

```
Shift briefing · Fri 20 Nov PM

5 decisions waiting
1. SIDE-5: approve the SIC target list?
2. SIDE-7: OK with the SIC list and "micro or small"?
3. SIDE-6: OK with statuses new/enriched/queued/contacted/suppressed?
4. SIDE-11: sold/withdrawn for owners and brokers, or admin only?
5. SIDE-4: keep /preview-onboarding?

Ready to merge (in this order)
SIDE-5 → SIDE-6 → SIDE-7. Tests all pass. Nothing pushed.
Also from this morning: SIDE-11, SIDE-3, SIDE-2, SIDE-4.

Blocked
SIDE-8, SIDE-9 wait on SIDE-7.
VEK-2, 3, 4, 6 wait on VEK-1 (yours).

Problems
None that need you.
```

## Before sending

Count the lines. If there are more than 20, cut detail from the decisions first, then merge the blocked lines. Never cut a decision or a ready-to-merge ticket.
