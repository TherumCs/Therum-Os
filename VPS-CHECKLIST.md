# VPS checklist — what happens once the box exists

Written 2026-07-31, while still local. Everything here is blocked on having a
real Linux host and a domain; none of it can be done or verified from a laptop.

Order matters: each block assumes the one above it worked. Nothing here is
guesswork about what the code does — the advisor rule ids are the real ones
from `hostAdvisorService`, and the deploy steps come from `DEPLOY.md`.

---

## 1 · Provision and get code running

- [ ] Buy the box. Hostinger KVM 4 (4 vCPU / 16 GB / 200 GB NVMe) is the plan
      of record from `_core/memory.md`.
- [ ] Ubuntu 24, non-root sudo user, SSH key installed. **Confirm key login in
      a second terminal before disabling passwords** — locking yourself out of
      a fresh box is the classic way to lose an afternoon.
- [ ] Install Node (current LTS), PostgreSQL 16, Redis, nginx, PM2, certbot.
- [ ] Clone the repo. `npm ci` in the root and in `admin/`.
- [ ] **Generate FRESH secrets on the box** — do not copy them from local:
      `JWT_SECRET`, `CREDENTIAL_KEY`, `WEBHOOK_SECRET` (`openssl rand -base64 48`).
      `JWT_SECRET` must be identical in `.env` and `admin/.env`, or every admin
      login fails signature verification.
- [ ] `chmod 600` both env files.
- [ ] `prisma migrate deploy` — **not** `migrate dev`, which can prompt and can
      reset. 37 migrations should apply cleanly (count checked 2026-07-31 — if
      the repo has moved on, trust `ls prisma/migrations`, not this line).
- [ ] `prisma generate`. Skipping this is what produced
      "Unknown argument `shippingTotal`" locally after a schema change.
- [ ] **Install the sudo grant for the Server panel**:
      `sudo cp deploy/therum-sudoers /etc/sudoers.d/therum` (edit the username
      first), `chown root:root`, `chmod 440`, then **`sudo visudo -c` must print
      "parsed OK" before you close the session** — a malformed sudoers file
      locks out sudo for everyone. Without this the panel's privileged actions
      fail with a message telling you exactly this; nothing silently half-works.
- [ ] Confirm in Settings → Server that the actions are no longer greyed out,
      and run **Test the nginx config** as the first proof the grant works.
- [ ] PM2: the API, the admin, **and `src/worker.ts`**. The worker is the one
      `DEPLOY.md` flags as never wired — without it, queued imports sit forever
      and nothing says so.

## 2 · Domain, TLS, nginx

- [ ] DNS A/AAAA to the box. Wait for propagation before certbot.
- [ ] `deploy/nginx.conf` installed. **It has never served a real domain** —
      expect to fix paths and server names on first load.
- [ ] certbot for the storefront and the admin host.
- [ ] `nginx -t`, then reload.
- [ ] Confirm `https://` serves the storefront and `/tos-admin` reaches the
      admin behind auth.
- [ ] Set `PUBLIC_ORIGIN` — receipt emails build their "View your order" link
      from it, and it is null-safe, so a wrong value means receipts quietly
      ship without the link.

## 3 · Run the advisor — the real hardening pass

Settings → Advisor → Run scan. **These 12 rules have never executed anywhere.**
They are unit-tested against synthetic payloads only; this is the first time
they run against a real host, so treat surprises as equally likely to be a bug
in the rule as a problem with the box.

Security:
- [ ] `sec.prod-node-env` — `NODE_ENV=production`
- [ ] `sec.ssh-root` — `PermitRootLogin no`
- [ ] `sec.ssh-password` — `PasswordAuthentication no` (key login confirmed first)
- [ ] `sec.firewall` — ufw active; 80/443/22 only
- [ ] `sec.exposed-ports` — nothing but 80/443/22 on `0.0.0.0`; Postgres and
      Redis on `127.0.0.1`
