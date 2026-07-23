---
name: skill-builder
description: Builds new Claude Code skills using the Skill Prompting Framework. Use when the user says "build me a skill", "create a new skill", "I want a skill that...", or "skill builder".
version: 1.3
---

# Skill Builder

Builds production-ready Claude Code skills using the **Skill Prompting Framework**.

All skills saved to `~/.claude/skills/{skill-name}/`.

---

## The Skill Anatomy

Every skill follows this folder structure:

```
{skill-name}/
├── SKILL.md                    ← Core skill file
├── CHANGELOG.md                ← Version history — every change logged
├── references/                 ← Files the skill reads during execution
│   ├── 01_*.md
│   ├── 02_*.md
│   └── mcp-instructions.md     ← Required if skill uses any MCP/tool
├── assets/                     ← Example images, videos, presentation references
├── code-scripts/               ← Only if skill runs code
└── knowledge-base/
    ├── good-examples.md        ← Approved outputs + correct answers
    ├── failure-log.md          ← Bad outputs + root cause + fix
    └── lessons-learned.md      ← Rules derived from patterns
```

---

## Step 1 — Gather Requirements

Ask the user ALL of these at once. Never drip them one by one.

**Before asking anything — scan existing skills:**
Run `ls ~/.claude/skills/` and read the names. When proposing a skill name, make sure it:
- Doesn't duplicate an existing skill name
- Doesn't sound so similar it could cause confusion (e.g. don't create `lead-finder` if `media-ip-lead-finder` exists)
- Is specific enough to be unambiguous — prefer `media-ip-mockup` over `mockup`, `shopogenie-lead-gen` over `lead-gen`
- Uses lowercase-hyphen-case, verb-led or noun-led (e.g. `roundtable-queue-runner`, `brand-extractor`)

Propose the name to the user and confirm before building.

**About the skill:**
1. **Name & Trigger** — What is this skill called? When exactly should it be triggered? What phrases activate it?
2. **The Goal** — What does this skill need to do? One clear sentence describing the perfect output.
3. **Connectors** — What MCPs, tools, APIs, or methods does it need to use? Be exact (e.g. "Nano Banana MCP", "Chrome MCP navigate", "Bash osascript", "Notion MCP notion-create-pages").

**About the process:**
4. **Step-by-step process** — Walk me through exactly how the skill should work, step by step.

**For each step, also ask:**
- **HITL?** — Does this step require human input or approval before moving on? (Human in the Loop)
- **Reference file?** — Does this step need to read a specific file? Which one?
- **Output format?** — What should this step produce? (a list, a widget, a file, a question to the user, etc.)

**About assets & references:**
5. **Assets** — Do you have any example images, videos, or presentation examples to include as visual reference? (goes in `/assets/`)
6. **Reference files** — Any context docs, style guides, ICP profiles, brand guidelines, or other files the skill should read?

**About failure & maintenance:**
7. **Where can it go wrong?** — What are the risky steps? What failure modes should it watch for?
8. **Progressive updates** — What kinds of things, if the user says "never do X again", should automatically get added to the Rules section?

**About quality:**
9. **Skill type** — Is this skill more creative/generative (titles, thumbnails, copy) or data/qualification-driven (lead finding, scoring, classification)? This determines the evaluation system:
   - **Creative** → rubric only (spectrum of quality, scored dimensions, threshold to deliver)
   - **Data/qualification** → hard gates only (binary pass/fail on must-haves)
   - **Both** → hard gates first (must-haves that are binary), then rubric for the subjective parts
10. **Success criteria** — How do we know the output is good? List 4–6 specific, measurable criteria. (These become the rubric dimensions or gate checks depending on skill type.)
11. **Good example output** and **bad example output** — one of each, as specific as possible.

Wait for all answers. Then build.

---

## Step 1.5 — Solution Survey (before locking any connector or mechanism)

**This thinking happens HERE, at build time, and ONLY here. Generated skills never deliberate about alternative methods at runtime - they lock one mechanism and execute (Connectors rule). The survey is where that mechanism earns its lock.**

Before writing the Connectors section, for every fragile or expensive step (image generation, pasting into web apps, rendering, exporting, uploading, anything automated through a UI):

1. **Enumerate candidates across ALL layers, not just tools available right now.** Include options that require building something first. Typical layers:
   - OS-level automation (osascript, keyboard/clipboard simulation)
   - Browser automation from outside (CDP, Chrome MCP, Playwright)
   - In-page script injection (synthetic events)
   - A Chrome extension living inside the page
   - Headless render (Playwright + HTML template)
   - A direct API call (skip the UI entirely)
   - A one-time coded tool/script that replaces the manual flow
