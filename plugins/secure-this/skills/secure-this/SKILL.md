---
name: secure-this
description: Security audit and hardening for any skill or workflow before it goes live. Maps it as a data flow diagram, descends nine layers to find threats and ascends them to verify enforcement, then writes the sandbox config and hooks that contain it. Refreshes its own threat catalogue when stale, and is allowed to return UNKNOWN. ALWAYS trigger when the user says "secure this", "/secure-this", "audit this skill", "is this safe", "harden this workflow", "security review", "can this leak my keys", or when a skill-building workflow reaches its final checklist for a new skill.
version: 2.4
status: draft
---

## Name & Trigger
**Name:** secure-this

**Trigger:**
- "secure this", "/secure-this <target>", "audit this skill", "harden this", "is this workflow safe", "security review", "what could go wrong with this agent", "can this leak my keys"
- **Optional auto-gate:** if you use a skill-building workflow, have it call this before marking any new skill complete.

## The Goal
Reduce one skill or workflow to a known set of accepted risks and name what is still
unknown, delivering kernel-, proxy-, or hook-enforced controls with the config staged.

The goal is NOT "make this secure." Nobody can promise that. It is a bounded, named risk
position plus an honest list of what was not checked.

## Connectors

- **Bash (read/inspect)** - read the target's SKILL.md, scripts, settings, MCP config
  - How: `cat`, `grep`, `find`, `jq` over the skill folder and `~/.claude/settings.json`
  - If it fails: check the path. Never audit from memory - read it.
  - Known issues: skills live in TWO stores (`~/.claude/skills` and the app plugin store).

- **Write (staged only)** - emit into `<target>/.security/`
  - If it fails: fix the path. NEVER write `~/.claude/settings.json` directly.

- **WebFetch + WebSearch (freshness pass only)** - refresh the catalogue when stale (Step 0)
  - If it fails: proceed on the stale catalogue but SAY SO and mark affected findings UNKNOWN.

RULE: if a connector fails, debug it. Never switch methods.

**Secrets:** read credential store PATHS only. Never print a key value, never copy
your key file, never put a real credential in a report, config, or example.

## The Process

0. **Load context, check catalogue freshness.**
   Read `last_verified` in `references/02_control-catalogue.md` and `03_anthropic-data.md`.
   Over 30 days old: fetch current Claude Code settings/sandboxing/hooks docs, ask "what
   containment primitives exist now that are not listed here", search for new attack
   classes, update and restamp. Never use a stale catalogue silently.
   - Reference: `02`, `03`, `knowledge-base/lessons-learned.md`, `good-examples.md`
   - HITL: no | Output: one line on catalogue age

1. **Scope and read the target.** One system. Read its SKILL.md, every script it calls,
   its connectors, and any settings or hooks in force. Never audit from a description.
   - HITL: no | Output: one plain paragraph of what it actually does

1b. **Ask before modelling. Never model on assumptions.**
   If the target does not exist yet, there is nothing to read, so ASK. Batch the questions,
   never drip them. Cover at minimum:
   - **What reaches the model** - text only, or images and files too?
   - **What it writes, and whether a human moves it** - does the workflow write to the
     destination, or does a person carry the output there by hand?
   - **Tenancy** - one client or subject per run, or many in one context?
   - **Where it runs and who operates it** - whose machine, whose credentials, watched or not
   - **Where the data is stored** - each store, who else can read it, and does the workflow
     write back or only read
   - **The transit** - what actually moves data between systems, and what credentials it holds
   Then RE-ASK whenever an answer contradicts the map. An answer that changes the shape is
   worth more than a whole layer of analysis.
   - HITL: **yes - wait for answers before Step 2**
   - Output: a "decisions locked" table of what is settled and what is still open

2. **Map it as a data flow diagram.** Five symbols: external entity, process, data store,
   data flow, trust boundary. Every flow gets a verb. Stores do not act. Boundaries last,
   drawn wherever the level of trust changes.
   Then the four-column inventory:

   | Ingests | Holds (data + creds) | Reaches (egress) | Feeds (what consumes its output) |

   Then the table that produces the sharpest findings, **who can actually write to each
   source**. Trust is set by everyone who CAN write to a source, never by whoever usually
   does. A note "typed by a trusted employee" is really "writable by every user of the tool
   it lives in, anyone who takes over one of those accounts, and the vendor."
   - Reference: `01_threat-model.md`
   - HITL: no | Output: the DFD, the inventory, and the write-access table

