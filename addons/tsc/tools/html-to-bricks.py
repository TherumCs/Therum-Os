#!/usr/bin/env python3
"""Decompose rendered HTML fragments into REAL Bricks element trees.

Every ported raw-HTML text-basic blob (header, footer, tickers, banners,
news carousel, season panels) becomes a structured, builder-editable tree:

  <div class>          -> div      (settings._cssClasses)
  <section|ul|li|...>  -> div      (settings.tag custom + customTag)
  <h1..h6>             -> heading  (settings.tag, text)
  text node            -> text-basic (settings.text, tag span)
  <img>                -> image    (settings.image.url external)
  <svg>                -> svg      (settings.code — Bricks' own svg element
                                    stores raw svg code natively)
  <a>                  -> div w/ customTag a + href attribute (children kept)

class -> _cssClasses, id -> _cssId, href/data-*/aria-* -> _attributes.
Output: flat Bricks element list (id/name/parent/children/settings) ready to
splice into _bricks_page_content_2 / header / footer metas.
"""
import hashlib
import re
from html.parser import HTMLParser

VOID = {"img", "br", "hr", "input", "meta", "link", "source"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


def bid(seed, n):
    return hashlib.sha1(f"{seed}:{n}".encode()).hexdigest()[:6]


class Frag:
    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children = []  # Frag | str


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Frag("__root__", [])
        self.stack = [self.root]
        self.svg_depth = 0
        self.svg_buf = []

    def handle_starttag(self, tag, attrs):
        if self.svg_depth:
            a = "".join(f' {k}="{v}"' for k, v in attrs)
            self.svg_buf.append(f"<{tag}{a}>")
            if tag == "svg":
                self.svg_depth += 1
            return
        if tag == "svg":
            self.svg_depth = 1
            a = "".join(f' {k}="{v}"' for k, v in attrs)
            self.svg_buf = [f"<{tag}{a}>"]
            return
        f = Frag(tag, attrs)
        self.stack[-1].children.append(f)
        if tag not in VOID:
            self.stack.append(f)

    def handle_endtag(self, tag):
        if self.svg_depth:
            self.svg_buf.append(f"</{tag}>")
            if tag == "svg":
                self.svg_depth -= 1
                if self.svg_depth == 0:
                    f = Frag("__svg__", [])
                    f.code = "".join(self.svg_buf)
                    self.stack[-1].children.append(f)
            return
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.svg_depth:
            self.svg_buf.append(data)
            return
        if data.strip():
            self.stack[-1].children.append(re.sub(r"\s+", " ", data).strip())


def parse(html):
    p = Parser()
    p.feed(html)
    return p.root


def to_elements(html, seed, root_parent=0, extra_root_classes=""):
    """Return (flat_element_list, root_ids)."""
    tree = parse(html)
    out = []
    counter = [0]

    def mk(name, parent, settings):
        counter[0] += 1
        el = {"id": bid(seed, counter[0]), "name": name, "parent": parent,
              "children": [], "settings": settings}
        out.append(el)
        return el

    def attrs_settings(f):
        s = {}
        cls = f.attrs.get("class", "")
        if cls:
            s["_cssClasses"] = cls
        if f.attrs.get("id"):
            s["_cssId"] = f.attrs["id"]
        extra = []
        for k, v in f.attrs.items():
            if k in ("class", "id", "style"):
                continue
            extra.append({"id": bid(seed, f"{counter[0]}:{k}"), "name": k, "value": v or ""})
        if f.attrs.get("style"):
            s["_cssCustom"] = ""  # inline styles are dropped; theme CSS governs
            extra.append({"id": bid(seed, f"{counter[0]}:style"), "name": "style", "value": f.attrs["style"]})
        if extra:
            s["_attributes"] = extra
        return s

    def walk(f, parent):
        if isinstance(f, str):
            el = mk("text-basic", parent, {"text": f, "tag": "span"})
            return el["id"]
        if f.tag == "__svg__":
            el = mk("svg", parent, {"source": "code", "code": f.code})
            return el["id"]
        if f.tag == "img":
            s = attrs_settings(f)
            src = f.attrs.get("src", "")
            s["image"] = {"url": src, "external": True, "filename": src.rsplit("/", 1)[-1]}
            if f.attrs.get("alt"):
                s["altText"] = f.attrs["alt"]
            el = mk("image", parent, s)
            return el["id"]
        if f.tag in HEADINGS:
            s = attrs_settings(f)
            s["tag"] = f.tag
            inner = "".join(c if isinstance(c, str) else "" for c in f.children)
            if inner and all(isinstance(c, str) for c in f.children):
                s["text"] = inner
                el = mk("heading", parent, s)
                return el["id"]
            el = mk("heading", parent, s)
            for c in f.children:
                cid = walk(c, el["id"])
                el["children"].append(cid)
            return el["id"]
        # generic structural node
        s = attrs_settings(f)
        if f.tag == "a":
            s["tag"] = "custom"
            s["customTag"] = "a"
        elif f.tag != "div":
            s["tag"] = "custom"
            s["customTag"] = f.tag
        el = mk("div", parent, s)
        for c in f.children:
            cid = walk(c, el["id"])
            el["children"].append(cid)
        return el["id"]

    root_ids = []
    for c in tree.children:
        rid = walk(c, root_parent)
        root_ids.append(rid)
    if extra_root_classes and root_ids:
        first = next(e for e in out if e["id"] == root_ids[0])
        cur = first["settings"].get("_cssClasses", "")
        first["settings"]["_cssClasses"] = (extra_root_classes + " " + cur).strip()
    return out, root_ids


if __name__ == "__main__":
    import sys, json
    html = sys.stdin.read()
    els, roots = to_elements(html, sys.argv[1] if len(sys.argv) > 1 else "frag")
    print(json.dumps({"elements": els, "roots": roots}, indent=1))
