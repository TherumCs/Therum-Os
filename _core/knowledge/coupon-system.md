---
name: coupon-system
description: "how storefront coupons work — cart-scope only, the single per-product exemption lever, per-customer cap enforcement, and that all jerseys are already promo-exempt"
metadata:
  node_type: memory
  type: project
  originSessionId: e745e2aa-9578-48ef-9843-d125d121f24c
  modified: 2026-09-04T12:13:33.699Z
---

Coupons are the Counter C3 system (`Coupon` + `CouponRedemption` tables, `src/services/coupon.service.ts`). **v1 is CART-SCOPE** (schema comment: "percent|fixed, cart-scope, single-coupon-per-cart"). A coupon has NO product / category include-or-exclude field — the model is code, type(percent|fixed), amount, min/maxAmount, usageLimit (global), usageLimitPerUser, startsAt/expiresAt, status, milieuId (members-only group), individualUse. The discount is computed on the cart subtotal, best-single-wins, no stacking; member price is a FLOOR (a member's coupon isn't quoted at all).

**The ONLY product-level exemption lever is `product.meta.noMemberDiscount === true`.** In `cart.service.ts` (~line 187) the coupon is quoted against `eligibleSubtotal`, which SUMS only lines whose product is NOT flagged `noMemberDiscount`. So a flagged product is excluded from BOTH member discounts AND every coupon (audit H2 — a store-wide code used to discount an at-cost item below cost). This is GLOBAL per product, not per-coupon: flagging a product exempts it from all codes and member prices at once. There is no way to exempt a product from ONE specific coupon without new schema + apply-path code.

**All 9 jerseys are already flagged `noMemberDiscount:true`** (5 Sixers: ixers-season-jersey-{red,black,split-76,blue,white}; 4 Bird practice: bird-season-practice-jersey-{darkmode,kelly-green,midnight-green,snowflare}). So "jerseys exempt from a code" needs ZERO product edits — it already holds. (Bird Season Bespoke Crewneck is also flagged, for its own at-cost reason.) `minMarginPct` = 0 in commerce settings, so the margin floor (`maxDiscountForMargin`) does not clamp normal % discounts.

**Per-customer limit** = `usageLimitPerUser`. Enforced ONLY at checkout in `reserveForOrder` (atomic conditional increment, re-checked inside the txn), keyed on the VERIFIED `customerId` first, guest `email` fallback (audit C15 — email alone was bypassable). A refund releases the slot (`releaseForOrder`), so a refunded order doesn't burn a use. Quote/apply never reserves, so testing a cart doesn't consume usage.

Created 2026-09-04: **GIVEAWAY15** — percent 15, `usageLimitPerUser:1`, `usageLimit:null` (unlimited total, one per customer), no expiry. Made it 15% to match the existing WELCOME10 (percent 10) pattern. Verified live via the cart API: a $50 snapback + $120 jersey cart discounted $7.50 (15% of the snapback only — jersey excluded). See [[live-store-real-money]] [[inventory-stock-model]] [[sidemoney-storefront-render]].

**WELCOME10 / popup chain verified end to end 2026-09-18** (Bam: "if it's not, what are we doing?"). Real signup through the public `/api/subscribe` with `source: popup` → subscriber row + a queued CampaignSend on the welcome automation → **email delivered in about one second** carrying `WELCOME10` → applied to a live cart: Money Wash Wallet $70.00 became **$63.00**. Coupon row: percent 10, status active, `usageLimitPerUser: 1`, no expiry, `individualUse: true` (so it will not stack), and the 9 jerseys carry `meta.noMemberDiscount` so they are exempt — a cart of only jerseys gets nothing off. Two defects found and fixed in the same pass: the welcome SUBJECT had an em dash and rendered "Welcome in, there" when no first name (the popup does not ask for one) — now "Welcome in. Here is 10% off your first order."; and automation email images were remote, so `automation.service.ts deliver()` now runs them through `inlineImages()` like campaigns do (the only remote image left is the open pixel, on purpose). Popup counters at the time: 124 views, 0 real submits — nobody has used it yet, the feature works. All test subscribers, sends and the cart removed; form counter put back to 0.
