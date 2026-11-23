# Claude-compatible entry

This repository is a skill package, not a course database. Read `AGENTS.md` first;
it points to `README.md`, `SKILL.md` and the reference files. The non-negotiables
(no host fonts, no local template overrides, no copyrighted assets, no student data)
are in `AGENTS.md` and apply to every host.

If you are a coding agent with a shell, the first three commands are:

```bash
python3 scripts/preflight.py
(cd examples/demo && ./build.sh)
python3 scripts/check_topic.py examples/demo/Demo_Topic
```

Do not start a topic until those pass. If you cannot run a shell, use the review
prompt in `PROMPT.md`; do not claim that a PDF was built.
