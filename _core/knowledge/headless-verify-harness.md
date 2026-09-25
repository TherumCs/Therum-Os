---
name: headless-verify-harness
description: "How to drive real headless Chrome over CDP to verify UI, and the four harness traps that each produced a confidently wrong verdict"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f39b8ece-7f47-4ca7-9b74-38aa7b85aa50
  modified: 2026-08-03T17:44:44.548Z
---

Verify UI by driving **real Chrome over CDP**, never the in-app Browser pane: the
pane reports **zero React fibers on a healthy Next.js dev app**, so it cannot tell
"the app is broken" from "the sandbox blocked hydration." On 2026-07-27 it showed
every admin control dead and sent me chasing proxy headers for hours.

**Harness:** spawn `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
--headless=new --remote-debugging-port=N --user-data-dir=<temp>`, connect a
`WebSocket` to the target from `/json/list`, auth via `Network.setCookie` (works
for HttpOnly), then `Runtime.evaluate`. Node's global `fetch` and `WebSocket` are
enough — no npm dependency. Also read the dev server's stdout; Next logs refusals
there that never reach the browser.

**Four traps, each of which produced a wrong answer I reported as fact:**

1. **Never resize the viewport to the page height to capture full-page.** Sections
   built on `100vh` re-render at that height, so the capture shows one giant hero
   and matches nothing on screen. Both my page and the reference "looked right"
   this way while Bam was staring at a broken page. Keep the viewport fixed
   (1440x900) and pass `captureBeyondViewport: true` with an explicit `clip`.
   Also keep `deviceScaleFactor: 1` — a `clip` is in CSS pixels, so dsf 2 renders
   the page twice into one image.
2. **Transitions and animations never tick.** `getComputedStyle` on a
   transitioning property returns the START value forever. Inject
   `*,*::before,*::after{transition:none!important;animation:none!important}`
   before measuring an animated state. If a computed value and a screenshot
   disagree, suspect the harness first.
3. **No window focus**, so `:focus` never matches and `.focus()` looks broken. Use
   `Emulation.setFocusEmulationEnabled`, and dispatch a real
   `Input.dispatchMouseEvent` when the rule is about mouse focus vs `:focus-visible`.
4. **Validate the harness itself before trusting a green result.** A run that
   exits 0 having executed nothing reads exactly like a clean pass — a main-module
   guard written as ``import.meta.url === `file://${process.argv[1]}` `` silently
   never matches when the repo path contains a space (this repo lives under
   "Local Sites"). Use `pathToFileURL(process.argv[1]).href`.

Related: [[verify-settings-by-rendered-geometry]], [[compare-against-the-reference-site]],
[[ported-chrome-has-two-headers]], [[bam-working-style]].
