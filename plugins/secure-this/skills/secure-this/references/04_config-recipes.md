---
last_verified: 2026-08-19
---

# Config Recipes - copy-paste starting points

Always STAGE these to `<target>/.security/proposed-settings.json` and diff
against the live `~/.claude/settings.json`. Never write live without approval.

Settings precedence: managed > user (`~/.claude/settings.json`) > project
(`.claude/settings.json`) > local. A `deny` entry from ANY scope narrows access
and no scope can remove one another scope added.

---

## R1 - Lock a workflow to its own directory, block the home dir

```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    }
  }
}
```

Exact-deny beats wide-allow, so a later broad `allowRead` cannot silently
re-expose a secret. Note `.` resolves relative to the settings file's location.

## R2 - Deny credentials outright (breaks tools that need the value)

```json
{
  "sandbox": {
    "enabled": true,
    "credentials": {
      "files": [
        { "path": "/path/to/your-key-file.json", "mode": "deny" },
        { "path": "/path/to/your-oauth-token.json", "mode": "deny" },
        { "path": "~/.ssh", "mode": "deny" }
      ],
      "envVars": [
        { "name": "GITHUB_TOKEN", "mode": "deny" }
      ]
    }
  }
}
```

## R3 - MASK credentials (the agent authenticates without ever holding the value)

This is the answer to "but the workflow needs the key." Preferred over R2
whenever the tool must actually authenticate.

```json
{
  "sandbox": {
    "enabled": true,
    "network": {
      "tlsTerminate": {},
      "allowedDomains": ["api.example.com", "api.github.com"]
    },
    "credentials": {
      "envVars": [
        { "name": "SERVICE_TOKEN", "mode": "mask", "injectHosts": ["api.example.com"] },
        { "name": "GH_TOKEN", "mode": "mask", "injectHosts": ["api.github.com"] }
      ]
    }
  }
}
```

Mechanics: the sandboxed command sees a per-session sentinel. On an outbound
request to a listed host, the proxy substitutes the real value into headers and
body. The command and anything it logs never hold the real credential.

Requirements and traps:
- `network.tlsTerminate` is REQUIRED. Without it masking fails closed: the
  sentinel reaches the server unchanged and auth fails.
- Every `injectHosts` destination must ALSO be reachable via `allowedDomains`.
- An entry with no `injectHosts` is substituted on every allowed domain. Scope it.
- `mask` is honored only from user settings, managed settings, or `--settings`.
  It is IGNORED in a repo's `.claude/settings.json`. That is deliberate.
- `deny` beats `mask` if the same name appears in both.
- AWS: mask access key ID and secret TOGETHER (SigV4 signs request contents; the
  proxy re-signs). Masking the secret alone produces requests signed with the
  placeholder that fail at AWS.

## R4 - Egress allowlist only, filesystem isolation off

```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": { "disabled": true },
    "network": { "allowedDomains": ["github.com", "*.npmjs.org"] }
  }
}
```

WARNING: with filesystem isolation off and commands auto-allowed, a sandboxed
command can write shell startup files, executables on PATH, or
`~/.claude/settings.json` and widen its own access on the next run. Use only for
workloads trusted not to escalate themselves.

## R5 - Strict mode (no escape hatch)

```json
{
  "sandbox": {
    "enabled": true,
    "allowUnsandboxedCommands": false,
    "autoAllowBashIfSandboxed": false
  }
}
```

`allowUnsandboxedCommands: false` makes `dangerouslyDisableSandbox` completely
ignored. Everything runs sandboxed or is listed in `excludedCommands`.

Also available: `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` strips provider credentials
from ALL subprocesses regardless of sandboxing.

---

## H1 - PreToolUse deny hook (the deterministic wall)

Input arrives on stdin as JSON: `tool_name`, `tool_input`, `cwd`,
`permission_mode`, `session_id`, `tool_use_id`.

Output contract - exit 0 and print:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "why"
  }
}
```

`permissionDecision` accepts `deny` (Claude cannot override), `allow`, or
`escalate` (prompt the user). Exit code 2 blocks unconditionally regardless of
JSON, with the reason on stderr. Any other exit code is a non-blocking error and
the action proceeds.

Guard that blocks reads of the credential store:

```bash
#!/bin/bash
# .claude/hooks/block-secret-reads.sh
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // .tool_input.file_path // ""')

# Replace the first two patterns with the names of your own key and token files
if echo "$CMD" | grep -qE 'your-key-file\.json|your-oauth-token\.json|\.ssh/|\.aws/credentials'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Credential store access blocked by secure-this hook. Use sandbox credential masking instead."
    }
  }'
fi
exit 0
```

Wiring:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Read|Grep",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-secret-reads.sh" }
        ]
      }
    ]
  }
}
```

## H2 - Escalate irreversible actions to a human (G4)

Same shape, but `"permissionDecision": "escalate"` matched against send /
publish / push / delete / payment commands. Escalate rather than deny when the
action is legitimate but must not be autonomous.

## H3 - PostToolUse audit log (G6)

Append `session_id`, `tool_name`, and a truncated input to a log OUTSIDE the
agent's write scope. An audit trail the agent can rewrite is not an audit trail.

## H4 - Memory write gate (G7)

Match writes to `MEMORY.md`, `~/.claude/skills/**`, and any persistent store.
Escalate if the session has touched untrusted content. Memory poisoning is the
only attack that survives the session that caused it.
