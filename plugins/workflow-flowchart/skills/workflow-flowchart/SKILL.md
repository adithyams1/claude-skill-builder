---
name: workflow-flowchart
version: 1.8
description: >
  Turns any multi-step system discussed in conversation into an interactive pan-zoom
  flowchart page - colour-coded by who does each step (input / AI / human / tool /
  review gate / output), grouped into engines or phases, with optional build hours and
  clickable nodes that open live examples. Every diagram is filed into a permanent
  workflows directory (default ./workflows/) with a browsable index, so past clients
  and prospects can be pulled up any time. Built for showing a prospect how a system
  actually works on a call. ALWAYS trigger when the user says "make a flowchart", "build
  the flow chart", "workflow diagram", "show me the flows", "turn this into a diagram",
  "/workflow-flowchart", or asks to visualise builds/pipelines/steps just defined in
  conversation. Also trigger on "open my workflows", "show me all the workflows",
  "workflows directory" - that is index-only mode, Step 11 alone.
pipeline: meta
status: ready
tools: [Read, Write, Bash, Python, optional Artifact, optional browser preview]
---

## Name & Trigger
Triggers are in the frontmatter description.

**Index-only mode:** "open my workflows", "show me all the workflows", "workflows
directory", "what flowcharts have I built". Run Step 11 only, skip everything else.

## The Goal
One shareable pan-zoom page where a non-technical person can click through each flow in
a system and immediately see how many steps there are, which ones a machine does, which ones
a human still touches, and where the review gates sit - filed into a permanent directory so
it can be pulled up months later.

## Where Things Live

`<skill>` below means this skill's own folder (the folder this SKILL.md sits in).
`<workflows>` means the workflows directory. It defaults to `./workflows/` in the current
working directory. Set the `WORKFLOWS_DIR` environment variable, or pass `--root <dir>` to
`build_index.py`, to keep it somewhere else (for example `~/workflows/`).

## Connectors

- **Read** - loads `<skill>/references/template.html`, the locked render engine
  - How to call it: Read on this skill's `references/template.html`
  - If it fails: check the skill folder path. Never regenerate the engine from scratch
  - Known issues: none

- **Write** - writes the filled HTML
  - How to call it: Write to `<workflows>/<slug>/<slug>-flows.html`
  - If it fails: `mkdir -p` the slug folder first
  - Known issues: never write into the user's project source folders unless asked

- **Bash (python3 http.server)** - serves the file for the mandatory smoke test
  - How to call it: `cd <dir> && (python3 -m http.server 8931 >/dev/null 2>&1 &)`
  - If it fails: try another free port
  - Known issues: shell cwd may reset between Bash calls - always `cd` inside the same command

- **Browser preview (optional, if you have a browser tool)** - visual verification
  - How to call it: open `http://localhost:8931/<file>.html` in whatever browser tool your
    Claude setup has (a preview pane, a Chrome extension, Playwright) and take a screenshot
  - If it fails: confirm the server returns 200 via curl first
  - Known issues: `file://` URLs often do not render in automated browsers - serve over http.
    If you have no browser tool, open the page yourself and look at it before sharing

- **Artifact (optional, if your Claude setup can publish pages)** - publishes the final page
  - How to call it: Artifact with file_path and a short description
  - If it fails: check for `<!doctype>`/`<html>`/`<head>`/`<body>` tags, or an external asset
  - Known issues: hosted pages usually block every external host (CSP). Everything must be
    inline. Without a publishing tool, the local HTML file is the deliverable - share it
    directly or host it anywhere static

- **Bash python3 validate.py** - runs the Layer 1 structural gates on the written file
  - How to call it: `python3 <skill>/validate.py <file>`
  - If it fails: it prints the flow and node id for every fault - fix them, do not bypass
  - Known issues: it cannot see visual faults, so it never replaces the smoke test

- **Bash python3 build_index.py** - regenerates the workflows directory
  - How to call it: `python3 <skill>/build_index.py [--root <workflows>] [--open]`
  - If it fails: check each `meta.json` parses as JSON
  - Known issues: a folder without a `meta.json` is skipped, never guessed at

RULE: If a connector fails, debug and fix that connector. Never switch to an alternative
method. Log the root cause in `references/mcp-instructions.md`.

