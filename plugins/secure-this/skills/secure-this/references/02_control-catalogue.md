---
last_verified: 2026-08-19
refresh_if_older_than: 30 days
refresh_method: fetch current Claude Code settings / sandboxing / hooks docs and ask
  "what containment primitives exist now that are not listed here?" Then one search
  for new attack classes since the stamp date. Restamp on completion.
---

# Control Catalogue - the volatile half

Controls are grouped by the four Frontier Model Forum layers. Cross-lab
consensus: no single layer suffices; combine them.

**Order of application is not negotiable: environment first, then harness, then
model, then content.** Environment controls hold when the model is fully
compromised. Nothing else does.

---

## Layer 1 - ENVIRONMENT (kernel / hypervisor / proxy enforced)

The defining property: these hold even if the model is 100% convinced it should
do the bad thing. The kernel is not persuadable.

| Control | Mechanism | Notes |
|---|---|---|
| Filesystem scoping | kernel | `sandbox.filesystem.denyRead` / `allowRead` / `allowWrite`. Exact deny holds inside a wider allow, so a broad allow cannot silently re-expose a secret |
| Bash sandbox | kernel (Seatbelt on macOS, bubblewrap on Linux/WSL2) | Applies to the command AND every child process. Not available on native Windows |
| Network egress allowlist | proxy | `sandbox.network.allowedDomains`. Named by Anthropic's CISO as the single strongest control against prompt injection |
| Credential deny | kernel | `sandbox.credentials.files` / `envVars` with `"mode": "deny"`. Breaks tools that need the value |
| Credential MASK | proxy | `"mode": "mask"` + `injectHosts`. Agent sees a sentinel; the proxy swaps in the real value only on outbound requests to listed hosts. Agent authenticates without ever holding the credential. Requires `network.tlsTerminate`. THE control for the "but it needs the key" case |
| Subprocess env scrub | runtime | `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` strips provider credentials from all subprocesses regardless of sandboxing |
| Strict sandbox | policy | `allowUnsandboxedCommands: false` disables the `dangerouslyDisableSandbox` escape hatch entirely |
| Capability removal | absence | Do not give the agent a delete tool. Not "gate delete" - do not provide it. A gate approved 93% of the time is not a control |
| VM / dev container | hypervisor | Strongest isolation. Cost: it also blinds endpoint detection to what happens inside the guest |
| Scoped credential translation | proxy | Sandbox holds a narrow credential; a proxy translates it to the real token outside. The real token never sits where an injected agent can read it |

## Layer 2 - HARNESS (orchestration: planning, memory, tool execution)

This is the layer you actually control when writing a skill.

| Control | Mechanism | Notes |
|---|---|---|
| PreToolUse deny hook | hook (deterministic) | Returns `permissionDecision: "deny"`; Claude CANNOT override. This is how a control stops being a suggestion |
| PostToolUse audit hook | hook | Append-only log the agent does not write to |
| ConfigChange hook | hook | Blocks or alerts on settings changes mid-session |
| Plan-then-execute | architecture | Fix the plan BEFORE untrusted content enters context. Injection can then corrupt parameters but cannot add steps |
| Action-selector | architecture | Model picks from a fixed menu; tool output never feeds back into a decision. Most secure, least flexible |
| Dual LLM / CaMeL | architecture | Privileged LLM plans and never sees raw untrusted data; quarantined LLM reads the data and has no tools. Values carry provenance metadata (capabilities); a taint-tracking interpreter enforces policy before any tool call. Makes injection structurally unable to affect control flow, the way parameterised queries did for SQL |
| Map-reduce isolation | architecture | Fan untrusted items out to isolated unprivileged workers, reduce only sanitised results |
| Context minimisation | architecture | Strip untrusted content from context once it has served its purpose |
| Tool filtering | architecture | Restrict which tools are available for a given task. In AgentDojo this simple control dropped ASR to 7.5%, beating cleverer prompt defenses |
| Sub-agent constraint | architecture | Child's toolset defined independently of the parent; pass structured data, not free prose (ASI07/ASI08) |
| Human gate on ground truth | human | The reviewer sees the source artifact, not the agent's summary of it (ASI09) |
| **Dynamic capability shifting** | code | THE control from Brauchler. The toolset available to the model narrows as untrusted data enters its context. Developer prompt with no external data: all tools. User prompt: privileged tools removed. Untrusted third-party content read: sensitive tools removed. Trust recomputed at prompt time, not inherited at init |
| **Trust binding by pinning** | code | The backend attaches the user's own auth token to every tool call the model triggers, so the model can never exceed the user. NEVER put that token in the context window - context leaks |
| **Proxying** | code | Route tool calls through the user's browser, which converts intent into an API call. Existing app authn/authz then applies unchanged, with no new trust path |
| **Trust tagging** | code | Tag data by origin at write time, so capability shifting can fire correctly on read. The fix for laundered stores: a row derived from a scrape stays marked as such |
| **IO synchronisation** | code | Bind the value presented to a human to the value actually executed. Guards **operator evasion**: the model showing "purchase coat 33" for approval and calling the tool with something else. A human gate that only displays honestly is not enough |
| **Trust splitting** | architecture | Route requests to two zones: a quarantined model with dirty data and no privileged tools, and a trusted model with tools and no dirty data |
| **Trust isolation** | architecture | When low-trust output would enter a high-trust context, substitute a placeholder. The user sees the real text; the privileged model never does |
| **Data type gating** | structural | Only typed values cross between trust zones: numbers, IDs, GUIDs, a selection from a fixed list, non-string code objects. Never arbitrary text. Hard to hide an injection in an integer |

