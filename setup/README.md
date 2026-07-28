# setup — one-command install for TSC-BETA

`install.sh` read registry across base kit (`addons/base`) **and every addon**
(`addons/<tool>`), pull each tool enable command, check prereqs, install
opt-in tools. Registry files stay single source of truth — update tables,
re-run, nothing to sync.

## Run
```bash
cd "TSC-BETA"
chmod +x setup/install.sh
./setup/install.sh          # interactive — asks before each command
./setup/install.sh --all    # non-interactive — install everything
```

## What it does
1. Check prereqs (git, curl required; node/npm/npx, python3/pip, uv, claude used per-tool), report what missing — with exact command to install anything missing.
2. Walk `addons/base` then every `addons/<tool>` folder, pull backticked commands from `skills.md` + `mcp.md`, run install/enable ones. Translate `/plugin install X` to `claude plugin install X`; skip claude-CLI commands if `claude` absent.
3. List MCP **connectors** (Filesystem, Google Drive, Chrome, Apify, GitHub, Notion, …) that use OAuth / Claude Desktop GUI, can't be scripted — connect those in Settings → Connectors.

## Safety
- Every command printed before run; interactive mode confirms each.
- Commands come from your own registry files, not internet. Read first.
- Some tools install via `curl … | bash` from own repo — those run only if you confirm.

## Notes
- Extraction heuristic: run entries that look like installs (`install`, `mcp add`, `/plugin`, `plugin marketplace`, `tool install`, `npm i`, `pip install`, `uv tool`, `uvx`, `npx`). Usage-only snippets ignored.
- Any tool whose exact command not in registry prints nothing to run — install by hand from its repo. Verify commands against each source before trusting.
- Also see `setup/token-stack.md` for tested ~40% Claude Code token-efficiency stack.