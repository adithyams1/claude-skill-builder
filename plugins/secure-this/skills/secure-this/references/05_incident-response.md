# Incident Response - what to do if it actually happened

Every hardening report ends with this block, filled in for the specific workflow.
A control plan with no recovery plan is half a plan.

## Signals that an injection may have landed

- The agent took an action nobody asked for, especially a network call or a write
- A tool result mentions instructions, roles, or "ignore previous"
- An unexplained diff in `MEMORY.md`, a skills folder, or a settings file
- Egress to a domain not on the allowlist appearing in logs
- A run that took materially longer or made far more calls than usual
- The agent's summary and the underlying artifact disagree

## Immediate steps, in order

1. **Stop the loop.** Kill the session and any scheduled job (cron, LaunchAgent, systemd timer) that
   would restart it. Do this before investigating - the loop compounds.
2. **Snapshot before touching anything.** Copy the transcript and any audit log
   somewhere the agent cannot write.
3. **Assume every credential in reach was read.** Rotate them. Not the ones you
   think were touched - everything the asset inventory listed under "Holds."
4. **Check the persistence sinks first**, because these survive: `MEMORY.md`,
   the skills directories (BOTH stores), settings.json, hooks, any MCP config,
   any vector store or notes DB the workflow writes to.
5. **Check egress logs** for what actually left, over the whole session, not
   just around the suspicious step. Legs of the trifecta split across time.
6. **Check downstream artifacts**: drafts created, files shared, DB rows written,
   messages queued. Anything staged for later human approval is now suspect.

## Then

- Re-run secure-this on the workflow. The gate that failed is the finding.
- Log it to `knowledge-base/failure-log.md` with root cause, and to your own
  lessons file if a fresh session would walk into it again.
- If the entry vector was a dependency, treat every other workflow using that
  dependency as affected.

## Kill switch

Every unattended workflow needs a documented way to stop it that does not require
reading this file first. Name it explicitly in the report: the scheduler job name,
its config file path, or the queue file to empty.
