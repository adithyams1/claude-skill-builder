# Tool Instructions - workflow-flowchart

## Locked Methods
These are the ONLY methods this skill uses. If one fails, debug it - do not switch.

- **Read** -> `references/template.html`. Never regenerate the engine from scratch.
- **Write** -> the filled HTML, into `<workflows>/<slug>/`.
- **Bash** -> `python3 -m http.server` for the local smoke test.
- **Browser preview (optional)** -> open the served page and take a screenshot with whatever
  browser tool you have. Without one, open it yourself and look before sharing.
- **Artifact / any static host (optional)** -> publish.
- **Bash python3** -> `validate.py` for the hard gates, `build_index.py` to regenerate the
  workflows directory.

## Known Failure Fixes

| Symptom | Root cause | Fix |
|---|---|---|
| A node renders as an empty box | icon key not in the IC library | use a key from `node-grammar.md` |
| An edge does not appear | `from` or `to` id does not exist in that flow | fix the id typo |
| Two nodes sit on top of each other | duplicate `(col,row)` in one flow | re-lay the grid |
| Sidebar shows a flow but clicking does nothing | id in GROUPS has no match in BUILDS | align the ids |
| Whole diagram is blank, no console error | a marker was filled but the default `const` under it was left, so the identifier is declared twice | replace the marker AND the default line together |
| Published page is blank | `<!doctype>`/`<html>`/`<head>`/`<body>` present, or an external asset | strip the tags, inline everything |
| Published page renders unstyled | external stylesheet or font | hosted pages often block all external hosts (CSP), inline it |
| Sub-label text spills out of the node | sub longer than ~40 chars | shorten it |
| `0h` chips appear on an hourless diagram | `hb` set to 0 instead of omitted | delete the `hb` key |
| Shell "cwd was reset" between Bash calls | each call is a fresh shell | `cd` inside the same command |

## Rejected alternatives

- **Rebuilding the canvas inside a design tool** - the pan-zoom canvas would have to be
  rebuilt there, and it adds a review round-trip for a single diagram. Rejected.
- **Local HTML file only** - you own the file, but there is no shareable link for a prospect
  without hosting it. Kept as the source of truth, not as the only deliverable.
- **Mermaid** - far less code, but no role colouring, no icons, no clickable example chips,
  no pan-zoom. The colour split is the whole argument, so mermaid loses the point. Rejected.

## Tool Failure Protocol
1. Read the error message carefully
2. Check Known Failure Fixes above first
3. If not listed: diagnose the root cause of THIS tool - do not switch methods
4. Log the failure + fix here under Known Failure Fixes
5. Retry with the fix applied