No secrets are used by this skill.

## Storage

Client data lives OUTSIDE this skill folder, so the skill stays portable and can be shared
or backed up without shipping prospect names.

```
<workflows>/
├── index.html                    regenerated every run, the directory you open
├── registry.json                 machine-readable mirror
└── <slug>/
    ├── <slug>-flows.html         the page source, self-contained
    └── meta.json                 name, kind, note, created, flows, hours, artifact_url
```

`meta.json` shape:

```json
{
  "name": "Example Content Agency",
  "kind": "prospect",
  "note": "one line of context",
  "created": "2026-01-15",
  "flows": ["B1 Copywriting & Captions", "B2 Editor Briefing"],
  "hours": 120,
  "artifact_url": "https://example.com/your-published-page"
}
```

`kind` is `client` or `prospect`. Omit `hours` when there are none. Omit or leave
`artifact_url` empty if the page was not published anywhere.
Disk is the source of truth - deleting a folder removes it from the index on the next run.

## The Process

1. Derive the structure from THIS conversation before drawing anything: what the system
   is, what problem it solves, how the user has described it, and how complex it really is.
   The handoff test decides one-vs-many: if one part's output feeds the next part, it is
   ONE flow. Separate flows only where pipelines run independently of each other.
   Phases, build status and "what's next" are NOT a reason to split - they are nodes in
   the same flow, and they say so in the goal sentence, not with a Power Up marker.
   State the structure back as a statement and proceed in the same turn.
   - Reference: none
   - HITL: only if genuinely ambiguous. The user may rename, merge or drop flows, but
     do not stop and ask them to confirm a structure the conversation already implies
   - Output: a one-line statement of the structure, then a numbered table if multi-flow

2. Ask for the three registry facts if not already obvious: who it is for, client or
   prospect, and one line of context.
   - Reference: none
   - HITL: **yes** - one short question, batched with step 1 where possible
   - Output: name, kind, note

3. For each flow write the node list. Every node gets id, column, row, role, icon, label,
   sub-label.
   - Reference: `references/node-grammar.md`
   - HITL: no
   - Output: a JS node array per flow

4. Lay out the grid. Column = stage in the pipeline, left to right. Row = parallel branches.
   Verify no two nodes in one flow share the same (col,row).
   - Reference: `references/node-grammar.md`
   - HITL: no
   - Output: validated coordinates

5. Write the edges. Every edge references two node ids that exist in that flow. Label only
   the handoffs that are not self-evident.
   - Reference: `references/node-grammar.md`
   - HITL: no
   - Output: a JS edge array per flow

6. Group the flows ONLY where they are genuinely independent of each other. One connected
   system gets a single group named after the system - never an invented split. Each group
   gets a name, a plain-language tag, a colour and its member ids. Add hours only if
   the user gave them.
   - Reference: none
   - HITL: no
   - Output: the ENGINES array

7. Fill the template. Seven markers: `{{TITLE}}`, `{{HEADER}}`, `{{SUBHEADER}}`,
   `{{BUILDS}}`, `{{GROUPS}}`, `{{ATTACH}}`, `{{FOUNDATIONS}}`. Change nothing else.
   Write to `<workflows>/<slug>/<slug>-flows.html`.

   **Four of them are marker + default PAIRS.** The template carries an empty
   declaration on the line straight after the marker:

   ```
   /*{{BUILDS}}*/
   const BUILDS=[];
   ```

   Replace **both lines together**, never the marker alone - filling only the marker
   declares the identifier twice, the entire `<script>` block fails to parse, and the
   diagram renders blank with no console error while every other gate still passes.
   Same for `{{GROUPS}}`/`const ENGINES=[]`. For `{{ATTACH}}` and `{{FOUNDATIONS}}`,
   when there is nothing custom to inject, delete the marker line and keep the default.
   - Reference: `references/template.html`
   - HITL: no
   - Output: a complete HTML file

8. Run the validator against the written file. It checks the Layer 1 structural gates
   automatically: unfilled placeholders, document tags, bad roles, unknown icons, grid
   collisions, dangling edges, oversized sub-labels, ungrouped flows. Fix everything it
   reports before going near the browser.
   - Reference: none
   - HITL: no
   - Output: `python3 <skill>/validate.py <file>` exiting 0

