# Ship Product

The loop I build every client workflow with, from the AI Automation Workshop (25 Sep 2026). Level 2, after the skill builder.

## What it does

1. **Intake:** an eight-question ask so the client sends what you actually need (a screen recording, real examples, the ones they rejected and why).
2. **Spec:** writes SPEC.md from a nine-section template: what and why, before how.
3. **Benchmark:** 20 to 50 test cases before any code exists.
4. **Build** one step at a time, **check** it, **label** real outputs approve or reject.
5. **Lock and re-test:** approved cases become regression tests, so a change never quietly breaks what worked.
6. **Decide:** ship, fix or stop, based on the numbers.

Includes `code-scripts/check_spec.py`, which fails a spec that is missing parts.

## Install

Hand it to Claude Code:

> Install the ship-product plugin from https://github.com/adithya12345678/claude-skill-builder

Or run it yourself:

```bash
claude plugin marketplace add adithya12345678/claude-skill-builder
claude plugin install ship-product@adithya-skills
```

## Use it

Say **"ship product"**, **"let's build X"** or **"write the spec"**.

## Good to know

- Works best with skill-builder-v2: ship-product plans and tests the workflow, the skill builder builds each step as a skill.
- This is my working copy with client details removed. The worked examples are from a content agency, anonymised.
