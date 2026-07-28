# skills.md — Base Skills
TSC-BETA · addons/base · universal skills · load ON DEMAND.
Scope: UNIVERSAL — method / format / system level only. Apply any tool regardless of topic.
Topic-specific skills not here; go in tool's addon (addons/tsc). This base stay domain-agnostic.

## Methodology (pick by project size)
| Skill | What it does | Use when |
|---|---|---|
| Superpowers | clarify → design → plan → code → verify; brainstorming, writing-plans, TDD, systematic-debugging, subagent review. Also non-coding (e.g. presentations). Enable: `/plugin install superpowers@claude-plugins-official` (or community: `/plugin marketplace add obra/superpowers-marketplace` → `/plugin install superpowers@superpowers-marketplace`) | Small–medium, well-defined work. Faster, more efficient. |
| GSD (Get-Shit-Done) | Slower, methodical, heavy safety checks; install locally to project folder, map existing codebase to start mid-flight. | Large, complex, iterative builds where thoroughness beat speed. |

## Session & workflow
| Skill | What it does | Use when |
|---|---|---|
| /close | End-of-session routine: scan session for decisions + open tasks, update memory files, handle commits, write session log — so context not rebuilt from scratch next time. | Run at end of every working session. |
| QA Session (qa) | Conversational issue intake: user report problems own words; you clarify lightly (2–3 questions max), gather domain context in background, file durable user-focused GitHub issues — break big reports into thin, independently-fixable, dependency-ordered slices for parallel work. Behavior-focused, no file/line refs that go stale. (mattpocock) | Reporting bugs / filing issues conversationally. |

## Build the system
| Skill | What it does |
|---|---|
| skill-creator | Create, improve, measure skills |
| mcp-builder | Build MCP servers |
| Task Observer (meta-skill) | Run alongside your work, watch three things: corrections you make, gaps no skill covers (→ drafts new skills), own blind spots. Write per-session observation log of suggested skill updates for you to review — never edit skills directly. Cross-cutting patterns go to shared principles file that new skills checked against. Domain-agnostic (rebelytics, CC BY 4.0). |

## Code quality
| Skill | What it does |
|---|---|
| slop (agent-slop-lint) | Language-agnostic code-quality linter for agentic era: flags structural rot — cyclomatic/cognitive complexity, hotspots (complex + churned), package instability, dependency cycles, class coupling, inheritance depth. One config, exit 0/1. Deterministic gate on agent-written code. Python/JS/TS/Go/Rust/Java. (JordanGunn, Apache-2.0) Enable: `pip install agent-slop-lint` |

## Memory (persistence)
| Skill | What it does | Use when |
|---|---|---|
| LogseqBrain | Graph-backed persistent memory: brain-save / brain-load / brain-status store project context, decisions, progress across sessions AND devices (syncs via Logseq). Complements local memory.md. (jame581, MIT) | Cross-session / cross-device memory that travels between machines. |
| skill-everything | Git-versioned self-learning memory: accepted mistakes become reviewed, schema-validated skills (learn(errors) PRs, CODEOWNERS-gated). Router + selective sub-skill loading keep per-message tokens flat (~84% less than monolith). Cross-runtime, plain Markdown. (sordi-ai, MIT — github.com/sordi-ai/skill-everything) Enable: `npx agent-skills-cli add sordi-ai/skill-everything` (or clone → copy to ~/.claude/skills/) | Self-extending memory where quality compound and mistakes not repeat. |
| cavemem | Persistent semantic memory (hybrid BM25 + local vectors): memory_search / memory_save, relevant recall auto-injected each turn; consolidate observations into facts. Bundled with caveman-code (installing caveman-code covers it). (JuliusBrussee, MIT) | Semantic recall auto-injected per turn. |

## Orchestration
| Skill | What it does |
|---|---|
| Swarm | Launch per-task agent team (lead + Socratic facilitator + specialists); they research, argue, self-score. Work reach you only at 9/10 bar; facilitator — not doer — control the gate. Governance override conflicting ambient config. (DheerG — github.com/DheerG/swarms; install per repo, vet first) |
| PraxisKit | Five governed skills chaining intent → shipped: seed-to-idea → idea-to-prd → prd-to-kanban → kanban-to-agents → build-to-review. Handoffs via artifacts (idea.md, PRD.md, kanban.md, SUBAGENT.md), not chat. Dependency-ordered parallel board. (xmu-csnoob, MIT — github.com/xmu-csnoob/PraxisKit) |
| LLM Council | For hard question, ask several models independently, have them cross-rank each other anonymized, chairman model compile final answer. (karpathy) |
| effortmining | Right-size reasoning effort per subagent: classify each subtask, dispatch cheapest effort tier a blind grader still accept (miner-low..max). −64.7% output tokens at equal pass rate; SessionStart policy + self-refit. (nagisanzenin, MIT) Enable: `claude plugin marketplace add nagisanzenin/effortmining` then `claude plugin install effortmining@effortmining` |

## Read any input
| Skill | What it does |
|---|---|
| file-reading | Route + read any uploaded file type |
| pdf-reading | Extract and inspect PDF content |

## Produce standard outputs
| Skill | What it does |
|---|---|
| docx | Word documents |
| pptx | PowerPoint decks |
| xlsx | Spreadsheets — formulas, charts, cleanup |
| pdf | Create, fill, merge, split PDFs |

## Output quality
| Skill | What it does |
|---|---|
| humanizer | Strip AI writing patterns from generated text — buzzwords, hedging, filler, fake enthusiasm. Editing-pass form of claude.md's banned-language rules. |

## Thinking (author from _core/skill-template.md)
| Skill | What it does |
|---|---|
| deep-research | Real research pass: fan out searches to LOCATE sources, then PULL each real page/file with clean extractor (Firecrawl/crawl4ai/markitdown — base/mcp.md), separate verified facts from claims, cited summary. Never answer from search snippets. |
| source-auditor | Split claim/article into supported facts, speculation, useful frameworks, likely-wrong. |
| devils-advocate | Pressure-test a plan: strongest case against, who push back hardest, the assumption that sink it if false. |
| decision-architect | Turn fork into a call: 1-yr gain, 5-yr regret, hidden costs, who you want to become → recommendation + the fact that would change it. |
| doc-to-action | Long doc → 5-line summary + concrete next actions + the one thing to do in 24h. |

## Personal OS (author from _core/skill-template.md)
| Skill | What it does |
|---|---|
| weekly-review | End-of-week: what got done, what you avoided + why, energy in/out → 5-line summary + one focus next week. |
| brain-dump-sorter | Unfiltered dump → real priorities vs anxieties-as-priorities vs let-go vs park + the one 24h action. |

## Platform
| Skill | What it does |
|---|---|
| product-self-knowledge | Accurate, current Anthropic product facts |