# Known pitfalls

Every item here has been hit in production. Read the symptom first, then the fix.

## TeX and fonts

1. **`xdvipdfmx:fatal: Unable to find TFM file "rsfs10"`**
   `mathptmx` uses `rsfs` for some arrow/script glyphs. Without it, any `\to` or
   `\rightarrow` kills the PDF.
   Fix: build through `build.sh`, which sets `TEXMFHOME` to the repo's
   `vendor/texmf` (or the topic's `_模板/texmf`). If you build by hand:
   `export TEXMFHOME=<repo>/vendor/texmf`.

2. **`Font ... not found` / output falls back to Latin Modern**
   `\JTFONTDIR` is empty or wrong, so the TeX Gyre files are not found.
   Fix: use `build.sh`; it passes `\def\JTFONTDIR{<abs path>}`. Check
   `template/fonts/texgyretermes-regular.otf` exists.

3. **Times New Roman bold does not work on macOS**
   The family name is `Times`, not `Times New Roman`. The repo avoids the issue by
   using TeX Gyre Termes. Do not "fix" fonts back to system names.

4. **`Missing $ inserted` in a placeholder**
   A missing-image placeholder printed a filename containing `_`. Keep placeholder
   text generic (`[missing image]`), never the filename.

5. **`Misplaced \omit`**
   `\jtrowhead{\jtheadc{...}}` combines `\rowcolor` and `\multicolumn`.
   `\jtrowhead` already applies the colour; put plain text inside it.

6. **`Runaway argument ... \TX@get@body`**
   A `tabularx` was wrapped in a custom environment. Use `\begin{jttab}{...}` /
   `\end{jttab}` directly.

7. **Table runs past the text block**
   The column spec has no `X` column. Add at least one.

8. **`\jtfig` cannot find the image**
   `\IfFileExists` does not honour `\graphicspath`. The macro checks
   `assets/<file>`; put images in `src/assets/` and pass only the filename.

9. **A topic redefines `\jtchapter` to fix pagination**
   This breaks on the next template update and makes the book different from every
   other book. Fix `template/jt_lecture.tex` and rebuild; never patch one topic.

## Pagination and whitespace

10. **Blank page after the cover**
    A large `\needspace` fired on page 1. The template uses a plain `\vspace`; do not
    add a large `\needspace` back.

11. **Near-blank page before a chapter, or 8–14 cm of white at the bottom**
    `needspace` v1.3e interacts badly with an unbreakable `tcolorbox`. The template
    uses `\Needspace` for section headings and makes the boxes unbreakable. Do not
    re-enable `breakable` on the boxes.

12. **A box is cut in half by a page break**
    `tcolorbox` was set `breakable`. Remove it; if the box is too long, split the
    bullets into two boxes.

13. **Figure and caption separate**
    Use an inline `minipage` (`jtfigbox`) or `figure[tbp]`; pick one style per book.

14. **A full-page structured question pushes the next page empty**
    Shrink the image to 0.9 line width, split it across two pages, or move the
    structured question after the MCQs.

## Images and crops

15. **Answer-box bottom border missing**
    The rect came from the text block. Use `page.get_drawings()` to locate the box,
    then extend the bottom by 2–6 pt.

16. **Crop includes the page header or the next question**
    Start 4–8 pt above the question number; stop at the answer box. Inspect every
    crop with the image viewer.

17. **Textbook figure includes body text or a sidebar**
    Tighten the rect to the figure frame; remove the book's own caption. Caption only
    the book title and edition.

18. **Header photo is soft**
    Textbook inline photos are often 400–600 px wide. Use a full-width chapter
    opener if possible; otherwise record the low resolution in `核对记录.md`. Do not
    claim it is high resolution.

19. **Demo/placeholder image shows `$^{-1}$` literally**
    PIL/matplotlib do not parse LaTeX. Use Unicode (`m s⁻¹`) in generated images, or
    render the label in LaTeX.

## Content and workflow

20. **Last chapter's practice block is missing from the PDF**
    One `\IfFileExists` guard is missing. After integration,
    `grep -c "IfFileExists" src/<Stem>.tex` must equal the chapter count.

21. **Two agents build at the same time**
    They share `qa/build/`; logs and PDFs get mixed. Only the lead runs `build.sh`.
    Practice authors may compile a minimal test document in a temp directory.

22. **Key is shorter than the student edition**
    `\jtselfq` and `\jtmcqspace` add answer lines to the student edition only. A small
    difference is normal; check that the key has no blank page.

23. **Chinese leaks into the student edition**
    Chinese is only allowed in `\jtsolution` / `\jtsolpart`. `check_topic.py`'s `zh`
    gate catches it.

24. **An author-written question looks like a past paper**
    Use `\jtselfq` (prints "Author-written exam-style question") and never put a
    year/paper number in its source line.

25. **A scaffold still contains `%%PLACEHOLDER%%`**
    The PDF then shows the placeholder or the QA leak check catches `%%`. Re-run
    `scaffold_topic.py` or replace every placeholder before writing.

26. **Template copies drift**
    `template/jt_lecture.tex` and `examples/demo/_模板/jt_lecture.tex` are two files.
    After changing the template, re-copy it into the demo and rebuild. CI should diff
    them.

27. **Windows path with spaces breaks `\def\JTFONTDIR{...}`**
    Keep the repo and course paths free of spaces. If unavoidable, use a short
    symlink/junction for the build.

28. **A PDF leaks an internal path**
    A caption, source note or placeholder printed `assets/`, `.tex`, `_模板` or an
    absolute path. Never print filenames in the document; the QA leak gate catches it.

29. **Registry points at a file that no longer exists**
    Renaming a PDF without updating the registry leaves a broken entry. Update the
    path and re-check the registry, or mark the entry retired.

30. **The template is edited but only one topic is rebuilt**
    Layout changes affect every book. Rebuild all affected topics, or do not change
    the template.
