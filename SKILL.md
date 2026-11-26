---
name: group-lecture-builder
description: "Build a group-style topic handout as two PDFs: student edition (blanks) and answer key (answers + Chinese worked solutions). Fixed visual template, English body, EXAM FOCUS / COMMON MISTAKES boxes, chapter practice with past-paper questions and written answers. Use when the user asks for 集团讲义/集团版式/双版本讲义/学生版+答案版/group lecture/topic handout. Do not use for bilingual self-study notes, question banks, or past-paper cropping only."
---

# Group Lecture Builder

Turn one syllabus topic into a **student PDF + answer-key PDF** by filling a fixed
LaTeX template. The model writes content; the template owns the visual design.

This repository is self-contained: template, fonts, rsfs, placeholder assets,
QA script and a runnable demo are included. Nothing is fetched at build time.

## Cross-project installation

For Codex or Claude Code user-level installation, see `docs/installation.md`. Install once, then invoke `group-lecture-builder` in any project. Always resolve tooling relative to the installed `SKILL.md` location; never assume the working directory is the skill repository.

## First run (do this before any topic)

```bash
cd "<SKILL_ROOT>" && ./bootstrap.sh
```

It picks a Python with PyMuPDF, runs preflight, builds the demo (student + key) and
runs the structural QA. It prints `READY` only if all three pass. If it fails, stop
and report the FAIL lines; do not start writing a topic on a broken toolchain.

## Exam-board selection

Read `references/boards.md`. The supported `--board` values are `IB`, `CIE`, `AQA`, `EDEXCEL` and `AP`. Use the supplied syllabus version to determine level labels and question-citation fields; do not apply IB SL/HL or TZ requirements to other boards. `--board` controls output filenames but is not a substitute for verifying syllabus alignment.

## Materials gate (before writing)

Read `MATERIALS.md` and ask the user for every missing item. At minimum: board and
topic code, level and hours, syllabus path/section, textbook PDF + page offset (recommended, not required),
past-paper folder + allowed range, official mark-scheme folder (recommended, not required), course root, and
output constraints.

**Do not start writing if the syllabus or the question corpus is missing.** Say what
is missing; never invent a paper, year, question number, page or mark.

## Inputs (ask only for what is missing)

1. **Board + topic code**, e.g. `IB DP Physics A.3` or `CIE 9702 3.1`.
2. **Level and teaching hours** (use the board-specific level convention from `references/boards.md`; 4 h, 8 h, 14 h ...).
3. **Chapter map**: 3–5 chapters × 2–4 sections, grouped from the syllabus
   understandings. Show it to the user once before writing.
4. **Course root**: the directory that will hold `_模板/` and `<Code>_<Name>/`.
   Default: `$GLB_ROOT`, else the current directory.
5. **Question corpus range**: which past papers and mark schemes may be used.
   Never invent a paper, year, question number or mark.

The full checklist, including the textbook and mark-scheme paths, is in
`MATERIALS.md`. Those sources are **user-supplied**; they are not in this repository.

## Pipeline

| Phase | Who | Output |
|---|---|---|
| 0 Scaffold | lead | `python3 "<SKILL_ROOT>/scripts/scaffold_topic.py" --board IB --root <course> A.3 Energy "Work, energy and power"` |
| 1 Chapter map | lead | 3–5 chapters × 2–4 sections, written into `qa/chapter_map.md`; one user confirmation |
| 2 Body | body agent | `src/<Stem>.tex` + `src/assets/fig_*.png` + `MANIFEST.md` |
| 3 Practice | practice agent, parallel | `src/<Stem>_p<N>.tex` + `src/assets/exam*/` + `qa/practice_mapping.md` |
| 4 Integrate | lead only | clean rebuild, QA, page spot-check |
| 5 Register (optional) | lead | your own registry/README; not required by the template |

Rules that prevent parallel work from drifting:

- **One chapter map** is the only source of chapter/section numbering. Both agents
  copy it; neither invents headings.
- The body ends every chapter with
  `\IfFileExists{<Stem>_p<N>.tex}{\input{<Stem>_p<N>.tex}}{}`.
  After integration, `grep -c IfFileExists src/<Stem>.tex` must equal the chapter count.
- File ownership: body agent writes only `<Stem>.tex`, `fig_*`, `MANIFEST.md`;
  practice agent writes only `_p<N>.tex`, `exam*`, `practice_mapping.md`.
  Only the lead runs `build.sh`; parallel builds fight over `qa/build/`.

## Default presentation and answer evidence

- Keep prose concise, but preserve the reasoning: introduce the most useful
  diagram, graph, comparison, timeline or worked figure where it explains a step.
  Caption what the learner should notice. Prefer one informative visual over
  decorative images; set no subject-independent figure quota.
- Use `\jtdefs` for essential definitions and `\keyeq[<symbol legend>]{<equation>}`
  for the relations learners need to find quickly. Directly below every standalone
  teaching or reference formula (including in summary sheets), define every
  quantity and meaningful constant, subscript, superscript or qualifier in order
  of appearance; give units for measured quantities where applicable and major
  assumptions or sign conventions. Keep each explanation with its formula and
  visible in both editions, not in a blank or only in the key. An adjacent group
  of formulas sharing notation may use one complete legend directly below the
  group. In a continuous derivation, explain only new or redefined notation at its
  first use. Do not rewrite publisher question or MS images. A section without an
  essential equation need not have a formula box.
