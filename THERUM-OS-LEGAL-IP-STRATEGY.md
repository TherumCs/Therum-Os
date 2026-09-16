# Therum OS — Legal & IP Strategy

**Status:** working strategy + checklist, drafted 2026-08-14. **Not legal advice.**
This is the map you bring to a qualified IP attorney so the first meeting is
fast and you're not paying billable hours to explain what you built. Every item
marked **[ATTORNEY]** must be executed by licensed counsel — especially patents,
which are unforgiving about timing.

---

## 0. ⚠️ TIME-SENSITIVE — read this first

**sidemoney.co is now public, and it runs Therum OS in the open.** Public
disclosure of an invention starts (or in some places ends) your window to patent it:

- **United States:** a **1-year grace period** from first public disclosure /
  offer for sale to file. The clock effectively started at launch
  (**~2026-08-14**). Practical deadline to file at least a **provisional**:
  **before 2026-08-14 (2027).** Do not sit on it.
- **Most other countries (EU, etc.):** **absolute novelty** — any public
  disclosure *before* filing can bar a patent entirely. If international
  protection matters, filing should have preceded launch; talk to counsel
  **now** about what's still salvageable (e.g., filing a US provisional fast,
  then PCT within 12 months).

**Action this week:** book an initial consult with a patent attorney and ask the
single question — *"Given the site is already live, what's my real filing
window, and should we file a provisional immediately to lock a priority date?"*
A provisional is cheap, fast, and buys 12 months to decide on the full utility
filing. It is the cheapest insurance here.

Trademarks and copyright are **not** harmed by launching — those you can pursue
on a normal timeline. It's only patents that are on a clock.

---

## 1. The IP inventory — what Therum OS actually has worth protecting

Before choosing *how* to protect, name *what* exists. Rough buckets:

**Brand / names (→ trademark):**
- **Therum OS** (the platform/engine)
- **Counter** (commerce module), **Nexus** (credential vault), **Milieus**
  (member pricing/audiences), **Cluster** (product clustering)
- **Sidemoney / The Sidemoney Company** (the store brand — likely already
  in use; confirm ownership + register)
- Any logos, wordmarks, taglines

**Technical inventions (→ patent candidates / trade secrets):**
- The **product-card system** — three independent axes (shell / media / preset)
  composed at render, with graceful fallback when a product can't support a
  style. This composition doesn't exist off-the-shelf.
- **Cluster merge with distinct swatches** — collapsing multiple vendor
  product-pushes into one storefront card, with split-gradient swatches so
  same-color variants stay distinguishable instead of collapsing.
- **Variant→image swatch binding** pipeline (per-color imagery bound from
  unlabeled vendor mockups).
- The **WooCommerce-parity compatibility bridge** (`wooCompat`) — a non-WordPress
  backend that speaks WooCommerce's wire protocol byte-for-byte so POD partners
  connect as if it were a real Woo store.
- The **closed-world folder / loop / second-brain operating model** — how the
  AI agent is constrained to an authored source-of-truth (arguably the most
  novel and defensible thing here; may be method + trade-secret rather than patent).

**Written/creative works (→ copyright, automatic):**
- The entire Therum OS codebase (all three apps)
- Brand copy, product descriptions, editorial, the design system

**Confidential know-how (→ trade secret):**
- Anything above that is **not** publicly visible (server architecture, the
  compat internals, prompts, the agent operating rules, pricing logic).

---

## 2. Protection strategy by type

### 2a. Trademarks **[ATTORNEY]** (normal timeline)
- File US trademark applications (USPTO) for **Therum OS** and the module names
  you'll take to market. File based on **use in commerce** where you're already
  using them, **intent-to-use** where not yet.
- Run **clearance searches first** (USPTO TESS + common-law) to make sure the
  names aren't already taken — before spending on filing or printing.
- Register the **word mark** (the name in any font) first; add logo/design marks
  if the logo is core.
- Lock the **domains + social handles** for every name you intend to keep.
- Add ™ to unregistered marks now; ® only after registration issues.

### 2b. Patents **[ATTORNEY — URGENT, see §0]**
- **File a provisional patent application** ASAP to stamp a priority date on the
  technical inventions in §1. One provisional can cover several related
  inventions. ~cheap, buys 12 months.
