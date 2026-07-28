#!/usr/bin/env python3
"""Replace every raw-HTML text-basic blob in the Bricks metas with real
element trees (html-to-bricks decomposer). Rerunnable.

Targets:
  home (165012)  _bricks_page_content_2 : tickers, trio, band, carousel,
                                          season panels (tscbrd1/2)
  header (165645) _bricks_page_header_2 : whole header blob
  footer (165646) _bricks_page_footer_2 : whole footer blob
"""
import importlib.util
import json
import subprocess
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "h2b", str(Path(__file__).parent / "html-to-bricks.py"))
h2b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h2b)

MYSQL = "/Users/bam/Library/Application Support/Local/lightning-services/mysql-8.4.0/bin/darwin-arm64/bin/mysql"
SOCK = "/Users/bam/Library/Application Support/Local/run/aMNHd3PFU/mysql/mysqld.sock"
PHP = sorted(__import__("glob").glob(
    "/Users/bam/Library/Application Support/Local/lightning-services/php-8.5*/bin/darwin-arm64/bin/php"))[0]


def read_meta(post, key):
    r = subprocess.run([MYSQL, "-S", SOCK, "-u", "root", "-proot", "-N", "--raw", "-e",
                        f"SELECT meta_value FROM local.smxxpostmeta WHERE post_id={post} AND meta_key='{key}'"],
                       capture_output=True, text=True)
    Path("/tmp/deblob-in.ser").write_text(r.stdout.rstrip("\n"))
    p = subprocess.run([PHP, "-r",
        'echo json_encode(unserialize(trim(file_get_contents("/tmp/deblob-in.ser"))));'],
        capture_output=True, text=True)
    return json.loads(p.stdout)


def write_meta(post, key, els):
    Path("/tmp/deblob-out.json").write_text(json.dumps(els))
    subprocess.run([PHP, "-r",
        'file_put_contents("/tmp/deblob-out.ser", serialize(json_decode(file_get_contents("/tmp/deblob-out.json"), true)));'],
        check=True)
    hexv = Path("/tmp/deblob-out.ser").read_bytes().hex()
    Path("/tmp/deblob.sql").write_text(
        f"UPDATE smxxpostmeta SET meta_value = UNHEX('{hexv}') WHERE post_id={post} AND meta_key='{key}';")
    subprocess.run(f'"{MYSQL}" -S "{SOCK}" -u root -proot local < /tmp/deblob.sql', shell=True, check=True)


def deblob(els, seed_prefix):
    """Replace text-basic elements whose text contains markup with subtrees."""
    out = []
    n = 0
    for el in els:
        text = el.get("settings", {}).get("text", "")
        is_blob = el.get("name") == "text-basic" and isinstance(text, str) and "<" in text and ">" in text
        if not is_blob:
            out.append(el)
            continue
        n += 1
        keep_cls = el.get("settings", {}).get("_cssClasses", "")
        sub, roots = h2b.to_elements(text, f"{seed_prefix}:{el['id']}")
        if len(roots) == 1:
            # graft: the single subtree root REPLACES the blob element in place
            root = next(e for e in sub if e["id"] == roots[0])
            root["parent"] = el["parent"]
            cur = root["settings"].get("_cssClasses", "")
            root["settings"]["_cssClasses"] = (keep_cls + " " + cur).strip()
            old_id, new_id = el["id"], root["id"]
            # keep the ORIGINAL id so parent children lists + el-classes stay valid
            root["id"] = old_id
            for e in sub:
                if e["parent"] == new_id:
                    e["parent"] = old_id
            out.extend(sub)
        else:
            # multiple roots: blob element becomes a plain div holding them
            el = dict(el)
            el["name"] = "div"
            el["settings"] = {k: v for k, v in el["settings"].items() if k != "text"}
            el["children"] = roots
            for e in sub:
                if e["parent"] == 0:
                    e["parent"] = el["id"]
            out.append(el)
            out.extend(sub)
    return out, n


def run(post, key, label):
    els = read_meta(post, key)
    els2, n = deblob(els, f"{label}")
    write_meta(post, key, els2)
    print(f"{label}: {n} blobs -> trees; elements {len(els)} -> {len(els2)}")


if __name__ == "__main__":
    run(165012, "_bricks_page_content_2", "home")
    run(165645, "_bricks_page_header_2", "header")
    run(165646, "_bricks_page_footer_2", "footer")
