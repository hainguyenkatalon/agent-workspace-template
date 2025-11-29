VC Template — Codex Working System

This repository is a *manager* for the template rather than the template itself. The actual scaffolding files live inside `template/`, keeping the root clean for maintainer docs (this `README.md`).

Inside `template/` you will find the usual spec documents for agent-driven development:
- `AGENTS.md` — repo-agnostic execution flow and conventions (human-owned; edit sparingly).
- `REPOS.md` — human-maintained list of codebases (relative paths) where the agent is allowed to work.
- `SPEC.md`, `TECHNICAL_NOTES.md`, `SPEC_PROGRESS.md`, `TODO.md`, `TO_HUMAN.md`, `WAY_OF_WORKING.md`, `USER_GUIDE.md` — start empty and should be populated by the human owner per slice.

### Generating a working copy
Manually copy `template/` into a brand-new sibling folder when starting a working repo, e.g. `cp -R template ../new-repo && rm ../new-repo/README.md`. Keep the template itself untouched; adjust the copies inside the working repo instead.

In actual working repos, the style is layered: repo-agnostic (`AGENTS.md`), repo-specific (`REPO_WAY_OF_WORKING.md`), and branch-specific (`WAY_OF_WORKING.md` in each working repo). Spec documents such as `SPEC.md`, `TODO.md`, `TO_HUMAN.md`, and `USER_GUIDE.md` typically live at the root of each working repo rather than under a `specs/` folder; this template follows that layout once instantiated.
