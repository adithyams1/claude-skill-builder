# Failure Log - workflow-flowchart

Every bad output gets logged here, one row per failure. The more data collected, the
smarter the skill becomes.

| Output | Failure Type | Root Cause | Fix / Lesson |
|---|---|---|---|
| Template rendered a previous client's name in the sidebar during a smoke test with unrelated data | Wrong Format | The h1 and tag line were hardcoded in the HTML shell, outside the parameterised data block | Added `{{HEADER}}` and `{{SUBHEADER}}` markers. Caught only by the local smoke-test screenshot, which is why the smoke test is mandatory |
| Title rendered literally as `/*Template smoke test*/` | Wrong Format | The marker was written as `/*{{TITLE}}*/` so the JS comment syntax leaked into the `<title>` tag | Markers inside HTML (not JS) must be bare `{{NAME}}` with no comment wrapper |