- [ ] `sec.updates` — apply pending security patches, enable unattended-upgrades
- [ ] `sec.tls-expiry` — cert valid, `certbot renew --dry-run` passes, timer on
- [ ] `sec.hsts` — add **only after** https is confirmed working; it is sticky
      in browsers and a premature one locks visitors out of a broken cert

Compression (all three are nginx's job — `@fastify/compress` was tried and
reverted after it served every page as 0 bytes):
- [ ] `cmp.html-uncompressed` — `gzip on` **and `gzip_proxied any`**. That
      second line is the one that was missing before; without it nginx will not
      compress a proxied response, which is every page here.
- [ ] `cmp.no-cache-headers` — `Cache-Control` on HTML, long + immutable on
      hashed static assets
- [ ] `cmp.no-brotli` — optional, after gzip works

Performance:
- [ ] `perf.memory-pressure` — reads `MemAvailable`, which only exists on
      Linux. This rule has **never once produced a number**; the VPS is where it
      first does.
- [ ] Tune to the box you actually bought: Postgres `shared_buffers` ≈ 25% of
      RAM, `effective_cache_size` ≈ 50–75%; Redis `maxmemory` +
      **`volatile-lru`** (currently unlimited with `noeviction`, which is how
      the OOM killer ends up taking Postgres instead of Redis). See §6b for why
      it must not be `allkeys-lru` on this stack.

## 3b · Connect Hostinger itself

Not another store integration — the provider that owns the machine. Everything
in §3 and the Server panel runs ON the box and dies with it; this is the way
back in when it is wedged.

- [ ] hPanel → **Dev Tools → API → Generate Token**. It is shown once.
- [ ] Paste it into **Connections → Hostinger**.
- [ ] Settings → Server → **The machine itself** should now list the VPS with
      its state and IP. If it lists nothing, the token is scoped to a different
      account rather than broken.
- [ ] Take one **snapshot** before you touch anything else, and know that
      Hostinger keeps ONE per machine — a second snapshot replaces the first.
- [ ] Do **not** test Hard restart on a box you are mid-install on. It is a
      hypervisor-level reset, not a clean shutdown.

## 4 · Connect what only works on a real host

These are the ones that cannot be done locally at all — the reason they were
never blockers to getting here.

- [ ] **Square** in Connections (Nexus). The gateway is built and registered;
      it reports `setupRequired: true` until its credential exists.
- [ ] **Email provider** in Nexus — Resend, SendGrid or Postmark — or SMTP in
      Settings → Notifications. The page now states which transport a send would
      actually use; confirm it does not say "nothing connected".
- [ ] Send a test notification and confirm it arrives.
- [ ] Printful: once catalog lines carry Printful variant ids, live shipping
      rates replace the configured flat rates automatically. Until then the
      Standard/Express/Overnight defaults are what shoppers see.
- [ ] Any webhook the providers need — public URL now exists, which is the
      whole reason these waited.

## 5 · Data and content

- [ ] Sync products. The four nav categories (`mens`, `womens`,
      `kids-playmoney`, `home-house-money`) and `accessories` currently hold
      **0 products**, so those header links land on empty pages. Re-check after
      the sync — an empty category reads as a broken store.
- [ ] Set `currency` and `locale` in Settings → Site if not USD.
- [ ] Set `taxRatePct` if you are charging tax and no provider quotes it. It
      defaults to 0 deliberately — no store should start charging a rate nobody
      chose.
- [ ] Contact topics: four still fall back to `info@`. There is no admin UI for
      `counter.contactTopics` yet; it is edit-by-API.
- [ ] Backups: destination is `local`. Point at S3 (bucket, region, keys are
      already fields) so a dead box does not take the backups with it.

## 6 · Prove it end to end

Not "does the page load" — does a stranger's money reach you.

- [ ] Place a real order as a customer: add to cart → checkout → address →
      **pick a shipping method and watch the total change** → pay with Square.
