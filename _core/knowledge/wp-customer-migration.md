---
name: wp-customer-migration
description: "WordPress customers + orders imported into prod, the new Customers admin section, and first/last name support"
metadata: 
  node_type: memory
  type: project
  originSessionId: f4504c37-caac-4f64-affa-6039105bec50
  modified: 2026-08-19T03:30:19.790Z
---

2026-08-18, therum-cms-2 (live store).

**Migrated from :10025 WordPress → prod:** 55 customers + 53 orders (all real ones; audit-*/test junk filtered). Idempotent — orders carry `sourceId='wp:<wpPostId>'` (re-run skips existing), customers carry `meta.source='wp-migration'`. WP order dates preserved (`createdAt`), status mapped (wc-completed→delivered etc.), line items snapshotted to `order.meta.wpItems` (WP products don't map to v2 variants, so NO OrderItem FK rows — historical record only). Migrated customers have **no login identity** — they claim their account via the new forgot-password / email-code flows. Done as **direct Prisma inserts (zero emails)** per Bam's rule.

**IMPORTANT pending:** Bam will review all customers and tell me (a) which get Friends & Family (assign via the new Customers page), (b) which to email. **Do NOT send welcome/any emails to migrated customers until he says.**

**Dedup + F&F cleanup (2026-08-18):** merged 6 duplicate people (same name / same email-root, plus Nantale = gooliegirl2000@comcast.net↔njn2105 which Bam flagged) → 53 customers; merged-away emails recorded in the primary's `meta.mergedEmails`. Also found + removed **29 migrated customers wrongly assigned Friends & Family (40%)** — migrated customers must have NO discount/group until Bam assigns. F&F back to the 4 real accounts. My dup scan only catches same-name / same-email-root; person-specific dups (name AND email both differ) need Bam to flag.

**Customer model gained** `firstName`/`lastName` (`first_name`/`last_name` cols, additive DDL applied to prod). `name` = freely-editable display name / username (unlimited changes); first/last = real name for back office. Migration populated first/last from WP billing names.

**Dashboard redesign (2026-08-18, Bam-approved Neka bento direction):** `admin/app/(app)/page.tsx` (server, fetches data) → `DashboardTabs.tsx` (client, tabs + bento + inline `<style>`). Four tabs: Overview (site-wide), Counter (commerce, reads /counter/activity), Content (pages/posts/journal), Growth (attribution + abandoned carts + issues + Studio AI). A `+` adds custom dashboards (localStorage, v1). Sidebar deliberately NOT touched. Theme-aware via the admin's `[data-color-mode='dark']`. Gradient tiles + big numbers = the "less WordPress" look.

**Admin gotcha (cost a debugging round):** the Next admin has NO catch-all `/api` proxy — every client-called endpoint needs its OWN `admin/app/api/<path>/route.ts` that calls `proxyToBackend(...)`. A new admin page whose client `fetch`es `/tos-admin/api/<x>` will 404 silently (never reaches the backend) until that route handler exists. The Customers page shipped without `app/api/customers/route.ts` + `[id]/route.ts`, so name edits silently failed. Also: `API_URL` differs from the docs — backend runs on **:10009**, not :4100.

**New admin section: Counter › Customers** (`admin/app/(app)/customers/`, nav in `admin/lib/nav.ts`). Lists every customer with their milieu groups (view + quick-set inline via `/milieus/:id/members`), order count, and inline edit of display/first/last (`PATCH /api/customers/:id` → `customerService.update`). No card data shown. `customerInclude` now carries memberships + `_count.orders`.

**Storefront account Details redesigned** (`accountPage.ts`): unified the two clashing input styles into one field style (was 14px vs 15px, no radius); Name row rebuilt into a clean Profile form (display name + first + last + read-only email), saved via `PATCH /shop/account/profile` (now accepts name/firstName/lastName; `/shop/account/me` returns them).

See [[store-attribution-and-feed]], [[live-store-real-money]].

**Friends & Family invites — how to do one (2026-09-20, Fresco).** Bam gives an email + first name. Steps that worked: (1) look the email up first — it may already be a migrated customer under a different name (`fresco.pbm@gmail.com` was "Terrence Jones", wp-migration, 1 order; Bam's name wins → set `customer.name`); (2) `customerService.create` only if missing; (3) `milieuService.assign(<friends-family milieu id>, { customerId, source: 'manual' })` — a NEW membership auto-fires `lifecycleService.sendFriendsFamilyWelcome`, but it is fire-and-forget, so in an ad-hoc script it dies with `process.exit` — call `sendFriendsFamilyWelcome` explicitly and wait ~8s before exiting; (4) prove delivery in Gmail's `[Gmail]/Sent Mail` (or Postmark activity once approved) and that the body greets with the right first name. F&F milieu id `cmsyqq76v000025kzi0arn4tx`, 26 members after Fresco. The F&F template (`welcomeFriendsFamilyHtml`) still contains em dashes — Bam has not asked to change transactional templates; flag, don't touch.
