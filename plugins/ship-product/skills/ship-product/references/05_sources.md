# Sources

Every claim in this skill is traceable. Check them rather than trusting the summary.

## The loop and the gates
- Claude Code best practices, "Give Claude a way to verify its work" - the verification loop, the
  four gate levels, "after the tenth approval you're clicking through rather than reviewing":
  https://code.claude.com/docs/en/best-practices
- Demystifying evals for AI agents - 20-50 cases, what a case holds, code vs LLM graders, "grade
  what the agent produced, not the path it took":
  https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Define your success criteria - eval-driven development:
  https://docs.anthropic.com/en/docs/build-with-claude/develop-tests

## The Description Chain
- AI Fluency for Builders - "user voice to requirement to technical spec to AI instruction to
  tests", "The builder is the translator at every step. AI cannot hear what the user did not
  say", "Tests are the most precise form of description", and Diligence: ship it, fix it, or stop
  it: https://academy.claude.com/courses/ai-fluency-for-builders

## Specs
- Spec Kit - the spec template and its "No implementation details" rule:
  https://github.com/github/spec-kit
- Kiro - requirements.md / design.md / tasks.md split: https://kiro.dev/docs/specs/
- Architecture decision records, Michael Nygard (2011) - decisions are superseded, never edited

## Error analysis and judges
- Hamel Husain, field guide: https://hamel.dev/blog/posts/field-guide/
- Hamel Husain, evals FAQ - the numbers, binary over Likert, the annotation tool requirements:
  https://hamel.dev/blog/posts/evals-faq/
- Criteria drift, Shankar et al.: https://arxiv.org/abs/2404.12272
- Eugene Yan, evaluating LLM evaluators - binary for objective, pairwise for subjective
- Li et al., arXiv 2601.03444 - the only head-to-head scale study: 0-5 best, 0-10 worst
- Zheng et al., MT-Bench - pairwise position bias, 50-70% preference for whatever is shown first
- AlignEval, Eugene Yan - the four-column labelling schema:
  https://eugeneyan.com/writing/aligneval/
- promptfoo web viewer - the matrix shape:
  https://www.promptfoo.dev/docs/usage/web-ui/

## Building discipline
- Kent Beck, augmented coding - unrequested functionality as a failure signal:
  https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes
- Nate Herk, ~300 discovery calls - map the process on paper first, 20% building / 80%
  understanding, "complexity kills and simplicity scales"
- Boris Cherny - aligning on the plan first "can two, three X success rates"; Anthropic Labs
  removed per-sprint evaluation in favour of one end-of-build QA pass after finding agents
  "confidently praising the work"
- Databricks - expert labels and critiques beat expert-written prompts by 30-50% agreement
