#!/usr/bin/env python3
"""
check_spec.py - does this SPEC.md actually say anything, or does it just have the headings?

    python3 check_spec.py <path to SPEC.md>      one spec, prints why it fails
    python3 check_spec.py <folder>               finds SPEC.md inside it

The bar: all nine sections present AND filled. Non-goals and open questions
are the two that get left empty, and they are the two that would have caught this year's
problems, so they carry extra checks of their own.

Exit 0 passes, exit 1 fails. This is what you run before letting a project leave
"not started" - a rule in a prompt is a suggestion, a rule in the tool is a restriction.
"""

import re
import sys
from pathlib import Path

SECTIONS = [
    ("the job", "one sentence saying what this is and who it is for"),
    ("what it produces", "the exact deliverables and how many"),
    ("inputs", "each one named, with where it comes from"),
    ("success criteria", "measurable, and stated without naming a tool"),
    ("non-goals", "at least one thing this deliberately does not do"),
    ("assumptions", "the default chosen wherever nobody said"),
    ("open questions", "what is still needed, each with the assumption running meanwhile"),
    ("budget", "hours, model cost, and the dumbest version that would work"),
    ("decisions", "dated lines: what was chosen, what was rejected, why"),
]

PLACEHOLDER = re.compile(r"^(tbd|todo|n/?a|none yet|\.\.\.|-)\s*$", re.I)
MIN_CHARS = 25          # a heading with three words under it is not a section


def body(text, name):
    """Everything under the heading that contains `name`, up to the next heading of any level."""
    pat = re.compile(r"^#{1,4}\s*(?:\d+\.\s*)?.*" + re.escape(name) + r".*$", re.I | re.M)
    m = pat.search(text)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^#{1,4}\s", rest, re.M)
    return (rest[:nxt.start()] if nxt else rest).strip()


def check(path):
    text = Path(path).read_text()
    fails = []
    for name, wants in SECTIONS:
        b = body(text, name)
        if b is None:
            fails.append(f"no section for '{name}' - needs {wants}")
            continue
        # strip the template's own italic guidance so a spec cannot pass on instructions alone
        real = re.sub(r"^\s*[*_].*[*_]\s*$", "", b, flags=re.M).strip()
        if not real or PLACEHOLDER.match(real) or len(real) < MIN_CHARS:
            fails.append(f"'{name}' is empty - needs {wants}")

    # The two that get skipped, and the two that matter most.
    ng = body(text, "non-goals") or ""
    if ng and len(ng) >= MIN_CHARS and not re.search(r"\bnot\b|\bno\b|\bnever\b|\bwithout\b", ng, re.I):
        fails.append("'non-goals' does not say what is NOT being done - name at least one thing")

    oq = body(text, "open questions") or ""
    if oq and len(oq) >= MIN_CHARS and not re.search(r"assum", oq, re.I):
        fails.append("'open questions' has no assumption beside the questions - "
                     "every open question needs the assumption running meanwhile")

    return fails


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: check_spec.py <path to SPEC.md or its folder>")
    p = Path(sys.argv[1]).expanduser()
    if p.is_dir():
        p = p / "SPEC.md"
    if not p.exists():
        print(f"FAIL: no spec at {p}")
        print("  nothing gets built without one. Run /ship-product to write it.")
        sys.exit(1)

    fails = check(p)
    if not fails:
        print(f"{p}: PASS, all nine sections are filled")
        sys.exit(0)
    print(f"{p}: FAIL, this spec is not finished")
    for f in fails:
        print(f"  {f}")
    sys.exit(1)


if __name__ == "__main__":
    main()
