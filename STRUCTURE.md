# STRUCTURE.md

This file describes the folders and files that the commands in `commands/`, the skills in `skills/`, and the agents in `agents/` read and write. All paths are relative to the root of the **study repository** (the repository where you run the commands), not this repository.

## Overview

```
<study-repo>/
├── CLAUDE.md                  # Created by /bootstrap. Study profile, study environment and language rule. You can add teaching guidance.
├── ROADMAP.md                 # Created by /bootstrap (roadmap-builder agent). Detailed scope per subject.
├── PROGRESS.md                # Created by /bootstrap. Checklist of subjects to study.
├── README.md                  # Created by /bootstrap (from skills/bootstrap/assets/README.md, in the profile language). How to use the skills.
├── state.json                 # Created by /bootstrap. Current lesson and current project.
├── Lessons/
│   └── <NN>_<subject>/        # One folder per lesson, e.g. 03_records/
│       ├── quiz.md
│       ├── progress.json
│       ├── assets/            # Optional: images and files for quiz.md
│       ├── Theory/
│       │   ├── 1_<topic>/     # One folder per roadmap bullet
│       │   │   ├── theory.md
│       │   │   ├── practice.md
│       │   │   ├── practice-solution.md
│       │   │   └── assets/    # Optional: images, HTML pages, sample files for the theory
│       │   └── 2_<topic>/
│       │       └── ...
│       └── Exercises/
│           ├── 1_<exercise_name>/
│           │   ├── exercise.md
│           │   ├── <verification file>  # e.g. a test file
│           │   ├── <setup files>        # Optional, e.g. compose.yaml, seed.sql
│           │   ├── assets/    # Optional: illustrations for exercise.md
│           │   └── ...        # Optional starter file, then the student's code
│           └── 2_<exercise_name>/
│               └── ...
├── Teacher/
│   └── <NN>_<subject>/        # Optional. Support files that /teacher creates (diagrams, pages, setups to try)
└── Projects/
    └── <project_name>/        # One folder per project, e.g. library_manager/
        ├── project_description.md
        ├── progress.json
        └── ...                # The student's code
```

## Which command touches which file

