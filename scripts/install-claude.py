#!/usr/bin/env python3
"""Install the commands, skills and agents of this repository for Claude Code.

Source layout (in this repository):
    commands/<name>.md          -> <dest>/commands/<name>.md
    skills/<name>/SKILL.md      -> <dest>/skills/<name>/SKILL.md (whole folder)
    agents/<name>.md            -> <dest>/agents/<name>.md

<dest> is `<target>/.claude` for a project, or `~/.claude` with --global.

Usage:
    python3 scripts/install-claude.py                  # install in the current directory
    python3 scripts/install-claude.py path/to/study-repo
    python3 scripts/install-claude.py --global
    python3 scripts/install-claude.py --dry-run

This script uses only the Python standard library. It works on Windows,
macOS and Linux.
"""

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IGNORED_NAMES = {".gitkeep", ".DS_Store"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Install the commands, skills and agents of this repository for Claude Code."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Project directory that receives the .claude folder (default: current directory).",
    )
    parser.add_argument(
        "--global",
        dest="use_global",
        action="store_true",
        help="Install in ~/.claude instead of a project.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be copied. Do not write any file.",
    )
    return parser.parse_args()


def copy_file(src, dst, dry_run):
    print(f"  {src.relative_to(REPO_ROOT)} -> {dst}")
    if dry_run:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def install_commands(dest, dry_run):
    """commands/*.md -> <dest>/commands/*.md"""
    return install_markdown_files(REPO_ROOT / "commands", dest / "commands", dry_run)


def install_agents(dest, dry_run):
    """agents/*.md -> <dest>/agents/*.md"""
    return install_markdown_files(REPO_ROOT / "agents", dest / "agents", dry_run)


def install_markdown_files(src_dir, dst_dir, dry_run):
    count = 0
    if not src_dir.is_dir():
        return count
    for src in sorted(src_dir.glob("*.md")):
        copy_file(src, dst_dir / src.name, dry_run)
        count += 1
    return count


def install_skills(dest, dry_run):
    """skills/<name>/ -> <dest>/skills/<name>/ (every file, same structure)"""
    count = 0
    src_dir = REPO_ROOT / "skills"
    if not src_dir.is_dir():
        return count
    for skill in sorted(p for p in src_dir.iterdir() if p.is_dir()):
        if not (skill / "SKILL.md").is_file():
            print(f"  skip {skill.relative_to(REPO_ROOT)} (no SKILL.md)")
            continue
        for src in sorted(p for p in skill.rglob("*") if p.is_file()):
            if src.name in IGNORED_NAMES:
                continue
            copy_file(src, dest / "skills" / skill.name / src.relative_to(skill), dry_run)
        count += 1
    return count


def main():
    args = parse_args()
    if args.use_global:
        dest = Path.home() / ".claude"
    else:
        target = Path(args.target).expanduser().resolve()
        if not target.is_dir():
            print(f"error: target directory does not exist: {target}", file=sys.stderr)
            return 1
        if target == REPO_ROOT:
            print("error: target is this repository. Choose a study repository.", file=sys.stderr)
            return 1
        dest = target / ".claude"

    prefix = "[dry run] " if args.dry_run else ""
    print(f"{prefix}Installing into {dest}")

    print("Commands:")
    commands = install_commands(dest, args.dry_run)
    print("Skills:")
    skills = install_skills(dest, args.dry_run)
    print("Agents:")
    agents = install_agents(dest, args.dry_run)

    print(f"{prefix}Done: {commands} commands, {skills} skills, {agents} agents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
