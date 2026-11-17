---
name: review-prd
description: Score an existing PRD against the build-ready checklist and fix or extend it
arguments: prd_file
---

# Review PRD

PRD file: `$ARGUMENTS` (default: `PRD.md`).

Use the `prd` skill (`${CLAUDE_PLUGIN_ROOT}/skills/prd/SKILL.md`):
- The user wants it checked: run Mode B with `references/review-checklist.md`. Give a score out of 10, list every ❌ and ⚠️ with a fix, and offer to fill the gaps.
- The user wants to add or change requirements: run Mode C. Merge the changes without deleting anything, mark them `[UPDATED]`, and surface conflicts for the user to decide.

Afterwards, rebuild the tracker. If section 12 changed, remind the user that `/prd-loop` picks up the new units.
