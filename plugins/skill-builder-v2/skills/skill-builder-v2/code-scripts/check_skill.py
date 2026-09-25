#!/usr/bin/env python3
"""
check_skill.py - is this skill actually finished, or does it just look finished?

    python3 check_skill.py <skill-name>        one skill, prints why it fails
    python3 check_skill.py --all               every skill, a table
    python3 check_skill.py <skill> --stamp     also write status: draft or ready into the frontmatter

The bar: a skill is not built until its knowledge base holds THREE approved
outputs from at least TWO different runs, plus ONE correction showing something it got wrong and
what the right answer was. One example is not a definition of good; it is an anecdote.

ATTRIBUTED examples. Most steps in a chain produce something no human can judge
on its own - nobody can say whether a middle step's intermediate output is "right". Demanding three directly
approved examples for every such step is more labelling than anyone can meaningfully do. So an entry headed "<- ATTRIBUTED" counts as approved, on one condition: it names, on a
"From:" line, the end output whose labelling pass produced it. The evidence is still real and still
labelled by a person; it just arrives from the end of the chain rather than from the middle. Two
attributed examples from the same end output count as one source, exactly as two examples from one
run count as one run.

Everything checked here was already in skill-builder as an instruction and was skipped again and again,
because an instruction inside the thing being skipped cannot enforce itself.
Exit 0 passes, exit 1 fails.
"""

import argparse
import re
import sys
from pathlib import Path

SKILLS = Path.home() / ".claude" / "skills"
MEMORY = Path.home() / ".claude" / "projects" / "<your-project>" / "memory" / "MEMORY.md"
NEED_APPROVED, NEED_RUNS, NEED_CORRECTIONS = 3, 2, 1
PLACEHOLDERS = ("Populated from live test runs", "After first approved test run", "{skill name}",
                "{one line}", "[the actual output]", "[the bad output]", "TBD")


def entries(kb):
    """Every ## entry in good-examples.md, split into approved and corrections, with their dates.

    An approved entry also carries where it came from: its own run date, or, for an ATTRIBUTED
    entry, the end output named on its "From:" line. That value is what "different runs" counts."""
    if not kb.exists():
        return [], [], []
    text = kb.read_text()
    approved, corrections, bad = [], [], []
    for m in re.finditer(r"^##\s+(.+?)$(.*?)(?=^##\s|\Z)", text, re.S | re.M):
        head, body = m.group(1), m.group(2)
        if len(body.strip()) < 40:          # a heading with nothing under it is not an example
            continue
        date = re.search(r"(\d{4}-\d{2}-\d{2})", head)
        row = {"head": head.strip(), "date": date.group(1) if date else None}
        if "CORRECTION" in head.upper():
            corrections.append(row)
            continue
        if "ATTRIBUTED" in head.upper():
            src = re.search(r"^\s*\**From:\**\s*(.+?)\s*$", body, re.M)
            if not src:
                bad.append(f'attributed example "{row["head"][:44]}" has no "From:" line naming '
                           f"the end output its labelling pass came from")
                continue
            row["source"] = src.group(1).strip()
        else:
            row["source"] = row["date"]
        approved.append(row)
    return approved, corrections, bad


def check(name):
    """Two kinds of failure, kept apart: EVIDENCE (this skill was never proven) and TIDY (it was
    proven but the file is untidy). Both block, but only one of them is real work."""
    d = SKILLS / name
    fails, warns, tidy = [], [], []
    skill = d / "SKILL.md"
    if not skill.exists():
        return ["no SKILL.md"], [], {"tidy": []}
    text = skill.read_text()

    fm = re.match(r"^---\n(.*?)\n---", text, re.S)
    front = fm.group(1) if fm else ""
    for key in ("name:", "description:", "version:"):
        if key not in front:
            tidy.append(f"frontmatter has no {key.rstrip(':')}")

    approved, corrections, bad = entries(d / "knowledge-base" / "good-examples.md")
    fails.extend(bad)
    runs = {a["source"] for a in approved if a.get("source")}
    if len(approved) < NEED_APPROVED:
        fails.append(f"{len(approved)} approved examples, needs {NEED_APPROVED}")
    if len(runs) < NEED_RUNS and len(approved) >= NEED_APPROVED:
        fails.append(f"all examples come from {len(runs) or 'no dated'} source(s), needs {NEED_RUNS} different "
                     f"runs (or, for attributed examples, {NEED_RUNS} different end outputs)")
    if len(corrections) < NEED_CORRECTIONS:
        fails.append(f"{len(corrections)} corrections, needs {NEED_CORRECTIONS} (what it got wrong, and the right answer)")

    body = re.sub(r"^---\n.*?\n---", "", text, flags=re.S)
    left = [p for p in PLACEHOLDERS if p in body]
    if left:
        tidy.append(f"SKILL.md still has template text: {left[0][:40]}")

    for f in ("CHANGELOG.md", "knowledge-base/failure-log.md", "knowledge-base/lessons-learned.md"):
        if not (d / f).exists():
            tidy.append(f"no {f}")
    if re.search(r"^## Connectors", body, re.M) and "none" not in body.split("## Connectors")[1][:300].lower():
        if not (d / "references" / "mcp-instructions.md").exists():
            warns.append("has connectors but no references/mcp-instructions.md")
    try:
        if name not in MEMORY.read_text():
            warns.append("not registered in MEMORY.md")
    except OSError:
        pass
    return fails, warns, {"approved": len(approved), "runs": len(runs), "corrections": len(corrections),
                          "tidy": tidy}


def stamp(name, ok):
    """Write the verdict where a run will see it: status: ready or status: draft."""
    p = SKILLS / name / "SKILL.md"
    t = p.read_text()
    want = "ready" if ok else "draft"
    if re.search(r"^status:\s*\w+", t, re.M):
        t = re.sub(r"^status:\s*\w+", f"status: {want}", t, count=1, flags=re.M)
    else:
        t = re.sub(r"^(version:.*)$", rf"\1\nstatus: {want}", t, count=1, flags=re.M)
    p.write_text(t)
    return want


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--stamp", action="store_true")
    o = ap.parse_args()
    names = sorted(p.name for p in SKILLS.glob("*") if (p / "SKILL.md").exists()) if o.all else [o.skill]
    if not names or names == [None]:
        sys.exit("name a skill, or --all")
    bad = 0
    for n in names:
        fails, warns, c = check(n)
        tidy = c.get("tidy") or []
        ok = not fails and not tidy
        bad += not ok
        if o.stamp:
            stamp(n, ok)
        if o.all:
            mark = "PASS" if ok else ("EVIDENCE" if fails else "TIDY")
            print(f'{mark:<9}{n:<34} {c.get("approved", 0)} examples / '
                  f'{c.get("runs", 0)} runs / {c.get("corrections", 0)} corrections'
                  + ("" if ok else f'   <- {(fails or tidy)[0]}'))
        else:
            print(f'{n}: {"PASS, this skill is finished" if ok else "FAIL, this skill is not finished"}')
            for f in fails:
                print(f"  not proven: {f}")
            for f in tidy:
                print(f"  untidy: {f}")
            for w in warns:
                print(f"  warn: {w}")
    if o.all:
        print(f"\n{len(names) - bad} of {len(names)} skills are actually finished.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
