# Admin audit — logic gaps, dead controls, broken links

Run 2026-07-30 against the running admin. Method was the same as the storefront
audit: crawl and measure, not read and assume. Where a first result was wrong,
the correction is recorded rather than quietly dropped.

## 1. Does every control have something to save to?

Compared every `field=` the admin renders against the fields each settings
schema actually accepts, per domain.

**Dead controls: ZERO.** Nothing in the admin writes to a field the API would
reject.

Worth knowing though: **the API answers 200 to an unknown field.** The settings
schemas strip unknown keys rather than rejecting them, so a misspelled `field=`
would look like it saved and silently never persist. Nothing is broken today,
but the API will not catch it if it happens — which is why the static comparison
above is the check that matters.

## 2. Settings the API supports with no UI

30 remain. Split by whether they should have one:

| Domain | Fields with no control | Verdict |
|---|---|---|
| `commerce` | currency, locale | **FIXED** — added to Settings → Site |
| `seo-defaults` | siteName, siteDescription, siteLogo | **FIXED** — added to Settings → Site |
| `counter` | contactTopics | Real gap. Contact routing addresses are still edit-by-API. |
| `counter` | toolbarSearchPlaceholder | Minor. |
| `site` | chromeCssUrl, chromeHeaderSlug, chromeFooterSlug | Advanced; the ported chrome wiring. Deliberate for now. |
| `appearance` | ~14 (autoSave, bentoGap, bgImage, cardImage, cardTemplate, …) | Ported from 1.9.44. Stored and validated, controls never built. |
| `onboarding` | completed, step | Internal state. Correctly has no UI. |
| `import` | appearance, behavior | Internal payload. Correctly has no UI. |

Currency was the one that mattered: a store about to take real orders on a
domain had no way to set what it charges in, short of calling the API by hand.

## 3. Links and pages

Crawled 40 admin pages following every internal link.

- **No broken pages, no empty pages, no wrong redirects.** The two pages that
  showed a notice were informational banners ("Edition: Pure", "Native Bricks
  renderer active"), not errors.
- `/tos-admin/appearance` and `/tos-admin/settings` return 307 — correct, they
  redirect to a default section (`/appearance/theme`, `/settings/site`).
- Every storefront link reached from the admin resolves.

## 4. A source file was excluded from the repository

`.gitignore` line 14 read `uploads/`. Unanchored, so it matched **any**
directory called `uploads` at any depth — including
`admin/app/(app)/settings/uploads/`. The entire Uploads settings page was on
disk, working locally, and **not in the repository**. Nothing looked wrong; a
fresh clone simply would not have had that page.

Anchored to `/uploads/`. Verified both ways: the settings page is now tracked,
and the repo-root media directory is still ignored.

This is also what made the first pass of the audit report "uploads: 0 controls"
— the file was invisible to `git ls-files`.

## Corrections made during the audit

- A first pass reported 22 admin list pages with no row links. Most were false:
  content links rows to the builder, media opens a lightbox, milieus and
  promotions use in-page panels. Only **orders** was a genuine dead end, and
  only **products** lacked row actions. Both fixed before this audit.
- `minMarginPct` was reported as having no UI. It does — `MarginFloor.tsx`
  posts it directly rather than through a `field=` control, so the pattern
  match missed it.

## Still open, deliberately

- No admin UI for `counter.contactTopics` — contact-form routing addresses.
- ~14 appearance settings ported from 1.9.44 that are stored but have no
  control.
- Settings schemas accept unknown keys silently (see §1).
