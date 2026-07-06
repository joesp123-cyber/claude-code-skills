---
name: ultraplan
description: "Deploys multiple parallel Opus 4.8 planning agents to produce one battle-tested implementation plan for a non-trivial task, then writes it to a plan file that /goal executes. Use when the user says 'ultraplan', 'ultra plan', 'plan this out', or wants a hard task planned before any code is written. This is the PLAN phase of the ultraplan → goal → ultrareview loop. Always ends by writing a plan file and handing off — never starts coding itself."
---

# Ultraplan — Multi-Agent Planning Phase

You are the planning lead. The user has a non-trivial task. Your job is to turn it into **one ordered, verifiable implementation plan** by deploying several planning agents in parallel, each attacking the problem from a different angle, then synthesising their output into a single plan file.

**You do not write production code in this skill.** The only artefact you produce is the plan. Execution is the `/goal` skill's job.

This is phase 1 of a four-part loop:
1. **`/ultraplan`** (this skill) — plan the task
2. **`/goal`** — code the plan in a loop until complete (can run in the background)
3. **background agents** — zoom out, let `/goal` run detached
4. **`/ultrareview`** — deploy sub-agents to review the finished code

---

## Model

Use **Opus 4.8** (`model: "opus"`) for every planning agent. (Fable is retired — Opus 4.8 is the planning brain now.) Execution agents in `/goal` use cheaper models; planning is where reasoning quality pays off, so spend the good model here.

---

## Phase 0 — Frame the task

1. Restate the task in one sentence. Confirm you have it right.
2. Read the relevant files yourself first (or dispatch an `Explore` agent if the surface area is wide) so the planning agents get real context, not guesses. Name the files that matter.
3. Identify hard constraints from `CLAUDE.md` (repo-root and user-level) that any plan must respect — e.g. crown-jewel files needing a proposal, no auto-commit, archive-before-change, IP separation, GDPR. List them. A plan that violates these is a failed plan.
4. State the success criterion: how will we know the task is *done*?

Do not skip Phase 0. Planning agents with no context produce generic plans.

---

## Phase 1 — Deploy parallel planning agents

Dispatch **3–4 planning agents in parallel** (one message, multiple `Agent` calls), each `model: "opus"`, each with the full task, the file context from Phase 0, and the constraints. Give each a distinct mandate:

- **Architect** — the cleanest implementation structure. What changes where, in what order, what the interfaces are. Prefer generalising existing mechanisms over bolting on special cases.
- **Risk / Contrarian** — every way this breaks. Edge cases, ordering hazards, data-loss risks, things that look done but aren't. What must be verified after each step.
- **Simplicity** — the smallest viable change that satisfies the success criterion. What can be cut, deferred, or reused instead of built. Name existing helpers/patterns to reuse.
- **Sequencer** (use when the task has ≥4 steps or cross-file dependencies) — the correct order of operations, what's independent and parallelisable, what's gated on something else (a DB migration, an API key, an approval).

Each agent returns: ordered steps, per-step verify criterion, risks, and anything it would refuse to do without human sign-off.

> Scaling hook: for very large tasks the user may want these agents in the cloud / on a local server rather than in-session. That infrastructure is separate from this skill. For now run them in-session (parallel foreground). If `run_in_background: true` or `isolation: "remote"` is genuinely warranted, say so — don't pretend a local-server fleet exists when it doesn't.

---

## Phase 2 — Synthesise into one plan

Reconcile the agents' output. Where they disagree, you arbitrate and say why. Produce a single plan:

- **Goal** — one sentence, plus the success criterion.
- **Constraints** — the CLAUDE.md rules that gate this work, quoted.
- **Steps** — ordered, each with: what changes (file + section), why, and a concrete **verify** step (a command, a test, a diff to inspect, byte-identical characterisation where there's no test suite).
- **Batches** — group steps into batches that can each be executed and verified as a unit, so `/goal` can stop and report between them.
- **Gates** — steps that must STOP for human approval before proceeding (crown-jewel edits, DB migrations, git push, spend, anything irreversible or outward-facing).
- **Risks & rollback** — top risks and how to undo each batch.
- **Out of scope** — what this plan deliberately does not do.

---

## Phase 3 — Write the plan file and hand off

1. Write the plan to `plans/YYYY-MM-DD_<slug>.md` (create the `plans/` dir if missing). Use today's date.
2. Print a 5-line summary: goal, number of batches, the gates that will need approval, top risk, and the plan file path.
3. End with the handoff line, verbatim:

   > Plan written to `plans/YYYY-MM-DD_<slug>.md`. Run `/goal plans/YYYY-MM-DD_<slug>.md` to execute it — or `/goal` and I'll pick up the latest plan. It can run in the background while you zoom out.

Do not begin implementation. The user decides when to start `/goal`.
