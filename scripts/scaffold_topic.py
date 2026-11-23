#!/usr/bin/env python3
"""Scaffold a topic folder for the group-style lecture pipeline.

Example:
    python3 scripts/scaffold_topic.py --root "/path/to/course/IB/集团讲义" \
        A.3 Energy "Work, energy and power"

Creates:
    <root>/_模板/                     template, fonts, rsfs, assets, helper scripts
    <root>/A3_Energy/src/             main .tex, build.sh, assets/{exam,exam2,exam3}
    <root>/A3_Energy/dist/            output PDFs
    <root>/A3_Energy/qa/              QA records and build logs
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "template"
VENDOR_TEXMF = REPO / "vendor" / "texmf"


def copy_tree(src: Path, dst: Path) -> None:
    if not src.is_dir():
        return
    shutil.copytree(src, dst, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.environ.get("GLB_ROOT", "."),
                    help="course 集团讲义 directory (default: $GLB_ROOT or cwd)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing topic")
    ap.add_argument("--board", choices=["IB", "CIE", "AQA", "EDEXCEL", "AP"], default="IB", help="exam board (default: IB for backwards compatibility)")
    ap.add_argument("code", help="topic code, e.g. A.3")
    ap.add_argument("name", help="short directory name, e.g. Energy")
    ap.add_argument("title", help="English title, e.g. Work, energy and power")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    stem = args.code.replace(".", "")
    topic = root / f"{stem}_{args.name.replace(' ', '_')}"
    if topic.exists() and not args.force:
        print(f"error: {topic} exists; use --force to overwrite its skeleton", file=sys.stderr)
        return 1

    tmpl_dir = root / "_模板"
    for sub in (tmpl_dir / "assets", tmpl_dir / "fonts"):
        sub.mkdir(parents=True, exist_ok=True)

    # Template + tooling (authoritative copy lives in this repo).
    for name in ("jt_lecture.tex", "jt_topic.tex", "TOPIC_KIT.md"):
        shutil.copy2(TEMPLATE / name, tmpl_dir / name)
    shutil.copy2(REPO / "scripts" / "build_topic.sh", tmpl_dir / "build_topic.sh")
    shutil.copy2(REPO / "scripts" / "check_topic.py", tmpl_dir / "check_topic.py")
    copy_tree(TEMPLATE / "fonts", tmpl_dir / "fonts")
    copy_tree(TEMPLATE / "assets", tmpl_dir / "assets")
    if VENDOR_TEXMF.is_dir():
        copy_tree(VENDOR_TEXMF, tmpl_dir / "texmf")

    topic.mkdir(parents=True, exist_ok=True)
    (topic / ".glb-board").write_text(args.board + "\n", encoding="utf-8")

    src = topic / "src"
    assets = src / "assets"
    for sub in [src, assets, assets / "exam", assets / "exam2", assets / "exam3",
                topic / "dist", topic / "qa"]:
        sub.mkdir(parents=True, exist_ok=True)

    build = src / "build.sh"
    shutil.copy2(REPO / "scripts" / "build_topic.sh", build)
    build.chmod(0o755)

    skel = (TEMPLATE / "jt_topic.tex").read_text(encoding="utf-8")
    header = f"header_{stem.lower()}.jpg"
    main = (skel.replace("%%CODE%%", args.code)
                .replace("%%ENUPPER%%", args.title.upper())
                .replace("%%TITLE%%", args.title)
                .replace("%%HEADER%%", header)
                .replace("%%STEM%%", stem)
                .replace("%%CH1_TITLE%%", "Chapter 1")
                .replace("%%SECTION TITLE%%", "First section")
                .replace("%%CH2_TITLE%%", "Chapter 2"))
    (src / f"{stem}.tex").write_text(main, encoding="utf-8")

    chapter_map = f"""# Chapter map — {args.code} {args.title}

The chapter and section numbers below are the only numbering source for the body
and practice authors. Fill this in, show it to the user once, then write.

| Chapter | Sections | Syllabus understandings |
|---|---|---|
| 1 | 1.1, 1.2 | |
| 2 | 2.1, 2.2 | |

Page target (student body, excluding practice): ____ pages.
HL-only content: yes / no.
"""
    (topic / "qa" / "chapter_map.md").write_text(chapter_map, encoding="utf-8")

    # Default header: reuse the neutral placeholder until a real photo is supplied.
    default_header = TEMPLATE / "assets" / "header_default.jpg"
    if default_header.is_file():
        shutil.copy2(default_header, assets / header)
    placeholder = TEMPLATE / "assets" / "fig_placeholder.png"
    if placeholder.is_file():
        shutil.copy2(placeholder, assets / "fig_xxx.png")

    print(topic)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
