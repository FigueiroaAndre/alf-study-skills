---
name: bootstrap-update
description: Update a study repository that an older version of the study skills set up. Find what is outdated (study profile in state.json, no Study environment section, old language rule, PascalCase JSON keys, progress.json without theory list or with missing entries, state.json out of sync, old ROADMAP.md or PROGRESS.md format, missing README.md, old commands in .claude/commands), ask only for the missing facts (with the same questions as bootstrap), and update the files to the current structure. It never changes the content of the lessons. It changes only CLAUDE.md, state.json, the progress.json files, ROADMAP.md and PROGRESS.md headings and checkboxes, README.md and old command files. Use when the user runs /bootstrap-update, or after they install a new version of the skills in an existing study repository.
argument-hint: [--check] [any extra information, e.g. your language or operating system]
---

Update an existing study repository to the current structure. All paths below are relative to the root of the **study repository** (the current working directory). `STRUCTURE.md` of the study skills repository describes the current structure.

This skill uses parts of the `bootstrap` skill. Its file is `../bootstrap/SKILL.md`, next to the folder of this `SKILL.md`. Read it before you start. Below, "bootstrap step N" means step N of that file.

## Rules

- **Do not change the content of the lessons.** Do not change, move, rename or delete these files: `theory.md`, `practice.md`, `practice-solution.md`, `quiz.md`, the files in `Exercises/`, the files in `Projects/` (except `progress.json`), and the student's files. Do not add a `**Covers:**` line. Do not move an old `theory.md` into a `Theory/` folder.
- You can change only these files: `CLAUDE.md`, `state.json`, `Lessons/*/progress.json`, `Projects/*/progress.json`, `ROADMAP.md` and `PROGRESS.md` (only the headings, the format and the checkboxes, see step 1.5), `README.md`, and the old command files in `.claude/commands/` (see step 1.7).
- **Never lose progress.** Never change a `true` value to `false`. Never uncheck a `- [x]` item. When you are not sure, keep the value and ask the user.
- Ask before you replace or delete a file that the user may have changed (`ROADMAP.md`, `PROGRESS.md`, `README.md`, old commands).
- Do not change files before the user confirms the plan in step 4.

## 0. Read the context

- If `$ARGUMENTS` contains `--check`, remove it and remember it. With `--check`, you only find and report what is outdated (steps 1 and 2). You do not ask questions, and you do not change files.
- Read the rest of `$ARGUMENTS`. The user can give facts there (language, operating system, background). Use them, and do not ask again for them.
- Make sure that the study repository is not empty. If there is no `CLAUDE.md`, no `state.json`, no `ROADMAP.md`, no `PROGRESS.md` and no `Lessons/` folder, the repository was never set up. Tell the user to run `/bootstrap`, and stop.
- If the repository is a git repository, run `git status`. If there are changes that are not committed, tell the user that it is safer to commit them first (with `/commit`), so they can compare the result of the update. Ask (with the question tool) "Continue anyway" or "Stop". On "Stop" (or no answer), stop. Skip this question with `--check`.

### The language for this conversation

Use the `**Language:**` line of the study profile in `CLAUDE.md`, if there is one. If there is no such line, use the language of `$ARGUMENTS` if it is clear, and English in other cases. Step 3.1 asks for the language if it is missing.

## 1. Find what is outdated

Read the files and make a list of the problems. Do not change files in this step. For each item below, note the problem and the planned fix.

### 1.1 `CLAUDE.md`

Compare the file with the format in bootstrap step 5:

- **No file, or no `## Study profile` section.** Older versions kept the study profile in `state.json`. Look for the profile facts in these places:
  - The old profile keys in `state.json`, also with PascalCase names: `subjectOfStudy`, `technicalLevel`, `subjectFamiliarity`, `goal` (or `SubjectOfStudy`, `TechnicalLevel`, …).
  - The title of `ROADMAP.md` (e.g. `# Java Learning Roadmap (Java 25, no Spring)`) for the subject and the version.
  - Other text in `CLAUDE.md`, e.g. teaching guidance such as "Audience: a fullstack engineer strong in TypeScript with no Java experience".
