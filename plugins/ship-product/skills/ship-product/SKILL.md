---
name: ship-product
description: The loop we build by, for any workflow or product: intake, spec, benchmark, build, check, look, lock, re-test, decide. Generates the eight-slot intake ask, writes SPEC.md from the nine-section template, produces a 20-50 case benchmark before any code exists, and holds the gates. Trigger: "/ship-product", "let's build X", "write the spec", "how do we build this".
version: 1.5
status: draft
---

# Ship Product

## Name & Trigger
**Name:** ship-product
**Trigger:** `/ship-product`. Also fires whenever you describe building something new
("let's build X", "I want a workflow that...", "can we make a tool for..."), before any code is
written. Can be waved off in one word; never argues about it twice.

## The Goal
Every build starts from what the user actually said, states what it will NOT do, carries a check
the machine can run without you watching, and ends with you saying one of three words: ship
it, fix it, or stop it.

## Connectors
None. This skill reads and writes local files only.

- **Local files (read/write)** - the spec, the intake, the benchmark, all next to the product
  - How to call it: Read/Write/Bash against the product's own folder
  - If it fails: the folder moved. Find it. Never write a spec to a default location
- **`code-scripts/check_spec.py`** - the gate: are all nine sections filled
  - How to call it: `python3 <this skill's folder>/code-scripts/check_spec.py <path to SPEC.md>`
  - If it fails: read its output; it names the empty section
  - Known issues: none yet

RULE: If a connector fails, debug and fix that connector. Never switch to an alternative method.

SECRETS: none. If that ever changes, read from `~/.claude/keys.json`, never inline.

## Two loops
The spec loop (stages 1-4) runs once per piece of work; the eval loop (stages 5-7) runs after every
full pipeline run. Never confuse them: `references/00_two_loops.md`.

## The Process

### Stage 0 - Intake (user voice)

1. **Generate the eight-slot ask** for whoever owns the requirements, paste-ready in a fenced
   block, with every slot made concrete for this product.
   - Reference: `references/01_intake.md`
   - HITL: yes - you sends it and brings back the answers
   - Output: the ask in chat, then `INTAKE.md` next to the product

### Stage 1 - Spec (requirement, then technical spec)

2. **Ask ALL requirement questions in one message.** Then at most 5 clarifiers, one at a time,
   and only where two readings would produce two different products. 200-300 words per turn.
   - Reference: `references/02_spec_template.md`
   - HITL: yes - one batch of answers, then one approval
   - Output: `SPEC.md` next to the product, nine sections

3. **Run the gate.** `check_spec.py <path>`. An empty non-goals or open-questions section fails.
   - Reference: none
   - HITL: no
   - Output: pass, or the named empty section

### Stage 2 - Benchmark (tests)

4. **Set the top question once, at the start, on the FINAL output**, in the words of whoever
   owns the result: "would <the person who approves it> use this as-is?" (Client example:
   "would the client film this?"). It never changes for that product. Then **write 20-50 cases
   BEFORE any code exists**, including a
   small check per step on what that step hands to the next. Code graders first; a model judge
   only where code cannot capture it, and binary. Grade what was produced, never the path taken.
   A step check passing says nothing about the top question.
   - Reference: `references/03_benchmark.md`
   - HITL: yes - you approves the criteria once
   - Output: `evals/<product>.jsonl` next to the product

### Stage 3 - Build (AI instruction)

5. **One piece at a time.** Build a piece, run it on real data, have a person read the output,
   fix what is wrong, and only then start the next piece. Never build everything and test at the
   end: in a pipeline each step eats the previous step's output, so a bad early step makes every
   later step look fine while it works on bad material.
   Fresh session, built from SPEC.md alone, never from the transcript. New skills go through
   skill-builder. Plan mode before anything touching more than one file. An unclear spec stops
   and asks. The run iterates against the benchmark until it passes.
   - Reference: `SPEC.md`
   - HITL: yes, once per piece - a person reads that piece's real output before the next starts
   - Output: the piece, a passing benchmark, and output a person has actually looked at

### Stage 4 - Check

6. **Show evidence:** what ran, what it produced, what it cost. A fresh reviewer reads the diff.
   - Reference: none
   - HITL: yes - you read the evidence
   - Output: pass or fail, with evidence

### Stage 5 - Look (error analysis)

7. **Label real outputs, in three parts:** doubt-check, a random sample the tool picks (20-30), and a
   random handful of the drop pile. Binary plus half a sentence on the first failure. Method and sizes: reference.
   - Reference: `references/04_error_analysis.md`
   - HITL: yes - the domain expert labels, not the developer
   - Output: `labels/<run>.jsonl`

### Stage 6 - Lock

8. **Group the notes into failure types and COUNT them.** The count decides what gets fixed, not
   the last thing anyone noticed. Every confirmed failure becomes a new benchmark case.
   - Reference: `references/04_error_analysis.md`
   - HITL: yes - you approve the top 2 fixes
   - Output: new cases in `evals/`

### Stage 6.5 - Re-test (regression, code checks only)

9. **After every fix, re-run the code-check cases on frozen inputs** (the saved upstream output,
   never a fresh fetch), 3 runs per case; a case passes only if all 3 pass. Report three numbers:
   fixed, still broken, newly broken. Fix and re-test until nothing is newly broken and the
   targeted failures pass. Keep ~20% of labelled cases as a holdout, never looked at while fixing,
   and check it once at the end. Judge and taste cases wait (`TODO.md`).
   - Reference: `references/03_benchmark.md`
   - HITL: no, until the report
   - Output: `evals/runs/<date>.json` with the three numbers

