# Nexus provider audit

Generated from the code on 2026-08-01 — not written by hand, so it cannot drift from what ships.

Legend: **tester** = Test connection actually calls the provider. **adapter** = something in this system uses the credential for real work. **shape** = the credential fields were confirmed against the provider's own docs.

| Provider | Category | Connect via | Fields | Tester | Adapter | Shape |
|---|---|---|---|---|---|---|
| Anthropic | ai | api key | API Key | yes | — | assumed |
| OpenAI | ai | api key | API Key | yes | — | assumed |
| Gemini | ai | api key | API Key | yes | — | assumed |
| Grok | ai | api key | API Key | yes | — | assumed |
| Mistral | ai | api key | API Key | yes | — | assumed |
| DeepSeek | ai | api key | API Key | — | — | assumed |
| Perplexity | ai | api key | API Key | — | — | assumed |
| Ollama | ai | api key | Server Base URL | — | — | assumed |
| Cohere | ai | api key | API Key | yes | — | assumed |
| Stability AI | ai | api key | API Key | yes | — | assumed |
| ElevenLabs | ai | api key | API Key (xi-api-key) | — | — | assumed |
| Replicate | ai | api key | API Token | yes | — | assumed |
| Hugging Face | ai | api key | User Access Token | yes | — | assumed |
| Mailchimp | messaging | api key + oauth | API Key (keep the -us21 suffix) | — | — | assumed |
| SendGrid | messaging | api key | API Key | yes | — | assumed |
| Twilio | messaging | api key | Account SID + Auth Token | yes | — | assumed |
| OneSignal | messaging | api key | App ID + REST API Key | — | — | assumed |
| Telegram | messaging | api key | Bot Token | yes | — | assumed |
| Mapbox | messaging | api key | Access Token | yes | — | assumed |
| Postmark | messaging | api key | Server API Token | yes | — | assumed |
| Flodesk | messaging | api key | API Key | yes | — | confirmed |
| Resend | messaging | api key | API Key | yes | — | assumed |
| Pusher | messaging | api key | App ID + Key + Secret + Cluster (e.g. us2) | — | — | assumed |
| Vonage | messaging | api key | API Key + API Secret | — | — | assumed |
| WhatsApp | messaging | api key | Phone Number ID + Permanent Access Token + WhatsApp Business Account ID *(opt)* | — | — | assumed |
| Discord | messaging | api key | Bot Token | yes | — | assumed |
| Gmail | messaging | oauth | (single box) | yes | — | assumed |
| Shopify | ecommerce | api key | Store domain (x.myshopify.com) + Admin API access token | — | — | assumed |
| BigCommerce | ecommerce | api key | Store hash + Access token | — | — | assumed |
| Etsy | ecommerce | api key + oauth | Keystring (Client ID) + Shared Secret | — | — | assumed |
| Amazon | ecommerce | api key | LWA Client ID + LWA Client Secret + Refresh Token | — | — | assumed |
| Magento | ecommerce | api key | Store Base URL + Integration Access Token | — | — | assumed |
| Wix | ecommerce | api key | API Key + Site ID + Account ID *(opt)* | — | — | assumed |
| Squarespace | ecommerce | api key | Commerce API Key | — | — | assumed |
| Lemon Squeezy | ecommerce | api key | API Key + Store ID *(opt)* | — | — | assumed |
| Printful | fulfillment | store-pull-woo + oauth | API token + Store ID *(opt)* | yes | yes | confirmed |
| Printify | fulfillment | store-pull-woo | Personal Access Token + Shop ID *(opt)* | yes | yes | confirmed |
| Gelato | fulfillment | store-pull-woo | API Key + Store ID (ecommerce endpoints only) *(opt)* | yes | — | confirmed |
| Gooten | fulfillment | store-pull-woo | Recipe ID + Partner Billing Key | — | — | assumed |
| SPOD | fulfillment | store-pull-woo | API Key (Spreadconnect dashboard) | yes | — | confirmed |
| Podplus | fulfillment | store-pull-woo | API Key | — | — | **UNVERIFIED (says so)** |
| PodPartner | fulfillment | store-pull-woo | API Key | — | — | **UNVERIFIED (says so)** |
| Tapstitch | fulfillment | store-pull-woo | Consumer Key + Consumer Secret | — | — | assumed |
| Contrado | fulfillment | store-pull-woo | API Key | — | — | **UNVERIFIED (says so)** |
| Stripe | payments | api key + oauth | Secret Key | yes | — | assumed |
| PayPal | payments | api key | Client ID + Client Secret | yes | — | assumed |
| Square | payments | api key + oauth | Access Token + Location ID + Environment ("sandbox" or blank) *(opt)* | yes | — | assumed |
| Braintree | payments | api key | Public Key + Private Key | yes | — | assumed |
| Adyen | payments | api key | API Key + Merchant Account | — | — | assumed |
| Klarna | payments | api key | Username (UID) + Password (API key) | — | — | assumed |
| Coinbase Commerce | payments | api key | API Key + Webhook Shared Secret *(opt)* | — | — | assumed |
| Authorize.net | payments | api key | API Login ID + Transaction Key | — | — | assumed |
| Mollie | payments | api key | API Key | — | — | assumed |
| Razorpay | payments | api key | Key ID + Key Secret | — | — | assumed |
| Wise | payments | api key | API Token + Profile ID *(opt)* | yes | — | assumed |
| PayU | payments | api key | Client ID (POS ID) + Client Secret | — | — | assumed |
| Whop | payments | api key | API Key + Company ID *(opt)* | yes | — | assumed |
| Slack | apps | oauth + oauth | (single box) | yes | — | assumed |
| Notion | apps | api key + oauth | Internal Integration Secret | yes | — | assumed |
| Airtable | apps | api key + oauth | Personal Access Token + Base ID (appXXXXXXXXXXXXXX) *(opt)* | — | — | assumed |
| Google Drive | apps | oauth | (single box) | — | — | assumed |
| Google Calendar | apps | oauth | (single box) | — | — | assumed |
| Google Sheets | apps | oauth | (single box) | — | — | assumed |
| Dropbox | apps | api key + oauth | Access Token | yes | — | assumed |
| Figma | apps | api key + oauth | Personal Access Token | yes | — | assumed |
| GitHub | apps | oauth + oauth | (single box) | yes | — | assumed |
| Linear | apps | api key + oauth | Personal API Key | yes | — | assumed |
| Zapier | apps | api key | Webhook URL | — | — | assumed |
| Trello | apps | api key | API Key + Token | yes | — | assumed |
| Asana | apps | api key + oauth | Personal Access Token | yes | — | assumed |
| Jira | apps | api key | Site URL (https://you.atlassian.net) + Email + API Token | — | — | assumed |
| Zoom | apps | api key + oauth | Account ID + Client ID + Client Secret | — | — | assumed |
| Calendly | apps | api key + oauth | Personal Access Token | yes | — | assumed |
| HubSpot | apps | api key + oauth | Private App Access Token | yes | — | assumed |
| Salesforce | apps | api key | Instance URL (https://you.my.salesforce.com) + Client ID (Consumer Key) + Client Secret (Consumer Secret) | — | — | assumed |
| Intercom | apps | api key + oauth | Access Token | yes | — | assumed |
| Zendesk | apps | api key | Subdomain + Email + API Token | — | — | assumed |
| Sign in with Google | identity | api key | Client ID + Client Secret *(opt)* | — | — | assumed |
| Sign in with Apple | identity | api key | Services ID (the client_id) + Team ID *(opt)* + Key ID *(opt)* | — | — | assumed |
| Facebook Login | identity | api key | App ID + App Secret | — | — | assumed |
| Hostinger | hosting | api key | API Token | — | — | confirmed |

## Totals

- 81 providers
- 39 have a real connection tester; 42 do not
- 2 have a catalog-sync adapter
- 6 had their credential shape confirmed against live docs or a live probe
- 3 say plainly in the UI that their shape is unconfirmed
- 72 are ASSUMED — inherited from the original inventory and never checked