- [ ] Confirm the receipt email arrives, and that it shows items, discount,
      shipping (with the method), tax and total.
- [ ] Confirm the order in the admin shows the same breakdown and the shipping
      address.
- [ ] Refund it. Confirm the refund notice sends.
- [ ] **Delete the test order and any test products** before real traffic —
      standing rule in `CLAUDE.md`.

## 6b · Server hardening and tuning

Everything above gets the store working. This is what makes it survive being
public. Ordered by what actually bites an ecommerce box first.

### Clock — do this early, it breaks auth silently

- [ ] `timedatectl set-ntp true`, confirm `systemctl status systemd-timesyncd`.
      This is not housekeeping here: **2FA (TOTP) and webhook signature
      verification are both time-windowed**. A box that drifts a minute starts
      rejecting valid admin logins and valid PSP webhooks, and the errors point
      everywhere except the clock.

### Kernel and system limits

- [ ] Swap: 2 GB file even with 16 GB RAM. Not for speed — so a spike degrades
      instead of the OOM killer taking Postgres.
- [ ] `vm.swappiness=10` — swap exists as a safety net, not a first resort.
- [ ] `fs.file-max` and a systemd `LimitNOFILE=65535` for the Node services.
      nginx + Node + Postgres + Redis on one box runs out of file descriptors
      before it runs out of anything else.
- [ ] `net.core.somaxconn=1024`, `net.ipv4.tcp_max_syn_backlog=2048` — the
      default accept queue is small enough to drop connections during a
      traffic burst that the box could otherwise serve.

### SSH

- [ ] Key-only (already in §3), plus `MaxAuthTries 3`, `AllowUsers <you>`,
      `LoginGraceTime 30`.
- [ ] Moving off port 22 stops log noise, not a real attacker. Do it for the
      quieter logs, do not count it as security.

### Firewall and intrusion

- [ ] ufw: deny incoming, allow 80/443/SSH. Nothing else public — Postgres
      (5432) and Redis (6379) stay on `127.0.0.1`.
- [ ] fail2ban with the `sshd` jail, plus an nginx jail for repeated 401/429s
      against `/tos-admin` and the login route.
- [ ] The app already rate-limits login, checkout and order creation in Redis
      (`ratelimit:*` keys). fail2ban is the layer below it — it stops the
      traffic before Node has to think about it.

### TLS and nginx

- [ ] TLS 1.2 and 1.3 only. Disable everything below — an ecommerce site
      accepting TLS 1.0/1.1 fails a PCI scan on sight.
- [ ] Modern cipher suite, `ssl_prefer_server_ciphers off`, OCSP stapling on.
- [ ] HTTP/2 (`listen 443 ssl http2`). HTTP/3 optional.
- [ ] `ssl_session_cache shared:SSL:10m` — TLS handshakes are the most
      expensive thing a first-time visitor does.
- [ ] `client_max_body_size` sized for media uploads (the admin uploads images;
      the default 1 MB will reject them with a confusing 413).
