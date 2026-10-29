---
description: Create a new Java project for the student to build, from a given idea or based on what PROGRESS.md says they've studied
argument-hint: [project idea or extra information]
---

Create a new study project for the Java repository. The student builds it themselves; you only write the description.

## 0. Check the current project

- Read `state.json`. If `Project.Current` is set, read `<Project.Current>/progress.json` (its `Completed` is the source of truth).
- If the current project is **not completed**, do not create anything yet. Ask the user (with the question tool) whether they really want to start a new project while `<Project.Current>` is unfinished. Offer "Yes, create a new project" and "No, keep working on the current project".
  - On "No" (or no answer), stop and reply with the current project path.
  - On "Yes", continue. The unfinished project's folder is left untouched.
- If `Project.Current` is `null`, missing, its folder or `progress.json` doesn't exist, or the project is completed, continue without asking.

## 1. Decide what the project is

First work out what the student has **already studied**: read `PROGRESS.md` and collect every checked (`- [x]`) item, and look at `Lessons/` for context on what was actually taught (`theory.md` files). Only these concepts are in scope.

- **If `$ARGUMENTS` is not empty:** the project is based on the idea or information given. Still check it against the studied concepts. If it needs important concepts the student hasn't studied yet, say which ones and ask whether to continue anyway, simplify the project to fit, or stop.
- **If `$ARGUMENTS` is empty:** propose a project yourself whose scope **uses the lessons the student has completed together**, rather than one single topic. It should feel like a small real program (e.g. a library manager, inventory tracker, text-adventure engine), not a toy snippet. Don't require anything not yet checked in `PROGRESS.md`.
- **If nothing is checked in `PROGRESS.md`:** there's nothing to build on. Tell the user to finish at least one lesson first (`/new-lesson`, `/check-lesson`) and stop, unless they gave an idea in `$ARGUMENTS`.

Tell the user which project you picked and which studied topics it covers before writing files.

## 2. Create the folder

- Create `Projects/<project_name>/`, where `<project_name>` is a short `snake_case` name. If a folder with that name already exists, stop and ask whether to overwrite it or pick another name.

## 3. Write `project_description.md`

Audience: a fullstack engineer strong in JS/TS who is learning Java. Include:

- **Overview:** what the program does and why it is a good exercise.
- **Concepts practiced:** the studied topics it exercises, linked to lessons in `Lessons/` where relevant.
- **Requirements:** a **numbered, checkable list** (R1, R2, …). Each requirement must be specific and verifiable by running the program or reading the code (e.g. "R3: `Inventory.add` throws `IllegalArgumentException` when the quantity is negative"). `/check-project` verifies against this list, so avoid vague wording.
- **Expected behavior:** example input/output, CLI interactions or API usage.
- **Suggested structure:** optional layout of packages/classes. Keep it a suggestion, not the solution.
- **Constraints:** Java 25 only; standard library only (plus whatever build tool or test libraries the student already set up per `PROGRESS.md`); no Spring or other frameworks. It must run with `java`/`javac --release 25` unless a build tool is already checked off.
- **Stretch goals:** optional extras, clearly separate from the requirements.
- **Do not include a solution**, and don't create source files unless a tiny boilerplate genuinely helps.

## 4. Write `progress.json` and update `state.json`

- Create `Projects/<project_name>/progress.json` with exactly:

  ```json
  {
    "Completed": false
  }
  ```

- Update `state.json` at the repository root. Keep the existing structure (including `Lesson`) and only change the `Project` fields:

  ```json
  "Project": {
    "Current": "Projects/<project_name>",
    "Completed": false
  }
  ```

  `Current` is relative to the repository root. If `state.json` or its `Project` key is missing, create it with this shape.

## 5. Verify

- Confirm `progress.json` and `state.json` are valid JSON.
- Confirm every requirement is numbered and checkable, and nothing in the description needs a concept the student hasn't studied.
- Do not edit `PROGRESS.md`.

## 6. Report

Reply with the project path, a short summary, the studied topics it covers, and the number of requirements.
