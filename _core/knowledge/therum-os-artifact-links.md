---
name: therum-os-artifact-links
description: "Published Artifact share links Bam refers to (Therum OS case study, dashboard mockup, etc.)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: f4504c37-caac-4f64-affa-6039105bec50
  modified: 2026-08-20T21:44:25.766Z
---

Artifact links Bam asked to keep handy (there is no chat-pin, so they live here).

- **Therum OS** (the "html thing" — the WordPress/WooCommerce case study on WP runtime
  mechanics / why WP is slow): https://claude.ai/code/artifact/12907b8f-147b-435e-87b7-80b856d36b84
- Therum OS — Server panel and the connected assistant: https://claude.ai/code/artifact/ab2a5231-2181-4c22-bf3a-4d614cabfecf
- Therum OS 1.9.44 → CMS 2.0 — Feature Inventory: https://claude.ai/code/artifact/c321c86d-9d08-4096-b71b-57431cfbb105
- Therum Dashboard (mockup): https://claude.ai/code/artifact/87fd9606-9c4d-49ad-8a38-fc644dcc52e8
- Therum Site Preview: https://claude.ai/code/artifact/7ef13406-35b0-4096-9ccf-24101cc47d2d

Artifacts start PRIVATE — Bam shares from the artifact page's Share control. To update
one, publish with `url:` set to its link (never a new file path).

- **Therum OS Admin Demo** (2026-09-21) — https://claude.ai/artifact/Rhyot7tydaWwApDJRwfwQ4 — clickable prototype of the sidemoney.co admin for Bam's case study: rebuilt sidebar + Flow tab hotspots over 19 scrubbed page captures, 8-step tour. Source in scratchpad `demo/` (index.html + pages/*.jpg); flat screenshots + 2x PNGs in TSC-BETA `addons/tsc/case-study/admin-screens-2026-09-21/`. **How the scrub was done** (reuse): pull every customer/subscriber name and shipping line from the DB into a file (never stdout), replace exact matches in-page with placeholders filtered against that list so none collide, then regex-sweep emails/phones/addresses/keys, then a separate pass re-loads every page and asserts 0 real names / 0 real emails / 0 keys in `innerText` before any image is kept. Driver: puppeteer-core in the scratchpad against system Chrome, admin session cookie from `scripts/mint-jwt.mjs` written to a file. Still real in the captures: dollar figures, order numbers, vendor names, bank last-4 (app-masked).

