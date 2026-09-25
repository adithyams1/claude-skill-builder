---
name: skill-builder-v2
description: Builds new Claude Code skills using the Skill Prompting Framework. Use when you say "build me a skill", "create a new skill", "I want a skill that...", or "skill builder".
version: 1.11
status: draft
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
├── CHANGELOG.md                ← Version history - every change logged
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

## Step 1 - Gather Requirements

**First: is there a SPEC.md?** Look next to the product this skill serves. If one exists, read it
and answer every question below that it already answers - never re-ask you something you
settled in the spec. Then **list what was taken from the spec** ("the goal, the volume and the
non-goals come from a client pipeline skill/SPEC.md") and ask only the remainder.

A spec answers: the goal (Q2), what the outputs are and how many, the success criteria (Q10), the
non-goals, and usually the connector decision (Q3) with its rejected alternatives. It does NOT
answer: the trigger phrases (Q1), the step-by-step process (Q4), assets (Q5), failure modes (Q7),
or the good/bad examples (Q11).

**If a spec answers a question only partly, ask.** A thin spec is a reason to ask more, never a
licence to build on the gap. Say which question the spec left open and why you are asking it.

Ask you ALL the remaining questions at once. Never drip them one by one.

**Before asking anything - scan existing skills:**
Run `ls ~/.claude/skills/` and read the names. When proposing a skill name, make sure it:
- Doesn't duplicate an existing skill name
- Doesn't sound so similar it could cause confusion (e.g. don't create `lead-finder` if `acme-lead-finder` exists)
- Is specific enough to be unambiguous - prefer `acme-mockup` over `mockup`, `acme-lead-gen` over `lead-gen`
- Uses lowercase-hyphen-case, verb-led or noun-led (e.g. `queue-runner`, `brand-extractor`)

Propose the name to you and confirm before building.

**Splitting work across skills - split by job, never to save context.** Context has its own
answers: work that never enters the window (scripts), research that happens elsewhere (subagents),
and detail read only when needed (progressive disclosure inside one skill). The real limit is
human comprehension, not the model's - twenty skills for one client is how features get built
that nobody asked for.

Test before splitting: **can a person produce a judgeable example of this step's output?** If
nothing in the pipeline can, it is not a job - it is an implementation detail of the step beside
it, and it belongs inside that skill.

**About the skill:**
1. **Name & Trigger** - What is this skill called? When exactly should it be triggered? What phrases activate it?
2. **The Goal** - What does this skill need to do? One clear sentence describing the perfect output.
3. **Connectors** - What MCPs, tools, APIs, or methods does it need to use? Be exact (e.g. "Nano Banana MCP", "Chrome MCP navigate", "Bash osascript", "Notion MCP notion-create-pages").

**About the process:**
4. **Step-by-step process** - Walk me through exactly how the skill should work, step by step.

**For each step, also ask:**
- **HITL?** - Does this step require human input or approval before moving on? (Human in the Loop)
- **Reference file?** - Does this step need to read a specific file? Which one?
- **Output format?** - What should this step produce? (a list, a widget, a file, a question to the user, etc.)

**About assets & references:**
5. **Assets** - Do you have any example images, videos, or presentation examples to include as visual reference? (goes in `/assets/`)
6. **Reference files** - Any context docs, style guides, ICP profiles, brand guidelines, or other files the skill should read?

**About failure & maintenance:**
7. **Where can it go wrong?** - What are the risky steps? What failure modes should it watch for?
8. **Progressive updates** - What kinds of things, if you say "never do X again", should automatically get added to the Rules section?

**About quality:**
9. **Skill type** - Is this skill more creative/generative (titles, thumbnails, copy) or data/qualification-driven (lead finding, scoring, classification)? This determines the evaluation system:
   - **Creative** → rubric only (spectrum of quality, scored dimensions, threshold to deliver)
   - **Data/qualification** → hard gates only (binary pass/fail on must-haves)
   - **Both** → hard gates first (must-haves that are binary), then rubric for the subjective parts
10. **Success criteria** - How do we know the output is good? List 4-6 specific, measurable criteria. (These become the rubric dimensions or gate checks depending on skill type.)
11. **Good example output** and **bad example output** - one of each, as specific as possible.

Wait for all answers. Then build.

---

