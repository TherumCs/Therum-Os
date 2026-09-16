# FUTURE-DEVELOPMENTS.md — The Sidemoney Company (store-specific)

Started 2026-08-19 at Bam's instruction. This is the **store** roadmap: things
that belong to sidemoney.co specifically — go-to-market, campaigns, catalog,
store content. Engine/platform capabilities (accounts, login, Counter, Milieu)
live in `_core/FUTURE-DEVELOPMENTS.md` instead.

Living doc. Nothing here is built. Each entry is a note to pick up later, not an
approved spec.

---

## 1. Instagram / Meta Shopping

Let people shop the store directly on Instagram. The Meta product feed is
already live and variant-level (`/feed/facebook.xml`), so the catalog side is
done. What's left is the commerce side Bam flagged as "the CTX fee situation" —
resolve that so checkout/shopping can happen in-feed. This is the next growth
step after Friends & Family and the preorder launch.

---

## 2. Preorders

Preorders launch **2026-08-31** (the homepage countdown is already set to it).
Before then, confirm the preorder buy-flow and how preordered items flow through
fulfillment (they ship later than in-stock — the order/fulfillment path must not
treat a preorder as immediately fulfillable).

---

## 3. Migrated WordPress customers — Bam's call

55 customers + 53 orders were imported from the old :10025 WP store as basic
accounts, no discounts, and **no welcome emails sent**. Still pending Bam's
decision: which of them get Friends & Family, and which ones are cleared to be
emailed. **Do not email any migrated customer until Bam says who.**

---

## 4. Multi-email / any-email login

Motivated here by a sidemoney customer (Uzo, two addresses), but it's an
**engine** feature — every store gets it. The design sketch, plus the optional
SMS 2FA layer, lives in `_core/FUTURE-DEVELOPMENTS.md §1`. Recorded here only so
the sidemoney trail points to it.
