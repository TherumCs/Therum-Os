# demo.md — TSC Demo Environment (Local.app)
Addon layer · load ON DEMAND when demo or test TSC changes.

## What it is
Dedicated demo site in Local.app: **tsc-beta** — full clone of `the-sidemoney-company` (2026-07-25, verified HTTP 200). Isolated: break it, blow away, re-clone. Source site stay untouched.

| Thing | Value |
|---|---|
| Site name (Local) | tsc-beta (id aMNHd3PFU) |
| URL | http://localhost:10009 (Local run localhost routing mode — NOT tsc-beta.local) |
| WP admin | http://localhost:10009/wp-admin (one-click admin: TheSidemoneyCompany) |
| Site folder | `~/Local Sites/tsc-beta/` |
| Cloned from | the-sidemoney-company (uncode + uncode-child, Elementor, ACF, WP, PHP 8.5.3, MySQL 8.4.0) |
| Active theme | **bricks-child** (Bricks 2.3.1 parent) — Sidemoney default theme per Bam 2026-07-25, copied from bam-leon site. Build on this. uncode stays installed, inactive. Bricks license key NOT in this DB — builder edit mode will ask activation (Bam has license). Child ships custom element `elements/title.php`. |
| DB | name `local`, root/root, table prefix `smxx`, socket `~/Library/Application Support/Local/run/aMNHd3PFU/mysql/mysqld.sock`, TCP localhost:10008 |
| Services | mailpit 10005/10006 · php-cgi 10007 · mysql 10008 · nginx 10009 |

## Demo flow
1. Open Local.app → start **tsc-beta** (green dot = running).
2. Open http://localhost:10009 (or "Open site" button).
3. Demo changes go in `~/Local Sites/tsc-beta/app/public/` — NEVER in the-sidemoney-company folder.
4. Shell: Local → tsc-beta → "Site shell" (wp-cli, mysql on site env).

## Known caveats (from setup, 2026-07-25)
- **Port share with source site**: tsc-beta and the-sidemoney-company both assigned ports 10005-10009. Do NOT run both at once — start whichever needed, stop other first.
- **Local Clone crashes on this site**: `wp-content/plugins/counter` in source is symlink into therum-os folder; Local cloner dies on it (unhandled rejection, stuck "Copying site files…" at ~147MB). tsc-beta finished manually: rsync `--copy-links` (symlink materialized to real files — demo does NOT share plugin files with therum-os), manual `mysqld --initialize-insecure`, DB import from `app/sql/local.sql`, missing `run/<id>/nginx/logs` dir created by hand. Re-clone via Local UI hit same bug — use Reset procedure below.
- DB dump URLs already `http://localhost:10009`; no search-replace needed. If Local reassign ports later, run search-replace old-port → new-port.

## Elementor → Bricks conversion (2026-07-25)
- Source site ran **Moderno** theme (Elementor-based, ideapark widgets) — NOT uncode. Confirmed from DB dump.
- Converter: `addons/tsc/tools/elementor-to-bricks.py` (deterministic; rerunnable; `--dry-run`, `--page ID`). Reads `_elementor_data`, writes `_bricks_page_content_2` (PHP-serialized flat element list) + `_bricks_editor_mode=bricks`.
- Converted 22 pages. Mapping: core widgets faithful (heading/text/image/button/list); composites approximated (image-box, spacer, galleries, social, countdown, reviews, slider); theme-coupled ideapark widgets (product-tabs, mega-menu, running-line, news-carousel, circle-text, banners) → labeled placeholder blocks, original settings preserved in embedded JSON (`class="ideapark-orig"`).
- Elementor + ideapark-moderno + ideapark-fonts plugins DEACTIVATED (were hijacking the_content). `_elementor_data` left intact (rollback possible).
- Bricks license key copied from bam-leon DB (`bricks_license_key`, unlimited-sites license).
- State: content-level conversion done, front page renders 82 brxe elements. DESIGN not carried — Elementor style settings + Moderno CSS don't map; restyle in Bricks builder ("build on this").

## Reset procedure (Local Clone bug workaround)
1. Local → stop + right-click tsc-beta → Delete (move files to trash).
2. Local → right-click the-sidemoney-company → Clone site → name `tsc-beta`. It WILL stall at "Copying site files…" — quit Local (site registered anyway).
3. `rsync -a --copy-links --delete "~/Local Sites/the-sidemoney-company/app/public/" "~/Local Sites/tsc-beta/app/public/"`
4. Rewrite `~/Local Sites/tsc-beta/local-site.json` from tsc-beta entry in `~/Library/Application Support/Local/sites.json` (fix path to `/Users/bam/Local Sites/tsc-beta`).
5. `mysqld --initialize-insecure --datadir="~/Library/Application Support/Local/run/<newId>/mysql/data"` (mysqld from `~/Library/Application Support/Local/lightning-services/mysql-8.4.0/bin/darwin-arm64/bin/`).
6. Relaunch Local, Start site. If nginx fail: `mkdir -p run/<newId>/nginx/logs run/<newId>/nginx/temp`, Restart.
7. `CREATE DATABASE IF NOT EXISTS local; ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';` then import `app/sql/local.sql`. Verify HTTP 200 + URLs in `smxxoptions`.
Alternative permanent fix: replace symlink in SOURCE with real files (ask Bam first — source protected).