## Step 1.5 - Solution Survey (before locking any connector or mechanism)

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
3. **Present the tradeoff to the user and let them choose.** Never silently pick the zero-setup path because it starts working in ten minutes. "Works today but fragile forever" vs "one day of building, then free and reliable" is THEIR decision, not a default.
4. The chosen mechanism gets locked into Connectors. The rejected candidates get one line each in `references/mcp-instructions.md` under "Rejected alternatives" with the reason - so a future patch session knows what was already considered.

**Why this exists:** weeks can go into patching fragile UI automation because nobody surveyed the options at build time, when a one-day build (an extension, a direct API) would have been reliable from then on.

---

## Step 2 - Build the SKILL.md

**Progressive Disclosure Rule:** Keep SKILL.md under 500 lines. If detailed content (schemas, API docs, style guides, long examples) would push it over, move that content into a `references/` file and link to it from SKILL.md with a clear note of when to read it. SKILL.md should contain the core workflow - not every detail.

The SKILL.md follows this exact structure - in this order:

### Section 1: Name & Trigger
```
## Name & Trigger
**Name:** {skill name}
**Trigger:** {exact conditions - what phrases, contexts, or user actions activate this skill}
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

- **{Tool/MCP name}** - {what it's used for in this skill}
  - How to call it: {exact tool name / command / method}
  - If it fails: {debug steps for THIS tool - never switch to an alternative method}
  - Known issues: {any pre-logged quirks}

RULE: If a connector fails, debug and fix that connector. Never switch to an alternative method.
If the connector keeps failing, update `references/mcp-instructions.md` with the root cause and fix.
```

**MANDATORY - Secrets & Credentials (never hardcode a key in a skill).** Every skill that needs an API
key, token, OAuth credential, DB id-with-auth, or any secret MUST read it at runtime from the ONE central
store, never inline it in SKILL.md, a script, an .env, or a token file inside the skill folder. This way a
leaked/shared skill exposes zero credentials - restore = reload the skill, keys come from the central store.

- **API keys** live in `~/.claude/keys.json`, keyed by service. Load them, e.g.:
  `KEY = __import__("json").load(open(__import__("os").path.expanduser("~/.claude/keys.json")))["<service>"]`
  (bash: `python3 -c 'import json,os;print(json.load(open(os.path.expanduser("~/.claude/keys.json")))["<service>"])'`).
  If a service has a rotation pool, store a list (e.g. `service_pool`) and index/rotate over it.
- **OAuth token files** (Gmail/Drive/etc.) live in `~/.claude/*.json` (e.g. `~/.claude/google-login.json`),
  NOT inside the skill. Reference the central path; never cache a token into the skill's own folder.
- When a skill needs a NEW key, add it to `~/.claude/keys.json` under a clear service name and reference
  it - tell you which name to populate. Never write the literal value into any skill file.
- A hardcoded key is a bug even if something downstream would scrub it: the SOURCE must be clean.

### Section 4: The Process
```
## The Process

{Numbered steps. For every step - call out HITL, reference file, and output format inline.}

1. {Step description}
   - 📁 Reference: {file to read, or "none"}
   - 👤 HITL: {yes - wait for user input/approval before proceeding | no - continue automatically}
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
Whenever you say a clear thing not to do anymore, automatically add it to the Rules section above.
Do not ask - just update the Rules and confirm it was added.

Pattern triggers for auto-update:
- "never do X"
- "stop doing X"
- "don't X"
- "I don't want X"
```

### Section 7: Quality Gate / Rubric

Choose the right evaluation system based on skill type (question 9):

**NEVER score 1 to 10.** Every camp in the evidence agrees a 0-10 scale is the worst choice: the
difference between a 6 and a 7 is indefensible, models and people both drift to the middle, and it
gives no action. What the evidence supports (sources at the end of this section):

| Kind of judgment | Format |
|---|---|
| Objective, gateable ("does it name a fact the client confirmed?") | **Binary** pass/fail, one isolated check per dimension |
| Subjective quality ("which of these two hooks is better?") | **Pairwise**, with the order randomised |
| A scale, only when a gradient is genuinely needed | **0-5 at most**, never 0-10 |

Prefer decomposition over any scale: "4 of 5 expected facts included" as five binary checks beats
"accuracy: 7/10".