3. **DESCEND the nine layers.** Discovery. Authority flows down, so you meet each threat
   where it is introduced. **Every layer gets a line, even if the line is "nothing here,
   because X." Silence is not allowed.**
   - Reference: `09_nine-layer-sweep.md`, `10_os-hardening.md` for L4, L5 and L7
   - HITL: no | Output: findings per layer, L0 through L8

4. **Models as threat actors.** On the DFD, replace every model with a threat actor
   sitting in the infrastructure. What could that actor reach? Anything it could reach and
   you would want protected is a probable vulnerability, not a hypothetical.
   - HITL: no | Output: reachability list per model

5. **Source-sink matrix.** Enumerate every SOURCE (anything whose data ends up in a
   context window) and every SINK (anything consuming model output). Then: can an attacker
   reach a source and thereby change a sink they do not already control? Each yes is a
   finding.
   - HITL: no | Output: the matrix, with attacker-reachable paths marked

6. **ASCEND the nine layers.** Verification, L8 back to L0. The question changes to **what
   enforces the control I assigned, and can it be persuaded?** Record a mechanism for every
   control: kernel, proxy, deterministic code, model judgment, or human review. The last
   two are persuadable and must be labelled so.
   - Reference: `02_control-catalogue.md`
   - HITL: no | Output: mechanism per control, plus any control voided because a lower
     layer it depends on does not exist

7. **Build TWO models, not a graded set of postures.** The user decides; the skill does
   not pre-pick for them.

   **Model A - Maximum security.** Convenience deliberately set aside. What does this
   workflow look like if security is the only priority? Build it honestly, including the
   parts that are annoying to use.

   **Model B - Balanced.** Security and convenience both maintained. Where A and B differ,
   state exactly what convenience bought and exactly what it cost.

   Both models are broken out across ALL FIVE layers: environment, harness, model, content,
   output. A layer needing nothing gets a line saying so. A model empty at environment but
   full at model layer is REJECTED, not presented.

   **Every control in both models carries its cost.** A control with no cost stated is not
   a real proposal, because the cost is the reason people ignore security advice.

   | Field | Means |
   |---|---|
   | **Build** | One-time effort to implement. Hours or days |
   | **Run** | Time added per execution. Seconds, minutes, or none |
   | **Friction** | What a human has to do differently. Extra logins, extra clicks, extra approvals, a step they did not have before |
   | **Money** | Recurring cost. Licence tiers, hosting, per-seat fees |

   Then a one-line summary per model: what you give up, and what you get.
   - Reference: `02`, `06_model-selection.md`
   - HITL: no | Output: two complete models, layered, every control costed

7b. **Name the models.** The agent-loop model and any screening model, with reasons.
   Never inherited, never implicit.
   - Reference: `06_model-selection.md`
   - HITL: no | Output: two named models + the re-audit trigger

8. **Run the gates, then grade.** Worst thing true, never averaged.
   - HITL: no | Output: gate table, grade, confidence, leverage flag

9. **Stage the controls, in the target's own language.** Not every target is Claude Code.

   | Target | What "staged config" means |
   |---|---|
   | A Claude Code skill | `proposed-settings.json` and `proposed-hooks/*.sh`, diffed against the live `~/.claude/settings.json`, **plus the OS-level commands from `10_os-hardening.md`** |
   | An n8n or other platform workflow | The platform's own settings, named exactly: retention, redaction, RBAC tier, node placement, credential scoping, approval statuses |
   | A SaaS-to-SaaS integration | Per-service settings named per service: OAuth scopes, service accounts, share lists, roles, form field types |

   Whatever the target, each item is a **specific setting with its current and proposed
   value**, not advice. "Set execution retention to 30 days" is staged. "Consider retention
   policies" is not.
   - Reference: `04_config-recipes.md`
   - HITL: **yes - show the diff and wait. Never merge or ask anyone to change a live
     setting without an explicit yes.**

10. **Produce BOTH deliverables, then merge on approval.**
    - **The document** at `<target>/.security/threat-model.md`
    - **The visual artifact (optional)**: the workflow drawn as a flowchart (any diagram
      tool, or a single HTML page), with a trust marker on each node and, per step, the
      reads, writes, credentials, threat, control and cost. Where the two models differ in
      shape, show both so the difference is visible rather than described.
    Filed together under `<target>/.security/` (or wherever you keep diagrams).
    Internal by default; publish only when asked.

