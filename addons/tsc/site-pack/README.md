# Sidemoney site pack

Everything Sidemoney-specific that Therum OS needs at runtime but must NOT live in
the product repo (`TherumCs/Therum-OS-2.0` is Therum OS only — Bam's rule).

| Path | What | Where it goes on the box |
|---|---|---|
| `categoryPages.json` | Category landing editorial (Sixers Season, Bird Season, À Pas Dorés, City Series, Men's, Women's…): hero, tagline, sections, callouts, lookbook | `/home/therum/site-pack/categoryPages.json` — read at boot via `SITE_PACK_DIR` |
| `site.env` | The instance's env additions (site name, email logo, careers inbox, pack dir) | merged into `/home/therum/therum/.env` |
| `deploy/sidemoney.nginx.conf` | public vhost | `/etc/nginx/sites-enabled/sidemoney` |
| `deploy/sm-engine-internal.nginx.conf` | headless WooPayments engine vhost (127.0.0.1:8088) | `/etc/nginx/sites-enabled/sm-engine-internal` |
| `deploy/pay-mu-plugins/sm-appliance.php` | the WordPress→Counter payment bridge | `/var/www/pay/wp-content/mu-plugins/sm-appliance.php` |

Brand values that live in the DATABASE (Counter › Settings), not here: site name
"The Sidemoney Company", tagline, chrome header/footer slugs, ported stylesheet URL,
SEO defaults incl. the Meta domain-verification token, notification/SMTP From.

Deploy a change: edit here → `scp categoryPages.json therum@2.25.93.243:/home/therum/site-pack/`
→ `pm2 reload therum-cms-api` (the JSON is read once at boot). nginx/php changes:
copy, `sudo nginx -t && sudo systemctl reload nginx`.
