---
name: simulate-user
description: Test the study kit of this repository end to end. Act as a student. Create a study repository in tmp/learning-<subject>, write a plan in tmp/plan.md, install the kit, then talk to the kit skills (bootstrap, new-lesson, select-lesson, teacher, check-progress, recap, commit) through separate Claude Code sessions, as a real user does. Do the lesson work as the student, and complete 2 or 3 lessons. Record what the kit did wrong. Use only in this repository, when the user runs /simulate-user or wants to test the kit. It is not part of the kit.
argument-hint: [optional: subject or persona, e.g. "Go, backend dev from Python, in Brazilian Portuguese"]
---

Test the study kit. You act as a **student** who uses the kit for the first time. You do not do the work of the kit. The kit skills do it, in separate Claude Code sessions. You only talk to them, as a user talks to Claude Code, and you do the student's work (practice, exercises, quiz).

In this file, `<kit>` is the root of this repository (the current working directory). All `tmp/` paths are relative to `<kit>`.

## Rules

- **Do not do the work of the kit.** Never create or edit the files that the kit creates (`CLAUDE.md`, `ROADMAP.md`, `PROGRESS.md`, `README.md`, `state.json`, `progress.json`, lesson files). If the kit does something wrong, record it as a finding. Do not fix it.
- **The student can edit only the student's files:** the practice files in the theory topic folders, the code in the exercise folders, and the answers in `quiz.md` (on the `**Your answer:**` lines). This is what a real student does.
- **Talk to the kit only with `say.py`** (see [Talk to the kit](#talk-to-the-kit)). Never use the Agent tool or the Skill tool to run a kit skill. The kit skills must run in a Claude Code session that has the study repository as its working directory.
- **Act as a real user.** Give short, natural answers. Give the facts of your persona, and nothing more. Do not tell the kit that this is a test.
- **Do not change files outside `tmp/`**, except that you can read the kit files to compare what the kit did with what it must do.
- **Keep the plan up to date.** After each step, update `tmp/plan.md` (see [Follow the plan](#3-follow-the-plan)).

## 1. Prepare

1. Run `mkdir -p tmp`.
2. Choose the persona. If `$ARGUMENTS` gives a subject or a persona, use it, and add the missing facts. If not, choose one of these. Use a subject whose toolchain is installed (check with `command -v`), because the student must run the exercise tests:

   | Subject | Language | Toolchain | Persona message for `/bootstrap` |
   | --- | --- | --- | --- |
   | Go | English | `go` | I am a backend developer. I use Python every day, 4 years. I never used Go. I want to learn Go to write CLI tools and small services. |
   | TypeScript | Brazilian Portuguese | `node` | Sou desenvolvedor Python júnior. Nunca usei TypeScript. Quero aprender TypeScript para trabalhar com frontend. |
   | Python | English | `python3` | I am a Java developer with 6 years of experience. I know a little Python from scripts. I want to learn modern Python for data pipelines. |

   The persona also has these facts. Give them only when the kit asks: the operating system is Linux (Debian), the tools are already installed, and the student does not need help to set up the environment.
3. Set `<slug>` to a short lowercase name of the subject, e.g. `go`. The study repository is `tmp/learning-<slug>`. If this folder already exists, add a timestamp: `tmp/learning-<slug>-<YYYYMMDD-HHMM>`. Never delete an earlier study repository.
4. If `tmp/plan.md` already exists, rename it to `tmp/plan-<YYYYMMDD-HHMM>.md`. Do the same for `tmp/report.md`.

## 2. Write the plan

Before you run any step, write `tmp/plan.md`. Use this format:

```markdown
# Simulation plan

- **Study repository:** tmp/learning-<slug>
- **Subject:** <subject>
- **Language:** <language>
- **Persona:** <persona message>
- **Hidden facts:** Linux (Debian), tools installed, no setup help
- **Target:** 2 lessons (3 if the first two go well)

## Steps

- [ ] 1. Create the study folder, and run `git init` in it
- [ ] 2. Install the kit with `scripts/install-claude.py`
- [ ] 3. `/bootstrap <persona message>`, and answer the questions
- [ ] 4. `/commit` the setup
- [ ] 5. `/new-lesson`, and select the new lesson
- [ ] 6. Study lesson 1: practice, exercises, quiz (one exercise with a deliberate bug)
- [ ] 7. `/teacher <a question about lesson 1>`
- [ ] 8. `/check-progress`, fix the bug, `/check-progress` again
- [ ] 9. `/recap`
- [ ] 10. `/new-lesson`, and select the new lesson
- [ ] 11. Study lesson 2, and `/check-progress`
- [ ] 12. `/select-lesson` with no argument (it must offer to create lesson 3), and accept
- [ ] 13. Study lesson 3, and `/check-progress` (optional)
- [ ] 14. `/recap`
- [ ] 15. Write `tmp/report.md`

## Log

| Step | Status | Session | Log file | Notes |
| --- | --- | --- | --- | --- |

## Findings
```

You can adapt the steps to the persona and to `$ARGUMENTS`. Keep at least: install, `/bootstrap`, `/commit`, two `/new-lesson` runs, `/select-lesson`, `/teacher`, `/check-progress`, and `/recap`.

## 3. Follow the plan

Run the steps in order. For each step:

1. Run it. Use [Talk to the kit](#talk-to-the-kit) for the kit commands, and [Study a lesson](#study-a-lesson) for the student's work.
2. Check the result. Compare it with what the kit skill must do: read `<kit>/skills/<name>/SKILL.md` and `<kit>/STRUCTURE.md`. Look at the files in the study repository and at `git log`.
3. Update `tmp/plan.md`: check the step (`- [x]`), add a row to `## Log` (status `done`, `failed` or `skipped`, the session ID, the log file, a short note), and add each problem to `## Findings`.

A finding has this format:

```markdown
- **[high|medium|low] <skill or agent>, step <N>:** <what happened>. Expected: <what the SKILL.md or STRUCTURE.md says>. Evidence: <file, log file, or commit>.
```

Severity:

- **high:** the step fails, a file is missing or broken, the kit loses the student's work, or the kit gives the solution when it must not.
- **medium:** the kit does not follow its SKILL.md or STRUCTURE.md, but the student can continue.
- **low:** a small problem, e.g. a question that is not necessary, unclear text, or a wrong language.

If a step fails and the next steps depend on it, try one time more. If it fails again, record a high finding, mark the dependent steps `skipped`, and go to step 15.

### Steps 1 and 2: create and install

These are terminal steps that the user does, not kit commands. Run them yourself with Bash:

```bash
mkdir -p tmp/learning-<slug>
cd tmp/learning-<slug>
git init
git config user.name "Simulated Student"
git config user.email "student@example.com"
python3 ../../scripts/install-claude.py
```

Check that `.claude/skills/`, `.claude/agents/` (and `.claude/commands/` if the kit has commands) have the same items as `<kit>/skills/`, `<kit>/agents/` and `<kit>/commands/`.

### Talk to the kit

Each user message is one call of `say.py`. Run it from `<kit>`:

```bash
python3 .claude/skills/simulate-user/scripts/say.py \
  --repo tmp/learning-<slug> \
  --log tmp/logs/<NN>-<step-name>.md \
  "<message>"
```

- The first message of a step starts a new session. For example: `"/bootstrap <persona message>"` or `"/new-lesson"`.
- The script prints one JSON line with `session_id`, `result` (the answer of Claude), `is_error` and `duration_s`.
- If the answer asks a question, answer it in the same session: add `--session <session_id>` and give your answer as the message. Continue until the skill is done.
- One step = one session. Use a new log file for each step (`<NN>` is the step number).
- The session cannot show the question tool, because it runs without a terminal. Usually the skill then asks in plain text. If the session stops without a question, or it chose an answer for you, record a finding.
- A call can take a long time: `/bootstrap`, `/new-lesson` and `/check-progress` start other agents. Run these calls with the Bash tool option `run_in_background: true`, then wait for the completion notification. Do not poll in a loop. For short calls (an answer, `/recap`, `/teacher`), use the foreground with `timeout: 600000`.
- If `is_error` is `true`, read `stderr` in the JSON line and the log file. Record a finding if the error comes from the kit.

How to answer:

- Give the facts of the persona, and the hidden facts when the kit asks.
- If the kit asks you to confirm a summary, read it. If it is correct, confirm it. If it is wrong, ask for a correction one time, and record a finding.
- If the kit asks to select the new lesson, say yes.
- If the kit asks something that the persona does not know, choose the recommended option, and record a low finding only if the question was not necessary.

### Study a lesson

Do the student's work, as a student of the persona's level:

1. Read `state.json` and find the current lesson. Read the theory of each topic.
2. For each theory topic, do the two exercises of `practice.md`. Save each file with the name that `practice.md` gives, in the topic folder. Do not read `practice-solution.md` first.
3. For each exercise, read `exercise.md`, write the solution in the exercise folder, and run the verification command from "How to verify". In lesson 1, leave one small bug in one exercise on purpose. Do not run its tests after the bug. Note in the plan which exercise has the bug.
4. Answer each quiz question on its `**Your answer:**` line. Do not read the answer key first. Answer one question wrong on purpose in lesson 1.
5. Do not commit. `/check-progress` commits the progress.

Then check the work of the kit:

- After `/check-progress`, the feedback must find the bug, and it must not give the solution of the exercise. The wrong quiz answer must get feedback, but the quiz is complete. Record a finding if this is not true.
- Fix the bug, and run `/check-progress` again. The lesson must now be complete: `progress.json`, `state.json` and `PROGRESS.md` must be updated, and `git log` must have one progress commit for each item.
- If an exercise or its test is wrong (for example, the test fails for a correct solution, or the test cannot run), record a finding. Then continue with the next item.

### `/teacher`

Ask one natural question about a concept of the current lesson, and one question about the exercise with the bug ("Why does my test fail?"). The teacher must guide you, and it must not give the solution. It must not change the lesson files or the student's files. Check with `git status`.

## 4. Write the report

Write `tmp/report.md`:

```markdown
# Simulation report

- **Study repository:** tmp/learning-<slug>
- **Persona:** <subject, language>
- **Lessons completed:** <N> of <target>
- **Steps:** <done> done, <failed> failed, <skipped> skipped
- **Total time and cost:** <sum of duration_s and cost_usd of the say.py calls>

## Findings

<all findings from tmp/plan.md, the high ones first>

## What worked

<a short list of the steps that worked as the SKILL.md files say>
```

Then give the user (or the caller) a short summary: the study repository path, the number of lessons completed, the number of findings for each severity, and the paths of `tmp/plan.md` and `tmp/report.md`.
