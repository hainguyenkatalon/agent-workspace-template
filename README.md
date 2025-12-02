# Agent Workspace Template — Codex Working System

This repository is a *manager* for the agent workspace template rather than a working code repo itself. The actual scaffolding files live inside `template/`, keeping the root clean for maintainer docs like this `README.md` and the root `AGENTS.md`.

If you’re here to *use* Codex with a project, you almost never work inside this repo directly. Instead, you copy `template/` into a new folder to create a workspace repo and run Codex there. See `USER_GUIDE.md` for the full end-to-end flow and examples.

## Layout

- `template/` – golden copy of the workspace template; do not edit it directly in this repo.
  - `AGENTS.md` — repo-agnostic execution flow and conventions (human-owned; edit sparingly).
  - `REPOS.md` — human-maintained list of codebases (relative paths) where the agent is allowed to work once the workspace is instantiated.
  - `SPEC.md`, `TECHNICAL_NOTES.md`, `SPEC_PROGRESS.md`, `TODO.md`, `TO_HUMAN.md`, `WAY_OF_WORKING.md`, `USER_GUIDE.md`, `CODE_CONVENTIONS.md` — collaboration and coordination docs that start empty and are filled per workspace/slice.
- Root `AGENTS.md` — rules for this template manager itself (including “do not edit \`template/\` without explicit human approval”).

For details on creating a workspace repo, filling in `SPEC.md` / `REPOS.md`, daily human workflow, loop advice, and multi-repo setups (including VS Code workspaces), refer to `USER_GUIDE.md`.

## Editing rules for this manager

- Do not edit anything under `template/` in this repo unless a human explicitly approves changes (see root `AGENTS.md`).
- Use this repo to evolve the *template itself* in deliberate, version-controlled changes; never treat it as a working project.
- Make all project-specific edits only in instantiated working repos created from `template/`.
