# Workflow Flowchart

A Claude Code skill that turns a multi-step system you have just described in conversation into an interactive pan-zoom flowchart. Every step is colour-coded by who does it (input, AI, human, tool, review gate, output), so a non-technical person can see at a glance what is automated and where a person still steps in. Built for walking a client or prospect through a system on a call.

## What it produces

- A single self-contained HTML page per system: sidebar of flows, pan-zoom canvas, optional build hours and clickable "see example" chips on nodes.
- An optional "what you asked for / where it is now" panel for platform builds.
- A browsable directory of every diagram you have made (`workflows/index.html`), rebuilt from disk on every run.

## Install

```
claude plugin marketplace add adithya12345678/claude-skill-builder
claude plugin install workflow-flowchart@adithya-skills
```

## Use

Describe the system in conversation, then say something like:

- "make a flowchart"
- "turn this into a diagram"
- "workflow diagram" or `/workflow-flowchart`

To see everything you have built: "open my workflows" or "show me all the workflows".

Diagrams are saved to `./workflows/<slug>/` by default. Set `WORKFLOWS_DIR` (or pass `--root` to `build_index.py`) to keep them somewhere else, for example `~/workflows`.

## Requirements

- Claude Code
- Python 3 (standard library only)
- Optional: a browser tool for Claude (for the screenshot smoke test) and a way to publish pages (for a shareable link). Without them, open the local HTML file yourself and share it directly.

## Note

This is a working copy of a skill used on real client work, with client names, personal paths and private links removed. The process, rules and lessons are intact.

## License

MIT
