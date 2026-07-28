#!/usr/bin/env python3
"""Elementor -> Bricks converter for tsc-beta demo site.

Reads _elementor_data postmeta, emits Bricks flat element list into
_bricks_page_content_2 (PHP-serialized) + _bricks_editor_mode='bricks'.

Mapping policy (registered in addons/tsc/demo.md):
- Core Elementor widgets -> native Bricks elements (faithful).
- Composite widgets (image-box, banners) -> Bricks block with children.
- Theme-coupled ideapark-* widgets with no Bricks equivalent -> placeholder
  block labeled IDEAPARK:<type>; original Elementor settings preserved in
  the placeholder's _cssClasses + a JSON comment child so nothing is lost.

Usage: python3 elementor-to-bricks.py [--dry-run] [--page ID]
"""
import argparse
import base64
import hashlib
import json
import subprocess
import sys

MYSQL = "/Users/bam/Library/Application Support/Local/lightning-services/mysql-8.4.0/bin/darwin-arm64/bin/mysql"
SOCK = "/Users/bam/Library/Application Support/Local/run/aMNHd3PFU/mysql/mysqld.sock"
DB = "local"
PREFIX = "smxx"


def q(sql: str) -> str:
    r = subprocess.run(
        [MYSQL, "-S", SOCK, "-u", "root", "-proot", "-N", "-B", "-e", sql],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:400])
    return r.stdout


# ---------- PHP serializer (arrays/str/int/float/bool/None) ----------

def php_serialize(v) -> bytes:
    if v is None:
        return b"N;"
    if isinstance(v, bool):
        return b"b:1;" if v else b"b:0;"
    if isinstance(v, int):
        return f"i:{v};".encode()
    if isinstance(v, float):
        return f"d:{v};".encode()
    if isinstance(v, str):
        b = v.encode("utf-8")
        return b"s:%d:\"%s\";" % (len(b), b)
    if isinstance(v, (list, tuple)):
        items = b"".join(php_serialize(i) + php_serialize(x) for i, x in enumerate(v))
        return b"a:%d:{%s}" % (len(v), items)
    if isinstance(v, dict):
        items = b"".join(php_serialize(k) + php_serialize(x) for k, x in v.items())
        return b"a:%d:{%s}" % (len(v), items)
    raise TypeError(f"unserializable: {type(v)}")


# ---------- id + element helpers ----------

def bid(seed: str) -> str:
    """Deterministic 6-char bricks id from seed."""
    return hashlib.sha1(seed.encode()).hexdigest()[:6]


class Doc:
    def __init__(self, page_id):
        self.page_id = page_id
        self.flat = []
        self.stats = {"converted": 0, "approximated": 0, "placeholder": 0}

    def add(self, name, parent, seed, settings=None, label=None):
        el = {
            "id": bid(f"{self.page_id}:{seed}"),
            "name": name,
            "parent": parent if parent else 0,
            "children": [],
            "settings": settings or {},
        }
        if label:
            el["label"] = label
        self.flat.append(el)
        if parent:
            for e in self.flat:
                if e["id"] == parent:
                    e["children"].append(el["id"])
                    break
        return el["id"]


# ---------- widget mappers ----------

def map_link(l):
    url = (l or {}).get("url") or ""
    return {"type": "external", "url": url} if url else None