**Creative skills → binary checks, then a pairwise pick:**
```
## Quality Gate
Generate at least 3 variations. Every one must pass all the checks; then pick the best by comparing
them in pairs, in random order. Never score a variation 1 to 10.

- [ ] {check 1, answerable yes or no} - fail → {what to do}
- [ ] {check 2, answerable yes or no} - fail → {what to do}
- [ ] {check 3, answerable yes or no} - fail → {what to do}

**Pick:** compare the survivors two at a time on {the one thing that matters}, randomise which is
shown first, keep the winner.
```

**Data/qualification skills → Hard gates only:**
```
## Quality Gate
All must pass or output is rejected - no partial credit.

- [ ] {must-have check 1} - fail → {what to do}
- [ ] {must-have check 2} - fail → {what to do}
- [ ] {must-have check 3} - fail → {what to do}
```

**Both → gates, then the pairwise pick:**
```
## Quality Gate

**Layer 1 - Hard gates (all must pass or reject immediately):**
- [ ] {binary check} - fail → {what to do}
- [ ] {binary check} - fail → {what to do}

**Layer 2 - The pick:** compare survivors in pairs on {the subjective thing}, order randomised.
```

**A judge is never trusted until it is measured against a person.** If a skill uses a model to grade,
take 30 to 50 outputs, have the domain expert label them pass/fail, and compare. Report the judge's
true positive and true negative rates SEPARATELY; raw agreement is a trap, because a judge that always
says pass scores 90% when failures are 10% of cases.

Sources: Anthropic, "Demystifying evals for AI agents" (one isolated judge per dimension, binary
rubric items) and platform.claude.com test-and-evaluate (binary for objective, 0-5 for subjective);
Hamel Husain, evals FAQ (binary, decomposition, TPR/TNR); Eugene Yan, "Evaluating LLM-Evaluators"
(binary for objective, pairwise for subjective); Li et al. arXiv 2601.03444 (0-5 best, 0-10 worst);
Zheng et al., MT-Bench (pairwise position bias, 50-70%).

### Section 8: Examples
```
## Examples

Populated from live test runs - never invented.
Run Step 5 to generate real examples before deploying.

<!-- After first approved test run, replace this with:
**Good Example:**
{actual output from run}
*Why it works: {specific reason tied to success criteria}*
*Checks passed: {e.g. 4 of 4 yes/no checks}*

**Bad Example / Correction:**
{what Claude produced}
*What was wrong: {specific reason}*
*Correct answer: {what you said it should be}*
-->
```

### Section 9: Failure Modes
```
## Failure Modes
{Things to never do - based on the "where can it go wrong" answers.}
- {Never X because Y}
- {Never X because Y}
```

### Section 10: Testing & Iterating
```
## Testing & Iterating - What To Do When Something Goes Wrong

When something goes wrong, don't silently retry. Stop and tell you:
1. **What went wrong** (specific)
2. **Why it likely happened** (root cause)
3. **What the fix is** - based on this table:

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
- Output approved → log to `knowledge-base/good-examples.md` with which checks it passed
- Output rejected → you write the correct answer → log as CORRECTION entry in `good-examples.md` (this is the training data)
- Tool/process failure → log to `knowledge-base/failure-log.md` with root cause + fix
- Pattern emerging (2+ same failures) → update `knowledge-base/lessons-learned.md` + this SKILL.md + increment version in frontmatter + log to `CHANGELOG.md`
```

**If this skill runs unattended** (a scheduled task, overnight queue, or any step with no human
watching live), add one more line to "After Every Run": log a one-line outcome somewhere you
actually read (a daily summary, a log file, a message to yourself). The line must state what
actually happened ("3 drafts pushed, 1 flagged: missing CTA"), never just that the script ran
without error.

---

## Degrees of Freedom - Before Writing Each Step

Before writing each process step, decide how specific the instructions need to be:

| Freedom Level | When to use | How to write it |
|---|---|---|
| **High** (text guidance) | Multiple approaches are valid, context drives the decision | Write heuristics and principles |
| **Medium** (pseudocode/pattern) | A preferred pattern exists, some variation OK | Write the pattern with parameters |
| **Low** (exact steps, no variation) | Fragile, error-prone, must be done a specific way | Write exact commands, exact tool calls, exact sequence |

Fragile steps (MCP calls, file writes, Notion pushes) = low freedom. Creative steps (writing, scoring) = high freedom.

---

## Step 3 - Create Reference Files

- **Always create `references/mcp-instructions.md`** if any connectors are listed. Pre-populate with known issues if you flagged any.
- Create any other reference files mentioned in question 6 - stub them with the right headers if full content wasn't provided.
- **If assets were provided (question 5)** - save them into the `/assets/` folder and note in SKILL.md which steps reference them.

