---
name: bootstrap
description: Set up a study repository for a new subject. Ask the user their language, then what they want to study, their current experience, and their goals. Then create CLAUDE.md (study profile and language rule), state.json, ROADMAP.md (with the roadmap-builder agent) and PROGRESS.md. Use when the user runs /bootstrap or wants to start studying a new subject in an empty repository.
argument-hint: [subject and any extra information]
---

Set up the study profile, the roadmap, and the progress checklist of the study repository. The formats of `CLAUDE.md`, `state.json`, `ROADMAP.md` and `PROGRESS.md` are described in `STRUCTURE.md` of the study skills repository. All paths below are relative to the root of the **study repository** (the current working directory).

The study profile has three parts. All three go in the `## Study profile` section of `CLAUDE.md`:

- **Language:** the language that the user wants to use.
- **Subject of study:** what the user studies, with the version.
- **User context:** one paragraph about the user's current experience and goals.

## 0. Check what already exists

If `CLAUDE.md` exists and has a `## Study profile` section with a `**Subject of study:**` line, the repository is already set up. Tell the user the current subject and ask (with the question tool) whether to set it up again. Offer "Yes, start over" and "No, keep the current setup". On "No" (or no answer), stop.

If `ROADMAP.md` or `PROGRESS.md` exist, ask (in the same question tool call) whether to replace them. If the user keeps a file, skip the step that writes it.

## 1. Find the language

Write the language as the English name of the language, e.g. `English`, `Spanish`. If the language has a variant, write the variant, e.g. `Brazilian Portuguese`, `European Portuguese`.

You can assume the language in these cases:

- `$ARGUMENTS` is written in one clear language. Use that language.
- You start over (step 0), and the old study profile in `CLAUDE.md` has a `**Language:**` line. Use that language.

In all other cases, ask for the language. For example, `$ARGUMENTS` is empty, is too short to show a language, or mixes languages.

- This is the first question. Ask it before all other questions.
- Ask it alone, in its own question tool call. Do not put other questions in the same call.
- Offer the 3 most likely languages as options (start with English). The user can type a different language with "Other".

### Ask for the variant

Some languages have variants that are different in written text: spelling, words, or grammar. Examples:

- Portuguese: Brazilian Portuguese, European Portuguese.
- Spanish: Spain Spanish, Latin American Spanish.
- French: France French, Canadian French.
- Chinese: Simplified Chinese, Traditional Chinese.

If the language has such variants, and you do not know the variant, ask a follow-up question:

- Ask it right after the language question, before all other questions.
- Ask it alone, in its own question tool call, in the chosen language.
- Offer the main variants as options. Put the most likely variant first. Add a "No preference" option. On "No preference", use the variant with the most speakers.

Do not ask in these cases:

- The user already gave the variant (e.g. "Brazilian Portuguese", or "Other" with a variant).
- `$ARGUMENTS` shows the variant clearly (e.g. Brazilian spelling and words). Use that variant.
- The old study profile has a language with a variant.
- The variants are almost the same in written technical text (e.g. US English and UK English). Use the language without a variant.

From this point, use the chosen language and variant for all questions and all replies to the user.

## 2. Gather the information

You need the subject of study and the facts for the user context:

- **Subject:** what the user wants to study, e.g. "Java".
- **Background:** the user's general technical experience: role, years of experience, the languages and tools they know.
- **Experience with the subject:** what the user already knows about the subject. For example: never used it, tried it a little, used it for real tasks with gaps, uses it daily.
- **Goals:** why the user studies the subject, and what they want to do next (e.g. "learn Spring next", "get a backend job").

Background and experience with the subject are different. A senior engineer who has never written Java has a strong background and no experience with the subject.

How to ask:

