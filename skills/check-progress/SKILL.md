---
name: check-progress
description: Check the student's work on the current lesson of the study repository (the practice of each theory topic, the exercises, and the quiz), give feedback, and update progress.json, state.json and PROGRESS.md. It starts one lesson-checker agent for each theory topic and each exercise, and one for the whole quiz, in parallel. At the end, it commits the progress with the commit skill. Use when the user runs /check-progress or wants their lesson work checked.
argument-hint: [optional: "show solution for <item>" or a similar explicit request]
---

Check the student's work on the **current lesson** and update the progress. All paths below are relative to the root of the **study repository** (the current working directory).

## 0. Read the context

- Read `CLAUDE.md`. Use the language of the study profile when you talk to the user, and follow the language rule. If there is no study profile, tell the user to run `/bootstrap` and stop.
- Read `state.json`. If `lesson.current` is `null` or missing, or its folder does not exist, tell the user that there is no current lesson. Tell them to run `/select-lesson` or `/new-lesson`, and stop.
- Read `<lesson.current>/progress.json`. If the file has no `theory` list (an older lesson), the lesson has no theory topics to check. Do not add the list.
- If `$ARGUMENTS` asks for the solution of an item, remember which item. Also do this when the user asks for it in this conversation.

### Re-sync `state.json`

`progress.json` is the source of truth. Do this before anything else, also when there is nothing to check:

- If `completed` in `progress.json` is different from `lesson.completed` in `state.json`, set `lesson.completed` to the value in `progress.json`. Tell the user about the fix.
- If `completed` in `progress.json` is `false`, but all theory topics, all exercises and the quiz are complete, do step 4 (lesson completion).

### Choose what to check

- Check only the theory topics and the exercises with `"completed": false`. List the completed ones as done before.
- Check the quiz only if `isQuizCompleted` is `false`.
- If all items are complete, say so (after the re-sync), and go to step 6.

## 1. Find what is not answered

Before you start the agents, find the items that have no work from the student. Do not start an agent for them:

- **Theory topic:** the topic folder has no files except `theory.md`, `practice.md`, `practice-solution.md` and the `assets/` folder.
- **Exercise:** the folder has no student code. It has only `exercise.md`, the verification file or `checklist.md`, the setup files from the `## Setup` section of `exercise.md`, the `assets/` folder, and an untouched starter file. A starter file is untouched when it has no change in `git status` (if git is set up), or it has only the `TODO` markers and no real code.
- **Quiz:** every `**Your answer:**` line is empty. Do not count the answer key.

If you are not sure, the item has work. The agent decides.

## 2. Start the agents

Start the `lesson-checker` agent with the Agent tool, **one time for each item with work**:

- one agent for each theory topic,
- one agent for each exercise,
- one agent for the whole quiz.

Start all the agents in **one message**, so they run in parallel. The agents do not change files, so they do not interfere.

Give each agent its own temporary directory in your scratchpad directory (for example, `<scratchpad>/check-progress/exercise-3_bank_account`). If you have no scratchpad directory, use a new temporary directory outside the study repository.

Prompt for each agent:

```
Check one item of a lesson in the study repository at <absolute path of the current working directory>.
Lesson folder: <lesson.current>
Item type: <theory | exercise | quiz>
Item path: <lesson.current>/Theory/<N>_<topic>   (or: <lesson.current>/Exercises/<N>_<name>, or: <lesson.current>/quiz.md)
Temporary directory: <absolute path>
Show the solution: <yes | no>
```

`Show the solution` is `yes` only for the item that the user asked about.

After all agents finish:

- Read the `Result:` line of each report.
- If a report has no `Result:` line, or the agent reports a problem, start the agent again one time with the problem in the prompt. If it fails again, tell the user that you could not check this item, and do not change its progress.

## 3. Update `progress.json`

Use the results of the agents:

- **Theory topic:** `Result: correct` sets its `completed` to `true`. All other results leave it `false`.
- **Exercise:** `Result: correct` sets its `completed` to `true`. All other results leave it `false`. If the user asked for the solution of this exercise, leave it `false`, also if the result is `correct`.
- **Quiz:** `Result: all answered` sets `isQuizCompleted` to `true`, even if some answers are wrong, because the agent gave the correct answers. `not all answered` leaves it `false`.

Never change a value from `true` to `false`. Use Edit, and keep the structure and the format of the file. Check that the file is still valid JSON.

## 4. Lesson completion

If all theory topics, all exercises and the quiz are now complete:

- Set `completed` to `true` in `progress.json`.
- Set `lesson.completed` to `true` in `state.json`. Do not change other keys. Check that `state.json` is valid JSON.
- Update `PROGRESS.md` (see below).
- Tell the user that the lesson is finished. Tell them that they can run `/select-lesson` to go to the next lesson.

Otherwise, leave both values `false`, and do not change `PROGRESS.md`.

### Update `PROGRESS.md`

- Find the subsection that the lesson covers from the `**Covers:**` line of `<lesson.current>/Theory/1_*/theory.md` (for an older lesson with no `Theory/` folder, of `<lesson.current>/theory.md`). For example, `**Covers:** PROGRESS.md 1.1 Toolchain and running code`.
- If there is no `**Covers:**` line, match the lesson subject to the closest `####` subsection. Tell the user which subsection you chose.
- Change `- [ ]` to `- [x]` for every item of that subsection, also the `Practice:` item, because the exercises cover it. Change only those lines. Do not change other lines, and never uncheck an item.
- If all `####` subsections of a `###` section are now checked, also check that section in the "Section Summary" list.
- If the lesson has `**Covers:** none`, or it matches no subsection, do not change `PROGRESS.md`, and tell the user.
- Also do this step when the re-sync in step 0 finds a complete lesson with items that are not checked.

## 5. Report

Show the feedback of each agent, grouped by item type, in this order: theory topics, exercises, quiz. Keep the explanations and the correct answers of the quiz. Then give a compact summary:

- **Theory:** ✅ complete now · ❌ wrong · ⚠️ not answered · ✔️ complete before
- **Exercises:** ✅ complete now · ❌ wrong · ⚠️ not answered · ✔️ complete before
- **Quiz:** the score on the answered questions, the numbers of the questions that are not answered, and if the quiz is now complete
- **Next step:** what the student does next

## 6. Commit the progress

Invoke the `commit` skill with the Skill tool, with no arguments. It makes one progress commit for each completion (theory topic, exercise, quiz, lesson), and a work in progress commit for each item that the student worked on but did not complete.

- If git is not set up, the `commit` skill does nothing. Do not tell the user about it.
- Do this step also when nothing became complete, so the work in progress is recorded.
- After the `commit` skill finishes, show the user the list of progress commits.
