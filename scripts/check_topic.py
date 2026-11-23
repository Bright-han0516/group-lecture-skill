#!/usr/bin/env python3
"""Structural QA for a built topic handout.

Usage:
    python3 check_topic.py <TopicDir> [--json] [--no-fail]

Checks each PDF in <TopicDir>/dist:
  pages, bookmarks, blank pages, internal path leaks, missing-image placeholders,
  embedded fonts, Chinese character count.

Exit code 1 if a gate fails (student edition must have zero Chinese characters).
Requires PyMuPDF (`pip install pymupdf`). `pdffonts` from poppler is optional;
without it, font embedding is checked through PyMuPDF.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except Exception as exc:  # pragma: no cover
    sys.exit(f"PyMuPDF is required: pip install pymupdf ({exc})")

LEAK_PATTERNS = [
    ".tex", "assets/", "_模板", "%%", "/Users/", "/home/",
    "C:\\Users\\", "GLB_TEMPLATE", "GLB_FONTS",
]
MISSING_MARKERS = ("missing figure", "missing image", "cover image missing")


def embedded_fonts_via_pdffonts(pdf: Path) -> list[str] | None:
    exe = shutil.which("pdffonts")
    if not exe:
        return None
    out = subprocess.run([exe, str(pdf)], capture_output=True, text=True).stdout
    lines = out.splitlines()
    if len(lines) < 2:
        return []
    # Columns are right-aligned: ... emb sub uni object ID. Split from the
    # right so font names containing spaces (CID Type 0C) do not shift the index.
    bad = []
    for line in lines[2:]:
        parts = line.split()
        if len(parts) < 6:
            continue
        if parts[-5] != "yes":
            bad.append(parts[0])
    return bad


def embedded_fonts_via_fitz(doc: fitz.Document) -> list[str]:
    bad = []
    seen = set()
    for page in doc:
        for font in page.get_fonts(full=True):
            xref = font[0]
            if xref in seen:
                continue
            seen.add(xref)
            try:
                info = doc.extract_font(xref)
            except Exception:
                continue
            buffer = info[3] if len(info) > 3 else b""
            if not buffer:
                bad.append(font[3])
    return bad


def check_pdf(pdf: Path, strict: bool) -> dict:
    doc = fitz.open(pdf)
    text = "".join(page.get_text() for page in doc)
    blanks = []
    for i, page in enumerate(doc, start=1):
        plain = page.get_text().strip()
        images = page.get_images(full=True)
        drawings = page.get_drawings()
        if len(plain) < 40 and not images and len(drawings) < 5:
            blanks.append(i)

    leaks = [p for p in LEAK_PATTERNS if p in text]
    missing = sum(text.count(m) for m in MISSING_MARKERS)
    zh = len(re.findall(r"[\u4e00-\u9fff]", text))

    not_embedded = embedded_fonts_via_pdffonts(pdf)
    font_source = "pdffonts"
    if not_embedded is None:
        not_embedded = embedded_fonts_via_fitz(doc)
        font_source = "pymupdf"

    is_student = "student" in pdf.name.lower()
    gates = {
        "blank_pages": blanks,
        "path_leaks": leaks,
        "missing_images": missing,
        "not_embedded_fonts": not_embedded,
    }
    if is_student:
        gates["student_chinese"] = zh
    failed = (
        bool(blanks) or bool(leaks) or missing > 0 or bool(not_embedded)
        or (is_student and zh > 0)
    )
    return {
        "file": pdf.name,
        "pages": doc.page_count,
        "bookmarks": len(doc.get_toc()),
        "chars": len(text),
        "chinese": zh,
        "font_source": font_source,
        **gates,
        "pass": not failed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", nargs="?", default=".", help="topic directory")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--no-fail", action="store_true", help="always exit 0")
    args = parser.parse_args()

    dist = Path(args.topic).resolve() / "dist"
    if not dist.is_dir():
        print(f"NO dist directory: {dist}")
        return 0 if args.no_fail else 1
    pdfs = sorted(dist.glob("*.pdf"))
    if not pdfs:
        print(f"NO PDF in {dist}")
        return 0 if args.no_fail else 1

    results = [check_pdf(p, strict=not args.no_fail) for p in pdfs]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(
                f"{r['file']}: pages={r['pages']} bookmarks={r['bookmarks']} "
                f"chars={r['chars']} zh={r['chinese']} fonts={r['font_source']}"
            )
            print(
                f"  blanks={r['blank_pages']}  leaks={r['path_leaks']}  "
                f"missing_images={r['missing_images']}  "
                f"not_embedded={r['not_embedded_fonts']}"
            )
            print(f"  {'PASS' if r['pass'] else 'FAIL'}")

    if args.no_fail:
        return 0
    return 0 if all(r["pass"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
