---
name: shift-briefing
description: "Writes the AM or PM shift briefing email that tells Joe, in plain English, what Claude built while working through his Jira to-do list and what it needs from him. Every item says which project it belongs to and what it does in everyday words, so the email makes sense with no other context. Use when a shift run ends and the briefing is due, or when the user says 'shift briefing', 'write the briefing' or 'send the briefing'."
---

# Shift Briefing

You write the email Joe reads on his phone after a shift. A "shift" is a run where Claude works through Joe's Jira to-do list on its own.

Joe reads this cold. He may not remember any of the tickets, and he does not know the technical terms. **Every line must make sense to someone who has never seen the ticket.**

**Test: could a friend of Joe's who isn't technical read this and understand what was done and what Joe has to decide? If not, rewrite it.**

---

## Inputs

Gather these before writing:

1. Jira tickets touched this shift: what they are for, status, and whether tests pass
2. Open questions from the shift log, and any ticket with `shift_hold: true`
3. Tickets still To Do and what each is waiting on
4. Problems from the run log

## Projects

Group everything by project. Open each project with a one-line description in brackets, so Joe knows which project he's reading about:

| Jira key | Name | One-line description |
|---|---|---|
| SIDE (Biz-for-sale) | Biz-for-sale | your website where people list businesses for sale |
| VEK | VektorMark | your product for private equity firms |

If a ticket belongs to a project not in this table, use the Jira project's own description. If it has none, describe the project from its tickets in under 10 words, and add it to this table next time the skill is edited.

## Plain English

Say what a thing does, never what it's called inside the code. Put the ticket key in brackets at the end of the line, never at the start.

| Don't write | Write instead |
|---|---|
| merge, ship | approve, make it live |
| branch, stacked on | a saved version waiting for you |
| migration, table, schema | database change, a place to store X |
| RLS, admin-only | only you can see it |
| SIC codes | industry codes |
| Companies House bulk CSV | the government's list of every UK company |
| fixture, tests 281/281 | tested and working |
| upsert, refresh | update the list each month |
| enrichment | look up extra details, such as directors' names |
| moderation bypass | a way to skip your approval |
| spoofable | can be faked |

If a technical word has no plain version, explain it in the same line in under 8 words.

## Format

Subject: `Claude's work update: <Ddd DD Mon> <morning|evening>`

```
What this is: Claude worked through your Jira to-do list.
Here's what it built and what it needs from you.

<Project name> (<one-line description>)

Needs your answer
1. <Plain question with enough context to answer it> (<KEY>)
2. ...

Built and ready for you to approve
- <What it does, in plain words> (<KEY>)
Approve them in this order: <KEY>, <KEY>, <KEY>.

Waiting
- <What> waits on <what, in plain words> (<KEY>)

<Next project, same sections>

Problems
<only problems Joe has to act on, one line each>
```

## Rules

- Start every email with the two "What this is" lines.
- Group by project. Leave out any section with nothing in it.
- Questions come first in each project. Each one gives the background Joe needs and then asks a single yes/no or either/or question.
- "Built and ready" lines say what the thing does for Joe or his users, not how it works. If tests fail on a ticket, don't list it as ready; put it under Problems in plain words.
- Problems: only ones Joe has to act on. If there are none, write "Nothing needs fixing." Credit limits, tool outages, connector failures and duplicate runs go in the run log, not the email, unless they stopped work getting done.
- Leave out file paths, git commands, branch names, test counts, memory figures and line numbers.
- Keep it under 30 lines. Each line under 80 characters.
- Plain British English. Short sentences. No em dashes or en dashes in prose.

## Example

```
What this is: Claude worked through your Jira to-do list.
Here's what it built and what it needs from you.

Biz-for-sale (your website where people list businesses for sale)

Needs your answer
1. Claude drafted a list of industries to find sellers in.
   Approve the list? (SIDE-5)
2. Only target micro and small companies. Is that right? (SIDE-7)
3. Outreach stages: new, researched, queued, contacted,
   do not contact. OK? (SIDE-6)
4. Can owners and brokers mark a listing as sold or withdrawn,
   or only you? (SIDE-11)
5. There's a test page that previews sign-up. Keep it? (SIDE-4)

Built and ready for you to approve
- A tool that reads the government's list of every UK company
  and picks out possible sellers (SIDE-7)
- A place in the database to store those companies.
  Only you can see it (SIDE-6)
Approve them in this order: SIDE-5, SIDE-6, SIDE-7.
Also still waiting from this morning: 5 more (see that email).

Waiting
- Looking up directors' names, and updating the list each month,
  wait on the company finder above (SIDE-8, SIDE-9)

VektorMark (your product for private equity firms)

Waiting
- 4 jobs wait on you saving the unsaved work on your PC (VEK-1)

Problems
Nothing needs fixing.
```

## Before sending

Read every line and ask: would Joe know what this means without opening Jira? If not, add the missing context or cut the line. Then count the lines. If there are more than 30, shorten the "Built" and "Waiting" lines first. Never cut a question.
