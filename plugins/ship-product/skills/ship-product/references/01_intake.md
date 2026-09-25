# Stage 0 - The intake ask

The Description Chain starts at **user voice**, not at technical spec. Everything downstream is a
translation of what the person who owns the requirements actually said, so if this step is skipped
the whole chain is built on a guess.

## Two asks, kept separate

- **Ask A goes to whoever owns the process** (Client example: the agency's founder and its
  content lead). How they work, what
  good means, what breaks.
- **Ask B is the client-facing form**, if one exists. It stays short and it never asks the client
  to do work that is ours. Client example, the owner on their old 11-question survey: *"a few of them ask
  clients to do our job"* - trends and competitor analysis. Clients skipped it.

## The eight slots

| # | Slot | What it unlocks | Make it concrete by |
|---|---|---|---|
| 1 | A screen recording of one real run, start to finish, thinking out loud. 30-45 min, Loom, messy is fine | The process map. You cannot automate a process you have never watched | Naming the specific decisions to narrate: how they choose inputs, what they reject, where they stop |
| 2 | The actual inputs they used for that run, not the idea of them | Whether input selection is itself a skill or just a list | Asking for the real handles / URLs / rows |
| 3 | 3 outputs they approved and 2 they rejected, one line each on why | The benchmark seed and the `good-examples.md` seed | Asking for their words, not a rating |
| 4 | 5 things they looked at and did NOT use, and why | Rejections carry more signal than approvals, and rejection is usually what the pipeline is trying to reproduce | Asking for the reason per item, not a list |
| 5 | Three numbers: volume that actually ships, options they want to choose between, hours it takes today | Settles scope, and gives the only honest ROI baseline | Asking for three numbers, explicitly |
| 6 | The one thing they rewrite every single time | A failure taxonomy before anything has run. The cheapest error analysis available | "Name it, even if it's small" |
| 7 | The 3 things they check before it goes out, and the one thing that gets it sent back | Success criteria and the must-never-happen list, in their words. Becomes the first judge questions | Never asking "it's good if ___" - nobody can answer that |
| 8 | What the client actually receives today, and what they do with it in the first hour | The outcome being bought, which decides how much gets built | Asking what they do next, never what we hand over |

Items 3, 4 and 6 convert directly into benchmark cases. Items 5 and 8 decide how much gets built:
5 is the volume, 8 is the outcome. A build sized from 5 alone still builds the wrong thing, larger.

## Rules for writing the ask

- **Paste-ready**: one fenced block, one unbroken line per paragraph, no markdown inside.
- **Every question answerable in a sentence.** A question that needs an essay comes back empty.
- **Ask for artifacts, not opinions.** "The five you skipped" beats "how do you evaluate them".
- **Say what you are NOT asking for**, so they do not do our work.
- **One recording plus one sitting.** If the ask looks like homework, it does not come back.

## The template

Adapt every slot to the product. Fill every <slot>; never send a placeholder.

```
Hey <name>, to build this properly I need a few things from you that I can't get from the files. It's one recording plus one sitting, and it replaces a lot of guessing on my end.

1. A screen recording of one real <run>, start to finish, thinking out loud as you go. I want to see how you choose <inputs>, how you decide what is worth keeping, and where you stop. 30 to 45 minutes, Loom is fine. Messy is better than polished.

2. The actual <inputs> you used for that run. The real ones, not the idea of them.

3. Three finished <outputs> you approved, and two you rejected. One line on each: why it worked, or why it didn't.

4. Five <candidates> you looked at and skipped, with the reason for each. The ones that didn't make the cut tell me more than the winners do.

5. Three numbers. How many <outputs> actually get used per <period>. How many options you want to choose between. And roughly how many hours this takes you today.

6. The one thing you end up rewriting every single time. Name it, even if it's small.

7. The three things you check before it goes out, and the one thing that would make you send it back.

8. When you send this to a client today, what do they actually get, and what do they do with it in the first hour? And if you could only give them one thing out of the whole <run>, what would it be?

Nothing here is research that's my job to do. This is all about how you already work.
```

The worked example below is the ask as it was actually sent, before slot 8 existed. It is a record,
not a template: never back-fill it.

### Worked example (a client, a content agency making Instagram reels for clients)

Names swapped for roles:

```
Hey <founder>, to build this properly I need a few things from you and <content lead> that I can't get from the files. It's one recording plus one sitting, and it replaces a lot of guessing on my end.

1. A screen recording of one real month, start to finish, thinking out loud as you go. the most recent client, whichever is freshest. I want to see how you choose the 20 accounts, how you decide which reels are worth modelling, how you decide what gets swapped for the client, and where you stop. 30 to 45 minutes, Loom is fine. Messy is better than polished.

2. The actual account list you used for that client. The real handles, not the idea of 20 accounts.

3. Three finished pieces from a recent month that <content lead> approved, and two they rejected. One line from them on each: why it worked, or why it didn't.

4. Five reels you looked at and skipped, with the reason you skipped each one. The ones that didn't make the cut tell me more than the winners do.

5. Three numbers. How many pieces actually get filmed and posted per client per month. How many options per topic you want to choose between. And roughly how many hours the whole month takes you today, per client.

6. The one thing you end up rewriting every single month. Name it, even if it's small.

7. The three things <content lead> checks before a month goes out to a client, and the one thing that would make them send it back to you.

No trends, no competitor research, nothing that's your job to do. This is all about how you already work.
```

## What lands on disk

`INTAKE.md` next to the product, holding the answers verbatim plus a link to the recording. Never
paraphrased: the point of this file is that it is in their words.

Anything not answered becomes an **open question in section 7 of the spec**, with the assumption
being used meanwhile written beside it. Never a guess.

**Evidence:** Databricks measured experts labelling and explaining as 30-50% better than experts
editing prompts. Nate Herk, from ~300 discovery calls: *"if you can't explain a process clearly on
paper and get alignment with your client or your team, then there's no way you can go automate
that process."*
