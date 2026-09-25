# Threat Model - the stable half

This file does NOT rot. It is security thinking, not product detail.
The volatile parts live in 02_control-catalogue.md and 03_anthropic-data.md.

---

## 1. The root cause: no channel separation

A CPU separates the instruction pointer from the data segment. A prepared SQL
statement separates the query from the parameter. An LLM separates nothing.
System prompt, user message, fetched page, tool result, filename - all arrive as
one flat token sequence through the same attention mechanism.

So prompt injection is not a bug awaiting a patch. It is SQL injection with no
parameterised query available, because the escaping would itself be natural
language the attacker can also write.

Consequence, and the axis this whole skill turns on:

> You cannot make the model refuse everything, so make sure it cannot do much
> damage when it obeys.

There IS a learned priority (system > user > tool_result). It is a trained
habit, not a lock. Habits degrade under adversarial pressure. Locks do not.

## 2. The lethal trifecta (Willison, 2025)

Data theft becomes possible when one agent has all three:
1. Access to private data
2. Exposure to untrusted content
3. Ability to communicate externally

Three things people get wrong:
- Exfiltration is broader than it looks: a markdown image tag pointing at an
  attacker URL, a DNS lookup, a git push, a write into a synced folder.
- The legs can be split across a session. Read secrets at step 3, read the
  hostile page at step 7, make a request at step 12. Same breach.
- Allowlisting a domain does not close leg 3 if that domain accepts uploads.

## 2b. Trust is computed at prompt time

Traditional apps inherit trust at object creation and keep it for the object's lifetime.
A model cannot: it is an agent of its inputs, controlled by whatever reaches its context
window, whether that came from the developer, the user, application data, or a tool call.

> **A model can only be trusted as much as the least trusted input it receives.**

Two consequences:

- **Pollution moves downstream.** Once hostile input enters the pipeline, reformatting,
  JSON encoding, guardrails, and watchdog models do not remove it. A second model asked to
  cleanse it becomes the compromised one: **multi-order prompt injection**.
- **A model exposed to untrusted data must never read from or write to sensitive
  resources.** This is the Rule of Two arriving as a runtime rule rather than a design-time
  audit, and it is the single most operational sentence in the field.

**Operator evasion** is the attack on the human gate: the model presents one action for
approval and executes another. Any human-in-the-loop control needs the presented value
bound to the executed value, not merely displayed honestly.

## 3. Rule of Two (Meta) - the operational form

Properties per session:
- [A] processes untrustworthy input
- [B] has access to sensitive systems or private data
- [C] can change state or communicate externally

An unsupervised agent gets AT MOST TWO. If it genuinely needs all three, it does
not operate autonomously - human-in-the-loop approval or another reliable
validation is mandatory.

Worked examples from Meta:
- [AB] Travel assistant: reads the web, holds booking creds, every transaction
  needs human approval. C removed.
- [AC] Research browser: browses anything, fills forms, sandboxed with zero
  access to private data. B removed.
- [BC] Internal coder: touches prod, can push out, ingests only trusted-author
  sources. A removed.

Rule of Two is a SUPPLEMENT to least privilege, not a substitute.

## 4. Delivery vectors - where injected text actually hides

- Invisible text: white-on-white, display:none, 0px font, off-screen absolute
- HTML comments, alt attributes, aria-label, meta tags
- Unicode tag characters and zero-width codepoints (invisible to a human
  reviewer, fully visible to the tokeniser)
- Text baked into an image, reached via OCR or vision
- URL query parameters echoed into the page
- File metadata, EXIF, PDF annotations, spreadsheet cell comments
- MCP tool DESCRIPTIONS - the model reads them every turn, you read them never
- Commit messages, issue bodies, PR descriptions, CI logs
- Filenames themselves
- Skill and plugin markdown - a skill is instructions loaded into context, so
  installing one from a repo is `curl | bash` for your model's instructions

## 5. Agentic amplifiers - why agents are worse than chatbots

An injected chatbot says something wrong. An injected agent DOES something
wrong, then does the next thing.

- Multi-step execution: one poisoned step contaminates every later step in the
  same context window
- Memory persistence: inject once, it lives in MEMORY.md / a skills folder / a
  vector store and re-fires every session. THE ONLY ATTACK THAT SURVIVES THE
  SESSION THAT CAUSED IT. Treat memory writes as the highest-severity sink.
- Delegated authority: the agent runs with the user's OAuth token, keychain,
  and shell
- Sub-agents: an injected parent writes the prompt for a clean child. The child
  has no idea it was born compromised.
- Approval surface capture: if the agent writes the summary the human approves
  from, the human gate is theatre

## 6. OWASP Top 10 for Agentic Applications (2026) - coverage checklist

| ID | Risk |
|---|---|
| ASI01 | Agent Goal Hijack - objectives redirected through content, not code |
| ASI02 | Tool Misuse and Exploitation - tools bent by poisoned metadata or input |
| ASI03 | Identity and Privilege Abuse - over-permissioned agent identities |
| ASI04 | Agentic Supply Chain - compromised frameworks, MCP servers, registries, skills |
| ASI05 | Unexpected Code Execution - natural language becoming code outside the sandbox |
| ASI06 | Memory and Context Poisoning - planted information shaping future behaviour |
| ASI07 | Insecure Inter-Agent Communication - unauthenticated agent-to-agent messages |
| ASI08 | Cascading Failures - one agent's error propagating through workflows that trust it |
| ASI09 | Human-Agent Trust Exploitation - the agent controlling what the human sees before approving |
| ASI10 | Rogue Agents - operating outside policy while looking legitimate, persisting across sessions |

## 7. The four questions (Anthropic CISO framework)

1. What untrusted content does it ingest?
2. What actions can it take, and on whose behalf?
3. What is the blast radius if it is misaligned? (scope x severity)
4. What observability do I have? Can I tell agent actions from human actions?

## 8. Identity spectrum

Use either a narrow single-purpose service account, OR a human's credentials
with that human accountable at the keyboard. AVOID THE MIDDLE - delegated human
identity running unsupervised creates ambiguous accountability, which is how an
incident becomes unresolvable.
