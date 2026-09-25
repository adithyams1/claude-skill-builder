# The two loops

Moved out of SKILL.md in v1.4. Read before Stage 5.

These are not the same loop, and confusing them is how a pipeline gets built step by step without
anyone reading one finished output end to end (a client: twenty skills, no finished month read).

| | **The spec loop** | **The eval loop** |
|---|---|---|
| Runs | once per piece of work | once per run of the whole pipeline |
| Stages | 1-4: spec, benchmark, build, check | 5-7: look, lock, re-test, decide |
| Triggered by | starting a new piece of work | a run finishing, however many features changed |
| Asks | did this piece do what the spec said | is the finished output any good |

A run gets read end to end even if nothing changed. A piece of work gets its own spec even if no
run has happened yet.
