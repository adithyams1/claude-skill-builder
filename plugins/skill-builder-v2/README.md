# Skill Builder v2

The skill builder from the AI Automation Workshop (25 Sep 2026). It builds one Claude Code skill with you, step by step.

## What it does

- Asks every question up front: what the skill does, its inputs, tools, what a good output looks like.
- Writes the SKILL.md, reference files and a knowledge base that learns from every run.
- Won't call the skill done until real outputs are approved (3 approved outputs from 2 runs, plus 1 correction).
- Ships a checker (`code-scripts/check_skill.py`) that audits any skill against that bar.

This is a newer version of the original `skill-builder` plugin in this repo. Both can be installed side by side.

## Install

Hand it to Claude Code:

> Install the skill-builder-v2 plugin from https://github.com/adithyams1/claude-skill-builder

Or run it yourself:

```bash
claude plugin marketplace add adithyams1/claude-skill-builder
claude plugin install skill-builder-v2@adithya-skills
```

## Use it

Start a new Claude Code session and say **"build me a skill"** or **"skill builder"**.

## Good to know

- It stores API keys in one file (`~/.claude/keys.json`, keyed by service) and never inside a skill. Use your own file if you prefer, and tell it where.
- Some steps are optional (a memory index, a project tracker, tracing). Skip what you don't use.
- This is my working copy with client and personal details removed.
