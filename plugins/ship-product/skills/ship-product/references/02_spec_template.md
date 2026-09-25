# Stage 1 - The spec

## What a spec is for - three uses, nothing else

1. **A fresh session builds from it.** The transcript is gone by the time it matters; the file
   survives. This is the whole reason it exists.
2. **Non-goals live in it.** It is the only place that can say "we do not make ten times what
   gets used" (Client example: 36 blueprints for a client who posts 4 reels).
3. **It holds the why**, so decisions stop being re-litigated or silently reversed.

If a spec is not doing one of those three, it is paperwork. Do not write it.

## How many specs

**One spec per piece of work.** Not per feature, and not one for the whole build.

Client example: about **four**: the monthly workflow, the team screens, the
runner, and the output viewer.

- **Stop buttons, form pre-fill, a new column on a screen** - these are work *inside* a spec, not
  specs of their own.
- **If a change can be described in one sentence, skip the spec and do it.** A spec for a
  one-sentence change is the paperwork failure, and it teaches everyone to route around specs.
- **Never one spec per skill.** (Client example: four specs, about twenty skills.)

## Spec vs SKILL.md

**The spec is what and why. The skill is how.** Not our invention: spec-kit's template says
*"No implementation details"*; Kiro splits requirements (what) / design (how) / tasks (the build).
**SKILL.md already is the design file.**

| Question | Where it lives |
|---|---|
| What are we making, for whom, why | SPEC.md |
| How much, how often | SPEC.md |
| What we deliberately do NOT do | SPEC.md |
| What would prove it works | SPEC.md states it, `evals/` runs it |
| Which tool we chose, what we rejected | SPEC.md Decisions |
| The step-by-step process | SKILL.md |
| How to call the MCP, what to do when it fails | `references/mcp-instructions.md` |
| What good looks like | `knowledge-base/good-examples.md` |
| "Never do X" | SKILL.md Rules |

## How the questions work

All requirement questions in **one message**, never dripped. Then **at most 5 clarifiers**, one at
a time, and only where two readings would produce two different products. Keep each turn to
200-300 words so the person answering does not tune out on a wall of text.

## Does it change later? Two halves, two rules

- **The top** (job, deliverables, volume, non-goals) changes **only on an approved scope change**.
  Otherwise the spec is just the chat again, moving under the build.
- **The Decisions section is append-only**, written in the turn a decision is made. This is an
  architecture decision record (Nygard, 2011): never edited, never deleted, superseded by a later
  dated line while the old one stays visible.

The case that proves it: Apify to Bright Data. That call was made, the reason lived only in a
chat, and today it exists nowhere. In six months someone sees Apify is cheaper on the pricing page
and re-runs the whole experiment, or silently switches back and loses play counts again.

## The nine sections

```markdown
# SPEC - <product>

*Written <date>. Top half changes only on an approved scope change. Decisions append freely.*

## 1. The job
One sentence, no jargon. What this is and who it is for.

**The outcome being bought:** what changes for the person receiving it, in their words. Not the
deliverable. Client example: "the client knows what is working right now" and "the client has
reels ready to film" are different products, and they are not built the same way.

## 2. What it produces
The exact deliverables, and how many per run or per period. Numbers, not adjectives.

## 3. Inputs
Each one named, and where it comes from. A named file, a named form, a named person.

## 4. Success criteria
Measurable, and stated WITHOUT naming a tool. Client example: "Every hook matches its source reel word for word"
is a criterion. "Bright Data returns play counts" is an implementation detail.

## 5. Non-goals
What this deliberately does not do. At least one line, always. This section is the defence
against scope growth and it is never empty.

## 6. Assumptions
The default chosen wherever the owner did not say. Each one marked as an assumption so it can be
corrected rather than discovered later.

## 7. Open questions
What is still needed, who owes it, and the assumption running in the meantime. Never a guess
silently adopted.

## 8. Budget
Hours, model cost, and the dumbest version that would still work. Stated before the build starts.

## 9. Decisions
Append-only, dated, one line each: what was chosen, what was rejected, why, and whether it is
reversible. Client example:

    2026-08-14  Scraper B, not scraper A. Scraper A drops the play count, and the run cost
                ~$X per client-month against B's ~$Y. Reversible: swap inside the scraping skill.

## Verdict
Written at stage 7. One of: ship it / fix it / stop it, with the date.
```

## The chain

The spec holds the **chain** - what goes in at the start, what comes out at the end, each step as
one line saying what it hands to the next. It does not hold the step detail; each skill holds its
own contract.

Where a runner already lists the steps and their proof files, **point at it rather than
duplicating it**. Client example: a runner script like `run.py`, whose step table
is both the workflow map and the source of most code graders for free.

## Where it lands

`SPEC.md` **next to the product**, in the folder that holds the thing it describes. Never a
central default location: a fresh session finds the spec by being in the folder.