- **No `**Language:**` line.** Older versions wrote all files in English.
- **No `**Subject of study:**` line, or no `### User context` paragraph**, or the paragraph is empty.
- **No `## Study environment` section, or no `Operating system` line.**
- **The `Environment setup` line does not match the roadmap.** The line must be there only if subsection `1.1` of `ROADMAP.md` is the setup of the development environment.
- **No language rule, or an old language rule.** The current rule is in bootstrap step 5. For English, it names ASD-STE100 and says to write the study files in English. For other languages, it also says not to translate technical terms, it lists all the fixed markers (`## BEGINNER`, `## INTERMEDIATE`, `## ADVANCED`, `## Section Summary`, `Practice:`, `**Covers:**`, `**Your answer:**` and `Answer key`), and it has a paragraph of adaptations for the language.

Keep all other content of `CLAUDE.md`, e.g. the teaching guidance.

### 1.2 `state.json`

The current format is in bootstrap step 6. Look for:

- No file.
- The old profile keys: `language`, `subjectOfStudy`, `technicalLevel`, `subjectFamiliarity`, `goal` (also with PascalCase names). Move their facts to `CLAUDE.md`. Then remove them.
- PascalCase keys, e.g. `Lesson`, `Current`, `Completed`, `Project`. The current keys are camelCase: `lesson`, `current`, `completed`, `project`.
- No `lesson` key or no `project` key.
- `lesson.current` or `project.current` points to a folder that does not exist.
- `lesson.completed` or `project.completed` is different from `completed` in the `progress.json` of that folder. `progress.json` is the source of truth.

### 1.3 `Lessons/*/progress.json`

The current format is in `STRUCTURE.md` and in step 7 of the `new-lesson` skill. For each lesson folder, look for:

- **No `progress.json`.** Plan a new file with all values `false`. If all the items of the subsection that the lesson covers are checked in `PROGRESS.md`, the lesson was probably complete. Note it. Step 3.4 asks the user.
- **PascalCase keys:** `Completed`, `Theory`, `Exercises`, `Name`, `IsQuizCompleted`. The current keys are `completed`, `theory`, `exercises`, `name`, `isQuizCompleted`. Keep all the values.
- **No `theory` list:**
  - If the lesson has no `Theory/` folder (an older lesson with `theory.md` at the lesson root), this is correct. The other skills know this format. Do not add the list.
  - If the lesson has a `Theory/` folder, add one entry for each folder in `Theory/`, in order. The value of each entry is `true` if the lesson is complete (`completed: true`), and `false` in other cases.
- **Missing entries:** a folder in `Theory/` or `Exercises/` with no entry in the list. Add an entry at the right position. The value is `true` if the lesson is complete, and `false` in other cases.
- **Entries with no folder:** an entry whose `name` matches no folder. Do not remove it. Note it. Step 3.4 asks the user.
- **No `isQuizCompleted`.** Add it. The value is `true` if the lesson is complete, and `false` in other cases.
- **A complete lesson that is not marked:** all theory topics, all exercises and the quiz are `true`, but `completed` is `false`. Set `completed` to `true`.
- Do not judge the student's work. Only `/check-progress` does that.

### 1.4 `Projects/*/progress.json`

For each project folder, look for PascalCase keys (`Completed`) and a missing `completed` key. Do not create `progress.json` for a project that has none. Note it in the report.

### 1.5 `ROADMAP.md` and `PROGRESS.md`

The current formats are in bootstrap step 8 and in the `roadmap-builder` agent. Check both files:

- **The file is missing.**
  - No `ROADMAP.md`: plan to build it with the `roadmap-builder` agent (step 5.5). Warn the user that the new roadmap can have different subsection numbers than the `**Covers:**` lines of the lessons.
  - No `PROGRESS.md`: plan to build it from `ROADMAP.md`, as in bootstrap step 8. Then check the items of the complete lessons (see below).