10b. **Merge on approval, write the report.** `<target>/.security/hardening-report.md`:
    inventory, DFD, layer findings, gates, grade, chosen posture, incident response,
    and what was left undone.
    - Reference: `05_incident-response.md`
    - HITL: yes (the approval from step 9)

11. **Completeness pass.** What did I NOT check? Which findings rest on assumption rather
    than reading? What would change this verdict? Anything unverified is UNKNOWN, never PASS.
    - Reference: `07_coverage-map.md`
    - HITL: no | Output: unknowns, accepted risks, re-check triggers, and a verdict of
      CONTAINED / GAPS FOUND / UNKNOWN

## Rules
- Environment layer first, always. A model-layer or prompt instruction is never the primary
  control for anything a gate flagged. Prose is not enforcement.
- **Guardrails are not security boundaries.** They are the WAF of AI: heuristics that lower
  the odds, never a first-order control. Every guardrail can and will be bypassed.
- **Trust is computed at prompt time, not at initialisation.** A model can only be trusted
  as much as the least trusted input in its context window.
- **A model exposed to untrusted data must never read from or write to sensitive resources.**
  If it can, that is the finding, and no amount of screening fixes it.
- A classifier over tool output is a **detector, not a sanitiser**. It can flag and refuse.
  It cannot make dirty text safe. Passing untrusted text through a second model to clean it
  produces multi-order prompt injection, where the cleansing model is now compromised.
- Every control names its enforcement mechanism: kernel, proxy, deterministic code, model,
  or human. If it cannot name one, it is a recommendation and does not count.
- Never propose leaving a credential readable "because the workflow needs it." Use `mask`
  with scoped `injectHosts`.
- Never call egress closed while an allowlisted domain accepts uploads or sharing.
- Never treat a newer model as a control. Robustness is not monotonic across versions.
- Never justify with "models are good at this now." Quote the figure from `03`.
- Never widen an allowlist or disable a gate to make a failing run pass during an audit.
- Never output PASS for something not read and verified. UNKNOWN is valid and often correct.
- Every posture addresses all five layers every run. Never leave a layer silent.
- Pitch explanations at the level of `08_systems-foundations.md` and reuse its vocabulary.
- Every open decision carries a recommendation with its reason. Never leave one blank -
  an open item with no steer is work handed back, not analysis.
- Report what was left unfixed. An audit that only lists wins is a marketing document.
- **Always present two models: maximum security, and balanced.** Never a single recommendation.
  The tradeoff is the user's decision to make, and they cannot make it if only one option is shown.
- **Every control states its cost: build, run, friction, money.** A control with no cost
  attached is not a proposal. Cost is the reason security advice gets ignored, so it is part
  of the finding, not an afterthought.
- **Convenience is a legitimate reason to accept risk**, provided the risk is named and the
  acceptance is written down with an owner. Never present convenience as a mistake.

## Progressive Updates
Whenever the user says a clear thing not to do anymore, add it to Rules above.
Do not ask - update and confirm. Triggers: "never do X", "stop doing X", "don't X",
"I don't want X".

## Quality Gate

**Layer 1 - Hard gates. Any FAIL blocks the verdict. UNKNOWN stays UNKNOWN.**

