---
name: commit
description: Commit the current changes of the study repository, with a subject line only (no body, no footer). Split the changes into one commit per logical change. A change that records study progress (a theory topic, an exercise, the quiz, a lesson or a project is complete, or the student worked on one) gets a progress commit with a fixed template, so the git history shows the progress of the student. Progress commits are atomic: one commit per progression. If the study repository is not a git repository, or git has no user name or email, do nothing. All other changes (skills, CLAUDE.md, new lessons, and so on) get a Conventional Commits subject line. Use when the user runs /commit or asks to commit in the study repository, when the check-progress skill invokes it, and after /check-project.
argument-hint: [optional note about what to commit]
---

Commit the current changes of the study repository. All paths below are relative to the root of the **study repository** (the current working directory).

The git history of the study repository is also the progress log of the student. The student uses `git log` to see what they completed, and when. For this reason, progress commits always use the same template, and progress commits are **atomic**: one commit records exactly one progression (one theory topic, one exercise, the quiz, one lesson, or one project). Never put two progressions in one commit, even if they happened at the same time.

## 0. Check git

Before you do anything else, check that git is set up in the study repository:

- Run `git rev-parse --is-inside-work-tree`. If the command fails, the study repository is not a git repository.
- Run `git config user.name` and `git config user.email`. If one of them is empty, git is not configured.

If one of these checks fails, do nothing. Do not run `git init`, do not change the git configuration, and do not change any file. If the user ran `/commit` directly, tell them in one sentence that git is not set up, and stop. If another skill or command invoked this skill, stop silently.

## 1. Read the context

- Read `CLAUDE.md`. If it has a study profile, use the language of the study profile when you talk to the user, and follow the language rule. The commit messages are always in English, because the template is fixed.
- Run `git status` and `git diff` (staged and unstaged) to see all the changes. Read the untracked files too.
- If `$ARGUMENTS` is not empty, use it as a hint about what to commit. It does not change the message rules.
- If there are no changes, tell the user and stop.
- If a merge, a rebase, or a cherry-pick is in progress, or there are merge conflicts, do not commit. Tell the user, and stop.
- If the repository has no commits yet, `HEAD` does not exist. Treat all files as untracked.
- If some files are already staged, unstage them (`git restore --staged .`, or `git rm -r -q --cached .` if the repository has no commits yet). The changes stay in the working tree. Each group in step 6 stages its own files, so a commit never gets files from another group.

## 2. Message rules for all commits

- Write the subject line only. Do not write a body. Do not write a footer.
- This rule overrides any default attribution footer, such as `Co-Authored-By`.
- Write the description in the imperative mood, in lowercase (except for folder names), with no period at the end.
- Do not use interactive commands such as `git add -p` or `git rebase -i`.

## 3. Find the progress changes

A progress change is a change that records the work of the student. Find them in these files:

- `Lessons/<NN>_<subject>/progress.json` and `Projects/<project_name>/progress.json`: compare each file with its version in `HEAD` (`git show HEAD:<path>`). If the file is untracked, compare it with a file where all values are `false`.
- The student's files: the code in `Exercises/<N>_<name>/`, the answers in `quiz.md`, the student's work in `Theory/<N>_<topic>/`, and the code in `Projects/<project_name>/`.

A value that changes from `false` to `true` is a **completion**. Only `progress.json` decides a completion. Do not decide that an item is complete from the student's code. The `check-progress` skill and the `/check-project` command set these values.

| Change in `progress.json` | Completion |
| --- | --- |
| `theory[].completed` of `<N>_<topic>` | theory topic `<N>_<topic>` |
| `exercises[].completed` of `<N>_<name>` | exercise `<N>_<name>` |
| `isQuizCompleted` | quiz |
| `completed` of a lesson | lesson |
| `completed` of a project | project |

A change in the student's files with no completion is **work in progress**. For example, the student wrote code for an exercise, but the exercise is not complete.

If a value changes from `true` to `false`, do not commit it as progress. Tell the user, and ask what to do.

## 4. Progress commit template

Use exactly this template:

```
progress(<folder>): <verb> <item>
```

- `<folder>` is the name of the lesson folder (e.g. `03_records`) or the project folder (e.g. `library_manager`), not the full path.
- `<verb>` is `complete` for a completion, or `work on` for work in progress.
- `<item>` is one of these:

