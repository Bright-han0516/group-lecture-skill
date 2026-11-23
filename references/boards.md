# Exam-board profiles

The production workflow is board-neutral; the syllabus and question corpus remain authoritative.
Pass `--board` when scaffolding. Supported values: `IB`, `CIE`, `AQA`, `EDEXCEL`, `AP`.

| Board | Common level/unit notation | Exam question source line (examples are FORMAT ONLY; not citations) |
|---|---|---|
| IB | SL, HL | `YYYY session · Paper N · TZ/variant if applicable · SL/HL · QN` |
| CIE | AS, A2, A Level; syllabus code e.g. 9702 | `9702/YYYY/session/PaperVariant · QN` |
| AQA | AS, A Level; paper/component code | `Qualification · unit/component · YYYY series · paper · QN` |
| EDEXCEL | IAL/AS/A Level; unit/paper code | `Specification · unit · YYYY series · paper code · QN` |
| AP | Physics 1/2/C Mechanics/C E&M | `Exam · YYYY · FRQ N / released question ID` (where actually published) |

**These strings illustrate fields, not real question references.** The agent must read the supplied paper, identify the correct jurisdiction/specification and year, and transcribe only fields actually available. Do not invent IB time zones, AQA units, CIE variants, or AP released MCQ provenance.

Selection policy:
1. User provides the precise syllabus version/first-assessment date and permitted past-paper folder.
2. Crosswalk every syllabus learning objective to chapter sections.
3. Select only questions present in the authorised corpus. Record the exact source file, page and question/part.
4. If the user has an official mark scheme, verify solutions against it and record evidence. Otherwise label solutions `provisional, independently calculated; not MS-verified` and require teacher checking.
5. Keep sample/publisher figures or exam questions in the user's local course directory, not this public repository.

`scripts/scaffold_topic.py --board CIE` writes `.glb-board` in the topic root.
`src/build.sh` reads that file (or `GLB_BOARD`) for the PDF prefix. Legacy topics lacking it default to `IB`. This is a filename convention, not proof of exam-board compliance.