1. Read `$ARGUMENTS` first. The user often gives some or all of the facts there, e.g. "I am a senior fullstack engineer (TypeScript, Python). I have never used Java. I want to learn Java so I can learn Spring next and get a backend job." Take every fact you can from it. Do not ask again for a fact that is already clear.
2. If the subject is still unknown, ask for it in plain text and wait for the answer. If the background is also unknown, ask the user in the same message to describe it in one or two sentences.
3. Ask the missing facts with the question tool, in one call:
   - **Background** (only if still unknown): New to programming or to the field; Works with technology regularly; Senior, learns new technologies fast. The user can give details with "Other".
   - **Experience with `<subject>`:** Never used it, or only tried it; Used it for real tasks, has gaps; Uses it daily, wants depth.
   - **Goal:** 2–4 likely goals for this subject (e.g. "Learn Java as a base for Spring", "Prepare for job interviews", "Maintain an existing codebase"). The user can type a custom goal with "Other".

## 3. Make the subject precise

- **Version:** if the subject has versions and the user did not give one, suggest the latest LTS version. If the subject has no LTS releases, suggest the latest stable version. If you are not sure which version is the latest, check it with a web search. Ask the user to confirm the version with the question tool, and offer the previous LTS version as a second option.
- **Follow-up questions:** ask only the questions that make the subject or the goals clear. Ask at most 3, in one question tool call. Good examples:
  - Scope boundaries: "Only the core language, or also frameworks such as Spring?"
  - Environment: "Do you want to use a build tool (Maven/Gradle) from the start, or only `java` and `javac`?"
  - Do not ask about facts you already have.
- In each question about the subject, add an option "I don't know". Put the option you recommend first, and say in its description why you recommend it.
- The subject of study is the subject plus the version, e.g. `Java 25`, `Python 3.13`, `PostgreSQL 17`. If the subject has no versions, use only the subject, e.g. `Distributed systems`.

### When the user cannot answer

A user who is new to the subject often cannot answer questions about it. This is normal. It is also a signal of their experience with the subject.

Look for these signs:

- The user selects "I don't know", or writes "I don't know", "not sure", "no idea", or a similar answer.
- The answer does not match the question (e.g. the question asks for a version, and the user describes a project).
- The answer uses the terms of the subject in a wrong way, or shows that the user does not know a basic concept of the subject.

When you see a sign:

- Do not ask the same question again, and do not ask more questions about the same topic. Use the recommended option and tell the user, in one short sentence, what you chose and why.
- Lower your estimate of the user's experience with the subject. One sign means the user probably does not have deep experience. Two or more signs, or a sign on a basic question, mean the user is probably new to the subject.
- If the user said they have more experience in step 2, do not change it without asking. In step 4, tell the user what you noticed and suggest a lower estimate. The user decides.
- These signs say nothing about the user's background. A senior engineer can know nothing about a new subject.

## 4. Write the user context and confirm

Write the user context: one paragraph, in English, of 2 to 5 sentences. It tells a teacher who the student is. Include:

- The background: role, years of experience, the technologies the user knows.
- The current experience with the subject, with concrete examples when the user gave them.
- The goals: why the user studies the subject, and what they want to do next.

Write facts, not labels. Do not invent facts. Example:

> Senior fullstack engineer with 8 years of experience, mostly TypeScript (Node.js, React) and Python. Has never written Java, but knows object-oriented programming and static types from TypeScript. Wants to learn the Java language as a base for Spring, and then get a backend software engineer position.

Show the user a short summary: language (with the variant), subject of study, the user context paragraph, and the scope decisions from step 3. Ask (with the question tool) "Is this correct?" with "Yes, create the files" and "No, change something". On "No", ask what to change and repeat this step.

## 5. Write `CLAUDE.md`

`CLAUDE.md` at the repository root holds the study profile and the language rule. Write the file in English, because the agent reads it.

If the language is English, write:

```markdown
# CLAUDE.md

## Study profile

- **Language:** English
- **Subject of study:** Java 25

### User context

Senior fullstack engineer with 8 years of experience, mostly TypeScript (Node.js, React) and Python. Has never written Java, but knows object-oriented programming and static types from TypeScript. Wants to learn the Java language as a base for Spring, and then get a backend software engineer position.

## Rules

- **Language:** communicate with the user in English, and write the study files in English. Use about 80% of ASD-STE100 (Simplified Technical English): short sentences, simple words, active voice, one idea per sentence.
```

