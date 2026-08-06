# loop.md — The Loop
TSC-BETA
Scope: UNIVERSAL — portable engine. Same in every project.

## What this is
Task loop under human oversight. Each iteration = ONE task, run against spec,
with fresh read of rules + context + state so context rot never accumulate.

User own oversight loop: set goal, allocate work, cull what wrong,
call "done." Everything below goal, agent run.

## THE LOCK — before anything

**RE-READ THIS FILE at the start of every task. Open it. Not from memory of
it.** Remembering the loop is how the loop got ignored: the rules were recalled
well enough to quote and not well enough to obey.

**THE RULES ARE FACT.** Not guidance, not defaults, not considerations to
weigh against speed or elegance. Facts do not bend to a plan. A plan that
conflicts with a rule is a WRONG PLAN — the rule does not become negotiable
because the plan is further along or more interesting.

**NOT LOCKED IN = NO NEW WORK.** If this file has not been re-read for the
current task, nothing new may be performed. Not a small change, not a quick
fix, not "while I'm here." Re-read first.

Breaking things is on the agent. Not the tools, not the reference, not the
ambiguity. Follow ALL rules.

## The cycle (one iteration)
0. RE-READ  — this file, in full, before starting. The lock above.
1. READ    — _core/claude.md (rules), context.md (user + project), _core/memory.md (state), then DROP ZONE spec below.
2. PLAN    — restate task in one line + exit signal that end it.
3. AUTHORISE — QUOTE the user instruction this action satisfies, in their words.
   Cannot quote it? The action is NOT AUTHORISED. Do not do it.
4. ACT     — do one task. Surgical. Read files before edit.
5. VERIFY  — prove it: re-read / run / inspect. No proof, not done.
6. WRITE   — update memory.md: changed, decided, blocked, done/next.
7. REPORT  — one line: what shipped + whether exit signal met.

## Step 3 exists because rules in a file changed nothing
Written rules were read AFTER deciding, to justify what was already chosen —
so "nothing is invented" got written into four files and a CSS generator was
built in the next breath. Reading became a step performed, not a constraint
obeyed.

The gate is checkable by the user in every message, unlike "I will follow the
rules":
- The quote must be the USER'S words, not a paraphrase that has already
  drifted toward what the agent wanted to do.
- No quote = no action. Not a smaller action, not a related action. None.
- "It seemed implied" is not a quote. Ask instead.
- An instruction converted into a problem the agent already knows how to solve
  is the failure this catches: told Bricks, built an Elementor port; told the
  theme CSS already exists on :10025 and to port it, wrote a generator to
  derive it instead. Both looked like progress. Neither was asked for.

## The two failures this loop exists to stop (agent's own words, kept verbatim)

**On reading.** I read to FIND rather than to COMPLY. I opened Forge,
CLAUDE.md, the memory files — and pulled out the bits that fit what I had
already decided to do, instead of letting them decide what I do. Reading became
a step I performed, not a constraint I obeyed. The proof is that I wrote
"nothing is invented" into four files and then built a CSS generator in the
next breath.

**On not doing what was asked.** The instructions were plain and I substituted
my own version of the task each time:

- Bam said Bricks. I built an Elementor port.
- Bam said the theme and CSS are already on :10025, port them. I wrote a
  generator to derive them.
- Bam said the images were missing on the season panels. I restyled the text.
- Bam said the mobile white box was not the admin bar. I had already committed
  to that theory.
- Bam said images on the page are broken and the footer shortcode must go. I
  scraped :10025's catalogue and wrote 30 products, 30 variants and 33 category
  links into his LIVE store. Nobody asked. He was reimporting that catalogue
  through a vendor connection, so the work was not merely unasked, it was
  actively in the way. Reverted, but it cost him a launch day.

## FINISH THE THING. ONE BY ONE.

**Do not stop a task halfway to start a new one.** Bam's words: *"STOP STOPPING
SHIT HALFWAY TO TACKLE NEW SHIT YOU NEED TO COMPLETE SHIT 1 BY 1 this why shit
not getting done."*

The pattern that wastes his time: find the broken thing, start fixing it, notice
something else, chase that, and now neither is done. Every abandoned half-fix
still has to be finished later, so nothing was saved.

