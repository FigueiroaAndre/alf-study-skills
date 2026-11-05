---
name: new-lesson
description: Create the next lesson of the study repository. Find the next ROADMAP.md subsection that has no lesson in Lessons/, or use the subject in the argument. Then create the lesson folder with one theory topic per roadmap bullet (lesson-theory-writer agent), ordered exercises with test files (lesson-exercise-writer agent), a quiz, and progress.json. It does not change state.json: at the end, it asks if the user wants to select the new lesson with the select-lesson skill (with --select, it selects it without a question). Use when the user runs /new-lesson or wants a new lesson, and from the select-lesson skill.
argument-hint: [roadmap subsection number or title, or any subject] [--select]
---

Create a new lesson in the study repository. All paths below are relative to the root of the **study repository** (the current working directory). This skill works for any subject of study. It does not read `state.json` to decide what to create, and it does not change `state.json`. The user can create more lessons in advance. The `select-lesson` skill selects the current lesson.

## 0. Read the context

- Read `CLAUDE.md`. It must have a `## Study profile` section with `**Language:**`, `**Subject of study:**` and `### User context`. If it does not, tell the user to run `/bootstrap` and stop. Also note any teaching guidance in the file.
- Read `ROADMAP.md`. If it is missing and `$ARGUMENTS` is empty, tell the user to run `/bootstrap` and stop.
- Read `PROGRESS.md` if it exists. The checked items show what the user already studied.
- List the folders in `Lessons/`. For each lesson folder, find which roadmap subsection it covers:
  - Read the `**Covers:**` line of `Lessons/<lesson>/Theory/1_*/theory.md`.
  - For an older lesson with no `Theory/` folder, read the `**Covers:**` line of `Lessons/<lesson>/theory.md`.
  - If no file has a `**Covers:**` line, match the folder name to the closest roadmap subsection title. If no subsection matches, the lesson covers nothing.
  - `**Covers:** none` means that the lesson is not in the roadmap.

If `$ARGUMENTS` contains `--select`, remove it from the arguments and remember it. It means that the user already chose to select the new lesson (the `select-lesson` skill sends it). Step 10 uses it.

Write all study files in the language of the study profile, and follow the language rule in `CLAUDE.md`. Use the same language when you talk to the user.

## 1. Pick the lesson

A lesson always covers one `####` subsection of `ROADMAP.md`, or one custom subject.

**`$ARGUMENTS` is empty:**

- Go through the `####` subsections of `ROADMAP.md` in file order. Pick the first subsection that no lesson in `Lessons/` covers.
- A lesson that exists counts as covered, also if the user did not finish it.
- If every subsection has a lesson, tell the user that the roadmap is complete. Tell them that they can run `/new-lesson <subject>` for a custom subject. Stop.

**`$ARGUMENTS` is not empty:**

- If it is a subsection number (e.g. `2.3`) or matches a subsection title, use that subsection. The order of the roadmap does not matter here.
- If it does not match a subsection, it is a custom subject. The lesson is not in the roadmap.
- If a lesson already covers the chosen subsection, ask the user (with the question tool) what to do. Offer "Create a new lesson anyway" and "Stop". On "Stop" (or no answer), reply with the path of the lesson that exists, and stop.

## 2. Plan the theory topics

Each theory topic becomes one folder in `Theory/`.

- **Roadmap subsection:** make one topic for each concept bullet of the subsection, in the same order. Do not make a topic for the `**Practice:**` bullet. The exercises cover it.
- **Custom subject:** split the subject into 2 to 6 topics, from basic to advanced. Use the study profile and `PROGRESS.md` to choose the depth.
- Give each topic:
  - a folder name `<N>_<topic>`: `<N>` starts at `1`, with no leading zero; `<topic>` is a short `snake_case` name in English.
  - a title in the language of the study profile.
  - the full text of its roadmap bullet (for a custom subject, one sentence about the scope).

Tell the user which lesson you picked, and why (next in the roadmap, or from the argument). Show the list of topics. Then continue. Do not wait for an answer.

## 3. Create the folders

- Create `Lessons/<NN>_<subject>/`. `<NN>` is the next free two-digit number, from the folders in `Lessons/` (`01` if the folder is empty or missing). `<subject>` is a short `snake_case` name in English (e.g. `Lessons/03_records/`).
- Create `Lessons/<NN>_<subject>/Theory/` and `Lessons/<NN>_<subject>/Exercises/`.

## 4. Write the theory

Start the `lesson-theory-writer` agent with the Agent tool, **one time for each topic**, in topic order. Start the next agent only after the previous agent is finished. Do not run them in parallel: each agent reads the theory of the topics before it.

Prompt for each agent:

```
Write theory topic <N> of <total> for the study repository at <absolute path of the current working directory>.
Lesson folder: Lessons/<NN>_<subject>
Topic folder: Lessons/<NN>_<subject>/Theory/<N>_<topic>
Topic title: <title>
Topic scope: <full text of the roadmap bullet, or the scope sentence>
Covers line: **Covers:** PROGRESS.md <number> <subsection title>   (or: **Covers:** none)
Roadmap subsection (all bullets, for context):
<the full text of the subsection, including the Practice bullet>
All topics of this lesson, in order:
<N>_<topic>: <title>
...
```

