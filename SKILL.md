---
name: group-lecture-builder
description: "Build a group-style topic handout as two PDFs: student edition (blanks) and answer key (answers + Chinese worked solutions). Fixed visual template, English body, EXAM FOCUS / COMMON MISTAKES boxes, chapter practice with past-paper questions and written answers. Use when the user asks for 集团讲义/集团版式/双版本讲义/学生版+答案版/group lecture/topic handout. Do not use for bilingual self-study notes, question banks, or past-paper cropping only."
---

# Group Lecture Builder

Turn one syllabus topic into a **student PDF + answer-key PDF** by filling a fixed
LaTeX template. The model writes content; the template owns the visual design.

This repository is self-contained: template, fonts, rsfs, placeholder assets,
QA script and a runnable demo are included. Nothing is fetched at build time.

## First run (do this before any topic)

```bash
python3 scripts/preflight.py          # must exit 0
cd examples/demo && ./build.sh        # must produce two PDFs
python3 scripts/check_topic.py examples/demo/Demo_Topic   # must PASS
```

If preflight fails, stop and report what is missing. Do not start writing a topic
on a broken toolchain.

## Inputs (ask only for what is missing)

1. **Board + topic code**, e.g. `IB DP Physics A.3` or `CIE 9702 3.1`.
2. **Level and teaching hours** (SL / HL / SL+HL; 4 h, 8 h, 14 h ...).
3. **Chapter map**: 3–5 chapters × 2–4 sections, grouped from the syllabus
   understandings. Show it to the user once before writing.
4. **Course root**: the directory that will hold `_模板/` and `<Code>_<Name>/`.
   Default: `$GLB_ROOT`, else the current directory.
5. **Question corpus range**: which past papers and mark schemes may be used.
   Never invent a paper, year, question number or mark.

Also needed as source material: syllabus statements, a textbook PDF for figures,
past papers + official mark schemes. These are **user-supplied**; they are not in
this repository.

## Pipeline

| Phase | Who | Output |
|---|---|---|
| 0 Scaffold | lead | `python3 scripts/scaffold_topic.py --root <course> A.3 Energy "Work, energy and power"` |
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

- English body; each section has at least three element types: definition/comparison
  table, key equation, textbook-style figure, worked example.
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

- `references/pipeline.md` — full phase detail and the two agent prompts.
- `references/layout-and-macros.md` — design tokens and every macro.
- `references/practice-and-questions.md` — selecting, cropping and annotating questions.
- `references/qa-and-registry.md` — QA gates and an optional registry adapter.
- `references/known-pitfalls.md` — TeX, font, pagination and image traps.
- `template/TOPIC_KIT.md` — the short checklist an author keeps open.
- `examples/demo/` — a runnable three-chapter example.
