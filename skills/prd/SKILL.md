---
name: prd
description: Interview the user and write a build-ready Product Requirements Document (PRD) plus an interactive HTML tracker to follow during the build. Also reviews or updates existing PRDs. Use whenever the user mentions a PRD, product requirements, a spec, "I want to build an app/tool/feature", "help me structure my idea", or asks to check or extend an existing requirements doc — even if the description is short.
---

# PRD Skill

Turn a product idea into a PRD that a coding agent (Claude Code) can build from without guessing, then ship it as an interactive tracker the user follows phase by phase.

**Principles**
- Validate direction before details. A wrong direction makes every detail waste.
- Look through three lenses every time: **user need → business viability → technical feasibility**.
- Fill the blind spots non-PMs miss: edge cases, states, data specs, copy tone, acceptance criteria.
- Never invent facts. Unknown = `[TBD]`. Guess = `[ASSUMPTION]` with the reason.
- Diagrams and tables beat prose: Mermaid flows, state tables, feature trees, ASCII wireframes.
- The PRD has two readers: the builder (agent/dev, needs precise specs) and the end user (needs good product copy). Keep their language separate.

## Pick the mode

| Situation | Mode |
|-----------|------|
| Idea, no doc yet | **A — Interview → Concept → Full PRD → Tracker** |
| Has a doc, wants it checked | **B — Review** (see `references/review-checklist.md`) |
| Has a doc, wants to add or change things | **C — Merge update** (see `references/review-checklist.md`) |

If the conversation already contains a lot of context (a planning chat, a brain dump), extract it first and only ask about what is still missing.

---

## Mode A

### Step 0 — Intake gate
Ask once: *"In one or two sentences: whose problem are you solving, and roughly how?"*
- Clear "who + problem + approach" → Step 1.
- Vague but directional ("an app to help people budget") → ask 1–2 sharpening questions, then Step 1.
- No direction ("build me an app, you pick") → say this skill structures an idea; suggest they first decide whose problem they want to solve. Offer to brainstorm instead.

### Step 1 — Three-lens interview
Ask **1–2 questions per turn**, conversationally. In Claude Code, prefer the AskUserQuestion tool with concrete options (put your recommendation first). Stop each lens once the answer is basically clear — not perfect.

1. **User lens — is the need real?** How do target users solve this today? What is worse about that? Have you talked to real users; how do they describe the pain?
2. **Business lens — is it worth doing?** How does it make money or create value (subscription, ads, lead magnet, internal cost saving, personal use)? Who are the alternatives and what is the key difference? Rough audience size?
3. **Build lens — can it be built?** Which core capability exists vs. depends on third parties? What feels hardest? Which features are must-haves for an MVP? Preferred stack, hosting, budget, deadline?
4. **Product form.** Web app, mobile web/PWA, native app, chat/mini-program, CLI, or plugin/skill/extension. If the user already named one, confirm it was a real choice. If not, recommend one with reasons: where the users are, device needs (camera/GPS/offline/push), usage frequency, team cost and speed. When unsure, recommend the form that validates demand fastest. A phased strategy ("web first, native later") is fine — say so.

If a lens is blank (e.g. no business logic at all), point it out and think it through with them; do not skip it. Finish by restating the direction in 3–4 sentences and getting a yes.

### Step 2 — Concept brief (version 1)
Purpose: align on direction only. Keep it short. Output exactly:

```markdown
# <Product name> (working title)

## Positioning
> A <product form> for <target user> that helps them <solve problem>.
> Unlike <current alternative>, it <key difference>.

## Product form
- **Choice:** … **Why:** … **Phasing:** … (if any)

## Target users
- 1–2 personas, their core pain, why they would switch

## Value
- User value · Business value / monetization

## Core feature directions (no details yet)
- …

## Non-goals
- … (and why)

## Open questions
- …
```

Then ask: *"Does this match what you have in mind — positioning, users, direction? Once you confirm, I'll write the full PRD."* Revise until the user **explicitly** confirms. "Close enough" is not a confirmation; ask what is off.

### Step 3 — Full PRD (version 2)
Only after explicit confirmation. Read `references/TEMPLATE.md` and follow it section by section. `references/EXAMPLE.md` shows the expected depth. Rules:
- Reuse the concept brief; do not re-ask what is answered.
- Every P0 feature gets its own spec section: user stories, Given/When/Then acceptance criteria as checkboxes, edge-case table, states, data fields, copy.
- Section 12 is a DAG of work units (ralphinho RFC pipeline): each unit has `depends_on`, tier, risk, rollback, a Scope, acceptance-test checkboxes, and a final `**Ux done**` box. Each unit fits one agent session or one loop iteration.
- Keep the exact markers `[TBD]` and `[ASSUMPTION]` — the tracker counts them.
- Write to `PRD.md` in the project root unless the user named a path.

### Step 4 — Quality gate
Before showing the user, run the checklist in `references/review-checklist.md` against your own draft and fix every ❌. Then report: file path, 3-line summary, assumptions made, open `[TBD]` count.

### Step 5 — Live tracker
The artifact the user follows during the build. It ticks itself: when the build agent changes `- [ ]` to `- [x]` in `PRD.md`, the page updates within 2 seconds.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/prd/scripts/serve_tracker.py" PRD.md --open
```

It serves a page at `http://127.0.0.1:4747/` with:
- a table of contents showing progress for each section and unit
- build and acceptance progress bars
- rendered Mermaid diagrams, including the unit DAG
- a panel listing every `[TBD]` and `[ASSUMPTION]`

Clicking a box in the page writes it back to `PRD.md`. Tell the user to run it in its own terminal; don't block the session on it.

For a static copy to share (no live updates; clicks are saved in that browser only), use:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/prd/scripts/build_viewer.py" PRD.md PRD.html
```

On claude.ai or Claude Desktop without a shell, create an HTML artifact from `assets/prd-viewer.html` instead. Replace `{{PRD_TITLE}}` and `{{PRD_MARKDOWN}}`, and escape any `</script` as `<\/script`.

### Step 6 — Build handoff and loop
1. Offer to append section 15 (Build Handoff) to the project's `CLAUDE.md`, so every Claude Code session starts with the rules.
2. Offer `/prd-loop`. It follows `references/ralph-loop.md` to turn section 12 into a Ralph loop command in the `/ralph-wiggum-helper:create-prompt` format. Each iteration picks the next unblocked unit, builds and verifies it, ticks its boxes in `PRD.md` (the live tracker updates), commits, and logs a row in section 16. The loop ends with `<promise>PRD_COMPLETE</promise>` once every unit is done.
3. For one big unit or a quick manual run, the same rules apply without the loop: one unit at a time, tick only after verifying, log each unit.

---

## Always
- One or two questions per turn. Never dump a questionnaire.
- `[TBD]` over invention. `[ASSUMPTION]` with a reason over silent guessing.
- Merge, don't overwrite, when updating. Mark changes with `[UPDATED]`.
- Match the user's language for the conversation and the document.
