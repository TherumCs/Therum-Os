# FUTURE-DEVELOPMENTS.md — Therum OS / Counter / Milieu / studio engine

Started 2026-08-19 at Bam's instruction. This is the **engine** roadmap: things
that belong to the platform every store inherits — Counter (commerce + customer
accounts), Milieu (membership/discount groups), the CMS, and studio tooling.
Store-specific ideas live in `addons/tsc/FUTURE-DEVELOPMENTS.md` instead.

Living doc. Nothing here is built. "PINNED" = parked on purpose, do NOT build
until Bam says go. Each entry is a sketch to make the eventual build cheap, not
a spec that's been approved.

---

## 1. Multi-email login (up to 3 emails per account)

**Motivation.** A customer can have more than one address. Today the account has
exactly one login email (`Customer.email`, unique). When Uzo (a sidemoney
customer) gave a second address, it could only be recorded as a dead contact
field in `meta.altEmails` — you cannot sign in with it. Bam wants: **up to 3
emails on an account, log in with any of them, one shared password.**

**Design sketch (buildable):**
- **Data.** Add a `CustomerEmail` table — `{ id, customerId, email @unique,
  isPrimary Boolean, verifiedAt DateTime? }`. `Customer.email` stays as the
  display/primary address; a customer has 1 primary + up to 2 additional, max 3
  total, all rows here.
- **Login lookup.** `customerAuth` resolves the entered address against
  `CustomerEmail` → the owning customer → the existing credential/session path.
  Any of the account's emails authenticates against the account's **single**
  credential — same password, whichever email was typed.
- **Verification.** Adding an email sends a verify link/code to THAT address. An
  unverified email cannot log in and receives no account mail — otherwise anyone
  could bolt a stranger's address onto their account.
- **Reset / codes.** Password reset or a login code can be requested from any
  verified linked email and routes back to that same address.
- **Notifications.** Decide which address account mail goes to — default the
  primary; optionally let the customer pick, or CC the alts. The store-mail law
  still holds: send FROM the store's own address (for sidemoney,
  `commoncents@sidemoney.co`), never a personal one.
- **Migration.** Fold today's `meta.altEmails` stopgap into `CustomerEmail`
  rows (unverified until the owner confirms). Uzo is the first case:
  `uzomastudios@gmail.com` (primary) + `uzomatherapy@gmail.com`.
- **Cap.** Hard limit 3. Enforce on add.

**Optional 2FA on top (Bam, 2026-08-19).** Because any-email login widens the
front door, let an account **turn on two-factor auth**: on sign-in, text an SMS
one-time code to the account's verified phone and require it to finish logging
in. Needs — a verified phone on the account, an SMS provider (Twilio or similar
— **PINNED: provider choice not decided**), per-account opt-in, rate limiting,
and a sane fallback when no phone is set. This pairs naturally with multi-email
but can ship independently.

---

## 2. Social login — PINNED, DO NOT BUILD

Bam: "figure out whatever our social login is gonna work. But don't build out
the social login shit. Let's put a PIN in that."

**Intent.** OAuth sign-in (Google, Apple at minimum) that links to the same
customer by verified email, so social and email login land on one account.

**Open questions to settle before any build:**
- Which providers first — Google and Apple, or more.
- Account-linking rule: a social login whose verified email matches an existing
  account links to it (does not create a duplicate); how guest → account merge
  behaves.
- Which pages surface it (login, account, checkout).
- Consent/privacy handling.

**Status: parked.** No work until Bam lifts the pin.

---

## 3. Other engine candidates (confirm before building)

Real items already surfaced elsewhere — recorded here so they aren't lost. Each
needs Bam's go before it becomes work.

- **Stripe webhook hardening.** No PSP webhooks are configured
  (`webhookSecret=none`). Order emails no longer depend on them, but wiring
  `payment_intent.succeeded` would add robustness against a missed capture.
- **Dashboard live-activity feed.** A lightweight `GET /api/counter/feed`
  returning recent cross-domain events (order, cart, signup, sync, review) for
  the dashboard's activity card — currently derived from recent orders only.
  (Open item from `docs/dashboard-redesign.md`.)
- **Pinned-widget injection convention.** Any NEW default dashboard widget must
  inject itself into already-saved layouts, or existing admins never see it (a
  saved `dsh_layouts_v2` overrides DEFAULTS). The Purchase-activity widget set
  the pattern with a one-time `dsh_pin_*` flag — reuse it for the next pinned
  widget.
