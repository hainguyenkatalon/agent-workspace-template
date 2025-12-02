#!/usr/bin/env python3
"""
codex_loop.py — opt-in Codex loop runner (example)

This script does **not** run as part of the template by default. It lives in
the root of `agent-workspace-template` so that humans can:

- Read the comments to understand one way to run Codex in a loop, and
- Copy/adapt it into their own workspace or tooling repo if they choose to
  opt in to longer autonomous runs.

High-level behavior
-------------------
- Detect the current Git branch.
- Log each iteration under `specs/<branch>/logs/`.
- On each iteration, call Codex with the prompt:
    "Continue working on this branch."

Configuration (REQUIRED before use)
-----------------------------------
Edit the constants below before running:

    MODEL = ""            # REQUIRED
    REASONING_EFFORT = "" # REQUIRED

Examples (non-exhaustive):
- MODEL:
    gpt-5.1-codex-max, gpt-5, gpt-4.1, gpt-4.1-mini,
    o4-mini, o3-mini, o1 (logprob),
    claude-3-5-sonnet-20241022, gemini-1.5-pro, deepseek-chat
- REASONING_EFFORT:
    "low", "medium", "high", or "auto"

The script will refuse to run if either constant is left empty. This is
intentional: you must choose a model and reasoning effort mindfully each time,
instead of relying on a hard-coded expensive default.

Token usage warning
-------------------
Higher-end models (especially with REASONING_EFFORT="high") can consume a lot
of tokens per iteration. To stay safe:
- Start with a small number of iterations (e.g. 1–3).
- Prefer lighter models for exploratory or low-risk work.
- Monitor your usage/cost dashboards and only scale up once you’re confident
  in the flow.

Where to use this script
------------------------
- Do **not** run it in the `agent-workspace-template` repo itself.
- Instead, copy it into:
  - A workspace repo created from `template/`, or
  - A separate tooling/working-style repo that you control.
- Run it from the root of that repo so that:
  - Git branch detection works, and
  - Logs are written under `specs/<branch>/logs/` in that repo.

Usage example (after copying & editing MODEL / REASONING_EFFORT):

    python codex_loop.py           # uses default iterations=5
    python codex_loop.py  # then edit code if you want a different default

You can tune the number of iterations by changing the default argument of
`loop(iterations: int = 5)` at the bottom of this file.
"""

import subprocess
import sys
import textwrap
from pathlib import Path
from datetime import datetime


def run(cmd, input_text=None):
    return subprocess.run(cmd, input=input_text, text=True, capture_output=True)


def git_branch():
    """Return the current git branch name.

    Handles non-worktree clones, detached HEAD, and common CI envs.
    Fallbacks (in order):
    - `git rev-parse --abbrev-ref HEAD`
    - `git branch --show-current`
    - `git symbolic-ref --quiet --short HEAD`
    - CI env vars (GITHUB_REF_NAME, GITHUB_HEAD_REF, CI_COMMIT_REF_NAME, BRANCH_NAME,
      BUILDKITE_BRANCH, CIRCLE_BRANCH, GIT_BRANCH)
    - Local branch pointing at HEAD (if unique)
    - `detached-<shortsha>`
    """

    # 1) Standard branch lookup
    r = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    b = (r.stdout or "").strip()
    if r.returncode == 0 and b and b != "HEAD":
        return b

    # 2) Modern Git helper
    r = run(["git", "branch", "--show-current"])
    b = (r.stdout or "").strip()
    if r.returncode == 0 and b:
        return b

    # 3) Symbolic ref (quiet)
    r = run(["git", "symbolic-ref", "--quiet", "--short", "HEAD"])
    b = (r.stdout or "").strip()
    if r.returncode == 0 and b:
        return b

    # 4) CI environment fallbacks
    import os
    for key in (
        "GITHUB_REF_NAME",  # branch or tag name
        "GITHUB_HEAD_REF",  # PR source branch
        "CI_COMMIT_REF_NAME",  # GitLab
        "BRANCH_NAME",  # Jenkins
        "BUILDKITE_BRANCH",
        "CIRCLE_BRANCH",
        "GIT_BRANCH",
    ):
        val = os.environ.get(key, "").strip()
        if val:
            return val

    # 5) Try to find a local branch that points at HEAD (unique)
    r = run([
        "git",
        "for-each-ref",
        "--format=%(refname:short)",
        "--points-at",
        "HEAD",
        "refs/heads",
    ])
    candidates = [ln.strip() for ln in (r.stdout or "").splitlines() if ln.strip()]
    if r.returncode == 0 and len(candidates) == 1:
        return candidates[0]

    # 6) As a last resort, create a deterministic name for detached state
    r = run(["git", "rev-parse", "--short", "HEAD"])
    short = (r.stdout or "").strip() or "unknown"
    fallback = f"detached-{short}"
    print(
        f"[codex_tools] Branch not detected (detached or non-worktree). Using '{fallback}'.",
        file=sys.stderr,
    )
    return fallback


def spec_dir_for_branch(branch: str) -> Path:
    return Path("specs") / branch


PROMPT = textwrap.dedent(
    """
    Continue working on this branch.
    """
).strip()

# REQUIRED: choose deliberately before running.
# Examples:
# MODEL options: gpt-5, gpt-4.1, gpt-4.1-mini, o4-mini, o3-mini, o1 (logprob), claude-3-5-sonnet-20241022, gemini-1.5-pro, deepseek-chat
# REASONING_EFFORT options: low, medium, high, auto
MODEL = ""
REASONING_EFFORT = ""


def codex_exec(
    prompt: str,
    log_file: Path,
):
    cmd = [
        "codex",
        "exec",
        "--skip-git-repo-check",
        "--yolo",
        "--model",
        MODEL,
        "-c",
        "tools.web_search=true",
        "-c",
        f"reasoning_effort={REASONING_EFFORT}",
        prompt
    ]
    with open(log_file, "a") as out:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=out, stderr=out, text=True)
        p.wait()
        return p.returncode


def git_changes_pending() -> bool:
    r = run(["git", "status", "--porcelain"])
    return bool((r.stdout or "").strip())


def git_commit(msg: str):
    run(["git", "add", "-A"])
    run(["git", "commit", "-m", msg])


def loop(iterations: int = 5):
    if not MODEL or not REASONING_EFFORT:
        print("[codex_tools] Please set MODEL and REASONING_EFFORT constants before running.", file=sys.stderr)
        sys.exit(1)

    branch = git_branch()
    spec = spec_dir_for_branch(branch)
    spec.mkdir(parents=True, exist_ok=True)
    log_dir = spec / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = log_dir / f"loop-{ts}.log"
    for i in range(1, iterations + 1):
        if (spec / "STUCK.md").exists():
            with open(log_file, "a") as f:
                f.write("[codex_tools] STUCK.md present — stop.\n")
            break
        with open(log_file, "a") as f:
            f.write(f"[codex_tools] iteration {i}/{iterations}\n")
        codex_exec(PROMPT, log_file)
        # if git_changes_pending():
        #     git_commit(f"chore(loop): iteration {i}/{iterations} updates (auto)")
    print(f"[codex_tools] log: {log_file}")


def main():
    loop()


if __name__ == "__main__":
    main()
