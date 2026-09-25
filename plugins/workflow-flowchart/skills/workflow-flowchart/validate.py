#!/usr/bin/env python3
"""
validate.py - run the Layer 1 hard gates against a generated flowchart.

Checks the FINAL rendered file, not the source data, so it catches anything that
went wrong during template filling too.

    python3 validate.py workflows/<slug>/<slug>-flows.html

Exit 0 = all gates pass, safe to smoke test and publish.
Exit 1 = at least one gate failed, listed with the flow and node it came from.

This does NOT replace the smoke-test screenshot in step 9. It catches structural
faults; only the render catches visual ones (overflow, leftover client strings,
tangled edges). Run both.
"""

import re
import sys
from pathlib import Path

ICONS = set("""mic cam ig li fb mail cal ai person gate doc db search chart form frame
asana notion drive code clock img send bank tag sked""".split())

ROLES = {"inp", "ai", "human", "tool", "gate", "out"}

SUB_MAX = 40          # sub-labels longer than this overflow the node box
FLOW_MAX = 18         # past this a flow stops being readable
BANNED_TAGS = ["<!doctype", "<html", "<head", "<body"]


def flows_in(src):
    """Split the BUILDS array into one blob per flow. Regex is fine here: the
    template's shape is locked, so we are not parsing arbitrary JS."""
    m = re.search(r'const BUILDS=\[(.*?)\n?\];', src, re.S)
    if not m:
        return None
    body = m.group(1)
    return re.split(r'\n\s*\n(?=\{id:")', body)


def check(path):
    src = Path(path).read_text()
    errs, warns = [], []

    # --- whole-file gates ------------------------------------------------
    if "{{" in src:
        for ph in set(re.findall(r'\{\{(\w+)\}\}', src)):
            errs.append(f"unfilled placeholder {{{{{ph}}}}}")
    low = src.lower()
    for t in BANNED_TAGS:
        if t in low:
            errs.append(f"document tag {t} present - Artifact wraps the page itself")
    if re.search(r'(src|href)=["\']https?://(?!claude\.ai)', src):
        warns.append("external URL in a src/href - CSP will block it unless it is a link")

    # Each template marker is followed by an EMPTY default declaration, so filling the
    # marker instead of replacing the marker+default PAIR declares the identifier twice.
    # The whole script block then fails to parse and the diagram renders blank, with no
    # console error and every other gate passing.
    for ident in ("BUILDS", "ENGINES", "ATTACH", "FOUND"):
        n = len(re.findall(r'\bconst\s+' + ident + r'\s*=', src))
        if n > 1:
            errs.append(f"const {ident} declared {n} times - replace the marker AND the "
                        f"default line after it, not just the marker. The script will not "
                        f"parse and the diagram will be blank.")

    blobs = flows_in(src)
    if blobs is None:
        errs.append("could not find the BUILDS array")
        return errs, warns, {}

    # --- per-flow gates --------------------------------------------------
    seen_ids, counts = set(), {}
    for blob in blobs:
        num = re.search(r'num:"([^"]+)"', blob)
        fid = re.search(r'\{id:"(\w+)"', blob)
        if not (num and fid):
            continue
        num, fid = num.group(1), fid.group(1)
        seen_ids.add(fid)

        coords, ids = {}, set()
        for m in re.finditer(
                r'n\("(\w+)",\s*(\d+),\s*(\d+),\s*"(\w+)",\s*"(\w+)",\s*"([^"]*)",\s*"([^"]*)"',
                blob):
            nid, c, r, role, icon, label, sub = m.groups()
            ids.add(nid)
            if (c, r) in coords:
                errs.append(f"{num}: nodes '{coords[(c,r)]}' and '{nid}' both at ({c},{r})")
            coords[(c, r)] = nid
            if role not in ROLES:
                errs.append(f"{num}.{nid}: role '{role}' is not one of {sorted(ROLES)}")
            if icon not in ICONS:
                errs.append(f"{num}.{nid}: icon '{icon}' not in the IC library - renders blank")
            if len(sub) > SUB_MAX:
                warns.append(f"{num}.{nid}: sub-label {len(sub)} chars, will overflow (max {SUB_MAX})")

        n_edges = 0
        for m in re.finditer(r'e\("(\w+)",\s*"(\w+)"', blob):
            n_edges += 1
            for side, x in zip(("from", "to"), m.groups()):
                if x not in ids:
                    errs.append(f"{num}: edge {side} '{x}' is not a node in this flow")

        if len(ids) > FLOW_MAX:
            warns.append(f"{num}: {len(ids)} nodes, over the {FLOW_MAX} readability ceiling - split it")
        if not ids:
            errs.append(f"{num}: no nodes")
        counts[num] = (len(ids), n_edges)

    # --- groups reference real flows -------------------------------------
    g = re.search(r'const ENGINES=\[(.*?)\n?\];', src, re.S)
    if g:
        for gid in re.findall(r'"(\w+)"', re.sub(r'(name|tag|color):"[^"]*"', '', g.group(1))):
            if gid not in seen_ids and not gid.startswith("var"):
                errs.append(f"group references flow id '{gid}' which does not exist in BUILDS")
        grouped = set(re.findall(r'ids:\[([^\]]*)\]', g.group(1)))
        flat = {x for chunk in grouped for x in re.findall(r'"(\w+)"', chunk)}
        for fid in seen_ids - flat:
            warns.append(f"flow '{fid}' is in BUILDS but in no group - it will not appear in the sidebar")
    return errs, warns, counts


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: validate.py <flowchart.html>")
    p = Path(sys.argv[1]).expanduser()
    if not p.exists():
        sys.exit(f"no such file: {p}")

    errs, warns, counts = check(p)
    for num, (n, e) in counts.items():
        print(f"  {num:4} {n:>2} nodes  {e:>2} edges")
    if warns:
        print("\nWARNINGS (not blocking):")
        for w in warns:
            print(f"  ~ {w}")
    if errs:
        print(f"\nFAILED - {len(errs)} gate error(s):")
        for e in errs:
            print(f"  x {e}")
        sys.exit(1)
    print(f"\nPASS - {len(counts)} flows, all hard gates clear.")
    print("Still run the smoke-test screenshot. This does not catch visual faults.")


if __name__ == "__main__":
    main()
