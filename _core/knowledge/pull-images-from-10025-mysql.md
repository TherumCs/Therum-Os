---
name: pull-images-from-10025-mysql
description: how to pull product galleries from the :10025 reference WP site via its MySQL DB + uploads
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1eb82035-25c8-45fb-83e3-63b52d3072eb
  modified: 2026-08-12T11:48:34.097Z
---

:10025 (the-sidemoney-company Local WP) product images live in the WP DB + uploads
folder — NOT the WooCommerce Store API, which only exposes PUBLISHED products
(many, e.g. the Bird Season jerseys, are drafts). Pull galleries via MySQL:

- mysql client: `~/Library/Application Support/Local/lightning-services/mysql-8.4.0/bin/darwin-arm64/bin/mysql`
- socket: `~/Library/Application Support/Local/run/zff81gb8N/mysql/mysqld.sock` (zff81gb8N = :10025)
- DB `local`, user `root`, pass `root`. **Table prefix is `smxx` with NO underscore** (`smxxposts`, `smxxpostmeta`).
- Mapping: product post (`post_type='product'`) → postmeta `_thumbnail_id` (featured = primary) + `_product_image_gallery` (CSV of attachment IDs) → each attachment's `_wp_attached_file` = relative path under `.../the-sidemoney-company/app/public/wp-content/uploads/`.
- Match a live product to its :10025 product by the numeric :10025 post ID baked into the live slug (`...-455083583`), else by `post_name`, else fuzzy name (risky — several "It Cost Me" totes collapse onto one; require exact slug/ID there).
- Printify-origin items (socks like symbol/signature/series-005, some totes/dad-hats) are NOT on :10025 — they need POD-partner mockups instead.
- Push to the live store: copy files locally → rsync to VPS `~/therum/<dir>/` → `mediaService.upload({filename,mimetype,buffer})` (returns `.url`) → set `product.image` (primary) + `product.images` (gallery `[{url,alt}]`).
- `resizeMaxPx=2560`; full-bleed category heroes want a ~2800px+ source or a 2000px paste upscales and looks pixelated (esp. clean studio shots). See [[live-store-real-money]] and [[the-port-law]].