9. Smoke test locally. Serve the file, screenshot it, and actually read the screenshot.
   The validator cannot see visual faults - leftover client strings, text overflow, tangled
   edges, a diagram that is simply confusing. Only the render shows those.
   - Reference: none
   - HITL: no
   - Output: a screenshot you have looked at

9b. OPTIONAL, for a platform rather than a pipeline: add a sidebar button that opens a
    panel over the diagram with a plain table - what the client asked for, how we are
    solving it, where it is now, limits to know - with the same colour language as the
    nodes (green working, amber next, purple waiting on them). The third column doubles as
    the ask list. Patch it into the GENERATED file, never into `template.html`. See
    `references/features-panel.md` for the block to paste.
    Ship nothing interactive beyond open and close unless it has been verified in the
    PUBLISHED page - a zoom control that worked on localhost did not work once published,
    and had to be reverted the night before a call.
    - Reference: `references/features-panel.md`
    - HITL: no
    - Output: button + panel in the generated file

10. Fix anything the screenshot revealed and re-test. Repeat until clean. Then publish
    (if you have a publishing tool) and write `meta.json` with the returned URL.
    - Reference: `references/mcp-instructions.md`
    - HITL: **yes** - the user reviews before it goes to a client
    - Output: page URL (if published) + `meta.json`

11. Regenerate the directory and hand back both links.
    - Reference: none
    - HITL: no
    - Output: `python3 <skill>/build_index.py`, then the published URL (if any) plus a
      `file://` link to `<workflows>/index.html`

## Rules
- Never force a shape onto a system. Read the conversation and let the system's own
  structure decide how many flows there are and whether they group at all. Splitting one
  connected build into several flows under an invented grouping has happened more than
  once. Phases and build status are nodes inside one flow, not a reason to split it.
- Ask first whether a flow diagram is the right form at all. A pipeline that runs step by
  step draws well. A platform someone opens and uses does not - forcing one into a
  left-to-right sequence makes it look smaller than it is. When it is a platform, the
  diagram carries the shape and a panel carries the substance (see step 9b).
- Frame the panel around what the client ASKED FOR, never around what they got wrong.
  "What you asked for / How we are solving it / Where it is now" beats
  "What you hit / How it is solved" - the first reads as progress, the second as a
  post-mortem of their failure.
- Keep every panel cell to one idea in one short line. It gets talked over on a call,
  not read. If a cell needs a comma-spliced second clause, cut the clause.
- Carry the LIMITS into the panel as their own column. Quotas, approval waits and hard
  caps are what a technical buyer asks about in the room, and they live in the project's
  notes rather than in anyone's head. Name the number and who grants it - "about 5 working
  days", "roughly 100 uploads a day per project, ask the vendor to raise it" - never a vague
  "subject to limits".
- Say what the system will actually do, not what it does while you are still testing.
  A node reading "manual CSV exports" is wrong if the built system reads the API and the
  export was only a stand-in until access lands.
- Any dialog, panel or overlay goes OUTSIDE `#canvas`. The canvas calls
  `setPointerCapture` on pointer-down to pan, which steals the pointer-up and stops every
  click inside it from completing - a close button that does nothing while Escape still
  works is this bug. Then hit-test each added control with `elementFromPoint` and assert
  the state actually changed. `.click()` bypasses reachability and proves nothing.
- Never rewrite, restyle or "improve" the render engine in `template.html`. Replace the
  seven markers and nothing else. The engine is proven; edits to it are how it breaks.
- Never invent an icon name. Use only the keys listed in `references/node-grammar.md`.
  An unknown key renders an empty box with no error.
- Never publish without the local smoke test in step 9. A broken diagram opened in front of
  a client is worse than no diagram. This rule exists because an early version shipped
  with two hardcoded client strings that only the screenshot caught.
- Never put a client name, URL or hour figure into `references/template.html`. It stays
  generic. Client data lives only in `<workflows>/<slug>/`.
- Every node must carry one of the six roles: inp, ai, human, tool, gate, out. The role is
  what colours the node, and the colour split is the entire argument the diagram makes.
