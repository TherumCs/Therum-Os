# Nexus provider audit

Generated from the code on 2026-08-01 — not written by hand, so it cannot drift from what ships.

**Every tester in this table was written by probing the provider's live API with a deliberately bad credential, and  re-runs them all against those real APIs on every suite run.** A tester pointed at a dead URL is a green tick that means nothing.

| Provider | Category | Connect via | Fields | Test | Adapter |
|---|---|---|---|---|---|
| Anthropic | ai | api key | API Key | yes | — |
| OpenAI | ai | api key | API Key | yes | — |
| Gemini | ai | api key | API Key | yes | — |
| Grok | ai | api key | API Key | yes | — |
| Mistral | ai | api key | API Key | yes | — |
| DeepSeek | ai | api key | API Key | live-verified | — |
| Perplexity | ai | api key | API Key | live-verified | — |
| Ollama | ai | api key | Server Base URL | live-verified | — |
| Cohere | ai | api key | API Key | yes | — |
| Stability AI | ai | api key | API Key | yes | — |
| ElevenLabs | ai | api key | API Key (xi-api-key) | live-verified | — |
| Replicate | ai | api key | API Token | yes | — |
| Hugging Face | ai | api key | User Access Token | yes | — |
| Mailchimp | messaging | api key + oauth | API Key (keep the -us21 suffix) | live-verified | — |
| SendGrid | messaging | api key | API Key | yes | — |
| Twilio | messaging | api key | Account SID + Auth Token | yes | — |
| OneSignal | messaging | api key | App ID + REST API Key | live-verified | — |
| Telegram | messaging | api key | Bot Token | yes | — |
| Mapbox | messaging | api key | Access Token | yes | — |
| Postmark | messaging | api key | Server API Token | yes | — |
| Flodesk | messaging | api key | API Key | live-verified | — |
| Resend | messaging | api key | API Key | yes | — |
| Pusher | messaging | api key | App ID + Key + Secret + Cluster (e.g. us2) | **none — explained in UI** | — |
| Vonage | messaging | api key | API Key + API Secret | live-verified | — |
| WhatsApp | messaging | api key | Phone Number ID + Permanent Access Token + WhatsApp Business Account ID *(opt)* | live-verified | — |
| Discord | messaging | api key | Bot Token | yes | — |
| Gmail | messaging | oauth | (oauth — nothing to paste) | yes | — |
| Shopify | ecommerce | api key | Store domain (x.myshopify.com) + Admin API access token | live-verified | — |
| BigCommerce | ecommerce | api key | Store hash + Access token | live-verified | — |
| Etsy | ecommerce | api key + oauth | Keystring (Client ID) + Shared Secret | live-verified | — |
| Amazon | ecommerce | api key | LWA Client ID + LWA Client Secret + Refresh Token | live-verified | — |
| Magento | ecommerce | api key | Store Base URL + Integration Access Token | live-verified | — |
| Wix | ecommerce | api key | API Key + Site ID + Account ID *(opt)* | live-verified | — |
| Squarespace | ecommerce | api key | Commerce API Key | live-verified | — |
| Lemon Squeezy | ecommerce | api key | API Key + Store ID *(opt)* | live-verified | — |
| Printful | fulfillment | store-pull-woo + oauth | API token + Store ID *(opt)* | live-verified | catalog sync |
| Printify | fulfillment | store-pull-woo | Personal Access Token + Shop ID *(opt)* | live-verified | catalog sync |
| Gelato | fulfillment | store-pull-woo | API Key + Store ID (ecommerce endpoints only) *(opt)* | live-verified | — |
| Gooten | fulfillment | store-pull-woo | Recipe ID + Partner Billing Key | **none — explained in UI** | — |
| SPOD | fulfillment | store-pull-woo | API Key (Spreadconnect dashboard) | live-verified | — |
| Podplus | fulfillment | store-pull-woo | API Key | **none — explained in UI** | — |
| PodPartner | fulfillment | store-pull-woo | API Key | **none — explained in UI** | — |
| Tapstitch | fulfillment | store-pull-woo | Consumer Key + Consumer Secret | **none — explained in UI** | — |
| Contrado | fulfillment | store-pull-woo | API Key | **none — explained in UI** | — |
| Stripe | payments | api key + oauth | Secret Key | yes | — |
| PayPal | payments | api key | Client ID + Client Secret | yes | — |
| Square | payments | api key + oauth | Access Token + Location ID + Environment ("sandbox" or blank) *(opt)* | yes | — |
| Braintree | payments | api key | Public Key + Private Key | yes | — |
| Adyen | payments | api key | API Key + Merchant Account | live-verified | — |
| Klarna | payments | api key | Username (UID) + Password (API key) | live-verified | — |
| Coinbase Commerce | payments | api key | API Key + Webhook Shared Secret *(opt)* | yes | — |
| Authorize.net | payments | api key | API Login ID + Transaction Key | live-verified | — |
| Mollie | payments | api key | API Key | live-verified | — |
| Razorpay | payments | api key | Key ID + Key Secret | live-verified | — |
| Wise | payments | api key | API Token + Profile ID *(opt)* | yes | — |
| PayU | payments | api key | Client ID (POS ID) + Client Secret | live-verified | — |
| Whop | payments | api key | API Key + Company ID *(opt)* | yes | — |
| Slack | apps | oauth | (oauth — nothing to paste) | yes | — |
| Notion | apps | api key + oauth | Internal Integration Secret | yes | — |
| Airtable | apps | api key + oauth | Personal Access Token + Base ID (appXXXXXXXXXXXXXX) *(opt)* | live-verified | — |
| Google Drive | apps | oauth | (oauth — nothing to paste) | yes | — |
| Google Calendar | apps | oauth | (oauth — nothing to paste) | yes | — |
| Google Sheets | apps | oauth | (oauth — nothing to paste) | yes | — |
| Dropbox | apps | api key + oauth | Access Token | yes | — |
| Figma | apps | api key + oauth | Personal Access Token | yes | — |
| GitHub | apps | oauth | (oauth — nothing to paste) | yes | — |
| Linear | apps | api key + oauth | Personal API Key | yes | — |
| Zapier | apps | api key | Webhook URL | **none — explained in UI** | — |
| Trello | apps | api key | API Key + Token | yes | — |
| Asana | apps | api key + oauth | Personal Access Token | yes | — |
| Jira | apps | api key | Site URL (https://you.atlassian.net) + Email + API Token | live-verified | — |
| Zoom | apps | api key + oauth | Account ID + Client ID + Client Secret | live-verified | — |
| Calendly | apps | api key + oauth | Personal Access Token | yes | — |
| HubSpot | apps | api key + oauth | Private App Access Token | yes | — |
| Salesforce | apps | api key | Instance URL (https://you.my.salesforce.com) + Client ID (Consumer Key) + Client Secret (Consumer Secret) | live-verified | — |
| Intercom | apps | api key + oauth | Access Token | yes | — |
| Zendesk | apps | api key | Subdomain + Email + API Token | live-verified | — |
| Sign in with Google | identity | api key | Client ID + Client Secret *(opt)* | **none — explained in UI** | — |
| Sign in with Apple | identity | api key | Services ID (the client_id) + Team ID *(opt)* + Key ID *(opt)* | **none — explained in UI** | — |
| Facebook Login | identity | api key | App ID + App Secret | live-verified | — |
| Hostinger | hosting | api key | API Token | live-verified | — |

## Totals

- 81 providers
- **72 have a working connection tester** (34 of them probed against the live API on 2026-08-01)
- 0 connect by OAuth, where the consent flow itself is the test
- 9 have no automated test AND say so in their own card, with the reason
- 0 silently pretend to be testable