- Within 12 months, decide on **utility (non-provisional)** filings for the
  strongest candidates, and **PCT** if you want a shot at international.
- Attorney will assess **patentability** (novel + non-obvious + eligible subject
  matter — software patents are doable but need to be framed as a technical
  improvement, not an abstract idea). Not everything will qualify; the product-
  card composition and the compat bridge are the strongest-sounding candidates.
- **Do not publish deeper technical detail** (architecture write-ups, how the
  compat works internally) until counsel says the filing is in.

### 2c. Copyright (automatic, but formalize)
- Copyright exists the moment code/content is written — but **registration**
  (US Copyright Office) is what lets you sue for statutory damages. Register the
  core codebase and key creative works.
- Put a **© notice + LICENSE** in the repo. Decide the license posture:
  all-rights-reserved/proprietary (default for a product you're selling) vs. any
  open-source component boundaries.
- **Audit third-party/open-source dependencies** for license compatibility
  (nothing viral like GPL sneaking into proprietary core).

### 2d. Trade secrets (free, but only if you actually keep them secret)
- Anything not disclosed stays protected **as long as you take reasonable steps
  to keep it secret**: access controls, `.env` out of git (already done), NDAs
  before showing internals, "confidential" marking on sensitive docs.
- The agent operating model + prompts + compat internals are prime trade-secret
  material — protect by *not* publishing them, rather than by patenting.

---

## 3. Ownership, entity & leadership **[ATTORNEY]**

Protection is worthless if ownership is murky. Nail this:

- **Form the entity** that will *own* Therum OS (LLC or, if you'll raise money,
  Delaware C-corp). The IP should be owned by the company, not scattered across
  personal names.
- **Assign all IP to the entity.** Founders and **every contributor/contractor**
  who touched the code or brand must sign an **IP assignment**. Without it, a
  contractor can own what they built. Close this gap before going public/raising.
  - (Note: work produced with an AI assistant — clarify with counsel how that's
    treated; the human-authored contributions and the assembled product are what
    you own and assign.)
- **Founders' agreement / operating agreement** — equity split, roles,
  vesting, what happens if someone leaves. "Get our leadership together" =
  this document + who holds what.
- **Confirm the "Therum" name is clear** to use as a company/product name
  (trademark + entity-name conflict checks).

---

## 4. Pre-public (scale/PR/fundraise) legal checklist

Before you *promote Therum OS itself* as a product (vs. quietly running your
own store on it):

- [ ] Provisional patent filed (or explicit attorney sign-off that you're skipping it)
- [ ] Trademarks filed for the names you'll market
- [ ] Entity formed; all IP assigned to it; contributor assignments signed
- [ ] Repo LICENSE + copyright notices in place; dependency licenses audited
- [ ] Privacy Policy + Terms of Service for the live store (you're taking
      emails, phone numbers, payments — this is required, not optional)
- [ ] Payment/PCI posture confirmed (card data never touches your origin — the
      hosted-field design already handles this; document it)
- [ ] Data handling / customer-data policy (esp. the pickup emails+phones you collect)
- [ ] Trade-secret hygiene: NDAs ready before showing internals to anyone

---

## 5. Prioritized next actions

1. **Book a patent attorney consult this week** — the disclosure clock is the
   only true deadline (§0).
2. **Trademark clearance + filing** for Therum OS + core module names (§2a).
3. **Form the entity + sign IP assignments** (§3) — do before any fundraise or
   public product push.
4. **Privacy Policy + ToS live on sidemoney.co** (§4) — you're already collecting
   personal data, so this one is overdue independent of everything else.
5. Copyright registration + repo license/notices (§2c).

## What to bring to the attorney
- This document.
- A one-paragraph plain-English description of each invention in §1.
- The launch date (2026-08-14) and confirmation the site is public.
- List of everyone who contributed code/brand and their status (employee /
  contractor / founder) — for the assignment gap analysis.

---

*Reminder: I'm an AI assistant, not a lawyer. Treat this as preparation, not
counsel. The patent timing in §0 is the item most likely to cost you if it
slips — verify it with a real attorney immediately.*
