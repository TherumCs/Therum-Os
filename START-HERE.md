# TSC-BETA — Start Here
Portable agent OS. Drop in any project; run same.

## Structure
- `_core/`   → UNIVERSAL engine. Never edit per project.
  - `claude.md`   — rules + 10 Rules. Read FIRST.
  - `loop.md`     — task loop + DROP ZONE (drop specs here).
  - `memory.md`   — volatile working state. Update every loop.
  - `autonomy.md` — machinery for unattended run. On demand.
  - `operator.md`  — cross-session operator layer (learning, memory, hooks, security). On demand.
- `context.md` → PER-USER. Claude fill from what you tell it. Start empty.
- `addons/`   → TOOL-SPECIFIC + defaults. ONE place "specific" live.
  - `base/`      — built-in default kit: universal skills + MCP connectors. Every tool inherit it.
  - `tsc/`     — this instance purpose: The Sidemoney Company beta (skills + connectors + knowledge, filled as work define).
  - `_template/` — copy this to start new tool addon.
- `setup/`    → one-command installer. `./setup/install.sh` read base registry, install opt-in tools (interactive; `--all` for everything).

## The universal / specific line
`_core/` = universal, same everywhere. `addons/<tool>/` = specific to one tool. If specific, go in addon — never `_core/`.

## Run order (every loop)
_core/claude.md → context.md → _core/memory.md → _core/loop.md → DROP ZONE → act → update _core/memory.md.
Work on addon? Read `addons/<tool>/manifest.json` (auto-router index — map intent to right knowledge/skills/servers) first, if present, then load `addons/<tool>/`. Run unattended? Also load `_core/autonomy.md`.

## Using it
1. Tell Claude who you are + what you build — it record durable parts in `context.md`.
2. Drop task (with exit signal) into DROP ZONE in `_core/loop.md`.
3. Claude run one task per pass, verify, update `memory.md`. You call "done."

## Reuse
Copy folder for new project. `_core/` stay as-is; `context.md` + `memory.md` refill from scratch; add your tool under `addons/`.