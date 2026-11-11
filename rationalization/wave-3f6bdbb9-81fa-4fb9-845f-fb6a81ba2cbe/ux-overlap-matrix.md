# UX Overlap Matrix — Wave `3f6bdbb9-81fa-4fb9-845f-fb6a81ba2cbe`

**Generated:** 2026-10-05 · **Methodology:** 1.0.0 · **Profile:** `faa`
**Result:** no cross-application UX overlap measurable — **minimum-input guard TRIPPED**

---

## Executive summary

This wave contains **exactly one application**: the Student Management System (VB.NET),
`c70846ac-0948-4953-990c-c68a2be292d9`. UX overlap is a **pairwise** measure — it asks
whether the same kind of user must move between *different* applications to finish one
piece of work. With one application there are **zero pairs**, so there is nothing to
compare.

Every analysis array in the JSON is therefore empty, and the application is named in
`coverage_exclusions[]` with its reason so the wave coverage check sees it as
**accounted for, not dropped**.

> **Read the empty result correctly.** It means *"one application, nothing to compare"* —
> **not** *"several applications compared and found unrelated."* Those two readings
> support opposite consolidation conclusions. `avg_ux_overlap_pct` is **omitted**
> rather than reported as `0` for exactly this reason: a literal zero would read
> downstream as a measured finding about apps that were actually compared.

| Signal | Value |
|---|---|
| Wave applications | 1 |
| Apps with `ux-accessibility.json` | 1 (threshold: 2) |
| App pairs available to score | **0** |
| Normalized personas | 0 |
| Swivel-chair patterns | 0 |
| Fragmented journeys | 0 |
| `avg_ux_overlap_pct` | omitted — not computable |
| Headless archetypes excluded | 0 |

## Persona / task matrix

**Empty.** Persona normalization across a set of one application is not a normalization.

For the reviewer's context, Discovery found **one** undifferentiated user type in the
single application — *Student-Records Operator* (`local-workstation-operator`) — with no
login, no role model and no permission checks anywhere in source. It is deliberately
**not** promoted into `personas[]`; Discovery's own artifact remains the citable source.

## Swivel-chair hotspots

**None found — and none were available to find.**

All four human-facing screens (dashboard, insert, edit, view) live inside **one
executable**, reparented into a single navigation shell (`Form1.Panel5`). A user
completing a task never leaves the application and never re-authenticates. There is no
app-to-app jump that could constitute a swivel-chair.

Two routes to reaching the two-app threshold were available and **both were rejected as
dishonest**: counting the four internal WinForms screens as separate applications, and
counting the Insert → View → Edit flow as a cross-application journey. Neither is an
application boundary. Reporting ordinary in-application navigation as a swivel-chair
would have manufactured consolidation evidence.

## Fragmented journeys

**None.** Same reason: a fragmented journey requires a journey crossing ≥ 2 applications.

## Severity-ranked findings

No overlap findings — zero pairs means zero findings. No `blocker`, `major` or `minor`
severity was assigned, because no finding existed to assign one to. (Severity thresholds
were not exercised; no severity was assigned by judgment.)

### Context that is *not* a UX-overlap finding

Discovery's accessibility assessment of the single application returned
**`gate_decision: FAIL`** — 1 critical, 2 serious, 4 moderate, 2 minor — driven by
**A11Y-001**: none of the application's 137 controls carries an `AccessibleName`, so a
non-visual user has no mechanism to operate it. **This finding is real and
consequential.** It is a single-application finding and so has no home in a cross-app
overlap matrix; it is already recorded in
`discovery/c70846ac-.../ux-accessibility.json` and should be actioned from there.

## Limitations

- **`redundancy-matrix.json` not staged as an input.** Cross-app redundancy runs at the
  *same* wave sequence as this skill, not ahead of it, so no structural overlap was
  available to cross-reference. Immaterial: with zero pairs there was nothing to annotate
  `structurally_redundant`. No structural figure was estimated or carried over.
  **Corroborated anyway:** the peer cross-app-redundancy run output (read from disk, not
  relied on as an input) independently reports `applications_analyzed: 1` with zero pairs
  and empty overlap arrays — two skills converging on *scope of one* from different
  evidence bases, which argues this is the wave's real shape rather than a staging failure.
- **No `profiles/faa/personas.yaml` staged**, so the optional canonical persona registry
  could not be consulted. Immaterial for the same reason.
- **Sequential execution.** Per the skill's *When NOT to fan out* rule, a guard-trip wave
  exits early; per-persona sub-agents cannot detect a cross-app pattern that does not exist.

## Carried-forward caveat (unresolved, not a UX finding)

Discovery's catalog, structural-analysis, identity-landscape and ux-accessibility passes
each **independently** flag that this application's content — a student-records desktop
tool — bears no relation to the FAA profile's aviation/NAS domain. Those artifacts
affirm `faa` as the governing profile while questioning the application's fit for the
engagement; **none asserts a competing profile.** Carried forward for the engagement
owner as a wave-composition question. It did not influence any value in this artifact.

## Reviewer ask

| Ask | Action | Subject |
|---|---|---|
| `ux-overlap-inventory` | `aware` | wave `3f6bdbb9-81fa-4fb9-845f-fb6a81ba2cbe` |

No decision, waiver or investigation is requested. **If this wave is later expanded to
include a second user-facing application, re-run this analysis — the result would change.**
