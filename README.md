# alf-study-skills

A collection of Claude Code commands, skills, and agents. They help you study a technical subject in a dedicated **study repository**. Claude writes lessons, exercises, quizzes, and projects for you. Then it checks your work and records your progress.

## What you need

- [Claude Code](https://code.claude.com/docs)
- Python 3 (only to run the install script)
- Git

## Set up a study repository

You install the commands, skills, and agents into the study repository. They go into its `.claude/` folder. Claude Code then finds them when you open the study repository.

### 1. Clone this repository

Go to the folder where you keep your projects. Clone this repository there:

```bash
git clone https://github.com/FigueiroaAndre/alf-study-skills.git
```

### 2. Create the study folder

In the same parent folder, create a folder for the subject. For example, `java-study`:

```bash
mkdir java-study
```

Now the two folders are next to each other:

```
...
├── alf-study-skills/
├── java-study/
```

### 3. Initialize Git in the study folder

```bash
cd java-study
git init
```

### 4. Install into the study repository

From `java-study`, run the install script. The syntax is:

```bash
python3 <path-to-alf-study-skills>/scripts/install-claude.py
```

The two folders are next to each other, so the command is:

```bash
python3 ../alf-study-skills/scripts/install-claude.py
```

With no arguments, the script installs into the current directory. It copies these items:

| From `alf-study-skills` | To `java-study` |
| --- | --- |
| `commands/<name>.md` | `.claude/commands/<name>.md` |
| `skills/<name>/` | `.claude/skills/<name>/` |
| `agents/<name>.md` | `.claude/agents/<name>.md` |

To see the list of files before the script copies them, add `--dry-run`:

```bash
python3 ../alf-study-skills/scripts/install-claude.py --dry-run
```

> **Note:** You cannot install into `alf-study-skills`. The script stops with an error if the target is this repository.

### 5. Start Claude Code

Start Claude Code in `java-study`:

```bash
claude
```

Type `/` to see the list of commands. Make sure that `/bootstrap` is in the list.

### 6. Run the bootstrap skill

Run `/bootstrap`. You can add the subject and your background after the command. This gives Claude the facts, so it asks fewer questions:

```
/bootstrap I am a senior fullstack engineer (TypeScript, Python). I never used Java. I want to learn Java, then Spring, to get a backend job.
```

The bootstrap skill does these steps:

1. It asks for your language, if it cannot find it from your message. It asks this question first, and alone. For some languages, it then asks for the variant, e.g. Brazilian or European Portuguese.
2. It asks for the facts that it does not have: the subject, your background, your experience with the subject, and your goals.
3. It asks for your operating system. It also asks if you need instructions to set up the development environment, and for your preferences (for example, an editor or IDE).
4. It asks you to confirm the version of the subject and the scope.
5. It writes a short paragraph about you: your experience and your goals. It shows a summary. You confirm it.
6. It creates `CLAUDE.md` with your study profile (language, subject, and the paragraph about you), your operating system in the `## Study environment` section, and one rule: the agent communicates in your language, with about 80% of ASD-STE100 (Simplified Technical English), or an adaptation of it for other languages.
7. It creates `state.json`. This file tracks the current lesson and the current project.
8. It starts the `roadmap-builder` agent. The agent creates `ROADMAP.md`. If you need the setup instructions, lesson 1.1 is the setup of the development environment on your operating system.
9. It creates `PROGRESS.md`, a checklist that follows `ROADMAP.md`.

You can edit `ROADMAP.md` and `PROGRESS.md` after bootstrap.

### 7. Optional: add teaching guidance

Add your teaching preferences to the `CLAUDE.md` file at the root of `java-study`. Do not remove the `## Study profile` and `## Study environment` sections. For example: "Compare each Java concept to TypeScript." `/new-lesson` follows this file when it writes the theory.

### 8. Commit the setup

```bash
git add -A
git commit -m "chore: set up study repository"
```

## Study

After setup, use these commands in a loop:

| Command | What it does |
| --- | --- |
| `/new-lesson [subject]` | Creates a lesson: theory topics with small practice exercises, exercises with test files, and a quiz. With no subject, it uses the next `ROADMAP.md` subsection that has no lesson in `Lessons/`. |
| `/check-lesson` | Checks your exercises and quiz answers. It gives feedback and updates your progress. |
| `/new-project [idea]` | Creates a project description from what you studied. You write the code. |
| `/check-project` | Checks your project against its requirements and updates your progress. |

[STRUCTURE.md](STRUCTURE.md) describes all the files and folders that the commands read and write.

## Update the installed files

To get a new version, pull `alf-study-skills`. Then run the install script again from the study repository. The script replaces the files that already exist:

```bash
git -C ../alf-study-skills pull
python3 ../alf-study-skills/scripts/install-claude.py
```
