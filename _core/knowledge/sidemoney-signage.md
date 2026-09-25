---
name: sidemoney-signage
description: "The two 8.5x11 print signs (Bird Season + The Sidemoney Company) + the product-PDP QR set — artifact URL, assets, and the QR lessons"
metadata: 
  node_type: memory
  type: project
  originSessionId: e745e2aa-9578-48ef-9843-d125d121f24c
  modified: 2026-09-14T20:44:42.544Z
---

Two print signs Bam made (Sept 2026), one artifact, both 8.5×11 @ 300 DPI, rendered to JPEG via headless Chrome (`--force-device-scale-factor=3.125 --window-size=816,1056`).

**Artifact:** https://claude.ai/code/artifact/5be746f7-5440-4541-ae9b-1149b34fab76 (title "Sidemoney Signage"). Source `scratchpad/signs.html`; two `<section class="sheet bs">` / `.ts`. Both: top line "The Sidemoney Company" pinned, middle group vertically centred (`.mid{flex:1;justify-content:center}`), bottom row pinned, all text WHITE.
- **Bird Season sheet:** eagle logo `eagle.webp` (Bam's brand asset), headline in **Vegan Style** font (`/Users/bam/FontBase/Vegan Style Personal Use.ttf` → published as `vegan.ttf`, @font-face). BG = stadium photo `stadium.jpg`. Real copy from the "bird-season-is-back" post (homage to Philly football + À Pas Dorés "with golden steps"). Bottom ledger: left "The capsule" (Practice jerseys · Snapback · Joggers · Sweat shorts · Hoodie · Tee), right "Series À Pas Dorés". 2 QRs (collection /c/bird-season + /shop).
- **Sidemoney sheet:** logo `sig-white.png` (full-sig-white). BG = currency-engraving texture Bam gave (Dropbox) → `tsc-bg.png`, with a dark overlay kept. Tagline "Money is universal · the only language". Bottom = ticker strip ($SMNY/$SME/$PLAY/$SAFE/$SMU/$MOVE/$000). 2 QRs (about + /shop).

**Product QR set (for his Figma "reserve note" product cards):** `scratchpad/product-qr/` + `Sidemoney-Product-QRs.zip`, 7 products, PNG(1640px)+SVG each, generated with `segno`.
- **LESSON (I shipped these wrong first):** transparent-background QRs FAILED to scan on his colored cards ("no product found"; one decoded empty). FIX = **black modules on SOLID WHITE**, error='q', border=4. Always **decode-verify** before sending (`opencv-python-headless` `cv2.QRCodeDetector`).
- Verified PDP targets (all 200, canonical links the collection uses; jersey/snapback = cluster primary): practice-jersey→`/product/bird-season-practice-jersey-midnight-green`, joggers→`/product/bird-season-joggers-4`, sweat-shorts→`/product/bird-season-sweat-shorts`, snapback→`/product/bird-season-snapback-455511187`, easy-money-tee→`/product/easy-money-tee`, hunting-season-hoodie→`/product/hunting-season-hoodie`, sev7n-fold-snapback→`/product/sev7n-fold-snapback-455083583`.
- Figma MCP is NOT authed in these sessions → can't edit his Figma; hand him the files. [[sidemoney-blog-system]]