## Layer 3 - MODEL (probabilistic, never primary)

| Control | Mechanism | Notes |
|---|---|---|
| Instruction hierarchy | training | system > user > tool_result. A learned habit |
| Injection-resistance training | training | RL against simulated injections so the model learns "that came from a page" |
| Action classifier | probabilistic | Reviews proposed actions pre-execution |
| System-prompt policy | prose | Cheap, imperfect, still worth stating |

## Layer 4 - CONTENT (screening before context)

| Control | Mechanism | Notes |
|---|---|---|
| Untrusted content in tool_result ONLY | structural | The model is specifically trained to be skeptical there. Putting a fetched page in a user turn throws that training away |
| JSON-encode untrusted strings | structural | Unambiguous delimiters so an attacker cannot close a tag and break out. Closest thing to a prepared statement available |
| Label source and nature | structural | "body of an inbound email from an unknown sender" |
| Never put your own instructions in a tool result | structural | They get discounted along with everything else there. Put them in the following user turn |
| Cheap-classifier screen | probabilistic | Small fast model over tool output, structured boolean verdict, before the main model sees it. **A DETECTOR, NOT A SANITISER.** It may flag and refuse. It cannot make dirty text safe. Passing untrusted text through a second model to clean it produces multi-order prompt injection: the cleansing model is now the compromised one (Brauchler, Black Hat 2025) |
| Isolated fetch context | structural | Read the hostile thing where its output cannot become instructions |

---

## Supply chain and time-of-use

- Treat every skill, plugin, and MCP server as executable code from its author
- **Tool poisoning**: malicious instructions in a tool's `description` field
- **Rug pull**: correct at review time, malicious after a silent update. Approval
  was a snapshot; the tool is a live feed. Hash tool definitions at startup and on
  every connection, diff against a known-good baseline, any change triggers re-review
- **Confused deputy**: server acts with its own broad privileges on behalf of a
  user who lacks them. With a static client ID plus dynamic registration, an
  attacker can reuse an existing consent cookie and get an auth code with no
  consent screen shown
- **Token passthrough**: never forward a client token upstream; mint a narrower one
- **SSRF**: block egress to private IP ranges and cloud metadata endpoints
- **Cross-server contamination**: no isolation between MCP servers in one context;
  server A's descriptions can influence how the model calls server B's tools
- OAuth 2.1 with mandatory PKCE; validate token audience
- OS-native credential storage; never plaintext tokens in MCP config files
- Anthropic reviews connectors against listing criteria but does NOT
  security-audit MCP servers. Directory presence is not an audit.

## Rejected as primary controls (use only as depth)

- Prompt hardening alone: Google measured multi-turn failure moving only from
  75.00% to 46.88%
- Classifier stacks alone: Meta's full LlamaFirewall stack reached 1.75% ASR.
  Better, not zero, and adaptive attackers evade probabilistic filters
- "Use a newer model": Opus 4.8 is less robust than 4.7 on several agentic
  injection surfaces


## Threat modeling techniques (Brauchler, Black Hat 2025)

- **Trust flow tracking** - tag data with the entity that created it and follow it
  downstream. Pollution moves downstream: once hostile input is anywhere in the pipeline,
  no amount of reformatting, JSON encoding, or guardrail passes removes it. Track where it
  lands, not just where it entered.
- **Source-sink matrices** - a SOURCE is anything whose data eventually reaches a context
  window; a SINK is anything consuming model output. List both exhaustively, then ask: can
  an attacker reach a source and thereby change a sink they do not already control? Each
  yes is a finding.
- **Models as threat actors** - on the data flow diagram, replace every model with a threat
  actor standing in your infrastructure. Whatever that actor could reach is what an
  injection reaches. If it touches something you would protect, that is a probable
  vulnerability, not a hypothetical one.

## Framing that keeps the layers honest

**Guardrails are the WAF of AI.** In the real history of the web, the WAF arrived after the
vulnerabilities and was never the boundary; behind it lived XSS, SQLi, SSRF, RCE. AI was
built backwards: defense in depth first, security fundamentals second. A guardrail lowers
the odds. It is never a first-order control, and every one of them can be bypassed given
enough effort.

**Trust in traditional software is inherited at object creation and stable for its
lifetime. A model has no such property.** It is an agent of its inputs, so its trust must be
recomputed from what is in the context window at prompt time. This single difference is why
the classic permission model does not transfer.