2. **Compare on four axes:** reliability, speed per run, running cost (tokens / credits / quota), and one-time build effort.
3. **Present the tradeoff to the user and let him choose.** Never silently pick the zero-setup path because it starts working in ten minutes. "Works today but fragile forever" vs "one day of building, then free and reliable" is HIS decision, not a default.
4. The chosen mechanism gets locked into Connectors. The rejected candidates get one line each in `references/mcp-instructions.md` under "Rejected alternatives" with the reason - so a future patch session knows what was already considered.

**Why this exists:** the osascript-vs-Chrome-extension case (2026-07). Weeks were spent patching OS-level paste automation (focus bugs, clipboard races, serial-only rules, tab-title tagging) because the build-time survey never happened. The extension - one build day, then flawless - was never presented as an option because it couldn't be run in-session that day. See `knowledge-base/lessons-learned.md`.

---

## Step 2 — Build the SKILL.md

**Progressive Disclosure Rule:** Keep SKILL.md under 500 lines. If detailed content (schemas, API docs, style guides, long examples) would push it over, move that content into a `references/` file and link to it from SKILL.md with a clear note of when to read it. SKILL.md should contain the core workflow — not every detail.

The SKILL.md follows this exact structure — in this order:

### Section 1: Name & Trigger
```
## Name & Trigger
**Name:** {skill name}
**Trigger:** {exact conditions — what phrases, contexts, or user actions activate this skill}
```

### Section 2: The Goal
```
## The Goal
{One clear sentence. What does a perfect output look like? What is this skill ultimately producing?}
```

### Section 3: Connectors
```
## Connectors
{List every MCP, tool, API, or method this skill uses.}

- **{Tool/MCP name}** — {what it's used for in this skill}
  - How to call it: {exact tool name / command / method}
  - If it fails: {debug steps for THIS tool — never switch to an alternative method}
  - Known issues: {any pre-logged quirks}

RULE: If a connector fails, debug and fix that connector. Never switch to an alternative method.
If the connector keeps failing, update `references/mcp-instructions.md` with the root cause and fix.
```

**MANDATORY — Secrets & Credentials (never hardcode a key in a skill).** Every skill that needs an API
key, token, OAuth credential, DB id-with-auth, or any secret MUST read it at runtime from the ONE central
store, never inline it in SKILL.md, a script, an .env, or a token file inside the skill folder. This way a
leaked/shared skill exposes zero credentials — restore = reload the skill, keys come from the central store.

- **API keys** live in `~/.claude/api_keys.json`, keyed by service. Load them, e.g.:
  `KEY = __import__("json").load(open(__import__("os").path.expanduser("~/.claude/api_keys.json")))["<service>"]`
  (bash: `python3 -c 'import json,os;print(json.load(open(os.path.expanduser("~/.claude/api_keys.json")))["<service>"])'`).
  If a service has a rotation pool, store a list (e.g. `youtube_data_api_pool`) and index/rotate over it.
- **OAuth token files** (Gmail/Drive/etc.) live in `~/.claude/*.json` (e.g. `~/.claude/gmail_token.json`),
  NOT inside the skill. Reference the central path; never cache a token into the skill's own folder.
- When a skill needs a NEW key, add it to `~/.claude/api_keys.json` under a clear service name and reference
  it — tell the user which name to populate. Never write the literal value into any skill file.
- The `backup-skills` skill's redactor + fail-closed gate is the backstop, but the SOURCE must be clean:
  a hardcoded key is a bug even if the backup scrubs it.

### Section 4: The Process
```
## The Process

{Numbered steps. For every step — call out HITL, reference file, and output format inline.}

1. {Step description}
   - 📁 Reference: {file to read, or "none"}
   - 👤 HITL: {yes — wait for user input/approval before proceeding | no — continue automatically}
   - 📤 Output: {what this step produces}

2. {Step description}
   - 📁 Reference: {file to read, or "none"}
   - 👤 HITL: {yes/no + what kind of input}
   - 📤 Output: {what this step produces}

...and so on for every step.
```

### Section 5: Rules
```
## Rules
{Specific, non-obvious constraints. Not generic advice.}
- {Never do X because Y}
- {Never do X because Y}
- {Never do X because Y}
```