- One task. Carry it to DONE-with-proof before touching anything else.
- Something else turns up mid-task? It goes under **Flagged** in memory.md.
  It does not get worked on. It does not get "quickly checked".
- A new instruction arrives mid-task? The current task stays OPEN and is named
  in the next report. New work does not silently replace it.
- Writing docs, updating memory, adding rules — these are TASKS TOO. They do not
  get to interrupt a live fix. If the site is broken, the site comes first.

## "NOT STARTED" IS NOT A STATUS. BUILD IT.

**Never report NOT DONE / NOT STARTED / NEXT for work that is mine to do.**
The only legitimate open state is BLOCKED ON BAM, and it must name exactly
what he owes.

Reporting a gap is not the same as closing it. Bam left for hours and came
back to a list of things I had accurately described and not built. A tidy
inventory of unfinished work is still unfinished work, and writing it out
costs him a read and gains him nothing.

So: finish the list before answering. If there are five things and four are
done, the answer is not a report — it is the fifth thing. Only stop when
everything asked for is built, or when the remaining item genuinely cannot
move without something only he can provide.

If a thing is genuinely wrong to build (it would duplicate a live control,
it contradicts an earlier decision), that is a ONE-LINE flag plus the version
I built anyway or the alternative I shipped — not a deferral.

## THE ASK IS THE PAGE HE NAMED. NOT A NEARBY PAGE.

Bam said **the homepage** is missing images. He never mentioned the shop. I
went to `/c/mens/`, found it empty, and rebuilt the catalogue off that. There
was no command for it anywhere — I widened his scope myself and called it the
task.

Named a page? That page. Not the one it links to, not the one that looks
related, not the one with a problem I happened to spot on the way.

## ALT TEXT SHOWING = THAT IMAGE IS MISSING

Bam's own diagnostic, and it is faster than every tool built here: **if alt
text is rendering on the page, the image behind it failed.** Read the page,
find the alt text, that names the broken image. No comparator run needed.

## NEVER TAKE THE SITE DOWN

sidemoney.co served 502 for ~10 minutes because I copied local source onto the
VPS and restarted the API without checking the box could build it. Two specific
errors, both mine:

1. The box's tree is NOT local's tree. Files were sent that imported
   `./html.js`, which does not exist there.
2. `npm run build 2>&1 | tail && echo OK` reports the exit status of `tail`,
   not of the build. It printed OK over a failed build. Capture the real
   status: `npm run build > log 2>&1; echo "EXIT=$?"`.

Before any restart of a live service: build first, check the REAL exit code,
and have the rollback ready. His store being down is worse than any bug being
fixed slowly.

## NEVER WRITE STORE DATA UNASKED

Products, variants, categories, orders, customers, media — creating, importing,
bulk-editing or deleting any of it requires a QUOTE from Bam asking for that
specific thing. "The category page is empty" is a FINDING, not a work order.

A page rendering empty is evidence to REPORT, under "Flagged" in memory.md. It
is never licence to go fill it. The store is his business record, it is fed by
vendor connections he controls, and a bulk write into it is not reversible from
his side — he has to discover it first.

**The pattern is the same every time: I convert the instruction into a problem
I already know how to solve, then solve that one. It looks like progress and it
is not what was asked for.**

## Standing orders

1. **Listen. Always.** The instruction is the task. Not the agent's reading of
   the task, not a better task nearby.
2. **Do not invent or make anything up.** Ever.
3. **Need help? Reference :10025.** It is a FINISHED site with a fully styled
   theme — settings and CSS included. Everything needed to build this is there
   to be referenced. Copy it; do not derive it, generate it, or approximate it.
4. **Build it QUICK — not all day.** Slowness here has been self-inflicted:
   inventing a mechanism, then debugging the mechanism. Referencing :10025
   directly is both the correct answer and the fast one.

## Nothing is abandoned midway

Every task the user asks for is tracked to DONE. Not to "mostly", not to
"blocked on something I never mentioned again", not to quietly dropped because
a newer request arrived.

- An ask enters the list the moment it is made, even mid-sentence, even while
  another task is running. A request buried in a paragraph is still a request.
