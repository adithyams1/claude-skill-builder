# Skill Builder — a Claude Code plugin

A Claude Code skill that builds *other* production-ready skills using a structured framework:
requirements gathering, connector locking, quality gates / rubrics, and a self-improving
knowledge base that gets smarter every run.

## Install (from this repo)

In Claude Code, run:

```
/plugin marketplace add adithya12345678/claude-skill-builder
/plugin install skill-builder@adithya-skills
```

That's it. To get future updates:

```
/plugin marketplace update adithya-skills
```

## Use it

Once installed, just say:

- **"build me a skill"**
- **"create a new skill"**
- **"skill builder"**

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
