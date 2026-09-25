---
name: local-sites-and-dbs
description: "Local runs several sites and names EVERY database \"local\" — the-sidemoney-company is :10025 (socket zff81gb8N); tsc-beta is :10020 (aMNHd3PFU). Confirm the socket before any mysql write."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f39b8ece-7f47-4ca7-9b74-38aa7b85aa50
  modified: 2026-08-05T20:52:46.818Z
---

Local by Flywheel runs multiple sites at once, each with its own MySQL instance,
and **names every database `local` with prefix `smxx`**. So a `mysql` CLI pointed
at the wrong socket reads a *different site's* data under identical names — no
error, just wrong answers.

Confirmed mapping (2026-08-05, from `~/Library/Application Support/Local/sites.json`
+ `run/<id>/`):

| Site | HTTP port | run-id / mysql socket | theme | notes |
|------|-----------|----------------------|-------|-------|
| **the-sidemoney-company** | **:10025** | `zff81gb8N` | `moderno` | the reference Bam calls ":10025"; WooCommerce + WooPayments store |
| **tsc-beta** | :10020 | `aMNHd3PFU` | `bricks` | the Therum-OS-on-WP beta; DB `siteurl` wrongly says :10020 on BOTH — stale |

Socket path: `~/Library/Application Support/Local/run/<id>/mysql/mysqld.sock`.
Bundled tools: mysql at
`/Applications/Local.app/Contents/Resources/extraResources/lightning-services/mysql-8.4.0/bin/darwin-arm64/bin/mysql`,
php 8.2 at `.../php-8.2.29+0/bin/darwin-arm64/bin/php`.

**This bit hard (2026-08-05).** I did DB writes for the-sidemoney-company against
socket `aMNHd3PFU` — which is *tsc-beta* — so the reads came back "wrong" (my
writes weren't visible to :10025's FPM) and I nearly edited the beta site's config
by accident. The FILE edits were on the right path
(`/Users/bam/Local Sites/the-sidemoney-company/...`) so those took; only the DB
went astray. Proof of which DB a running site actually uses: drop a one-request
mu-plugin that prints `$wpdb->get_var(...)` and `get_option(...)` from inside FPM
— that reads the site's REAL database, unlike a guessed CLI socket.

**How to apply:** before any `mysql` write, verify the socket belongs to the
intended site — match `blogname`/`stylesheet`/`active_plugins` against what that
port serves over HTTP, or read `sites.json`. Never assume "the DB is `local`"
identifies anything. Two installs = two PHP-FPM pools = two OPcaches too, so an
`opcache_reset()` hit on one port does nothing for the other. Ties into
[[get-evidence-before-theorising]] (know your system of record) and
[[the-port-law]].
