# references/ — deep-dive notes for the pipeline

Read `SKILL.md` first. This directory holds the detail that would make the entry
card too long.

| File | Read it when |
|---|---|
| `syllabus-evidence.md` | Before planning or drafting. Verify the precise scope and map what is recalled, derived or provided. |
| `academic-qa.md` | Before handoff. Review the academic evidence in both editions. |
| `pipeline.md` | Before starting a topic. Phase 0–5, the two agent prompts, batch rules. |
| `layout-and-macros.md` | Before writing body text. Design tokens and every macro. |
| `practice-and-questions.md` | Before selecting or cropping questions. Corpus, crops, numbering, Chinese solutions. |
| `qa-and-registry.md` | At integration. QA commands, gates, optional registry fields. |
| `known-pitfalls.md` | When something breaks. TeX, fonts, pagination, images, parallel work. |
| `../template/TOPIC_KIT.md` | The short checklist to keep open while authoring. |

## Source of truth

- `template/jt_lecture.tex` is the only visual template. Topic directories receive a
  copy under `_模板/`; that copy is disposable.
- `scripts/build_topic.sh` is the only build path. It is copied to each topic as
  `src/build.sh`; fix the source and re-copy, never patch a single topic's copy.
- `examples/demo/` embeds a copy of the template so the demo can run without
  scaffolding a course. When you change the template, re-copy it into
  `examples/demo/_模板/` and rebuild the demo. A CI diff check catches drift.

## What this repo deliberately does not contain

Past papers, textbook figures, mark schemes, school logos, student data, or a
course registry. Those are supplied by the user and stay outside the repository.
