---
description: Check the student's exercises and quiz answers for the current lesson, give feedback, and update progress
argument-hint: [optional: "show solution for <exercise>" or similar explicit request]
---

Review the student's work on the **current lesson** and update their progress.

## 0. Find the current lesson

- Read `state.json`. If `lesson.current` is `null`, missing, or its folder doesn't exist, tell the user there is no current lesson (suggest `/new-lesson`) and stop.
- Read `<lesson.current>/progress.json`.
- **Re-sync `state.json`:** `progress.json` is the source of truth. If its `completed` differs from `state.json`'s `lesson.completed`, set `lesson.completed` to match it, and mention the fix to the user. If `progress.json`'s `completed` is `false` but every exercise and the quiz are marked completed, set both flags to `true` (see step 4). Do this before anything else, including when there is nothing left to review.
- `progress.json` decides what is checked:
  - Only exercises with `"completed": false` are reviewed. Skip completed ones (just list them as already done).
  - The quiz is only reviewed if `"isQuizCompleted": false`.
- If everything is already completed, say so (after the re-sync above) and stop.

## 1. Report what's missing

Before grading anything, tell the user what has **not been answered**:

- **Exercises:** an exercise counts as not answered when its folder contains no student-written Java code, or only the untouched boilerplate (the `// TODO`s are still there). Read `exercise.md` and the folder contents to decide.
- **Quiz:** a question counts as not answered when its `**Your answer:**` blank is empty. Don't count the answer key.

List the missing exercises and question numbers clearly. Then continue and review everything that *was* answered.

## 2. Review the exercises

For each not-completed exercise that has an answer:

1. Read `exercise.md` (requirements, examples) and the student's code.
2. Compile and run it (`javac --release 25` / `java Foo.java`) and test it against the requirements and the examples in `exercise.md`, including edge cases. Write any extra test harness in the scratchpad directory, never in the lesson folder, and never modify the student's files.
3. Judge correctness against the exercise's requirements. Also note anything that clearly violates the lesson's idioms (e.g. legacy patterns the theory told them to avoid), but a working solution that meets the spec is **correct**.
4. Outcome:
   - **Correct:** set that exercise's `completed` to `true` in `progress.json`. Give a short congratulation and, if useful, one improvement suggestion.
   - **Wrong or incomplete:** leave `completed` as `false`. Explain *what* is wrong (compile error, failing case, misunderstanding of the concept) and give **tips** and pointers to the relevant part of `theory.md` so they can try again.
5. **Do not give the solution** (no corrected code, no full fix) unless the user explicitly asked for it, either in `$ARGUMENTS` or in this conversation. Small illustrative snippets of a *different* example are fine. If they do ask for the solution of a specific exercise, give it, but leave its `completed` as `false`.

## 3. Review the quiz

If the quiz is not completed:

1. Read `quiz.md` and the student's answers. Use the answer key at the bottom to grade, but verify code-based questions yourself if in doubt.
2. For each answered question say whether it is **correct** or **wrong**. For every wrong answer, explain why it is wrong and **give the correct answer** with the reasoning. For open questions, judge against the key points, not exact wording; credit partial answers and explain what was missed.
3. Don't edit the student's written answers in `quiz.md`.
4. Completion: if **every** question has been answered, set `isQuizCompleted` to `true`, **even if some answers were wrong**, because the correct answers were given. If any question is still unanswered, leave it `false` and remind them which ones remain.

## 4. Lesson completion

If after this review every entry in `exercises` has `"completed": true` **and** `isQuizCompleted` is `true`:

- Set `completed` to `true` in `progress.json`.
- Set `lesson.completed` to `true` in `state.json`.
- **Mark the subject as completed in `PROGRESS.md`** (see below).
- Tell the user the lesson is finished and that they can run `/new-lesson` for the next one.

Otherwise leave both as `false` and do not touch `PROGRESS.md`.

### Updating `PROGRESS.md`

- Find which items the lesson covers from the `**Covers:**` line at the top of `<lesson.current>/theory.md` (e.g. `Covers: PROGRESS.md 1.1 Toolchain and running code`). If the line is missing, match the lesson's subject to the closest `###` subsection and tell the user which one you chose.
- Change `- [ ]` to `- [x]` for every item under that subsection, including its "Practice:" item, since the exercises cover it. Change only those lines; edit nothing else in the file and never uncheck anything.
- If every `###` subsection of a `##` section is now checked, also check that section in the "Section Summary" list at the bottom of `PROGRESS.md`.
- If the lesson doesn't correspond to any item (e.g. a custom subject the student asked for), leave `PROGRESS.md` unchanged and say so.
- Also run this step when the re-sync in step 0 finds a fully completed lesson whose items are still unchecked.

## 5. Report

Use Edit for JSON changes, keeping the existing structure, and confirm the files are still valid JSON. End with a compact summary:

- Exercises: ✅ correct (newly completed) · ❌ wrong · ⚠️ not answered · ✔️ already completed earlier
- Quiz: score on answered questions, unanswered question numbers, and whether it is now completed
- What to do next
