---
name: bootstrap
description: Set up a study repository for a new subject. Ask the user what they want to study, their technical level, their familiarity with the subject, and their goal. Also ask their operating system and whether they need help to set up the development environment. Then create state.json, ROADMAP.md (with the roadmap-builder agent) and PROGRESS.md, and record the operating system in CLAUDE.md. Use when the user runs /bootstrap or wants to start studying a new subject in an empty repository.
argument-hint: [subject and any extra information]
---

Set up the study profile, the roadmap, and the progress checklist of the study repository. The formats of `state.json`, `ROADMAP.md` and `PROGRESS.md` are described in `STRUCTURE.md` of the study skills repository. All paths below are relative to the root of the **study repository** (the current working directory).

## 0. Check what already exists

If `state.json` exists and has a `subjectOfStudy`, the repository is already set up. Tell the user the current subject and ask (with the question tool) whether to set it up again. Offer "Yes, start over" and "No, keep the current setup". On "No" (or no answer), stop.

If `ROADMAP.md` or `PROGRESS.md` exist, ask (in the same question tool call) whether to replace them. If the user keeps a file, skip the step that writes it.

`CLAUDE.md` can already exist. The user writes teaching preferences in it. Never replace it. Step 5 changes only the `## Study environment` section.

## 1. Gather the information

You need four facts for `state.json`:

| Fact | Field in `state.json` | Values |
| --- | --- | --- |
| What the user wants to study | `subjectOfStudy` | Free text, e.g. `"Java 25"` |
| The user's general technical level | `technicalLevel` | `"beginner"`, `"intermediate"` or `"advanced"` |
| The user's familiarity with this subject | `subjectFamiliarity` | `"beginner"`, `"intermediate"` or `"advanced"` |
| Why the user studies the subject | `goal` | Free text, one or two sentences |

`technicalLevel` and `subjectFamiliarity` are different. A senior engineer who has never written Java has `technicalLevel: "advanced"` and `subjectFamiliarity: "beginner"`.

How to ask:

1. Read `$ARGUMENTS` first. The user often gives some or all of the facts there, e.g. "I am a senior fullstack engineer (TypeScript, Python). I have never used Java. I want to learn Java so I can learn Spring next and get a backend job." Take every fact you can from it. Do not ask again for a fact that is already clear.
2. If the subject is still unknown, ask for it in plain text and wait for the answer. Also ask the user to describe their background in one or two sentences (role, years of experience, the languages and tools they know).
3. Ask the missing facts with the question tool, in one call:
   - **Technical level:** Beginner (new to programming or to the field), Intermediate (works with the technology regularly, needs guidance on harder topics), Advanced (senior, learns new technologies fast).
   - **Familiarity with `<subject>`:** Beginner (never used it, or only tried it), Intermediate (used it for real tasks, has gaps), Advanced (uses it daily, wants depth).
   - **Goal:** 2–4 likely goals for this subject (e.g. "Learn Java as a base for Spring", "Prepare for job interviews", "Maintain an existing codebase"). The user can type a custom goal with "Other".

### The development environment

You also need two facts about the user's machine. They do not go into `state.json`.

| Fact | Where it goes | Values |
| --- | --- | --- |
| The user's operating system | `CLAUDE.md` (step 5) | Free text, e.g. `"Windows 11"`, `"macOS"`, `"Ubuntu 24.04"` |
| Whether the user needs a guide to set up the development environment | The roadmap (step 6) | Yes or no, plus the user's preferences |

How to ask:

1. Take these facts from `$ARGUMENTS` if they are there. Do not ask again for a fact that is already clear.
2. Ask the missing facts in the same question tool call as the facts above:
   - **Operating system:** Windows, macOS, Linux. The user can type a more precise answer with "Other" (e.g. "Windows with WSL", "Fedora 41").
   - **Environment setup:** "Do you need instructions to set up the development environment for `<subject>` on your machine?" Offer "No, my environment is ready" and "Yes, guide me".
3. If the user selects "Yes", ask in plain text if they have preferences, and wait for the answer. Give examples that fit the subject: an editor or IDE, a way to install the tools (package manager, version manager, Docker), a build tool. Tell the user that "no preference" is a good answer. If the operating system is Linux and the user did not give the distribution, ask for it in the same message.
4. If the user has no preference, or cannot answer, choose common defaults for the subject and the operating system. Tell the user in one short sentence what you chose. Add them to the list of defaults for step 6.

## 2. Make the subject precise

- **Version:** if the subject has versions and the user did not give one, suggest the latest LTS version. If the subject has no LTS releases, suggest the latest stable version. If you are not sure which version is the latest, check it with a web search. Ask the user to confirm the version with the question tool, and offer the previous LTS version as a second option.
- **Follow-up questions:** ask only the questions that make the subject or the goal clear. Ask at most 3, in one question tool call. Good examples:
  - Scope boundaries: "Only the core language, or also frameworks such as Spring?"
  - Environment: "Do you want to use a build tool (Maven/Gradle) from the start, or only `java` and `javac`?"
  - Do not ask about facts you already have.
- In each question about the subject, add an option "I don't know". Put the option you recommend first, and say in its description why you recommend it.
- Write `subjectOfStudy` as the subject plus the version, e.g. `"Java 25"`, `"Python 3.13"`, `"PostgreSQL 17"`. If the subject has no versions, write only the subject, e.g. `"Distributed systems"`.

### When the user cannot answer

A user who is new to the subject often cannot answer questions about it. This is normal. It is also a signal of their familiarity with the subject.

Look for these signs:

