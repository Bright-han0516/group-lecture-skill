# group-lecture-skill

> **Start here:** [中文快速使用指南](README.zh-CN.md) · [Global installation guide](docs/installation.md). The installer registers this skill in the user-level directory for Codex or Claude Code; actual PDF production also requires XeLaTeX and Python dependencies.

[中文说明](README.zh-CN.md)

A self-contained skill for building **group-style topic handouts**: one student PDF
with blanks, one answer-key PDF with answers and Chinese worked solutions. The visual
design is fixed in a LaTeX template; the model only fills content through macros.

By default, keep explanations concise, pair them with useful visuals, and box
core definitions and relations where applicable. In the answer key, place a
legible official mark-scheme excerpt next to the solution when source and reuse
permission are available. This does not make the public repository a source of
exam materials.

This repository is the portable distribution of the pipeline. It includes the
template, the fonts, the `rsfs` fonts needed by `mathptmx`, placeholder assets, QA
scripts and a runnable demo. It does **not** include past papers, textbook figures,
mark schemes or any school/publisher branding.

Existing courses may have a local template copy. A skill update does not
rewrite older PDFs: sync the course template before using the new commands,
retain project customisations, and rebuild both editions.

## Recommended onboarding

For nontechnical teachers, copy the installation prompt in the [Chinese quick-start guide](README.zh-CN.md#1-一段话让-ai-协助安装推荐) into a coding agent with local shell and filesystem access. The full agent-facing checklist lives in [docs/ai-install.md](docs/ai-install.md). A plain chat assistant cannot install a local skill or build PDFs. This workflow has primarily been designed/tested for physics and adjacent science materials; other subjects are experimental and must adapt content and question requirements to their own syllabus.

Minimum source materials are a syllabus and authorised past questions. Textbooks and official mark schemes are recommended but optional; do not claim mark-scheme verification without the actual MS.

## 30-second environment check (not global installation)

Requirements: XeLaTeX (TeX Live / TinyTeX), Python 3.9+, PyMuPDF. Poppler is optional.
`bootstrap.sh` picks a Python that actually has PyMuPDF; on macOS this is often
`/usr/bin/python3`, not a Homebrew Python.

```bash
gh repo clone Bright-han0516/group-lecture-skill ~/group-lecture-skill
cd ~/group-lecture-skill
./bootstrap.sh
```

This just verifies the toolchain. To install as a skill, clone into the directory
your host scans:

| Host | Clone target | Entry |
|---|---|---|
| DSH | `~/.dsh/skills/group-lecture-builder` | `SKILL.md` |
| Claude Code | `~/.claude/skills/group-lecture-builder` | `SKILL.md` |
| Codex / Cursor / Kimi Code | any directory, e.g. `~/group-lecture-skill` | `AGENTS.md` / `CLAUDE.md` |
| WorkBuddy / Doubao Office | no clone; use the ZIP or paste `PROMPT.md` | `PROMPT.md` |

Only skill-scanning hosts require the directory name to match the `name` in
`SKILL.md`. Coding agents read `AGENTS.md` from the repo root.

`bootstrap.sh` runs preflight, builds the demo, and runs QA in one go. It prints
`READY` only if all three pass; otherwise it stops at the first failure. Expected:
two PDFs in `examples/demo/Demo_Topic/dist/` and `PASS` for both. The student edition
has `zh=0`; the key contains Chinese solutions.

If you prefer the individual commands:

```bash
python3 scripts/preflight.py
(cd examples/demo && ./build.sh)
python3 scripts/check_topic.py examples/demo/Demo_Topic
```

### One-command agent prompt

Give this to Codex / Kimi Code / Claude Code / DSH (replace the skill directory if
your host uses a different one):

```text
Run this, then paste the last 30 lines of output:
gh repo clone Bright-han0516/group-lecture-skill ~/group-lecture-skill && \
  cd ~/group-lecture-skill && ./bootstrap.sh

If bootstrap fails, stop and show me the FAIL lines and fix hints.
If it succeeds, read SKILL.md and ask me for the materials in MATERIALS.md.
Do not start writing a topic before that.
```

## Three ways to use it

| Your AI | What works | Recommended path |
|---|---|---|
| Chat only, can read a URL | Explain, review, draft LaTeX | Review mode only; cannot compile |
| Local coding agent (Claude Code, Cursor, DSH, Codex) | Full pipeline | Clone + install as a skill |
| Cloud IDE / Codespaces | Full pipeline, uniform toolchain | Open the repo and run the demo |

A URL alone is not an installation. The agent must be able to read the files and
run a shell. If it cannot run `xelatex`, it cannot produce the PDFs.

Host-specific setup and a 5-minute compatibility test: [docs/hosts.md](docs/hosts.md).
Copy-paste prompts for build, review and conversion: [PROMPT.md](PROMPT.md).

### Install as a skill

DSH scans `~/.dsh/skills/<name>/SKILL.md`; Claude Code scans
`~/.claude/skills/<name>/SKILL.md`. For those two, clone to the skill name:

```bash
mkdir -p ~/.dsh/skills
gh repo clone Bright-han0516/group-lecture-skill ~/.dsh/skills/group-lecture-builder
cd ~/.dsh/skills/group-lecture-builder && ./bootstrap.sh
```

For **cross-project** invocation in Codex, install into the user-level skill directory as described in [docs/installation.md](docs/installation.md); simply cloning into an unrelated directory is not equivalent to global registration. Other hosts must be checked individually.

Then give the agent this bootstrap prompt:

```text
Read SKILL.md and references/README.md in this skill.
Run ./bootstrap.sh. If it fails, stop and tell me what is missing.
If it passes, read MATERIALS.md and ask me for the materials it lists.
Only then start my topic. Do not skip these steps.
```

## Requirements

| Dependency | Why | Install |
|---|---|---|
| GitHub CLI (`gh`) | Optional for the legacy clone workflow; the public repository can also be cloned with `git` | <https://cli.github.com> |
| XeLaTeX + TeX Live | Build the PDFs | `tlmgr` / TinyTeX; full TeX Live recommended |
| `fontspec`, `xeCJK`, `tcolorbox`, `tikz`, `tabularx`, `needspace`, `lastpage`, `hyperref` | Template | `tlmgr install ...` |
| Python 3.9+ and PyMuPDF | Cropping, QA | `pip install -r requirements.txt`; verify with `python3 -c "import fitz"` |
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

Use [MATERIALS.md](MATERIALS.md) as the checklist. At minimum:

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
see `NOTICE` and `template/fonts/GUST-FONT-LICENSE.txt`. PyMuPDF is not bundled; it is
AGPL-3.0/commercial, so check its license before redistributing a bundled environment.