- **Old heading format.** The current format has three levels (`## BEGINNER`, `## INTERMEDIATE`, `## ADVANCED`), `### <N>. <Title>` sections and `#### <N>.<M> <Title>` subsections. An older file can have the sections as `##` and the subsections as `###`, with no levels. Plan to convert the file:
  - Move each section and each subsection down one heading level.
  - Put the sections under the three levels. Choose the level of each section from its content, in order. Each level gets at least one section. The order of the sections does not change.
  - **Keep the numbers and the titles of the sections and subsections.** The `**Covers:**` lines of the lessons refer to them.
  - Keep all bullets, all items and all checkboxes as they are.
- **Missing fixed markers.** `**Practice:**` in `ROADMAP.md`, `Practice:` items and a `## Section Summary` list at the end of `PROGRESS.md`. Plan to add the missing `## Section Summary`. A section is checked in the summary only if all its subsections are checked.
- **The two files do not match.** A subsection is in one file and not in the other. Note it. Step 3.4 asks the user if you add the missing subsection to `PROGRESS.md`. Never remove a subsection.
- **Checkboxes out of sync.** A complete lesson (`completed: true`, or planned as complete in step 1.3) covers a subsection, but some items of the subsection are not checked. Plan to check them, as in step 4 of the `check-progress` skill. Find what a lesson covers from the `**Covers:**` line of `Theory/1_*/theory.md` (or of `theory.md` for an older lesson). Never uncheck an item.
- **The language of the files.** If the profile language is not the language of the two files, note it. Step 3.4 asks the user.

### 1.6 `README.md`

The current `README.md` comes from `../bootstrap/assets/README.md`. Check:

- No `README.md`: plan to write it, as in bootstrap step 9.
- A `README.md` from an older version, or one that is different from the current asset: for English, compare it with the asset. For other languages, compare the sections and the commands with the asset. Plan to replace it. Step 3.4 asks the user.
- A `README.md` that the user wrote (it is not about how to use the skills): keep it. Step 3.4 asks the user if you replace it.

### 1.7 Old files in `.claude/`

The install script copies the new files, but it does not delete the old ones. Look in `.claude/commands/` for these files from older versions:

- `check-lesson.md`, `check-project.md`, `new-lesson.md`, `new-project.md`
- `check-lesson-old.md`, `check-project-old.md`, `new-lesson-old.md`, `new-project-old.md`

An old `new-lesson.md` command has the same name as the `new-lesson` skill. It can run the old process. Plan to delete these files. Step 3.4 asks the user. Do not touch other files in `.claude/`.

Also check that `.claude/skills/` has the current skills: `bootstrap`, `bootstrap-update`, `check-progress`, `commit`, `new-lesson`, `select-lesson`. If one is missing, tell the user to run the install script again (see `README.md` of the study skills repository), and stop.

## 2. Report what is outdated

Show the user a short list, grouped by file, of what is outdated and the planned fix. Also list what is already up to date.

- If nothing is outdated, tell the user that the repository is up to date, and stop.
- With `--check`, stop here.

## 3. Gather the missing facts

Ask only for the facts that you need for the planned fixes, and that you do not have. Follow the order and the rules of bootstrap steps 1 to 3. Use the facts from step 1.1 and from `$ARGUMENTS` first, and do not ask again for a fact that is already clear.

### 3.1 Language

If the profile has no `**Language:**` line, ask for the language, as in bootstrap step 1. This is the first question, alone in its own question tool call. Put the language of the current study files first (English for older versions). Ask for the variant if needed, as in bootstrap step 1.

In the question, tell the user that the lessons that exist stay in their language. Only new lessons use the chosen language.

From this point, use the chosen language for all questions and all replies.

### 3.2 Study profile

Do this only if the study profile is missing, or a part of it is missing.

