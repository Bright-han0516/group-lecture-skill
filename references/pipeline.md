# Pipeline detail and agent prompts

`SKILL.md` gives the contract. This file gives the working detail: phases, the two
parallel author prompts, integration, and batch rules.

Placeholders used below:

- `{{COURSE_ROOT}}` — the directory that holds `_模板/` and the topic folders.
- `{{CODE}}` — syllabus code, e.g. `A.3`.
- `{{STEM}}` — code without punctuation, e.g. `A3`.
- `{{DIR}}` — topic directory, e.g. `A3_Energy`.
- `{{LEVEL}}` — SL / HL / SL+HL.
- `{{SYLLABUS}}`, `{{TEXTBOOK_PDF}}`, `{{PAST_PAPERS}}` — local source files.

## Phase 0 · Scaffold

Resolve `{{SKILL_ROOT}}` as the directory containing the installed `SKILL.md`. `{{COURSE_ROOT}}` is a separate user-selected output directory and may be in any project. Read `references/boards.md` for valid `{{BOARD}}` values. Never assume a relative `scripts/` path resolves from the course directory.

```bash
python3 "{{SKILL_ROOT}}/scripts/scaffold_topic.py" --board "{{BOARD}}" --root "{{COURSE_ROOT}}" {{CODE}} Energy "Work, energy and power"
```

This creates `_模板/` (template, fonts, `texmf`, assets, helper scripts) and
`{{DIR}}/{src,src/assets/{exam,exam2,exam3},dist,qa}`. The skeleton compiles
immediately; its figure is a neutral placeholder to be replaced.

Checks:

- `_模板/jt_lecture.tex` exists.
- `_模板/fonts/texgyretermes-regular.otf` exists.
- `_模板/texmf/fonts/tfm/public/rsfs/rsfs10.tfm` exists.
- `src/build.sh` is executable.

## Phase 1 · Chapter map

1. Run the [syllabus and past-paper evidence gate](syllabus-evidence.md):
   identify current objectives, compatible verified applications and exclusions
   in `{{DIR}}/qa/syllabus_scope.md`.
2. Group verified content, typically into **3–5 chapters × 2–4 sections**. Chapter titles are English
   phrases, not "Chapter 3: ...". Section titles are the assessed points.
3. Write the map into `{{DIR}}/qa/chapter_map.md`. It is the only numbering source
   for both authors.
4. Show the map to the user once. Confirm chapter count, section count, and whether
   HL-only content is included.

Page target for the student body (excluding practice): 4 h topic 14–22 pages;
6–8 h 18–26; 10 h+ 26–34. Do not pad to hit a number.

## Phase 2 · Body author prompt

Copy this block to the body agent. Replace the placeholders.

```text
You are writing one topic handout for a group-style lecture pipeline.
Working directory: {{COURSE_ROOT}}.

Task: write the English body for {{CODE}} {{TITLE}} ({{LEVEL}}, {{HOURS}} h)
in {{DIR}}/src/{{STEM}}.tex, following the fixed template.

Read first:
1. {{COURSE_ROOT}}/_模板/TOPIC_KIT.md (rules; do not edit template macros)
2. references/layout-and-macros.md (tokens and macro list)
3. {{DIR}}/qa/chapter_map.md (use these chapter/section numbers; do not renumber)
4. {{SYLLABUS}} and {{DIR}}/qa/syllabus_scope.md (objectives, supported demands and exclusions)
5. {{TEXTBOOK_PDF}} (PDF page = printed page + {{OFFSET}})
6. examples/demo/Demo_Topic/src/Demo.tex (minimal working pattern)

Target file: {{DIR}}/src/{{STEM}}.tex (the scaffold; rewrite it completely).
- Cover: \jtcover{{{CODE}}}{{EN TITLE}}{{header_{{STEM_LOWER}}.jpg}}
- {{N}} chapters; end each chapter with
  \IfFileExists{{{STEM}}_p<N>.tex}{\input{{{STEM}}_p<N>.tex}}{}
- Figures: src/assets/fig_*.png; record source in src/assets/MANIFEST.md.
- Do not write practice files; another author writes them in parallel.

Writing requirements:
- English body. Each section has at least three of: definition/comparison table
  (jttab + \blank), key equation (\eqd/\key), textbook-style figure (\jtfig),
  worked example (\jtexample), where supported by the approved scope. Use fewer
  rather than padding a section.
- Every section ends with jtexamfocus + jtmisconception (2-4 bullets each).
  Use concise reasoning and put the relevant visual next to the inference it supports.
  Use \jtdefs for key definitions and \keyeq with a symbol legend for essential
  relations. Keep the formula and definitions of all its symbols (with units
  where applicable) together; add assumptions or sign conventions when relevant.
  No fixed figure quota or formula requirement for every section.
  EXAM FOCUS: how it is asked, mark scheme, answer format. COMMON MISTAKES:
  what students actually get wrong.
- Cover in-scope objectives. Check that equations, captions, exam tips and worked
  examples do not turn given-only information or out-of-scope material into requirements.
- Target: {{PAGES}} pages of body text. Prefer 20 solid pages over 30 padded ones.

Build and self-check:
cd "{{COURSE_ROOT}}/{{DIR}}/src" && ./build.sh
grep -c "IfFileExists" {{STEM}}.tex      # must equal {{N}}
python3 ../../_模板/check_topic.py ..     # must PASS
Student edition must have zero Chinese characters.

Reply with: pages (student/key), chapter count, figure count, bookmark count,
and any gaps you could not cover.
```

