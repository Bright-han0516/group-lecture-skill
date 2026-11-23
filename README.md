# group-lecture-skill

A self-contained skill for building **group-style topic handouts**: one student PDF
with blanks, one answer-key PDF with answers and Chinese worked solutions. The visual
design is fixed in a LaTeX template; the model only fills content through macros.

This repository is the portable distribution of the pipeline. It includes the
template, the fonts, the `rsfs` fonts needed by `mathptmx`, placeholder assets, QA
scripts and a runnable demo. It does **not** include past papers, textbook figures,
mark schemes or any school/publisher branding.

## 30-second check

Requirements: XeLaTeX (TeX Live / TinyTeX), Python 3.9+, PyMuPDF. Poppler is optional.
Use the Python interpreter where `python3 -c "import fitz"` succeeds. On macOS this
is often `/usr/bin/python3`; a Homebrew Python may not have PyMuPDF.

```bash
git clone https://github.com/Bright-han0516/group-lecture-skill.git
cd group-lecture-skill
python3 scripts/preflight.py
cd examples/demo && ./build.sh
python3 ../../scripts/check_topic.py Demo_Topic
```

Expected: two PDFs in `examples/demo/Demo_Topic/dist/`, and a QA report with
`PASS` for both. The student edition has `zh=0`; the key contains Chinese solutions.

## Three ways to use it

| Your AI | What works | Recommended path |
|---|---|---|
| Chat only, can read a URL | Explain, review, draft LaTeX | Review mode only; cannot compile |
| Local coding agent (Claude Code, Cursor, DSH, Codex) | Full pipeline | Clone + install as a skill |
| Cloud IDE / Codespaces | Full pipeline, uniform toolchain | Open the repo and run the demo |

A URL alone is not an installation. The agent must be able to read the files and
run a shell. If it cannot run `xelatex`, it cannot produce the PDFs.

### Install as a skill

DSH scans `~/.dsh/skills/<name>/SKILL.md`. Clone the repo to the skill name:

```bash
git clone https://github.com/Bright-han0516/group-lecture-skill.git \
  ~/.dsh/skills/group-lecture-builder
```

Claude Code uses `~/.claude/skills/` in the same way. The repo directory name can
differ from the skill name; keep the clone target as `group-lecture-builder` so it
matches the frontmatter.

Then give the agent this bootstrap prompt:

```text
Read SKILL.md and references/README.md in this skill.
Run python3 scripts/preflight.py. If it fails, stop and tell me what is missing.
Run examples/demo and confirm both PDFs plus QA pass.
Only then start my topic. Do not skip these steps.
```

## Requirements

| Dependency | Why | Install |
|---|---|---|
| XeLaTeX + TeX Live | Build the PDFs | `tlmgr` / TinyTeX; full TeX Live recommended |
| `fontspec`, `xeCJK`, `tcolorbox`, `tikz`, `tabularx`, `needspace`, `lastpage`, `hyperref` | Template | `tlmgr install ...` |
| Python 3.9+ and PyMuPDF | Cropping, QA | `pip install pymupdf`; verify with `python3 -c "import fitz"` |
| Poppler (`pdftoppm`, `pdffonts`, `pdfinfo`) | Preview, font check | optional but recommended |
| CJK font | Chinese solutions in the key | macOS Songti SC, or `tlmgr install fandol` |

Windows: use WSL or Git Bash. `build.sh` is a Bash script; native
`cmd.exe`/PowerShell is not supported. macOS and Linux work natively.

Run `python3 scripts/preflight.py` for the exact state of your machine. It prints a
`fix:` line for every missing item and exits non-zero if a hard requirement is absent.

## Build a topic

```bash
python3 scripts/scaffold_topic.py --root "/path/to/course/IB/集团讲义" \
  A.3 Energy "Work, energy and power"

cd "/path/to/course/IB/集团讲义/A3_Energy/src"
./build.sh
python3 ../../_模板/check_topic.py ..
```

`scaffold_topic.py` creates `_模板/` (template, fonts, `texmf` with `rsfs`, assets)
and the topic skeleton. The skeleton compiles as-is: it has a table, a placeholder
figure, both boxes, and two chapter guards.

Output naming: `dist/IB_<Slug>_GroupLecture_Student.pdf` and `..._Key.pdf`, where
`<Slug>` is the topic directory name. Override with `GLB_SLUG`.

## What the skill expects from you

1. Board + topic code.
2. Level and teaching hours.
3. A chapter map of 3–5 chapters × 2–4 sections (or permission to propose one).
4. A course root.
5. The question corpus you are allowed to use, plus the syllabus, textbook and
   mark schemes as local files.

The skill will not invent past-paper references. If the corpus has no question for
a point, it must say so and use `\jtselfq` for a clearly marked author-written item.

## Layout of this repo

```
SKILL.md                 entry card for the agent
AGENTS.md                repo-level rules for coding agents
README.md                this file
scripts/preflight.py     dependency check
scripts/scaffold_topic.py
scripts/build_topic.sh   copied into each topic as src/build.sh
scripts/check_topic.py   structural QA
template/jt_lecture.tex  the visual contract
template/jt_topic.tex    topic skeleton
template/TOPIC_KIT.md    short author checklist
template/fonts/          TeX Gyre Termes / Heros / Heros Condensed (GUST)
template/assets/         neutral logo, default header, figure placeholder
vendor/texmf/            rsfs (needed by mathptmx under XeLaTeX)
examples/demo/           runnable three-chapter demo
references/              pipeline, macros, practice rules, QA, pitfalls
```

## QA gates

`check_topic.py` checks each PDF for blank pages, internal path leaks, missing-image
placeholders, embedded fonts and Chinese characters. The student edition must have
zero Chinese. It exits 1 on failure, so it can be used in CI.

Visual QA is still human: render the cover, a section end with both boxes, a practice
block and an answer-key page, then look at them. The script cannot tell whether the
design "looks right".

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Unable to find TFM file "rsfs10"` | `TEXMFHOME` not pointing at `vendor/texmf` | use `build.sh`, or `export TEXMFHOME=$PWD/vendor/texmf` |
| `Font ... not found` | fonts not on the path | run `build.sh`; it passes `\JTFONTDIR` |
| `File '' not found` | `\jtlogo` was called with an empty path | pass `logo.png` or remove the call |
| Chinese boxes in the key | no CJK font | install Songti SC / `tlmgr install fandol` |
| Every arrow fails | `mathptmx` needs `rsfs` | the repo vendors it; check `TEXMFHOME` |
| QA says `not_embedded_fonts` | a font was not embedded | rebuild after fixing the font path |
| `No module named 'fitz'` | wrong Python | run `python3 -c "import fitz"`; if it fails, use the interpreter that has it (often `/usr/bin/python3`) |

## Copyright and scope

The template is an independent recreation of a common group-handout look. It is not
affiliated with CIE, IB, Hodder or any publisher. Do not commit publisher figures,
past papers, mark schemes, a school logo or student data to this repository. See
`NOTICE` for the font and `rsfs` credits.

## License

Code and documentation: MIT (see `LICENSE`). Bundled fonts keep their own licenses;
see `NOTICE` and `template/fonts/GUST-FONT-LICENSE.txt`.
