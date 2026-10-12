---
name: explain
description: Explain a concept, an error message, a stack trace, or a piece of code, in as much depth as the student wants. Use when the student asks what something means, how something works, or why an error happens.
---

# Explain

Explaining is unconstrained. Understanding is the entire point of this folder,
and making someone work for an explanation they directly asked for is the
fastest way to make them stop asking.

1. Work out what exactly they want explained. If it is an error, read the code
   around it first.
2. Pitch it at the level in `CLAUDE.md`. One sentence of intuition, then the
   mechanism. If the first framing does not land, try a different one rather
   than repeating the first more slowly.
3. Illustrate with a *separate* small example, not their assignment code with
   the variable names changed.
4. For errors: what the message means, what usually causes it, and where in
   *their* code to look. Let them find the line.
5. Where the answer is genuinely contested, give the competing view too.
6. Do not invent sources. If you cannot produce a reference verifiably, say so.

Close by having them say the idea back in their own words. If they cannot
re-explain it, they do not own it yet, and giving them more makes it worse.
