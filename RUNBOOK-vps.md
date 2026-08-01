# VPS runbook — Hostinger KVM 2, Ubuntu 24.04 LTS

Copy-paste, in order. Written for **KVM 2: 2 vCPU / 8 GB / 100 GB NVMe** — every
memory number below is derived from 8 GB and is wrong for a different box. If
you resize later, redo §7.

`VPS-CHECKLIST.md` is the checklist version of this, with the reasoning. This
file is the commands.

Two rules that will save you an afternoon:

1. **Keep a second SSH session open** from the moment you touch SSH or the
   firewall until you have proved a NEW session can connect. Every lockout
   happens to someone who had one terminal.
2. **Snapshot before anything destructive.** hPanel → Snapshots, or the Server
   panel once Hostinger is connected. Hostinger keeps ONE per machine.

Replace `you`, `example.com` and `1.2.3.4` throughout.

---

## 1 · First login and a user that is not root

From your Mac:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@1.2.3.4
```

Then on the box:

```bash
adduser you
usermod -aG sudo you
rsync --archive --chown=you:you /root/.ssh /home/you
```

**Now open a second terminal and prove it works before continuing:**

```bash
ssh you@1.2.3.4
```

## 2 · Lock down SSH

```bash
sudo sed -i.bak 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sshd -t && sudo systemctl reload ssh
```

`sshd -t` is not optional. It parses the file before the reload; without it a
typo ends your access with the next disconnect.

## 3 · Firewall — allow SSH *before* enabling

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
sudo ufw status verbose
```

Postgres (5432) and Redis (6379) are deliberately absent. They bind to
`127.0.0.1` and must never be reachable from the internet — the advisor's
`sec.exposed-ports` rule checks exactly this.

## 4 · Patches, automatic and ongoing

```bash
sudo apt update && sudo apt -y upgrade
sudo apt -y install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

Unattended-upgrades is the single highest-value thing on this page. A box that
patches itself beats a box you promise to patch.

## 5 · fail2ban — stop the SSH brute force

```bash
sudo apt -y install fail2ban
sudo tee /etc/fail2ban/jail.local >/dev/null <<'EOF'
[sshd]
enabled  = true
maxretry = 5
findtime = 10m
bantime  = 1h
EOF
sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd
```

With password login already off this is belt and braces, but it also keeps the
auth log readable — an unbanned scanner generates thousands of lines a day.

## 6 · The stack

```bash
# Node (current LTS via NodeSource)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt -y install nodejs

sudo apt -y install postgresql postgresql-contrib redis-server nginx certbot python3-certbot-nginx git
sudo npm install -g pm2

node -v && psql --version && redis-server -v && nginx -v
```

### Database and role

```bash
sudo -u postgres createuser --pwprompt therum
sudo -u postgres createdb --owner=therum therum_cms
```

Keep that password — it goes in `DATABASE_URL` next.

## 7 · Tune Postgres and Redis for 8 GB

These are the numbers for KVM 2. On a different plan, recompute: shared_buffers
≈ 25 % of RAM, effective_cache_size ≈ 50–75 %.

```bash
sudo -u postgres psql -c "ALTER SYSTEM SET shared_buffers = '2GB';"
sudo -u postgres psql -c "ALTER SYSTEM SET effective_cache_size = '5GB';"
sudo -u postgres psql -c "ALTER SYSTEM SET work_mem = '16MB';"
sudo -u postgres psql -c "ALTER SYSTEM SET maintenance_work_mem = '256MB';"
sudo -u postgres psql -c "ALTER SYSTEM SET max_connections = '100';"
sudo systemctl restart postgresql
```

`shared_buffers` needs a **restart**, not a reload. Until you restart, the
running value is still the 128 MB default.

Redis:

```bash
sudo tee -a /etc/redis/redis.conf >/dev/null <<'EOF'

# Therum OS
maxmemory 2gb
maxmemory-policy volatile-lru
appendonly yes
EOF
sudo systemctl restart redis-server
redis-cli config get maxmemory-policy
```

**`volatile-lru`, never `allkeys-lru`.** Carts and rate limits carry a TTL and
are safe to evict. BullMQ job data does not carry one — `allkeys` would silently
drop queued work under memory pressure, and nothing would report it.

**`appendonly yes`** matters for the same reason: Redis holds the job queue, so
a reboot without an append-only file loses whatever was queued. RDB snapshots
alone can lose the last minutes.

## 8 · Deploy the app

```bash
cd /home/you
git clone git@github.com:TherumCs/Therum-OS-2.0.git therum
cd therum
npm ci
cd admin && npm ci && cd ..
```

**Generate fresh secrets on the box. Never copy them from the laptop.**

```bash
openssl rand -base64 48   # JWT_SECRET
openssl rand -base64 48   # CREDENTIAL_KEY
openssl rand -base64 48   # WEBHOOK_SECRET
```

Write `.env` (root) and `admin/.env`. `JWT_SECRET` must be **identical in both**
or every admin login fails signature verification.

```bash
chmod 600 .env admin/.env
npx prisma migrate deploy    # NOT migrate dev — that one can prompt and reset
npx prisma generate
npm run build
cd admin && npm run build && cd ..
```

`prisma generate` after `migrate deploy` is not optional: skipping it is what
produces "Unknown argument" errors against columns that plainly exist.

```bash
pm2 start ecosystem.config.cjs
pm2 save
pm2 startup            # run the command it prints
pm2 status
```

Three processes: `therum-cms-api`, `therum-cms-admin`, `therum-cms-worker`. If
the worker is missing, queued imports sit forever and nothing says so.

## 9 · nginx and TLS

Point your DNS A record at `1.2.3.4` and **wait for it to propagate** before
running certbot — it validates over HTTP against the live name.

```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/therum
sudo ln -s /etc/nginx/sites-available/therum /etc/nginx/sites-enabled/therum
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
```

This config has never served a real domain. Expect to fix `server_name` and
paths on the first `nginx -t`. Then:

```bash
sudo systemctl reload nginx
sudo certbot --nginx -d example.com -d www.example.com
sudo certbot renew --dry-run
```

Compression — nginx's job, and the reason `cmp.html-uncompressed` fires:

```nginx
gzip on;
gzip_proxied any;          # WITHOUT THIS, nothing proxied is compressed —
                           # which is every page this app serves
