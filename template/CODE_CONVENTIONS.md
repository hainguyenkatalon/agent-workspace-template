# CODE_CONVENTIONS.md

This file is repo-agnostic and human-owned; Codex must not change it unless a human explicitly requests an update. It describes preferred coding and commit practices for the code repos referenced from this workspace via `REPOS.md`.

## Code conventions
- Minimal, purpose-driven edits; avoid speculative churn.
- Preserve legacy behavior unless `SPEC.md` explicitly demands change.
- Each helper script must document usage in its README.
- Prefer fail-fast behavior; do not add fallback logic unless the spec explicitly requires it.

## Commit conventions
- Keep commits scoped to the completed slice.
- Ensure logs or build artifacts remain gitignored before committing.
