# Lessons Learned - workflow-flowchart

General rules derived from failure patterns (2+ occurrences). Read at the start of every run.

## Entry format

```
## Rule: <short rule>
**Pattern:** what kept going wrong
**Rule:** what to do instead
**How to verify it:** (optional)
```

---

## Rule: screenshot before you publish, always
**Pattern:** Template extraction left client-specific strings behind in places that looked
structural rather than content, and no amount of re-reading the source caught them.
**Rule:** Serve the file locally, screenshot it, and read the screenshot before publishing.
Re-reading your own code is not verification - the render is.

---

## Rule: a gate that is a checklist is not a gate
**Pattern:** Checks written as tick-boxes got implemented as a throwaway inline script,
useful once, then gone.
**Rule:** Any check that can be expressed as code belongs in `validate.py` and is run as a
command. Keep the manual checklist for what cannot be automated, which here is the render.

---

## Rule: let the system's own shape decide, do not apply a template
**Pattern:** One connected build was rendered as several flows under an invented
"working today / what we build next" split nobody asked for.
**Rule:** Apply the handoff test: if one part's output feeds the next, it is ONE flow.
Separate flows only for pipelines that run independently. Infer, state it, proceed - do
not add a confirmation question for structure the conversation already implies.

---

## Rule: added JS goes in its OWN script block
**Pattern:** Panel controls worked locally and died once published. The template ships one
`<script>` block, so anything appended to it is hostage to every line above it.
**Rule:** Any behaviour added to a generated flowchart goes in a separate `<script>` block
after the template's. Look the elements up, bail if absent, retry once on
`DOMContentLoaded`.
**How to verify it:** copy the file, inject `BOOM.explode();` immediately before the
template's first `</script>`, load it, and confirm the addition still works.

---

## Rule: an overlay inside a pan surface has dead clicks
**Pattern:** A panel's close button did nothing while Escape still worked. The panel lived
inside `#canvas`, whose pan handler calls `setPointerCapture`, retargeting the pointer-up.
**Rule:** Any dialog, panel or overlay is a sibling of `#canvas`, never a child.
**How to verify it:** hit-test with `document.elementFromPoint(cx,cy)`, then click at real
coordinates and assert the state changed. `el.click()` bypasses reachability and gives
false passes.

---

## Rule: the marker contract is the marker AND the line under it
**Pattern:** Four markers are followed by an empty default declaration. Filling the marker
alone declares the identifier twice and the script silently never runs.
**Rule:** Treat every marker as a pair - read the line after it before writing anything.
`validate.py` enforces the duplicate-const half; the comment-syntax half is on you.

---

## Rule: correct a bad reference, never append next to it
**Pattern:** Wrong guidance in `references/` was followed by the next run and reproduced
the exact fault. The skill trusts its references.
**Rule:** When a run proves reference guidance wrong, REPLACE that section and note it in
the CHANGELOG. Never leave the old advice sitting above the new.
