---
description: Create a new Java lesson (theory + ordered exercises), for a given subject or the next unchecked item in PROGRESS.md
argument-hint: [subject]
---

Create a new lesson for the Java study repository.

## 0. Check the current lesson

- Read `state.json`. If `Lesson.Current` is set, read `<Lesson.Current>/progress.json`. That file's `Completed` is the source of truth; `state.json`'s `Lesson.Completed` should match it.
- If the current lesson is **not completed**, do not create anything yet. Ask the user (with the question tool) whether they really want to start a new lesson while `<Lesson.Current>` is unfinished. Offer "Yes, create a new lesson" and "No, keep working on the current lesson".
  - On "No" (or no answer), stop and reply with the current lesson path.
  - On "Yes", continue. The unfinished lesson's folder and `progress.json` are left untouched.
- If `Lesson.Current` is `null`, missing, or its folder or `progress.json` doesn't exist, or the lesson is completed, continue without asking.

## 1. Pick the subject

- If `$ARGUMENTS` is not empty, the subject is `$ARGUMENTS`.
- Otherwise, read `PROGRESS.md` and take the first unchecked (`- [ ]`) item, in file order. Skip items that start with "Practice:" unless nothing else is left in that subsection, since those are covered by the exercises. Use the surrounding `###` subsection (and the matching section in `ROADMAP.md`) as the scope of the lesson, so one lesson covers a whole subsection rather than a single bullet.
- Tell the user which subject you picked and why before writing files.

## 2. Create the folder

- Create `Lessons/<NN>_<subject>/`, where `<subject>` is a short `snake_case` name (e.g. `Lessons/03_records/`) and `<NN>` is the next free two-digit number based on the existing folders in `Lessons/` (`01` if empty). If a lesson for the same subject already exists, stop and ask whether to overwrite it.

## 3. Write `theory.md`

Audience: a fullstack engineer strong in JavaScript/TypeScript with **no Java experience**. Follow the guidance in `CLAUDE.md`:

- Start the file with a title and then a line `**Covers:** PROGRESS.md <number> <subsection title>` (e.g. `**Covers:** PROGRESS.md 1.1 Toolchain and running code`). `/check-lesson` uses it to know which `PROGRESS.md` items to check off. For a subject that isn't in `PROGRESS.md`, write `**Covers:** none`.
- Explain the concept and *why* the idiom exists, not just the syntax.
- Relate it to a JS/TS equivalent where a useful analogy exists, and call out where the analogy breaks down.
- Include small, runnable code snippets that each illustrate one idea. Show output in comments where helpful.
- Use idiomatic modern Java 25. Mention the Java version when a feature needs a specific one, and flag preview features (`--enable-preview`). Do not use anything newer than 25.
- Do not introduce Spring or any other framework.
- End with a short "Common pitfalls" list and a "Key takeaways" list.

## 4. Write the exercises

Create `Lessons/<NN>_<subject>/Exercises/` containing **up to 10** exercise folders, ordered by increasing difficulty (fewer is fine if the subject is small; don't pad):

```
Exercises/1_<exercise_name>/exercise.md
Exercises/2_<exercise_name>/exercise.md
...
```

- `<exercise_name>` is `snake_case`.
- Each `exercise.md` contains: a title, the goal, requirements/specification, example input/output or expected behavior, and optional hints. Do **not** include the solution.
- The student writes the Java classes. Add boilerplate (e.g. a class skeleton with `// TODO`, or a `Main.java` with the calls to make) in the exercise folder only when it makes the exercise clearer.
- Everything must run with `java Foo.java` or `javac --release 25`, with no build tool, unless the lesson is about build tooling.
- Early exercises are guided and small; later ones combine concepts and are open-ended.

## 5. Write `quiz.md`

Create `Lessons/<NN>_<subject>/quiz.md` with **at most 10 questions** (fewer is fine; don't pad) that check understanding of `theory.md`:

- Mix question types: multiple choice (options A–D, exactly one correct), true/false, "what does this code print / does it compile?" with a short snippet, and a few open questions ("explain why...", "compare X with its JS/TS equivalent").
- Number the questions and order them roughly from easy to hard. Only ask about things the theory actually covers.
- Leave blanks for the student's answers (e.g. `**Your answer:**`) under each question.
- Put the answer key at the very end, inside a collapsed `<details><summary>Answer key</summary> ... </details>` block, so the student isn't spoiled. For open questions give the key points a good answer should hit, with a one-line explanation for each answer.

## 6. Write `progress.json` and update `state.json`

- Create `Lessons/<NN>_<subject>/progress.json` with one entry in `Exercises` per exercise folder you created (in order, `Name` being the exact folder name), every `Completed` set to `false`:

  ```json
  {
    "Completed": false,
    "Exercises": [
      { "Name": "1_<first_exercise_name>", "Completed": false },
      { "Name": "2_<second_exercise_name>", "Completed": false }
    ],
    "IsQuizCompleted": false
  }
  ```

- Update `state.json` at the repository root so the new lesson becomes the current one. Keep the existing structure and only change these fields:

  ```json
  {
    "Lesson": {
      "Current": "Lessons/<NN>_<subject>",
      "Completed": false
    }
  }
  ```

  `Current` is the path relative to the repository root. If `state.json` is missing, create it with this shape.

## 7. Verify

- Confirm `quiz.md` has no more than 10 questions, and that any code snippets in it behave as the answer key says (run them if in doubt).
- Compile and run any boilerplate you added to confirm it compiles (expected to fail only where the `TODO` is intentional; say so).
- Confirm `progress.json` and `state.json` are valid JSON.
- Do not edit `PROGRESS.md`: `/check-lesson` checks the items off once the lesson is fully completed.

## 8. Report

Reply with the lesson path, a one-line summary of the theory, a list of the exercise names in order, and the number of quiz questions.
