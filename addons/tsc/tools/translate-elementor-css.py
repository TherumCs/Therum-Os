#!/usr/bin/env python3
"""Translate Elementor generated per-page CSS into Bricks-compatible CSS.

Source: wp-content/uploads/elementor/css/post-<ID>.css (the exact rendered
design spec of the Moderno production pages — positions, sizes, typography).
Converted elements carry class `el-<elementorId>` (converter v5), so the
translation is selector rewriting, not guesswork:

  .elementor-165012 .elementor-element.elementor-element-abc123  ->  .el-abc123
  inner wrappers (.elementor-widget-container, .elementor-heading-title,
  .elementor-button, .elementor-column-wrap, ...)                 ->  dropped
  section containers (> .elementor-container)                    ->  dropped

Output: one combined stylesheet written to bricks-child/moderno-elementor-port.css
(enqueued by the child theme). Rerunnable.
"""
import re
import sys
from pathlib import Path

SOURCES = [
    # (label, path)
    ("kit-164552", "/Users/bam/Local Sites/the-sidemoney-company/app/public/wp-content/uploads/elementor/css/post-164552.css"),
    ("home-165012", "/Users/bam/Local Sites/tsc-beta/app/public/wp-content/uploads/elementor/css/post-165012.css"),
    ("contact-147399", "/Users/bam/Local Sites/the-sidemoney-company/app/public/wp-content/uploads/elementor/css/post-147399.css"),
    ("footer-505", "/Users/bam/Local Sites/the-sidemoney-company/app/public/wp-content/uploads/elementor/css/post-505.css"),
    # about CSS regenerated from source site when available:
    ("about-165613", "/Users/bam/Local Sites/tsc-beta/app/public/wp-content/uploads/elementor/css/post-165613.css"),
]

OUT = "/Users/bam/Local Sites/tsc-beta/app/public/wp-content/themes/bricks-child/moderno-elementor-port.css"


# Elementor container-era layout ships as CSS custom properties consumed by
# Elementor's frontend core CSS (.e-con{min-height:var(--min-height);...}),
# which Bricks never loads. Convert the layout vars to the real properties.
LAYOUT_VARS = (
    "display", "min-height", "height", "width", "max-width",
    "flex-direction", "justify-content", "align-items", "align-content",
    "flex-wrap", "gap", "row-gap", "column-gap",
    "flex-grow", "flex-shrink", "align-self", "order",
    "position", "z-index", "overflow", "top", "right", "bottom", "left",
    "padding", "margin", "border-radius",
)
_UNVAR = re.compile(r"--(" + "|".join(LAYOUT_VARS) + r"):")


def translate(css: str) -> str:
    # element id hooks
    css = re.sub(r"\.elementor-element\.elementor-element-([0-9a-f]+)", r".el-\1", css)
    css = re.sub(r"\.elementor-element-([0-9a-f]+)", r".el-\1", css)
    # chained structural classes converted elements don't carry
    css = re.sub(r"(\.el-[0-9a-f]+)\.elementor-element", r"\1", css)
    css = re.sub(r"(\.el-[0-9a-f]+)\.e-con(-full|-boxed)?", r"\1", css)
    # container-era layout vars -> real properties
    css = _UNVAR.sub(lambda m: m.group(1) + ":", css)
    # page scope prefixes
    css = re.sub(r"\.elementor-\d+\s+", "", css)
    css = re.sub(r"\.elementor-kit-\d+", ":root", css)
    # inner wrappers Bricks doesn't have — collapse onto the element itself
    for inner in (
        r"\s*>\s*\.elementor-widget-container",
        r"\s+\.elementor-widget-container",
        r"\s*>\s*\.elementor-container",
        r"\s+\.elementor-container",
        r"\s*>\s*\.elementor-column-wrap",
        r"\s+\.elementor-widget-wrap",
        r"\s+\.elementor-heading-title",
        r"\s*>\s*\.elementor-heading-title",
        r"\s+\.elementor-button",
        r"\s+\.elementor-text-editor",
    ):
        css = re.sub(inner, "", css)
    # icon list structure -> plain list
    css = css.replace(".elementor-icon-list-items", "ul")
    css = css.replace(".elementor-icon-list-item", "li")
    css = css.replace(".elementor-icon-list-text", "span")
    # image widget wrapper
    css = css.replace(".elementor-widget-image img", "img")
    # leftover elementor state/structural classes that have no Bricks twin:
    # neutralize by making them match nothing harmful (drop whole rule is
    # overkill; these selectors simply won't match and that's fine).
    return css


SHIM = """/* ===== bricks-side shim ===== */
/* Converted Elementor containers behave like e-con: flex column by default,
   full-bleed at root. Bricks container max-width must not box them. */
[class*="el-"].brxe-container, [class*="el-"].brxe-block, [class*="el-"].brxe-section {
  display: flex; flex-direction: column; max-width: 100%;
}
#brx-content > [class*="el-"],
#brx-header > [class*="el-"],
#brx-footer > [class*="el-"] { width: 100%; }
#brx-content, #brx-header, #brx-footer { max-width: 100%; }
/* Elementor's frontend clips decorative over-wide elements (serial ticker,
   letter-spaced headings) at the page edge; without its wrappers the page
   gains a huge horizontal scroll — clip it like production does. */
html, body { overflow-x: clip; }
[class*="el-"] { min-width: 0; }
"""


def main():
    parts = [SHIM]
    for label, path in SOURCES:
        p = Path(path)
        if not p.exists():
            print(f"skip (missing): {label}")
            continue
        parts.append(f"/* ===== {label} ===== */\n" + translate(p.read_text()))
        print(f"translated: {label} ({p.stat().st_size} bytes)")
    Path(OUT).write_text("\n\n".join(parts))
    print(f"wrote {OUT} ({Path(OUT).stat().st_size} bytes)")


if __name__ == "__main__":
    main()