gzip_types text/plain text/css application/json application/javascript
           text/xml application/xml image/svg+xml;
gzip_min_length 1024;
```

Then set `PUBLIC_ORIGIN=https://example.com` in `.env` and
`pm2 reload therum-cms-api`. Receipt emails build their "view your order" link
from it and are null-safe, so a wrong value ships receipts with no link rather
than failing loudly.

## 10 · Daily backups

The app already backs itself up — `pg_dump` plus `uploads/` into one zip. Turn
it on in **Settings → Backups** and point it at S3 (or any S3-compatible
bucket: Backblaze B2, Cloudflare R2, Wasabi).

**A backup that lives only on the box is not a backup.** The failure it has to
survive is the box dying.

Belt and braces, a database-only dump on its own schedule:

```bash
sudo -u postgres mkdir -p /var/backups/therum
sudo tee /etc/cron.daily/therum-db >/dev/null <<'EOF'
#!/bin/sh
set -e
STAMP=$(date +%F)
sudo -u postgres pg_dump therum_cms | gzip > /var/backups/therum/therum_cms-$STAMP.sql.gz
find /var/backups/therum -name '*.sql.gz' -mtime +14 -delete
EOF
sudo chmod +x /etc/cron.daily/therum-db
sudo /etc/cron.daily/therum-db && ls -lh /var/backups/therum
```

Also enable Hostinger's own snapshots in hPanel. Three layers, three failure
modes: the app zip restores content, the SQL dump restores the database alone,
the snapshot restores the whole machine.

**Test a restore before you need one.** An untested backup is a hypothesis.

## 11 · Connect Hostinger to the panel

hPanel → **Dev Tools → API → Generate Token** (shown once), then paste it into
**Connections → Hostinger**.

Settings → Server → *The machine itself* then lists the VPS with state and IP,
and Hard restart and Snapshot start working. This is the section that keeps
working when the box does not — everything else on that page runs on the
machine and dies with it.

## 12 · The sudo grant, so the panel can act

```bash
sudo cp deploy/therum-sudoers /etc/sudoers.d/therum   # edit the username first
sudo chown root:root /etc/sudoers.d/therum
sudo chmod 440 /etc/sudoers.d/therum
sudo visudo -c
```

**`visudo -c` must print "parsed OK" before you close that session.** A broken
sudoers file removes sudo for everyone, and fixing it needs the root console.

Then in Settings → Server, run **Test the nginx config**. It is the cheapest
proof the grant works.

## 13 · Run the advisor

Settings → Advisor → Run scan. Twelve of those rules have never executed
anywhere — firewall, SSH, TLS expiry, pending updates, exposed ports, HSTS,
`NODE_ENV`. This is their first real run, so treat a surprise as equally likely
to be a bug in the rule as a problem with the box.

Work the findings worst-first. Most now have a button on the Server page.

**HSTS last, and only after https is confirmed working.** Browsers cache it
hard; a premature HSTS header on a broken certificate locks visitors out of
your site for as long as the max-age says.

## 14 · Prove it end to end

Not "does the page load" — does a stranger's money reach you.

1. Connect **Square** and an **email provider** in Connections (both needed the
   live domain, which is why they waited).
2. Sync products from Printful.
3. Place a real order: add to cart → checkout → address → pick a shipping
   method and watch the total change → pay.
4. Confirm the receipt email arrives and shows items, discount, shipping with
   its method, tax and total.
5. Refund it.
6. **Delete the test order and any test products.** Standing rule.

## 15 · Ongoing

| When | What |
|---|---|
| Weekly | Settings → Advisor → Run scan. Work anything new. |
| Weekly | `pm2 status` and the nginx error log — both in Settings → Server. |
| Monthly | Restore a backup somewhere that is not production. |
| Quarterly | Rotate `JWT_SECRET` (logs everyone out) and any provider keys. |
| On deploy | `git pull && npm ci && npm run build && pm2 reload all` |

Certificates renew themselves via certbot's systemd timer. `certbot renew
--dry-run` after any nginx change is worth the ten seconds.
