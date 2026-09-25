---
name: ported-chrome-has-two-headers
description: "The TSC ported chrome renders a desktop AND a mobile header — querySelector picks the hidden one, so always use querySelectorAll"
metadata: 
  node_type: memory
  type: project
  originSessionId: f39b8ece-7f47-4ca7-9b74-38aa7b85aa50
  modified: 2026-07-29T14:38:18.752Z
---

The ported TSC header markup contains **two** complete headers — a desktop one and a mobile one (`c-header__outer--mobile`) — and hides whichever does not apply with `display:none`. Every theme hook therefore exists at least twice: `.js-cart`, `.js-cart-info`, `.js-wishlist-info`, `.js-search-button`.

**Why:** `document.querySelector('.js-cart')` returns the MOBILE bag first in DOM order. On a desktop viewport that element sits inside a `display:none` ancestor, so anything attached to it measures 0x0 and looks like a CSS bug. This cost real time on the mini cart — the dropdown had correct computed `display:block` and `width:315px` and still had a zero bounding rect.

**How to apply:** bind to `querySelectorAll` and act on all matches, letting the theme's own CSS decide which is on screen. Do not try to detect the "live" header — that needs re-detection on every resize. Confirmed 2026-07-29 while wiring `src/site/headerCart.ts`. Related: [[headless-verify-harness]].
