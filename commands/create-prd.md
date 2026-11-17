---
name: create-prd
description: Interview me, then write a build-ready PRD with a live interactive tracker and a Ralph build loop
arguments: output_file
---

# Create PRD

Output file: `$ARGUMENTS` (default: `PRD.md`).

Use the `prd` skill (`${CLAUDE_PLUGIN_ROOT}/skills/prd/SKILL.md`) in Mode A, start to finish:

1. Intake gate, then the three-lens interview, 1–2 questions per turn. Skip anything the conversation already answers.
2. Concept brief. Wait for explicit confirmation.
3. Full PRD from `references/TEMPLATE.md`, with section 12 as a work-unit DAG.
4. Quality gate from `references/review-checklist.md`.
5. Build the tracker, and tell the user how to run it live.
6. Offer the build handoff: a `CLAUDE.md` snippet and `/prd-loop` to start the Ralph build loop.

If the user already has a PRD, switch to Mode B (review) or Mode C (merge update) instead.
