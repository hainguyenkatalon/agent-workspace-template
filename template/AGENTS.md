# AGENTS.md

This `AGENTS.md` is repo-agnostic and human-owned. Keep it short. Codex must not change it unless a human explicitly asks.

This repository is a *workspace template* for collaborating with Codex. It lives alongside your main code repos so Codex can take notes, track plans, and coordinate work without touching those repos. `REPOS.md` lists the code repos where Codex may create, read, update, and delete files.

## Workspace docs
All paths are relative to this workspace repo.

Human-maintained:
- `AGENTS.md` — this guide.
- `REPOS.md` — where Codex may work.
- `SPEC.md` — goals and acceptance criteria.
- `WAY_OF_WORKING.md` — cadence for runs, builds, tests.
- `CODE_CONVENTIONS.md` — coding and commit guidelines.

Agent-updated:
- `TECHNICAL_NOTES.md` — entry points, modules, validation tips.
- `SPEC_PROGRESS.md` — high-level done vs remaining.
- `TODO.md` — thin-slice checklist.
- `TO_HUMAN.md` — questions, decisions, suggestions.
- `USER_GUIDE.md` — user-facing value, usage, limits.

## Main flow
1. **Stuck gate** — if `STUCK.md` exists, stop and summarize the block in `TO_HUMAN.md`. If you become blocked, create `STUCK.md` and add the block to both `STUCK.md` and `TO_HUMAN.md`.
2. **TO_HUMAN housekeeping** — read `TO_HUMAN.md`. For each addressed item, update relevant workspace docs, then remove the resolved entry so `TO_HUMAN.md` only holds open items.
3. **Clarify request vs SPEC** — compare the human request with `SPEC.md`. If it is missing, misaligned, or in conflict, explain the mismatch in your reply and ask whether to update `SPEC.md` or treat the request as an explicit exception before changing code.
4. **Plan** — choose the next thin, reversible slice and record it as a clear, testable TODO.
5. **Implement and validate** — make minimal, precise edits for the slice and run appropriate checks.
6. **Update workspace docs** — bring all necessary docs (progress, notes, questions, guides) in line with the new behavior.
7. **Commit & push** — keep commits scoped to the completed slice.

## Reconcile flow (on human request)
Use this when a human asks to “sync/reconcile docs” or drift blocks progress.

1. **Review current state** — read and analyze workspace docs and relevant code to understand actual vs documented behavior.
2. **Align docs** — update all necessary workspace docs so they consistently describe current behavior; log open questions, decisions, and suggestions in `TO_HUMAN.md`.
3. **Confirm changes** — summarize major doc or process changes in `TO_HUMAN.md` for human review.
