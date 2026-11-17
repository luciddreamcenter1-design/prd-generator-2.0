# Review Checklist (Mode B, Mode C, and the Step 4 quality gate)

Mark each item ✅ / ⚠️ / ❌.

## Direction
- [ ] Clear target user and core pain
- [ ] One-sentence positioning with a named alternative and difference
- [ ] Product form chosen, with reasons
- [ ] Business value or monetization (even if simple)
- [ ] Explicit non-goals
- [ ] All three lenses (user / business / build) have a basic answer
- [ ] Success metrics are numbers with a time window

## Structure
- [ ] User flow diagram with at least two failure branches
- [ ] Feature tree with P0/P1/P2 priorities
- [ ] ASCII wireframe of the key screen
- [ ] Every P0 feature has its own spec section
- [ ] Implementation phases are checkbox tasks with a validation step each

## Detail (where AI-written PRDs cut corners)
- [ ] Every P0 feature has Given/When/Then acceptance criteria
- [ ] Every interactive element lists its states (loading, error, disabled, empty)
- [ ] Edge cases covered: empty, overlong, offline, no permission, concurrency, destructive actions
- [ ] Data fields have type, required, default, constraints
- [ ] End-user copy is written and has a defined tone, separate from developer field notes
- [ ] Env vars and secrets handling are listed
- [ ] Unknowns are `[TBD]`, guesses are `[ASSUMPTION]` — nothing vague passed off as decided
- [ ] Feature tree, specs, flows, and phases agree with each other

## Mode B output
1. Score out of 10 plus a one-line verdict.
2. Every ❌ and ⚠️, grouped by layer, with the concrete fix.
3. Ask: "Want me to fill in the gaps directly, or would you rather revise first and have me re-check?"

## Mode C — merge update
1. Get the current doc (path or pasted).
2. Pin down exactly what is being added or changed.
3. Map the blast radius. A new feature usually touches: feature tree (4), flows (5), feature spec (7), data model (8), phases (12).
4. Merge into each affected section. Do not delete existing content. If old and new conflict, stop and show the conflict; the user decides.
5. Mark every changed spot with `[UPDATED]`.
6. Re-check: flows updated? New fields have edge cases and copy? Tree and specs still consistent? Then rebuild the tracker.