### Section 6: Progressive Updates
```
## Progressive Updates
Whenever the user says a clear thing not to do anymore, automatically add it to the Rules section above.
Do not ask — just update the Rules and confirm it was added.

Pattern triggers for auto-update:
- "never do X"
- "stop doing X"
- "don't X"
- "I don't want X"
```

### Section 7: Quality Gate / Rubric

Choose the right evaluation system based on skill type (question 9):

**Creative skills → Rubric only:**
```
## Rubric
Always generate at least 3 variations. Score all. Deliver only the highest scoring one.
Self-score silently. Only show scores if asked. Minimum 28/40 — regenerate if all score below.

| Dimension | What it measures | Score (1–10) |
|---|---|---|
| {from success criteria 1} | {what it measures} | /10 |
| {from success criteria 2} | {what it measures} | /10 |
| {from success criteria 3} | {what it measures} | /10 |
| {from success criteria 4} | {what it measures} | /10 |

**Total: /40**
```

**Data/qualification skills → Hard gates only:**
```
## Quality Gate
All must pass or output is rejected — no partial credit.

- [ ] {must-have check 1} — fail → {what to do}
- [ ] {must-have check 2} — fail → {what to do}
- [ ] {must-have check 3} — fail → {what to do}
```

**Both → Hard gates first, then rubric:**
```
## Quality Gate

**Layer 1 — Hard Gates (all must pass or reject immediately):**
- [ ] {binary check} — fail → {what to do}
- [ ] {binary check} — fail → {what to do}

**Layer 2 — Rubric (scored, minimum {X}/{Y*10} to deliver):**
| Dimension | What it measures | Score (1–10) |
|---|---|---|
| {subjective dimension} | {what it measures} | /10 |
| {subjective dimension} | {what it measures} | /10 |

**Total: /{Y*10}**
```

### Section 8: Examples
```
## Examples

Populated from live test runs — never invented.
Run Step 5 to generate real examples before deploying.

<!-- After first approved test run, replace this with:
**Good Example:**
{actual output from run}
*Why it works: {specific reason tied to success criteria}*
*Rubric Score: {X/40}*

**Bad Example / Correction:**
{what Claude produced}
*What was wrong: {specific reason}*
*Correct answer: {what the user said it should be}*
-->
```

### Section 9: Failure Modes
```
## Failure Modes
{Things to never do — based on the "where can it go wrong" answers.}
- {Never X because Y}
- {Never X because Y}
```

### Section 10: Testing & Iterating
```
## Testing & Iterating — What To Do When Something Goes Wrong

When something goes wrong, don't silently retry. Stop and tell the user:
1. **What went wrong** (specific)
2. **Why it likely happened** (root cause)
3. **What the fix is** — based on this table:

| What happened | What to do |
|---|---|
| Didn't follow the process | Update the Process section in this SKILL.md |
| Bad outputs | Add more info or examples to `/references/` |
| Does something wrong (behaviour) | Add a Rule to the Rules section in this SKILL.md |
| Uses a Tool/MCP wrong | Create or update `references/mcp-instructions.md` |

Then ask: "Want me to apply the fix now?"
If yes → make the change, increment version in frontmatter, log to CHANGELOG.md.

After applying the fix, re-test. If the same failure appears 2+ times → update `knowledge-base/lessons-learned.md`.
```

### Section 11: Before & After Every Run
```
## Before Every Run
Read these files:
- `references/mcp-instructions.md` (if exists)
- `knowledge-base/lessons-learned.md`
- `knowledge-base/good-examples.md`

## After Every Run
- Output approved → log to `knowledge-base/good-examples.md` with rubric score
- Output rejected → the user writes the correct answer → log as CORRECTION entry in `good-examples.md` (this is the training data)
- Tool/process failure → log to `knowledge-base/failure-log.md` with root cause + fix
- Pattern emerging (2+ same failures) → update `knowledge-base/lessons-learned.md` + this SKILL.md + increment version in frontmatter + log to `CHANGELOG.md`
```

**If this skill runs unattended** (a LaunchAgent/cron, or any step with no human watching live -
overnight queues, nightly pushes, scheduled scans), log a one-line status to whatever monitoring
or daily-briefing system you use (a status file, a log, a dashboard). The summary must state what
actually happened ("3 drafts pushed, 1 flagged: missing CTA"), never just that the script ran
without error, and any "needs attention" flag should mirror this skill's own verdict (an
evaluator's FLAG/FAIL, a nonzero queue) rather than a separate guess. If you don't have a
monitoring system, skip this — it's optional infrastructure.

---

## Degrees of Freedom — Before Writing Each Step

