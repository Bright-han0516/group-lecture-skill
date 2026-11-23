# Global install: Codex and Claude Code

## One command, once per computer

For a public repository, run in macOS/Linux terminal (Windows: WSL):

```bash
git clone https://github.com/Bright-han0516/group-lecture-skill.git "$HOME/.local/share/group-lecture-builder" && bash "$HOME/.local/share/group-lecture-builder/install.sh" --hosts all
```

The command installs the **Skill registration**, not a full TeX distribution. It creates user-level symlinks:

- Codex: `~/.agents/skills/group-lecture-builder -> ~/.local/share/group-lecture-builder`
- Claude Code: `~/.claude/skills/group-lecture-builder -> ~/.local/share/group-lecture-builder`

The original repository folder must remain. The installer is idempotent for symlinks it already owns and refuses to overwrite other files. Restart your agent if it does not discover newly added skills.

Use only one host with `--hosts codex` or `--hosts claude`. Hosts without verified user-level Skill support may still follow `PROMPT.md` manually.

## Verify build readiness

```bash
cd "$HOME/.local/share/group-lecture-builder"
./bootstrap.sh
```

This checks XeLaTeX, packages, Python/PyMuPDF, bundled fonts and a demo build. If it prints `READY`, the **environment** is ready. If dependencies are missing, follow its `fix:` hints before attempting a real topic. Installing a complete TeX distribution is a separate, potentially large system operation; this script does not silently run `sudo`, `brew` or `apt`.

## Use in any project

Start a fresh Codex / Claude Code session anywhere and ask:

> Use group-lecture-builder to make a CIE 9702 AS topic handout. First check the environment and ask me for the syllabus and authorised past papers. Do not invent source references.

The agent should find the user-level skill, locate its repository root from its own `SKILL.md` path, and call scripts with **absolute paths**. Course files are created in the `--root` location, not inside the skill installation.

## Update an existing installation

```bash
git -C "$HOME/.local/share/group-lecture-builder" pull --ff-only
bash "$HOME/.local/share/group-lecture-builder/install.sh" --hosts all
```

To run the demo check in the same step, add `--check`. Updates from Git are not automatically installed and may alter production; review changes before updating.

## Notes

- `AGENTS.md` is repository-wide development guidance. It is not a substitute for a user-level Skill installation.
- A purely chat-based assistant cannot run the local build. Give it `PROMPT.md` to review sources and content instead.
- Local university/publisher materials and exam questions are not included. Minimum genuine inputs: syllabus and authorised past papers.
