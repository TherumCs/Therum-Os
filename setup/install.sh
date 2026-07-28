#!/usr/bin/env bash
# TSC-BETA universal installer.
# Reads the registry across _core's kit (addons/base) AND every addon (addons/<tool>),
# pulls each tool's enable/install command out of the tables, checks prerequisites, and
# installs the opt-in tools. Interactive by default; `--all` / `-y` runs non-interactively.
#
# MCP connectors that use OAuth / the Claude Desktop GUI can't be scripted; they're listed
# at the end so you can connect them in Settings -> Connectors.
#
# Safety: nothing runs without being printed first. Interactive mode asks per command.
# Commands are read straight from the registry files, so those stay the single source of truth.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ASSUME_YES=0
case "${1:-}" in --all|-y|--yes) ASSUME_YES=1 ;; esac

say(){ printf '%s\n' "$*"; }
have(){ command -v "$1" >/dev/null 2>&1; }

# ---------------------------------------------------------------- prerequisites
say "== Prerequisites (if MISS, run the command shown) =="
hint(){ case "$1" in
  git)         echo "xcode-select --install   # or: brew install git" ;;
  curl)        echo "brew install curl" ;;
  node|npm|npx) echo "brew install node   # or https://nodejs.org" ;;
  python3|pip) echo "brew install python" ;;
  uv)          echo "curl -LsSf https://astral.sh/uv/install.sh | sh" ;;
  claude)      echo "npm i -g @anthropic-ai/claude-code   # Claude Code CLI" ;;
  *)           echo "see the tool's site" ;;
esac; }
missing=0
for c in git curl; do
  if have "$c"; then say "  ok   $c"; else say "  MISS $c (required)  -> $(hint $c)"; missing=1; fi
done
for c in node npm npx python3 pip uv claude; do
  if have "$c"; then say "  ok   $c"; else say "  --   $c (some tools need it)  -> $(hint $c)"; fi
done
[ "$missing" -eq 1 ] && { say ""; say "Install the MISS (required) tools with the commands shown above, then re-run this script."; exit 1; }
say ""

# ------------------------------------------------ extract backticked commands from a table
extract(){ # $1 = file  ->  name<TAB>command per backticked command
  awk -F'|' '
    /^\|/ && $0 !~ /^\|[-: ]+\|/ && $0 !~ /What it does/ && $0 !~ /What Claude can do/ {
      name=$2; gsub(/^[ *]+|[ *]+$/,"",name); if (name=="Skill"||name=="Tool"||name=="Server"||name=="") next;
      line=$0;
      while (match(line, /`[^`]+`/)) {
        cmd=substr(line, RSTART+1, RLENGTH-2);
        print name "\t" cmd;
        line=substr(line, RSTART+RLENGTH);
      }
    }' "$1"
}

# --------------------------------- collect GUI/OAuth connectors (status rows, no command)
connectors(){ # $1 = mcp.md file  ->  connector names
  awk -F'|' '
    /^\|/ && $0 !~ /^\|[-: ]+\|/ && $0 !~ /What Claude can do/ {
      name=$2; gsub(/^[ *]+|[ *]+$/,"",name); if(name==""||name=="Server") next;
      if ($0 ~ /`/) next;
      last=$(NF-1); gsub(/^ +| +$/,"",last);
      if (last ~ /connect|connected|reconnect|available|needed/) print name;
    }' "$1"
}

translate(){ case "$1" in
  /plugin\ *)                    printf 'claude %s' "${1#/}" ;;
  pip\ install\ *)              printf 'uv tool install %s' "${1#pip install }" ;;   # no system pip on macOS; uv brings its own Python
  pip3\ install\ *)             printf 'uv tool install %s' "${1#pip3 install }" ;;
  "uv tool install --python"*)  printf '%s' "$1" ;;                                    # already pinned
  "uv tool install "*)          printf 'uv tool install --python 3.12 %s' "${1#uv tool install }" ;;  # pin a modern Python (Apple ships 3.9)
  *)                            printf '%s' "$1" ;;
esac; }

is_install(){
  case "$1" in
    *install*|*"mcp add"*|/plugin\ *|*"plugin marketplace"*|*"tool install"*|npm\ i*|pip\ install*|uv\ tool*|uvx\ *|npx\ *) return 0 ;;
    *) return 1 ;;
  esac
}

run_cmd(){
  local raw="$1" cmd; cmd="$(translate "$raw")"
  case "$cmd" in claude\ *) have claude || { say "     (needs the 'claude' CLI - skipping)"; return; } ;; esac
  case "$cmd" in "claude mcp add "*) case "$cmd" in *" -- "*|*http*) ;; *) say "     (incomplete 'claude mcp add' — needs a command/URL; skipping)"; return ;; esac ;; esac
  say "     \$ $cmd"
  if [ "$ASSUME_YES" -eq 0 ]; then
    printf '     run this? [y/N] '; read -r ans </dev/tty || ans=""
    case "$ans" in y|Y|yes) ;; *) say "     skipped"; return ;; esac
  fi
  eval "$cmd" && say "     ok" || say "     FAILED (continuing)"
}

process_dir(){ # $1 dir  $2 label
  local d="$1"
  [ -f "$d/skills.md" ] || [ -f "$d/mcp.md" ] || return
  say "== $2 =="
  for f in "$d/skills.md" "$d/mcp.md"; do
    [ -f "$f" ] || continue
    extract "$f" | while IFS="$(printf '\t')" read -r name cmd; do
      is_install "$cmd" || continue
      say "-- $name"; run_cmd "$cmd"
    done
  done
  say ""
}

# ------------------------------------------------------------------------------- run
process_dir "$ROOT/addons/base" "Base (universal)"
for d in "$ROOT"/addons/*/; do
  d="${d%/}"; b="$(basename "$d")"
  case "$b" in base|_template) continue ;; esac
  process_dir "$d" "Addon: $b"
done

# connectors that need manual connect
say "== MCP connectors - connect in Claude Desktop -> Settings -> Connectors =="
{ for f in "$ROOT"/addons/*/mcp.md; do [ -f "$f" ] && connectors "$f"; done; } | sort -u | sed 's/^/  - /'
say "  (OAuth/GUI connectors can't be scripted. GitHub can also use the CLI:"
say "   claude mcp add --transport http github https://api.githubcopilot.com/mcp/ )"
say ""
say "== Notes =="
say "  - cavemem installs with caveman-code (no separate step)."
say "  - OAuth/GUI connectors above can't be scripted — connect them in Claude Desktop."
say ""
say "Done. Re-run with --all to install everything non-interactively."
