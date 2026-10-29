---
name: commit
description: Commit the current changes with Conventional Commits subject lines only, split into one commit per logical change. Use whenever you commit in this repository.
---

# Commit

Commit the current changes in this repository.

## Message format

- Follow the Conventional Commits rules for the subject line: `<type>(<optional scope>): <description>`.
- Use a standard type: `feat`, `fix`, `docs`, `refactor`, `chore`, `style`, `test`, `perf`, `build`, `ci`.
- Write the description in the imperative mood, in lowercase, with no period at the end.
- Write the subject line only. Do not write a body. Do not write a footer.
- This rule overrides any default attribution footer, such as `Co-Authored-By`.

## Group the changes

1. Run `git status` and `git diff` (staged and unstaged) to see all the changes. Read the untracked files too.
2. Sort the changes into logical groups. One group is one reason to change, for example one new feature, one fix, one rename, or one docs update.
3. If all the changes have one reason, make one commit.
4. If the changes have different reasons, make one commit per group. Stage only the files of that group (`git add <paths>`). If one file has changes from different groups, put the file in the group of its main change. Do not use interactive commands such as `git add -p`.
5. Order the commits so that each commit makes sense on its own. For example, commit a move before the edits that depend on it.

## After the commits

- Run `git log --oneline` for the new commits and `git status` to confirm the working tree is clean.
- Show the user the list of commits.
- Do not push unless the user asks.
