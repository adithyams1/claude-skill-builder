# MCP & Tool Instructions for secure-this

## Locked Methods
These are the ONLY methods this skill uses. If a method fails, debug it - do not switch.

- **Bash (read/inspect)** - reading the target skill, its scripts, settings, MCP config.
  Check BOTH skill stores: `~/.claude/skills` and the app plugin store.
- **Write (staged only)** - to `<target>/.security/` exclusively. Never write
  `~/.claude/settings.json` directly; stage and diff.
- **WebFetch + WebSearch** - freshness pass only (Step 0), when the catalogue is
  over 30 days old. If it fails, proceed on the stale catalogue but say so at the
  top of the report and mark affected findings UNKNOWN.

## Rejected alternatives (Solution Survey, 2026-08-19)

| Considered | Why rejected |
|---|---|
| Write config live into `~/.claude/settings.json` | A wrong `denyRead` locks the user out of their own tooling mid-session, and settings changes are the exact thing an attacker would want. Staging + diff keeps a human between the audit and the boundary change |
| Emit a patch file for manual application | Defeats the chosen output mode. Controls that require a second manual step tend not to exist |
| Run the audit as a subagent fan-out | The audit needs the full picture of one workflow in one context. Splitting it across agents loses the cross-step trifecta view, which is the whole point |
| Hardcode the control list permanently | It rots invisibly. Credential masking is the proof: a skill built before it shipped would confidently recommend a worse answer forever. Hence the freshness stamp + live capability discovery in Step 0 |

## Known Failure Fixes

- `code.claude.com/docs/*` and `platform.claude.com/docs/*` fetch cleanly.
  Some vendor security blogs return 403 - skip them, do not retry in a loop.
- Large system-card PDFs exceed the fetch size limit. Use a secondary summary
  source for those numbers rather than retrying the PDF.
- Some browser automation tools mangle `file://` URLs. To open a local report, use the
  OS open command (`open <path>` on macOS, `xdg-open <path>` on Linux).

## Tool Failure Protocol
1. Read the error message carefully
2. Check Known Failure Fixes above first
3. If not listed: diagnose root cause of THIS tool - do not switch methods
4. Log the failure + fix here under Known Failure Fixes
5. Retry with fix applied
