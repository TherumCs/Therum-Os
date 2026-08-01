# Scope — Studio Agent + Host Advisor

Two features, one foundation. Written 2026-07-30, nothing built yet.

**Target host: local.** Therum OS runs in this folder, there is no VPS yet.
The advisor is written host-agnostic — it inspects whatever machine it runs
on — so the same code points at the Hostinger box later with no rewrite. The
consequence is that rules which only make sense on a deployed server (TLS
expiry, firewall, fail2ban, unattended-upgrades) must report **not applicable**
here rather than firing. An advisor that opens by complaining his Mac has no
firewall is noise, and noise is how a tool like this gets ignored.

## What already exists (build on it, don't duplicate)

Checked before scoping, because most of this turned out to be present:

| Piece | Where | State |
|---|---|---|
| MCP server | `src/api/routes/mcp.ts` | Real. JSON-RPC, protocol 2024-11-05, `tools/list` + `tools/call`. |
| Tool registry | `src/lib/mcpTools.ts` | 7 tools. `{name, description, inputSchema, write?, handler}`. |
| Scoped tokens | `src/services/apiToken.service.ts` | read/write scopes; write tools already require a write token. |
| Capability gate | `src/middleware/bundle.ts` | `requireBundle('manage-settings')`. |
| Preview-then-execute | `src/services/findReplace.service.ts` | `preview()` / `execute()` split — already the confirm pattern. |
| Credential vault | `src/services/connection.service.ts` | Encrypted at rest, masked, audited, `credentialFor()` never routed. |
| Audit rows | `ConnectionAuditLog` | Per-provider action log to copy for agent runs. |
| System checks | `src/services/system.service.ts` | Health checks, stops at the Node process. |
| Controlled exec | `src/services/backup.service.ts` | Uses `execFile` with an args array — no shell string. The precedent. |
| Bento dashboard | `admin/app/(app)/page.tsx` | 12-col grid, `{id, size}` cards, xs/sm/md/lg, drag-resize, per-user layout. |

**The consequence:** every agent tool is an entry in `mcpTools.ts`. It is then
reachable from the dashboard card AND from Claude Code locally over MCP, with
no second implementation. That is the whole reason to do it this way.

## Part 1 — Host Advisor

Lives in Settings. Reads the host, reports findings across security,
compression and performance, and explains them. Runs against the local stack
today; the same probes point at the VPS when there is one.

Every rule declares `scope: 'any' | 'deployed'`. A `deployed` rule on a local
host renders as "not applicable — local" and never counts as a finding.

### The rule that keeps it honest

**Checks are code. Narrative is the model.**

A finding is produced by a deterministic check with a sourced threshold. The
model orders findings, explains them in context, and writes the fix-up — it
never decides *whether* something is wrong. This is what stops the advisor
drifting into confident nonsense about a box it cannot see, and it means two
runs on an unchanged server produce the same findings.

Anything version- or price-dependent (package versions, current stable
releases, VPS tiers) is pulled live and cited, never recited from memory —
same source-router rule as everywhere else in this folder.

### Probes

The model never composes a command. It selects a probe by name; the server
runs a hardcoded `execFile` with a fixed args array. New probe = new registry
entry, reviewed like any other code.

`src/services/vpsProbe.service.ts`

```
os · cpu · memory · swap · loadavg · disk · inodes
listening-ports · firewall · ssh-config · fail2ban · pending-updates
file-perms · service-user
nginx-config · tls · http-headers · cache-headers · compression
postgres-config · postgres-slow-queries · postgres-indexes
redis-config · node-process · docker
```

Each: `{ id, axis, bin, args, parse(stdout) -> structured, timeoutMs, redact() }`.

`redact()` is not optional — `ssh-config` and `postgres-config` output can
carry hostnames, key paths and credentials. Redact before the payload is built,
not before display, because the payload is what leaves the box.

### Rule packs

`src/lib/vpsRules/{security,compression,performance}.ts`

Rule shape: `{ id, axis, severity, appliesTo(probe), check(data) -> Finding|null, why, fix, source? }`

**Security** — `.env` and key file permissions (world-readable is a finding);
Postgres and Redis bound to localhost rather than `0.0.0.0`; unexpected
listening ports; secrets present in tracked files; JWT/credential key strength;
CORS origin not `*`; security headers on responses the app itself serves.
*Deployed-only:* root SSH login, password auth, SSH port; firewall active and
rules sane; fail2ban; pending security patches; TLS expiry, protocol versions,
cipher suite; HSTS; service running as a non-root user.

The locally-meaningful half is the half that has actually bitten this project —
an unignored `.env`, a service on `0.0.0.0`, a route without an auth hook.

**Compression** — `gzip on` plus **`gzip_proxied any`** and `gzip_types`
coverage (this exact line is why compression silently did nothing on this
stack before); brotli available and enabled; static `Cache-Control` and
`immutable`; ETags; image formats and byte sizes; JS/CSS minified; bundle
sizes against a budget; HTTP/2 or HTTP/3.

**Performance** — CPU/RAM/swap headroom and load average; disk space and
inodes; Postgres `shared_buffers` / `work_mem` / `max_connections` against
actual RAM, slow queries, missing indexes on FKs, pool saturation; Redis
`maxmemory` and eviction policy; Node heap and worker count against vCPU;
nginx `worker_processes` / `worker_connections`; app TTFB; CDN in front of
static.

