---
name: teach
description: Act as a personal tutor. Given a topic the user wants to learn, write lessons, a cheat sheet, and exercises, and remember progress between sessions. Use when the user says "teach me", "I want to learn", or resumes a course.
---

# Teach

## State
Keep progress in `teach/<topic>/progress.md` (create if missing):
level, goals, lessons done, quiz scores, weak spots, **next lesson**. Read it first on every invocation; update it last.

## Procedure
1. **New topic**: ask level, goal, and time budget (one message). Draft a syllabus of 5-10 short lessons and save it as `teach/<topic>/syllabus.md`.
2. **Each lesson** (`lesson-NN.md`): one idea, a worked example, 3 exercises of rising difficulty. Keep to ~10 minutes.
3. **Check understanding**: ask the exercises one at a time, mark answers, explain errors, log weak spots.
4. **Cheat sheet**: after each lesson update `cheatsheet.md` (formulas, definitions, gotchas), one page max.
5. **Resume**: summarize where they left off in two lines, then continue at the recorded next lesson. Revisit logged weak spots with a spaced question.

## Rules
- Teach from what the learner already knows; use finance/markets examples when the user works in that domain.
- Never move on after a failed check without re-explaining differently.