### Stage 7 - Decide

10. **Ask for one of three words: ship it, fix it, or stop it.** Never ask for ship it while
    anything is newly broken. Write it into SPEC.md with today's date.
    - Reference: none
    - HITL: yes
    - Output: a dated verdict line in SPEC.md

## Rules
- **Never start building without a SPEC.md.** If you say build and no spec exists, write the
  spec first, or get an explicit "skip it" for a job under an hour.
- **Never write a spec with an empty non-goals section.** That section is the entire defence
  against building far more than the owner will ever use (Client example: 36 blueprints
  for a client who posts 4 reels).
- **Never guess a missing input.** It becomes an open question with the assumption written beside
  it, in section 7.
- **The Decisions section is append-only.** Never edit or delete a decision; a later dated line
  supersedes it and the old one stays visible.
- **Never change the top of a spec without approval.** Job, deliverables, volume and non-goals
  move only on an approved scope change. Decisions append freely.
- **Never score 1 to 10.** Binary for objective, pairwise for subjective, 0-5 only if a gradient
  is genuinely needed.
- **Never put implementation detail in the spec.** How belongs in SKILL.md and
  `references/mcp-instructions.md`. The spec answers what and why.
- **Never size a build from the deliverable. Size it from the outcome.** What does the client
  receive today, and what do they do with it in the first hour? Client example: the agency
  hands clients outliers, and we built scripts, shot lists and storyboards on top of an outcome
  nobody had asked to change.
- **Anything you did not ask for is a defect, not a bonus.** A good idea mid-build goes to
  the backlog.
- **Never let the model grade its own work.** A check that returns pass or fail, or a fresh
  reviewer, or it is not done.
- **Every build states its size before it starts.** Default: the dumbest thing that works.
- **One spec per piece of work.** Not per feature, not one for everything. A change describable in
  one sentence does not get a spec at all.
- **Never ask "it is good if ___".** Nobody can answer it. Ask what they check before it
  goes out, and what gets it sent back.

## Progressive Updates
Whenever you say a clear thing not to do anymore, automatically add it to the Rules section
above and confirm it was added. Do not ask.

Pattern triggers: "never do X", "stop doing X", "don't X", "I don't want X".

## Quality Gate
Data/judgment skill - hard gates. All must pass or the output is rejected:

- [ ] SPEC.md has all nine sections, none empty - fail: `check_spec.py` names it, fill it
- [ ] Non-goals names at least one thing we are deliberately not doing - fail: ask for it
- [ ] Every open question carries the assumption running meanwhile - fail: write the assumption
- [ ] Success criteria are stated without naming a tool - fail: rewrite them
- [ ] The benchmark exists before the build starts, with at least 20 cases - fail: stop, write it
- [ ] At least half the graders are code, not model judges - fail: decompose further
- [ ] Every tool decision is one dated line saying what was rejected and why - fail: write it
- [ ] The loop ends with ship it, fix it or stop it - fail: ask for the word

A model judge is never trusted until measured against a person: 30 to 50 labelled examples, with
catch-rate and pass-rate reported separately. Raw agreement is a trap.

## Examples
Populated from live test runs - never invented. See `knowledge-base/good-examples.md`.

## Failure Modes
- **Writing the spec from the chat instead of from the client.** The Description Chain starts at
  user voice. One client's first build started at technical spec, which is why none of it matched how they
  actually work.
- **Asking questions nobody can answer.** "What does good mean" comes back empty; "what three
  things do you check" comes back in thirty seconds. One client's 11-question client survey died of this.
- **Asking the client to do our job.** Nothing in an intake ask that is research we should do
  ourselves (Client example: trends, competitor research).
- **Collecting examples per skill.** Twenty skills times three examples is sixty labelling
  sessions. Label the end output once and attribute failures backwards to the step that caused them.
- **Letting the developer label instead of the domain expert.** The expert is the expert.
- **Treating the spec as frozen.** The Decisions section is meant to grow during the build.
- **Skipping stage 7.** A thing that is never shipped and never stopped stays in "fix it" forever.

## Testing & Iterating - What To Do When Something Goes Wrong
Stop and tell you: what went wrong (specific), why (root cause), and the fix:

| What happened | What to do |
|---|---|
| Didn't follow the process | Update the Process section in this SKILL.md |
| Bad outputs | Add more info or examples to `/references/` |
| Does something wrong (behaviour) | Add a Rule to the Rules section |
| Uses a tool wrong | Update `references/mcp-instructions.md` |

Then ask "Want me to apply the fix now?". On yes: make the change, bump the version, log
CHANGELOG.md. Same failure twice: update `knowledge-base/lessons-learned.md`.

## Before Every Run
Read `knowledge-base/lessons-learned.md` and `knowledge-base/good-examples.md`.

## After Every Run
- Spec or benchmark approved: log to `knowledge-base/good-examples.md`
- Rejected: you writes the correct version, log as a CORRECTION entry
- Something cost time to diagnose: `knowledge-base/failure-log.md`
- Pattern twice: `lessons-learned.md` + this SKILL.md + version bump + CHANGELOG.md
