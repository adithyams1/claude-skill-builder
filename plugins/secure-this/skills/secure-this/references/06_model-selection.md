---
last_verified: 2026-08-19
refresh_if_older_than: 30 days
refresh_method: read the system card for any newly released model and record its
  agentic / prompt-injection numbers here. Do NOT assume a newer release is safer.
---

# Model Selection as a Security Decision

## The framing that keeps this honest

Model choice is a **layer 3** control. It is probabilistic, and it is a TIEBREAKER
applied after environment and harness controls are set. If a hardening plan's main
argument is "we use the safer model," it has no hardening plan.

Read that first, then use the rest of this file.

## Two separate decisions

### Decision 1 - the agent-loop model

The model doing the work while exposed to untrusted content. Injection robustness
matters here.

Published figures (see `03_anthropic-data.md` for the full table):

| Model | Agentic injection robustness |
|---|---|
| Claude Opus 4.7 | Gray Swan: ~0.1% ASR single attempt, ~5-6% after 100 adaptive attempts |
| Claude Sonnet 4.6 | Browser scenario ASR 1.29%, down from 49.36% on Sonnet 4.5 |
| Claude Opus 4.8 | Robustness sits BETWEEN Opus 4.7 and Sonnet 4.6. Less robust than 4.7 in several agentic contexts; ahead of competitive frontier models; safeguards close the gap in practice. Lower false-positive rate (fewer benign items misread as injections) |
| Claude Sonnet 4.5 | Browser scenario ASR 49.36%. Do not use on an untrusted-content surface |

**The non-negotiable rule: robustness is NOT monotonic across versions.** Opus 4.8
is newer than 4.7 and less robust on several agentic surfaces. Never reason from
version number. Read the system card for the specific release.

### Decision 2 - the screening model

The cheap fast model that classifies tool output before it reaches the main context
(layer 4). Different job, different criteria: latency and cost dominate, and it
needs structured outputs so the verdict is parseable.

Default: **Claude Haiku 4.5**, constrained with a JSON schema to a boolean verdict.

## Choosing

| Situation | Agent loop | Screening |
|---|---|---|
| Unattended + reads untrusted content | Highest published robustness for that surface. Also the case where layers 1 and 2 must already be complete, because supervision does not exist | Haiku 4.5, mandatory |
| Attended, reads untrusted content | Robustness matters, but a human is in the path. Capability can win | Haiku 4.5, recommended |
| No untrusted content at all | Pick on capability. Injection robustness is not the binding constraint | Not needed |
| Browser or computer use | Check the browser-specific number, not the general one. The spread between versions is enormous (49.36% to 1.29% across one minor version) | Haiku 4.5, mandatory |

## The false-positive tradeoff

A model that over-flags benign content as injection breaks the workflow. AgentDojo's
core methodological point is that utility and security must be measured JOINTLY - a
defense that destroys utility is not a defense. Opus 4.8 explicitly traded some
robustness for fewer false positives and less disruption to legitimate tasks. Whether
that trade is right depends on whether the workflow is unattended (favour robustness)
or supervised (favour utility).

## Re-audit trigger

**A model change invalidates the audit.** Record in every report which model the audit
assumed. When that model changes, re-run this skill. Treat a model upgrade as a
config change to a security control, because that is what it is.
