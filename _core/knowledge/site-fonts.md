---
name: site-fonts
description: What fonts sidemoney.co actually renders vs the :10025 reference, where each comes from, and the Roboto Condensed/Montserrat fallback bug fixed 2026-09-15
metadata:
  type: project
---

Measured with computed styles + `document.fonts` (never trust the CSS declaration alone).

- **Body** = Manrope (both live and :10025). ✔
- **Headings** = live renders `Inter Tight` via `var(--th-font-display)` (Therum Appearance default, `displayFont: ''`); the :10025 reference renders headings in **Manrope** (weights 500–700) and has no Inter Tight at all. **Changed 2026-09-15 (Bam: "lets just fix it up")**: `--th-font-display` is defined in `:root` of the ported sheet `uploads/sidemoney-port-v2.css` on the box (hand-ported static file, no repo source; backup `sidemoney-port-v2.css.bak-2026-09-15-intertight`) — set to `"Manrope"`. That file is served `immutable`, so the site setting `chromeCssUrl` was bumped to `/api/uploads/sidemoney-port-v2.css?v=3` (DB `settings.site`) AND the Redis settings cache `cache:v1:settings:*:site` had to be deleted before pages picked it up. Verified: home + product headings render Manrope, zero Inter Tight elements. Inter Tight is still in the Google Fonts link (unused now).
- **Banner captions / buttons** ("SHOP MEN", "IT COST US ALOT", "THE CITY SERIES AT FOOTLOCKER", Reserve Notes heading) = ported CSS (`uploads/sidemoney-port-v2.css`, `.th-page-1803` / `165012`) asks for **Roboto Condensed**; ~111 `.th-heading-title` rules on `.th-page-165613` ask for **Montserrat**. Live never loaded either → Arial/Helvetica fallback (Bam: "these fonts look off", screenshot of IT COST US ALOT). **Fixed 2026-09-15:** Google Fonts link in `storefrontHtml.ts` + `siteHtml.ts` now also loads Roboto Condensed, Roboto, Montserrat (100..900). Verified live: `document.fonts.check('700 28px "Roboto Condensed"')` true, banner spans resolve.
- Emails use the system stack on purpose (mail clients don't load webfonts reliably); the popup inherits the page font (Manrope).
- Leftover spotted: `settings.site.tagline` = "AuditTag" (August audit residue) — flagged to Bam, not changed.
- Trap: settings are cached in Redis (`cached('settings', key)`); a direct DB edit is invisible until the key is deleted or the admin saves the form.
- Trap: my rule scan for "Inter Tight" found nothing because headings use the CSS variable, not a literal family.
