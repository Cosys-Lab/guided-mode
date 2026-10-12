#!/usr/bin/env python3
"""The re-injection hook: reads a hook event on stdin, writes one on stdout.

Its whole job is to put Guided Mode in front of the model on every turn, because
a cooperative model still forgets a policy stated once by turn 40. Drift is the
entire reason this is a hook rather than markdown files alone.

Claude Code also loads the stance as an output style, so there it is belt and
braces. Codex has no output styles, so here this is the only thing keeping the
stance present at all.

Both CLIs share this event name and wire format, so one script serves both.
Stdlib only, and it must never raise: it runs on every prompt the student
submits, so anything it does badly, it does constantly.
"""

import json
import re
import sys
from pathlib import Path

ARMED_DIRNAME = ".guided-mode"
# The stance has to live under .claude/ to work as a Claude Code output style,
# and there is exactly one copy of it, so Codex reads it from there too.
STANCE_PATH = Path(".claude") / "output-styles" / "tutor.md"
MECHANICS_PATH = Path(ARMED_DIRNAME) / "mechanics.md"
# The instructor's per-assignment addendum. Never written by us, and it wins.
OVERRIDE_PATH = Path(ARMED_DIRNAME) / "override.md"
LOG_PATH = Path("LEARNING-LOG.md")
LOG_TEMPLATE_PATH = Path(ARMED_DIRNAME) / "log-template.md"
EVENT_NAME = "UserPromptSubmit"

GOAL_LINE = re.compile(r"^\s*\*\*Learning Goal:\*\*\s*(?P<goal>.+?)\s*$", re.MULTILINE)
# What the seeded Log says before the student has answered. Treated as no Goal at
# all: scoping the stance to a placeholder sentence is worse than not scoping it.
UNSTATED = "not stated yet"
FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)


def armed_root(start):
    """The nearest folder at or above `start` holding a `.guided-mode/`, or None.

    Walking up is what gives the stance the same scope the CLIs give an
    AGENTS.md: the entire tree rooted at the folder that carries it.
    """
    try:
        here = Path(start).resolve()
    except (OSError, ValueError):
        return None
    for folder in (here, *here.parents):
        if (folder / ARMED_DIRNAME).is_dir():
            return folder
    return None


def _read(path):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


NO_GOAL_NOTICE = """## No Learning Goal is set yet

The Learning Goal line in `LEARNING-LOG.md` is still the placeholder, so nothing
has told you what this student is here to learn.

**Until that line is filled in, treat everything in this repo as inside the
Goal, and hold back the whole way.** An unset Goal is not permission to hand
work over. It is the case where you know least about what you would be taking
away from them, so it is the wrong moment to guess generously.

Early in this turn, ask them in one short question what they are here to learn.
Answer whatever they asked first if you can do it without producing their work.
When they tell you, write their answer onto the Learning Goal line yourself."""


def ensure_log(root):
    """Create the Log from its template if the student has not got one yet.

    Done here rather than asked of the model, because asking did not work: the
    instruction sits in several thousand characters of injected context and got
    skipped every time. A file either exists or it does not, so this is not a
    thing to leave to judgement.

    The Log is gitignored, so creating it commits nobody to anything.
    """
    log = root / LOG_PATH
    if log.exists():
        return
    try:
        log.write_text(
            (root / LOG_TEMPLATE_PATH).read_text(encoding="utf-8"), encoding="utf-8"
        )
    except OSError:
        pass  # read-only checkout, or no template. Never break the session.


def learning_goal(root):
    """The student's stated Goal, or "" if they have not written one yet."""
    match = GOAL_LINE.search(_read(root / LOG_PATH))
    if not match:
        return ""
    goal = match.group("goal").strip()
    return "" if UNSTATED in goal.lower() else goal


def context_for(root):
    """Everything the model should be holding this turn, or "" if nothing."""
    stance = FRONTMATTER.sub("", _read(root / STANCE_PATH)).strip()
    if not stance:
        return ""

    parts = [stance]
    goal = learning_goal(root)
    if goal:
        parts.append(
            "## What this student is here to learn\n\n"
            f"{goal}\n\n"
            "This is the only thing the stance is scoped to. Help with anything "
            "outside it freely and directly."
        )
    else:
        # Fail closed. With no Goal the stance has nothing to scope itself to,
        # and staying silent here reads as "nothing is protected".
        parts.append(NO_GOAL_NOTICE)
    for path in (MECHANICS_PATH, OVERRIDE_PATH):
        section = _read(root / path).strip()
        if section:
            parts.append(section)
    return "\n\n".join(parts)


def main():
    try:
        event = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        event = {}
    if not isinstance(event, dict):
        event = {}

    root = armed_root(event.get("cwd") or Path.cwd())
    if root:
        ensure_log(root)
    context = context_for(root) if root else ""
    if context:
        payload = {
            "hookSpecificOutput": {
                "hookEventName": EVENT_NAME,
                "additionalContext": context,
            }
        }
    else:
        payload = {}
    json.dump(payload, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:  # noqa: BLE001 - a broken hook must not break the session
        sys.stdout.write("{}")
    sys.exit(0)
