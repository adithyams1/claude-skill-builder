# Features panel - the paste-in block

An optional add-on for a PLATFORM rather than a pipeline. The diagram carries the shape;
this panel carries the substance. Patch it into the GENERATED file, never `template.html`.

## Why it exists

On a platform build, a left-to-right sequence made the build look smaller than it was:
the client was not buying a workflow, they were buying a platform. The fix was
to keep the diagram AND put a plain table one click away.

## The four columns, always in this order

| What you asked for | How we are solving it | Where it is now | Limits to know |

- Frame it around the ask, never around what the client got wrong. "What you hit" was
  rejected: it reads as a post-mortem of their failure.
- One idea per cell, one short line. You talk over it on a call, nobody reads it.
- **Limits is not optional.** Quotas, approval waits and caps are what a technical buyer
  asks about in the room. Name the number and who grants it - "about 5 working days",
  "roughly 100 uploads a day per project, ask the vendor to raise it". Never "subject
  to limits". Pull them from the project's own notes; they are never in memory.

Status pills reuse the node colours so panel and diagram speak the same language:
`ps ok` green working, `ps next` amber next, `ps need` purple waiting on them. Column
three doubles as the ask list, column four kills the follow-up questions.

## The script MUST be its own block

Do not append it to the template's `<script>`. The template ships a single block, so an
error anywhere above kills everything after it - silently, and only in some environments.
That took out the zoom controls and then the panel button itself, both times passing
locally and failing published.

Put it in a separate `<script>` after the template's, look the elements up, bail if they
are absent, and retry once on `DOMContentLoaded`.

**Verify the isolation, do not assume it:** copy the file, inject `BOOM.explode();` right
before the template's first `</script>`, load it, and confirm the panel still opens.

## Do not add more interaction

Open and close only. Zoom controls were tried and pulled - they are not worth the surface
area on a diagram the client only looks at for a minute.

## 1. Button - insert after `<div id="list"></div>`

```html
  <button id="pbtn" type="button">
    <span class="pb-ic">!</span>
    <span><span class="pb-t">What you asked for</span>
    <span class="pb-s">and where each one is now</span></span>
  </button>
```

## 2. Panel - insert after the `#hint` div

The rows below are an illustrative ad-analytics example. Replace them with your own.

```html
<div id="pscrim" hidden></div>
<div id="ppanel" role="dialog" aria-modal="true" aria-labelledby="ptitle" hidden>
  <div class="pp-head">
    <h3 id="ptitle">What you asked for, and where it is</h3>
    <button class="btn" id="pclose" aria-label="Close">&times;</button>
  </div>
  <div class="pp-body">
    <table class="ptbl">
      <thead><tr><th>What you asked for</th><th>How we are solving it</th><th>Where it is now</th><th>Limits to know</th></tr></thead>
      <tbody>
        <tr><td>See the creatives next to the numbers</td>
            <td>An AI watches every ad and it plays inside the tool.</td>
            <td><span class="ps ok">Working</span> 5 ads watched, scene by scene</td>
            <td>The model watches each video once. The free tier covers a few hours of video a day.</td></tr>
        <tr><td>Compare shorts to shorts, in-stream to in-stream</td>
            <td>Every ad split by placement. Never blended.</td>
            <td><span class="ps ok">Working</span> variant A 83% vs variant B 57%</td>
            <td>Needs the Ad x Format report. Cells under 20k impressions are not scored.</td></tr>
        <tr><td>Your full metric list</td>
            <td>Every metric mapped or derived from the export.</td>
            <td><span class="ps ok">Working</span> 17 of 17</td>
            <td>None.</td></tr>
        <tr><td>Segment by campaign, audience, demographic</td>
            <td>Demographics kept as their own breakdown, not squeezed onto the ad.</td>
            <td><span class="ps ok">Working</span> 11 of 11</td>
            <td>Comes from a separate platform report, not the ad export.</td></tr>
        <tr><td>A naming taxonomy to use before uploading</td>
            <td>The name is built from dropdowns, so it cannot break.</td>
            <td><span class="ps ok">Working</span> also flags where your names drift</td>
            <td>None.</td></tr>
        <tr><td>Name the ads here and push them live</td>
            <td>One action uploads the video and creates the ad, paused.</td>
            <td><span class="ps next">Next</span> write access, 5 days</td>
            <td>Write access needs an approval, about 5 working days. Roughly 100 video uploads a day per project - more projects, or ask the vendor to raise it.</td></tr>
        <tr><td>Numbers that are current when you open it</td>
            <td>Refreshes overnight and shows when it last synced.</td>
            <td><span class="ps next">Next</span> needs the API connection</td>
            <td>A daily pull is about 150 calls. The entry API tier allows a few thousand a day.</td></tr>
        <tr><td>See what is scaling and what is declining</td>
            <td>Movement fills in on its own once a second period exists.</td>
            <td><span class="ps need">Need</span> a second export from you</td>
            <td>Nothing to compare against until a second period exists.</td></tr>
        <tr><td>Take the weekly client notes off your team</td>
            <td>Drafts 60 to 70%. You add the strategy and the client context.</td>
            <td><span class="ps next">Later</span> separate build</td>
            <td>Spans several ad platforms, so it is a bigger build.</td></tr>
      </tbody>
    </table>
  </div>
</div>
```

