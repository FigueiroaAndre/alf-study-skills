# Study repository

This repository is for the study of one technical subject. Claude Code writes lessons, exercises, and quizzes for you. Then it checks your work and records your progress.

The `/bootstrap` skill set up this repository. It wrote your study profile in `CLAUDE.md`, and your study plan in `ROADMAP.md` and `PROGRESS.md`.

## The files

This tree shows a study repository after two lessons. The names in `<>` change for each subject. The names of the files and folders are always in English, in all languages:

```
<study-repo>/
├── .claude/                        # The skills and agents
├── CLAUDE.md                       # Your study profile
├── README.md                       # This file
├── ROADMAP.md                      # The study plan
├── PROGRESS.md                     # The progress checklist
├── state.json                      # The current lesson and the current project
└── Lessons/
    ├── 01_<subject>/
    │   └── ...
    └── 02_<subject>/
        ├── quiz.md
        ├── progress.json
        ├── Theory/
        │   ├── 1_<topic>/
        │   │   ├── theory.md
        │   │   ├── practice.md
        │   │   ├── practice-solution.md
        │   │   ├── assets/             # Optional: images, pages, and other files for the theory
        │   │   └── <practice file>     # Your practice file
        │   └── 2_<topic>/
        │       └── ...
        └── Exercises/
            ├── 1_<exercise_name>/
            │   ├── exercise.md
            │   ├── <test file>
            │   ├── <setup files>       # Optional: e.g. compose.yaml for a database
            │   └── <code file>         # Your code
            └── 2_<exercise_name>/
                └── ...
```

| File or folder | What it is |
| --- | --- |
| `.claude/` | The skills and agents. Do not edit these files. |
| `CLAUDE.md` | Your study profile: language, subject, and a paragraph about you. It also has your operating system and the language rule. |
| `ROADMAP.md` | The study plan. It has three levels: `BEGINNER`, `INTERMEDIATE`, and `ADVANCED`. Each `####` subsection becomes one lesson. |
| `PROGRESS.md` | A checklist that follows `ROADMAP.md`. `/check-progress` checks the items when you complete a lesson. |
| `state.json` | The current lesson and the current project. |
| `Lessons/` | One folder for each lesson. The name has a number and a subject: `<NN>_<subject>/`. |
| `Theory/` | One folder for each topic of the lesson. Each folder has the theory, two small practice exercises, and their solutions. You save your practice files here. |
| `Exercises/` | One folder for each exercise, in order of difficulty. Each folder has the instructions and a test file. You write your code here. |
| `assets/` | Optional support files: images, HTML pages, diagrams, sample data. Do not edit them. |
| Setup files | Optional files in an exercise folder that prepare what the exercise needs, e.g. a `compose.yaml` that starts a database. The `## Setup` section of `exercise.md` tells you how to use them. Do not edit them. |
| `Teacher/` | Optional. Support files that `/teacher` creates for you, e.g. a diagram or a page to try. You can delete them. |
| `quiz.md` | The quiz of the lesson. You write your answers in this file. |
| `progress.json` | The progress of the lesson. `/check-progress` updates it. |

You can edit `ROADMAP.md` and `PROGRESS.md`. Keep the headings `## BEGINNER`, `## INTERMEDIATE`, `## ADVANCED`, and `## Section Summary` in English. The skills search for them.

## Study

Start Claude Code in this folder:

```bash
claude
```

Then use these commands in a loop:

1. Run `/new-lesson`. It creates the next lesson of the roadmap. At the end, it asks if you want to select the new lesson. Select it.
2. Study the lesson. The next section tells you how.
3. Run `/check-progress`. It checks your work, gives feedback, and records your progress.
4. When the lesson is complete, go back to step 1.

| Command | What it does |
| --- | --- |
| `/new-lesson [subject]` | Creates a lesson. With no subject, it uses the next `ROADMAP.md` subsection that has no lesson. You can also give a subsection number (e.g. `2.3`), a subsection title, or any subject. |
| `/select-lesson [lesson]` | Selects the current lesson. You can give a folder name, a lesson number, a roadmap subsection, or a subject. With no argument, it selects the next lesson of the roadmap. If the lesson does not exist, it offers to create it. |
| `/check-progress [request]` | Checks the current lesson: the practice of each theory topic, the exercises, and the quiz. It gives feedback and updates your progress. Then it commits your progress. It does not give the solution of an exercise. To see a solution, ask for it, e.g. `/check-progress show solution for exercise 3`. |
| `/teacher [question]` | Helps you learn the subject. It does not only give the answer: it guides you to it with questions, analogies, and examples. It does not give the solution of an exercise or a quiz question. It gives hints instead. If the question is about a lesson that you did not study yet, it tells you, and asks if you want to continue. |
| `/commit` | Commits your changes. Each completed item gets its own progress commit. |
| `/bootstrap` | Sets up the repository again, e.g. for a new subject. It asks before it replaces a file. |
| `/bootstrap-update` | Updates this repository to the structure of a new version of the skills. It does not change the content of your lessons. |

You can create more than one lesson in advance. `/new-lesson` does not change the current lesson. `/check-progress` checks only the current lesson.

## A lesson

Study the lesson in this order:

1. **Theory.** For each topic folder in `Theory/`, in order:
   1. Read `theory.md`.
   2. Do the two small exercises in `practice.md`. Save each file in the topic folder, with the name that `practice.md` gives.
   3. Do not open `practice-solution.md` before you try the exercises.
2. **Exercises.** For each exercise folder in `Exercises/`, in order:
   1. Read `exercise.md`.
   2. If `exercise.md` has a `## Setup` section, do the setup first (e.g. start the database).
   3. Write your code in the exercise folder.
   4. Run the test command from the "How to verify" section of `exercise.md`.
3. **Quiz.** Open `quiz.md`. Write each answer on the `**Your answer:**` line. Do not open the answer key before you answer.

You can run `/check-progress` at any time. It checks the work that you did. It also tells you what is missing.

If you have a question, or you are blocked on an exercise, run `/teacher <question>`. It guides you to the answer with questions and hints, but it does not give the solutions.

The lessons use Mermaid diagrams. GitHub shows them as pictures. In your editor, you can need an extension, e.g. a Mermaid preview extension for VS Code.

## Track your progress with git

`/commit` and `/check-progress` write progress commits with this template:

```
progress(<lesson or project folder>): <complete | work on> <item>
```

For example:

```
progress(02_<subject>): complete theory 1_<topic>
progress(02_<subject>): complete exercise 1_<exercise_name>
progress(02_<subject>): complete lesson
```

To see your progress and your consistency, run:

```bash
git log --format='%ad %s' --date=short --grep='^progress('
```

If this folder is not a git repository, `/commit` does nothing. To get the commits, run `git init`. Then set your git user name and email.

## Change how Claude teaches

Add your teaching preferences to `CLAUDE.md`. For example: "Compare each concept to a language that I know." or "Give shorter theory and more exercises." `/new-lesson` follows them when it writes the next lessons.

Do not remove the `## Study profile` and `## Study environment` sections. You can edit them, e.g. to change your goals.

## Update the skills

The skills come from the `alf-study-skills` repository. To get a new version, pull that repository. Then run its install script again from this folder:

```bash
git -C <path-to-alf-study-skills> pull
python3 <path-to-alf-study-skills>/scripts/install-claude.py
```

Then run `/bootstrap-update`. It finds the files that use an older structure, and updates them. It does not change the content of your lessons, and it does not remove your progress. To only see what is outdated, run `/bootstrap-update --check`.
