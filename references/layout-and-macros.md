# Layout tokens and macros

All visual decisions live in `template/jt_lecture.tex`. A topic's
`_模板/jt_lecture.tex` is a copy; the repo file is authoritative. Body authors call
macros and never set fonts, colours, spacing or box styles themselves.

The design is an independent recreation of a common group-handout style (deep-red
chapter bars, pink table headers, fill-in lines). It is not an official template of
CIE, IB or any publisher.

## 1. Design tokens

| Item | Value |
|---|---|
| Paper / margins | A4; top 2.64 cm, bottom 2.35 cm, left 2.24 cm, right 2.1 cm |
| Body ink | `jtink` #231F20 |
| Dark red (code block) | `jtdark` #7C2C2E |
| Main red (titles/rules/icons) | `jtred` #95383C |
| Pink (table header) | `jtpink` #B87D72 |
| Pale pink (cover banner) | `jtpale` #F7E1DC |
| Chapter bar gradient | `jtbarL` #8E4E45 → `jtbarR` #CFB2AA |
| Caption grey | `jtnode` #8C8C8C |
| Text font | TeX Gyre Termes (Times-compatible) |
| Sans font | TeX Gyre Heros (Helvetica-compatible) |
| Condensed font | TeX Gyre Heros Condensed (Arial Narrow-compatible) |
| CJK font | Songti SC (macOS) or Fandol Song (TeX Live) |
| Math | `mathptmx` + `rsfs` |
| Leading / indent | `parindent=0`, `parskip=4.2pt`, table `arraystretch=1.28` |
| Header | Group logo, 0.5 cm high, mirrored on odd/even pages |
| Footer | Answer key only: grey `n / total` |
| Cover | Full-width header 7.11 cm high, 0.49 cm from top; code block + pale title bar; red "Content" rule |

Fonts are loaded from `template/fonts/` through `\JTFONTDIR`, which the build script
passes as an absolute path. If the files are absent, the template falls back to host
Times/Helvetica, then Latin Modern. Do not rely on the fallback for production: it
changes the look.

## 2. Two editions, one source

```bash
xelatex -jobname=Demo_student "\def\JTFONTDIR{...}\input{Demo.tex}"
xelatex -jobname=Demo_key     "\def\JTFONTDIR{...}\def\JTKEY{}\input{Demo.tex}"
```

`\ifkey` controls `\blank` (line vs dark-red answer), `\jtanswer`, `\jtsolution`,
`\jtsolpart` and the footer page number. The body must not contain its own `\ifkey`
branches. If you need a different student/key layout, add a macro, not a branch.

## 3. Main file skeleton

```latex
\documentclass[11pt,a4paper]{article}
\input{../../_模板/jt_lecture.tex}
\jtlogo{../../_模板/assets/logo.png}
\graphicspath{{assets/}{../../_模板/assets/}}
\hypersetup{pdftitle={Physics A.3 Work, energy and power},pdfauthor={Group Lecture Builder}}

\begin{document}
\thispagestyle{empty}
\jtcover{A.3}{WORK, ENERGY AND POWER}{header_a3.jpg}

\jtchapter{1}{Work and energy transfer}
\jtsub{1.1}{Work done by a force}
...
\begin{jtexamfocus}...\end{jtexamfocus}
\begin{jtmisconception}...\end{jtmisconception}
\IfFileExists{A3_p1.tex}{\input{A3_p1.tex}}{}

\jtcolophon{Source notes: syllabus statements from ...; figures from ...}
\end{document}
```

The header image must be in `src/assets/`; `\jtcover` checks `assets/#3` so it can
show a placeholder when the file is missing.

## 4. Macros

| Macro | Use | Notes |
|---|---|---|
| `\jtcover{code}{EN TITLE}{header.jpg}` | Cover | Header is in `src/assets/`; placeholder if absent |
| `\jtchapter{n}{title}` | Chapter bar + level-1 bookmark | Do not use `\section` |
| `\jtsub{n.m}{title}` | Section title + level-2 bookmark | Uses `\Needspace{3.2cm}` |
| `\jtsubsub{title}` | Unnumbered subheading | |
| `\begin{jttab}{cols}` | Definition/comparison table | Must contain at least one `X` column |
| `\jtrowhead{...}` | Pink row head | Already applies `\rowcolor`; do not nest `\jtheadc` |
| `\blank[width]{answer}` | Fill-in | Line in student, dark-red answer in key |
| `\eqd{...}` / `\key{...}` | Display equation / key sentence | |
| `\jtexample{title}` | Worked example heading | Follow with `\blank` steps |
| `\jtfig[scale]{file.png}{caption}` | Single figure | Path relative to `src/assets/`; placeholder if missing |
| `\jtfigtwo[scale]{f1}{c1}{f2}{c2}` | Two figures side by side | Placeholder per file |
| `jtexamfocus` environment | Pale pink box | Required at every section end |
| `jtmisconception` environment | White box, red left rule | Required at every section end |
| `\jtprac{}{title}` | Practice block bar | Adds a bookmark |
| `\jtexamtip{...}` | Practice intro line | Common question patterns |
| `\jtquestion{n}{source}{marks}{image}` | Past-paper question | Source line is mandatory |
| `\jtmcqspace` | MCQ answer line | Student edition only |
| `\jtanswer{letter}` | MCQ answer | Key only |
| `\jtsolution{Chinese}` | Solution | Key only |
| `\jtsolpart{2(a)}{Chinese}` | Structured part solution | Key only; minipage, not tabularx |
| `\jtconcept{}{title}` | Written-answer block heading | |
| `\jtwritten{W1}{source}{marks}{image}` | Written past-paper question | Key shows the solution |
| `\jtselfq{W1}{marks}{stem}` | Author-written written question | Prints an "Author-written" marker |
| `\scribble[n]` | Answer lines | Both editions; use sparingly |
| `\jtcolophon{...}` | Source note at the end | Required |

`\jtimg[width]{file}` is the internal helper used by question/written macros: it
shows a placeholder instead of failing when an image is missing.

## 5. Tables

```latex
\begin{jttab}{|>{\raggedright\arraybackslash}p{3.1cm}|>{\raggedright\arraybackslash}X|>{\centering\arraybackslash}p{2.6cm}|}
\hline
\rowcolor{jtpink}\jtrowhead{quantity} & \jtheadc{definition} & \jtheadc{unit}\\\hline
momentum & mass × velocity = \blank[2.2cm]{$mv$} & \blank[1cm]{kg m s$^{-1}$}\\\hline
\end{jttab}
```

- Always leave one `X` column; otherwise `tabularx` cannot fit the text block.
- `\\` only at the end of a row. Do not put `\newline` before `\blank`.
- Chinese is allowed only inside `\jtsolution` / `\jtsolpart`.

## 6. Figures

- Crop textbook figures at 4× with PyMuPDF, white background, excluding body text,
  sidebars and the book's own caption.
- Caption only the book title and edition. Never invent a figure number or page.
- Keep figure and caption together: inline `minipage` or `figure[tbp]`; use one
  style throughout a book.
- A missing figure becomes a placeholder box. Replace it before delivery.

## 7. Changing the design

Change `template/jt_lecture.tex`, then:

1. re-copy it to `examples/demo/_模板/` and to every course `_模板/`;
2. rebuild the demo and run QA;
3. rebuild affected topics and spot-check the four pages.

Never add a local `\renewcommand{\jtchapter}` (or any other template macro) to a
single topic. That is how books drift apart.
