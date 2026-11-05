---
name: select-lesson
description: Select the current lesson of the study repository. Set lesson.current in state.json to a lesson in Lessons/, chosen from the argument (folder name, lesson number, roadmap subsection number or title, or a subject). With no argument, choose the next lesson of the roadmap. Warn the user if the current lesson is not complete. If the chosen lesson does not exist, offer to create it with the new-lesson skill. Use when the user runs /select-lesson or wants to change the current lesson, and from the new-lesson skill.
argument-hint: [lesson folder, lesson number, roadmap subsection, or subject] [--yes]
---

Select the current lesson of the study repository. All paths below are relative to the root of the **study repository** (the current working directory). Only this skill changes `lesson` in `state.json` to a different lesson. `/new-lesson` creates lessons, but it does not select them.

## 0. Read the context

- Read `CLAUDE.md`. Use the language of the study profile when you talk to the user, and follow the language rule. If there is no study profile, tell the user to run `/bootstrap` and stop.
- Read `ROADMAP.md`, if it exists.
- Read `state.json`. If it is missing, use this shape. You write it in step 5:

  ```json
  {
    "lesson": { "current": null, "completed": false },
    "project": { "current": null, "completed": false }
  }
  ```

- List the folders in `Lessons/`. For each lesson folder, find:
  - If it is complete: `completed` in its `progress.json`. If the file is missing, the lesson is not complete.
  - Which roadmap subsection it covers: the `**Covers:**` line of `Theory/1_*/theory.md` (or of `theory.md` for an older lesson with no `Theory/` folder). If no file has a `**Covers:**` line, match the folder name to the closest roadmap subsection title. `**Covers:** none` means that the lesson is not in the roadmap.
- Find the **current lesson**: `lesson.current`, if it is set and its folder exists. Otherwise there is no current lesson. A current lesson is **not complete** if its `progress.json` has `completed: false`. In that case, also note what is not done: the exercises that are not complete, and if the quiz is not complete.

If `$ARGUMENTS` contains `--yes`, remove it from the arguments and remember it. It means that the user already confirmed the change (for example, in `/new-lesson`).

## 1. Find the target

The target is a lesson folder that exists, or a lesson that does not exist yet (a roadmap subsection or a custom subject).

### 1.1 `$ARGUMENTS` is empty: the next lesson of the roadmap

Find the **next subsection**:

- If the current lesson covers a roadmap subsection, go through the `####` subsections of `ROADMAP.md` that come after it, in file order.
- If there is no current lesson, or it covers no subsection, go through all the `####` subsections in file order.
- Pick the first subsection that has no complete lesson.

If you find no subsection (or there is no `ROADMAP.md`), tell the user that there is no next lesson in the roadmap. List the lessons that are not complete. Tell them that they can run `/select-lesson <lesson>` or `/new-lesson <subject>`. Stop.

The target is the lesson that covers the next subsection. If more than one lesson covers it, use the first one that is not complete. If no lesson covers it, the target is the subsection, and the lesson does not exist yet.

Then:

- **The current lesson is complete, or there is no current lesson:** continue with the target. The user does not need to confirm. Go to step 2.
- **The current lesson is not complete, and you did not get `--yes`:** ask the user (with the question tool) what to do:
  - In the question, say that the current lesson is not complete, and what is not done. Tell them that its progress stays in its `progress.json`.
  - Offer "Keep the current lesson" and "Select the next lesson: <target>". If the target does not exist yet, the second option is "Create and select the next lesson: <subsection>".
  - On "Keep the current lesson" (or no answer), do not change `state.json`. Stop.
  - On the second option, the user confirmed the change. Continue as if you got `--yes`. Go to step 2.

### 1.2 `$ARGUMENTS` is not empty

Find the lesson folder in this order:

1. A path or folder name, e.g. `Lessons/03_records` or `03_records`.
2. A lesson number, e.g. `3` or `03`: the folder that starts with `03_`.
3. A roadmap subsection number or title, e.g. `2.3`: the lesson that covers this subsection. If more than one lesson covers it, ask the user which one.
4. A part of a folder name, e.g. `records`.

If no lesson folder matches, the lesson does not exist yet:

- If the argument is a roadmap subsection number or title, the target is that subsection.
- Otherwise, the target is a custom subject: the text of the argument.

## 2. The target lesson does not exist

Skip this step if the target is a lesson folder that exists.

- If you did not get `--yes`, ask the user (with the question tool) if they want to create the lesson:
  - In the question, say that no lesson in `Lessons/` matches the target. Say what the target is: the roadmap subsection (number and title) or the custom subject.
  - If the current lesson is not complete, also say this in the question, and what is not done.
  - Offer "Create and select the lesson" and "Stop". On "Stop" (or no answer), list the lessons that exist, and stop.
- Invoke the `new-lesson` skill with the Skill tool. Give it the subsection number (e.g. `2.3`) or the custom subject, followed by `--select`. `--select` tells `new-lesson` that the user already chose to select the new lesson. At the end, `new-lesson` invokes this skill again, with the new lesson folder and `--yes`.
- Stop after `new-lesson` is finished. Do not change `state.json` here.

## 3. Check the current lesson

- If the target is already the current lesson, tell the user. Correct `lesson.completed` if it is different from `completed` in the `progress.json` of the lesson. Stop.
- If the current lesson is not complete, and you did not get `--yes`:
  - Tell the user which lesson is current, and what is not done. Tell them that its progress stays in its `progress.json`, and that they can select it again later.
  - Ask the user (with the question tool) if they want to change the current lesson. Offer "Change the lesson" and "Keep the current lesson". On "Keep the current lesson" (or no answer), stop.

## 4. Check the target lesson

If the target lesson is already complete, tell the user. You can still select it, for example to review it.

## 5. Update `state.json`

- Set `lesson.current` to `"Lessons/<NN>_<subject>"`, the path relative to the repository root.
- Set `lesson.completed` to the `completed` value in the `progress.json` of the lesson (`false` if the file is missing).
- Do not change other keys.
- Check that `state.json` is valid JSON.

Do not change the lesson files, `ROADMAP.md` or `PROGRESS.md`.

## 6. Report

Reply with:

- The lesson that is now current, and what it covers.
- The lesson that was current before, and if it was complete.
- The next step: study the theory in `Theory/`, do the exercises, then run `/check-lesson`.