Before writing each process step, decide how specific the instructions need to be:

| Freedom Level | When to use | How to write it |
|---|---|---|
| **High** (text guidance) | Multiple approaches are valid, context drives the decision | Write heuristics and principles |
| **Medium** (pseudocode/pattern) | A preferred pattern exists, some variation OK | Write the pattern with parameters |
| **Low** (exact steps, no variation) | Fragile, error-prone, must be done a specific way | Write exact commands, exact tool calls, exact sequence |

Fragile steps (MCP calls, file writes, Notion pushes) = low freedom. Creative steps (writing, scoring) = high freedom.

---

## Step 3 — Create Reference Files

- **Always create `references/mcp-instructions.md`** if any connectors are listed. Pre-populate with known issues if the user flagged any.
- Create any other reference files mentioned in question 6 — stub them with the right headers if full content wasn't provided.
- **If assets were provided (question 5)** — save them into the `/assets/` folder and note in SKILL.md which steps reference them.

`mcp-instructions.md` template:
```markdown
# MCP & Tool Instructions for {skill-name}

## Locked Methods
These are the ONLY methods this skill uses. If a method fails, debug it — do not switch.

{connector entries}

## Known Failure Fixes
{pre-populated from requirements, or empty}

## Tool Failure Protocol
1. Read the error message carefully
2. Check Known Failure Fixes above first
3. If not listed: diagnose root cause of THIS tool — do not switch methods
4. Log the failure + fix here under Known Failure Fixes
5. Retry with fix applied
```

---

## Step 4 — Create Knowledge Base Files

The knowledge base is the skill's memory. It turns the skill into a compounding asset — the more it runs, the smarter it gets.

Every skill gets this self-improvement loop baked in:
```
GENERATE → EVALUATE (rubric) → ANALYZE FAILURES → STORE LESSONS → IMPROVE FUTURE RUNS → repeat
```

**`knowledge-base/good-examples.md`**
```markdown
# Good Examples — {skill-name}
Read at the start of every run to calibrate what "good" looks like.
When Claude gets something wrong, the user writes the correct answer here — this is the training data.

---

## [Date] — [Task]
**Output:** [the actual output]
**Why it worked:** [specific reason]
**Rubric Score:** [X/40]

---

## [Date] — [Task] ← CORRECTION
**What Claude did:** [the wrong output]
**Correct answer:** [what the user wrote as the right answer]
**What to do differently:** [specific instruction]
```

**`knowledge-base/failure-log.md`**
```markdown
# Failure Log — {skill-name}
Every bad output gets logged here. The more data collected, the smarter the system becomes.

| Output | Failure Type | Root Cause | Fix / Lesson |
|--------|-------------|------------|--------------|
| [the bad output] | Generic / Too Broad / Low Curiosity / Wrong Format / etc. | [specific reason it failed] | [what to do differently] |
```

**`knowledge-base/lessons-learned.md`**
```markdown
# Lessons Learned — {skill-name}
General rules derived from failure patterns. Read at start of every run.

---

## Rule: [rule name]
**Pattern:** [what keeps going wrong]
**Rule:** [the fix, stated as a clear instruction]
**Added:** [date]
```

---

## Step 5 — Populate Examples with the user

Once skill files are written, ask the user:

> "Skill is built. To populate the examples, I can either:
> A) Run it live on a real task right now — you tell me if the output is right
> B) You give me examples directly — I'll ask you what makes them good or bad
> Which do you want, or both?"

**Path A — Live test run:**
1. Run the skill on a real task, show the user the full output
2. Ask: "Does this look right? What would you change?"
3. Output approved → log to `knowledge-base/good-examples.md` with rubric score
4. Output wrong → the user writes the correct answer → log as CORRECTION entry
5. Process broke → fix SKILL.md, run again
6. the user can request more runs — keep going until they say they're done

**Path B — the user provides examples directly:**
1. the user gives a good example → ask "What makes this good? What specifically should I replicate?"
2. the user gives a bad example → ask "What's wrong with this? What should I have done instead?"
3. Log both with the explanation they gave

**Both paths feed the same files:** `knowledge-base/good-examples.md` and the Examples section in SKILL.md.

**Never:**
- Invent examples, fabricate outputs, make up leads or data
- Mark the skill as deployed before at least one example is logged
- Stop after one run if the user wants more

## Step 6 — Create CHANGELOG.md