- The user selects "I don't know", or writes "I don't know", "not sure", "no idea", or a similar answer.
- The answer does not match the question (e.g. the question asks for a version, and the user describes a project).
- The answer uses the terms of the subject in a wrong way, or shows that the user does not know a basic concept of the subject.

When you see a sign:

- Do not ask the same question again, and do not ask more questions about the same topic. Use the recommended option and tell the user, in one short sentence, what you chose and why.
- Lower your estimate of `subjectFamiliarity`. One sign means the user is probably not `"advanced"`. Two or more signs, or a sign on a basic question, mean the user is probably `"beginner"`.
- If the user selected a higher familiarity in step 1, do not change it without asking. In step 3, tell the user what you noticed and suggest the lower level. The user decides.
- These signs say nothing about `technicalLevel`. A senior engineer can know nothing about a new subject.

## 3. Confirm

Show the user a short summary: subject, technical level, familiarity, goal, background, operating system, environment setup (yes or no, with the preferences), and the scope decisions from step 2. Ask (with the question tool) "Is this correct?" with "Yes, create state.json" and "No, change something". On "No", ask what to change and repeat this step.

## 4. Write `state.json`

Create `state.json` at the repository root. A new repository has no current lesson and no current project:

```json
{
  "subjectOfStudy": "Java 25",
  "technicalLevel": "advanced",
  "subjectFamiliarity": "beginner",
  "goal": "Learn the Java language, then learn Spring and get a backend software engineer position.",
  "lesson": {
    "current": null,
    "completed": false
  },
  "project": {
    "current": null,
    "completed": false
  }
}
```

If you start over on an existing repository and `state.json` points to a lesson or a project, keep its `lesson` and `project` values only if the subject did not change. Otherwise set them to `null` / `false`.

Check the file:

- `state.json` is valid JSON.
- `technicalLevel` and `subjectFamiliarity` are each one of `"beginner"`, `"intermediate"`, `"advanced"`.
- `subjectOfStudy` and `goal` are not empty.

## 5. Record the operating system in `CLAUDE.md`

Write a `## Study environment` section in `CLAUDE.md` at the repository root. Other commands read this file, so they can give commands that work on the user's machine.

```markdown
## Study environment

- Operating system: macOS
- Environment setup: guided in lesson 1.1. Preferences: VS Code, SDKMAN.
```

- Always write the `Operating system` line.
- Write the `Environment setup` line only if the user needs the setup guide. Give the preferences, or the defaults you chose.
- If `CLAUDE.md` does not exist, create it with only this section.
- If `CLAUDE.md` exists, keep all its other content. If it already has a `## Study environment` section, replace that section. If not, add the section at the end of the file.

## 6. Build `ROADMAP.md`

Start the `roadmap-builder` agent with the Agent tool. Wait for it to finish. `state.json` does not store the background or the scope decisions, so give them to the agent in the prompt:

```
Build ROADMAP.md for the study repository at <absolute path of the current working directory>.
Read the study profile from state.json.
Background: <role, experience, and the technologies the user knows>.
Scope decisions: <each decision from step 2, e.g. "core language only, no Spring", "no build tool at first">.
Operating system: <the operating system from step 1>.
Environment setup: <"not needed", or "needed. Preferences: <the preferences or the defaults you chose>">.
Defaults chosen because the user could not answer: <list, or "none">.
```

When the agent finishes, read `ROADMAP.md`. If the file is missing, or does not have the three levels `## BEGINNER`, `## INTERMEDIATE` and `## ADVANCED`, tell the user and stop. If the user needs the setup guide and subsection `1.1` is not the environment setup, tell the user and stop.

## 7. Write `PROGRESS.md`

Build `PROGRESS.md` from `ROADMAP.md`. It is a checklist with the same structure:

```markdown
# <Subject> Learning Progress

Tracks progress against [ROADMAP.md](ROADMAP.md). Change `[ ]` to `[x]` as topics are completed.

## BEGINNER

### 1. <Section title>

#### 1.1 <Subsection title>
- [ ] <Short form of the first concept>
- [ ] <Short form of the second concept>
- [ ] Practice: <Short form of the practice item>

## INTERMEDIATE
...

## ADVANCED
...

## Section Summary

- [ ] 1. <Section title>
- [ ] 2. <Section title>
...
```

Rules:

- Copy the levels, sections, and subsections from `ROADMAP.md`, with the same headings, numbers, and titles.
- Write one `- [ ]` item for each concept bullet in the roadmap subsection. Make each item a short form of the bullet (a few words, no explanation).
- A roadmap `**Practice:**` bullet becomes a `- [ ] Practice: ...` item.
- Do not copy the sections after `## ADVANCED` (project ideas, pacing, resources).
- "Section Summary" is the last `##` heading. It has one `- [ ]` item per `###` section, in order, with the section number and title.
- All boxes are unchecked.

## 8. Verify

- Every `####` subsection in `PROGRESS.md` has a matching subsection in `ROADMAP.md`, with the same number and title, under the same level and section. The reverse is also true.
- Every subsection in `PROGRESS.md` has at least one item.
- "Section Summary" lists every `###` section.
- `CLAUDE.md` has a `## Study environment` section with the operating system.

## 9. Report

Reply with:

- The profile: subject, technical level, familiarity, goal.
- The operating system, and whether lesson 1.1 is the environment setup.
- The files you created or changed: `state.json`, `CLAUDE.md`, `ROADMAP.md`, `PROGRESS.md`.
- For each level, the list of sections, with the number of subsections in each.
- Each default that you chose because the user could not answer.