| Item | Form | Example |
| --- | --- | --- |
| Theory topic | `theory <N>_<topic>` | `progress(03_records): complete theory 2_compact_constructors` |
| Exercise | `exercise <N>_<name>` | `progress(03_records): complete exercise 4_bank_account` |
| Quiz | `quiz` | `progress(03_records): complete quiz` |
| Lesson | `lesson` | `progress(03_records): complete lesson` |
| Project | `project` | `progress(library_manager): complete project` |

Work in progress uses the same items, e.g. `progress(03_records): work on exercise 4_bank_account`, or `progress(library_manager): work on project`.

- `<N>_<topic>` and `<N>_<name>` are the exact folder names, as in `progress.json`.
- One commit records one item. Do not put two items in one subject line, and do not put the files of two items in one commit. For example, two complete exercises are two commits, and a complete exercise and a complete lesson are also two commits.
- The type `progress` is only for these commits. Do not use it for other changes.

With this template, the student can see the progress with commands like these:

```bash
git log --format='%ad %s' --date=short --grep='^progress('
git log --format='%ad %s' --date=short --grep='^progress(03_records)'
git log --format='%ad %s' --date=short --grep=': complete lesson$'
```

## 5. Other commits

All changes that are not progress changes use a Conventional Commits subject line: `<type>(<optional scope>): <description>`.

- Use a standard type: `feat`, `fix`, `docs`, `refactor`, `chore`, `style`, `test`, `perf`, `build`, `ci`.
- Examples:
  - A new lesson from `/new-lesson`: `feat(lessons): add lesson 03_records`
  - A new project from `/new-project`: `feat(projects): add project library_manager`
  - A change to `ROADMAP.md` or `PROGRESS.md` by the user: `docs: add pattern matching to roadmap`
  - A change to `CLAUDE.md`: `docs: add teaching guidance to CLAUDE.md`
  - An update of the installed skills in `.claude/`: `chore: update study skills`
  - A fix in an exercise statement or test file: `fix(03_records): correct expected output of exercise 2_point`

## 6. Group the changes

1. Sort the changes into logical groups. One group is one reason to change.
   - Each completion is one group.
   - Each item with work in progress is one group.
   - Each other reason to change (one new lesson, one docs update, one skill update) is one group.
2. Put each file in the group that it belongs to:
   - The student's files of an item go with the completion or the work in progress of that item.
   - The lesson completion gets `PROGRESS.md`, `state.json`, and the lesson `completed` value in `progress.json`.
   - The project completion gets `state.json`, and the project `completed` value in `progress.json`.
   - A progress group contains only the files of its item. Do not add files of other items or other changes to it.
   - If a file that is not a `progress.json` file has changes from different groups, and one of them is a progress group, ask the user what to do. Otherwise, put the file in the group of its main change.
3. Order the commits:
   1. The other commits first (for example, a new lesson, or a fix in an exercise test).
   2. Then the progress commits of each lesson or project, in this order: the theory topics (in folder order), the exercises (in folder order), the quiz, and then the lesson or the project.
   3. A work in progress commit for an item comes before a completion of the same item, but you usually have only one of them.

## 7. Split a `progress.json` file

One `progress.json` file often has more than one completion, for example after `/check-progress`. Each completion must have its own commit. Do these steps for each `progress.json` file with more than one completion:

1. Copy the final file to the scratchpad directory. This is the final version.
2. Start from the version in `HEAD` (or from all values `false`, if the file is untracked).
3. For each completion, in the order of step 6:
   1. Write the file: the version from the step before, with only this value changed to `true`. Keep the format of the final version (indentation and key order).
   2. Stage the file and the other files of this group (`git add <paths>`).
   3. Commit with the progress template.
4. After the last completion, the file must be the same as the final version. Compare the two files. If they are different, write the final version back and tell the user.

If a `progress.json` file has only one completion, do not split it. Commit it with the other files of its group.

## 8. Make the commits

- Before each progress commit, run `git diff --cached --name-only`. Make sure that the staged files belong to only one item.
- For each group, in the order of step 6, stage only the files of that group (`git add <paths>`), and commit with the subject line (`git commit -m "<subject>"`).
- Do not commit files that should not be in the repository, such as build output or temporary test files. Tell the user about them.

## 9. Report

- Run `git log --oneline` for the new commits, and `git status` to make sure that the working tree is clean.
- Show the user the list of commits. Put the progress commits in a separate list, so the user sees what they completed.
- Do not push unless the user asks.
