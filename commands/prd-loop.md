---
name: prd-loop
description: Turn PRD.md's work units into a ready-to-paste Ralph loop command that builds the product unit by unit and ticks the live tracker as it goes
arguments: prd_file
---

# PRD Loop

PRD file: `$ARGUMENTS` (default: `PRD.md`).

Follow `${CLAUDE_PLUGIN_ROOT}/skills/prd/references/ralph-loop.md` exactly:

1. Read the PRD and check the preconditions. If section 12 is not a work-unit DAG with `**Ux done**` boxes, offer to convert the existing plan into units first (section 12 format in `${CLAUDE_PLUGIN_ROOT}/skills/prd/references/TEMPLATE.md`). Write the conversion into the PRD, and mark it `[UPDATED]`.
2. Find the project's test command (package.json scripts, Makefile, pyproject, CLAUDE.md). If none, use `[TBD]` and ask.
3. Check which loop command is installed (`/ralph-loop:ralph-loop` or `/ralph-wiggum:ralph-loop`). If neither is, tell the user to run `claude plugin install ralph-loop@claude-plugins-official` in a terminal.
4. Fill the loop prompt template and print both formats: human-readable, then the one-line copy-paste command.
5. Save both to `docs/00_prompts/`.
6. Give the run order: start `serve_tracker.py`, paste the command, watch the tracker.
