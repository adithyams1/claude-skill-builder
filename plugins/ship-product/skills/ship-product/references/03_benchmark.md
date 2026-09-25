# Stage 2 - The benchmark

This is the stage that lets you walk away. Without it you are the verification loop, and after
the tenth approval you are clicking rather than reviewing.

Anthropic states the problem exactly: *"Claude stops when the work looks done. Without a check it
can run, 'looks done' is the only signal available, and you become the verification loop: every
mistake waits for you to notice it."*

## Write the cases BEFORE the build

**Eval-driven development:** *"build evals to define planned capabilities before agents can
fulfill them, then iterate until the agent performs well."* The AI Fluency course says the same
thing from the other side: *"Write acceptance tests that define done before a single line of code
exists"*, and *"Tests are the most precise form of description."*

Writing the cases first also tests the spec: **if you cannot write the check, the requirement is
not concrete enough to build against yet.** That is the cheapest possible failure.

**What is NOT written in advance:** the failure taxonomy. You cannot guess which failures a chain
will produce. Success criteria go in upfront; failure types are discovered at stage 5 and added
back here.

## Two levels, and only one of them ever moves

**Level 1 - the top question.** Set once, at the start, on the FINAL output, in the
words of whoever approves it: *"would <that person> use this as-is?"*. Client example: *"would
the client film this?"*. It never changes, however many features move underneath it. It is what
the whole pipeline is for, and every run is judged against it.

**Level 2 - a small check per step**, on what that step hands to the next one. Cheap, code
wherever possible. Its only job is to stop bad material reaching the next step. It is not a
verdict on the output.

**A step check passing says nothing about the top question.** Twenty green steps and an
unusable final output is the exact failure this structure exists to catch, and it is not hypothetical
(Client example): twenty skills each passed their own gate and the finished month was never judged by
anyone.

This is also why the build order matters: each step eats the previous step's output, so a bad
early step leaves every later step passing its own check while working on bad material. Build one
piece, run it on real data, read the output, then start the next.

## Size

**20-50 cases**, *"drawn from real failures"*. Not hundreds. The intake's items 3, 4 and 6 are the
first cases, free.

## What one case holds

- The task, with its inputs
- The success criteria
- The grader
- After a run: the transcript and the outcome

Interchange format, when a human is labelling, is AlignEval's four columns: `id`, `input`,
`output`, `label`.

## Graders, in this order

**1. Code graders first.** Assertions, string matches, state checks, file existence. Free,
instant, objective, and they run on every build forever. Most of what matters is already this
shape:

- the expected number of outputs exists
- every quoted line matches its source word for word
- every reference points at something real
- every proof file is on disk
- no forbidden characters, no empty fields

Where a runner already names a proof file per step, every one of those is an assertion for free.

**2. LLM judges only where code cannot capture it.** Binary, one isolated question per dimension,
never 1 to 10. A judge is not trusted until measured against a person on 30-50 labelled examples,
reporting catch-rate and pass-rate **separately** - raw agreement is a trap, because a judge that
always says pass scores 90% when failures are 10% of cases.

**3. Grade what was produced, not the path taken.** *"Grade what the agent produced, not the path
it took"* - grading the route is brittle, because there is more than one valid route.

Target: **at least half the graders are code.** If fewer, decompose the judge questions further -
"4 of 5 expected facts present" as five binary checks beats "accuracy 7/10".

## How hard the check gates the stop

Least to most hands-off. Pick the weakest one that actually holds:

1. **In the prompt** - ask for the check and have it iterate in the same message. Works today, on
   any task, with no setup.
2. **A `/goal` condition** - re-checked after every turn until it resolves.
3. **A Stop hook** - a script that blocks the turn from ending until the check passes. The
   deterministic version, and what makes an unattended run finish correctly. A rule in a prompt is
   a suggestion; a rule in the tool is a restriction.
4. **A fresh subagent** that tries to refute the result, because the model that did the work
   should not be the one grading it. Tell it to flag only gaps that affect correctness, or it will
   invent findings and drive over-engineering.

## Evidence, not assertion

Have the run **show** the evidence: the check output, the command and what it returned, the file
it wrote. Reviewing evidence is faster than re-running the verification, and it works for runs
nobody watched.

## Re-testing after a fix (Stage 6.5, code checks only for now)

A fix that is never re-run against what was already approved can quietly break it. So after every
fix, re-run the code-check cases and compare with the labels already on file:

- **Frozen inputs.** Re-run the fixed step on the saved upstream output, never a fresh fetch, so
  the score moves because of the fix and not because the data changed. It is also cheaper.
- **3 runs per case, all must pass.** Model output varies; one lucky run is not a fix.
- **Three numbers, not one score:** fixed (failed before, passes now), still broken, newly broken
  (passed before, fails now). Newly broken is the real regression and the one that blocks ship it.
  A regression suite should sit at nearly 100%; new failures being worked on are tracked apart.
- **Holdout.** Keep ~20% of labelled cases unseen while fixing; check them once at the end, or the
  fixes overfit the cases you stared at.
- **Decision steps** (keep/drop, pick, assign) compare straight to the label. **Generated text**
  only re-tests what code can check (lengths, word-for-word matches, locked words, counts,
  forbidden characters). Judge-graded and pairwise taste re-tests are in `TODO.md`.
- The suite only knows failures already found. Stage 5 keeps a small fresh human sample every cycle.

## Where it lands

`evals/<product>.jsonl` next to the product, beside SPEC.md. It is a living file: every confirmed
failure from stage 6 gets appended, so a failure that has been seen once can never come back
unnoticed.
