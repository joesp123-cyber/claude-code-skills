---
name: goal
description: "Executes a plan (from /ultraplan or given inline) in an autonomous loop until the goal is met, blocked, or a safety cap is hit. Codes batch by batch, verifies each, and can run in the background so the user zooms out and lets it work. Use when the user says 'goal', 'run the goal', 'execute the plan', 'code this until done', or hands over a plan file. This is the BUILD phase of the ultraplan → goal → ultrareview loop. Stops at every approval gate — never edits crown-jewel files, commits, migrates a DB, or spends money without explicit sign-off."
---

# Goal — Autonomous Build Loop

You take a plan and drive it to completion. Batch by batch: implement, verify, report, continue. The user can zoom out and let you run — background agents do the work and notify on completion. You stop when the goal is met, when you hit a gate that needs a human, or when a safety cap trips.

This is phase 2 of the four-part loop:
1. `/ultraplan` — plan the task (Opus 4.8)
2. **`/goal`** (this skill) — code the plan until complete
3. **background agents** — the mechanism that lets the user zoom out
4. `/ultrareview` — review the finished code (user runs this; see handoff)

---

## Model routing

- **You** (this session) orchestrate: read the plan, sequence batches, verify, decide continue/stop.
- **Execution agents** use the cheapest model that can do the step well — **`model: "haiku"`** for mechanical edits and file moves, **`model: "sonnet"`** for anything needing judgement. Reserve Opus for planning (`/ultraplan`), not execution. This is the whole point of the loop: expensive reasoning up front, cheap execution after.

---

## Phase 0 — Load the plan

1. If given a plan file path, read it. If given none, read the newest file in `plans/`. If there is no plan, say so and suggest `/ultraplan` first — do not improvise a plan silently for a non-trivial task.
2. Re-read the constraints and gates in the plan, plus repo-root and user-level `CLAUDE.md`. These bind every action below.
3. Confirm the success criterion. This is the only definition of "done."

---

## Phase 1 — The build loop

For each batch in the plan, in order:

1. **Snapshot / reversibility.** Before changing a production file, ensure it's recoverable — git tracks it, or archive the prior version to `archive/YYYY-MM-DD_filename` per repo rules.
2. **Implement.** Dispatch execution agent(s) (haiku/sonnet) for the batch, or make the edits directly if small. Parallelise independent steps in one message.
3. **Verify.** Run the batch's verify step from the plan — the command, test, diff, or characterisation check. Where there is no test suite, capture before/after output (hashes + fields) and prove byte-identical when the change is meant to be behaviour-preserving. **A batch is not done until its verify passes.** If verify fails, fix and re-verify before moving on — do not proceed on a red check.
4. **Log.** Append a one-line entry to `research/decisions-log.md` (or the repo's decisions log) for any production change: what, why, verified-how.
5. **Report.** State: batch N done, what changed, verify result. Then continue to the next batch.

### Running in the background (the "zoom out")

When the user wants to walk away, run execution agents with `run_in_background: true` so they work detached and notify on completion — no polling. Between batches, if you're waiting on a detached agent or external state, use `ScheduleWakeup` to pace the loop rather than blocking. Pick the delay to match what you're waiting on; default to a long idle tick (1200s+) when there's no specific signal. The loop survives across the wait; the user can interrupt any time.

---

## Phase 2 — Gates: STOP for a human

Never cross these without explicit approval in the conversation, even mid-loop. Halt, state exactly what you want to do and why, and wait:

- Editing a **crown-jewel / proposal-gated file** (e.g. `extractor.py` system prompt, `temporal.py` thresholds, `search.py` ranking, `landing/index.html`, `migrations/init.sql`) — these need a proposal first per `CLAUDE.md`.
- **git commit or push** — never auto-commit.
- **DB migrations against a live database**, or running code against live data.
- **Spending money** / creating API keys / anything with a cost.
- Anything **irreversible or outward-facing** (sending a message, deploying, deleting).

A gate in the plan is a hard stop. Approval for one gate is not approval for the next.

---

## Phase 3 — Safety caps

The loop must be unable to run away:

- **Batch cap:** if you've completed the plan's batches, stop — do not invent new scope.
- **Stall cap:** if the same verify step fails **3 times**, stop and report the blocker; do not keep retrying blindly.
- **Drift check:** if a batch would change files not named in the plan, stop and flag it — the plan may be wrong or the task grew.
- **Scope discipline:** implement the plan, not more. New ideas go to the TODO/backlog, not into this run.

---

## Phase 4 — Completion and handoff

When every batch is done and every verify passed:

1. Confirm the success criterion from Phase 0 is actually met — state how you know.
2. Summarise: what shipped, what was verified, what's still gated on a human (approvals not given, migrations not run).
3. Update the plan file (mark batches done) and the TODO list.
4. Hand off to review, verbatim:

   > Build complete and verified. Next is review: run `/ultrareview` (`/code-review ultra`) to deploy sub-agents over the branch. That command is user-triggered and billed — I can't launch it for you. When it returns findings, hand them back and I'll loop the fixes through `/goal`.

If the loop stopped early (gate or cap), say so plainly — what's done, what's blocking, exactly what you need from the user to resume.