After each agent finishes:

- Check that `theory.md`, `practice.md` and `practice-solution.md` exist in the topic folder.
- If a file is missing, or the agent reports a problem, start the agent again one time with the problem in the prompt. If it fails again, stop and tell the user which topics are done.

## 5. Write the exercises

### 5.1 Plan the exercises

Read all the `theory.md` files of the lesson. Then plan **up to 10** exercises, in order of difficulty. Fewer is good if the subject is small. Do not add exercises only to have more.

- The first exercises are small and guided. They practice one idea each.
- The later exercises combine ideas from more topics. They are more open.
- The last exercises cover the `**Practice:**` bullet of the roadmap subsection, if there is one.
- Each topic is used by at least one exercise.

For each exercise, write: the folder name `<N>_<exercise_name>` (`<N>` starts at `1`, no leading zero; `<exercise_name>` is `snake_case` in English), a title, the topics it practices, and one or two sentences about what it asks and what it adds to the exercise before it.

### 5.2 Start the agents

Start the `lesson-exercise-writer` agent with the Agent tool, **one time for each exercise**, in order. Start the next agent only after the previous agent is finished. Do not run them in parallel: each agent reads the exercises before it, to keep the difficulty progression.

Prompt for each agent:

```
Write exercise <N> of <total> for the study repository at <absolute path of the current working directory>.
Lesson folder: Lessons/<NN>_<subject>
Exercise folder: Lessons/<NN>_<subject>/Exercises/<N>_<exercise_name>
Title: <title>
Topics practiced: <list of topic folders>
What it asks: <the sentences from the plan>
Full exercise plan, in order:
<N>_<exercise_name>: <title> — <what it asks>
...
```

After each agent finishes:

- Check that `exercise.md` and at least one verification file exist in the exercise folder.
- Check that the agent ran the verification against a correct solution and that it passed. The agent reports this.
- If a check fails, start the agent again one time with the problem in the prompt. If it fails again, stop and tell the user which exercises are done.

## 6. Write `quiz.md`

Create `Lessons/<NN>_<subject>/quiz.md` with **at most 10 questions**. Fewer is good. Do not add questions only to have more. The questions check the understanding of all the `theory.md` files of the lesson.

- Mix the question types: multiple choice (options A–D, exactly one correct), true/false, "what does this code do / what is the result?" with a short snippet, and some open questions ("explain why...", "compare X with <a technology from the user context>").
- Number the questions. Put them in order from easy to hard. Ask only about what the theory explains.
- Under each question, add a `**Your answer:**` line for the student.
- Put the answer key at the end, in a collapsed block: `<details><summary>Answer key</summary> ... </details>`. Give a one-line explanation for each answer. For open questions, give the key points of a good answer.

## 7. Write `progress.json`

Create `Lessons/<NN>_<subject>/progress.json`. Add one entry in `exercises` for each folder in `Exercises/`, in order. `name` is the exact folder name. All values are `false`:

```json
{
  "completed": false,
  "exercises": [
    { "name": "1_<first_exercise_name>", "completed": false },
    { "name": "2_<second_exercise_name>", "completed": false }
  ],
  "isQuizCompleted": false
}
```

Do not change `state.json`. Step 10 offers to select the new lesson.

## 8. Verify

- The lesson folder has `Theory/`, `Exercises/`, `quiz.md` and `progress.json`.
- `Theory/` has one folder for each planned topic. Each folder has `theory.md`, `practice.md` and `practice-solution.md`. `practice.md` has no solutions. Each `theory.md` has the same `**Covers:**` line on its second line.
- Each exercise folder has `exercise.md` and a verification file. No exercise folder has a solution.
- `quiz.md` has 10 questions or fewer. The code snippets in it give the results that the answer key says. Run them if you are not sure.
- `progress.json` lists every exercise folder. `progress.json` is valid JSON.
- Do not edit `ROADMAP.md`, `PROGRESS.md` or `state.json`. `/check-lesson` checks the `PROGRESS.md` items when the lesson is complete.

## 9. Report

Reply with:

- The lesson path, and what it covers (roadmap subsection or custom subject).
- The theory topics, in order.
- The exercises, in order, and the command that runs the verification of each one.
- The number of quiz questions.

## 10. Offer to select the new lesson

If you got `--select`, do not ask. Invoke the `select-lesson` skill with the Skill tool, with the arguments `Lessons/<NN>_<subject> --yes`. Then stop.

Otherwise:

- Read `state.json`. If `lesson.current` is set and its folder exists, read the `progress.json` of that lesson.
- Ask the user (with the question tool) if they want to select the new lesson as the current lesson. Offer "Select the new lesson" and "Keep the current lesson".
  - In the question, name the current lesson, or say that there is no current lesson.
  - If the current lesson is not complete (`completed: false` in its `progress.json`), say this in the question. Say what is not done (exercises, quiz). Tell the user that its progress stays in its `progress.json`.
- **"Select the new lesson":** invoke the `select-lesson` skill with the Skill tool, with the arguments `Lessons/<NN>_<subject> --yes`. `--yes` tells it that the user already confirmed the change.
- **"Keep the current lesson"** (or no answer): do not change `state.json`. Tell the user that they can run `/select-lesson Lessons/<NN>_<subject>` later to select the new lesson.