`mcp-instructions.md` template:
```markdown
# MCP & Tool Instructions for {skill-name}

## Locked Methods
These are the ONLY methods this skill uses. If a method fails, debug it - do not switch.

{connector entries}

## Known Failure Fixes
{pre-populated from requirements, or empty}

## Tool Failure Protocol
1. Read the error message carefully
2. Check Known Failure Fixes above first
3. If not listed: diagnose root cause of THIS tool - do not switch methods
4. Log the failure + fix here under Known Failure Fixes
5. Retry with fix applied
```

---

## Step 4 - Create Knowledge Base Files

The knowledge base is the skill's memory. It turns the skill into a compounding asset - the more it runs, the smarter it gets.

Every skill gets this self-improvement loop baked in:
```
GENERATE → EVALUATE (rubric) → ANALYZE FAILURES → STORE LESSONS → IMPROVE FUTURE RUNS → repeat
```

**`knowledge-base/good-examples.md`**
```markdown
# Good Examples - {skill-name}
Read at the start of every run to calibrate what "good" looks like.
When Claude gets something wrong, you write the correct answer here - this is the training data.

---

## [Date] - [Task]
**Output:** [the actual output]
**Why it worked:** [specific reason]
**Checks passed:** [e.g. 4 of 4]

---

## [Date] - [Task] ← CORRECTION
**What Claude did:** [the wrong output]
**Correct answer:** [what you wrote as the right answer]
**What to do differently:** [specific instruction]
```

**`knowledge-base/failure-log.md`**
```markdown
# Failure Log - {skill-name}
Every bad output gets logged here. The more data collected, the smarter the system becomes.

| Output | Failure Type | Root Cause | Fix / Lesson |
|--------|-------------|------------|--------------|
| [the bad output] | Generic / Too Broad / Low Curiosity / Wrong Format / etc. | [specific reason it failed] | [what to do differently] |
```

**`knowledge-base/lessons-learned.md`**
```markdown
# Lessons Learned - {skill-name}
General rules derived from failure patterns. Read at start of every run.

---

## Rule: [rule name]
**Pattern:** [what keeps going wrong]
**Rule:** [the fix, stated as a clear instruction]
**Added:** [date]
```

---

## Step 5 - Populate Examples with you

Once skill files are written, ask you:

> "Skill is built. To populate the examples, I can either:
> A) Run it live on a real task right now - you tell me if the output is right
> B) You give me examples directly - I'll ask you what makes them good or bad
> Which do you want, or both?"

**Path A - Live test run:**
1. Run the skill on a real task, show you the full output
2. Ask: "Does this look right? What would you change?"
3. Output approved → log to `knowledge-base/good-examples.md` with which checks it passed
4. Output wrong → you write the correct answer → log as CORRECTION entry
5. Process broke → fix SKILL.md, run again
6. You can request more runs - keep going until you're done

**Path B - you provide examples directly:**
1. You give a good example → ask "What makes this good? What specifically should I replicate?"
2. You give a bad example → ask "What's wrong with this? What should I have done instead?"
3. Log both with the explanation you gave

**Both paths feed the same files:** `knowledge-base/good-examples.md` and the Examples section in SKILL.md.

**Never:**
- Invent examples, fabricate outputs, make up leads or data
- Mark the skill as deployed before at least one example is logged
- Stop after one run if you want more

## Step 5.5 - The gate (a skill is not built until this passes)

```
python3 <this skill's folder>/code-scripts/check_skill.py <skill-name> --stamp
```

Three approved outputs from at least TWO different runs, plus one CORRECTION entry, or the skill stays
`status: draft` in its frontmatter. One example is an anecdote, not a definition of good.

A draft skill may be used, and **must say so when it runs**. It may NOT be marked done in any tracker, registered in your memory index as done, or described to you as finished. `--all` audits every skill.

Why this is a gate and not a step: Step 5 was an instruction for a long time and was skipped again and again.
The first audit found almost no skills actually finished. An
instruction inside the thing being skipped cannot enforce itself.

## Step 6 - Create CHANGELOG.md

