#!/bin/bash
# Build a topic handout in two editions: student (blanks) + answer key.
#
# Usage (from <Topic>/src):  ./build.sh [main.tex]
# Environment:
#   GLB_TEMPLATE_DIR  dir containing jt_lecture.tex (default: ../_模板)
#   GLB_FONTS_DIR     dir with TeX Gyre .otf files (default: $GLB_TEMPLATE_DIR/fonts)
#   GLB_TEXMF         texmf tree with rsfs (default: $GLB_TEMPLATE_DIR/texmf)
#   GLB_SLUG          output slug (default: topic directory name)
#   XELATEX           xelatex binary (default: first on PATH)
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SRC_DIR"
TOPIC_DIR="$(dirname "$SRC_DIR")"

TEMPLATE_DIR="${GLB_TEMPLATE_DIR:-$TOPIC_DIR/../_模板}"
if [ ! -f "$TEMPLATE_DIR/jt_lecture.tex" ]; then
  echo "error: jt_lecture.tex not found in $TEMPLATE_DIR" >&2
  echo "       run the scaffold script, or set GLB_TEMPLATE_DIR" >&2
  exit 1
fi
FONTS_DIR="${GLB_FONTS_DIR:-$TEMPLATE_DIR/fonts}"
if [ ! -f "$FONTS_DIR/texgyretermes-regular.otf" ]; then
  echo "error: TeX Gyre fonts not found in $FONTS_DIR" >&2
  echo "       set GLB_FONTS_DIR to the repo's template/fonts" >&2
  exit 1
fi

TEXMF="${GLB_TEXMF:-$TEMPLATE_DIR/texmf}"
if [ -d "$TEXMF" ]; then
  export TEXMFHOME="$TEXMF"
fi

if [ $# -ge 1 ]; then MAIN="$1"; else
  MAIN="$(ls *.tex 2>/dev/null | grep -vE '^_' | grep -vE '_[pw][0-9]+\.tex$' | head -1 || true)"
fi
[ -n "${MAIN:-}" ] || { echo "error: no main .tex file" >&2; exit 1; }
CODE="$(basename "$MAIN" .tex)"
SLUG="${GLB_SLUG:-$(basename "$TOPIC_DIR")}"
SLUG="$(printf '%s' "$SLUG" | tr ' ' '_')"

XELATEX="${XELATEX:-$(command -v xelatex || true)}"
[ -n "$XELATEX" ] || { echo "error: xelatex not found; install TeX Live or set XELATEX" >&2; exit 1; }

if ! kpsewhich rsfs10.tfm >/dev/null 2>&1; then
  echo "warning: rsfs10.tfm not found. Arrows (\to, \rightarrow) may fail." >&2
  echo "         set GLB_TEXMF to the repo's vendor/texmf, or: tlmgr install rsfs" >&2
fi

OUT="$TOPIC_DIR/dist"
BUILD="$TOPIC_DIR/qa/build"
mkdir -p "$OUT" "$BUILD"

run_tex() {
  local job="$1" log="$2"; shift 2
  "$XELATEX" -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory="$BUILD" -jobname="$job" "$@" >"$log" 2>&1
}

# Two passes per edition: the first writes .out/.aux, the second resolves
# bookmarks, lastpage and cross-references.
run_tex "${CODE}_student" "$BUILD/student.log" \
  "\def\JTFONTDIR{$FONTS_DIR}\input{$MAIN}"
run_tex "${CODE}_student" "$BUILD/student.log" \
  "\def\JTFONTDIR{$FONTS_DIR}\input{$MAIN}"
cp "$BUILD/${CODE}_student.pdf" "$OUT/IB_${SLUG}_GroupLecture_Student.pdf"

run_tex "${CODE}_key" "$BUILD/key.log" \
  "\def\JTFONTDIR{$FONTS_DIR}\def\JTKEY{}\input{$MAIN}"
run_tex "${CODE}_key" "$BUILD/key.log" \
  "\def\JTFONTDIR{$FONTS_DIR}\def\JTKEY{}\input{$MAIN}"
cp "$BUILD/${CODE}_key.pdf" "$OUT/IB_${SLUG}_GroupLecture_Key.pdf"

if command -v pdfinfo >/dev/null 2>&1; then
  pdfinfo "$OUT/IB_${SLUG}_GroupLecture_Student.pdf" | grep '^Pages:'
  pdfinfo "$OUT/IB_${SLUG}_GroupLecture_Key.pdf" | grep '^Pages:'
fi
echo "ok: $OUT/IB_${SLUG}_GroupLecture_{Student,Key}.pdf"
