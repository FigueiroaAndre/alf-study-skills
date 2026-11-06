#!/usr/bin/env python3
"""Send one user message to a Claude Code session in the study repository.

The simulated user talks to the kit with this script. Each call is one user
turn. The script starts a new session, or resumes a session with --session.
It appends the message and the answer to a Markdown log file, and prints a
JSON line: {"session_id": ..., "result": ..., "is_error": ..., "duration_s": ...}.

Usage:
    say.py --repo tmp/learning-go --log tmp/logs/03-bootstrap.md "/bootstrap I am ..."
    say.py --repo tmp/learning-go --log tmp/logs/03-bootstrap.md --session <id> "Yes"

The session runs with bypassPermissions, because nobody can answer a
permission prompt. It excludes the CLAUDE.md of the kit repository, because
the study repository is inside it, and a real study repository is not.
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[4]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("message", help="The user message, e.g. '/new-lesson' or an answer.")
    parser.add_argument("--repo", required=True, help="Path of the study repository.")
    parser.add_argument("--log", required=True, help="Markdown log file. The script appends to it.")
    parser.add_argument("--session", help="Session ID to resume. Omit it to start a new session.")
    parser.add_argument("--timeout", type=int, default=3600, help="Timeout in seconds (default: 3600).")
    return parser.parse_args()


def main():
    args = parse_args()
    repo = Path(args.repo).resolve()
    log = Path(args.log).resolve()
    if not repo.is_dir():
        sys.exit(f"Study repository not found: {repo}")

    settings = {"claudeMdExcludes": [str(KIT_ROOT / "CLAUDE.md")]}
    cmd = [
        "claude", "-p",
        "--output-format", "json",
        "--permission-mode", "bypassPermissions",
        "--settings", json.dumps(settings),
    ]
    if args.session:
        cmd += ["--resume", args.session]
    cmd.append(args.message)

    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, timeout=args.timeout)
        stdout, stderr, code = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = f"TIMEOUT after {args.timeout} s"
        code = -1
    duration = round(time.time() - started)

    try:
        data = json.loads(stdout)
    except (json.JSONDecodeError, TypeError):
        data = {"result": stdout, "is_error": True}

    out = {
        "session_id": data.get("session_id", args.session),
        "result": data.get("result", ""),
        "is_error": bool(data.get("is_error")) or code != 0,
        "duration_s": duration,
        "cost_usd": data.get("total_cost_usd"),
    }
    if stderr.strip():
        out["stderr"] = stderr.strip()[-2000:]

    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as fh:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fh.write(f"\n## USER ({stamp}, session {out['session_id']})\n\n{args.message}\n")
        fh.write(f"\n## CLAUDE ({duration} s, error={out['is_error']})\n\n{out['result']}\n")
        if "stderr" in out:
            fh.write(f"\n```\nstderr:\n{out['stderr']}\n```\n")

    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
