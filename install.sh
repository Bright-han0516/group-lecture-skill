#!/usr/bin/env bash
# Register this repository as a user-level skill; it can then be used in any project.
# Usage: bash install.sh [--hosts codex|claude|all] [--check]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
HOSTS="all"
CHECK=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --hosts) [ "$#" -ge 2 ] || { echo "Missing value for --hosts" >&2; exit 2; }; HOSTS="$2"; shift 2 ;;
    --check) CHECK=1; shift ;;
    -h|--help) echo "Usage: bash install.sh [--hosts codex|claude|all] [--check]"; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done
[ -f "$ROOT/SKILL.md" ] || { echo "Not a group-lecture-builder repository: $ROOT" >&2; exit 1; }

register_skill() {
  local target="$1"
  mkdir -p "$(dirname "$target")"
  if [ -L "$target" ]; then
    if [ "$(cd "$target" 2>/dev/null && pwd -P || true)" = "$ROOT" ]; then
      echo "OK already linked: $target"
      return
    fi
    echo "FAIL: $target is a symlink to a different location (will not overwrite)" >&2
    exit 1
  fi
  if [ -e "$target" ]; then
    echo "FAIL: $target already exists (will not overwrite)" >&2
    exit 1
  fi
  ln -s "$ROOT" "$target"
  echo "INSTALLED: $target -> $ROOT"
}

case "$HOSTS" in
  all)
    register_skill "$HOME/.agents/skills/group-lecture-builder"
    register_skill "$HOME/.claude/skills/group-lecture-builder"
    ;;
  codex) register_skill "$HOME/.agents/skills/group-lecture-builder" ;;
  claude) register_skill "$HOME/.claude/skills/group-lecture-builder" ;;
  *) echo "Unsupported --hosts: $HOSTS (choose codex, claude, all)" >&2; exit 2 ;;
esac

echo
echo "Skill registration complete. Open a new agent session and ask it to use group-lecture-builder."
echo "Source: $ROOT (keep this folder; links point to it)."
if [ "$CHECK" -eq 1 ]; then
  echo "Running environment and demo checks..."
  (cd "$ROOT" && ./bootstrap.sh)
else
  echo "Build prerequisites are checked separately. Run: cd \"$ROOT\" && ./bootstrap.sh"
  echo "XeLaTeX + Python/PyMuPDF are required to make PDFs; installation does not silently install system packages."
fi
