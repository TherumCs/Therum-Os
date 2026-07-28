---
name: <skill-name>
description: Use when <situation>. Triggers on "<phrase>", "<phrase>", "<phrase>".
---
# What this does
<one line — what skill produce>

## When to use
<situations that fire this; mirror trigger phrases above>

## Instructions
1. <step>
2. <step>
3. <step>

## Output
<exact format — e.g. "plain text, ready paste, no preamble">

<!--
Placement:
  personal (every project): ~/.claude/skills/<skill-name>/SKILL.md
  project (travels w/ repo): .claude/skills/<skill-name>/SKILL.md
Path must be exact. After add, restart, run /skills confirm loaded.
Description IS trigger — write phrases precise or no fire.
Keep body small: action directives, not prose (~3k-token ceiling).
-->