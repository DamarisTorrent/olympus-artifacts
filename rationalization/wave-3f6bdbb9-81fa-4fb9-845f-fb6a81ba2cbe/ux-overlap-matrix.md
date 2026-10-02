# UX Overlap Matrix — Wave `3f6bdbb9-81fa-4fb9-845f-fb6a81ba2cbe`

**Generated:** 2026-10-02T20:03:14Z · **Methodology:** 1.0.0 · **Governing profile:** `faa`
**Verdict:** No cross-application UX overlap — single-application wave. Minimum-input guard tripped (Methodology Step 0).

---

## Executive summary

This wave contains **exactly one application**, so there are **zero application pairs** and
therefore no cross-application UX overlap to report. That is a *result*, not a skipped analysis:
persona sharing, swivel-chair traversal and journey fragmentation are all pairwise measures that
only exist between two or more applications.

| | |
|---|---|
| Wave applications | **1** |
| Apps with a `ux-accessibility.json` | **1** (threshold: 2) → **guard tripped** |
| Application pairs evaluated | **0** |
| Normalized cross-app personas | **0** |
| Swivel-chair patterns | **0** |
| Fragmented journeys | **0** |
| Average UX overlap | *omitted — undefined with zero pairs (not 0%)* |
| Declared coverage exclusions | **1** (the wave's only application) |

The one in-scope application:

| Application | Archetype | Domain | UX surfaces | Personas |
|---|---|---|---|---|
| Student Management System (VB.NET)<br>`c70846ac-0948-4953-990c-c68a2be292d9` | `desktop` (WinForms thick client) | Admin | 4 (dashboard, insert, edit, view) | 1 (`local-workstation-operator`) |

**Consequence for disposition.** This artifact supplies **no evidence either way** on consolidating
this application. A Consolidate case for it must rest on structural or operational analysis, or on a
future wave that places it alongside peer applications.

---

## Persona / task matrix

*Empty.* Persona normalization (Step 1) is the act of clustering persona names **across** applications;
a single app's persona catalog passes through unchanged, so no normalized persona was emitted.

For the reviewer's context, the one source persona found — not carried into `personas[]`:

| Source persona | App | Headcount | Basis |
|---|---|---|---|
| Student-Records Operator (sole user class — no role differentiation observed) | Student Management System | **Unknown** — no CMDB, org chart or telemetry | Inferred from total absence of auth/roles in source, not measured |

---

## Swivel-chair hotspots

*None.* No workflow in this wave traverses two or more applications.

**One candidate was considered and rejected.** The application shows genuine internal navigation
churn — `Form1` is simultaneously startup form, navigation shell, child-form host and the only
statistics view (a "god-form"), and `ViewForm` reaches directly into `Form1.Panel5.Controls` to host
`EditForm`. This is **not** a swivel-chair: all of it happens inside one executable over one open
database connection, with no re-authentication, no re-keying an identifier into a second system and
no audit discontinuity *between systems*. Writing it up as one would require redefining
"application" to mean "screen" purely to populate an empty matrix. It belongs to
**`intra-app-redundancy`**, not here.

---

## Fragmented journeys

*None.* No journey in this wave crosses an application boundary.

Note also that the source Discovery artifact carries **no journey inventory** to draw on — only four
`ui_inventory` surfaces and one narrative `typical_workflow`. Every step of that workflow resolves
inside a single executable.

---

## Findings, ranked

| # | Severity | Finding |
|---|---|---|
| 1 | *Scope* | **Single-application wave.** 1 eligible app against a threshold of 2 → Step 0 guard tripped; all analysis arrays empty by design. The app is named in `coverage_exclusions[]` with its reason, which is what lets the G-RR coverage check excuse it rather than read the empty matrix as a silent gap. |
| 2 | *Scope* | **Archetype out of scope.** `desktop` (standalone WinForms thick client, no HTTP/web/API surface); UX overlap scopes to `web-app` / `hybrid`. An independent second reason this app would not contribute even in a larger wave. |
| 3 | *Input gap* | **No `redundancy-matrix.json` staged** for this wave, so `structurally_redundant` / `structural_overlap_pct` could not be cross-referenced. Moot — there are no pairs to annotate. |
| 4 | *Carried forward* | **Governing-profile discrepancy.** Declared profile is `faa`; the catalog, structural-analysis, ux-accessibility and identity-landscape passes **each independently** flag that this student-records tool has no aviation/NAS/FAA relevance. Recorded as a finding only — no alternative profile adopted, and it had no bearing on the determination above. Resolution sits with the engagement owner, upstream of this wave. |

No severity reached `blocker`, `major` or `minor` under the skill's thresholds, because those apply to
overlap findings and swivel-chair patterns and **none were produced**. No severity was assigned by feel.

---

## Review asks

| Ask | Action | Subject | Confidence |
|---|---|---|---|
| `ux-overlap-inventory` | `aware` | wave `3f6bdbb9…` | high (0.95) |

One ask, the unconditional `aware` record. `swivel-chair-pattern-tolerated` and
`journey-fragmentation-assessment` are **not** emitted — both are contingent on findings this run did
not produce. No action is required of the reviewer; the ask exists so the empty matrix is legible as a
result rather than an omission.

---

*Full evidence, run log and the declared exclusion are in `ux-overlap-matrix.json` alongside this file.
Nothing was fabricated to clear the minimum-input threshold, and the unit of comparison remains the
application.*
