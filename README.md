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

1. It asks for the facts that it does not have: the subject, your technical level, your familiarity with the subject, and your goal.
2. It asks you to confirm the version of the subject and the scope.
3. It shows a summary. You confirm it.
4. It creates `state.json` with your study profile.
5. It starts the `roadmap-builder` agent. The agent creates `ROADMAP.md`.
6. It creates `PROGRESS.md`, a checklist that follows `ROADMAP.md`.

You can edit `ROADMAP.md` and `PROGRESS.md` after bootstrap.

### 7. Optional: add teaching guidance

Write a `CLAUDE.md` file at the root of `java-study`. Put your teaching preferences in it. For example: "Compare each Java concept to TypeScript." `/new-lesson` follows this file when it writes the theory.

### 8. Commit the setup

```bash
git add -A
git commit -m "chore: set up study repository"
```

## Study

After setup, use these commands in a loop:

| Command | What it does |
| --- | --- |
| `/new-lesson [subject]` | Creates a lesson: theory, exercises, and a quiz. With no subject, it uses the next unchecked item in `PROGRESS.md`. |
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
