# The Nine-Layer Sweep
A composite threat modeling method for AI agent systems.
Drafted 2026-08-19. Used by secure-this at Step 3 (descent) and Step 6 (ascent).

---

## What this is

One traversal that puts every mainstream threat modeling methodology at the layer it
actually belongs to, so none of them has to pretend to be the whole framework.

Two passes, opposite directions:

- **DESCEND (L0 -> L8): discovery.** "What can go wrong here?"
- **ASCEND (L8 -> L0): verification.** "What enforces the control I assigned, and can it
  be persuaded?"

You descend because **authority flows down**. L0 decides what the system is allowed to be;
by L7 you are looking at the specific secret that carries that authority to a third party.
Going down means you meet each threat at the layer where it is introduced rather than
discovering it later as a symptom.

You ascend because **enforcement strength runs the opposite way**. The low layers hold
hardest (kernel, proxy); the high layers are judgment (model, human). Coming up from the
bottom you can see exactly where you stopped having walls and started having intentions.

---

## THE DESCENT

### L0 - Purpose and authority
**Ask:** What is this for? Whose authority does it carry? What is the blast radius if it
is fully compromised? Would I know?

**Prompts from:** the four CISO questions; PASTA in a light form (business impact first).

**Look for:** authority that exceeds the job. A workflow that only needs to read a
calendar holding a token that can also delete it. Ambiguous accountability, where a
delegated human identity runs unsupervised so no one owns the outcome.

**Controls:** narrow the identity (a single-purpose service account), or put a human
accountable at the keyboard. Avoid the middle.

**Also ask, every time:** if the operator's own account were taken over, what does this
workflow hand the attacker? And when that person leaves or changes role, what does it still
trust? Offboarding is not adjacent to a threat model, it IS one for anything with shared
access. See G15.

**Exit condition:** you can state the blast radius as a concrete worst case in one
sentence. "An attacker reads the CRM and mails it out as me." Not "data could be exposed."

---

### L1 - People and data
**Ask:** Whose personal data is in here? Should we be holding it at all? Can individuals
be singled out, linked across sources, or identified from what we keep?

**Prompts from:** LINDDUN. Linkability, Identifiability, Non-repudiation, Detectability,
Disclosure of information, Unawareness, Non-compliance.

**Look for:** data retained past its purpose. Personal data in logs, drafts, and caches
rather than the store you think holds it. Records assembled across sources into a profile
richer than any single source.

**Controls:** delete it, aggregate it, pseudonymise it, shorten retention. This is the
layer where **eliminate** beats **mitigate** more often than anywhere else.

**Exit condition:** every category of personal data is named, with a reason for holding it
and a retention answer. "We do not hold personal data" is a valid exit; assuming it is not.

---

### L2 - The agent
**Ask:** What untrusted text reaches the model's context? What are its goals, and what can
rewrite them? What does it write that will instruct it later?

**Prompts from:** MAESTRO L1 (foundation models) and L2 (data operations); prompt injection;
the lethal trifecta.

**Look for:** untrusted content arriving anywhere other than a tool result. Goal hijack via
retrieved content. Memory and context poisoning, which is the only attack that survives the
session that caused it. RAG and vector store poisoning where one exists.

**Controls:** untrusted content in tool results only, JSON-encoded, source-labelled. A
screening classifier over tool output. Context minimisation. A review gate on anything the
agent writes to a persistent instruction store.

**Exit condition:** you can list every untrusted input by name, and say for each one how it
enters context.

---

### L3 - The harness
**Ask:** What tools exist, who decided the plan, how do sub-agents get their instructions,
and where exactly does the human approve?

**Prompts from:** MAESTRO L3 (agent frameworks) and L7 (ecosystem); OWASP ASI07 (inter-agent
communication), ASI08 (cascading failures), ASI09 (human-agent trust exploitation).

**Look for:** tool allowlists that include a general interpreter, which defeats the
allowlist. Sub-agent prompts written by a parent that reads untrusted content. Queues and
job files that become instruction channels. Approval screens that show the agent's summary
rather than the artifact, which makes the gate theatre.

**Controls:** plan-then-execute so the plan is fixed before untrusted content is read. Tool
filtering. Dual LLM or map-reduce isolation. Sub-agent toolsets defined independently of
the parent. Route reviewers to the source artifact.

**Exit condition:** for every human approval in the workflow, you can say what the human
actually sees and where it came from.

---

### L4 - The process
**Ask:** What identity does this run as? What is in its environment? What can it open? Is
anything restricting it beyond ordinary user permissions?

**Prompts from:** STRIDE on processes. Processes are the only element all six letters apply
to, so this is the densest layer.

**Look for:** the agent running as you with your full permissions, which is the normal case
and the reason everything else matters. Child processes inheriting identity and environment.
Secrets sitting in the environment of a process that reads untrusted content. Working
directory mistaken for a restriction, which it is not.

**Controls:** OS sandbox (Seatbelt, bubblewrap, container, VM). Filesystem scoping with
deny rules. Capability removal. Strict mode with no unsandboxed escape hatch.
**Also ask at the host, not just the harness:** is this an admin account, is there a separate
standard user for agent work, and does the terminal it runs in hold Full Disk Access? A
sandbox rule working around an app that already has everything is not a control.
See `10_os-hardening.md`.

**Exit condition:** you can name the enforcement mechanism that stops this process reading
any given file. If the answer is "it wouldn't," that is a finding, not an exit.

---

