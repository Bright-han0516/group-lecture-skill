# QA and optional registry

## Check the rendered answer evidence

For each exercise, verify part-level correspondence between the evidence and
worked solution when an official MS is supplied. Inspect the rendered key:
image and caption on one page, legible source/marks, no clipping, no false
official label for author-written work. Inspect the student PDF for both
answer headings and answer images; text-based QA alone cannot prove images do
not leak. Check the selected visuals, definition boxes and relation boxes at
actual reading size. Teachers determine pedagogical quality.

## 1. Build

```bash
cd {{DIR}}/src
./build.sh
```

Four XeLaTeX passes: two for the student edition, two for the key. Logs go to
`{{DIR}}/qa/build/{student,key}.log`; PDFs to `{{DIR}}/dist/`.

`build.sh` uses:

- `_模板/fonts/` for TeX Gyre fonts (`\JTFONTDIR`);
- `_模板/texmf/` as `TEXMFHOME`, so `rsfs10.tfm` is found;
- `GLB_TEMPLATE_DIR`, `GLB_FONTS_DIR`, `GLB_TEXMF`, `GLB_SLUG` as overrides.

If the template changes, rebuild every affected topic and compare page counts and
bookmarks; a layout fix can move both.

## 2. Structural QA

```bash
python3 ../../_模板/check_topic.py ..
```

It reports, for each PDF:

- page count and bookmark count;
- blank pages (no text, no images, almost no vector drawing);
- internal path leaks (`assets/`, `.tex`, home-directory paths, `GLB_`, ...);
- missing-image placeholders;
- fonts not embedded;
- Chinese character count.

Gates:

| Gate | Target |
|---|---|
| `blank_pages` | `[]` |
| `path_leaks` | `[]` |
| `missing_images` | `0` |
| `not_embedded_fonts` | `[]` |
| student `zh` | `0` |

The script exits 1 on failure, so it can run in CI. It is structural only: it cannot
tell you that a table is ugly or a box is split. Do the page check below.

## 3. Human page check

Render a few pages and look at them:

```bash
pdftoppm -png -r 70 -f 1 -l 1 dist/IB_<Slug>_GroupLecture_Student.pdf /tmp/p1
pdftoppm -png -r 70 -f <practice-page> -l <practice-page> dist/..._Student.pdf /tmp/p2
pdftoppm -png -r 70 -f <solution-page> -l <solution-page> dist/..._Key.pdf /tmp/p3
```

Check:

1. **Cover**: header image, code block, title banner, Content rule, first section.
2. **Section end**: EXAM FOCUS and COMMON MISTAKES complete, not cut by a page break.
3. **Practice block**: PAST PAPER PRACTICE bar, Q number, source line, complete image.
4. **Key**: Chinese and formulas together, no clipped lines, no missing solution.

A page with more than 50% blank space at the bottom is a judgement call: sometimes it
is a natural chapter end; sometimes it is a pagination bug. Look at the next page
before accepting it.

## 4. `qa/核对记录.md`

Record:

- product files and page counts (student/key);
- template version or commit;
- chapter/section map;
- content sources (syllabus, textbook, papers);
- QA command output (gates);
- page checks performed;
- what is **not** tested (print, classroom, brand authorization);
- known gaps (missing question types, placeholder figures, author-written items).

Do not write "verified" for a check you did not run. "Not tested" is a valid entry.

## 5. Optional registry

If your course already has a product registry, add **one row per PDF**: student and
key separately, same product ID, audience/variant column distinguishes them. A
minimal schema:

```csv
id,title,audience,variant,path,lifecycle,content_check,open_check,rebuild_check,notes
A3-WEP-GRP-LEC,Work energy and power,student,blank,dist/...,draft,pass,pass,pass,
A3-WEP-GRP-LEC,Work energy and power,teacher,key,dist/...,draft,pass,pass,pass,Chinese solutions
```

Keep lifecycle values simple: `draft`, `review`, `usable`, `retired`, `blocked`.
Do not claim `usable` until content, opening and dependencies have all been checked.
Record rebuild status separately; a PDF can be usable but not reproducible if its
source is missing.

If there is no registry, skip this section. The template and QA do not depend on it.

## 6. Delivery note

At the end, report:

- the two PDF paths and page counts;
- chapter count and practice coverage (Q/W counts);
- QA evidence (gates and page checks);
- gaps and untested items;
- any parallel changes to the template or shared assets.