## 3. CSS - append before `</style>`

```css
  /* ---- problems & fixes panel ---- */
  #pbtn{margin:6px 8px 2px; padding:10px 11px; display:flex; gap:9px; align-items:flex-start;
    width:calc(100% - 16px); text-align:left; cursor:pointer; color:var(--ink);
    background:var(--surface-2); border:1px solid var(--line); border-radius:10px;
    font-family:var(--sans)}
  #pbtn:hover{border-color:var(--gate)}
  #pbtn:focus-visible{outline:2px solid var(--gate); outline-offset:1px}
  .pb-ic{width:19px; height:19px; flex:none; border-radius:5px; background:var(--gate-bg);
    color:var(--gate); font-family:var(--mono); font-size:12px; font-weight:700;
    display:grid; place-items:center; margin-top:1px}
  .pb-t{display:block; font-size:12.5px; font-weight:600; line-height:1.25}
  .pb-s{display:block; font-family:var(--mono); font-size:9.5px; color:var(--ink-faint); margin-top:2px}

  #pscrim{position:fixed; inset:0; background:rgba(10,14,22,.42); z-index:40}
  #ppanel{position:fixed; z-index:41; top:50%; left:50%; transform:translate(-50%,-50%);
    width:min(1180px,calc(100vw - 40px)); max-height:min(82vh,820px);
    display:flex; flex-direction:column;
    background:var(--surface); border:1px solid var(--line); border-radius:12px;
    box-shadow:0 18px 60px rgba(10,14,22,.3)}
  #ppanel[hidden],#pscrim[hidden]{display:none}
  .pp-head{display:flex; align-items:center; justify-content:space-between; gap:12px;
    padding:15px 18px; border-bottom:1px solid var(--line)}
  .pp-head h3{margin:0; font-size:15px; letter-spacing:-.015em}
  .pp-body{overflow:auto; padding:4px 18px 18px}
  .ptbl{border-collapse:collapse; width:100%; font-size:13px}
  .ptbl thead th{position:sticky; top:0; background:var(--surface);
    font-family:var(--mono); font-size:9.5px; letter-spacing:.1em; text-transform:uppercase;
    color:var(--ink-faint); font-weight:700; text-align:left; padding:12px 12px 9px;
    border-bottom:1.5px solid var(--line)}
  .ptbl td{padding:12px; vertical-align:top; border-bottom:1px solid var(--line);
    color:var(--ink-soft); line-height:1.45}
  .ptbl tbody tr:last-child td{border-bottom:0}
  .ptbl td:first-child{color:var(--ink); font-weight:600; width:22%}
  .ptbl td:nth-child(2){width:26%}
  .ptbl td:nth-child(3){width:22%}
  .ptbl td:last-child{width:30%; color:var(--ink-faint)}
  .ps{display:inline-block; font-family:var(--mono); font-size:9px; letter-spacing:.08em;
    text-transform:uppercase; font-weight:700; padding:3px 7px; border-radius:4px; margin-right:6px}
  .ps.ok{background:var(--out-bg); color:var(--out)}
  .ps.next{background:var(--human-bg); color:var(--human)}
  .ps.need{background:var(--gate-bg); color:var(--gate)}
```

## 4. Script - in its OWN `<script>` block after the template's (see above)

```js
/* features panel */
(function(){
  const btn=document.getElementById('pbtn'), pan=document.getElementById('ppanel'),
        scr=document.getElementById('pscrim'), cls=document.getElementById('pclose');
  const open=v=>{pan.hidden=!v; scr.hidden=!v; if(v) cls.focus(); else btn.focus();};
  btn.onclick=()=>open(true); cls.onclick=()=>open(false); scr.onclick=()=>open(false);
  document.addEventListener('keydown',e=>{ if(e.key==='Escape' && !pan.hidden) open(false); });
})();
```
