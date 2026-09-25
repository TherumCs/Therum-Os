---
name: catch-the-gaps-yourself
description: "Bam's #1 recurring complaint — stop shipping half-working things and making him find the gaps"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f39b8ece-7f47-4ca7-9b74-38aa7b85aa50
  modified: 2026-08-09T03:10:31.574Z
---

Bam has flagged this in loops and memory repeatedly and it keeps recurring: I ship
things that are "built but a piece doesn't work," miss small visual glitches, and
miss logic gaps — and HE ends up finding them, tap by tap, on his real phone.

**Why:** verifying the happy path in emulation ≠ the thing working. Real examples he
caught that I missed: the card runtime dead from a `\'` inside a template literal
(tsc passed), add-to-cart adding but the badge never updating, the mobile menu
runtime never included on store pages, a ghost/duplicate cart under the checkout
success screen. Every one was a "we built this, it doesn't fully work."

**How to apply:** before claiming ANYTHING done — walk the WHOLE flow end to end
on the surface the user actually uses (mobile especially: real taps, the post-action
state, scroll to the bottom of the page for stray/overlapping/ghost elements), not
just the one action. Check the three failure classes every time: (1) logic, (2)
small visual (duplicates, transparency bleed, misalignment, leftover elements),
(3) built-but-a-piece-is-dead. Run the runtime `node --check` gate on any touched
storefront runtime string. Assume a feature is broken until proven whole. See
[[bam-working-style]], [[headless-verify-harness]], [[get-evidence-before-theorising]].

**2026-08-08 additions — four wallet bugs shipped that were all catchable by
review, no iPhone needed. New hard checks:**
1. **iOS gesture law (static check):** any native sheet or popup — Stripe
   `paymentRequest.show()`, `ApplePaySession`, `window.open` — must be called
   with ZERO `await` between the event-handler entry and the call. Even a
   resolved promise's microtask breaks the gesture on iOS and the sheet wedges.
   Grep the tap path for `await` before every `.show(` when touching payments.
2. **"Message set" ≠ "message seen":** any user-facing feedback written by JS
   must be asserted VISIBLE (bounding rect inside the viewport after the action),
   not just present in the DOM. A correct message below the fold reads as a dead
   button.
3. **Native-sheet callbacks must be hang-proof:** every fetch inside a
   payment-sheet callback needs a timeout to the failure path — a hung request
   pins the sheet on its own "Processing…" spinner. Ask "what if this never
   resolves?" for each call while a sheet is open.
4. **My headless browser is Chromium, NOT WebKit.** Safari-sensitive surfaces
   (aspect-ratio on flex items → renders OVALS on Safari, gesture rules,
   100vh/dvh) can pass my screenshots and fail Bam's iPhone. For money-path UI
   use fixed dimensions over aspect-ratio, and SAY explicitly when a check ran
   only in Chromium instead of claiming it verified.
