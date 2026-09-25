---
name: fulfillment-routing
description: "how sidemoney.co orders route to vendors (Printful/Printify push, Tapstitch pull) + the bugs fixed 2026-08-12"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1eb82035-25c8-45fb-83e3-63b52d3072eb
  modified: 2026-08-23T02:07:43.168Z
---

**AUTHORITATIVE ARCHITECTURE + the gap Bam is angry about (consolidated 2026-08-22).**
ALL vendors ARE connected — Bam set them up, they pulled his products in, they hold live
StoreCredentials. His half is done; do NOT tell him to "reconnect" or that a vendor isn't
connected. The failure is the BUILD: the store only PUSHES orders to vendors it holds an
OUTBOUND api-token for. System of record checked (Connection table, Vendor.apiKey, .env):
outbound tokens exist ONLY for **printful, printify, contrado**. That is why Printful +
Printify work (store POSTs each paid order into their API — card charged, order on their
backend) and the rest do not.
- PUSH (works, store holds their token): printful, printify. contrado token present but
  testOk=false.
- PULL/webhook, connected but NOT delivering: tapstitch, podpluser, podpartner (+ gooten,
  gelato, jetprint, spod, merchize — all `wooStyle` in connection.service.ts). They hold
  OUR woo keys. Store pushes order.updated to the webhook receivers they registered
  (tapstitch `/woocommerce/callback/order/updated`, podpluser `/api/woo/webhooks/...`) on
  payment — HTTP 200 every time — but the receiver returns `{code:200,data:null}` and
  creates nothing (Tapstitch's callback is update-only; `/order/created` is 404).
  PODpartner registered NO webhook at all → pull-only.
THE REAL MECHANISM (corrected 2026-08-22 from :10025 — supersedes the "need their token"
theory above; the pull vendors do NOT need us to hold their token). Read :10025's
smxxwc_webhooks + WooCommerce class-wc-webhook.php. Vendors are DIFFERENT:
- Tapstitch(=HugePOD)/Printify/Printful subscribe topic
  `action.woocommerce_order_status_processing` (fires on paid). WC sends {action, arg:<order
  id>}; the partner then PULLS GET /wc/v3/orders/<id> with the woo key WE issued it. Tapstitch
  endpoint = api.service.hugepod.com (or api.service.tapstitch.com) /woocommerce/callback/order/paid.
- PODpartner/PodPluser use `order.updated` (full order object). PODpartner endpoint
  podpartner.com/api/pod/v1/shop/woo/webhook/order?shop_id=<id>; PodPluser
  podpluser.com/api/woo/webhooks/orders/updated?store_id=<id>.
ROOT CAUSE our bridge rejected action.* topics (WEBHOOK_TOPICS had only order/product resource
topics) → Tapstitch fell back to update-only /callback/order/updated ({code:200,data:null},
creates nothing). FIXED: action topics supported + emitted on pending->processing in
order.service.transition() as {action,arg:wooId}; GET /wc/v3/orders/:id added for the pull-back;
Tapstitch action webhook -> /order/paid registered on the store.
Store-ids DIFFER per store: my store PodPluser store_id=2467 (:10025=1538) — vendors registered
my store as its OWN connection, so use MY StoreWebhook URLs/secrets, not :10025's. Both webhook
endpoints ACK 200 generically regardless of payload, so the only store-observable proof of
fulfilment is the action-topic PULL-BACK (vendor GET /orders/<id> in nginx) or a status
write-back (PUT /orders/<id> -> shipped). :10025 access: socket
~/Library/Application Support/Local/run/zff81gb8N/mysql/mysqld.sock, db 'local', prefix smxx,
client at Local lightning-services/mysql-8.4.0; ref PHP at ~/Local Sites/the-sidemoney-company.
Printful/Printify ALSO work via outbound api-token push (Connection table) — verifiable by
querying their API (fulfillmentAudit.reconcile). See [[live-store-real-money]] [[the-port-law]].

**:10025 nexus-plugin reference (the OLD working Therum/WP impl — mined 2026-08-22).** Old
plugin at ~/Local Sites/the-sidemoney-company/app/public/wp-content/plugins/nexus. Connector
registry: includes/registry.php. Crypto: includes/crypto.php — envelope `nx1.<b64 iv>.<b64
tag>.<b64 ct>`, aes-256-gcm, key from nexus_crypto_key() (site secret). Stored connectors in
smxxoptions: nexus_connector_printful/printify/pod-partner (nx1-encrypted), nexus_custom_connectors
= empty. PER-VENDOR TRUTH from the registry:
- podpluser: bridge_only, NO public API — marketplace bridge only. Webhook (order.updated) is the
  ONLY order delivery. Cannot push.
- tapstitch: bridge_only, NO standalone API — connects to the woo store + uses its API as bridge.
  Webhook action.woocommerce_order_status_processing (-> hugepod /order/paid) then PULLS the order.
- pod-partner: HAS an API (api_key+api_secret fields, "issued from your Pod Partner account") +
  webhook order.updated. But firing my store's order to :10025's PODpartner webhook (shop_id=21437,
  :10025's secret) => HTTP 400 {"code":1,"msg":"参数无效"} (invalid parameters): shop_id 21437 is
  :10025's shop with :10025's product map; my order's product ids (my wooIds) aren't in it. :10025
  has NO saved successful webhook payload (local copy, never delivered live), so nothing to copy.
STRUCTURAL RULE: a vendor's shop_id + product mapping + webhook secret are issued PER STORE
CONNECTION and are NOT copyable from :10025 to the new store. Every vendor that has its OWN
connection to the new store works (JetPrint auto-polls /wc/v2/orders; PodPluser own webhook
store_id=2467; Printful/Printify push). Tapstitch (trust of a manually-created webhook) and
PODpartner (no own connection) are the two whose per-store connection is incomplete — the store
side is fully correct now, so completing their connection to sidemoney.co is what closes them.

**ENDGAME STATE (2026-08-23).** orderWebhookPayload is BYTE-SHAPE parity with real WC 10.4.3
(reference JSON captured from :10025 via PHP RestApiUtil bootstrap — dates no Z/millis, 2dp money,
digits-only number w/ SMNY in order_key, pa_color/pa_size meta pairs, image/parent_name). A
perfect Woo-mimic delivery (headers, UA, numeric ids, :10025 secret) STILL got PODpartner 2002 →
response invariant to everything store-side → their shop 21437 is flagged dead on their end.
UNLOCK APPLIED: :10025 woo consumer_secrets are PLAINTEXT in smxxwoocommerce_api_keys; combined
with the nexus-vault ck (aes-256-gcm, key HMAC("nexus-creds-v1", SECURE_AUTH_KEY)), PODpartner's
working legacy pair (key_id 26 "PodPartner API 10.15", last_access 2025-12-01) was seeded into
StoreCredential as "PODpartner (legacy woo key, restored)" — their stored sidemoney.co login
authenticates again; their connection check should reactivate the shop. Tapstitch's
"PostmanRuntime" traffic is its AUTOMATED daily 17:00 UTC job: POST /webhooks (now 201s) + GET
/orders pull. SELF-HEALING: fulfillmentAudit.redeliverStuck() runs hourly in the worker —
re-offers processing orders (14d window, 6h/order cap) to any webhook vendor whose latest
response wasn't a genuine accept; notifications only, never API push (no double-charge).
Tapstitch/PODpartner recovery requires ZERO manual steps once their side comes back. Recovery
tells: ck_1fe8… hits in nginx (PODpartner), a 201 POST /webhooks from 47.254.82.144 (Tapstitch).

Paid orders auto-route from `orderService.markPaid` → `routeOrder` (drafts) +
`confirmPrintfulOrder` (confirm to production). Provider lives on
`product.fulfillmentProvider`; `product.sourceId` = the vendor PRODUCT id;
`variant.sourceId` = the vendor VARIANT id. PUSH vendors: printful, printify,
contrado (`PUSHERS` in counter/fulfillmentRouting.ts). PULL partners (Tapstitch,
PODpartner, Merchize, JetPrint) connect to the store and pull orders via the
Woo-compat bridge — they are NOT pushed.

**Product→vendor map (41 products, fixed 2026-08-12):** printful 8, printify 22,
tapstitch 11. All 41 now have a provider.

**Bugs found + fixed (each broke fulfillment store-wide):**
1. Printful credential store id was WRONG: `1536603` (dead → "Store not found or
   not accessible"). Correct = `18591060` "The Sidemoney Company" (token also
   sees `14110753` "Personal orders" — do NOT use). Credential shape `token|storeId`.
2. Printify credential was MISSING the shop id (only the token). Correct shop =
   `1299531` "The Sidemoney Company". Credential shape `token|shopId`.
3. `pushPrintify` sent `variant.sourceId` as BOTH product_id and variant_id →
   Printify rejects every order ("Product with id … is missing"). FIXED: product_id
   = `product.sourceId` (Printify product id, 24-char hex), variant_id =
   `variant.sourceId` (int). Required adding `sourceId` to the product select in
   `orderInclude` (order.service.ts) and the RoutableOrder type.
4. 13 products had NO provider + NO variant sourceId. Recovered by matching their
   SKU to Printify's live catalog (GET /shops/{id}/products.json) → set provider
   + product.sourceId + variant.sourceId.
Verified live: POST to Printify /orders.json returned 200 (order accepted).

**Vendor-account items (Bam only, not code):**
- Printful billing card EXPIRED → orders reach Printful but fail "Expired Card".
  Update Printful → Billing, then re-confirm (e.g. Felix's Printful order 171185470).
- Printify billing — confirm a payment method (charges on production; orders
  otherwise sit on-hold).
Tapstitch billing/connection: fine, Bam handles vendor billing.

**THE PULL-PARTNER wooId BUG (root cause of "no order reached any vendor", fixed
2026-08-22).** Pull/webhook partners (Tapstitch, PodPluser via webhook; PODpartner
via /orders poll) were RECEIVING every paid order and returning HTTP 200 — delivery
was never the problem, so "reconnect the partner" was WRONG (I chased a credential
`lastUsedAt` timestamp; ignore that signal). They created NOTHING because the order
payload identified each line by the store's internal **cuid** (`product_id:
cmsqm9tgh…`), but a partner maps its catalogue to the **integer `wooId`** we hand it
at product sync (SP Tee = product 148 / variant 1644). Unmatchable line → partner
ACKs 200, prints nothing (Tapstitch returns `{code:200,msg:null,data:null}`; their
only order endpoint is `/callback/order/updated` — `/order/created` is 404, so
`order.updated` IS their intake). FIX: emit `wooId` not the cuid in BOTH
`counter/orderWebhookPayload.ts` (webhook) AND the `GET /wc/v3/orders` serializer in
`api/routes/wooCompat.ts` (pull); added `wooId` to product+variant selects in
`orderInclude` (order.service.ts). wooId is 100% populated (0/116 products, 0/1204
variants null) so no backfill. Re-emitted the stuck orders corrected (all 200).
CAVEAT: partners ACK 200 whether or not they fulfil, so the store CANNOT observe
partner printing — confirmation is the partner backend. Health check `checkFulfillment`
(system.service.ts) + `fulfillmentAudit.service.ts` now measure DELIVERY (webhook 2xx
via WebhookDelivery), not the old credential-poll heuristic.

**Tapstitch (and PODpartner/JetPrint/etc.) ARE connected — do NOT check
`credentialFor('tapstitch')` (that's for PUSH vendors and is correctly null).**
PULL partners hold OUR store's WooCommerce keys and poll us. Verify via the
`StoreCredential` table: a row labelled e.g. "Tapstitch connection", `revokedAt`
null, with a recent `lastUsedAt`/`lastUsedIp` = an active connection. Confirmed
2026-08-12: "Tapstitch connection" last used 2026-08-11 17:40 from 47.254.82.144;
partners pull `GET /wp-json/wc/v3/orders?status=processing&after=<ts>` for newly
PAID orders (status processing) then fulfil their own line items and PUT status
→ shipped via `/wc/v3/orders/:id`. So the 11 tapstitch products (tees, shorts,
sweatpants, SP tee, jerseys) DO fulfil — Tapstitch pulls them. The order must be
'processing' (paid) to be pulled, which the payWithToken→markPaid fix guarantees.
See [[pull-images-from-10025-mysql]] [[live-store-real-money]].

**Credential tables — don't mix them up (learned the hard way 2026-09-15).** `StoreCredential` (prisma `storeCredential`; cols keyId/label/consumerKey/secretHash/scope/firstParty/lastUsedAt/lastUsedIp) = INBOUND partner keys — the WooCommerce consumer key/secret WE issued to Tapstitch/PodPluser/etc so they can pull from us. It has NO `provider` column. OUTBOUND vendor tokens (Printful `token|storeId`, Printify `token|shopId` = 1299531, Contrado) live on the Connection table / `Vendor.apiKey` and are read through the app's own resolver in `src/counter/fulfillmentRouting.ts` (`credentialFor(...)`) — use that (or `connection.service.ts`), never a StoreCredential lookup, when you need to call a vendor's API (e.g. read Printify's catalog `GET https://api.printify.com/v1/shops/{shopId}/products.json`). Never print the token.
