# Stages 5 and 6 - Looking at outputs, then counting

The method is Hamel Husain and Shreya Shankar's error analysis. The numbers here are theirs, not
estimates.

## The four steps

1. **Gather traces** - the full record of one run end to end. Cold start: *"Start with 100 diverse
   traces and annotate at least the first 30 yourself."*
2. **Open coding** - read and journal what is wrong, in your own words. **Note only the FIRST
   failure** in each trace, because *"upstream errors can cause downstream issues"* and counting
   the cascade twice distorts the taxonomy. About 30 seconds per trace.
3. **Axial coding** - group the notes into a failure taxonomy and **count each category**.
   *"Axial coding is the most important step."* A model may help here. Never in step 2.
4. **Stop at theoretical saturation** - when new reviews stop revealing new failure modes.

**The count decides what gets fixed**, not the last thing anyone noticed.

## Every review has three parts

Doubt-checking is not enough on its own. Opening what looks wrong catches obvious mistakes, but misses
silent ones (things that look fine but are wrong) and anything quietly dropped, and it gives no hit rate.

1. **Doubt-check:** the expert opens what looks wrong. Keep doing this.
2. **Random sample:** the tool picks 20-30 items at random, doubted or not. The expert never picks them.
   The seed is fixed per run and recorded, so the sample can be reproduced.
3. **Drop pile:** a random handful of what the pipeline threw away, from every drop reason, to catch
   good things lost. (Skip only if the step drops nothing.)

Label each item right or wrong, plus a half-sentence note on the first thing wrong. Count the notes by
type (Stage 6) and fix the most common type first.

**Measured, then spot-checked.** Once a judge or step has 30-50 labels, report its catch rate (of the
truly bad items, how many it caught) and its pass rate (of the truly good items, how many it passed),
separately. When both look good, drop to a regular (e.g. monthly) spot-check of about 10 random items, plus doubt-checks.

## How often, and how much

| When | How much |
|---|---|
| Cold start | 100 diverse traces, first 30 by the expert |
| After any significant change | 30 minutes over 20-50 outputs |
| Steady state | 10-20 traces weekly, focusing on outliers |
| Each re-analysis cycle | 100+ fresh traces |

## Who does it

**One person: the benevolent dictator, and it must be the domain expert.** *"Do not outsource
this to developers... the domain expert is the domain expert, not the developer."* A single expert
eliminates annotation conflicts and the paralysis of too many cooks.

If more than one person labels: they label **independently first**, then hold an alignment
session, and agreement is measured with **Cohen's Kappa**, not raw agreement.

If the true expert is unavailable and someone else labels, **say so out loud** - the labels are
then one step removed from the taste that actually matters, and that belongs in the record.

## Criteria drift is expected, not a mistake

Shankar et al., arXiv 2404.12272: people need criteria to grade, but grading is what defines the
criteria. The standard will move somewhere around output 15.

**So earlier labels must be editable, not just appended.** A tool that only appends will bake in
the pre-drift standard and quietly corrupt the taxonomy.

## What the labelling tool must do

Hamel's list. Use it to judge whether an existing tool is good enough before building one:

- **Render outputs in their real form.** *"If you're evaluating generated emails, render them to
  look like emails."* A script judged inside a spreadsheet cell means mentally reconstructing it.
- **All context in one place.** *"Don't make users hunt through different systems."*
- **One-click binary**, not a scale. Correct / incorrect beats a lengthy form.
- **A free-text box beside the button.** Those notes become the taxonomy later. This is the
  load-bearing field.
- **Hotkeys**, so the session never touches the mouse.
- **A progress counter** - "trace 45 of 100" - so the session has an end.
- **Editable earlier labels** (criteria drift).

Bad tool: a generic trace list, multi-point scales, no free text, context spread across systems.

**Try what already exists first.** Langfuse's annotation queue takes a label and a comment and
costs nothing. Build a custom matrix only when the queue is demonstrably too slow. If one is
built, the reference shape is promptfoo's web viewer: one row per input, one column per version,
filters for All / Failures / Passes / **Different** / Highlights, per-cell pass or fail, comment
box, mark-for-review, CSV export.

## Collecting examples when no single skill does the whole job

Twenty skills each needing three approved examples is sixty labelling sessions - the boredom
problem rebuilt with extra steps. Most intermediate artifacts are not judgeable in isolation
anyway: nobody can say whether a skeleton assignment is "right".

**So: label the end of the chain once, and attribute backwards.**

1. Label the final outputs: good or bad, plus half a sentence, first failure only
2. The trace shows which step introduced the fault
3. The example files into THAT skill's `good-examples.md`, with the end output attached
4. The failure becomes a new case in `evals/`

**Exceptions:** wherever a human already looks at an intermediate as part of the normal workflow,
label it in place.

## Stage 6 output

A ranked list of failure types by count. That list is the build backlog. Fix the top two. Add both
as benchmark cases. Then stage 7: ship it, fix it, or stop it.
