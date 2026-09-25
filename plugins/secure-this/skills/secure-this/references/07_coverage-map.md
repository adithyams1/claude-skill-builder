---
last_verified: 2026-08-19
---

# Coverage Map - what this skill covers, and what it does NOT

This file exists because "does it cover everything?" has no honest yes. The honest
answer is a documented scope. Read this before claiming completeness in any report.

## Frameworks mapped

| Framework | Status |
|---|---|
| Lethal trifecta (Willison) | Covered - G2 |
| Agents Rule of Two (Meta) | Covered - G2, [A][B][C] |
| Anthropic containment model + published incidents | Covered - `03_anthropic-data.md` |
| Frontier Model Forum control layers | Covered - the 5 posture layers |
| Design Patterns for Securing LLM Agents (CaMeL et al) | Covered - `02_control-catalogue.md` harness section |
| OWASP Top 10 Agentic Applications 2026 (ASI01-10) | Covered - `01_threat-model.md` |
| OWASP Top 10 for LLM Applications 2025 (LLM01-10) | Partial - see below |
| Google SAIF / SAIF 2.0 agent map | Partial - Rogue Actions and response-rendering folded into G11 |
| MCP attack classes + OWASP MCP cheat sheet | Covered - G5, supply chain section |
| AgentDojo / LlamaFirewall / benchmark data | Covered - `03_anthropic-data.md` |
| Brauchler, *When Guardrails Aren't Enough* (NCC Group, Black Hat USA 2025) | Covered - prompt-time trust and multi-order injection in `01`, eight controls and three threat-modeling techniques in `02` |
| MITRE ATLAS (16 tactics, 84 techniques) | NOT mapped - see below |
| NIST AI RMF / ISO 42001 | NOT mapped - governance, not workflow-level |

## OWASP LLM Top 10 2025, item by item

| ID | Risk | Where |
|---|---|---|
| LLM01 | Prompt Injection | Core of the whole skill. Note the sub-case Brauchler calls **cross-user prompt injection**: poisoning one user's context via content another user authored, which is more specific than OWASP's "indirect" |
| LLM02 | Sensitive Information Disclosure | PARTIAL - G1 covers credential reach, but not normal-operation leakage of personal data into logs, drafts, or outputs. Flag it when the Feeds column touches anything shared |
| LLM03 | Supply Chain | G5 |
| LLM04 | Data and Model Poisoning | OUT OF SCOPE - training-time. Most skill authors train nothing; revisit if you fine-tune |
| LLM05 | Improper Output Handling | G11 (added v1.5) |
| LLM06 | Excessive Agency | G2, G4, capability removal |
| LLM07 | System Prompt Leakage | PARTIAL - SKILL.md files often hold real method IP. Commercial exposure, not just security. Note it, do not gate on it |
| LLM08 | Vector and Embedding Weaknesses | OUT OF SCOPE unless the target uses RAG or a vector store. Revisit if one appears |
| LLM09 | Misinformation | OUT OF SCOPE as a security gate - it is an accuracy problem. Relevant to the evaluator skills, handled by their own rubrics |
| LLM10 | Unbounded Consumption | G12 (added v1.5) |

## Known gaps, stated plainly

1. **MITRE ATLAS is not mapped.** It is a threat-technique catalogue for red teaming
   (16 tactics, 84 techniques, agentic techniques added in v5.4.0, Feb 2026). This skill
   audits architecture, it does not run attack techniques. A real red-team pass is a
   different exercise and this skill is not a substitute for one.
2. **No live probe.** The skill reasons about a workflow; it does not plant a test
   injection and watch what happens. Report findings as architectural, never as tested.
3. **NIST privacy/extraction attacks** (model inversion, membership inference) are not
   covered. Not relevant to a consumer of a hosted model.
4. **Multi-turn drift** across long sessions is not modelled.
5. **Human factors beyond G9 and G15.** Approval fatigue is cited (93% approval rate) but
   not measured per workflow.
6. **Phishing and social engineering are not auditable here** and never will be. This skill
   reads code and config; it cannot stop someone being tricked. What it CAN do, and now
   does at Step 5, is price it: if the operator's account were taken over, what would this
   workflow hand over? That is the only form of the question a workflow audit can answer.
7. **Access lifecycle is covered by G15.** Offboarding is easy to miss: a workflow can
   outlive the person who owned it, its threat model can carry that as an unowned accepted
   risk, and the builder's own access often has no end date.

## The rule this file enforces

Never write "fully covered" or "secure" in a report. Write which frameworks were applied
and which were not. A named scope is honest; a completeness claim is not.
