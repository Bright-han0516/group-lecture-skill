# examples/ — the runnable demo

`examples/demo/` is a three-chapter topic built with the same template and scripts as
a real course topic. It uses **original** text, figures and questions; no past paper,
textbook figure or mark scheme is included.

## Run it

```bash
cd examples/demo
./build.sh
python3 ../../scripts/check_topic.py Demo_Topic
```

`build.sh` points the generic build at the repo's `template/fonts` and
`vendor/texmf`, then builds `Demo_Topic/src/Demo.tex`.

Expected (font/page counts may move slightly after template edits):

| File | Pages | Chinese chars |
|---|---:|---:|
| `Demo_Topic/dist/IB_Demo_Topic_GroupLecture_Student.pdf` | 6 | 0 |
| `Demo_Topic/dist/IB_Demo_Topic_GroupLecture_Key.pdf` | 5 | ~112 |

Bookmarks: 9 (3 chapters + 3 sections + 3 practice blocks). QA must print `PASS` for
both PDFs, with `blanks=[]`, `leaks=[]`, `missing_images=0`,
`not_embedded_fonts=[]`.

## What it proves

- The template compiles with the bundled fonts and the vendored `rsfs`.
- The cover, chapter bars, pink tables, both boxes, practice block and Chinese
  solutions all render.
- The two editions come from one source (`\JTKEY`), and the student edition has no
  Chinese.
- `scaffold_topic.py` produces a skeleton that builds; the demo is the same shape.

## What it does not prove

- That a **real** topic's content is correct or covers the syllabus.
- That a real past-paper crop is clean (the demo has no past papers).
- That the output matches a particular publisher's original pixel for pixel. The
  template is an independent style recreation.

## Files

```
demo/
├─ build.sh                 wrapper: sets GLB_FONTS_DIR / GLB_TEXMF, calls src/build.sh
├─ _模板/                    local copy of jt_lecture.tex, jt_topic.tex, logo, header
└─ Demo_Topic/
   ├─ src/Demo.tex          body + guards
   ├─ src/Demo_p1..p3.tex   practice blocks, including a written answer
   ├─ src/assets/           original graph and question images
   ├─ src/build.sh          copy of scripts/build_topic.sh
   ├─ dist/                 generated, ignored by git
   └─ qa/                   generated logs/preview, plus a short record
```

If you change `template/jt_lecture.tex`, re-copy it into `demo/_模板/` and rebuild.
CI should fail if the two copies differ.
