#!/usr/bin/env bash
# One-command check: preflight + demo build + QA.
# Run from the repository root: ./bootstrap.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [ ! -f SKILL.md ] || [ ! -d examples/demo ]; then
  echo "error: run this script from the group-lecture-skill repository root." >&2
  echo "clone: gh repo clone Bright-han0516/group-lecture-skill ~/group-lecture-skill" >&2
  echo "       (skill hosts: clone into their skills directory instead)" >&2
  exit 1
fi

# Pick an interpreter that actually has PyMuPDF. On macOS the system Python often
# has it while a Homebrew Python does not.
PY=""
for cand in "${PYTHON:-python3}" python3 /usr/bin/python3 python; do
  [ -n "$cand" ] || continue
  if command -v "$cand" >/dev/null 2>&1 && "$cand" -c 'import fitz' >/dev/null 2>&1; then
    PY="$cand"
    break
  fi
done
if [ -z "$PY" ]; then
  echo "error: no Python with PyMuPDF found." >&2
  echo "fix:   python3 -m pip install -r requirements.txt" >&2
  echo "       (or use /usr/bin/python3 on macOS if it has PyMuPDF)" >&2
  exit 1
fi
echo "python: $PY"

echo
echo "== 1/3 preflight =="
if ! "$PY" scripts/preflight.py; then
  echo
  echo "NOT READY: fix the FAIL lines above, then run ./bootstrap.sh again." >&2
  exit 1
fi

echo
echo "== 2/3 demo build =="
if ! (cd examples/demo && ./build.sh); then
  echo
  echo "BUILD FAILED: see examples/demo/Demo_Topic/qa/build/*.log" >&2
  exit 1
fi

echo
echo "== 3/3 demo QA =="
if ! "$PY" scripts/check_topic.py examples/demo/Demo_Topic; then
  echo
  echo "QA FAILED: read the gate output above before starting a real topic." >&2
  exit 1
fi

cat <<'EOF'

READY. The toolchain, fonts, rsfs and template work on this machine.

Before starting a real topic, ask the user to fill in MATERIALS.md. At minimum:
  1. board + topic code + English title
  2. level (SL / HL / SL+HL) and teaching hours
  3. syllabus file path + section
  4. textbook PDF path + edition + "PDF page = printed page + offset"
  5. past-paper folder + allowed years/sessions/papers
  6. official mark-scheme folder
  7. course root directory (where _模板/ and the topic folder will live)
  8. any constraints: page target, HL-only, question count, Chinese key style

Do not start writing until the syllabus and past-paper corpus are available.
If a source is missing, say so; never invent a paper, year or question number.

Next: read README.zh-CN.md (or README.md), then SKILL.md and references/pipeline.md.
EOF
