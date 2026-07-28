# addons — Tool-Specific Layers
Everything specific to tool you build lives here. One folder per tool.
`_core/` universal, never change. `addons/` where "specific" go — so universal vs specific never confused.

## An addon holds
- `skills.md` — that tool's actual skills (discrete, invocable capabilities).
- `mcp.md` — that tool's connectors.
- `knowledge/` — that tool's reference material.
- (optional) autonomy implementation — that tool's loop / cron / ledger scripts.

## Load order
For task on tool X: `_core/` (rules + loop + memory) + `context.md` (user) + `addons/X/` (its skills, connectors, knowledge).
Load only addon for tool in play. Never load every addon at once.

## Start a new tool
Copy `addons/_template/` to `addons/<tool-name>/`, fill in.

## Built-in
- `base/` — default kit every tool inherit: universal skills + MCP connectors.
- `studio/` — this instance's own skills + connectors (run TSC-BETA itself — scope not yet defined, currently stub).
- `_template/` — blank scaffold for new tool.