# Skill Builder — a Claude Code plugin

A Claude Code skill that builds *other* production-ready skills using a structured framework:
requirements gathering, connector locking, quality gates / rubrics, and a self-improving
knowledge base that gets smarter every run.

---

## Easiest way to install — just hand this repo to Claude

Open Claude Code and paste this one line:

> Install the Claude Code plugin from https://github.com/adithya12345678/claude-skill-builder — read its README and set it up.

Claude will do the rest. Then say **"build me a skill"** to start.

---

## 🤖 CLAUDE: INSTRUCTIONS FOR YOU

If a user has pointed you at this repository and asked you to install/set it up, run these two
shell commands (non-interactive CLI — works from the Bash tool):

```bash
claude plugin marketplace add adithya12345678/claude-skill-builder
claude plugin install skill-builder@adithya-skills
```

Then confirm to the user: *"Skill Builder is installed — say 'build me a skill' to start."*
No API keys, no config, no personal data. Nothing else is required.

---

## Manual install (if you'd rather type it yourself)

**One terminal command:**

```bash
claude plugin marketplace add adithya12345678/claude-skill-builder && claude plugin install skill-builder@adithya-skills
```

**Or inside Claude Code (interactive):**

```
/plugin marketplace add adithya12345678/claude-skill-builder
/plugin install skill-builder@adithya-skills
```

To get future updates:

```
/plugin marketplace update adithya-skills
```

## Use it

Once installed, just say **"build me a skill"**, **"create a new skill"**, or **"skill builder"**
and it'll walk you through building one end to end — process steps, connectors, quality gates,
knowledge base, and a changelog.

## What's inside

```
plugins/skill-builder/
├── .claude-plugin/plugin.json     ← plugin manifest
└── skills/skill-builder/
    ├── SKILL.md                    ← the skill itself
    ├── CHANGELOG.md
    └── knowledge-base/             ← starts empty; fills as you use it
```

## Notes
- Zero setup. No API keys, no external services, no personal data bundled.
- Your built skills and their learned examples stay on your machine only.

## License
MIT
