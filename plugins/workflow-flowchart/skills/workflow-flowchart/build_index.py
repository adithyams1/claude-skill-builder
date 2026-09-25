#!/usr/bin/env python3
"""
build_index.py - regenerate the workflows directory from disk.

Every diagram this skill produces is filed at:

    <workflows>/<slug>/
        <slug>-flows.html   the artifact source, self-contained
        meta.json           who it is for, when, what is in it

This script walks those folders and rewrites <workflows>/index.html.

<workflows> is, in order of precedence: the --root argument, the WORKFLOWS_DIR
environment variable, or ./workflows in the current working directory.
Disk is the source of truth - delete a folder and it leaves the index on the
next run. Nothing is ever written back into a <slug>/ folder from here.

    python3 build_index.py            # rebuild
    python3 build_index.py --open     # rebuild and open in the browser
    python3 build_index.py --root ~/workflows
"""

import json
import os
import sys
import html
import webbrowser
from pathlib import Path
from datetime import datetime

def _root_from_args():
    args = sys.argv[1:]
    if "--root" in args:
        i = args.index("--root")
        if i + 1 < len(args):
            return args[i + 1]
        sys.exit("usage: build_index.py [--root <dir>] [--open]")
    return os.environ.get("WORKFLOWS_DIR") or "workflows"


ROOT = Path(_root_from_args()).expanduser().resolve()
INDEX = ROOT / "index.html"
REGISTRY = ROOT / "registry.json"


def load():
    """One entry per <slug>/meta.json. A folder without one is skipped, not guessed at."""
    out = []
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir():
            continue
        m = d / "meta.json"
        if not m.exists():
            print(f"  skip {d.name}: no meta.json")
            continue
        try:
            e = json.loads(m.read_text())
        except Exception as ex:
            print(f"  skip {d.name}: bad meta.json ({ex})")
            continue
        e["slug"] = d.name
        src = d / f"{d.name}-flows.html"
        e["local"] = str(src) if src.exists() else None
        out.append(e)
    out.sort(key=lambda e: e.get("created", ""), reverse=True)
    return out


CSS = """
:root{--ground:#EDF0F5;--surface:#fff;--ink:#121824;--ink-soft:#4b5666;--ink-faint:#8892a3;
--line:#ccd5e2;--ai:#1f8f9c;--gate:#8a52c4;--out:#2f8a52;--human:#c07a1f;--tool:#4560c8;}
@media (prefers-color-scheme:dark){:root{--ground:#12151c;--surface:#1b202a;--ink:#eef2f8;
--ink-soft:#a7b1c1;--ink-faint:#6f7b8d;--line:#2c3442;}}
:root[data-theme=dark]{--ground:#12151c;--surface:#1b202a;--ink:#eef2f8;--ink-soft:#a7b1c1;
--ink-faint:#6f7b8d;--line:#2c3442;}
:root[data-theme=light]{--ground:#EDF0F5;--surface:#fff;--ink:#121824;--ink-soft:#4b5666;
--ink-faint:#8892a3;--line:#ccd5e2;}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
font:15px/1.5 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif;padding:40px 28px 80px}
.wrap{max-width:1080px;margin:0 auto}
h1{font-size:30px;margin:0 0 4px}
.sub{color:var(--ink-faint);margin:0 0 30px;font-size:14px}
.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}
.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px 18px 15px;
display:flex;flex-direction:column;gap:10px}
.top{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}
.nm{font-weight:650;font-size:17px;line-height:1.25}
.badge{font-size:11px;font-weight:650;letter-spacing:.04em;text-transform:uppercase;
padding:3px 8px;border-radius:99px;white-space:nowrap}
.client{background:color-mix(in srgb,var(--out) 16%,transparent);color:var(--out)}
.prospect{background:color-mix(in srgb,var(--human) 18%,transparent);color:var(--human)}
.note{color:var(--ink-soft);font-size:13.5px;margin:0}
.stats{display:flex;flex-wrap:wrap;gap:6px;margin-top:2px}
.st{font-size:11.5px;color:var(--ink-soft);border:1px solid var(--line);border-radius:6px;padding:2px 7px}
.acts{display:flex;gap:8px;margin-top:auto;padding-top:6px}
a.btn{flex:1;text-align:center;text-decoration:none;font-size:12.5px;font-weight:600;
padding:8px 10px;border-radius:8px;border:1px solid var(--line);color:var(--ink-soft);background:transparent}
a.btn.pri{background:var(--ai);border-color:var(--ai);color:#fff}
a.btn.off{opacity:.4;pointer-events:none}
.flows{font-size:12.5px;color:var(--ink-faint);line-height:1.7}
.empty{background:var(--surface);border:1px dashed var(--line);border-radius:14px;
padding:44px;text-align:center;color:var(--ink-faint)}
.foot{margin-top:34px;color:var(--ink-faint);font-size:12px}
"""


