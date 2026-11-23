#!/bin/bash
# Build the demo without scaffolding a course directory.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
export GLB_TEMPLATE_DIR="$HERE/_模板"
export GLB_FONTS_DIR="$REPO/template/fonts"
export GLB_TEXMF="$REPO/vendor/texmf"
export GLB_SLUG="Demo_Topic"
cd "$HERE/Demo_Topic/src"
exec ./build.sh Demo.tex