```markdown
# Changelog - {skill-name}

## v1.0 - [date]
**Created.** Initial skill built via skill-builder.
- Objective: {one line}
- Process steps: {count}
- Connectors: {list or "none"}
- Reference files: {list or "none"}
- Assets: {list or "none"}

---

<!-- Every time SKILL.md is updated, log it here: -->
<!-- ## v1.X - [date] -->
<!-- **Changed:** [what changed and why - which failure or pattern triggered it] -->
```

Every time SKILL.md gets updated (new rule, process change, connector fix) → increment version in frontmatter + add entry here.

---

## Step 7 - Register it (optional)

If you keep a memory index (e.g. a MEMORY.md), add a one-line pointer to the new skill.

---

## Step 7.5 - Track it (optional)

If you keep a project tracker, add the skill with its proof files (SKILL.md, scripts). Mark it Building now while building, Built not tested once the files exist, and Built only after the Step 5 live test.

---

## Step 8 - Show you the Full SKILL.md for Review

Always show the complete generated SKILL.md before saving anything. Let you approve or request changes. Only write files after approval.

---

## Quick Checklist - Before a Skill is Done

Every skill must pass all of these before it's considered complete:

- [ ] Clear objective and success criteria defined
- [ ] Step-by-step process defined (with HITL + reference file + output format per step)
- [ ] Checks derived from success criteria, each answerable yes or no; the subjective pick is pairwise, never a 1-10 score
- [ ] Good & bad examples included (specific, tied to success criteria)
- [ ] Failure modes defined (specific, not generic)
- [ ] Solution Survey run on every fragile/expensive step - alternatives compared across layers, tradeoff shown to you, rejected options logged in mcp-instructions.md
- [ ] Connectors locked in (no improvisation when tools fail)
- [ ] **No secrets hardcoded** - every key/token/OAuth read from `~/.claude/keys.json` (or `~/.claude/*token*.json`), never inline in the skill
- [ ] Assets folder populated or confirmed not needed
- [ ] Reference files created or stubbed
- [ ] Progressive Updates section included
- [ ] Knowledge base created (all 3 files)
- [ ] `check_skill.py <name>` passes: 3 approved examples across 2+ runs, plus 1 correction
- [ ] Examples section populated from real run output (never invented), and `status: ready` in frontmatter
- [ ] CHANGELOG.md created with v1.0 entry
- [ ] Version number in SKILL.md frontmatter
- [ ] Registered in your memory index / tracker (if you use one), and its status matches reality
- [ ] Pipeline skills (multi-step, model or API calls): traced from day one, one trace per run, every step with its real input and output, checked before anyone reviews it (any tracing tool: Phoenix, Langfuse, LangSmith, or a plain JSON log)
- [ ] Pipeline skills that produce a list: one review sheet per list where a person marks approve/reject, linked both ways with the run's trace/report

**Remember: It's not about the perfect prompt. It's about the perfect system. Systems > Prompts.**

---

## Rules

1. Ask all questions upfront - never drip them one by one
2. Always call out HITL, reference file, and output format for every process step
3. Rubric dimensions must come from the success criteria - not invented
4. Progressive Updates section is mandatory in every skill
5. Connectors section must lock the method - never allow improvisation when a tool fails
5b. **Never hardcode a secret in a skill** - all API keys/tokens/OAuth read at runtime from the central `~/.claude/keys.json` (or `~/.claude/*token*.json`), keyed by service, so a leaked skill exposes nothing (see the Secrets & Credentials block under Section 3)
6. Failure modes must be specific ("never use X because Y") - not generic advice
7. Show full SKILL.md for review and get approval before saving any files
8. **Never invent examples** - good/bad examples only come from real test runs with you; leave the Examples section empty until Step 5 produces them
9. The Quick Checklist lives in the skill builder only - not in generated skills (the Testing & Iterating table covers it there)
10. **Solution Survey before locking any mechanism** - enumerate candidates across all layers (including build-first options like extensions, headless renders, direct APIs), compare reliability / speed / running cost / build effort, and let you choose. Never silently default to the zero-setup path.
11. **3+ patches on one mechanism = re-architect, not another rule** - re-run the Solution Survey on that step. This applies only in build/patch sessions; generated skills never explore alternatives at runtime.
12. **Pipeline skills are traced from day one.** One trace per run, code steps included, verified by a trace check.
13. **Lists get a review sheet, linked both ways.** Any list a pipeline produces (posts, hooks, scripts, leads) gets one review sheet where a person marks approve/reject with a note, and the sheet links back to the run's trace or report. Those labels become the test cases.
