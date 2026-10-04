# How the Claude Code team uses Claude Code: videos from Jul 6 – Oct 4, 2026

## How this was researched, and its limits
- **youtube.com, x.com and most podcast and transcript sites were blocked** from the research environment, so no video transcript was read directly.
- **Video content was rebuilt from three kinds of source:**
  - Search-engine summaries of show notes, host posts and third-party write-ups.
  - Pages on claude.com, anthropic.com and github.com, which could be fetched in full.
  - Publish timestamps decoded from the IDs of X posts.
- **Confidence labels used below:**
  - **[V]** = verified from a page fetched in full, or from a transcript on claude.com.
  - **[S]** = from summaries; it agrees across sources but is not confirmed against a transcript.
  - **[?]** = the date or the attribution is uncertain.

---

## 1. Video inventory (in window)

| Date | Video | Speaker(s) | Where | Confidence |
|---|---|---|---|---|
| Jul 6 | *The Origin Story of Claude Code* (oral history) | Boris Cherny, Sid, Cat Wu and others | YouTube `Mt0j7IS4qE4` | Date [S]; mostly history, not daily use |
| Jul 8 | *Designing Claude Code (and what's coming next)*, Dive Club | Meaghan Choi (Design Lead, Claude Code) | rss.com/podcasts/diveclub/2972105 | [S] |
| Jul 19 | *How I Plan, Build, and Run Loops with Claude Code in 40 Minutes*, Behind the Craft | Thariq Shihipar | creatoreconomy.so/p/how-i-plan-build-and-run-loops-with-claude-code-thariq-shihipar | [S] |
| Jul 20 | *The Creator of Claude Code on the Hottest Piece of Software in the World*, Bloomberg Odd Lots | Boris Cherny | bloomberg.com (2026-07-20) | [S] |
| Jul 21 | *Fireside Chat with Cat and Thariq*, AI Engineer World's Fair, published with a transcript by Simon Willison | Cat Wu, Thariq Shihipar | simonwillison.net/2026/Jul/21/cat-and-thariq/ · YouTube `uU5Gv2h8-9g` | [S]; recorded about Jul 1 |
| Jul 27 | *Boris Cherny: We Cut 80% of Claude Code's Prompt*, YC Startup School | Boris Cherny with Diana Hu | YouTube `qyPCVqFUyDo` · ycombinator.com/library/UN-boris-cherny-building-claude-code | [S], strong |
| Aug 11 | Webinar: *Claude Code for Data Engineering* | Anthropic data-engineering team | anthropic.com/webinars/claude-code-for-data-engineering | Agenda [V] |
| Aug 11 [?] | *How Anthropic uses Claude Code: Agentic Software Engineering at Scale*, NDC Copenhagen | Daisy Hollman | YouTube `shZgedW15vg` | Upload date [?] (talk given in June) |
| **Sep 2** | ***How the Claude Code team uses Claude Code*** (official, about 22 min) | Reportedly Thariq Shihipar and Sid Bidasaria [?] | YouTube `S-sYlFiGFv8` | Date [S]; content only from summaries |
| Sep 7 | *How Anthropic Builds And How Engineering Will Change Soon*, Peterman Pod | Thariq Shihipar | developing.dev/p/how-anthropic-builds-and-how-engineering | [S] |
| Sep 10 | Webinar: *Maximizing Value from Claude Code* | Lydia Hallie | anthropic.com/webinars/claude-code-maximizing-value | Agenda [V] |
| Sep 23 | *In Conversation with Boris Cherny*, Computer History Museum | Boris Cherny | computerhistory.org event · YouTube `djDt8J2_YVs` | Event date [V-ish]; few daily-use details |
| Sep 29 | *Claude Code's Next Era / Mods, Mutable Software & Multiplayer Agents*, Latent Space | Thariq Shihipar | latent.space/p/thariq | [S] |
| [?] | *Office Hours with Boris Cherny*: Ramp, DoorDash, Spotify, Stripe | Boris Cherny with customer CTOs | claude.com/office-hours · claude.com/customers/ramp-boris-office-hours | Ramp transcript [V]; date [?] (after June 9, featured Sep 30) |

**Probably outside the window, but often cited:**
- *How we Claude Code* (Thariq, Code w/ Claude, May 7, `IlqJqcl8ONE`)
- *Live coding with Boris & Jarred* (May 6)
- *Stop babysitting your agents* (Sid, May 19)
- Thariq's AIEWF keynote *Field Guide to Fable* (about Jul 1–3)
- Boris and Cat on Lenny's Podcast, Pragmatic Engineer, Every and Platformer (Feb–May 2026, or 2025)

**Written companions from Anthropic in the window [V]:**

| Date | Post |
|---|---|
| Jul 22 | Building verification loops with skills (Delba de Oliveira) |
| Aug 7 | Auto mode is now the default |
| Aug 14 | Maximizing the value of your Claude Code sessions (Lydia Hallie) |
| Aug 18 | Claude on call: Claude Tag as first responder for CI/CD |
| Sep 14 | Scaling test-impact analysis |
| Sep 17 | Projects redesigned |
| Sep 24 | Opus 5.5 and longer sessions |
| Oct 1 | Mods |

---

## 2. What the team actually does day to day (synthesis)

### A. They don't prompt; they build loops and workflows
- **Boris (Startup School, Ramp Office Hours [V]):**
  - "Use a workflow. That's it." Dynamic workflows let Claude plan and fan out subagents (sequence, parallel, fan-out, verify, summarize steps), which he calls "an algebra for agents".
  - "Loops are repetitive work, dynamic workflows are dynamic work."
  - He runs a `/loop` that babysits his PRs: it fixes CI and rebases them.
  - The team has **dozens of routines** (cloud cron jobs) for code review, PR babysitting, addressing feedback, and deleting dead code daily.
  - **CI speed-up [V]:** a dynamic workflow cut CI time from about 18 min to about 6 min at the median (P50). It profiled the CI runs, landed fixes, then scheduled itself a day later to read production data, and repeated this for days.
- **Thariq (Behind the Craft, Peterman Pod):**
  - "We've got /loop, /goal, and workflows."
  - Use `/goal` only when there is a **verifiable finish line**.
  - "Loop engineering" means building the system that prompts Claude rather than prompting it yourself.
  - Inside a loop, give Claude a safe default: log any deviation, pick the conservative option, keep going.
- **Daisy Hollman (NDC):**
  - Runs 20+ parallel sessions on separate git worktrees.
  - Uses agent teams through a send-message tool.
  - Uses `/loop` as a cron scheduler.
  - "Build the system that prompts itself."
  - Her NDC Oslo talk is titled *Build the loop, not the prompt*.

### B. Verification is the main skill
- **Boris:** verification "is probably the single most important thing that people do not get right." Give Claude "a hard task that seems a little bit too hard" *plus* a way to check its own work: a test suite, a pixel diff, opening a browser.
- **Team skill chain [V, Jul 22 post]:** "/code-review hunts for bugs, /simplify cleans up the diff, a /verify skill confirms end-to-end behavior, and a custom /design skill checks against guidelines in a DESIGN.md file if the change touched UI."
- **Boris, Sep 11 post:** production code written by Claude needs a *higher* bar than code written by a human. That means lots of lint rules and tests, Claude-driven end-to-end tests, daily Claude-run fuzzers, automated code review and security review, and automated refactoring.
- **Thariq:**
  - Aim for "~100× more testing code than you've ever had", with fixtures for everything.
  - Use separate creator and verifier subagents.
  - Have Claude quiz *you* before you merge.
- **Workshop repo, *How we Claude Code* [V]:** anthropics/cwc-workshops shows a "verifiable React" pattern:
  - Components emit `data-verify-*` attributes.
  - Fixtures are described with Zod schemas.
  - Each fixture gets an isolated route at `/verify/:unit/:fixture`.
  - `bun run verify` runs headless checks across all of them.

### C. Delete scaffolding with every new model
- **System prompt cut:** the team deleted **more than 80% of Claude Code's system prompt** for Opus 5 / Fable 5 with no regression on their evals. At each model release they strip the prompt and add lines back one at a time, keeping a line only if the model keeps making the mistake it fixes. (Boris and Thariq said this on several shows.)
- **Boris's advice to users:** "Every six months, delete your CLAUDE.md, delete your skills, delete your hooks, see what the model does."
- **Thariq on prompts:**
  - Examples and long "don't do X" lists now make results worse.
  - Keep CLAUDE.md to the repo's purpose plus gotchas Claude can't infer from the code.
  - Most CLAUDE.md files should probably be deleted.
- **Matching feature:** `/doctor prompt-audit` (v2.1.283, Sep 25) flags CLAUDE.md content written for older models.

### D. Claude Tag (Claude Code in Slack) is now the main interface
- **Cat and Thariq:** Tag lands about **65% of the Claude Code team's product-engineering PRs**.
- **Boris, Sep 25:** Tag writes more than 50% of his PRs every day and about 100% of his data analysis.
- **Swift rewrite:**
  - At Startup School, Boris started one Tag session asking it to rewrite the Electron desktop app in Swift, compare both apps pixel by pixel in a Mac VM, and "don't stop until you're done".
  - It ran for about 2 weeks.
  - It created its own Slack channel and posted progress screenshots there.
- **Experiments end to end [V, Ramp]:** Tag lands the PR, sets itself a reminder, checks that exposures are balanced, ramps the rollout, and ships the winning variant.
- **On-call [V, Aug 18 post]:**
  - Tag watches alert channels and fans out subagents across Grafana, PagerDuty, Kubernetes and Datadog.
  - It keeps a self-updating `lessons.md`.
  - It wrote the first situation report in every recent incident, median triage about 14 minutes.
- **Meaghan Choi (design):** she has moved "basically all" of her Claude chats into Slack via Tag.

### E. Auto mode everywhere
- **Inside Anthropic:** "Almost every single person uses auto mode" (Cat and Thariq). It has been the internal default since January 2026, and it is what makes Tag workable.
- **Incidents auto mode blocked [V, Aug 7 post]:**
  - An attempt to publish sensitive reports to a public site.
  - A mass process kill across about 2,000 pods.
  - Over-broad requests for admin permissions.

### F. From managing sessions to Projects
- **Boris (Sep 17):** "I stopped managing sessions. I just send thoughts as they come, Claude splits them into threads, and the project remembers how I work."
- **Lydia Hallie and Cat Wu** said the same.
- **Related feature:** fork mode is on by default, and forked subagents reuse the parent's prompt cache. Thariq says this makes supervisory checks almost free.

### G. Plan by interview, prototype in HTML
- **Thariq's sequence:**
  1. A "blind-spot pass": ask Claude what you don't know and where the traps are.
  2. "Interview me in depth using AskUserQuestion" to produce a spec; expect 30–40 questions.
  3. "Explore 4 different designs as HTML files", then react to real options before building.
- **Plans in HTML:** he uses HTML artifacts for plans instead of markdown.
- **Artifacts as shared memory:** for example, a Kanban artifact that several Claudes read and write.

### H. Context and cost hygiene (Lydia Hallie, webinar Sep 10 and post Aug 14) [V]
- **Clearing between tasks:** run `/clear` between tasks, and `/rename` the session first so you can find it later.
- **Choosing model and effort:** "Didn't know enough → bigger model; didn't try hard enough → more effort." Set both at the *start*, because switching mid-session busts the prompt cache.
- **Pointing at files:** use @-mentions instead of letting Claude search.
- **Noisy output:** send noisy commands to subagents.
- **Pruning context:** run `/context` once to see what CLAUDE.md and MCP servers add, and drop what you don't need.
- **Before a break:** run `/compact`, since the cache expires after 1 hour.
- **Prices:** cache reads cost 0.1× input; output costs about 5× input.

### I. Harness customization (Thariq, Latent Space; Oct 1 launch)
- **Mods** are TypeScript functions that run inside Claude Code: they rewrite prompts, gate tools and add UI. Thariq calls this "mutable software".
- **AGENTS.md fallback** was reportedly built as a mod.
- **"You should know"** is a built-in mod: a side agent that flags issues you missed.

### J. Scale numbers they cite
| Figure | Source |
|---|---|
| About 90% or more of Claude Code's code is written by Claude Code | [S] |
| Boris has written no code by hand in 2026 | [S] |
| Boris ships dozens of PRs a day, often from the phone app; his record is 150 in one day (earlier coverage) | [S] |
| Anthropic engineers ship 8× more code per quarter than in 2021–25, about 80% of it written by Claude | [V] |
| CI jobs grew 25× in 6 months | [V] |
| Bun was rewritten from Zig to Rust in 11 days: about 50 workflows, up to 64 concurrent agents, adversarial reviewer agents, about $165K in API cost | Jarred Sumner post, Jul 8 [S] |
| Opus 5.5 became Boris's daily driver by Sep 22. He chose it over Fable 5.1 for speed and cost: an HAProxy C-to-Rust port took 9.5 h vs 12 h at 51% lower cost | [S] |

---

## 3. How their workflow changed compared with before July
| Before (Feb–Jun 2026) | Now (Jul–Oct 2026) |
|---|---|
| Add a CLAUDE.md rule after every mistake | Delete CLAUDE.md, skills and hooks regularly, and re-add only what's needed |
| 5–10 terminal and web sessions, plan mode first | Projects and Tag split the work into threads; auto mode by default |
| `/loop` and routines for PR babysitting | Dynamic workflows ("use a workflow") for multi-day and multi-week jobs |
| Claude Code in the terminal or on the phone | Slack (Tag) as the main place work gets started |
| Prompt engineering | Verification engineering: tests, pixel diffs, fuzzers, review skills |

---

## 4. Takeaways to apply
1. **Before writing a prompt, decide how Claude will check its own work** (tests, a screenshot diff, `/verify`), then hand over a task that's slightly too big.
2. **Chain review skills on every change:** `/code-review` → `/simplify` → `/verify` (→ `/design` against a DESIGN.md).
3. **Audit CLAUDE.md** with `/doctor prompt-audit`. Cut examples and "don'ts", and keep only gotchas Claude can't infer.
4. **For big or repetitive work, say "use a workflow"** or set up a `/loop` or routine, rather than steering it turn by turn.
5. **Plan by interview:** do a blind-spot pass, then have Claude interview you with AskUserQuestion, then compare HTML prototypes.
6. **Run in auto mode**, and use Projects or Tag to work across many threads instead of managing sessions yourself.
7. **Watch the cache:** pick model and effort up front, `/clear` between tasks, and push noisy output to subagents.

---

## 5. Open gaps
- **The Sep 2 video (`S-sYlFiGFv8`):** neither its transcript nor its speakers could be confirmed. The points summarized for it overlap heavily with Thariq's other talks.
- **Exact quotes:** they still need checking against the full transcripts at simonwillison.net (Jul 21), developing.dev (Sep 7), latent.space (Sep 29) and spoken.md (Startup School).
- **Unconfirmed upload dates:** Daisy Hollman's NDC video, the CHM recording, and the Office Hours episodes.
- **Possible misses:** search limits may have hidden appearances by Sid Bidasaria, Adam Wolff, Dickson Tsai and Noah Zweben in the window.
