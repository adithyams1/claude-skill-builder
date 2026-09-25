# Good Examples - secure-this
Read at the start of every run to calibrate what "good" looks like.
When Claude gets something wrong, the user writes the correct answer here - this is the training data.

Format per entry: target, grade before and after, confidence, verdict, what made it good,
what is worth reusing. Populate from your own real runs only. Never invent an example.

---

## Example (anonymized): swapping a third-party scraper in a web app
**Target:** replacing one hosted scraping service with a lesser-known community alternative inside a small Python web app.
**Grade:** C before, B after applying Model B. Verdict GAPS FOUND, then bounded.
**What made it good:** tested instead of assumed. A harmless probe showed the download helper accepted `file://` URLs and followed redirects to any host, and reading the code showed an API token being appended to any URL that merely contained the vendor's hostname. Both gaps were pre-existing; the swap only raised their likelihood, and the report said so plainly.
**Worth reusing:** stage the controls as copies, then test the staged code against every probe plus a forced fallback before asking for approval. That test caught a real break (the vendor rejected a spend cap below its minimum) that a diff review alone would have shipped.
