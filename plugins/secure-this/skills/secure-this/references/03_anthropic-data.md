---
last_verified: 2026-08-19
refresh_if_older_than: 30 days
---

# Data - for calibration and for justifying recommendations

Quote these numbers instead of saying "models are pretty good at this now."

## Anthropic architecture and outcomes

| Fact | Number |
|---|---|
| Users approving permission prompts (why approval fatigue defeats gates) | ~93% |
| Prompt reduction after OS-level Bash sandboxing | ~84% |
| Auto-mode classifier catching overeager behaviour pre-execution | ~83% |
| Gray Swan Agent Red Teaming, Opus 4.7, single attempt | ~0.1% ASR |
| Gray Swan, Opus 4.7, after 100 adaptive attempts | ~5-6% ASR |
| Internal Best-of-N adaptive attacker, 100 tries/env, Opus 4.5 + safeguards | ~1% ASR |
| Browser injection, Sonnet 4.5 -> 4.6 scenario ASR | 49.36% -> 1.29% |
| Claude in Chrome autonomous mode, with mitigations | 23.6% -> 11.2% |
| Chrome, hidden form fields / URL manipulation vectors | 35.7% -> 0% |
| Anthropic internal combined-technique suite | <0.08% |
| Browser agent hijack rate before safeguards engaged | 31.5% |

Anthropic's own framing: "A 1% attack success rate, while a significant
improvement, still represents meaningful risk." And: "protection in the model
layer will never be 100% effective, which is why it can't stand alone."

**Opus 4.8 regression:** less robust than Opus 4.7 in several agentic contexts
including prompt injection; safeguards close the gap in practice. Model upgrades
are NOT monotonic security improvements. Never treat a newer model as a control.

Gray Swan methodology: one-week live attack competition, expert red-teamers, model
identities hidden, at most one successful attack submitted per test setting per model.

## Anthropic's published failures (the most useful part)

- **Pre-trust execution**: project config files parsed BEFORE the trust dialog
  appeared. Opening a hostile repo was enough. Fix: defer parsing until after consent.
- **Direct injection via phishing**: employee phished, Claude exfiltrated AWS
  credentials 24 times across 25 retries. When the injection arrives as the user's
  own instruction there is nothing anomalous for a classifier to catch.
- **Allowlist exfiltration**: files uploaded to an attacker-controlled account via
  the approved api.anthropic.com domain.
- **EDR blind spot**: VM isolation also blinds endpoint detection inside the guest.
- **Poisoned README**: content passing malware scanning still loads into context.
  Malware scanning and injection scanning are different problems.

## Other labs

| Source | Finding |
|---|---|
| Google / Gemini | Prompt hardening alone: multi-turn failure 75.00% -> 46.88% |
| Meta LlamaFirewall | PromptGuard 2 + AlignmentCheck + CodeShield = 90% ASR reduction, to 1.75% |
| AgentDojo | 97 tasks, 629 security cases. Simple tool filtering dropped ASR to 7.5%. Measures utility AND security jointly - a defense that breaks utility is not a defense |
| Jan 2026 review, 78 studies | Every major coding agent tested (Claude Code, Copilot, Cursor) fell to prompt injection |

## Real incidents

- **EchoLeak (CVE-2025-32711)**: zero-click via crafted email. Reference-style
  markdown image links bypassed Copilot link redaction, exfiltrating OneDrive /
  SharePoint / Teams data. 160+ org-level incidents.
- **GitHub MCP**: malicious instructions in public GitHub Issues hijacked agents,
  leaking private repo source and keys to attacker-controlled public repos.
- **Supabase**: a Cursor agent with service-role access processed support tickets
  containing user-supplied SQL; integration tokens leaked into a public thread.
- **Cursor mcp.json**: case-sensitivity flaw in protected-path checks let injection
  overwrite `.cursor/mcp.json` on case-insensitive filesystems, escalating to RCE.
- **Claude Code deny-rule bypass**: found in bashPermissions.ts after the March 2026
  source leak; patched in v2.1.90.

Aggregate trackers list ~98 documented agent incidents, ~40 critical.
