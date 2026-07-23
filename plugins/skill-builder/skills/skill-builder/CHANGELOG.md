# Changelog — skill-builder

## v1.0.0 — plugin release
**Published as a Claude Code plugin.** Portable, zero-setup edition of the skill-builder skill.
- Paths genericized: all hardcoded `/Users/...` paths replaced with `~/.claude/skills/...`
- Written in generic second person ("the user") — no personalization step required
- Personal infrastructure removed: unattended-run logging + memory-index registration made optional/generic
- Knowledge base ships as empty stubs — every installer starts clean and builds their own memory
- No secrets, no API keys, no personal data bundled

---

<!-- Every time SKILL.md is updated, log it here: -->
<!-- ## vX.Y.Z — [date] -->
<!-- **Changed:** [what changed and why] -->