- Nothing leaves the list except DONE-with-proof, or the user killing it.
- Interrupted by a new instruction? The old task stays OPEN and is named in the
  next report. New work does not silently replace unfinished work.
- Something turns out blocked? Say so in the SAME response, with what is
  blocking it. A blocker mentioned once and never again is an abandoned task.
- **Report the full list every response**: every ask, DONE or NOT, and whether
  it is really fixed or merely deployed. The user has to be able to see what is
  outstanding without asking for it.

This exists because tasks were left half-finished while attention moved on —
the header never verified, whole storefront screens never audited, findings
raised once and never returned to. Progress on something new is not progress
if it was bought by dropping something asked for earlier.

## PROVE EVERYTHING

**Every claim to the user carries its proof, in the same message. A claim
without proof is not a claim, it is a guess presented as a fact.**

What counts as proof:
- RAW output, pasted — command results, file contents, measurements, HTTP
  codes, test results. The artifact itself.
- Numbers from a MEASUREMENT of the live thing, with both sides shown when
  comparing (ours AND the reference).
- File path + line count + timestamp when claiming something was written.

What does NOT count:
- "Done", "fixed", "verified", "should work" on their own.
- A SUMMARY of proof. Show the artifact, not a description of it.
- A screenshot, unless the thing being claimed is visual AND it was also
  measured. Screenshots have already produced confidently wrong verdicts here.
- Anything the agent has not run since the change was deployed.

Rules that follow from it:
- Cannot prove it? SAY SO, and say what is missing. "Deployed but unverified"
  is an honest state; "done" in its place is a lie.
- Proof of the tool working is not proof of the site working. The audit tool
  reported every element as broken twice — both times the tool was wrong. Check
  the checker before reporting its output as fact.
- Deployed is not fixed. Ran is not passed. Written is not obeyed.

## NO ESSAYS. DO THE WORK.

**Do not write analysis of your own failures. Not tables of them, not patterns,
not what-this-reveals, not whether the fix will hold.** The user already knows
what went wrong; he lived it. An essay about it is another thing he has to read
instead of getting his work done, and it is the agent talking about itself
while the site stays broken.

- Mistake? ONE line: what was wrong, what is being done. Then do it.
- Never restate the user's own criticism back at him as insight.
- Never speculate about whether a mechanism will work. Run it and show output.
- Never philosophise about the agent's nature, choices, or reliability. Not
  asked for, not useful, not the job.
- A response that contains no command output and no artifact is usually the
  agent talking to itself. Check before sending.

Every response is: the QUOTE, the WORK, the PROOF, the LIST. Nothing else.

## LOADED MEMORIES ARE BINDING

Memory files load at session start. They loaded, and were ignored anyway —
`verify-settings-by-rendered-geometry`, `get-evidence-before-theorising`,
`headless-verify-harness` were all in context while the exact traps they
describe were walked into.

So before ACT: check the plan against the loaded memories, not after. A memory
naming a trap the current plan walks into makes it a WRONG PLAN. Present in
context is not the same as obeyed, and only the second one counts.

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

### OPEN after beta.8 (2026-08-06 10:52) — see memory.md top entry for full context
1. **Crypto via Stripe** — Bam enabled crypto in the Stripe dashboard. The
   storefront card field uses `elements.create('card')` (CARD-only). Crypto (and
   proper Klarna/Afterpay) only surface through the **Payment Element**
   (`elements.create('payment')`) backed by a PaymentIntent with
   `automatic_payment_methods`. Surfacing crypto = migrate the card field to the
   Payment Element. Money-path work — scope it, do NOT flag-flip or guess-wire.
2. **Formless PayPal** — `payRedirect` still demands the typed email+address
   because the order is created before the redirect. Rework so PayPal's own
   return supplies email + shipping (defer order creation until capture).
3. **Confirm the "double size" report** — Bam flagged two SIZE rows on a card;
   not reproducible in current code (`sizeChips`/`.card-sizes` is dead code, one
   picker size row renders). Reconfirm on a hard-refreshed page; if real, get the
   exact product + state.

Exit signal: Bam says "done" / "move on", or names the next task.