# Agent Workspace Template — Codex Working System

This repository is a *manager* for the agent workspace template rather than a working code repo itself. The actual scaffolding files live inside `template/`, keeping the root clean for maintainer docs like this `README.md` and the root `AGENTS.md`.

## Layout

- `template/` – golden copy of the workspace template; do not edit it directly in this repo.
  - `AGENTS.md` — repo-agnostic execution flow and conventions (human-owned; edit sparingly).
  - `REPOS.md` — human-maintained list of codebases (relative paths) where the agent is allowed to work once the workspace is instantiated.
  - `SPEC.md`, `TECHNICAL_NOTES.md`, `SPEC_PROGRESS.md`, `TODO.md`, `TO_HUMAN.md`, `WAY_OF_WORKING.md`, `USER_GUIDE.md`, `CODE_CONVENTIONS.md` — collaboration and coordination docs that start empty and are filled per workspace/slice.
- Root `AGENTS.md` — rules for this template manager itself (including “do not edit \`template/\` without explicit human approval”).

## Creating a new Codex workspace repo

1. From the parent directory of this repo, copy the template into a new folder, for example:
   - `cp -R agent-workspace-template/template ../my-codex-workspace`
2. In the new repo:
   - Remove the inherited `README.md` if you want a project-specific one: `rm README.md`.
   - Rename the folder and initialize git as needed.
   - Fill in `SPEC.md` with the current goals and acceptance criteria for Codex.
   - Populate `REPOS.md` with relative paths to the main code repos the agent is allowed to modify.
3. Commit the new workspace repo. From then on, all day-to-day collaboration docs (specs, TODOs, notes, links to changes) live in that workspace, not in the template manager.

## How Codex uses the template (in a workspace repo)

In each instantiated workspace repo (the copy created from `template/`):

- Read `AGENTS.md` to understand the execution flow and ownership rules.
- Load context from `SPEC.md`, `TECHNICAL_NOTES.md`, `SPEC_PROGRESS.md`, and `TODO.md`.
- Plan and implement changes in thin slices, updating workspace docs as behavior evolves.
- Record open questions, blockers, and suggestions in `TO_HUMAN.md`.
- Keep `USER_GUIDE.md` aligned with current user-visible behavior and access paths.

## Editing rules for this manager

- Do not edit anything under `template/` in this repo unless a human explicitly approves changes (see root `AGENTS.md`).
- Use this repo to evolve the *template itself* in deliberate, version-controlled changes; never treat it as a working project.
- Make all project-specific edits only in instantiated working repos created from `template/`.