| File | `/bootstrap` | `/bootstrap-update` | `/new-lesson` | `/select-lesson` | `/check-progress` | `/commit` |
| --- | --- | --- | --- | --- | --- | --- |
| `CLAUDE.md` | **create** | **update** (add the missing sections and the language rule) | read | read | – | – |
| `ROADMAP.md` | **create** (with the `roadmap-builder` agent) | **update** (headings only), or create | read | read | – | – |
| `PROGRESS.md` | **create** | **update** (headings and checkboxes), or create | read | – | **update** (check items) | – |
| `README.md` | **create** (from `skills/bootstrap/assets/README.md`, translated to the profile language) | **create / replace** | – | – | – | – |
| `state.json` | **create** | **update** (format and sync) | read `lesson` (only to ask to select the new lesson) | **create / update** `lesson` | **update** `lesson` | – |
| `Lessons/<NN>_<subject>/Theory/<N>_<topic>/theory.md` | – | – | **create** (with the `lesson-theory-writer` agent) | read (`**Covers:**` line) | read | – |
| `Lessons/<NN>_<subject>/Theory/<N>_<topic>/practice.md` and `practice-solution.md` | – | – | **create** (with the `lesson-theory-writer` agent) | – | read (with the `lesson-checker` agent) | – |
| `Lessons/<NN>_<subject>/Theory/<N>_<topic>/` (the student's practice files) | – | – | – | – | read (with the `lesson-checker` agent) | read (to find work in progress) |
| `Lessons/<NN>_<subject>/quiz.md` | – | – | **create** | – | read | – |
| `Lessons/<NN>_<subject>/progress.json` | – | **update** (format and missing entries) | **create** | read | **update** | read (to find progress commits) |
| `Lessons/<NN>_<subject>/Exercises/<N>_<name>/exercise.md` and verification file | – | – | **create** (with the `lesson-exercise-writer` agent) | – | read | – |
| `Projects/<project_name>/project_description.md` | – | – | – | – | – | – |
| `Projects/<project_name>/progress.json` | – | **update** (format) | – | – | – | read (to find progress commits) |

`/bootstrap-update` never changes the content of the lessons: the theory, practice, exercise and quiz files, and the student's files. It only changes the format of the files in the table, and it never removes progress.

`/teacher` is not in the table, because it does not change these files. It only creates new support files in `Teacher/`, when they help. It reads `CLAUDE.md`, `ROADMAP.md`, `PROGRESS.md`, `state.json`, and the lesson and project files, to answer the user's questions and to find the lessons that the user did not study yet.

`/commit` does not change the files. It only reads them to write the commit messages. To split the completions of one `progress.json` file into separate commits, it writes the file step by step, and the last step restores the final version.

The check commands never change the student's code or the student's answers in `quiz.md`. They put temporary test files in the scratchpad directory, not in the study repository.

`/check-progress` starts one `lesson-checker` agent for each theory topic and each exercise, and one agent for the whole quiz. The agents run in parallel and only read the files. `/check-progress` then updates `progress.json`, `state.json` and `PROGRESS.md`, and runs `/commit` to record the progress.

## Language of the files

`ROADMAP.md`, `PROGRESS.md`, and the lesson and project files use the language from the study profile in `CLAUDE.md`. Technical terms are not translated. These fixed markers stay in English in all languages, because the commands search for them: `## BEGINNER`, `## INTERMEDIATE`, `## ADVANCED`, `## Section Summary`, `**Practice:**` / `Practice:`, `**Covers:**`, `**Your answer:**` and `Answer key`. The file names, folder names, and JSON keys also stay in English. All JSON keys (in `state.json` and in every `progress.json`) use camelCase.

## Root files

### `PROGRESS.md`

`/bootstrap` creates this file from `ROADMAP.md`. You can edit it. It is a Markdown checklist of the subjects to study.

- `##` headings are levels: `## BEGINNER`, `## INTERMEDIATE` and `## ADVANCED`, in this order.
- `###` headings are sections: `### <N>. <Title>`. Section numbers continue across the levels.
- `####` headings are subsections: `#### <N>.<M> <Title>`. Each subsection has `- [ ]` items.
- The levels, sections, and subsections are the same as in `ROADMAP.md`, with the same numbers and titles.
- An item that starts with `Practice:` is covered by the lesson exercises.
- A list named "Section Summary" at the bottom has one checkbox per `###` section.

Example:

```markdown
# Java Learning Progress

## BEGINNER

### 1. Basics

#### 1.1 Toolchain and running code
- [ ] Install the JDK
- [ ] Run a single file with `java Foo.java`
- [ ] Practice: write and run a small program

## INTERMEDIATE

### 2. Object-Oriented Programming

#### 2.1 Classes and objects
- [ ] Fields, constructors, methods
- [ ] Access modifiers

## ADVANCED

### 3. Concurrency

#### 3.1 Fundamentals
- [ ] Threads and `Runnable`

## Section Summary
- [ ] 1. Basics
- [ ] 2. Object-Oriented Programming
- [ ] 3. Concurrency
```

How the commands use it:

- `/new-lesson` reads the checked items to know what the user already studied. It does not use the checkboxes to choose the next lesson.
- `/check-progress` changes `- [ ]` to `- [x]` for every item in the subsection when the lesson is complete. If all subsections of a `###` section are checked, it also checks the section in "Section Summary". It never unchecks an item.

### `ROADMAP.md`

The `roadmap-builder` agent creates this file. `/bootstrap` starts the agent after it creates `CLAUDE.md`. The agent reads the study profile in `CLAUDE.md`. You can edit the file.

`/new-lesson` (with no subject) takes the first `####` subsection that no folder in `Lessons/` covers. It finds what a lesson covers from the `**Covers:**` line of its theory. Each concept bullet of the subsection becomes one theory topic. The `**Practice:**` bullet is covered by the exercises.

- The headings are the same as in `PROGRESS.md`: `##` levels (`BEGINNER`, `INTERMEDIATE`, `ADVANCED`), `###` sections, and `####` subsections.
- Each subsection has a bullet list of concepts. Most subsections end with a `- **Practice:** ...` bullet.
- The three levels are always present. The user context changes the depth of each level, not the levels.
- Optional `## Project ideas` and `## Suggested order and pacing` sections, and a `**Resources:**` line, come after `## ADVANCED`. They are not copied to `PROGRESS.md`.

Example:

```markdown
# Java Learning Roadmap (Java 25, no Spring)

## BEGINNER

### 1. Basics

#### 1.1 Toolchain and running code
- JDK vs. JRE vs. JVM, and what `javac` and `java` do.
- Source-launcher mode (`java Foo.java`).
- **Practice:** Hello World, then a program that reads command-line args.
```

### `CLAUDE.md`

`/bootstrap` creates this file. It has three parts: the study profile, the study environment, and the rules. The file is in English, because the agent reads it.

```markdown
# CLAUDE.md

## Study profile

- **Language:** English
- **Subject of study:** Java 25

### User context

Senior fullstack engineer with 8 years of experience, mostly TypeScript (Node.js, React) and Python. Has never written Java, but knows object-oriented programming and static types from TypeScript. Wants to learn the Java language as a base for Spring, and then get a backend software engineer position.

## Study environment

- Operating system: macOS
- Environment setup: guided in lesson 1.1. Preferences: VS Code, SDKMAN.

## Rules

- **Language:** communicate with the user in English, and write the study files in English. Use about 80% of ASD-STE100 (Simplified Technical English): short sentences, simple words, active voice, one idea per sentence.
```

- `**Language:**` is the language that the user wants to use, as the English name of the language. It includes the variant when the language has variants that are different in written text (e.g. `English`, `Brazilian Portuguese`, `Simplified Chinese`).
- `**Subject of study:**` is the subject, with the version if the subject has versions (e.g. `Java 25`).
- `### User context` is one paragraph about the user: background (role, experience, known technologies), current experience with the subject, and goals.
- `## Study environment` gives the user's operating system, so the commands can give commands that work on the user's machine. The `Environment setup` line is there only if lesson 1.1 is the setup of the development environment. It gives the user's preferences.
- The language rule says: communicate with the user and write the study files in the profile language, with about 80% of ASD-STE100 (Simplified Technical English). It also says: do not translate technical terms, and keep the fixed markers in English (see [Language of the files](#language-of-the-files)). For a language other than English, the rule uses an adaptation of ASD-STE100, and one paragraph lists the main adaptations for that language.
- If the file already exists, `/bootstrap` keeps its content. It only adds or replaces the `## Study profile` and `## Study environment` sections and the language rule.

You can edit the study profile, and you can add teaching guidance to this file. `/new-lesson` and its agents follow it when they write the theory and the exercises.

### `state.json`

This file points to the current lesson and the current project. `/bootstrap` creates it. If it does not exist, `/select-lesson` creates it.

`/new-lesson` does not change it, so you can create more lessons in advance. At the end, `/new-lesson` asks if you want to select the new lesson. `/select-lesson` sets `lesson.current`. With no argument, it selects the next lesson of the roadmap. It warns you if the current lesson is not complete. If the lesson does not exist, it offers to create it with `/new-lesson`.

```json
{
  "lesson": {
    "current": "Lessons/03_records",
    "completed": false
  },
  "project": {
    "current": "Projects/library_manager",
    "completed": false
  }
}
```

- `/bootstrap` sets `lesson.current` and `project.current` to `null`.
- `current` is a path relative to the repository root, or `null`.
- `completed` is a copy of the `completed` value in the `progress.json` of that folder. The `progress.json` file is the source of truth. The check commands correct `state.json` if the two values are different.
- A selected lesson replaces `lesson.current`. The old folder and its `progress.json` stay as they are.

## Lessons

### Folder name: `Lessons/<NN>_<subject>/`

- `<NN>` is the next free two-digit number (`01`, `02`, …).
- `<subject>` is a short `snake_case` name.

### `Theory/<N>_<topic>/`

- One folder for each concept bullet of the roadmap subsection, in the same order. `<N>` starts at `1` and has no leading zero. `<topic>` is a short `snake_case` name.
- The `lesson-theory-writer` agent writes each folder. `/new-lesson` starts the agents one after another. Each agent reads the theory of the earlier topics, so the topics connect.

#### `theory.md`

The text of one topic. The second line must be a `**Covers:**` line. All topics of a lesson have the same line:

```markdown
# 1. Records basics

**Covers:** PROGRESS.md 1.1 Toolchain and running code
```

`/new-lesson` and `/check-progress` use this line to find the subsection that the lesson covers. A lesson that is not in `PROGRESS.md` uses `**Covers:** none`.

The file ends with a "Common pitfalls" list, a "Key takeaways" list, and a "Further reading" list (documentation, articles, videos).

#### `practice.md`

Two small exercises about the topic, each with the expected result and a hint in a collapsed block. Each exercise gives the name of the file that the student saves in the topic folder. The student does them right after the theory. They are not graded. When the student finishes them, `/check-progress` checks the files in the topic folder, and the topic is complete in `progress.json`.

#### `practice-solution.md`

The solutions of the two exercises in `practice.md`, with a short explanation. It is a separate file, so the student does not see the solutions by accident.

### `Exercises/<N>_<exercise_name>/`

- Up to 10 folders, in order of difficulty. `<N>` starts at `1` and has no leading zero.
- The `lesson-exercise-writer` agent writes each folder. `/new-lesson` starts the agents one after another. Each agent reads all the theory and the earlier exercises, to keep the difficulty progression.
- Each folder has an `exercise.md` with the title, goal, requirements, examples with the exact expected output, a "How to verify" section, and optional hints. It has no solution.
- Each folder has a verification file (e.g. a test file) that the student runs to test the solution. `exercise.md` gives the command. For an exercise that cannot be tested automatically, the folder has a `checklist.md`.
- A folder can also have a starter file with `TODO` markers. The student writes the code in this folder.

### `quiz.md`

- Up to 10 numbered questions about all the theory topics of the lesson.
- Each question has a `**Your answer:**` line. The student writes the answer there.
- The answer key is at the end, in a collapsed block:

```markdown
<details><summary>Answer key</summary>

1. B — one-line explanation.
...

</details>
```

### `progress.json`

```json
{
  "completed": false,
  "theory": [
    { "name": "1_<first_topic>", "completed": false },
    { "name": "2_<second_topic>", "completed": false }
  ],
  "exercises": [
    { "name": "1_<first_exercise_name>", "completed": false },
    { "name": "2_<second_exercise_name>", "completed": false }
  ],
  "isQuizCompleted": false
}
```

- `theory[].name` is the exact theory topic folder name.
- `/check-progress` sets a theory topic to `true` when all the exercises in its `practice.md` are done and correct.
- `exercises[].name` is the exact exercise folder name.
- `/check-progress` sets an exercise to `true` when the code is correct.
- `/check-progress` sets `isQuizCompleted` to `true` when all questions have an answer, even if some answers are wrong.
- `completed` becomes `true` when all theory topics, all exercises and the quiz are complete.

### Support assets

`/new-lesson` and its agents add visual aids and support files only when they help the student more than text does. The rules are in `skills/new-lesson/references/support-assets.md`.

- **Inline aids:** Markdown tables and Mermaid diagrams, in `theory.md`, `practice.md`, `exercise.md` or `quiz.md`.
- **`assets/` folders:** files that a Markdown file links, e.g. an HTML page and its screenshot. A theory topic, an exercise, and the quiz (in the lesson folder) can each have one. The student does not edit them.
- **Setup files:** files at the root of an exercise folder that prepare what the exercise needs but does not teach, e.g. a `compose.yaml` with a database and a `seed.sql`. The `## Setup` section of `exercise.md` lists them and gives the commands.

The check commands do not count the `assets/` folders and the setup files as the student's work.

## Teacher

`/teacher` can create support files to explain a concept: a Mermaid diagram in a Markdown file, a small HTML page and its screenshot, or a setup to try (e.g. a `compose.yaml`). It puts them in `Teacher/<NN>_<subject>/`, a new folder for each concept. It never changes an earlier folder. You can keep the files as notes, or delete them.

## Projects

No skill creates or checks projects yet. This section describes the planned format. `bootstrap`, `select-lesson` and `commit` already use it.

### Folder name: `Projects/<project_name>/`

`<project_name>` is a short `snake_case` name.

### `project_description.md`

The project specification. It has these sections:

- Overview
- Concepts practiced
- Requirements: a numbered list (`R1`, `R2`, …). The project check checks each one.
- Expected behavior
- Suggested structure (optional)
- Constraints
- Stretch goals (optional, they do not block completion)

### `progress.json`

```json
{
  "completed": false
}
```

The project check sets `completed` to `true` when all numbered requirements are met.

### Student code

The student adds all other files in the project folder. The project check reads every file except `project_description.md` and `progress.json`.