def convert_widget(doc: Doc, w, parent, seed):
    t = w.get("widgetType", "")
    s = w.get("settings", {})
    if not isinstance(s, dict):  # Elementor stores [] when empty
        s = {}
    st = doc.stats

    if t == "heading":
        cfg = {"text": s.get("title", ""), "tag": s.get("header_size", "h2")}
        link = map_link(s.get("link"))
        if link:
            cfg["link"] = link
        color = s.get("title_color")
        if isinstance(color, str) and color.startswith("#"):
            cfg["_typography"] = {"color": {"hex": color}}
        doc.add("heading", parent, seed, cfg)
        st["converted"] += 1
    elif t == "text-editor":
        cfg = {"text": s.get("editor", "")}
        color = s.get("text_color")
        if isinstance(color, str) and color.startswith("#"):
            cfg["_typography"] = {"color": {"hex": color}}
        doc.add("text", parent, seed, cfg)
        st["converted"] += 1
    elif t == "image":
        img = s.get("image", {})
        url = img.get("url", "")
        cfg = {"image": {"url": url, "external": True}} if url else {}
        link = map_link(s.get("link"))
        if link:
            cfg["link"] = link
        doc.add("image", parent, seed, cfg)
        st["converted"] += 1
    elif t in ("ideapark-button", "button"):
        cfg = {"text": s.get("text", s.get("button_text", "Button"))}
        link = map_link(s.get("link"))
        if link:
            cfg["link"] = link
        doc.add("button", parent, seed, cfg)
        st["converted"] += 1
    elif t in ("icon-list", "ideapark-icon-list-1"):
        items = []
        raw = s.get("icon_list")
        for it in (raw if isinstance(raw, list) else []):
            if not isinstance(it, dict):
                continue
            entry = {"title": it.get("text", "")}
            link = map_link(it.get("link"))
            if link:
                entry["link"] = link
            items.append(entry)
        doc.add("list", parent, seed, {"items": items})
        st["converted"] += 1
    elif t == "image-box":
        blk = doc.add("block", parent, seed, label="image-box")
        url = (s.get("image") or {}).get("url", "")
        if url:
            doc.add("image", blk, seed + ":img", {"image": {"url": url, "external": True}})
        if s.get("title_text"):
            doc.add("heading", blk, seed + ":h", {"text": s["title_text"], "tag": s.get("title_size", "h3")})
        if s.get("description_text"):
            doc.add("text-basic", blk, seed + ":d", {"text": s["description_text"]})
        st["approximated"] += 1
    elif t == "spacer":
        doc.add("block", parent, seed, {"_height": f"{(s.get('space') or {}).get('size', 20)}px"}, label="spacer")
        st["approximated"] += 1
    elif t == "ideapark-social":
        doc.add("social-icons", parent, seed, {})
        st["approximated"] += 1
    elif t == "ideapark-countdown":
        due = s.get("due_date", "")
        if due:
            doc.add("countdown", parent, seed, {"date": due})
            st["approximated"] += 1
        else:
            # empty date renders as digit garbage — hide, keep data
            blk = doc.add("block", parent, seed, {"_cssClasses": "ideapark-placeholder ideapark-countdown"}, label="IDEAPARK:countdown")
            doc.add("code", blk, seed + ":code", {"code": f"<script type=\"application/json\" class=\"ideapark-orig\">{json.dumps({'widgetType': t, 'settings': s}, ensure_ascii=False)}</script>", "executeCode": False})
            st["placeholder"] += 1
    elif t == "ideapark-running-line":
        # Real marquee: Moderno's own classes, CSS ported into bricks-child
        # (moderno-port section). Content duplicated so the loop has width.
        items = [it.get("title", "").strip() for it in (s.get("item_list") or []) if isinstance(it, dict) and it.get("title")]
        line = "   ·   ".join(items) if items else ""
        wrap = doc.add("block", parent, seed, {"_cssClasses": "c-ip-running-line c-ip-running-line--active"}, label="running-line")
        for rep in range(2):
            row = doc.add("block", wrap, f"{seed}:row{rep}", {"_cssClasses": "c-ip-running-line__content"})
            doc.add("text-basic", row, f"{seed}:txt{rep}", {"text": line, "_cssClasses": "c-ip-running-line__item"})
        st["approximated"] += 1
    elif t == "ideapark-reviews":
        doc.add("testimonials", parent, seed, {})
        st["approximated"] += 1
    elif t in ("ideapark-image-list-2", "ideapark-image-list-3", "ideapark-brand-list"):
        imgs = []
        for key in ("image_list", "images", "list"):
            v = s.get(key)
            if not isinstance(v, list):
                continue
            for it in v:
                if not isinstance(it, dict):
                    continue
                u = (it.get("image") or {}).get("url") if isinstance(it.get("image"), dict) else None
                if u:
                    imgs.append({"url": u, "external": True})
        doc.add("image-gallery", parent, seed, {"items": {"images": imgs}} if imgs else {})
        st["approximated"] += 1
    elif t == "ideapark-slider":
        doc.add("slider", parent, seed, {})
        st["approximated"] += 1
    else:
        # theme-coupled / unmapped: labeled placeholder, settings preserved
        blk = doc.add("block", parent, seed, {"_cssClasses": f"ideapark-placeholder {t}"}, label=f"IDEAPARK:{t}")
        note = json.dumps({"widgetType": t, "settings": s}, ensure_ascii=False)
        doc.add("code", blk, seed + ":code", {"code": f"<!-- {t} settings preserved -->\n<script type=\"application/json\" class=\"ideapark-orig\">{note}</script>", "executeCode": False})
        st["placeholder"] += 1