Every finding carries a concrete fix — a config diff or an exact command —
and is **never auto-applied**. Part 1 is read-only, end to end.

### Surface

- `GET /api/vps/probes` — what can be run
- `POST /api/vps/scan` — run probes, evaluate rules, return findings (`requireBundle('manage-settings')`)
- Settings → System → Advisor: findings grouped by axis, severity-sorted, each expandable to why + fix
- MCP tools: `vps_scan`, `vps_probe` (both read-only)

## Part 2 — Scoped edits: bricks and CSS only

File edits, not shell. Bam's scope, verbatim: "i would just just bricks / css
and thats it."

Three real surfaces, and they are not all files:

| Surface | Where | Notes |
|---|---|---|
| Bricks addons | `bricks-addons/` (`ADDONS_DIR`) | Files. |
| Ported chrome CSS | `uploads/*-tsc-chrome.css` | Files, ~1.1 MB each. |
| Per-user admin CSS | `adminUser.customCss` | **Database column, not a file.** Sanitized in `me.service.ts`. |

- **Containment already exists** — `readAddonFile()` in
  `bricksAddon.service.ts` does `safeJoinName()` plus a
  `startsWith(ADDONS_DIR)` check. Reuse it rather than writing a second path
  guard; two guards is one bug with two hiding places.
- Nothing outside those three. Not the repo root, not `admin/`, not `src/`,
  never `.env`.
- **Propose → diff → confirm → apply → commit.** Same shape as
  `findReplace.preview()/execute()`, which already works this way.
- One git commit per applied change, so revert is one command. `uploads/` is
  gitignored, so chrome-CSS edits need a sidecar copy of the previous version
  to be revertable — otherwise "revert" is a promise the system cannot keep.
- MCP tools: `read_file`, `list_files` (read); `propose_edit` (returns a diff,
  writes nothing); `apply_edit` (`write: true`, takes a proposal id).

`apply_edit` never runs off a model decision alone — it takes the id of a
proposal a human approved.

**Known trap:** `uploads/*-tsc-chrome.css` is partly generated by
`generate-live-diff.py`, and it has already been hand-edited once to fix font
URLs (see `_core/memory.md`). Agent edits there are lost if the generator is
re-run. The advisor should say so at edit time rather than letting the work
quietly disappear.

## The agent card

- Dashboard card, `{id: 'studio-agent'}`, existing size tiers. Compact tile =
  status, quick ask, recent runs. Expands to a full pane for real work.
- **Runs are server-side jobs with ids**, not socket-bound. The card
  subscribes. Collapsing the card, resizing it, or navigating away must not
  kill a run — retrofitting this later is expensive.
- Loop runs server-side using the Anthropic key from `credentialFor()`. The
  key never reaches the browser.
- Every tool call writes an audit row (actor, tool, args, result, duration),
  modelled on `ConnectionAuditLog`.
- **Run bounds, not a budget.** Dropped the budget setting — Bam pushed back
  ("idk why we need this") and he is right that a spend dashboard for a
  one-person install is overkill. What stays is a terminating bound, because
  an agent loop is a `while` loop: the model calls a tool, the output feeds
  back in, it calls again. Without a stop condition a confused run has no
  natural end — it re-reads the same file, or a rule pack returns 200 findings
  and each one round-trips. That is a hang, not an invoice.

  So: a max-steps and max-tokens ceiling per run, hardcoded defaults, no UI,
  no setting to configure. It surfaces only if a run hits it, as "stopped
  after N steps" rather than silent truncation.

## Non-negotiables

1. **Untrusted content and write tools never share a session.** Once a run has
   read product copy, an imported PDF, a contact-form message or a fetched
   page, that text can contain instructions. A run holding `apply_edit` or any
   exec tool must not also hold content-reading tools. Enforced by the tool
   set the run is issued, not by prompting.
2. **No shell composition, ever.** `execFile` with fixed args. No `exec`, no
   string interpolation, no model-supplied command text.
3. **The hidden knowledge directory lives outside the web root.** nginx serves
   this origin; a hidden dir underneath it is one misconfig from public.
4. **Part 1 applies nothing.** It reports. Fixes are copy-paste for a human.
5. **Least privilege.** Non-root service user; if any probe needs elevation,
   a named sudoers allow-list, not blanket sudo.

## Build order

1. Probe service + `vps_scan` MCP tool + Settings → System → Advisor (read-only)
2. Rule packs, one axis at a time — security, then compression, then performance
3. Agent card with runs-as-jobs, read-only tools only
4. Scoped file reads
5. `propose_edit` / `apply_edit` with the confirm flow

1 and 2 are independently useful and ship without any agent at all.

## Decisions — settled 2026-07-30

- **Host:** local, this folder. No SSH, no key in Nexus, plain `execFile`.
  Written host-agnostic so the VPS is a config change later, not a rewrite.
- **Editable:** bricks and CSS only — `bricks-addons/`,
  `uploads/*-tsc-chrome.css`, and the `customCss` column. Nothing else.
- **Budget:** dropped as a feature. Run bounds only, hardcoded, no UI.
- **VPS sizing:** not yet — thresholds stay relative (percentage of available
  RAM/vCPU) rather than tuned to a specific tier, so they hold on both the
  laptop and whatever gets bought.

Nothing outstanding. Ready to build.
