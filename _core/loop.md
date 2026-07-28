# loop.md — The Loop
TSC-BETA
Scope: UNIVERSAL — portable engine. Same in every project.

## What this is
Task loop under human oversight. Each iteration = ONE task, run against spec,
with fresh read of rules + context + state so context rot never accumulate.

User own oversight loop: set goal, allocate work, cull what wrong,
call "done." Everything below goal, agent run.

## The cycle (one iteration)
1. READ    — _core/claude.md (rules), context.md (user + project), _core/memory.md (state), then DROP ZONE spec below.
2. PLAN    — restate task in one line + exit signal that end it.
3. ACT     — do one task. Surgical. Read files before edit.
4. VERIFY  — prove it: re-read / run / inspect. No proof, not done.
5. WRITE   — update memory.md: changed, decided, blocked, done/next.
6. REPORT  — one line: what shipped + whether exit signal met.

## Exit signal (name it every run)
Loop end when spec satisfied and check pass — not when agent
decide done. If no signal named in DROP ZONE, default:
"The user says 'done' or 'move on.'"

## Human checkpoints (oversight loop = the user)
- Goal / spec: user write it.
- Done-ness: user judge it.
- Autonomy dial: default = one task, verify, stop. User turn up per run.

## Rules of the loop
- One task per iteration. Fresh read every iteration.
- Re-feed full spec each run; no lean on prior-turn memory.
- Edit in place; never rebuild from scratch.
- Flag extra issues in memory.md; no fix them unasked.
- Finished work graduate: turn completed goal into check that get re-verified, so nothing rot silently. Running unattended? Load _core/autonomy.md.

---

## DROP ZONE — current spec
<!-- Drop the task here. Include the exit signal. -->

(empty)