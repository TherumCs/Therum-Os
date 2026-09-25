---
name: drive-is-the-record
description: HARD RULE (2026-09-25) — the TSC-BETA Drive folder is the only record; auto-memory must be mirrored to _core/knowledge and _core/memory.md updated at every loop close
metadata:
  type: feedback
---

Bam, 2026-09-25: **"bro is all this work added to the mds on fucking drive?"** → it was not. For ten days the deep notes went only to `~/.claude/projects/…/memory/` on the Mac, `_core/memory.md` had no loop entries after 09-19, FAILURES.md and the case-study folder sat uncommitted, and the product CHANGELOG had nothing since beta.10. **"so you just be saying shit."**

**Why:** CLAUDE.md's closed-world law says the Drive folder is the ONLY source of truth. Notes he cannot open from the folder do not exist to him, and telling him something is "recorded" when it is not is the exact over-claim [[anticapitalist-script]] forbids.

**How to apply, every loop close, in this order:**
1. Write the durable finding to the auto-memory file as usual.
2. Run `bash "_core/tools/sync-knowledge.sh"` from the TSC-BETA folder → mirrors all memory files to `_core/knowledge/` (index `_core/knowledge/MEMORY.md`).
3. Append the loop entry to `_core/memory.md` (what changed, decisions, blockers, status).
4. Failures → `_core/FAILURES.md`. Product changes → `CHANGELOG.md` in the product repo under "Unreleased".
5. `git add -A && git commit && git push` in BOTH repos. Zero uncommitted files is the exit check.

Also 2026-09-25: `/Users/bam/Local Sites/therum-os/therum-cms-2` had vanished from the Mac; GitHub main was intact (`d784d89`), re-cloned to the same path. Verify the path exists before assuming the build tree is there.

See [[bam-working-style]] [[product-vs-instance]] [[github-access]].