For other languages, use an adaptation of ASD-STE100 to that language. Write the same rule, and add two points: do not translate technical terms, and keep the fixed markers in English (the commands search for them). Then add one paragraph with the most important adaptations for that language. For example, for Brazilian Portuguese, the `## Rules` section is:

```markdown
## Rules

- **Language:** communicate with the user in Brazilian Portuguese, and write the study files in Brazilian Portuguese. Use about 80% of an adaptation of ASD-STE100 (Simplified Technical English) to Brazilian Portuguese: short sentences, simple words, active voice, one idea per sentence. Do not translate technical terms: keep names of keywords, APIs, tools, and concepts as they are in the field (e.g. "record", "garbage collector", "thread", "framework"). Keep these fixed markers in English: `## BEGINNER`, `## INTERMEDIATE`, `## ADVANCED`, `## Section Summary`, `Practice:`, `**Covers:**`, `**Your answer:**` and `Answer key`.

  Adaptations for Brazilian Portuguese: use Brazilian spelling and words. Use the direct order subject–verb–object. Prefer the active voice to the passive voice with "ser" and to the "se" passive. Avoid long subordinate clauses and the mesoclisis. Use common words, not formal or literary words. Use one term for one concept.
```

Write the adaptations paragraph for the real language and variant (e.g. Brazilian Portuguese, not only Portuguese). Keep it to one paragraph. Give technical term examples that fit the subject of study. Focus on the grammar points that make text in that language long or hard to read.

If `CLAUDE.md` already exists, do not remove its other content:

- If it has a `## Study profile` section, replace that section. If not, add the section right after the `# CLAUDE.md` title.
- If it has a language rule, replace that rule. If not, add the rule under a `## Rules` heading.

Check the file:

- The `## Study profile` section has a `**Language:**` line and a `**Subject of study:**` line, and neither is empty.
- The `### User context` paragraph is not empty.

## 6. Write `state.json`

`state.json` points to the current lesson and the current project. It does not hold the study profile.

If `state.json` does not exist, create it at the repository root. A new repository has no current lesson and no current project:

```json
{
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

If you start over on an existing repository:

- Remove the old profile keys from `state.json` if they are there: `language`, `subjectOfStudy`, `technicalLevel`, `subjectFamiliarity`, `goal`.
- Keep the `lesson` and `project` values only if the subject did not change. Otherwise set them to `null` / `false`.

Check that `state.json` is valid JSON.

## 7. Build `ROADMAP.md`

Start the `roadmap-builder` agent with the Agent tool. Wait for it to finish. `CLAUDE.md` does not store the scope decisions, so give them to the agent in the prompt:

```
Build ROADMAP.md for the study repository at <absolute path of the current working directory>.
Read the study profile from the "## Study profile" section of CLAUDE.md.
Scope decisions: <each decision from step 3, e.g. "core language only, no Spring", "no build tool at first">.
Defaults chosen because the user could not answer: <list, or "none">.
```

When the agent finishes, read `ROADMAP.md`. If the file is missing, or does not have the three levels `## BEGINNER`, `## INTERMEDIATE` and `## ADVANCED`, tell the user and stop.

## 8. Write `PROGRESS.md`

Build `PROGRESS.md` from `ROADMAP.md`. It is a checklist with the same structure. Write it in the language from the study profile. Do not translate technical terms. Keep the fixed markers `## BEGINNER`, `## INTERMEDIATE`, `## ADVANCED`, `## Section Summary` and `Practice:` in English, because the other commands search for them. Translate the title and the intro line. The example below is in English:

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

## 9. Verify

- Every `####` subsection in `PROGRESS.md` has a matching subsection in `ROADMAP.md`, with the same number and title, under the same level and section. The reverse is also true.
- Every subsection in `PROGRESS.md` has at least one item.
- "Section Summary" lists every `###` section.

## 10. Report

Reply with:

- The profile: language, subject of study, user context.
- The files you created: `CLAUDE.md`, `state.json`, `ROADMAP.md`, `PROGRESS.md`.
- For each level, the list of sections, with the number of subsections in each.
- Each default that you chose because the user could not answer.
