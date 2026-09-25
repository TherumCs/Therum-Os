---
name: deploy-env-reload-trap
description: "pm2 reload <name> keeps the OLD captured env — env changes need a reload FROM ecosystem.config.cjs or they silently don't take effect"
metadata: 
  node_type: memory
  type: reference
  originSessionId: f4504c37-caac-4f64-affa-6039105bec50
  modified: 2026-08-21T13:01:55.147Z
---

**The trap that killed live card checkout (2026-08-20).** On the box (therum@2.25.93.243),
`ecosystem.config.cjs` reads `.env` at start time and hands pm2 a plain `env: apiEnv` object
(pm2's cluster bootstrap strips `--env-file`, so the app is NOT started with node's
`--env-file`; env.ts just does `EnvSchema.safeParse(process.env)`). pm2 CAPTURES that env when
the process is first started with `pm2 start ecosystem.config.cjs`.

**`pm2 reload therum-cms-api` (or restart <name>) reloads the CODE but keeps the ALREADY-CAPTURED
env.** So any var ADDED to `.env` after the last full ecosystem start never reaches the running
process. This is exactly why WooPayments card checkout was dead: `WOOPAY_BRIDGE_URL/AUTH` were in
`.env` and valid (a manual `fetch` with them returned 200), but the running process didn't have
them → `woopayBridge.cfg()` returned null → `engineGet` → status 0 → `/api/shop/wallets` reported
woopay `ready:false` "The WooPayments engine is unreachable" → card field never mounts → checkout
shows "payment is warming up, tap Place order again" → NOBODY CAN PAY BY CARD.

**RULE: after ANY change to `~/therum/.env`, reload from the ecosystem file, not by name:**
```
cd ~/therum && pm2 reload ecosystem.config.cjs --only therum-cms-api,therum-cms-worker --update-env
```
(re-runs envFile('.env'), graceful cluster reload). Code-only deploys can keep using
`pm2 reload therum-cms-api`, but env-touching deploys MUST use the ecosystem form. When debugging
a "feature configured but not working" symptom, SUSPECT the running process env is stale — the
`.env` file and a manual curl/node test will both look fine while the process is blind.

Note: `/proc/<pid>/environ` does NOT reveal `--env-file` vars (loaded post-exec), so it's a
misleading way to check; but pm2's `env: apiEnv` vars DO appear there. Best check is behaviour
(hit the endpoint) or a debug print of `process.env` from inside the app.

Related: [[live-store-real-money]], [[woopayments-engine]], [[local-sites-and-dbs]].
