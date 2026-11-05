---
description: Check the student's implementation of the current project against its project_description.md and update progress
argument-hint: [optional: explicit request such as "show me how to do R3"]
---

Review the student's work on the **current project** and update their progress.

## 0. Find the current project

- Read `state.json`. If `project.current` is `null`, missing, or its folder doesn't exist, tell the user there is no current project (suggest `/new-project`) and stop.
- Read `<project.current>/progress.json`, which is the source of truth.
- **Re-sync `state.json`:** if its `project.completed` differs from `progress.json`'s `completed`, set it to match and mention the fix.
- If the project is already completed, say so and stop.

## 1. Understand what was asked

Read `<project.current>/project_description.md`, in particular the numbered requirements (R1, R2, …) and the expected behavior. Stretch goals are optional and never block completion.

## 2. Inspect what the student built

- Read all student-written code in the project folder (everything except `project_description.md` and `progress.json`).
- If there's no student code, or only untouched boilerplate, tell the user nothing has been implemented yet and stop.
- Compile and run it (`javac --release 25`, `java ...`, or the build tool if the project uses one). Never modify the student's files. Put any extra test harness or input files in the scratchpad directory, not in the project folder.

## 3. Verify each requirement

For every requirement, decide **met**, **not met**, or **partially met**, based on running the code and reading it:

- Exercise the example input/output from the description and edge cases the requirement implies (invalid input, empty collections, null, boundaries).
- Judge against the requirement as written. A working solution that meets it is correct even if you'd have designed it differently; mention style or idiom issues (e.g. legacy patterns the lessons advised against) as optional suggestions.

For every requirement that isn't fully met:

- Explain **what is wrong and why** (compile error, failing case with the input that breaks it, a misunderstood concept, a behavior that contradicts the requirement).
- Give **tips** and point to the relevant `Lessons/*/theory.md` section so they can fix it.
- **Do not provide the solution** (no corrected code, no full fix). Small illustrative snippets of a *different* example are fine. Only give the answer if the user explicitly asked for it, in `$ARGUMENTS` or in this conversation; even then, don't mark that requirement as done on their behalf.

## 4. Project completion

If **all** numbered requirements are met:

- Set `completed` to `true` in `<project.current>/progress.json`.
- Set `project.completed` to `true` in `state.json`.
- Congratulate the user, mention any stretch goals still open, and say they can run `/new-project` for the next project.

Otherwise leave both as `false`. Use Edit for JSON changes, keep the existing structure, and confirm the files are still valid JSON. Do not edit `PROGRESS.md`.

## 5. Report

End with a compact summary:

- Requirements: ✅ met · ⚠️ partially met · ❌ not met (one line each, with the requirement number)
- What to fix first
- Whether the project is now completed
