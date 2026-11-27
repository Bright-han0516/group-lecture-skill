# Academic QA — required before teacher handoff

The automatic PDF check (`scripts/check_topic.py`) covers technical integrity only. Academic QA is a separate source-evidence review by the agent and must be shown to the teacher. No automated PASS proves pedagogical suitability or factual accuracy.

## Source-evidence table

Create `qa/academic_review.md` with a link to `qa/syllabus_scope.md` and the table below. Apply the [evidence gate](syllabus-evidence.md) in both directions: verify coverage and check that every claim presented as assessed is supported.

| Syllabus objective (exact version + ID) | Handout section/page | Question/source file + part | Status | Evidence / gap |
|---|---|---|---|---|

Allowed statuses: `verified`, `needs teacher check`, `missing`, `not applicable`.
Every in-scope syllabus objective needs a row. Missing objectives cannot be marked verified.

## Mandatory academic checks

1. **Syllabus fidelity:** verify board, subject/code, current specification, assessment year, level, component and applicable model. Check recall, derivation and given-only claims across both editions; log unsupported or excluded content and remove it from assessed material.
2. **Subject accuracy:** check claims and reasoning. Where relevant, verify sign conventions, equations and assumptions, units, significant figures and graph interpretation. For every standalone teaching/reference formula, confirm the adjacent legend covers all quantities, constants and meaningful notation, with applicable units and conditions, in both PDFs. Treat missing or misleading symbol definitions as blockers. Independently recalculate worked examples and numeric answers.
3. **Question provenance:** verify file, paper identity, year/session/variant, question number/part and marks against the actual page. Confirm the original QP/MS is unaltered and all dependencies are present beside the crop; block incomplete or unreadable items.
4. **Answer validity:** ensure every exercise has an answer. When an official MS is provided, map every relevant point to the MS. When it isn't, state `NOT MS VERIFIED`; never claim official mark-scheme agreement.
5. **Traceability:** no invented citation, textbook page, image source or exam-reference metadata. Author-written questions must be explicitly marked.
6. **Quality report:** output a table with `issue | severity | source evidence | smallest fix | status`; block delivery for wrong formulas, incorrect source attribution, missing required objectives or unresolved missing answers.

## Acceptance

- Technical build and PDF checks passed.
- Every syllabus objective has a mapped section or an explicitly recorded gap.
- Every exercise is checked for provenance and answer existence.
- Formula legends are complete and stay with their equation in both rendered editions.
- Every quantitative result is recalculated; mark-scheme verification only claimed when MS exists.
- Deliver the teacher both PDFs and `qa/academic_review.md`.

**The teacher** remains responsible for final content approval, classroom usability, choice of pedagogy and visual inspection. Do not output a fictional PASS when source files were inaccessible.
