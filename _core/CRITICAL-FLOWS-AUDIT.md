# CRITICAL-FLOWS-AUDIT.md — the "don't let checkout break again" playbook

Started 2026-08-20 after a checkout-blocking bug shipped to the live store (the country
field: a raw 2-letter text input that browser autofill overflowed with "United States", so
`country.length === 2` failed and nobody could place an order — with no way to fix it).

This file is the repeatable audit. Run it before cutting a release, after any change to the
purchase / account funnel, and any time something smells off. It has three parts: the flows
that MUST work, the failure patterns to hunt, and a findings log.

---

## 0. How to run it (two passes — do BOTH)

**Pass A — automated hunt (adversarially verified).** Re-run the bug-hunt workflow:
`Workflow({ scriptPath: "<session>/workflows/scripts/critical-flows-bug-audit-*.js" })`
(the canonical script; 5 hunters over the flow slices → each candidate adversarially
verified so only real user-blockers survive). Log confirmed findings in §3.

**Pass B — actually drive the flow (the part I skipped last time).** "Walk the flow" does
NOT mean eyeballing the form. It means DRIVING A REAL ORDER to the place-order gate in a
real browser, mobile viewport, with **browser autofill turned on** (autofill is what broke
country). Add a public product → fill the address by autofill → reach Shipping → reach the
active "Place order" button. Do not complete the live charge. If any step dead-ends, that's
a blocker. Repeat for: guest, logged-in, member (F&F), and a restricted-product attempt.

---

## 1. Flows that MUST complete (a real user, normal use)

1. **Purchase (guest):** PDP → pick variant → Add to bag → cart → details → shipping quote →
   payment method → **Place order** reaches the pay step. Confirmation email fires; order row
   created and marked paid (via `orderService.markPaid`, not just the webhook).
2. **Purchase (logged-in / member):** same, with member price shown AND charged correctly.
3. **Account:** register → verify → login; forgot-password → code → reset → login; the
   `?setup=1` first-password flow for migrated / F&F accounts.
4. **Restricted product:** a non-permitted shopper CANNOT see/add it; a permitted one can.
5. **Every payment rail** the UI offers (card, Apple/Google Pay, Link, PayPal) either works
   or is not shown — never a dead-end tile.

## 2. Failure patterns to hunt (the country bug is pattern #1)

1. **Client ↔ server validation mismatch.** The client sends a value the server zod rejects,
   or the client blocks a value the server would accept. (country `length(2)` vs a full name.)
2. **Autofill / maxlength traps.** A field with `maxlength` that browser autofill can
   overflow, or an `autocomplete` hint that fills a value the validation then rejects. Prefer
   a `<select>` or a normalizer over a hand-typed coded field.
3. **Dead-end error.** A validation error a real user has NO way to satisfy from the UI
   (no field, wrong widget, impossible format). This is the worst class — it silently kills
   conversion.
4. **Step-gating deadlock.** A funnel step whose "advance/enable" condition can never be met
   with valid input (place-order stays disabled; shipping never quotes).
5. **Money math.** Discount/tax/margin-floor/coupon producing negative, zero, or NaN totals,
   or charging an amount that differs from what was shown.
6. **Succeeded-but-nothing-happened.** Payment captured but no order/email; order created but
   never marked paid; guest order never claimable.
7. **Silent required field.** A field the server requires that the client never collects.

## 3. Findings log

Each run: date, what was checked, confirmed findings (severity + fix + commit), and the
Pass-B result ("drove a guest order to place-order: OK"). Newest first.

### 2026-08-20 — initial run
- FIXED (blocker): checkout country field was a raw 2-letter input; autofill overflowed it →
  `country.length===2` failed → place-order hard-blocked. Replaced with a country `<select>`
  (United States default, value `US`). Verified live to the Shipping step. (Pattern #1/#2/#3.)
- Automated hunt across the full funnel: _(results pending — appended when the workflow
  returns; blockers fixed immediately, majors triaged)._
