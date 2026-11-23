# Selecting, cropping and annotating questions

The practice blocks are what make the handout different from a textbook chapter.
This file covers the corpus, the crops, numbering and the Chinese solutions.

## 1. Corpus and priority

Use the papers the user has authorised. A typical order:

| Priority | Corpus | Note |
|---|---|---|
| 1 | The most recent full papers for the current syllabus | Best match for question style and wording |
| 2 | Older-syllabus papers that still map to the topic | Mark every source line `(older syllabus)` |
| 3 | Author-written questions | Only when the corpus has no usable question; must use `\jtselfq` |

Before selecting, make a table **chapter point → matching questions**. Aim for at
least one structured/calculation question per chapter. A sub-question may be split
across chapters if the crops do not overlap; the same sub-question must not be used
twice.

Cross-topic reuse: scan `{{COURSE_ROOT}}/*/src/assets/exam*/` filenames and existing
`practice_mapping.md` source lines. The same question belongs to one topic unless
different parts are used.

Do not use a question just because it is available. If it tests a point outside the
syllabus, or needs a prerequisite the chapter has not taught, leave it out and record
the gap.

## 2. Cropping with PyMuPDF

```python
import fitz

doc = fitz.open(pdf_path)
page = doc[pdf_page]                  # PDF page index, not the printed page
rect = fitz.Rect(x0, y0, x1, y1)      # points, measured on the page
pix = page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=rect, colorspace=fitz.csRGB)
pix.save(out_png)                     # 4x ~= 288 dpi, white background
```

Include:

- the question number;
- the full stem;
- diagrams and tables;
- **all** options or **all** sub-parts;
- the answer box, including its bottom border.

Exclude:

- page headers/footers and page numbers;
- adjacent questions;
- the mark scheme;
- watermarks and scan shadows.

The answer-box bottom border is often cut off when the rect is taken from text
blocks. Use `page.get_drawings()` to find the border, then extend the bottom by
2–6 pt. Inspect every crop with the host's image viewer; expect to re-crop 5–15
images on a first pass.

Naming:

- recent paper: `2026M_1A_TZ3_SL_Q4.png`
- older paper: `2024N_P2_TZ1_HL_Q1.png`
- cross-page: add `_p2`
- written question: add `_W` if needed

Store in `src/assets/exam2/` (recent) and `src/assets/exam3/` (older/written).
Keep the mapping from file to source in `qa/practice_mapping.md`.

## 3. Numbering and marks

- Q numbers run continuously through the book, in chapter order.
- W numbers run continuously and separately.
- Marks come from the paper's `[n]`. If only some parts are used, sum the used parts.
- Source line format:

  `2026 May · Paper 2 TZ1 SL Q3`

  Older syllabus: append `\textit{(older syllabus)}`. Older option question:
  `(older syllabus, Option D)`.
- The block intro `\jtexamtip{Common patterns: ...}` is 2–3 lines about **how the
  point is asked**, not a summary of the content.

## 4. Chinese solutions

- MCQ: `\jtanswer{letter}` + `\jtsolution{1–3 sentences: why, plus the key equation}`.
- Structured: continue the image on the next page if needed, then one
  `\jtsolpart{X(a)}{...}` per part. Follow the official mark scheme's points, with
  substitution and result. Keep the mark scheme's significant figures and units.
- 2–5 sentences per part. Do not translate the whole question.
- Recalculate every number yourself. State the unit and the power of ten.
- Use the textbook's standard Chinese terminology consistently.

## 5. Written answers

- 1–2 per chapter, preferably `explain` / `describe` / `outline` / `deduce` questions
  worth 2–3 marks.
- `\jtwritten{W1}{source}{marks}{image}` + `\jtsolution{Chinese answer organised by
  mark-scheme point}`.
- If the corpus has no suitable written question, use
  `\jtselfq{W1}{marks}{English stem}`. The page prints
  "Author-written exam-style question"; the source line must not pretend otherwise.
- For an author-written MCQ or structured question, put `Author-written` in the
  source line and do not invent a year, paper or question number. `\jtselfq` is the
  written-question macro; there is no separate marker for MCQ/structured.

## 6. Coverage self-check

| Item | Target |
|---|---|
| Questions per chapter | 3–5, at least one structured/calculation |
| Written answers per chapter | 1–2 |
| Recent-paper share | As high as the corpus allows; old papers fill gaps |
| Duplicates | 0 repeated sub-questions; 0 whole-question reuse across topics |
| Gaps | Recorded in `practice_mapping.md` and `qa/核对记录.md` |

## 7. `practice_mapping.md`

One row per question:

| Q | Chapter | Source | Marks | Type | Point | Mark-scheme points | Crop | PDF page | Rect |
|---|---|---|---|---|---|---|---|---|---|

Then add:

- source distribution (recent vs older vs author-written);
- cross-topic avoidance notes;
- gaps and unused backup questions;
- verification record (each crop inspected, each solution recalculated).

## 8. Copyright

Past papers, mark schemes and textbook figures are copyrighted. Keep them in the
user's course directory, not in this repository. Do not publish a built PDF that
contains them without the rights to do so.
