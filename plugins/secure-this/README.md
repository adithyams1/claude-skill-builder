# Secure This

A security audit and hardening skill for Claude Code skills and agent workflows. It maps the workflow as a data flow diagram, sweeps nine layers (purpose down to observability) for threats, applies the Rule of Two, and checks every control for what actually enforces it.

It assumes the model can be fully compromised by prompt injection and asks what it could reach if it were.

## What it produces

- A threat model (`<target>/.security/threat-model.md`): data flow diagram, inventory, layer-by-layer findings, 15 hard gates, a grade, and a confidence score
- Two options, maximum security and balanced, with every control costed (build, run, friction, money)
- Staged config, never applied without your yes: `proposed-settings.json` (sandbox, egress allowlist, credential masking), `proposed-hooks/*.sh`, and OS-level hardening commands
- A hardening report with incident response steps and a list of what was not checked. UNKNOWN is a valid verdict

## Install

```
claude plugin marketplace add adithyams1/claude-skill-builder
claude plugin install secure-this@adithya-skills
```

## Usage

Say "secure this", "audit this skill", "is this safe", "harden this workflow", "security review" or "can this leak my keys", pointing at a skill folder or describing the workflow. If the workflow does not exist yet, it asks its questions before modelling anything.

## Notes

This is a working copy of a skill in daily use, with personal and client details removed. The OS hardening reference is written for macOS; the questions carry over to Linux.

It is guidance, not a guarantee. It does architectural analysis, not live penetration testing, and its threat catalogue refreshes itself when older than 30 days. Treat the output as a structured second opinion and review every staged change before applying it.
