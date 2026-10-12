# How it works

No magic layer. Four plain files and one hook.

## The files

| File | What it is |
|---|---|
| `.claude/output-styles/tutor.md` | The rules. Written to the assistant, readable by you. |
| `.guided-mode/mechanics.md` | How it keeps `LEARNING-LOG.md`, and `break glass`. |
| `.guided-mode/override.md` | Your instructor's course rules. Wins over the rest. |
| `CLAUDE.md` / `AGENTS.md` | Course context. `AGENTS.md` is for Codex. |
| `.guided-mode/reminder.py` | The hook. |

## The chain

1. `.claude/settings.json` sets the output style, so Claude Code loads
   `tutor.md` at startup.
2. On every prompt you send, a `UserPromptSubmit` hook runs `reminder.py`.
3. It reads `tutor.md`, `mechanics.md` and `override.md` and appends them to
   that turn's context.
4. It reads the Learning Goal from the first line of `LEARNING-LOG.md` and
   appends that too. No Goal set means everything is treated as inside it.
5. Codex has no output styles, so there step 2 is the only thing applying the
   rules. Wired in `.codex/hooks.json`.

Repetition is the point: a model that read a policy once has drifted from it by
turn 40.

## Limits

This is context, not a sandbox. Nothing is enforced at the tool level, and the
assistant cooperates because it is asked to. You can work around it, and
`break glass` exists so you do not have to work around anything.

## What leaves your machine

Nothing. `LEARNING-LOG.md` is gitignored and git has never tracked it, so it
cannot be pushed by accident. The hook writes no network traffic and keeps no
state.
