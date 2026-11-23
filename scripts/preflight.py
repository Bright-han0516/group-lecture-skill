#!/usr/bin/env python3
"""Preflight check for the group-lecture-skill repo.

Run this before building anything:

    python3 scripts/preflight.py

It verifies the toolchain, TeX packages, bundled fonts, vendored rsfs, Python
dependencies and template assets. Missing hard requirements exit 1 with a fix hint.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "template" / "fonts"
TEXMF = ROOT / "vendor" / "texmf"
ASSETS = ROOT / "template" / "assets"

TEX_PACKAGES = [
    "fontspec.sty", "xeCJK.sty", "tcolorbox.sty", "tikz.sty",
    "tabularx.sty", "needspace.sty", "fancyhdr.sty", "lastpage.sty",
    "hyperref.sty", "enumitem.sty", "colortbl.sty", "geometry.sty",
    "etoolbox.sty", "amsmath.sty", "graphicx.sty", "xcolor.sty",
]
FONT_FILES = [
    "texgyretermes-regular.otf", "texgyretermes-bold.otf",
    "texgyretermes-italic.otf", "texgyretermes-bolditalic.otf",
    "texgyreheros-regular.otf", "texgyreheros-bold.otf",
    "texgyreheroscn-regular.otf", "texgyreheroscn-bold.otf",
]


def run(cmd: list[str], env: dict | None = None) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, env=env)
        return p.returncode, (p.stdout + p.stderr).strip()
    except FileNotFoundError:
        return 127, "not found"


def main() -> int:
    checks: list[dict] = []

    def add(name: str, ok: bool, detail: str, hard: bool = True, fix: str = "") -> None:
        checks.append({"name": name, "ok": ok, "detail": detail, "hard": hard, "fix": fix})

    xelatex = shutil.which("xelatex")
    add("xelatex", bool(xelatex), xelatex or "not on PATH",
        fix="install TeX Live / TinyTeX, or set XELATEX")

    kpsewhich = shutil.which("kpsewhich")
    add("kpsewhich", bool(kpsewhich), kpsewhich or "not on PATH",
        fix="install TeX Live / TinyTeX")

    env = dict(os.environ)
    if TEXMF.is_dir():
        env["TEXMFHOME"] = str(TEXMF)
    else:
        add("vendor/texmf", False, str(TEXMF), fix="restore vendor/texmf from the repo")

    if kpsewhich:
        for pkg in TEX_PACKAGES:
            rc, out = run([kpsewhich, pkg], env=env)
            path = out.splitlines()[0] if out else ""
            add(f"tex:{pkg}", rc == 0 and bool(path), path or "missing",
                fix=f"tlmgr install {pkg.replace('.sty', '')}")
        rc, out = run([kpsewhich, "rsfs10.tfm"], env=env)
        add("tex:rsfs10.tfm", rc == 0 and bool(out), out.splitlines()[0] if out else "missing",
            fix="the repo vendors it in vendor/texmf; check TEXMFHOME")

    for f in FONT_FILES:
        p = FONTS / f
        add(f"font:{f}", p.is_file(), str(p), fix="restore template/fonts from the repo")

    for f in ("logo.png", "header_default.jpg"):
        p = ASSETS / f
        add(f"asset:{f}", p.is_file(), str(p), fix="restore template/assets from the repo")

    try:
        import fitz  # noqa: F401
        add("python:pymupdf", True, "import fitz OK",
            fix="pip install pymupdf")
    except Exception as exc:
        add("python:pymupdf", False, str(exc), fix="pip install pymupdf")

    for tool, hard in (("pdftoppm", False), ("pdffonts", False), ("pdfinfo", False)):
        p = shutil.which(tool)
        add(f"tool:{tool}", bool(p), p or "not on PATH (optional)", hard=hard,
            fix=f"install poppler for {tool}")

    # CJK font: macOS Songti SC or TeX Live Fandol. Only needed for the key.
    cjk = False
    if shutil.which("fc-list"):
        rc, out = run(["fc-list", ":lang=zh"])
        cjk = rc == 0 and bool(out)
    if not cjk and kpsewhich:
        rc, out = run([kpsewhich, "FandolSong-Regular.otf"], env=env)
        cjk = rc == 0 and bool(out)
    if sys.platform == "darwin":
        cjk = cjk or Path("/System/Library/Fonts/Supplemental/Songti.ttc").exists()
    add("cjk-font", cjk, "Songti SC / Fandol", hard=False,
        fix="macOS: Songti SC is preinstalled; TeX Live: tlmgr install fandol")

    hard_fail = [c for c in checks if c["hard"] and not c["ok"]]
    if "--json" in sys.argv:
        print(json.dumps(checks, ensure_ascii=False, indent=2))
    else:
        for c in checks:
            mark = "OK  " if c["ok"] else ("FAIL" if c["hard"] else "WARN")
            print(f"[{mark}] {c['name']:<28} {c['detail']}")
            if not c["ok"] and c["fix"]:
                print(f"       fix: {c['fix']}")
        print()
        if hard_fail:
            print(f"{len(hard_fail)} hard requirement(s) missing; fix them before building.")
        else:
            print("preflight passed.")
    return 1 if hard_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
