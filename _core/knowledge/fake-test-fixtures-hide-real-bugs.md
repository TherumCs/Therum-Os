---
name: fake-test-fixtures-hide-real-bugs
description: "Two live auth holes survived a 437-test green suite because the fixtures were fake strings — check what a test ASSERTS, not whether it passes"
metadata: 
  node_type: memory
  type: project
  originSessionId: f39b8ece-7f47-4ca7-9b74-38aa7b85aa50
  modified: 2026-08-02T18:07:29.465Z
---

2026-08-02. Two production auth defects sat behind a fully green suite because
the credentials in the tests were made up:

- `test/counter.test.mjs` — `asAdmin` was the literal `th_session=admin-session-for-tests`,
  with a comment stating the hole as intent: *"the value only has to LOOK like a
  session cookie."*
- `test/site.test.mjs` — `th_session=whatever`, found only because fixing the
  maintenance gate made it fail.

Both passed for precisely the reason an attacker's forged cookie passed:
`hasAdminSession()` tested that a cookie by that NAME existed, never its
signature. Anyone sending `Cookie: th_session=garbage` could have read_write
store keys POSTed to a callback URL of their choosing. Confirmed against
production with one curl.

**Why it matters:** a test whose credential is fake proves only that the code
accepts fakes. Green means nothing about whether the assertion was real.

**How to apply:** in any auth-adjacent suite, grep the fixtures for literal
strings standing in for credentials before trusting coverage. Mint real signed
tokens. Add the negative case — a forged credential must be REFUSED — and
red-green it by reverting the fix. Fixed in `src/lib/adminSession.ts`, now the
single definition of "is an admin signed in". Related:
[[get-evidence-before-theorising]], [[suite-state-leaks-between-runs]].
