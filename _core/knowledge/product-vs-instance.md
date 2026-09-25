---
name: product-vs-instance
description: HARD RULE — the Therum OS product repo carries no store; everything Sidemoney-specific lives in the TSC-BETA instance repo as a site pack + DB settings + env
metadata:
  type: feedback
---

Bam, 2026-09-16 ("fam github shit should be the therum os only. we said the before"): `TherumCs/Therum-OS-2.0` = Therum OS ONLY. I broke it twice (hard-coded brand in beta.10, then `deploy/live` with the store's nginx + payment bridge).

**Why:** the product is sold/reused; a customer's name, domain, tokens, copy, infra or config in it is a leak and a lie about what the product is.

**How to apply:**
- Store-specific = `TherumCs/Therum-Os` (this TSC-BETA folder) → `addons/tsc/site-pack/` (categoryPages.json, site.env, deploy/ nginx + sm-appliance.php). Deployed to the box at `/home/therum/site-pack/` + `.env`.
- Brand in the product is a SETTING or ENV: site name (Settings › Site), Meta verification (SEO Defaults `facebookDomainVerification`), email logo `EMAIL_LOGO_URL`, careers `CAREERS_INBOX`, landings `SITE_PACK_DIR`.
- Before any product commit: `git grep -il "sidemoney\|\bbam\b" -- . ':!package-lock.json'` must be empty (comments and docs included).
- History still contains the old brand strings (pre-2026-09-16 commits). Rewriting history is a separate decision for Bam.
