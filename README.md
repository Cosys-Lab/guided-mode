# Your project

Work in here and Claude Code will tutor you instead of doing the work for you.
Ask why something happens and you get a straight answer. Ask it to write your
code and you get a question back.

## Why this exists

Dear students,

The speed at which AI is developing excites us, and more than that, it commands
our respect. In places our own work looks replaceable.

That makes teaching harder. We want to give you a format that is current, and
honest about the tools you will actually use, without skipping the skill
underneath, which is learning itself. And not only learning: examining a claim
critically, finding the alternative nobody mentioned, following a problem to its
cause. Those stay elementary for an engineer, whatever the tooling does next.

So we decided against banning AI. We would rather you stopped vibe coding and
treated AI as executive power: it carries things out, it does not decide them,
and it should never do your thinking.

That is what this repository is. It helps you structure a project and it stands
by you when you are stuck. It does not pre-chew the work.

Using it is voluntary, and nothing is hidden: every instruction we gave your
tutor sits in this folder for you to read.

If you work with it through the course and tell us at the end what it did and
did not do for you, that helps us a great deal.

Take your time with it, and have fun.

## Quickstart

```bash
git clone https://github.com/Cosys-Lab/guided-mode.git my-project
cd my-project
claude
```

Say **yes** when it asks whether you trust this folder. Nothing works if you
say no. (Codex asks the same thing about a hook.)

## First thing it will ask

**What are you here to learn?** Answer it honestly and in one line.

That answer is the only thing scoping any of this, so keep it **smaller than
your project**: the one skill you are building right now, not the whole build.
"How Dijkstra actually works", not "my route planner".

Outside that line, answers come fast and direct: setup, plotting, config,
build errors, git. It tells you straight away instead of making you work it out.

Change the line whenever your focus moves. It is the first line of
`LEARNING-LOG.md` and it is read literally, so keep the
`**Learning Goal:**` prefix.

## What to ask for

| | |
|---|---|
| **hint** | stuck, and you want the smallest nudge |
| **review** | you wrote something and want it torn apart |
| **explain** | a concept, an error, a stack trace, in any depth |
| **check** | test whether you actually understood it |

## Things worth knowing

**It never writes working code for you.** Anywhere in the project, not just
the part you are studying. What you get is the shape: a signature, a docstring
saying what the thing has to do, and comments marking what goes where. The
lines that do the work are yours to type.

Inside your Goal it also makes you work for the reasoning: questions first,
examples on different material, predict before you run. Outside it, it just
tells you.

**Nothing is hidden.** The rules are in `.claude/output-styles/tutor.md`, in
plain English. `HOW-IT-WORKS.md` explains how they are applied, and what the
limits are. Read them.

**`LEARNING-LOG.md` is yours.** It appears on your first session and it is never
committed, so it stays on your machine. Nobody grading you sees it. Edit it
freely; if a line is wrong, fix it.

**Say `break glass`** and the whole thing stops for the rest of the session. No
questions, nothing recorded, normal again next time. To opt out for good, delete
`.claude/`, `.codex/` and `.guided-mode/` from this folder.

## Updates

Your instructor may change the rules during the term.

```bash
git pull
```

## Keeping your work somewhere

Optional, and only if you want it backed up or handed in. Make an empty repo of
your own, then:

```bash
git remote rename origin course
git remote add origin <your empty repo url>
git push -u origin main
```

After that `git push` goes to yours, and updates come from
`git fetch course && git merge course/main`.