- [ ] `limit_req_zone` on `/api/` and the login route as a blunt second layer.
- [ ] Security headers (the advisor checks these): `X-Content-Type-Options`,
      `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, and a CSP
      built LAST and tested against the storefront — a wrong CSP is a blank
      page, which is worse than no CSP.
- [ ] `proxy_hide_header X-Powered-By`, `server_tokens off`.
- [ ] Static assets: long `max-age` + `immutable` for hashed files, and
      `Cache-Control: no-store` for `/tos-admin` — never let an admin page or
      an API response sit in a shared cache.

### PostgreSQL

- [ ] Dedicated least-privilege role for the app. Not the superuser, not
      `postgres`.
- [ ] `listen_addresses = 'localhost'`, and `scram-sha-256` in `pg_hba.conf`.
- [ ] `shared_buffers` ≈ 25% RAM, `effective_cache_size` ≈ 50-75%,
      `work_mem` modest (it is PER SORT, per connection — the classic way to
      OOM a box is a generous work_mem times a large max_connections).
- [ ] `max_connections` low (100-ish) and let the pool queue. Prisma opens a
      pool per process; PM2 cluster mode multiplies it. **Count them:
      workers × pool size must stay under max_connections**, or the app
      exhausts the database on its own with no traffic at all.
- [ ] Autovacuum on. Orders, carts and audit logs churn.
- [ ] `log_min_duration_statement = 500ms` so slow queries surface before a
      customer reports them.

### Redis

- [ ] `bind 127.0.0.1`, `requirepass`, `protected-mode yes`.
- [ ] `maxmemory` a fixed share of RAM, and **`maxmemory-policy volatile-lru`,
      NOT `allkeys-lru`**. This Redis is not only a cache: it holds carts
      (7-day TTL), rate-limit counters (TTL) and **BullMQ job data, which has
      no TTL at all**. `allkeys-lru` would evict queued imports and backups
      silently. `volatile-lru` only evicts keys that carry an expiry, so
      pressure sheds carts — annoying and recoverable — and leaves the queues
      alone.
- [ ] Persistence ON (AOF `everysec`). Carts live only in Redis: a restart
      without persistence empties every active shopper's basket.
- [ ] Rename or disable `FLUSHALL` / `FLUSHDB` / `CONFIG` in production.

### Node and PM2

- [ ] PM2 cluster mode for the API, sized to vCPU — but see the max_connections
      arithmetic above before picking a number.
- [ ] `max_memory_restart` so a leak recycles instead of taking the box.
- [ ] `pm2 startup` + `pm2 save` — services must come back after a reboot
      without you.
- [ ] `pm2-logrotate`. Unrotated logs are a slow-motion disk-full outage, and
      disk-full stops Postgres accepting writes.

### CDN / edge (optional, and worth it)

- [ ] Cloudflare (or similar) in front: DDoS absorption, bot filtering, and
      static caching at the edge.
- [ ] If you use one, restrict the origin firewall to its IP ranges — otherwise
      the origin is still directly reachable and the edge is decoration.
- [ ] Do NOT cache `/tos-admin`, `/api`, `/cart`, `/checkout` at the edge.

### Backups and monitoring

- [ ] Automated `pg_dump` on a schedule, **off the box** (S3). A backup on the
      same disk is not a backup.
- [ ] Retention + a restore you have actually run. Untested backups are a
      belief, not a plan.
- [ ] Uptime check on the storefront AND on `/health`.
- [ ] Disk-space alert at 80%. Disk-full is the most common way this class of
      box dies, and the advisor only tells you when you go looking.

### Ecommerce specifics

- [ ] **Never store card data.** Square hosts the payment page; keep it that
      way and PCI scope stays small.
- [ ] Confirm PSP webhooks verify signatures (the code does) and that the
      endpoint is reachable from the internet but rate-limited.
- [ ] Keep webhook handling idempotent — PSPs retry, and a double-applied
      payment or refund is real money.
- [ ] Test the whole path once more from a phone on cellular, not just from
      the office network.

## 7 · After it is live

- [ ] Re-run the advisor. It should be 0 critical / 0 high.
- [ ] Enable GitHub push protection on the repo (still outstanding; `gh` is not
      authenticated locally).
- [ ] Take a full backup — code, `.env`, and a `pg_dump` — and confirm the
      restore steps actually work on the box, not just on paper.

---

## Known-unproven, carried into production

Say these out loud on the day rather than discovering them:

- The 12 advisor rules above have never run.
- `deploy/nginx.conf` has never been loaded by a real nginx.
- The BullMQ worker has never drained a queue in production.
- Extension JS runs **in-process** — no sandbox. Fine while every extension is
  ours; not fine if that changes.
- Printful shipping rates have never been quoted live; the flat-rate fallback
  is what has actually been exercised.
