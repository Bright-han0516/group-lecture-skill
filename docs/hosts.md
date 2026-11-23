# Host compatibility

This repo is deliberately host-neutral: `AGENTS.md` is the common entry, `SKILL.md`
is the skill card for DSH/Claude-style hosts, and `PROMPT.md` has copy-paste prompts
for chat-only tools. The actual build needs a shell with XeLaTeX and Python.

Last verified: 2026-11-23.

## Where to put the repo

| Host | Path | Entry it reads |
|---|---|---|
| DSH | `~/.dsh/skills/group-lecture-builder` | `SKILL.md` |
| Claude Code | `~/.claude/skills/group-lecture-builder` | `SKILL.md` |
| Codex | any directory, e.g. `~/group-lecture-skill` | `AGENTS.md` |
| Cursor | any directory, e.g. `~/group-lecture-skill` | `AGENTS.md` |
| Kimi Code | any directory; verify its docs | `AGENTS.md` / `CLAUDE.md` |
| WorkBuddy / Doubao Office | no local path; ZIP or paste | `PROMPT.md` |

The directory name `group-lecture-builder` matters only to hosts that scan a skills
folder and match it to the `name` in `SKILL.md`. Coding agents that read `AGENTS.md`
do not care about the folder name.

| Host | Entry it reads | Can run shell? | Build PDFs? | Best use |
|---|---|---|---|---|
| **Codex** (CLI/IDE) | `AGENTS.md` | Yes (Windows via WSL) | Yes, if TeX Live is installed | Full pipeline |
| **Kimi Code** | `AGENTS.md` / `CLAUDE.md` (verify) | Yes, if it is the CLI/IDE form | Yes, if TeX Live is installed | Full pipeline |
| **Claude Code / DSH** | `SKILL.md` + `AGENTS.md` | Yes | Yes | Full pipeline, installed as a skill |
| **WorkBuddy** | paste `PROMPT.md` | Depends on the product | Only if it can execute local commands and has TeX | Review, or full pipeline if it has a code tool |
| **Doubao Office** | paste `PROMPT.md` | Typically no local TeX | No | Review, plan, polish text |
| **Any chat-only AI** | paste `PROMPT.md` | No | No | Review only |

"Can run shell" is the dividing line. A host that can read the repository but cannot
execute `xelatex` cannot produce the PDFs, no matter how well it understands the
skill.

## 5-minute compatibility test

Give the agent this, verbatim:

```text
Run this, then paste the last 30 lines of output:

gh repo clone Bright-han0516/group-lecture-skill ~/group-lecture-skill && \
  cd ~/group-lecture-skill && ./bootstrap.sh

If bootstrap fails, stop and show me the FAIL lines and fix hints.
If it succeeds, read MATERIALS.md and ask me for the missing materials.
Do not continue to a real topic yet.
```

`bootstrap.sh` runs preflight, the demo build and QA in one pass. It prints `READY`
only if all three succeed.

- `READY` → the host can run the full pipeline.
- Preflight fails on `xelatex`/packages → install TeX Live, or use a machine/container
  that has it.
- The host cannot run commands at all → review-only; use the review prompt.
- After `READY`, the agent must ask for the items in `MATERIALS.md` before writing.

## Per-host notes

### Codex

- Reads `AGENTS.md` at the repo root automatically; no skill installation needed.
- Has shell and file tools. On Windows, run Codex inside WSL; native PowerShell
  cannot execute `build.sh`.
- Codex Cloud may not have TeX Live. If it has no TeX, use it for editing/PRs and run
  the build on a local machine or in Codespaces.

### Kimi Code

- If it is the CLI/IDE form with a shell, it can follow `AGENTS.md`/`CLAUDE.md` and
  run the compatibility test. Confirm it actually reads one of those files; if not,
  paste the build prompt from `PROMPT.md`.
- If it is a chat-only form, treat it as review-only.

### Claude Code / DSH

- Clone to `~/.claude/skills/group-lecture-builder` or
  `~/.dsh/skills/group-lecture-builder`; `SKILL.md` is the entry.
- `CLAUDE.md` is a pointer to `AGENTS.md` for Claude-compatible hosts.

### WorkBuddy / Doubao Office

- These are usually document/office assistants. They can read a pasted prompt and
  review a chapter map, a draft or a QA record, but they generally cannot run
  `xelatex` or crop papers.
- Use the **review mode** prompt in `PROMPT.md`. Do not ask them to "build the PDF";
  they will either refuse or describe a build they did not perform.
- If the product has a local code-execution tool, run the compatibility test first.

### Private repository access

The repo is private. Cloud agents need to be connected to GitHub and invited as
collaborators; a pasted URL alone will 404. For a chat-only colleague, share a ZIP
of the repo or the release assets instead.

## What still needs the user

Even on a fully capable host, the pipeline needs the syllabus, the textbook PDF and
the authorised past papers. Those are not in this repository. The agent must stop
and ask for them rather than inventing sources.
