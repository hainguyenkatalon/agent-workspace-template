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
- For a fixed number of iterations, call Codex with the prompt:
    "Continue working on this branch."
  and let it write output to the terminal.

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

Usage example (after copying & editing MODEL / REASONING_EFFORT):

    python codex_loop.py           # uses default iterations=5
    # edit the script if you want a different default

You can tune the number of iterations by changing the default argument of
`loop(iterations: int = 5)` at the bottom of this file.
"""

import subprocess
import sys
import textwrap


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
    p = subprocess.Popen(cmd, text=True)
    p.wait()
    return p.returncode


def loop(iterations: int = 5):
    if not MODEL or not REASONING_EFFORT:
        print("[codex_tools] Please set MODEL and REASONING_EFFORT constants before running.", file=sys.stderr)
        sys.exit(1)

    for i in range(1, iterations + 1):
        print(f"[codex_loop] iteration {i}/{iterations}", file=sys.stderr, flush=True)
        rc = codex_exec(PROMPT)
        if rc != 0:
            print(f"[codex_loop] codex exited with code {rc}, stopping.", file=sys.stderr)
            break


def main():
    loop()


if __name__ == "__main__":
    main()
