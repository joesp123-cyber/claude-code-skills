---
name: ultrareview
description: "The REVIEW phase (step 4) of the ultraplan → goal → ultrareview loop. Deploys review sub-agents over the current branch/working diff to find correctness bugs and cleanup issues, then reports ranked findings. Use when the user says 'ultrareview', 'ultra review', or wants the just-built code reviewed before shipping. For the billed CLOUD review, the user runs `claude ultrareview` in a terminal; this skill runs the local high-effort multi-agent review in-session."
---

# Ultrareview — Review Phase

You are running the review phase of the four-part build loop:
1. `/ultraplan` — plan the task (Opus 4.8)
2. `/goal` — build the plan (Haiku/Sonnet execute)
3. background agents — the zoom-out
4. **`/ultrareview`** (this skill) — review the finished code, then fixes loop back through `/goal`

## What this does

Invoke the bundled **`code-review`** skill at **ultra / high** effort — i.e. the equivalent of `/code-review ultra`. That deploys independent finder agents across correctness, cross-file contracts, and cleanup angles, verifies the survivors, and returns ranked findings.

Concretely: run the `code-review` skill with the `ultra` argument. Follow its instructions exactly (gather the diff, dispatch finder angles via the Agent tool, verify, report ≤10 findings most-severe first).

## Cloud vs local — be honest about which is running

- **Cloud review** (the real "ultra", billed, deepest): only launchable by the user running **`claude ultrareview`** in a terminal. You cannot launch it from inside a session — if the user wants the cloud review, tell them to run that command.
- **Local review** (what this skill actually runs): the in-session multi-agent `code-review` at high effort. Thorough, but bounded by the session — and if the session limit is hit mid-run, finish the remaining angles inline yourself rather than failing.

State plainly at the start which one is running so the user is never misled into thinking a local pass was the cloud pass.

## Scope note

If the working tree has unrelated uncommitted changes, a raw `git diff HEAD` reviews all of it. When the intent is to review one specific piece of work, isolate that delta first (e.g. diff against an archived pre-change snapshot) and say so — don't silently review the whole pile.

## After findings

Report the ranked findings. For any confirmed bug, offer to loop the fix back through `/goal` (or apply it inline if small). Do not auto-commit — that stays gated on the operator.