- **Subject of study:** take it from the old `subjectOfStudy` key or from the title of `ROADMAP.md`. Ask only if you find neither.
- **User context:** write the paragraph from the old keys and the other text in `CLAUDE.md`. The old keys give levels, not facts. For example, `technicalLevel: "advanced"` and `subjectFamiliarity: "beginner"` mean a senior person who is new to the subject. If you do not know the role, the years of experience or the known technologies, ask the user to describe the background in one or two sentences, as in bootstrap step 2. Ask the experience with the subject and the goals with the question tool only if you have no facts about them.
- Do not ask about the version or the scope (bootstrap step 3). The roadmap already sets them. Ask about them only if you build a new `ROADMAP.md` (step 5.5).

### 3.3 Study environment

Do this only if the `## Study environment` section or its `Operating system` line is missing.

- **Operating system:** ask as in bootstrap step 2, in the same question tool call as the profile questions.
- **Environment setup:** do not ask. The roadmap already exists. If subsection `1.1` of `ROADMAP.md` is the setup of the development environment, write the `Environment setup` line with the tools from that subsection as the preferences. In other cases, do not write the line.
- If you build a new `ROADMAP.md` (step 5.5), ask the environment setup question as in bootstrap step 2.

### 3.4 Decisions

Ask these questions with the question tool, in one call (at most 4 questions per call). Ask only the questions that apply. Put the option you recommend first.

- **Old heading format in `ROADMAP.md` or `PROGRESS.md`:** "Convert the headings (keep the content)" (recommended), "Rebuild ROADMAP.md with the roadmap-builder agent" (the subsection numbers can change, and the `**Covers:**` lines of the lessons can stop matching), "Keep the file as it is" (the skills can fail to read it).
- **Missing subsections in `PROGRESS.md`:** "Add them" or "Keep the file as it is".
- **Language of `ROADMAP.md` and `PROGRESS.md`:** if the profile language is not the language of the files: "Keep the files in their language" (recommended) or "Translate the files". A translation keeps the numbers, the structure, the checkboxes and the fixed markers in English, as in bootstrap step 8.
- **`README.md` from an older version, or a different one:** "Replace it with the current version" or "Keep it".
- **Old command files:** "Delete them" (recommended) or "Keep them".
- **A lesson with no `progress.json`, and all its items checked in `PROGRESS.md`:** "Mark the lesson as complete" or "Mark the lesson as not complete". With "complete", all values in the new `progress.json` are `true`.
- **Entries in `progress.json` with no folder:** "Keep the entries" (recommended) or "Remove the entries". Name the lesson and the entries.

If the user cannot answer a question, use the recommended option, as in bootstrap step 3.

## 4. Confirm the plan

Show the user a summary:

- The study profile (language, subject of study, user context) and the study environment, if you write or change them.
- For each file, the changes that you will make.
- The files that you will not change.

Ask (with the question tool) "Is this correct?" with "Yes, update the files", "No, change something" and "Stop". On "No, change something", ask what to change and repeat this step. On "Stop" (or no answer), stop without changes.

## 5. Update the files

Do the updates in this order. Use Edit for small changes, so you keep the format of the files.

### 5.1 `CLAUDE.md`

Write the missing parts as in bootstrap step 5: the `## Study profile` section, the `## Study environment` section, and the language rule. Follow the rules of bootstrap step 5 for a file that already exists. Do not remove other content.

If the old teaching guidance in `CLAUDE.md` repeats the user context (e.g. "Audience: …"), do not remove it. Tell the user in the report that they can remove it.

### 5.2 `state.json`

- If the file is missing, create it as in bootstrap step 6.
- Rename the PascalCase keys to camelCase. Keep the values.
- Remove the old profile keys, after their facts are in `CLAUDE.md`.
- Add a missing `lesson` or `project` key with `"current": null` and `"completed": false`.
- If `current` points to a folder that does not exist, set `current` to `null` and `completed` to `false`. Tell the user.
- Set `lesson.completed` and `project.completed` to the `completed` value in the `progress.json` of the folder. Do this after step 5.3, so you use the updated values.
- Do not select a lesson. Only the `select-lesson` skill does that.
- Check that `state.json` is valid JSON.

