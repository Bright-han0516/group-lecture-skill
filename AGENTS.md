# AGENTS.md — rules for coding agents in this repository

This repo is a **skill package**, not a course database. Read this before changing
anything.

## Read order

1. `README.md` — what the package is and is not.
2. `SKILL.md` — the contract and the pipeline.
3. `docs/hosts.md` — how this host reads the repo and what it can run.
4. `references/README.md` — which deep-dive file to read next.
5. Only then open the template or a reference.

## Before you change code

```bash
./bootstrap.sh
```

It runs preflight, builds the demo and runs QA. The demo must be green before and
after your change. If it is already red, report that first; do not build on a broken
baseline. For debugging, the individual commands are in `README.md`.

## Before writing a topic

Read `MATERIALS.md` and ask for every missing item. Do not start if the syllabus or
the past-paper corpus is missing; do not invent sources to fill the gap.

## Non-negotiables

- **Do not edit a topic's copy of the template.** The authoritative template is
  `template/jt_lecture.tex`. Change it there, then rebuild the demo and any topic
  that uses it. A local `\renewcommand{\jtchapter}` is a bug, not a fix.
- **Do not add host fonts.** The repo ships TeX Gyre Termes / Heros / Heros
  Condensed. Switching back to Times / Helvetica Neue / Arial Narrow makes output
  machine-dependent.
- **Do not add a second build path.** `scripts/build_topic.sh` is copied to each
  topic as `src/build.sh`; fix the source and re-copy.
- **Never commit copyrighted material.** No textbook figures, past papers, mark
  schemes, school logos, student work, or answer keys derived from a publisher.
  The demo is original content; keep it that way.
- **Never write secrets or absolute user paths** into the repo. Use `GLB_*`
  environment variables, `--root`, or paths relative to the repo.
- **Do not make the student edition contain Chinese.** Chinese belongs in
  `\jtsolution` / `\jtsolpart` in the key only.
- **Do not invent sources.** A question without a real source line is either
  author-written (`\jtselfq`, clearly marked) or it does not ship.

## Parallel work

When two agents work on one topic:

- body agent: `src/<Stem>.tex`, `src/assets/fig_*`, `src/assets/MANIFEST.md`
- practice agent: `src/<Stem>_p<N>.tex`, `src/assets/exam*`, `qa/practice_mapping.md`
- only the lead runs `./build.sh`; parallel builds share `qa/build/` and will corrupt
  each other's logs and PDFs.

Both agents copy the same chapter map. Do not renumber chapters independently.

## Definition of done

- `preflight.py` exits 0.
- `examples/demo` builds two PDFs.
- `check_topic.py` prints `PASS` for both demo PDFs.
- `git diff` contains no absolute path, no secret, no publisher content.
- If you changed the template, the demo was rebuilt and the three visual spot-checks
  (cover, section end, practice block) still look right.

## Failure policy

If a dependency is missing, stop and print the `fix:` line from `preflight.py`.
Do not silently substitute a different font, skip QA, or claim a PDF was produced
when it was not. "It should work" is not a test result.
