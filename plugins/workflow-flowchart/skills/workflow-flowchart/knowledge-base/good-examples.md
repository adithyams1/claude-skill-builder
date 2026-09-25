# Good Examples - workflow-flowchart

Read at the start of every run to calibrate what "good" looks like.
When the skill gets something wrong, the user writes the correct answer here as a
CORRECTION entry - this is the training data.

## Entry format

```
## <date> - <what was drawn> (<n> flows, <hours or "no hours">)
**Output:** <published URL or local path>
**Why it worked:** bullet points
**Review checks:** Legible yes/no, Honest roles yes/no, Accurate yes/no, Clear yes/no
```

```
## <date> - <what went wrong> <- CORRECTION
**What Claude did:**
**Correct answer:**
**What to do differently:**
```

---

## Example - a content agency's delivery and growth system (2 groups, with hours)

**Why it worked:**
- Groups named in the prospect's own language, not ours: "Delivery - do the current work,
  faster" and "Growth - bring in the clients". They could tell them apart without being
  walked through it.
- Human and gate nodes left visible and honest. A node reading "You film one video - the
  only real work you do" was the most persuasive node in the diagram precisely because it
  admits what is not automated.
- Clickable example chips on nodes where a live build already existed, so claims were
  checkable in the room rather than asserted.
- Hour totals per group let the price conversation attach to something concrete.

---

## Example - an internal outreach pipeline (7 independent flows, no hours)

**Why it worked:**
- Flows were derived from the real dependency graph on disk, not from memory. Never guess
  a pipeline that already exists as code or config.
- One 17-node flow was split into two flows of 7 and 10. Right at the readability ceiling,
  two flows read far better than one.
- Hours omitted entirely because it was not a client quote. The chips and totals hid
  themselves.
- The human nodes carried the argument: "You approve the send - explicit, every time"
  made the drafts-only safety model visible in one glance.

---

## Step 1 HITL gate <- CORRECTION
**What Claude did:** Presented the flow list and asked "Good to draw?" after the user had
already said yes to the whole run.
**Correct answer:** Asking again read as stalling, not as a checkpoint.
**What to do differently:** When the run is already approved, present the flow list as a
statement of what is being built and proceed in the same turn. Only stop when the flows
are genuinely ambiguous or the diagram is going to a client.

---

## Invented Power Ups <- CORRECTION
**What Claude did:** Dashed every node in a not-yet-built flow as a Power Up.
**Correct answer:** Power Up means optional or later work the user named, not "unbuilt".
Dashing a whole plan makes it read as a list of extras rather than the build.
**What to do differently:** Leave nodes solid. Put build status in the goal sentence.
