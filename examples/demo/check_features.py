"""Check the demo boxes, symbol legends and answer-only scoring evidence."""
from pathlib import Path
from unicodedata import normalize

import fitz

TOPIC = Path(__file__).resolve().parent / "Demo_Topic"


def require(ok, message):
    if not ok:
        raise SystemExit(f"FAIL: {message}")


def image_pages(doc, asset):
    digest = fitz.Pixmap(str(TOPIC / "src" / "assets" / asset)).digest
    return {
        page.number
        for page in doc
        if any(img["digest"] == digest for img in page.get_image_info(hashes=True))
    }


for edition in ("Student", "Key"):
    pdfs = list((TOPIC / "dist").glob(f"*_{edition}.pdf"))
    require(len(pdfs) == 1, f"expected one demo PDF for {edition}")
    with fitz.open(pdfs[0]) as doc:
        text = {page.number: normalize("NFKC", page.get_text()) for page in doc}
        all_text = "\n".join(text.values())
        require("KEY DEFINITIONS" in all_text, f"{edition}: missing definition box")
        require(all_text.count("KEY RELATION") == 3, f"{edition}: expected three relation boxes")
        legend_groups = (
            ("average velocity", "displacement", "elapsed time", "denotes a change"),
            ("initial velocity", "final velocity", "acceleration", "displacement", "elapsed time", "Valid for constant acceleration"),
            ("downward displacement", "acceleration due to gravity", "elapsed time", "downward positive"),
        )
        require(all_text.count("Symbols.") == len(legend_groups), f"{edition}: missing symbol legend")
        for words in legend_groups:
            require(
                any(
                    all(term in segment for term in words)
                    for t in text.values()
                    for segment in (
                        " ".join(box.split()).split("Symbols.", 1)[1]
                        for box in t.split("KEY RELATION")[1:]
                        if "Symbols." in box
                    )
                ),
                f"{edition}: symbols missing or not on the same page as the relation: {words}",
            )
        require(image_pages(doc, "fig_demo_slope.png"), f"{edition}: missing explanatory figure")
        evidence = image_pages(doc, "ms/demo_scoring.png")
        caption_pages = {i for i, t in text.items() if "Demo scoring image (not official)" in t}
        if edition == "Key":
            require(evidence and evidence == caption_pages, "key image and caption must be together")
            require("Author-written marking points" in all_text, "missing author-written points")
        else:
            require(not (evidence or caption_pages), "student PDF contains demo scoring evidence")
            require("Author-written marking points" not in all_text, "student PDF contains marking points")

print("PASS: visual and formula-symbol checks in both editions; scoring evidence in Key only.")
