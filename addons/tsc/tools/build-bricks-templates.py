#!/usr/bin/env python3
"""Create Bricks header + footer templates on tsc-beta.

Header: white bar — Sidemoney signature logo (left), Main Menu nav (right).
Footer: converted from Moderno's Elementor footer block (html_block 505).
Meta shape copied from a real Bricks install (bam-leon posts 37/91):
  _bricks_template_type: header|footer
  _bricks_page_header_2 / _bricks_page_footer_2: flat element list
  _bricks_template_settings: templateConditions main=any (entire site)
Rerunnable: replaces templates with the same slug.
"""
import base64
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import importlib

conv = importlib.import_module("elementor-to-bricks")

MYSQL = conv.MYSQL
SOCK = conv.SOCK
DB, PREFIX = conv.DB, conv.PREFIX
q = conv.q
ser = conv.php_serialize

LOGO = "http://localhost:10009/wp-content/uploads/2026/03/full-sig-black.png"
MENU_ID = "278"  # Main Menu: New Arrivals, Mens, Womens, Playmoney, House Money, Contact


def header_elements():
    root = {
        "id": "hdroot", "name": "section", "parent": 0, "children": ["hdrcon"],
        "settings": {
            "_background": {"color": {"hex": "#ffffff"}},
            "_padding": {"top": "10", "right": "20", "bottom": "10", "left": "20"},
        },
    }
    con = {
        "id": "hdrcon", "name": "container", "parent": "hdroot",
        "children": ["hdrlog", "hdrnav"],
        "settings": {
            "_direction": "row",
            "_alignItems": "center",
            "_justifyContent": "space-between",
            "_columnGap": "30",
        },
    }
    logo = {
        "id": "hdrlog", "name": "image", "parent": "hdrcon", "children": [],
        "settings": {
            "image": {"url": LOGO, "external": True},
            "link": {"type": "external", "url": "/"},
            "_width": "180px",
            "altText": "The Sidemoney Company",
        },
    }
    nav = {
        "id": "hdrnav", "name": "nav-menu", "parent": "hdrcon", "children": [],
        "settings": {"menu": MENU_ID},
    }
    return [root, con, logo, nav]


def footer_elements():
    rows = q(
        f"SELECT TO_BASE64(meta_value) FROM {DB}.{PREFIX}postmeta "
        f"WHERE post_id=505 AND meta_key='_elementor_data'"
    ).strip()
    data = json.loads(base64.b64decode(rows.replace("\\n", "")).decode("utf-8", "replace"))
    doc = conv.Doc("tpl-footer")
    for i, node in enumerate(data):
        conv.convert_node(doc, node, 0, str(i))
    return doc.flat


def upsert(slug, title, ttype, elements):
    meta_key = f"_bricks_page_{ttype}_2"
    payload = base64.b64encode(ser(elements)).decode()
    settings = base64.b64encode(ser({"templateConditions": [{"main": "any"}]})).decode()
    q(
        f"USE {DB}; DELETE p, m FROM {PREFIX}posts p LEFT JOIN {PREFIX}postmeta m ON m.post_id=p.ID "
        f"WHERE p.post_type='bricks_template' AND p.post_name='{slug}';"
    )
    q(
        f"INSERT INTO {DB}.{PREFIX}posts (post_author, post_date, post_date_gmt, post_content, post_title, "
        f"post_excerpt, post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged, "
        f"post_modified, post_modified_gmt, post_content_filtered, post_parent, guid, menu_order, post_type, "
        f"post_mime_type, comment_count) VALUES (1, NOW(), UTC_TIMESTAMP(), '', '{title}', '', 'publish', "
        f"'closed', 'closed', '', '{slug}', '', '', NOW(), UTC_TIMESTAMP(), '', 0, '', 0, 'bricks_template', '', 0);"
    )
    pid = q(f"SELECT ID FROM {DB}.{PREFIX}posts WHERE post_type='bricks_template' AND post_name='{slug}'").strip()
    q(
        f"INSERT INTO {DB}.{PREFIX}postmeta (post_id, meta_key, meta_value) VALUES "
        f"({pid}, '{meta_key}', FROM_BASE64('{payload}')),"
        f"({pid}, '_bricks_template_type', '{ttype}'),"
        f"({pid}, '_bricks_template_settings', FROM_BASE64('{settings}')),"
        f"({pid}, '_bricks_editor_mode', 'bricks');"
    )
    print(f"{ttype}: post {pid} '{title}' ({len(elements)} elements)")


if __name__ == "__main__":
    upsert("tsc-site-header", "TSC Site Header", "header", header_elements())
    upsert("tsc-site-footer", "TSC Site Footer", "footer", footer_elements())
