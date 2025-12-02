# Agent Workspace Template — How to Use It with Codex

This page explains how to use the `agent-workspace-template` repo as the foundation for working with Codex on real projects.

> **Key idea:**  
> You do **not** work inside `agent-workspace-template` itself.  
> You copy its `template/` folder to create **workspace repos**, and Codex works inside those workspaces (and the code repos listed in `REPOS.md`).

## Concepts

- **Workspace repo** (copy of `template/`)
  - Created per feature/initiative (e.g. `hello-world-workspace`).
  - Holds **only coordination docs** (specs, TODO, notes, etc.).
  - Lives alongside your real code repos.

- **Code repos**
  - Your actual application/code repositories.
  - Listed in the workspace’s `REPOS.md` so Codex knows where it may edit.

- **Codex loop**
  - Repeatedly calls `codex exec` from the workspace root with the same branch checked out.
  - Lets Codex make incremental progress, update docs, and coordinate with you.

## Creating a Workspace Repo

From the parent directory that contains `agent-workspace-template`:

```bash
# 1) Copy the template to a new folder
cp -R agent-workspace-template/template ./my-codex-workspace
cd my-codex-workspace

# 2) Make it a Git repo (Codex uses this for snapshots)
git init
```

At this point, you have a **workspace repo** with these key files:

- `AGENTS.md` – instructions for how Codex should behave in this workspace.
- `SPEC.md` – what you want Codex to achieve (goals, acceptance criteria).
- `REPOS.md` – which code repos Codex is allowed to touch.
- `SPEC_PROGRESS.md`, `TECHNICAL_NOTES.md`, `TODO.md`, `TO_HUMAN.md`,
  `WAY_OF_WORKING.md`, `USER_GUIDE.md`, `CODE_CONVENTIONS.md` – all start empty.

### Optional: VS Code workspace

Add the workspace folder plus each repo from `REPOS.md` to a VS Code workspace so you (and Codex) can navigate everything in one place while keeping responsibilities clearly separated.

## Filling in the Workspace Docs

From the new workspace root:

1. **Define the work in `SPEC.md`**
   - Describe the feature/problem in plain language.
   - Add clear acceptance criteria (what “done” means).
   - Include any constraints (tech stack, performance, rollout, etc.).

2. **Tell Codex where it may work in `REPOS.md`**
   - One repo path per line, **relative to the workspace**. For example:
     ```text
     ../my-service-repo
     ../frontend-repo
     ```
   - These are the only code locations Codex is allowed to modify.

3. **Optionally constrain behavior**
   - `CODE_CONVENTIONS.md` – team-specific coding/commit rules.
   - `WAY_OF_WORKING.md` – how often to run Codex, when to run tests, etc.

4. **Initial commit**
   - Once filled in, commit the workspace:
     ```bash
     git add -A
     git commit -m "chore: bootstrap Codex workspace"
     ```

## What Codex Does in a Workspace

Codex uses the workspace docs as its “control room”:

- Reads `AGENTS.md` for the main flow and rules.
- Reads `SPEC.md` to understand goals and acceptance criteria.
- Maintains:
  - `TODO.md` – thin-slice checklist of concrete tasks.
  - `SPEC_PROGRESS.md` – high-level “done vs remaining”.
  - `TECHNICAL_NOTES.md` – entry points, modules, and validation tips.
  - `TO_HUMAN.md` – questions, decisions, and suggestions for you.
  - `USER_GUIDE.md` – user-facing behavior and usage instructions.

**Typical run loop for Codex (per iteration):**

1. Check if `STUCK.md` exists; if it does, stop and explain the block in `TO_HUMAN.md`.
2. Clean up `TO_HUMAN.md` (resolve already-answered items).
3. Compare your latest request with `SPEC.md` and highlight any mismatch.
4. Choose the next small, reversible slice and record it in `TODO.md`.
5. Make minimal code changes in the allowed repos and run appropriate checks.
6. Update workspace docs (`SPEC_PROGRESS`, `TECHNICAL_NOTES`, `USER_GUIDE`, `TO_HUMAN`).
7. Commit changes (scoped to that slice) and prepare for the next iteration.

## Running Codex in a Loop

This template intentionally does **not** include a loop tool, because long autonomous runs can consume tokens very quickly.

If your team wants longer multi-iteration runs:

- Use the sample `codex_loop.py` script in the root of this repo as a reference. It shows one way to:
  - Call Codex with a fixed prompt (“Continue working on this branch.”) multiple times.
  - Require explicit configuration of `MODEL` and `REASONING_EFFORT` before running.
- Copy and adapt that script into your own workspace or tooling repo, making sure:
  - `MODEL` and `REASONING_EFFORT` are required configuration (no hard-coded expensive default).
  - You start with a low iteration count (1–3) and monitor token usage/cost closely before increasing it.

## Daily Workflow for Humans

When working with Codex via this system:

- **Before runs**
  - Update `SPEC.md` if the goal changed.
  - Add any new questions/decisions you want addressed to `TO_HUMAN.md`.
  - Ensure `REPOS.md` stays accurate.

- **Run a loop**
  - Use the shell loop (or your helper script) for a small number of iterations.
  - Let Codex update code and workspace docs.

- **After runs**
  - Review the diffs in your code repos and workspace.
  - Answer questions in `TO_HUMAN.md`.
  - Decide whether to:
    - Run another loop with the same slice, or
    - Update `SPEC.md` / `TODO.md` for a new slice.

- **When blocked**
  - If Codex creates or updates `STUCK.md`, read it and `TO_HUMAN.md`.
  - Resolve the underlying issue (missing data, unclear requirements, conflicting constraints).
  - Once unblocked, remove or update `STUCK.md` and `TO_HUMAN.md`, then resume loops.

## Advantages

- **Clean main repos** – all agent notes, specs, progress logs, and questions live in the workspace repo, so your main code repos stay focused on code (files, PRs, commits aren’t polluted by agent-only docs).
- **Multi-repo support** – a single workspace can coordinate changes across multiple codebases listed in `REPOS.md`, while still keeping clear boundaries about where Codex may edit.
- **Consistent collaboration model** – every workspace uses the same set of docs and flows, so humans and Codex share a predictable way to plan work, track progress, and resolve questions.

You can paste this page into Confluence (using a Markdown macro or converter) and adapt path examples (e.g. repo names, default models) to match your organization.