def style_settings(s):
    """Carry Elementor container/section styling into Bricks settings.
    Covers what the visual audit flagged: background images, background
    colors, min-heights. Anything else stays with the builder rebuild."""
    out = {}
    bg = {}
    img = s.get("background_image")
    if isinstance(img, dict) and img.get("url"):
        bg["image"] = {"url": img["url"], "external": True}
        bg["size"] = s.get("background_size", "cover") or "cover"
        pos = s.get("background_position") or "center center"
        bg["position"] = pos
    color = s.get("background_color")
    if isinstance(color, str) and color.startswith("#"):
        bg["color"] = {"hex": color}
    if s.get("background_background") == "gradient" and isinstance(s.get("background_color_b"), str):
        # approximate gradient with its start color
        bg.setdefault("color", {"hex": s.get("background_color", "#000000")})
    if bg:
        out["_background"] = bg
    h = s.get("custom_height") or s.get("min_height")
    if isinstance(h, dict) and h.get("size"):
        out["_minHeight"] = f"{h['size']}{h.get('unit', 'px')}"
    elif s.get("height") == "full":
        out["_minHeight"] = "100vh"
    color = s.get("color_text")
    if isinstance(color, str) and color.startswith("#"):
        out["_typography"] = {"color": {"hex": color}}
    return out


def tag_el(el, eid):
    """Stamp the source Elementor id as a CSS class (el-<id>) so translated
    per-page Elementor CSS (see translate-elementor-css.py) can target the
    converted element 1:1."""
    if not eid:
        return
    cls = el["settings"].get("_cssClasses", "")
    el["settings"]["_cssClasses"] = (cls + " " if cls else "") + f"el-{eid}"


def convert_node(doc: Doc, node, parent, seed):
    et = node.get("elType")
    eid = node.get("id", "")
    s = node.get("settings", {})
    if not isinstance(s, dict):
        s = {}
    if et == "section":
        sec = doc.add("section", parent, seed, style_settings(s))
        tag_el(doc.flat[-1], eid)
        cont = doc.add("container", sec, seed + ":c")
        for i, ch in enumerate(node.get("elements", [])):
            convert_node(doc, ch, cont, f"{seed}.{i}")
    elif et == "column":
        blk = doc.add("block", parent, seed, style_settings(s), label="column")
        tag_el(doc.flat[-1], eid)
        for i, ch in enumerate(node.get("elements", [])):
            convert_node(doc, ch, blk, f"{seed}.{i}")
    elif et == "container":
        cont = doc.add("container", parent, seed, style_settings(s))
        tag_el(doc.flat[-1], eid)
        for i, ch in enumerate(node.get("elements", [])):
            convert_node(doc, ch, cont, f"{seed}.{i}")
    elif et == "widget":
        idx = len(doc.flat)
        convert_widget(doc, node, parent, seed)
        if len(doc.flat) > idx:
            tag_el(doc.flat[idx], eid)  # branch root gets the source id


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--page", type=int)
    args = ap.parse_args()

    # --page converts that ID regardless of post type (footer/header sources
    # live in Moderno's html_block CPT); bulk run stays scoped to pages.
    scope = f"AND p.ID={args.page}" if args.page else "AND p.post_type='page'"
    rows = q(
        f"SELECT p.ID, TO_BASE64(MAX(em.meta_value)) FROM {DB}.{PREFIX}posts p "
        f"JOIN {DB}.{PREFIX}postmeta em ON em.post_id=p.ID AND em.meta_key='_elementor_data' "
        f"AND LENGTH(em.meta_value)>10 WHERE p.post_status='publish' {scope} "
        f"GROUP BY p.ID"
    ).strip().splitlines()

    print(f"{'ID':>7}  {'conv':>4} {'appr':>4} {'plch':>4}  status")
    for row in rows:
        pid, b64 = row.split("\t")
        data = json.loads(base64.b64decode(b64.replace("\\n", "")).decode("utf-8", "replace"))
        doc = Doc(pid)
        for i, node in enumerate(data):
            convert_node(doc, node, 0, str(i))
        ser = php_serialize(doc.flat)
        if not args.dry_run:
            payload = base64.b64encode(ser).decode()
            q(
                f"DELETE FROM {DB}.{PREFIX}postmeta WHERE post_id={pid} AND meta_key IN ('_bricks_page_content_2','_bricks_editor_mode');"
                f"INSERT INTO {DB}.{PREFIX}postmeta (post_id, meta_key, meta_value) VALUES "
                f"({pid}, '_bricks_page_content_2', FROM_BASE64('{payload}')),"
                f"({pid}, '_bricks_editor_mode', 'bricks');"
            )
        s = doc.stats
        print(f"{pid:>7}  {s['converted']:>4} {s['approximated']:>4} {s['placeholder']:>4}  {'dry' if args.dry_run else 'written'} ({len(doc.flat)} elements)")


if __name__ == "__main__":
    main()
