---
name: recap
description: Remind the user of their latest progress in the study repository and tell them the most likely next step, so they do not have to read state.json, progress.json, PROGRESS.md or the git log. It reads the current lesson, the last progress commits, and the work that is not checked yet. It does not change any file. Use when the user runs /recap, or asks where they stopped, what they did last, or what to do next.
argument-hint: (no arguments)
---

Tell the user where they stopped and what to do next. All paths below are relative to the root of the **study repository** (the current working directory).

This skill only reads. It never changes a file, it never commits, and it never starts another skill. It only tells the user which command to run.

## 0. Read the context

- Read `CLAUDE.md`. Use the language of the study profile when you talk to the user, and follow the language rule.
- If there is no study profile, tell the user to run `/bootstrap`, and stop.
- Read `state.json`, if it exists. If it has the study profile, or its keys are not in camelCase, the repository uses an older structure. Note it for step 3.
- Read `ROADMAP.md` and `PROGRESS.md`, if they exist.
- List the folders in `Lessons/`. For each lesson folder, read its `progress.json`, and find the roadmap subsection that it covers: the `**Covers:**` line of `Theory/1_*/theory.md` (or of `theory.md` for an older lesson with no `Theory/` folder).

## 1. Find the latest progress

Collect these facts. Skip a fact if its source does not exist.

### Progress commits

If the study repository is a git repository (`git rev-parse --is-inside-work-tree`), run:

```bash
git log -n 10 --format='%ad|%s' --date=short --grep='^progress('
```

- The first line is the **last recorded progress**: the date, the lesson or project, and the item.
- Count the days from that date to today. The user can come back after a long break. Then a short reminder of the lesson subject helps.
- Also run `git log -1 --format='%ad|%s' --date=short` to find the date of the last commit of any kind.

If there are no progress commits, or there is no git, use only `progress.json`.

### The current lesson

- The current lesson is `lesson.current` in `state.json`, if it is set and its folder exists.
- From its `progress.json`, find:
  - the theory topics that are complete, and the first one that is not complete,
  - the exercises that are complete, and the first one that is not complete,
  - if the quiz is complete,
  - if the lesson is complete.
- Get the title of each item: the first heading of its `theory.md` or `exercise.md`.

### Work that is not checked yet

The student can do work after the last `/check-progress`. Find it in the current lesson, for each item that is **not complete** in `progress.json`. Use the same rules as `/check-progress` (see `../check-progress/SKILL.md`, relative to the folder of this skill):

- **Theory topic:** the topic folder has files other than `theory.md`, `practice.md`, `practice-solution.md` and the `assets/` folder.
- **Exercise:** the folder has student code. The verification file, `checklist.md`, the setup files, the `assets/` folder and an untouched starter file are not student code.
- **Quiz:** at least one `**Your answer:**` line has an answer. Do not count the answer key.

If git is set up, also run `git status --porcelain -- Lessons/ Projects/`. Changed or new files show the latest work, also when it is not committed.

Do not check if the work is correct. That is the job of `/check-progress`.

### The current project

If `project.current` is set and its folder exists, read its `progress.json`. Note if it is complete.

## 2. Find the most likely next step

Use the first rule that matches:

1. **The repository uses an older structure** (see step 0): run `/bootstrap-update`.
2. **There is no current lesson:**
   - If no lesson exists: run `/new-lesson`.
   - Otherwise: run `/select-lesson`. It selects the next lesson of the roadmap.
3. **The current lesson has work that is not checked yet:** run `/check-progress`. Name the items with work.
4. **The current lesson is not complete:** continue in the study order of the lesson. Give the path of the file to open:
   1. The first theory topic that is not complete: read `theory.md`, then do `practice.md`.
   2. Else, the first exercise that is not complete: read `exercise.md`.
   3. Else, the quiz: answer the questions in `quiz.md`.

   Then say that `/check-progress` checks the work. Say that `/teacher <question>` helps if the user is blocked.
5. **The current lesson is complete:** find the next roadmap subsection, as `/select-lesson` does with no argument (see `../select-lesson/SKILL.md`, step 1.1). Only read. Do not change `state.json`.
   - If a lesson covers it: run `/select-lesson`. Name the lesson.
   - If no lesson covers it: run `/select-lesson`. It offers to create the lesson. Name the subsection (number and title).
   - If there is no next subsection: the roadmap is complete. Congratulate the user. Tell them that they can run `/new-lesson <subject>` for a subject outside the roadmap.

If other lessons are not complete (not the current one), mention them in one line. Do not suggest them as the next step.

## 3. Report

Keep the report short. The user wants to start again quickly. Use this form:

- **Last progress:** the last progress commit, with its date and how many days ago. For example: `complete exercise 3_bank_account in 03_records, 4 days ago`. If there is no git, use the last complete item in `progress.json`, with no date.
- **Current lesson:** the folder, the roadmap subsection that it covers, and a compact status:
  - Theory: `2/4` complete
  - Exercises: `3/8` complete
  - Quiz: complete or not complete
- **Not checked yet:** the items with work that `/check-progress` did not check. Skip this line if there are none.
- **Roadmap:** the number of complete subsections in `PROGRESS.md`, of the total, and the level (`BEGINNER`, `INTERMEDIATE` or `ADVANCED`) of the current lesson.
- **Current project:** only if one is set.
- **Next step:** one action, with the file path or the command. Add one sentence that says why.

If the last progress is more than 14 days ago, add one sentence before the next step: the subject of the current lesson, and the title of the last item that the user completed. This helps the user to remember. Do not add a review of the theory.

Do not show the content of `practice-solution.md`, of the quiz answer key, or of other solutions.