### 5.3 `progress.json` files

Do the fixes from steps 1.3 and 1.4, with the answers from step 3.4.

- Keep the key order of the current format: `completed`, `theory`, `exercises`, `isQuizCompleted`. Use two spaces of indentation, and one line for each entry, as in step 7 of the `new-lesson` skill.
- Keep every `name` exactly as it is.
- Check that each file is valid JSON.
- For each file, check that no value changed from `true` to `false`.

### 5.4 `PROGRESS.md` and `ROADMAP.md`

Do the fixes from step 1.5, with the answers from step 3.4.

- When you convert the headings, change only the heading lines, add the level headings, and add the missing `## Section Summary`. Do not change the bullets, the items or their text.
- Check the items of the complete lessons, and the sections in "Section Summary" whose subsections are all checked. Change only `- [ ]` to `- [x]`.
- When you translate, follow bootstrap step 8 for `PROGRESS.md`, and the language rules of the `roadmap-builder` agent for `ROADMAP.md`. Keep every checkbox as it is.

### 5.5 A new `ROADMAP.md`

Do this only if `ROADMAP.md` is missing, or the user chose to rebuild it. Ask the scope questions of bootstrap step 3 first, if you did not ask them. Then follow bootstrap step 7, and build `PROGRESS.md` again as in bootstrap step 8. After that, check the items of the subsections that the complete lessons cover. If a `**Covers:**` line of a lesson matches no subsection of the new roadmap, tell the user.

### 5.6 `README.md`

Write the file as in bootstrap step 9, from `../bootstrap/assets/README.md`.

### 5.7 Old command files

Delete the old command files from step 1.7, if the user agreed. Delete only the files in that list.

## 6. Verify

- `CLAUDE.md` passes the checks of bootstrap step 5.
- `state.json` and every `progress.json` are valid JSON, and use only camelCase keys.
- `state.json` has no profile keys. `lesson.completed` and `project.completed` match the `progress.json` files.
- Every `progress.json` of a lesson with a `Theory/` folder has one entry for each folder in `Theory/` and in `Exercises/`.
- No progress value changed from `true` to `false`. No `PROGRESS.md` item changed from `- [x]` to `- [ ]`.
- `ROADMAP.md` and `PROGRESS.md` pass the checks of bootstrap step 10.
- Run `git status`, if git is set up. Make sure that the update changed no lesson content file (see the rules at the top). If it did, restore the file with `git restore <path>`, and tell the user.

## 7. Report

Reply with:

- The list of the files that you changed, and for each file what you changed.
- The list of the files that you did not change, and why (up to date, or the user chose to keep them).
- The problems that the user must fix, e.g. a project with no `progress.json`, or a `**Covers:**` line that matches no subsection.
- The next step: run `/select-lesson` if there is no current lesson. Or continue with the current lesson and `/check-progress`.

## 8. Commit the update

Skip this step if git is not set up (see step 0 of the `commit` skill).

Ask (with the question tool) if the user wants to commit the update. Offer "Commit the update" and "Do not commit".

On "Commit the update", commit the files directly with `git`. Do not use the `commit` skill: it reads a change from `false` to `true` in a `progress.json` file as a new completion. This update only changes the format, so it must not make progress commits.

- Stage only the files that this skill changed.
- Make one commit for each group, with a Conventional Commits subject line only (no body, no footer), in this order. Skip the groups with no changes:
  1. `docs: update study profile in CLAUDE.md`
  2. `chore: migrate state.json and progress.json to the current format`
  3. `docs: update ROADMAP.md and PROGRESS.md to the current format`
  4. `docs: update README.md`
  5. `chore: remove old study commands`
- Show the user the list of commits.