```markdown
# Changelog — {skill-name}

## v1.0 — [date]
**Created.** Initial skill built via skill-builder.
- Objective: {one line}
- Process steps: {count}
- Connectors: {list or "none"}
- Reference files: {list or "none"}
- Assets: {list or "none"}

---

<!-- Every time SKILL.md is updated, log it here: -->
<!-- ## v1.X — [date] -->
<!-- **Changed:** [what changed and why — which failure or pattern triggered it] -->
```

Every time SKILL.md gets updated (new rule, process change, connector fix) → increment version in frontmatter + add entry here.

---

## Step 7 — Register in your memory index (optional)

If you keep a memory index (e.g. a `MEMORY.md` that Claude loads each session), add a one-line
pointer to the new skill there so it's discoverable later. If you don't have one, skip this step.

---

## Step 8 — Show the user the Full SKILL.md for Review

Always show the complete generated SKILL.md before saving anything. Let the user approve or request changes. Only write files after approval.

---

## When to Change the Skill vs. Not

**CHANGE the process/skill when:**
- The same type of mistake keeps happening (2+ times)
- The current workflow is not solving the problem
- A pattern of failures appears frequently

**RE-ARCHITECT (don't patch) when:**
- A single mechanism has accumulated 3+ corrective rules, or keeps failing after repeated fixes
- That's the signal the mechanism is at the wrong layer, not that it needs another rule
- Action: stop patching, re-run the Step 1.5 Solution Survey on that step, and present alternatives (including build-first options) to the user
- This decision happens in a skill-builder / patching session only - NEVER inside a skill run. Mid-run, the locked mechanism stays locked.

Example: Outputs are often too generic → Add a step to extract the strongest specific angle first.

**DON'T change the skill when:**
- Only one or two outputs are bad
- It's random or rare
- The process is working but the output just missed

Example: One output is weak → Log the failure, learn from it, move on.

---

## Quick Checklist — Before a Skill is Done

Every skill must pass all of these before it's considered complete:

- [ ] Clear objective and success criteria defined
- [ ] Step-by-step process defined (with HITL + reference file + output format per step)
- [ ] Rubric dimensions derived from success criteria (generates 3 variations, scores all, delivers highest, 28/40 minimum)
- [ ] Good & bad examples included (specific, tied to success criteria)
- [ ] Failure modes defined (specific, not generic)
- [ ] Solution Survey run on every fragile/expensive step — alternatives compared across layers, tradeoff shown to the user, rejected options logged in mcp-instructions.md
- [ ] Connectors locked in (no improvisation when tools fail)
- [ ] **No secrets hardcoded** — every key/token/OAuth read from `~/.claude/api_keys.json` (or `~/.claude/*token*.json`), never inline in the skill
- [ ] Assets folder populated or confirmed not needed
- [ ] Reference files created or stubbed
- [ ] Progressive Updates section included
- [ ] Knowledge base created (all 3 files)
- [ ] At least one live test run completed with the user
- [ ] Examples section populated from real run output (never invented)
- [ ] CHANGELOG.md created with v1.0 entry
- [ ] Version number in SKILL.md frontmatter
- [ ] Registered in MEMORY.md

**Remember: It's not about the perfect prompt. It's about the perfect system. Systems > Prompts.**

---

## Rules

1. Ask all questions upfront — never drip them one by one
2. Always call out HITL, reference file, and output format for every process step
3. Rubric dimensions must come from the success criteria — not invented
4. Progressive Updates section is mandatory in every skill
5. Connectors section must lock the method — never allow improvisation when a tool fails
5b. **Never hardcode a secret in a skill** — all API keys/tokens/OAuth read at runtime from the central `~/.claude/api_keys.json` (or `~/.claude/*token*.json`), keyed by service, so a leaked skill exposes nothing (see the Secrets & Credentials block under Section 3)
6. Failure modes must be specific ("never use X because Y") — not generic advice
7. Show full SKILL.md for review and get approval before saving any files
8. **Never invent examples** — good/bad examples only come from real test runs with the user; leave the Examples section empty until Step 5 produces them
9. "When to Change" and Quick Checklist live in the skill builder only — not in generated skills (Testing & Iterating table covers it there)
10. **Solution Survey before locking any mechanism** — enumerate candidates across all layers (including build-first options like extensions, headless renders, direct APIs), compare reliability / speed / running cost / build effort, and let the user choose. Never silently default to the zero-setup path.
11. **3+ patches on one mechanism = re-architect, not another rule** — re-run the Solution Survey on that step. This applies only in build/patch sessions; generated skills never explore alternatives at runtime.
