# context.md — User & Project Context
TSC-BETA · Claude keep current from user share. Read every loop.
Scope: PER-USER — start empty. Fill ONLY from what user tell you. Never invent.

## User
- Who: Bam — run Therum Creative Studios (Philadelphia), solo creative studio + consultancy.
- Building here: TSC-BETA — beta iteration workspace for The Sidemoney Company (TSC).
- Goals (Bam, CORRECTED 2026-07-27 after Claude misread twice): **10009 IS the replatform — ONE site.** Therum OS **2.0 is its BACKEND**; **Bricks is its FRONT END**. The **Bricks Bridge exists to make Bricks run against 2.0** as the data/admin layer. NOT two sites. NOT an export/migration to a separate 4100 site. 10009 currently still runs Therum OS **1.9.44** (counter plugin) as its backend — that is the thing 2.0 replaces.

## Project
- Current project / tool: addons/tsc/ = The Sidemoney Company beta. Scope (unset).
- Existing TSC site (READ-ONLY reference, no edit): `/Users/bam/Local Sites/the-sidemoney-company` (OLD path per Bam 2026-07-25; Drive copy `../the-sidemoney-company/` also old) — Local WP install, `the-sidemoney-company.local`, PHP 8.5.3, MySQL 8.4. **Active theme was Moderno (ideapark)** — Elementor-based; uncode installed but inactive. Plugins: Elementor, ACF, Meta Box, LiteSpeed Cache, Google Site Kit, webappick product feed; several disabled. DB backup: `db-backup-pre-relink-20260618.sql`. All builder pages = Elementor (no WPBakery found).
- Stack / tools: tsc-beta = WP + Bricks 2.3.1 (design surface); target = Therum OS 2.0 (no WP). Old site LIVE at localhost:10025 = standing REFERENCE for structure/behavior of the original — keep it runnable, needed for future work (Bam directive).
- Constraints / must-nots: never edit source TSC site folder unless explicitly told with path named; universal `_core` vs addon separation non-negotiable; folder on Google Drive — flag before heavy deps (node_modules), verify writes (sync lag), no git yet.

## Preferences
- Working style: blunt, fast, low-trust-by-default; infer intent + execute (no over-ask); surgical edits, one ask = one change, no scope creep; complete full list before check in; dedupe automatically; use real tool access for real info.
- Communication: voice-to-text (interpret shorthand/garble); lead with answer; no preamble, hedging, or narrating work; brief.
- Rule variations (overrides to _core/claude.md): none.

## Notes
- This engine independent copy of Therum Creative Studios `_core` (relabeled) — not synced automatically. Durable decisions logged in _core/memory.md.
- Site facts above discovered by Claude during 2026-07-25 setup (from `the-sidemoney-company/local-site.json` + wp-content listing), not stated by Bam — correct if wrong.

## How to maintain this file
- User state durable fact about self, project, stack, or preferences → record here one line under right section.
- This file = who / what / why (stable-ish). Volatile task state go in _core/memory.md, not here.
- Never store secrets (passwords, API keys, account numbers).
- No guesses. Not said → stay "(unset)".