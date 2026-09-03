#!/usr/bin/env python3
"""Condense a day's Claude Code session transcripts into a readable digest.

Claude Code stores one JSONL transcript per session under ~/.claude/projects/<slug>/.
Those files are large and noisy. This script pulls out, per session active on a
given local date: the project directory, git branch, the user's prompts, the
files created/edited, and a condensed sequence of actions.

Usage:
    python3 find_sessions.py --date 2026-09-02
    python3 find_sessions.py --date 2026-09-02 --project doodlely
    python3 find_sessions.py --date today --exclude-session <id>

Output is Markdown on stdout. Nothing is sent anywhere.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

MAX_PROMPT_CHARS = 600
MAX_ASSISTANT_CHARS = 240
MAX_ACTIONS = 60


def parse_ts(raw: str) -> dt.datetime | None:
    if not raw:
        return None
    try:
        return dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def local_date(ts: dt.datetime) -> dt.date:
    return ts.astimezone().date()


def resolve_date(s: str) -> dt.date:
    s = s.strip().lower()
    today = dt.date.today()
    if s in ("today", ""):
        return today
    if s == "yesterday":
        return today - dt.timedelta(days=1)
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        sys.exit(f"Could not parse date: {s!r}. Use YYYY-MM-DD, 'today', or 'yesterday'.")


def clip(text: str, limit: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def tool_summary(name: str, inp: dict) -> str:
    if not isinstance(inp, dict):
        return name
    if name == "Bash":
        cmd = clip(str(inp.get("command", "")), 160)
        return f"Bash: {cmd}"
    if name in ("Edit", "Write", "NotebookEdit"):
        return f"{name}: {inp.get('file_path') or inp.get('notebook_path') or '?'}"
    if name == "Read":
        return f"Read: {inp.get('file_path', '?')}"
    if name in ("Grep", "Glob"):
        return f"{name}: {inp.get('pattern', '?')}"
    if name == "Task":
        return f"Task: {clip(str(inp.get('description', '')), 80)}"
    if name in ("WebFetch", "WebSearch"):
        return f"{name}: {clip(str(inp.get('url') or inp.get('query') or ''), 100)}"
    if name == "TodoWrite":
        return "TodoWrite"
    return f"{name}"


def extract_text(content) -> str:
    """User/assistant message content -> plain text, or '' if it's tool noise."""
    if isinstance(content, str):
        s = content.strip()
        if s.startswith("<command-message>") or s.startswith("<local-command"):
            return ""
        if s.startswith("Caveat:") or s.startswith("<system-reminder>"):
            return ""
        if s.startswith("Base directory for this skill:") or s.startswith("<command-name>"):
            return ""
        return s
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "\n".join(p for p in parts if p).strip()
    return ""


def process_file(path: Path, target: dt.date):
    """Return session dict if this file had activity on target date, else None."""
    cwd = branch = None
    prompts: list[str] = []
    assistant_notes: list[str] = []
    files_touched: list[str] = []
    actions: list[str] = []
    first_ts = last_ts = None
    matched = False

    try:
        lines = path.read_text(errors="replace").splitlines()
    except OSError:
        return None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue

        if o.get("cwd"):
            cwd = o["cwd"]
        if o.get("gitBranch"):
            branch = o["gitBranch"]

        ts = parse_ts(o.get("timestamp", ""))
        if ts is None:
            continue
        if local_date(ts) != target:
            continue
        matched = True
        first_ts = ts if first_ts is None else min(first_ts, ts)
        last_ts = ts if last_ts is None else max(last_ts, ts)

        typ = o.get("type")
        msg = o.get("message", {}) if isinstance(o.get("message"), dict) else {}

        if typ == "user":
            txt = extract_text(msg.get("content"))
            if txt:
                prompts.append(clip(txt, MAX_PROMPT_CHARS))
        elif typ == "assistant":
            content = msg.get("content")
            txt = extract_text(content)
            if txt:
                assistant_notes.append(clip(txt, MAX_ASSISTANT_CHARS))
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        name = block.get("name", "?")
                        inp = block.get("input", {})
                        actions.append(tool_summary(name, inp))
                        if name in ("Edit", "Write", "NotebookEdit"):
                            fp = inp.get("file_path") or inp.get("notebook_path")
                            if fp and fp not in files_touched:
                                files_touched.append(fp)

    if not matched:
        return None

    return {
        "session_id": path.stem,
        "cwd": cwd or "(unknown)",
        "branch": branch,
        "first_ts": first_ts,
        "last_ts": last_ts,
        "prompts": prompts,
        "assistant_notes": assistant_notes,
        "files_touched": files_touched,
        "actions": actions,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default="today", help="YYYY-MM-DD, 'today', or 'yesterday'")
    ap.add_argument("--project", default=None, help="only sessions whose cwd contains this substring")
    ap.add_argument("--exclude-session", default=None, help="session id to skip (e.g. the current one)")
    ap.add_argument("--projects-dir", default=os.path.expanduser("~/.claude/projects"),
                    help="Claude Code projects directory")
    args = ap.parse_args()

    target = resolve_date(args.date)
    root = Path(args.projects_dir)
    if not root.is_dir():
        sys.exit(f"No projects directory at {root}")

    sessions = []
    for jsonl in sorted(root.glob("*/*.jsonl")):
        if args.exclude_session and jsonl.stem == args.exclude_session:
            continue
        s = process_file(jsonl, target)
        if s is None:
            continue
        if args.project and args.project.lower() not in s["cwd"].lower():
            continue
        sessions.append(s)

    sessions.sort(key=lambda s: s["first_ts"] or dt.datetime.min.replace(tzinfo=dt.timezone.utc))

    print(f"# Claude Code sessions — {target.isoformat()}")
    if args.project:
        print(f"_filtered to project containing: {args.project}_")
    print()
    if not sessions:
        print("No sessions with activity on this date.")
        return

    print(f"{len(sessions)} session(s).\n")
    for i, s in enumerate(sessions, 1):
        span = ""
        if s["first_ts"] and s["last_ts"]:
            span = f' — {s["first_ts"].astimezone():%H:%M}–{s["last_ts"].astimezone():%H:%M}'
        print(f"## Session {i}: {s['cwd']}{span}")
        if s["branch"]:
            print(f"branch: `{s['branch']}`  ·  id: `{s['session_id']}`")
        else:
            print(f"id: `{s['session_id']}`")
        print()

        if s["prompts"]:
            print("**What the user asked:**")
            for p in s["prompts"]:
                print(f"- {p}")
            print()

        if s["files_touched"]:
            print("**Files created / edited:**")
            for f in s["files_touched"]:
                print(f"- `{f}`")
            print()

        if s["actions"]:
            print("**Actions:**")
            shown = s["actions"][:MAX_ACTIONS]
            for a in shown:
                print(f"- {a}")
            if len(s["actions"]) > MAX_ACTIONS:
                print(f"- …and {len(s['actions']) - MAX_ACTIONS} more")
            print()

        if s["assistant_notes"]:
            tail = s["assistant_notes"][-3:]
            print("**Assistant's last notes in the session:**")
            for n in tail:
                print(f"- {n}")
            print()


if __name__ == "__main__":
    main()