Extra guidance:

- Textbook figures: `page.get_pixmap(matrix=fitz.Matrix(4,4), clip=rect)`, white
  background, crop out body text/sidebars/captions. Caption only the book title and
  edition; never invent a figure number or page.
- Keep a figure and its caption together: inline `minipage` or `figure[tbp]`, but
  use one style for the whole book.
- If a figure is missing, `\jtfig` shows a placeholder. Replace it; a placeholder is
  not a finished page.

## Phase 3 · Practice author prompt

Copy this block to the practice agent. It runs in parallel with Phase 2.

```text
You are selecting past-paper questions and writing practice blocks for one topic.
Working directory: {{COURSE_ROOT}}.

Task: write {{N}} chapter practice blocks for {{CODE}} {{TITLE}} ({{LEVEL}}).

Read first:
1. {{COURSE_ROOT}}/_模板/TOPIC_KIT.md
2. references/practice-and-questions.md
3. {{DIR}}/qa/chapter_map.md (practice blocks follow the same chapter titles)
4. examples/demo/Demo_Topic/src/Demo_p1.tex and Demo_p2.tex (minimal patterns)
5. {{SYLLABUS}} and {{DIR}}/qa/syllabus_scope.md (current assessment boundary)

Output:
- {{DIR}}/src/{{STEM}}_p1.tex ... p{{N}}.tex
- Images: src/assets/exam2/ (recent papers), src/assets/exam3/ (older/written)
- {{DIR}}/qa/practice_mapping.md: one row per question with source, marks, type,
  official mark-scheme points, crop file, PDF page and Rect.

Per chapter:
- \jtprac{}{<chapter practice title>} + \jtexamtip{Common patterns: ...}
- Aim for 3-5 in-scope questions; use structured/calculation items when appropriate.
- Where appropriate, 1-2 written answers: \jtconcept{}{...} + \jtwritten{W<n>}{source}{marks}{image}
- Q numbers continuous across the book; W numbers continuous and separate.

Rules:
- Source line: year, session, paper, time zone, level, Q number. Older syllabus:
  \textit{(older syllabus)}. Never invent a year, paper or question number.
- Chinese solution: concise reasoning and the expected answer. Use the official
  mark scheme when available or independently solve and mark NOT MS VERIFIED.
  Recalculate every numeric answer.
- Crop at 4x with PyMuPDF; include question number, stem, diagram, all parts or
  options, and the answer box. Exclude headers, neighbouring questions and the
  mark scheme. Split a cross-page question into _p1/_p2.
- Match the primary QP and scoring source by paper/variant and part. Keep
  original crops unchanged; restore necessary earlier context beside the crop.
- Inspect every crop with the host's image viewer. Re-crop until clean.
- If the corpus has no question for a point, use \jtselfq (prints
  "Author-written exam-style question") and say so in the mapping. Never dress an
  author-written question as a past paper.
- Do not edit {{STEM}}.tex and do not run build.sh; the body author is using it.

Reply with: questions per block, total marks, W count, image count, source
distribution, and gaps.
```

Corpus priority: recent full papers first; compatible older-syllabus papers to fill gaps;
author-written only when the corpus genuinely has nothing. One sub-question may be
split across chapters, but the same sub-question must not appear twice. Scan
`{{COURSE_ROOT}}/*/src/assets/exam*/` and existing `practice_mapping.md` files to
avoid reusing a question already used by another topic.

## Phase 4 · Integrate (lead only)

1. Wait for both agents. Do not build in the middle; they share `qa/build/`.
2. Check the guards:

   ```bash
   grep -c "IfFileExists" src/{{STEM}}.tex    # must equal chapter count
   ```

3. Clean rebuild:

   ```bash
   rm -rf dist qa/build
   (cd src && ./build.sh)
   ```

4. QA:

   ```bash
   python3 ../../_模板/check_topic.py ..
   ```

5. Page spot-check with the host's renderer (e.g. `pdftoppm -png -r 70`):
   - cover: header, code block, title banner, Content rule, first section;
   - a section end: both boxes complete, no split across pages;
   - a practice block: title, Q number, image complete;
   - an answer-key page: Chinese and formulas together, no clipped lines.
6. Fix topic-local errors in the topic. Fix cross-topic layout in
   `template/jt_lecture.tex`, re-copy to the topic's `_模板/`, and rebuild every
   affected topic. Never patch one topic with `\renewcommand`.

## Phase 5 · Register (optional)

Before registration and teacher handoff, complete the source-grounded academic review in `references/academic-qa.md` as `qa/academic_review.md`.

A course may have its own product registry. If it does, add one row per PDF
(student and key separately), using the same product ID and an audience/variant
column. If it does not, write `qa/核对记录.md` and stop; do not invent a registry.

`qa/核对记录.md` should record:

- product files and page counts;
- template/version used;
- source coverage (syllabus, textbook, past papers);
- QA output (gates and page checks);
- what was tested and what was not (print, classroom, brand authorization);
- known gaps (missing question types, placeholder figures, author-written items).

## Batch rules

- Two topics per batch, four agents (two body + two practice). More than that makes
  integration and registry work slower, not faster.
- At the start of a batch, confirm the chapter maps and scan existing `exam*/`
  filenames for question avoidance.
- Finish and integrate a batch before starting the next one. Do not lay out ten
  topics and build them all at the end.
- When all topics are done: template fixes → full rebuild → per-book QA → registry
  and docs once, not per topic.
