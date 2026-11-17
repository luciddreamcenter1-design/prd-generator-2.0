# Build Loop: PRD → ralphinho units → Ralph loop

The PRD's section 12 is already a ralphinho-style work-unit DAG. A Ralph loop feeds the **same prompt** back every iteration, so the prompt must not carry progress itself. Progress lives in `PRD.md` (checkboxes + section 16 log) and git history. The live tracker reads the same file, so every box the agent ticks shows up on its own.

## Preconditions (check before generating)
- `PRD.md` exists and section 12 has units with `**Ux done**` boxes.
- No `[TBD]` blocks a tier-3 unit (auth, schema, security). If one does, ask the user first.
- The project is a git repo (the loop commits per unit).

## Loop prompt template

Fill `<Product>`, `<test command>`, and `<N units>`. Keep everything else verbatim.

```
Build <Product> from PRD.md, one work unit per iteration.

Each iteration:
1. Read PRD.md section 12 (work units) and section 16 (execution log), and run git log --oneline -10, to see what is done.
2. Pick the unit to work on: a unit marked in progress in the log, otherwise the first unit whose **Ux done** box is unchecked and whose depends_on units are all done.
3. Take the unit through research, plan, implement, tests, review. Stay inside the unit's Scope.
4. Verify each acceptance test. Tick its box in PRD.md (change "- [ ]" to "- [x]") only after it is verified. Never tick a box you have not verified.
5. When every box in the unit is ticked and <test command> passes, tick **Ux done** and commit: "feat(Ux): <unit name>".
6. Append one row to the section 16 table: time, unit, result (done / in progress / stalled / blocked), short notes.
7. If the same unit fails verification in 3 iterations, log it as stalled, split it into smaller units (Ux.a, Ux.b) in section 12 with updated depends_on and graph, and continue.
8. Never resolve a [TBD] by guessing. Log the unit as blocked with the question and move to another unblocked unit. If no unblocked unit remains, stop and state exactly which answers are needed.

Instructions:
- Use command /feature-dev:feature-dev whenever useful
- Create general sub-agents when reading files, analysing files, creating code, running code, run tests, etc.
- Whenever you want to see results on monitor and find no other way: use command /screenshot in a general agent and get results back to work on them

Definition of Done:
- [ ] Every **Ux done** box in PRD.md section 12 is ticked
- [ ] Every box under "Final verification" is ticked
- [ ] <test command> passes on a clean checkout

When finished, say: <promise>PRD_COMPLETE</promise>
```

`--max-iterations`: about 3 × the number of units, minimum 15.

## Output (same two formats as /ralph-wiggum-helper:create-prompt)

1. **Human-readable** — the filled prompt between `════` rules.
2. **Copy-paste command** — one line. Every newline becomes a literal `\n`, blank lines `\n\n`, and `"` becomes `\"`:

```
<loop command> "<prompt with \n>" --max-iterations <N> --completion-promise PRD_COMPLETE
```

`<loop command>` defaults to `/ralph-loop:ralph-loop` (official plugin `ralph-loop@claude-plugins-official`). Use `/ralph-wiggum:ralph-loop` if that is the one installed.

Save both formats to `docs/00_prompts/prompt-prd-loop-YYYY-MM-DD--HH-MM-SS.md`, the folder create-prompt uses.

## Run order to give the user
1. Start the live tracker in its own terminal:
   `python3 "${CLAUDE_PLUGIN_ROOT}/skills/prd/scripts/serve_tracker.py" PRD.md --open`
2. Paste the copy-paste command into Claude Code.
3. Watch the tracker: boxes tick, the build progress bar fills, and the log grows as units land. Clicking a box in the tracker writes back to PRD.md, so you can un-tick a unit to make the loop redo it.
