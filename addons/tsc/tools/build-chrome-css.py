#!/usr/bin/env python3
"""Build the site stylesheet for Therum OS 2.0 and upload it as a media asset.

The replatform runs 2.0 with NO WordPress, so this reads the theme CSS chain
straight off disk (no HTTP, no WP running), localizes every asset the CSS
references into 2.0's media library, rewrites the urls, uploads the bundle,
and points settings.site.chromeCssUrl at it.

Rerunnable: every run produces a fresh asset + repoints the setting.

Usage: python3 build-chrome-css.py [api_base]
"""
from __future__ import annotations  # system python is 3.9; keeps `Path | None`

import json
import mimetypes
import re
import subprocess
import sys
import urllib.request
import uuid
from pathlib import Path

API = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:10009"
CMS = Path("/Users/bam/Local Sites/therum-os/therum-cms-2")
THEME = Path("/Users/bam/Local Sites/tsc-beta/app/public/wp-content/themes/bricks-child")
WP_ROOT = Path("/Users/bam/Local Sites/tsc-beta/app/public")

# cascade order matters — later files override earlier ones
ORDER = [
    "moderno-full.css",          # whole upstream theme chain
    "moderno-elementor-port.css",
    "moderno-live-diff.css",
    "moderno-components.css",
    "moderno-inline.css",
    "moderno-header.css",
    "moderno-instance.css",
    "style.css",                 # our own overrides last
]

ASSET_RE = re.compile(
    r"(?:https?://[^\"'\s)]+)?/wp-content/[^\"'\s)]+?"
    r"\.(?:png|jpe?g|webp|gif|svg|avif|woff2?|ttf|eot)",
    re.I,
)


def mint_token() -> str:
    r = subprocess.run(["npm", "run", "--silent", "mint-jwt"], cwd=CMS,
                       capture_output=True, text=True)
    tok = (r.stdout or "").strip().splitlines()[-1].strip() if r.stdout.strip() else ""
    if tok.count(".") == 2:
        return tok
    return Path("/tmp/therum-jwt.txt").read_text().strip()


def upload(token: str, filename: str, data: bytes, mime: str) -> dict:
    boundary = uuid.uuid4().hex
    body = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="file"; '
        f'filename="{filename}"\r\nContent-Type: {mime}\r\n\r\n'
    ).encode() + data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        f"{API}/api/media/upload", data=body,
        headers={"authorization": f"Bearer {token}",
                 "content-type": f"multipart/form-data; boundary={boundary}"})
    return json.load(urllib.request.urlopen(req, timeout=180))


def disk_path(url: str) -> Path | None:
    """Map a /wp-content/... url to the file on disk."""
    m = re.search(r"/wp-content/.*", url)
    if not m:
        return None
    p = WP_ROOT / m.group(0).lstrip("/").split("?")[0]
    return p if p.is_file() else None


def main() -> None:
    token = mint_token()

    parts = []
    for name in ORDER:
        f = THEME / name
        if not f.exists():
            print(f"  skip (missing): {name}")
            continue
        parts.append(f"/* ===== {name} ===== */\n" + f.read_text(errors="replace"))
        print(f"  + {name} ({f.stat().st_size:,} bytes)")
    css = "\n".join(parts)

    urls = sorted(set(ASSET_RE.findall(css)))
    print(f"\nlocalizing {len(urls)} css-referenced assets from disk…")
    localized = missing = 0
    for url in urls:
        src = disk_path(url)
        if not src:
            print(f"  MISSING: {url[-60:]}")
            missing += 1
            continue
        mime = mimetypes.guess_type(src.name)[0] or "application/octet-stream"
        try:
            asset = upload(token, src.name, src.read_bytes(), mime)
        except Exception as e:  # one bad asset must not sink the bundle
            print(f"  FAILED: {src.name}: {e}")
            missing += 1
            continue
        css = css.replace(url, asset["url"])
        localized += 1

    # any remaining absolute refs to the old WP origins become root-relative
    css = re.sub(r"https?://localhost:\d+/", "/", css)
    css = css.replace("http://the-sidemoney-company.local/", "/")

    res = upload(token, "tsc-chrome.css", css.encode(), "text/css")
    print(f"\nuploaded: {res['url']}  ({len(css):,} bytes)")
    print(f"localized {localized}, missing {missing}")

    req = urllib.request.Request(
        f"{API}/api/settings/site",
        data=json.dumps({"chromeCssUrl": res["url"]}).encode(),
        headers={"authorization": f"Bearer {token}", "content-type": "application/json"},
        method="PATCH")
    urllib.request.urlopen(req, timeout=60)
    print("settings.site.chromeCssUrl repointed")

    leftover = len(re.findall(r"/wp-content/", css))
    print(f"remaining /wp-content/ refs in bundle: {leftover}")


if __name__ == "__main__":
    main()
