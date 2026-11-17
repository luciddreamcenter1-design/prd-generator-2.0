# PRD Generator 2.0

A Claude Code plugin that takes you from idea → interview → build-ready PRD → autonomous build loop, with a live tracker that ticks itself as the agent ships each piece.

```
/create-prd          interview → concept brief → full PRD → quality gate
serve_tracker.py     live tracker: boxes tick as PRD.md changes
/prd-loop            Ralph loop that builds one work unit per iteration
/review-prd          score / fix / extend an existing PRD
```

## How it works

1. **Interview, not guesswork.** Three lenses (user need, business, build) plus product-form choice, 1–2 questions at a time. A short concept brief must be explicitly approved before details get written.
2. **Build-ready PRD.** 16 sections: personas, metrics, a feature tree, Mermaid flows, an ASCII wireframe, and per-feature Given/When/Then criteria, edge-case tables, states, data, and copy. It also covers the data model, stack, API, NFRs, risks, and a `CLAUDE.md` handoff. Unknowns stay `[TBD]` and guesses are marked `[ASSUMPTION]`.
3. **Work units, not phases.** Section 12 is a dependency graph of units in the ralphinho RFC style. Each unit has `depends_on`, a tier, risk, rollback, a scope, acceptance-test checkboxes, and a final `**Ux done**` box.
4. **Live tracker.** `serve_tracker.py` serves an interactive page. When the agent changes `- [ ]` to `- [x]` in `PRD.md`, the page updates within 2 seconds. It shows:
   - a contents panel with progress for each section and unit
   - build and acceptance progress bars
   - Mermaid diagrams
   - every `[TBD]` and `[ASSUMPTION]`
   
   Clicking a box writes it back to `PRD.md`.
5. **Ralph build loop.** `/prd-loop` generates a `/ralph-loop:ralph-loop` command in the `/ralph-wiggum-helper:create-prompt` format. Each iteration:
   - picks the next unblocked unit
   - builds and verifies it, ticking boxes as it goes
   - commits and logs a row in section 16
   
   Stalled units are split into smaller ones, and blocked units are skipped with a logged question. The loop ends with `<promise>PRD_COMPLETE</promise>`.

## Install

```bash
git clone https://github.com/luciddreamcenter1-design/prd-generator-2.0 ~/.claude/plugins/prd-generator
```

Enable it in Claude Code. For the loop, also install the official Ralph loop plugin:

```bash
claude plugin install ralph-loop@claude-plugins-official
```

## Run the tracker

```bash
python3 ~/.claude/plugins/prd-generator/skills/prd/scripts/serve_tracker.py PRD.md --open
```

Python 3 stdlib only. It binds to `127.0.0.1:4747` (`--port` to change) and only accepts writes from its own page. For a static, shareable copy (no live updates):

```bash
python3 ~/.claude/plugins/prd-generator/skills/prd/scripts/build_viewer.py PRD.md PRD.html
```

## Layout

```
.claude-plugin/plugin.json
commands/            create-prd, review-prd, prd-loop
skills/prd/
  SKILL.md           the workflow
  references/        TEMPLATE, EXAMPLE, review-checklist, ralph-loop
  assets/            prd-viewer.html (tracker UI)
  scripts/           serve_tracker.py (live), build_viewer.py (static)
```

## Credits

- [dredozubov/prd-generator](https://github.com/dredozubov/prd-generator): the original plugin and section structure.
- [chituai/prd-writer](https://github.com/chituai/prd-writer): the three-lens diagnosis, the two-draft flow, the review and merge modes, and the edge-case and data-spec discipline.
- [ChatPRD — PRDs for Claude Code](https://www.chatprd.ai/learn/PRD-for-Claude-Code): the PRD as a persistent context file for coding agents.
- The ralphinho RFC pipeline and ralph-wiggum-helper: the work-unit DAG and the loop prompt format.

## License

MIT