def card(e):
    kind = (e.get("kind") or "prospect").lower()
    kind = "client" if kind == "client" else "prospect"
    flows = e.get("flows") or []
    stats = []
    if flows:
        stats.append(f"{len(flows)} flows")
    if e.get("hours"):
        stats.append(f"{e['hours']}h to build")
    if e.get("created"):
        stats.append(e["created"])
    names = " · ".join(html.escape(str(f)) for f in flows[:6])
    if len(flows) > 6:
        names += f" · +{len(flows)-6} more"

    art = e.get("artifact_url")
    loc = e.get("local")
    return f"""<div class="card">
  <div class="top">
    <div class="nm">{html.escape(e.get('name') or e['slug'])}</div>
    <span class="badge {kind}">{kind}</span>
  </div>
  {f'<p class="note">{html.escape(e["note"])}</p>' if e.get('note') else ''}
  <div class="stats">{''.join(f'<span class="st">{html.escape(s)}</span>' for s in stats)}</div>
  {f'<div class="flows">{names}</div>' if names else ''}
  <div class="acts">
    <a class="btn pri {'' if art else 'off'}" href="{html.escape(art or '#')}" target="_blank">Open artifact</a>
    <a class="btn {'' if loc else 'off'}" href="file://{html.escape(loc or '')}" target="_blank">Local file</a>
  </div>
</div>"""


def build():
    ROOT.mkdir(parents=True, exist_ok=True)
    entries = load()
    REGISTRY.write_text(json.dumps(entries, indent=2))

    n_c = sum(1 for e in entries if (e.get("kind") or "").lower() == "client")
    n_p = len(entries) - n_c
    body = "".join(card(e) for e in entries) if entries else ""
    grid = f'<div class="grid">{body}</div>' if entries else (
        '<div class="empty">No workflows yet. Run <b>/workflow-flowchart</b> '
        'and the first one lands here.</div>')

    def pl(n, word):
        return f"{n} {word}" if n == 1 else f"{n} {word}s"

    doc = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Workflows</title><style>{CSS}</style></head><body><div class="wrap">
<h1>Workflows</h1>
<p class="sub">{pl(len(entries),'diagram')} &middot; {pl(n_c,'client')} &middot; {pl(n_p,'prospect')}
&middot; rebuilt {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
{grid}
<p class="foot">Source of truth is <code>{html.escape(str(ROOT))}</code>. Delete a folder and it
leaves this index on the next rebuild.</p>
</div></body></html>"""

    INDEX.write_text(doc)
    print(f"index.html rebuilt: {len(entries)} entries ({n_c} clients, {n_p} prospects)")
    for e in entries:
        print(f"  - {e['slug']:24} {len(e.get('flows') or [])} flows"
              f"{'  [no artifact url]' if not e.get('artifact_url') else ''}")
    return INDEX


if __name__ == "__main__":
    p = build()
    if "--open" in sys.argv:
        webbrowser.open(f"file://{p}")
