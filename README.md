# Skill Builder — a Claude Code plugin

A Claude Code skill that builds *other* production-ready skills using a structured framework:
requirements gathering, connector locking, quality gates / rubrics, and a self-improving
knowledge base that gets smarter every run.

---

## AI Automation Workshop skills (new, 25 Sep 2026)

Four skills from the workshop. Each one installs on its own and has its own README.

| Skill | What it does | Install |
|---|---|---|
| [skill-builder-v2](plugins/skill-builder-v2) | Level 1. Builds one skill with you: every question up front, then the files, and it won't call it done until real outputs are approved. | `claude plugin install skill-builder-v2@adithya-skills` |
| [ship-product](plugins/ship-product) | Level 2. Runs a whole workflow build: intake, spec, a test set before any code, build, label, re-test, then ship, fix or stop. | `claude plugin install ship-product@adithya-skills` |
| [workflow-flowchart](plugins/workflow-flowchart) | Turns any workflow into an interactive flowchart you can show a client. | `claude plugin install workflow-flowchart@adithya-skills` |
| [secure-this](plugins/secure-this) | Security check before a workflow goes live: prompt injection, keys, what it can touch. | `claude plugin install secure-this@adithya-skills` |

First add the marketplace once:

```bash
claude plugin marketplace add adithya12345678/claude-skill-builder
```

Or just paste this into Claude Code:

> Install the skill-builder-v2, ship-product, workflow-flowchart and secure-this plugins from https://github.com/adithya12345678/claude-skill-builder

Suggested order: skill-builder-v2 to build your first skill, ship-product once you are building a full workflow, workflow-flowchart to show it, secure-this before it goes live.

These are my working copies with client and personal details removed.

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
plugins/
├── skill-builder/        the original skill builder
├── skill-builder-v2/     the workshop version (Level 1)
├── ship-product/         the full build loop (Level 2)
├── workflow-flowchart/   interactive workflow diagrams
└── secure-this/          security check before going live
```

Each plugin has its own README, a `.claude-plugin/plugin.json` and a `skills/<name>/` folder with the
SKILL.md, references, scripts and a knowledge base that starts empty and fills as you use it.

## Notes
- Zero setup. No API keys, no external services, no personal data bundled.
- Your built skills and their learned examples stay on your machine only.

## License
MIT