- In the answer key, follow the worked solution with the corresponding official
  MS excerpt by default if the actual source is supplied and reproduction is
  authorised. Use \jtms{source and question part}{ms/file.png}, relative to
  src/assets; a terse official answer-table entry may use \jtmsline for readability.
  If an excerpt cannot be reproduced, record the verified citation in QA without
  embedding it. If the official source is unavailable, record NOT MS VERIFIED.
  Author-written items use \jtmarkpoints, never an official label.
- Never expose answer evidence in the student edition or commit publisher assets
  to this repository. Check that each excerpt matches the question part and is legible.

## Academic QA

Before teacher handoff, read `references/academic-qa.md` and create `qa/academic_review.md`. Verify syllabus coverage, equations and symbol legends, calculations, provenance, question/answer mapping and optional mark-scheme evidence. Do not claim MS verification when no official MS was supplied. Teachers make the final teaching and visual-design judgement.

## Build and QA

```bash
cd <Course>/<Code>_<Name>/src && ./build.sh
python3 <Course>/_模板/check_topic.py ..
```

`build.sh` runs XeLaTeX twice per edition (four passes total). It uses the fonts in
`_模板/fonts/` and the rsfs tree in `_模板/texmf/`, so the output does not depend on
host fonts. `GLB_TEMPLATE_DIR`, `GLB_FONTS_DIR`, `GLB_TEXMF`, `GLB_SLUG` override
the defaults.

QA gates (all must pass):

- `blank_pages = []`
- `path_leaks = []`
- `missing_images = 0`
- `not_embedded_fonts = []`
- student edition `chinese = 0`

Then spot-check four pages with the host's image viewer: cover, a section end with
both boxes, a practice block, an answer-key solution page.

## Visual contract

The template is `template/jt_lecture.tex`. Body files **call macros only**:

`\jtcover`, `\jtchapter`, `\jtsub`, `\jtsubsub`, `jttab`, `\blank`, `\eqd`, `\key`,
`\jtexample`, `\jtfig`, `\jtfigtwo`, `jtexamfocus`, `jtmisconception`, `\jtprac`,
`\jtquestion`, `\jtmcqspace`, `\jtanswer`, `\jtsolution`, `\jtsolpart`,
`\jtconcept`, `\jtwritten`, `\jtselfq`, `\scribble`, `\jtcolophon`.

- Do **not** redefine template macros inside a topic. Fix the template and rebuild
  every affected topic.
- Student and key come from the same source. `\def\JTKEY{}` is the only switch;
  never write a separate key document.
- Chinese is allowed only in `\jtsolution` / `\jtsolpart` (answer key). The student
  edition must be English-only.
- `\jtfig` and `\jtimg` show a placeholder when an image is missing; a placeholder
  is a bug to fix, not a finished page.
- Fonts are bundled (TeX Gyre Termes / Heros / Heros Condensed, GUST license).
  Do not switch to Times/Helvetica Neue/Arial Narrow for "better" output; that
  breaks cross-machine consistency.

## Content contract

- English body; combine definition/comparison tables, key relations, visuals and
  worked examples as the objective requires. Use natural variation across sections.
- Every section ends with `jtexamfocus` (2–4 bullets: how it is asked, mark scheme,
  answer format) and `jtmisconception` (2–4 bullets: common student errors).
- Every chapter has `\jtprac` + `\jtexamtip` + 3–5 questions (at least one
  structured/calculation) + 1–2 written answers.
- Q numbers are continuous across the book; W numbers are continuous and separate.
- Every question has a source line: year, session, paper, time zone, level, Q number.
  Older-syllabus questions are marked `(older syllabus)`. Self-written written
  questions use `\jtselfq`; author-written MCQ/structured questions put
  `Author-written` in the source line. Neither may pretend to be a past paper.
- Chinese solutions: 2–5 sentences, written against the official mark scheme, with
  the working and the final value. Recalculate numbers; do not copy a solution you
  have not checked.

## Files

```
<Course>/
├─ _模板/                  template, fonts, texmf, logo, header, helper scripts
└─ <Code>_<Name>/
   ├─ src/<Stem>.tex       body + \IfFileExists guards
   ├─ src/<Stem>_p<N>.tex  one practice block per chapter
   ├─ src/build.sh         generic build (do not edit per topic)
   ├─ src/assets/          fig_*, exam*/, MANIFEST.md
   ├─ dist/                IB_<Slug>_GroupLecture_{Student,Key}.pdf
   └─ qa/                  核对记录.md, practice_mapping.md, build/
```

## Limits

- This is a **local build tool**. A chat-only AI can read the repo and review a plan,
  but cannot compile, crop papers or run QA. It needs a shell with TeX Live.
- The template is an independent recreation of a common group-handout style. It is
  not affiliated with CIE, IB, Hodder or any publisher. Do not put publisher figures,
  past papers, mark schemes, a school logo or student data into this repository.
- Visual QA is structural, not pixel-perfect. There is no golden-image regression.
- Content accuracy is not proven by QA. Run a separate content review (coverage,
  prerequisites, correctness) before delivery.

## Read next

- `docs/installation.md` — user-level cross-project installation and checks.
- `references/boards.md` — board-specific nomenclature and source rules.
- `references/academic-qa.md` — source-grounded physics content QA.

- `references/pipeline.md` — full phase detail and the two agent prompts.
- `references/layout-and-macros.md` — design tokens and every macro.
- `references/practice-and-questions.md` — selecting, cropping and annotating questions.
- `references/qa-and-registry.md` — QA gates and an optional registry adapter.
- `references/known-pitfalls.md` — TeX, font, pagination and image traps.
- `MATERIALS.md` — what the user must provide before writing starts.
- `template/TOPIC_KIT.md` — the short checklist an author keeps open.
- `examples/demo/` — a runnable three-chapter example.
