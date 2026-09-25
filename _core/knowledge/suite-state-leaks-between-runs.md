---
name: suite-state-leaks-between-runs
description: "Therum OS test failures are usually leaked state from the previous run, not the code just changed"
metadata: 
  node_type: memory
  type: project
  originSessionId: f39b8ece-7f47-4ca7-9b74-38aa7b85aa50
  modified: 2026-08-01T00:24:27.948Z
---

In therum-cms-2, a test that fails right after an unrelated change is usually
leaked state from an earlier run, not a regression. Three sources, all fixed in
commit `1e0cef2` but worth recognising when a new one appears:

- **Stock reservations.** Creating an order increments `reserved`; only a real
  status transition releases it. Tests delete order rows instead, so the count
  survives → later runs 409 "Insufficient stock". `test/support/reservations.mjs`
  restores the invariant (reserved = what pending orders hold).
- **Rate limiters.** order-create (10/10min), milieu-register (10/15min),
  customer-register (5/15min) all outlive a run. A hot window 429s an unrelated
  assertion — and if it hits a fixture, node cancels the whole FILE instead of
  failing one test ("test did not finish before its parent").
- **Fixtures a throwing teardown left behind.** Then the next run dies at setup
  on a duplicate slug, and the process HANGS on open Redis handles rather than
  exiting.

**Why:** twice I chased a "regression" that was the previous run's residue.

**How to apply:** when a test fails, check the status code first — 409 means
reservations, 429 means a limiter, duplicate-slug means a poisoned teardown.
Confirm by running that file alone before touching the code under test.

Related: [[headless-verify-harness]]
