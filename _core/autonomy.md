# autonomy.md — Autonomous Operation Layer
TSC-BETA · _core · load ON DEMAND when running unattended (not every loop).
Scope: UNIVERSAL — machinery for going supervised to self-running, minus stack-specific code.
Distilled from field-tested agentic-OS practice. Keep principles; wire implementation in tool's addon.

## Three principles (everything below follows from these)
1. Laws, not tips. Every rule has number, "never", or command that checks it. Soft rules get optimized away.
2. Nothing grades own homework. Planner, worker, verifier, gate = four different parties. Final gate deterministic. Fresh-context verifier (saw neither plan nor draft) beats self-critique.
3. Nothing that passed once goes unwatched. Finished work becomes re-verified invariant. Goal verified once = assumption with timestamp.

## done_when (define before starting)
- Every task gets machine-checkable done condition before work begins.
- "Done" = check passes. Nothing else counts — not maker's confidence, not "looks right".
- If script couldn't check it, not a done condition. Rewrite until it is.

## Autonomy contract (declare blast radius before running unattended)
- ACTS ALONE: reversible, low-risk work it may do without asking.
- QUEUES FOR ME: sensitive areas (auth, payments, migrations, anything below "trusted" tier, large diffs) — prepared, not shipped.
- WAKES ME: verification fails twice on one item; budget breached; secret requested; standing goal violated.

## Earned trust (autonomy per skill, not per run)
- Track pass/fail per skill. Grant autonomy by measured rate, not vibes.
- Tiers: watch (<10 runs or <90%) = draft only; queue = verified, waits for you; auto (20+ runs and ≥95%) = ships unattended.
- Demotion automatic and loud: skill dropping below bar loses autonomy immediately.

## Dispatch (right model for the job)
- Route by task type: decisions / plans / reviews → most capable model, read-only. Spec-complete implementation → cheaper model. Bulk reading → cheapest.
- Escalate one rung on miss, without asking. Never iterate on output from model you didn't choose.
- Architect/editor split: slower model plans, faster model executes — ~3–5× cheaper than one strong model doing both.

## Metabolism (cost is a design input)
- Cheap models do work; expensive model makes decisions and emits few tokens.
- Spend effort where loop branches (the decision), not on mechanical steps.
- Right-size reasoning effort per subtask, not per session: mechanical/extraction → lowest tier; diagnosis/hard reasoning → high; escalate genuinely hard instances. Maxing everything wastes ~7× for same answer. Caveat: too-low effort doesn't skim — it fabricates (invents plausible IDs), so route verification-sensitive work up.
- Cadence is cost decision: halving interval doubles floor. Compute bill before automating.

## Standing goals (finished → invariant)
- Goal met → write as predicate script can run, re-verify on schedule, forever.
- Detection separate from fix: sentinel finds violations; normal loop fixes them.
- Flaky predicate → quarantine and cheapen, never delete goal.

## Compost (failures become laws)
- Periodically read exhaust — failures, closed-unmerged work, demotions — propose at most 3 improvements: new law, skill fix, or missing standing goal. Propose only; user signs off.

## Graduated trust (don't skip levels)
- Report → Draft → Ship → Grow. Turn autonomy up only after prior level runs clean for set period. Each unlock earned, not assumed.

## Note
This universal architecture, not install. Full reference implementation (heartbeat loop, cron, trust/goal ledgers, isolated worktrees, deterministic gate) belongs in tool's addon, tuned to that tool's stack.