- NEVER mark anything a Power Up on your own. `pu` goes on a node, an edge or a flow ONLY
  where the user has said so in the conversation - "these are the power ups", "that one is
  later", "we could do that down the line". Absent that, leave every node solid. Inferring
  it from build status is the mistake: a whole flow dashed because it is not built yet is
  a label nobody asked for, and it makes the plan read as optional extras. Build status
  belongs in the goal sentence or the features panel, not in the Power Up device.
- Omit `hb` when there are no build hours. The chips and totals hide themselves. Never
  invent hours to fill the slot.
- ATTACH keys are `"<flowid>.<nodeid>"`. A key matching no node is silently ignored, so
  verify each against the node list.
- Keep sub-labels under about 40 characters or they overflow the node box.
- Always write `meta.json` in the same run that publishes the page. A diagram missing
  from the directory is a diagram that gets rebuilt from scratch six months later.

## Progressive Updates
Whenever the user says a clear thing not to do anymore, add it to the Rules section above
and confirm it was added.

Pattern triggers: "never do X", "stop doing X", "don't X", "I don't want X".

## Quality Gate

**Layer 1 - Hard Gates.** Most of these are executed, not eyeballed:

```
python3 <skill>/validate.py <file>
```

It must exit 0. It covers: unfilled placeholders, document tags, invalid roles, unknown
icon keys, grid collisions, dangling edges, oversized sub-labels, flows missing from every
group, and flows over the node ceiling. Never bypass a reported fault - fix it.

Three gates the validator cannot check, so they stay manual:
- [ ] Local smoke test screenshot taken and read - fail -> run step 9
- [ ] No leftover client name or stale text visible in the render - fail -> search and replace
- [ ] `meta.json` written and `build_index.py` run - fail -> run step 11

**Layer 2 - Review checks (yes/no, all four must be yes to deliver):**

| Check | Question |
|---|---|
| Legible | Could a non-technical prospect follow it with no explanation? |
| Honest roles | Do the human and gate nodes reflect reality, not a sales pitch? |
| Accurate | Does each flow match what was actually agreed in conversation? |
| Clear | Left-to-right progression, no crossing tangles, no text overflow? |

## Failure Modes
- Never show a human step as automated to make the diagram look stronger. The credibility of
  the whole page rests on the human and gate nodes being honest.
- Never let a flow exceed roughly 18 nodes. Past that it stops being readable - split it.
- Never guess at a step the user has not described. Ask, or leave it out.
- Never publish a page containing a client's private URLs unless the user confirms the
  page is going to that client.
- Never reuse a previous run's published URL for a different client. A new client gets a
  new file path, which mints a new URL.
- Never edit a file inside another client's `<slug>/` folder. One run touches one slug.

## Testing & Iterating - What To Do When Something Goes Wrong

When something goes wrong, don't silently retry. Stop and tell the user:
1. **What went wrong** (specific)
2. **Why it likely happened** (root cause)
3. **What the fix is** - based on this table:

| What happened | What to do |
|---|---|
| Didn't follow the process | Update the Process section in this SKILL.md |
| Bad outputs | Add more info or examples to `/references/` |
| Does something wrong (behaviour) | Add a Rule to the Rules section |
| Uses a Tool/MCP wrong | Update `references/mcp-instructions.md` |

Then ask: "Want me to apply the fix now?"
If yes -> make the change, increment version in frontmatter, log to CHANGELOG.md.

After applying the fix, re-test. If the same failure appears 2+ times -> update
`knowledge-base/lessons-learned.md`.

## Before Every Run
Read these files:
- `references/mcp-instructions.md`
- `references/node-grammar.md`
- `knowledge-base/lessons-learned.md`
- `knowledge-base/good-examples.md`

## After Every Run
- Output approved -> log to `knowledge-base/good-examples.md` with the review checks
- Output rejected -> the user gives the correct answer -> log as CORRECTION entry
- Tool/process failure -> log to `knowledge-base/failure-log.md` with root cause + fix
- Pattern emerging (2+ same failures) -> update `knowledge-base/lessons-learned.md` + this
  SKILL.md + increment version in frontmatter + log to `CHANGELOG.md`
