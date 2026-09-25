# Node & Edge Grammar - workflow-flowchart

The render engine in `template.html` is locked. This file is the grammar for the data
you inject into it. Read this before writing any nodes.

## Node

```js
n(id, col, row, role, icon, label, sub, opts)
```

| Arg | Meaning |
|---|---|
| `id` | short unique string within this flow, referenced by edges |
| `col` | 0-based column. Column = stage in the pipeline, left to right |
| `row` | 0-based row. Row = parallel branches at that stage |
| `role` | one of the six below. Drives the colour |
| `icon` | a key from the IC library below. An unknown key renders an EMPTY box, silently |
| `label` | the bold line. Keep under ~28 chars |
| `sub` | the grey line under it. Keep under ~40 chars or it overflows |
| `opts` | `{slot:0}` shows a clickable example chip. `{pu:1}` marks it a Power Up (dashed) - **only when the user has said that step is one**, never inferred from build status |

## The six roles

| Role | Colour | Use for |
|---|---|---|
| `inp` | grey | raw material entering the system: a brief, a recording, a form response |
| `ai` | teal | a step a machine does unattended |
| `human` | amber | a step a person still has to do. Be honest here |
| `tool` | blue | a stored asset or third-party app: a database, a scheduler, Notion, Drive |
| `gate` | purple | a review or approval checkpoint |
| `out` | green | something that ships: a post, an email, a report |

The colour split IS the argument the diagram makes. Never mark a human step as `ai` to
make the system look more automated.

## Edge

```js
e(from, to, label, powerup)
```

`from` and `to` must both exist in that flow's node list or the edge silently vanishes.
`label` is optional, use it only where the handoff is not self-evident.
`powerup` set to 1 renders it dashed.

## Icon keys (IC library)

Using any key not on this list renders a blank node with no error.

```
mic  cam  ig  li  fb  mail  cal  ai  person  gate  doc  db  search
chart  form  frame  asana  notion  drive  code  clock  img  send
bank  tag  sked
```

Rough mapping: `mic` audio/voice · `cam` filming · `ig`/`li`/`fb` platforms · `mail` email ·
`cal` scheduling · `ai` a model doing work · `person` a human · `gate` approval ·
`doc` a written document · `db` a store · `search` research · `chart` analytics ·
`form` a questionnaire · `frame` a review/proofing tool · `asana` a task manager · `notion` Notion ·
`drive` Drive · `code` a script · `clock` a wait · `img` an image · `send` publishing ·
`bank` money · `tag` labelling · `sked` a social scheduler

## Layout rules

- Column 0 is always inputs. The last column is always outputs.
- No two nodes in one flow may share the same `(col, row)`. They will overlap.
- Rows are centred visually, so keep parallel branches symmetric around the main line
  where you can: main path on row 1, branches on rows 0 and 2.
- Above ~18 nodes a flow stops being readable. Split it into two flows.

## Flow object

```js
{id, num, name, phase, hb, pu, goal, nodes:[], edges:[]}
```

`hb` is build hours. **Omit it entirely when there are no hours** and every hour chip and
total hides itself. Never invent a number to fill the slot.
`pu` is the Power Up label, e.g. `"time TBD"`. **Omit it unless the user named the Power
Ups in conversation.** A whole flow dashed because it is not built yet is a label nobody
asked for, and it makes the plan read as optional extras. Say "not built yet" in `goal`.
`goal` is one plain sentence a non-technical reader understands.

## Feedback loops

A system that learns from the human's edits needs the loop drawn, or the flywheel is
invisible. But **never draw a loop with `e()`.**

The engine leaves a node on its RIGHT and arrives on its LEFT. Any right-to-left return
edge therefore folds back over its own boxes, and no placement fixes it - the curve's
control points are derived from the two endpoints, so the last third always crosses the
target. Both placements have now been tried and both were rejected in the render.

Draw it by hand instead:

- Add one empty row **above** the chain as a return lane. Every existing node shifts down
  one row; the lane stays clear across its whole width.
- Put the learner in that lane, directly above the drafter it feeds.
- Route both hops as orthogonal paths in the added `<script>` block: up out of the
  reviewer, left along the empty lane into the learner's right edge, then straight down
  into the drafter's top edge. Rounded corner on the turn, arrowhead polygon at each head,
  class `epath` / `ehead` - or `epath pu` / `ehead pu` only if the nodes it joins are
  themselves Power Ups, so the loop matches whatever the rest of the flow is doing.
- Read the geometry off the DOM (`.node` style left/top plus `offsetWidth`), not from the
  node array - the engine owns the layout.
- Label the top run only ("your edits"). The arrow direction says the rest, and two labels
  on a tight cycle collide.
- Re-add on a `MutationObserver` watching `#edges` for `childList`. `draw()` replaces the
  SVG's innerHTML on every redraw and would wipe the loop. Guard the callback by checking
  for your own class first, or it re-enters forever.

Verify it: no `.elabel` rect may intersect a `.node` rect. Nothing in the validator checks
this - it is a visual fault, so it only shows in the render.