### L5 - The host
**Ask:** What is on disk, who else can reach it, and what stops one workload consuming
everything?

**Prompts from:** STRIDE on data stores (tampering, repudiation, disclosure, denial of
service, but never elevation, since a store holds no privilege); MAESTRO L4 (deployment and
infrastructure).

**Look for:** credential files. Outputs landing in synced folders, which is exfiltration
with no network call. Logs containing secrets. No cap on loops, retries, or API spend.
Containers sharing a kernel with weak boundaries.

**Controls:** file permissions and deny rules. Keep outputs out of synced directories.
Resource limits. Never log a secret.

**Exit condition:** every data store on the diagram has an owner and a stated sensitivity.

---

### L6 - The network
**Ask:** Where can this connect, what decides, and what can the decider actually see?

**Prompts from:** STRIDE on data flows (tampering, disclosure, denial of service).

**Look for:** unbounded egress. Allowlisted domains that accept uploads or content, which
remain exfiltration channels. SSRF to private ranges and cloud metadata. DNS as a covert
channel. Rendered image URLs, which are network requests wearing a disguise.

**Controls:** an egress proxy with a domain allowlist, which is the single strongest
control against prompt injection. Block private IP ranges. Remember the proxy decides on
destination only; it cannot see whether the payload is a lead name or a key.

**Exit condition:** you have the complete list of destinations this workflow can reach, and
for each one you know whether it accepts content.

---

### L7 - The credential
**Ask:** What proves this system's identity to the outside, where does that proof live, and
who holds it at the moment of use?

**Prompts from:** the TLS-versus-API-key distinction. TLS proves the server; the credential
proves the client. Only the second needs hiding from the process.

**Look for:** credentials readable by a process that also reads untrusted content. Tokens
passed through to upstream APIs unchanged. Plaintext tokens in config files. Credentials in
a file rather than handed in, which removes the interception point that makes masking
possible.

**Controls:** credential masking with scoped inject-hosts, so the process holds a sentinel
and the proxy substitutes the real value only for approved destinations. OS keychain
storage. Scoped credential translation at a proxy. Mint narrower tokens rather than
forwarding.

**Exit condition:** for every credential, you can say which process holds the real value at
the moment of use, and why that process is safe to hold it.

---

### L8 - Observability
**Ask:** If any of the above happened, would there be a record, and could the thing that did
it alter that record?

**Prompts from:** MAESTRO L5 (evaluation and observability).

**Look for:** no audit trail. A trail the agent can rewrite. Agent actions indistinguishable
from human actions in the log. Monitoring that the agent itself reports into.

**Controls:** append-only logging outside the agent's write scope. Telemetry to a system you
control. Distinguish agent from human in every record.

**Exit condition:** you can name the file or system where evidence would appear, and say why
the agent cannot edit it.

---

## THE ASCENT

Same nine layers, L8 back up to L0. The question is no longer "what can go wrong."
It is: **what enforces the control I assigned here, and can it be persuaded?**

At each layer, for every control written during the descent, record one of:

| Mechanism | Persuadable |
|---|---|
| Kernel / hardware | No |
| Proxy / network | No |
| Deterministic code (hooks, validation) | No |
| Model judgment | **Yes** |
| Human review | **Yes, and it fatigues** |

Three rules for the ascent:

1. **A control with no named mechanism is not a control.** It is a recommendation. Label
   it as one and move on. Do not count it.
2. **A control that depends on a lower layer that does not exist is void.** This is what the
   ascent is for. A tool allowlist at L3 means nothing if L4 has no sandbox and the
   allowlist includes a shell.
3. **Where the mechanism is persuadable, say so out loud.** Model judgment and human review
   are legitimate controls. They are not walls, and a plan that rests its weight on them at
   a low layer is mis-built.

The ascent ends at L0 with the question it started with: given everything that actually
holds, what is the blast radius now?

The difference between that answer and the L0 descent answer is the value of the work.

---

## Coverage rules

Three properties make coverage checkable rather than assumed.

**1. Every methodology has a home.** LINDDUN at L1. MAESTRO across L2, L3, L5 (as L8 here)
and L4-as-infrastructure. STRIDE at L4, L5, L6. Attack trees applied after the descent to
whatever ranked highest. None of them is "the framework."

**2. No layer may be silent.** A layer with nothing to report writes one line saying so and
why: "L1: no personal data, this workflow reads only public video metadata." Silence and
thoroughness are indistinguishable otherwise.

**3. Discovery and verification are separate passes in opposite directions.** The commonest
failure in threat modeling is writing a mitigation next to a threat and never checking the
mitigation is real. Two passes makes that hard to skip by accident.

---

## When to use the depth tools

The sweep is breadth. After the descent, take the top one to three findings and build an
**attack tree** for each: attacker goal at the root, branches for the ways to reach it,
leaves for concrete attacks.

The tree earns its place by showing which single control cuts the most branches. A flat
list of findings hides that.

---

## What this does not cover

State it in every report.

- **Known categories only.** Every catalogue at every layer was written by someone who had
  already seen the attack.
- **No live probing.** This is architectural analysis. It does not plant a test injection
  and watch. Findings are reasoned, not reproduced.
- **Not a red team.** MITRE ATLAS technique-level testing is a different exercise.
- **A snapshot.** It expires when a dependency updates, a connector is added, the model
  changes, or a new untrusted input appears. Name the re-check trigger explicitly.

Never write "secure" or "fully covered." Write which layers were examined, what each found,
and what was accepted.