- [ ] **G1 Secrets out of reach** - no credential file or env var readable at runtime, or masked with scoped `injectHosts`. **Never PASS on Claude Code config alone.** Check the file's permissions (`600`?), what created it (umask), whether it is in a cloud-synced directory, and whether it could be in the Keychain instead. See `10_os-hardening.md`.
- [ ] **G2 Least-trusted-input** - the model's authority does not exceed the least trusted thing in its context. Not all three of [A] untrusted input, [B] sensitive data, [C] state change or egress in one unsupervised session.
- [ ] **G3 Egress bounded** - every outbound path allowlisted, or nothing worth exfiltrating.
- [ ] **G4 Irreversible actions gated** - nothing sends, publishes, pays, pushes, shares, or deletes without a human or a hook.
- [ ] **G5 Dependencies pinned** - MCP servers and external skills pinned, tool descriptions hashed.
- [ ] **G6 Observable** - actions logged where the agent cannot rewrite them.
- [ ] **G7 Memory writes reviewed** - nothing reaches MEMORY.md, a skills folder, or a persistent store unreviewed after touching untrusted content. The only attack that survives its own session.
- [ ] **G8 Sub-agent boundary** - a compromised parent cannot set a child's prompt, tools, or trust level. Pass structured data, not prose.
- [ ] **G9 IO synchronisation** - what the human is shown is identical to what is in context and to what actually executes. Guards against **operator evasion**: the model presenting one action for approval and calling another. A gate that only displays honestly is not enough; the presented value and the executed value must be bound.
- [ ] **G10 Unattended surface** - headless or scheduled runs (cron, LaunchAgent, systemd timer) have no supervision by definition, so containment must be structural.
- [ ] **G11 Output handling** - output reaching anything that renders, executes, or parses it is escaped at the sink.
- [ ] **G12 Bounded consumption** - caps on loops, retries, spend, and generation.
- [ ] **G15 Access lifecycle** - when someone leaves, changes role, or a build finishes, what does this workflow still trust? Name every account, integration and token that can reach it, and who owns removing them. Fail: write the list and put a name against each entry. **Includes the builder's own access**, which is the one everybody skips because they are the person doing the audit.
- [ ] **G14 Host baseline** - FileVault on, SIP enabled, credential files `600`, nothing secret in a cloud-synced path, and the terminal the agent runs in does not hold Full Disk Access. A control at any higher layer is worth what this one is. See `10_os-hardening.md`.
- [ ] **G13 Capability shifting** - does the available toolset narrow when untrusted content enters context, or is it static for the session? Static is the default and is a finding wherever [A] and [B] coexist.

**Layer 2 - Grading. Worst thing true, never averaged.**

| Grade | Condition |
|---|---|
| **A** Contained | Fully compromise the model and it reaches nothing worth taking. Environment-enforced |
| **B** Bounded | No structural gaps. Remaining risks named and accepted |
| **C** Exposed | A real structural gap, held back by supervision or small blast radius |
| **D** Critical | G1 and G2 both failing |
| **F** Critical and unwatched | D plus G10 failing |
| **U** Unverified | Under 60% of the 15 gates verified by reading |

Always ships with: the named failed gates, `Confidence = (gates verified / 15) x 100`, and
the leverage flag. Under 60% confidence the grade is U regardless.

**Leverage flag.** Grade answers "how bad." It does NOT answer "what first." Raise
**HIGH LEVERAGE** when the workflow can write anything that steers other agents: skill
files, MEMORY.md, settings.json, hooks, MCP config, another agent's prompt, or a shared
queue. Fixed before any lower-graded workflow, including F.

**Grouping.** Workflows sharing failed gates are ONE finding with one fix, not N rows.

## Examples

Populated from live test runs - never invented. See `knowledge-base/good-examples.md`.

## Failure Modes
- Never declare a workflow secure because the model refused an injection in testing. One refusal is not a rate; the published figure is roughly 1% at 100 adaptive tries, with safeguards on.
- Never write to `~/.claude/settings.json` without showing the diff. A wrong `denyRead` locks the user out mid-session.
- Never treat directory listing as a security audit. Anthropic reviews connectors against listing criteria and explicitly does not security-audit MCP servers.
- Never audit from a description. Risk lives in the scripts and connectors.
- Never recommend screening as the fix for G1, G2, or G13. Those are structural.
- Never skip the egress inventory because it "doesn't send anything." Rendered image URLs, DNS lookups, sharing, and writes to synced folders are all channels.
- Never produce a grade without the completeness pass.

## Testing & Iterating

When something goes wrong, stop and tell the user: what went wrong, why, and the fix.

| What happened | What to do |
|---|---|
| Didn't follow the process | Update the Process section here |
| Bad outputs | Add to `/references/` |
| Wrong behaviour | Add a Rule here |
| Tool used wrong | Update `references/mcp-instructions.md` |

Then ask "Want me to apply the fix now?" If yes: change, bump version, log CHANGELOG.
Same failure 2+ times: update `knowledge-base/lessons-learned.md`.

## Before Every Run
Read `references/mcp-instructions.md`, `knowledge-base/lessons-learned.md`,
`knowledge-base/good-examples.md`.

## After Every Run
- Approved: log to `good-examples.md` with the grade
- Rejected: the user writes the correct answer, log as CORRECTION
- Tool/process failure: log to `failure-log.md` with root cause and fix
- 2+ same failures: update `lessons-learned.md` and this SKILL.md, bump version, log CHANGELOG
