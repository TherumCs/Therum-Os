---
name: sidemoney-storefront-render
description: "storefront render gotchas — descriptions render RAW HTML (never esc), Meta feed images must be local, PDP is 'apple' style with a lightbox + pretty rags"
metadata: 
  node_type: memory
  type: project
  originSessionId: e745e2aa-9578-48ef-9843-d125d121f24c
  modified: 2026-09-02T00:19:58.483Z
---

**Product descriptions are stored as raw HTML (`<p>`, `<ul>`, `<li>`, literal UTF-8) and MUST render raw.** The PDP (`storefront.ts` ~line 1310) used to `esc(p.description)`, shipping `&lt;p&gt;` as literal text ("mad descriptions have HTML tags showing" — 2026-09). Fixed: render raw when it contains tags, `esc`+`\n→<br>` only for plain text. The category story (`categoryTemplates.ts`) is likewise raw (`${s.body}`). Never reintroduce `esc()` on a description body. Write copy in the Sidemoney voice, **no em-dashes**; put copy in a file + scp + node reads it (heredoc mangles UTF-8).

**Meta feed (`/feed/facebook.xml`, variant-level) images must be LOCAL.** Meta's fetcher 403s / can't reliably pull external POD-CDN URLs (Printify / Aliyun / JetPrint S3) → "missing or invalid images", dead variants. Fix pattern: download each external `variant.image` / `product.images[]` / `variant.images[]`, re-upload via `mediaService.upload` (bounds 2560px + makes a `-thumb`), fall back to the product's local primary if the source URL is already dead; archive a product whose only image is a dead external with no fallback. The feed's `g:image_link` per item = `variant.image || product primary`. "Data file failed to upload" in Commerce Manager is usually the OLD woo-feed URL (`/wp-content/uploads/woo-feed/... ` = 404) or a transient failure mid-deploy — nginx access log shows Meta IPs (173.252.x / 31.13.x) actually getting 200.

**PDP** is the **'apple'** (centered) style. Desktop (≥1200px) widened vs tablet; click-to-zoom **lightbox** on `.gallery-main` (⛶ button, arrows page the gallery, X/Esc/backdrop closes); paragraph rags use `text-wrap:pretty`, titles `text-wrap:balance`. Grid cards + carousel strips request the 480px `-thumb` via `thumbUrl()` (productGrid.ts) — the site was slow serving 2560px originals + a 5MB hotlinked money-ball image. See [[inventory-stock-model]] [[store-attribution-and-feed]].

**Product shots can have grey baked INTO the file** (found 2026-09-18 when Bam said "there should be no grey on this image and dont fight me on it"). The '96 Series jersey was a 1500×1500 JPEG whose corners were pure white but whose centre field was a flat `246,246,246` studio backdrop — so fixing the email kit's CSS ground was only half of it. Fix that worked, reusable: PIL flood fill from every border pixel, treating a pixel as background only when `min(r,g,b) >= 234` AND `max-min <= 6` (neutral), painting matched pixels white. Border-connected only, so the jersey's cream trim, the pin's brushed metal and the drop shadows survive — verified by eye on all four. Cleaned + re-uploaded + `product.image` repointed for `ixers-season-jersey-red`, `bird-season-practice-jersey-kelly-green`, `money-wash-wallet`, `snake-skin-…-lapel-pin`; originals still on disk, rollback = set the old URL string back. The email kit's own `T.thumb` placeholder also went `#f2f2f2` → `#ffffff` (emailTemplate.ts) — product cut-outs sit on white.
