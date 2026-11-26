# Topic kit — the checklist an author keeps open

This is the short version. The full rules are in `../references/`.

## 1. File contract

```
<Course>/<Code>_<Name>/
├─ src/
│  ├─ <Stem>.tex              body author: preamble, cover, chapters, guards
│  ├─ <Stem>_p1.tex ...       practice author: one block per chapter
│  ├─ build.sh                copied by the scaffold; do not edit
│  └─ assets/
│     ├─ fig_*.png            textbook-style figures
│     ├─ exam/ exam2/ exam3/  past-paper crops
│     └─ MANIFEST.md          image and question sources
├─ dist/                      IB_<Slug>_GroupLecture_{Student,Key}.pdf
└─ qa/                        核对记录.md, practice_mapping.md, build/
```

End each chapter with a guarded input, so the body compiles before the practice
files arrive:

```latex
\IfFileExists{A3_p1.tex}{\input{A3_p1.tex}}{}
```

After integration, the number of guards must equal the number of chapters.

## 2. Body author

1. Start from `jt_topic.tex`; the scaffold already replaced the code, title and
   header placeholders.
2. Chapters group syllabus understandings (normally 3–5); sections are assessed
   points (2–4 per chapter).
3. Each section has at least three of:
   - a definition/comparison table: `\begin{jttab}{...}` with a pink header and
     `\blank` cells;
   - a key equation (`\keyeq[<symbol legend>]{<equation>}`) or key sentence (`\key`);
     define every formula symbol and give applicable units and conditions immediately below;
   - a textbook-style figure (`\jtfig`);
   - a worked example (`\jtexample`).
4. Every section ends with both boxes:

   ```latex
   \begin{jtexamfocus}
   \begin{itemize}[leftmargin=1.05em,itemsep=1pt,topsep=1pt,parsep=0pt]
     \item how it is asked / mark-scheme point / answer format
   \end{itemize}
   \end{jtexamfocus}
   \begin{jtmisconception}
   \begin{itemize}[leftmargin=1.05em,itemsep=1pt,topsep=1pt,parsep=0pt]
     \item common student error
   \end{itemize}
   \end{jtmisconception}
   ```

5. End the book with `\jtcolophon{...}`.
6. English body only. Chinese belongs in the key's `\jtsolution` / `\jtsolpart`.

## 3. Practice author

Per chapter:

```latex
\jtprac{}{<chapter practice title>}
\jtexamtip{Common patterns: ...}

\jtquestion{1}{<source>}{<marks>}{exam2/<file>.png}
\jtmcqspace
\jtanswer{C}
\jtsolution{中文解析}

\jtquestion{2}{<source>}{8}{exam2/<file>.png}
\jtsolpart{2(a)}{中文解析}
\jtsolpart{2(b)}{中文解析}

\jtconcept{}{Written answers: <subtitle>}
\jtwritten{W1}{<source>}{3}{exam3/<file>.png}
\jtsolution{中文标准答案}
```

Requirements:

- Q numbers continuous through the book; W numbers continuous and separate.
- 3–5 questions per chapter, at least one structured/calculation; 1–2 written answers.
- Every source line names year, session, paper, time zone, level and Q number. Older
  syllabus: `\textit{(older syllabus)}`.
- Chinese solution 2–5 sentences, against the official mark scheme, with the working
  and final value. Recalculate.
- Crop at 4× with PyMuPDF; include the question number, stem, diagram, all parts or
  options, and the answer box. Exclude headers, adjacent questions and mark schemes.
  Split a cross-page question into `_p1` / `_p2`.
- Inspect every crop. Re-crop until clean.
- If the corpus has no question, use `\jtselfq` (prints an author-written marker).
  For an author-written MCQ/structured question, put `Author-written` in the source
  line. Never make an author-written question look like a past paper.
- Do not edit `<Stem>.tex` and do not run `build.sh`; the body author is working.

## 4. Layout rules

- Do not redefine template macros inside a topic. If a chapter bar breaks a page,
  report it and fix the template; do not add a local `\renewcommand`.
- Do not change font sizes, colours or margins. They are design tokens.
- Keep figure and caption together; use one style per book.
- A placeholder figure (`[missing figure]` / `[missing image]`) is unfinished work.

## 5. Build

```bash
cd <Topic>/src && ./build.sh
```

Outputs:

```
dist/IB_<Slug>_GroupLecture_Student.pdf
dist/IB_<Slug>_GroupLecture_Key.pdf
```

## 6. Header image

Use a chapter-opening photo the user is allowed to use, 2481 × 840 px (or the same
aspect ratio), saved as `src/assets/header_<stem>.jpg`. If none is available, the
scaffold's neutral `header_default.jpg` is used; record that in `核对记录.md`.

Do not copy a publisher's photo into this repository. The repo ships only the neutral
placeholder.

## 7. QA

```bash
python3 ../../_模板/check_topic.py ..
```

Gates: no blank pages, no path leaks, no missing images, all fonts embedded, student
edition has zero Chinese. Then look at the cover, a section end, a practice block and
a key page yourself.

## 8. Delivery checklist

- [ ] Student and key both rebuild from a clean `dist/` and `qa/build/`.
- [ ] No `[missing figure]`, no blank page, no missing image.
- [ ] Key has a Chinese solution for every question; student has no Chinese.
- [ ] Every section has both boxes.
- [ ] Every chapter has a practice block and written answer(s).
- [ ] No internal path leak (`assets/`, `.tex`, home-directory paths, `GLB_`).
- [ ] Fonts embedded; bookmarks = chapters + sections + practice blocks.
- [ ] `qa/核对记录.md`, `qa/practice_mapping.md`, `src/assets/MANIFEST.md` written.
- [ ] Source lines checked; author-written items marked.
- [ ] Print and classroom use recorded as tested or not tested — not assumed.
