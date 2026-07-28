# token-stack.md — Claude Code Token-Efficiency Stack (SOTA, ~40% tested)
TSC-BETA · setup · UNIVERSAL. A tested layered stack for cutting tokens in the Claude Code workflow. Set this up once in Claude Code. Source: user-provided, community-tested (~40% avg reduction).

## Read first — integration notes (avoid collisions)
- **One proxy on ANTHROPIC_BASE_URL.** Layer 5 (cache-fix) uses `http://127.0.0.1:9801`. Headroom (8787) and pxpipe are ALSO proxies — you can only point ANTHROPIC_BASE_URL at one. Pick a lane: run THIS stack's cache-fix proxy, OR Headroom, not both. (base/mcp.md Headroom/pxpipe are alternatives to this lane.)
- **rtk overlap:** rtk here is standalone (Layer 3). It's also bundled inside Headroom and caveman-code. If you run this stack, rtk standalone is the source of truth.
- **Model IDs below are examples** — set them to current model ids at setup time.
- Settings/hooks/shell edits are manual config (the installer can't do these) — this file is the guide.

## Layers (install in order)
1. **codebase-memory-mcp** (DeusData) — codebase memory MCP.
   `curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash`
   `codebase-memory-mcp config set auto_index true`
2. **context-mode** (mksglu) — context plugin.
   `/plugin marketplace add mksglu/context-mode` · `/plugin install context-mode@context-mode` · `/reload-plugins` · `/context-mode:ctx-doctor`
3. **rtk** (rtk-ai) — shell-output rewriter.
   `brew install rtk` · `rtk init -g`
4. **caveman** (JuliusBrussee) — output compression (see base/mcp.md; skip output mode if already terse).
   `curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash`
5. **claude-code-cache-fix** (cnighswonger) — cache-fix proxy.
   `npm install -g claude-code-cache-fix` · `cache-fix-proxy install-service`
   Then wire `ANTHROPIC_BASE_URL` (settings.json + shell) + launchctl bootstrap/enable/kickstart the plist.
6. **ponytail** (DietrichGebert) — code-minimization workflow (YAGNI ladder).
   `/plugin marketplace add DietrichGebert/ponytail` · `/plugin install ponytail@ponytail` · `/reload-plugins`
   Config `~/.config/ponytail/config.json` → `{"defaultMode": "off"}`; enable per session with `/ponytail full`.
   Modes: `/ponytail lite|full|ultra|off`; reports: `/ponytail-review|-audit|-debt|-gain`.

After each layer, verify with Claude: "Is <tool> installed correctly and fully integrated into Claude Code?" (repo link).

## settings.json (Claude Code)
```
"ANTHROPIC_BASE_URL": "http://127.0.0.1:9801",        // cache-fix proxy
"ENABLE_TOOL_SEARCH": "true",                          // keep tool-search deferral behind proxy
"CLAUDE_CODE_DISABLE_LEGACY_MODEL_REMAP": "1",         // stop silent model remap on update
"ANTHROPIC_MODEL": "<current-opus-id>[1m]",            // pin + [1m] for 1M context beta header
"ANTHROPIC_SMALL_FAST_MODEL": "<current-haiku-id>",
"ENABLE_PROMPT_CACHING_1H": "1",                       // 1h prompt cache vs 5min default
"BASH_MAX_OUTPUT_LENGTH": "10000",                     // bash output cap
"MAX_MCP_OUTPUT_TOKENS": "10000",                      // MCP output cap
"CACHE_FIX_IMAGE_KEEP_LAST": "3",                      // drop Read images older than last 3
"effortLevel": "medium",                               // ~xhigh quality for 95% of tasks; raise for hard debug
"autoCompactEnabled": false,                           // manual /compact instead of bloated auto-compact
"skipDangerousModePermissionPrompt": true,
"skipAutoPermissionPrompt": true
```
(Note: a prior "CLAUDE_CODE_SUBAGENT_MODEL" pin was removed — it broke fork agents.)

## Hooks (settings.json "hooks") — reference: github.com/sgaabdu4/claude-code-tips/tree/main/hooks
- PreToolUse Bash → bash-ban-raw-tools → `rtk hook claude`
- PreToolUse Grep|Glob|Read → cbm-code-discovery-gate
- PostToolUse * → cbm-mcp-marker
- SessionStart * → context-mode-cache-heal → memory-repo-symlink → cbm-session-reminder
- Plugin-internal auto: caveman-activate, ponytail-activate; UserPromptSubmit trackers.
All custom hooks in `~/.claude/hooks/` (chmod +x), session_id-keyed via stdin JSON.

## shell (~/.zshrc / ~/.bashrc)
```
export PATH="$HOME/.local/bin:$PATH"
export ANTHROPIC_BASE_URL=http://127.0.0.1:9801
if command -v rtk >/dev/null 2>&1; then
  alias git='rtk git'; alias ls='rtk ls'; alias cat='rtk read'; alias grep='rtk grep'
fi
```

## savings dashboards
`cbm_list_projects` (mcp) · `/ctx-stats` · `rtk gain` (`--history`) · `/caveman-stats` · `/ponytail-gain`

## updates (re-verify with Claude periodically)
`codebase-memory-mcp update` · `/ctx-upgrade` · `brew upgrade rtk` · `/reload-plugins` (caveman+ponytail) · `npm update -g claude-code-cache-fix`
