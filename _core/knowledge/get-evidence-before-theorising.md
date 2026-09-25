---
name: get-evidence-before-theorising
description: "Assert only from the system of record — not from a stale note, not from a tool that skips the real rules, not from the subset you happen to hold a key for"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f39b8ece-7f47-4ca7-9b74-38aa7b85aa50
  modified: 2026-08-05T20:11:05.452Z
---

Three times this has cost Bam real time, and each time the evidence was one
query away.

**Theorising instead of querying.** He clicked Connect from PODpartner and got a
sign-in form. He reported it eight times while I proposed four causes — SameSite,
www vs apex, response caching, cookie domain — "proving" each fine with curl,
which does not enforce the browser rules that mattered. Actual cause: the admin
session lived 12 hours. Last login 2026-08-01 18:20, expired 06:20 next morning;
Tapstitch was approved 03:48, inside the window. Same code, different side of one
timestamp. One `authEvent` query finds it on round one. His words: *"you keep
telling me one thing and you're wrong… I don't have tokens and all this other
shit to keep going back and forth."*

**Quoting a stale note as current state.** I told him his working site was broken
three times in one message, reading the "Flagged" section of `_core/memory.md`:
footer shortcode (zero occurrences live), 4 header links 404 (all returned 200),
checkout has no shipping step (it collects seven fields and POSTs to
`/cart/shipping`). He was right on every one. A flag list records what was true
when written; nothing rewrites it when he fixes it between sessions. When a
static grep comes back empty, ask whether the markup is client-rendered before
concluding it is absent — that is what made checkout look unbuilt.

**Generalising from the account I could see (2026-08-05).** Asked which processor
ran the old store, I listed charges on the Stripe account our key opens, found a
coherent story, and reported that WooPayments "was never in the path." The system
of record was `smxxwc_orders` — 34 of ~53 orders were `woocommerce_payments`,
running to 2025-12-31, on an account our key cannot read at all. I had even
written "I can't see inside that account" and then asserted about its contents
anyway.

**Why:** each wrong answer was internally consistent, which is what made it
convincing. Partial access produces a complete-looking story. And repeating an
explanation is not evidence — to the person on the other end it reads as being
told they are wrong.

**How to apply:**
- Find the system of record and open it. Orders live in the orders table, not in
  whichever processor you hold credentials for. Sessions live in the auth log.
- Before claiming anything is broken or missing, exercise it — curl the live URL,
  query the live database, grep current source. Cite the check, not the note.
- State the boundary of what you checked and never assert past it. "No charges on
  this account" is not "no charges."
- Treat a cached value as dated, not true: read its timestamp first. The
  WooPayments `instant_deposits_eligible=false` I quoted as fact had been fetched
  2026-06-06, six months after the store's last sale — the flag had lapsed with
  the volume, so both it and Bam's memory of having the feature were correct.
- "It worked with X but not Y" is the strongest clue available — diff those two
  events before anything else.

Related: [[headless-verify-harness]], [[verify-settings-by-rendered-geometry]],
[[fake-test-fixtures-hide-real-bugs]], [[bam-working-style]].
