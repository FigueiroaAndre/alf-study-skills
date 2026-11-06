---
description: Test the study kit end to end. Run the simulate-user skill in a sub-agent, then the structure-verifier agent, in sequence. Then report the result.
argument-hint: [optional: subject or persona for the simulation]
---

Test the study kit of this repository. Run two sub-agents, **one after the other**. Do not run them in parallel: the second one checks the result of the first one.

## 1. Run the simulation

Start a `general-purpose` sub-agent with the Agent tool. Wait for it to finish. Give it this prompt:

> Run the `simulate-user` skill of this repository with these arguments: `$ARGUMENTS`. Use the Skill tool. If you cannot use the Skill tool, read `.claude/skills/simulate-user/SKILL.md` and follow it exactly. Do all the steps of the plan. When you finish, return: the study repository path, the number of lessons completed, the number of steps done, failed and skipped, and the findings for each severity (high, medium, low).

When it finishes:

- Find the study repository path in its answer, or in `tmp/plan.md`.
- If the sub-agent did not create a study repository in `tmp/`, do not start the second sub-agent. Go to step 3, and report the failure.

## 2. Verify the structure

Start a `structure-verifier` sub-agent with the Agent tool. Give it this prompt:

> Verify the study repository `<study repository path>`. Compare it with `STRUCTURE.md`. Read `tmp/plan.md` to see which steps ran. Write `tmp/verification.md`, and return its content.

Wait for it to finish.

## 3. Report the result

Read `tmp/report.md` and `tmp/verification.md`, if they exist. Then give the user one short report:

1. **Result:** PASS if the simulation has no high finding and the verification result is PASS. In all other cases, FAIL.
2. **Simulation:** the persona, the lessons completed, the steps done, failed and skipped, the time and the cost.
3. **Problems:** one merged list of the simulation findings and the failed verification checks, the high ones first. Remove duplicates: if both report the same problem, show it one time. For each problem, give the kit file to fix (`skills/<name>/SKILL.md`, `agents/<name>.md`, `STRUCTURE.md`, or `scripts/install-claude.py`), if you can find it.
4. **Files:** the paths of the study repository, `tmp/plan.md`, `tmp/report.md`, `tmp/verification.md`, and `tmp/logs/`.

Do not fix the kit in this command. Only report.
