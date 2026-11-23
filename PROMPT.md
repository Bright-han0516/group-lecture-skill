# Copy-paste prompts

Use the section that matches the host. The build prompt requires a shell with
XeLaTeX; the review prompt does not.

## A. Build mode — local coding agent (Codex, Kimi Code, Claude Code, DSH)

```text
You are using the group-lecture-skill repository.

1. Read AGENTS.md, README.md and SKILL.md.
2. Run: ./bootstrap.sh
   If it fails, stop and list every FAIL line with its fix hint.
3. If it passes, read MATERIALS.md and ask me for every missing item:
   board/code/title, level/hours, syllabus path, textbook path + page offset,
   past-paper folder + allowed range, mark-scheme folder, course root, output rules.
   Do not start writing if the syllabus or question corpus is missing.
4. Only after that, start my topic:
   - propose a 3-5 chapter map and get my confirmation
   - scaffold with scripts/scaffold_topic.py
   - write body + practice as described in references/pipeline.md
   - build and run check_topic.py; show me the gate output
5. Do not invent past-paper years, question numbers or mark-scheme points.
   If the corpus has no question, use \jtselfq and say so.
```

## B. Review mode — chat/office agent (WorkBuddy, Doubao Office, any chat AI)

```text
You are reviewing a group-style lecture handout. You do not have a shell in this
conversation, so you cannot compile PDFs or crop papers. Do not claim that you did.

Read the material I paste (chapter map, draft text, or QA record). Check:
1. Coverage: does each syllabus point appear, and is anything outside the syllabus?
2. Prerequisites: does each chapter rely only on earlier chapters or prior knowledge?
3. Explanation: is each section's key idea explained, not just stated?
4. Practice: does each chapter have 3-5 questions including one structured question,
   and 1-2 written answers, with source lines?
5. Visual plan: does each section have a table/equation/figure/example, and both
   EXAM FOCUS and COMMON MISTAKES boxes?
6. Risks: mark anything that needs the official mark scheme or a real past paper.

Return a table: item | pass/fail/uncertain | evidence | smallest fix.
Do not rewrite the whole handout unless I ask for a rewrite.
```

## C. Install as a skill — DSH / Claude Code

```bash
git clone https://github.com/Bright-han0516/group-lecture-skill.git \
  ~/.dsh/skills/group-lecture-builder
# Claude Code: ~/.claude/skills/group-lecture-builder
```

Then tell the agent:

```text
Read SKILL.md in the group-lecture-builder skill. Run its "First run" commands.
If preflight fails, stop and report. Then ask me for the five inputs before writing.
```

## D. Convert an existing topic

```text
I have an existing handout at <path>. Do not rewrite it from scratch.
1. Read it and list its chapters, sections, boxes, figures and questions.
2. Compare with the contract in SKILL.md and references/layout-and-macros.md.
3. Produce a gap list: missing boxes, missing practice, missing sources, layout
   deviations, Chinese in the student edition.
4. Fix only the gaps, rebuild, and run check_topic.py. Show the gate output.
```
