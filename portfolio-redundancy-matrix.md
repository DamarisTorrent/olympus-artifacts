# Rationalization Capability Clustering — Wave 3f6bdbb9-81fa-4fb9-845f-fb6a81ba2cbe

## Cluster summary

This wave clustered **2 rat-caps from 2 fine capabilities**, **0 bound to a strategy-of-record catalog, 2 unbound** (no strategy-of-record reference was staged for the `faa` profile — see Open Questions).

| Field | Value |
|---|---|
| Wave ID | `3f6bdbb9-81fa-4fb9-845f-fb6a81ba2cbe` |
| Portfolio ID | `650aa38b-87e7-4f20-a1d0-00399778a64f` |
| Portfolio / wave name | Student Management System (VB.NET) — single-application wave |
| Applications contributing | 1 (`c70846ac-0948-4953-990c-c68a2be292d9`, "Student Management System") |
| Fine capabilities in | 2 |
| Rat-caps out | 2 |
| Bound to strategy-of-record | 0 |
| Unbound (self-authored slug) | 2 |
| Splits | 0 |
| Generated | 2026-10-05 |

This is a single-application wave: the cross-application consolidation signal (the main value driver for this skill) is absent by construction — there is no peer application in the wave to consolidate against. Roll-up/split logic still applies at within-app grain, and that is what drove this clustering: the wave's two fine capabilities already sit at (or very close to) disposition-decision grain, and within-app evidence from `intra-app-redundancy.json` positively confirms they are two **distinct** business outcomes rather than one.

No `coverage_exclusions` are declared — the wave's one application contributes to both rat-caps below, so there is no application left uncovered.

## Per-rat-cap card

### 1. Student Personnel Records Management

- **External ID:** `RATCAP-STUDENT-RECORDS-CRUD` — unbound; no strategy-of-record catalog was staged for this profile/wave to bind against (see Open Questions).
- **Description:** Create, read, update, and delete of individual student academic records (identity, contact, demographics, course, admission year, DOB) in the single system of record. This is the disposition unit for the application's one genuine CRUD outcome.
- **Contributing fine capabilities:**
  - Student Management System (`c70846ac-0948-4953-990c-c68a2be292d9`) — `personnel-records-management` (`eabaec15-7f79-48fb-96f2-2f54c8ade035`)
- **Rationale:** Within-app cohesion signal from `intra-app-redundancy.json`: the three screens realizing this capability (insert-form, edit-form, view-form) cluster together as a 3-member clique at module grain, with every pairwise composite score (74–85) clearing the 60-point cluster threshold on shared entity/operation/persona overlap, and a reviewer-facing recommendation of `shared_service`. The fine capability already sits at this grain (one app, no peer in the wave to consolidate across), so it rolls into exactly one rat-cap unchanged.
- **Confidence:** 0.75 — the clustering boundary itself is well evidenced; confidence is held back from higher only by the unresolved external-vocabulary binding (see review ask below).

### 2. Student Population Reporting & Analytics

- **External ID:** `RATCAP-STUDENT-REPORTING-ANALYTICS` — unbound; no strategy-of-record catalog was staged for this profile/wave to bind against.
- **Description:** Read-only aggregate dashboard reporting on the student population (counts by gender, course, and admission-year bucket), the application's sole analytics surface, distinct from the CRUD outcome it reads from.
- **Contributing fine capabilities:**
  - Student Management System (`c70846ac-0948-4953-990c-c68a2be292d9`) — `reporting-and-analytics` (`0f159e42-7118-4ebb-9a1e-972e4e2df352`)
- **Rationale:** Within-app evidence shows this is NOT the same outcome as the CRUD cluster: `intra-app-redundancy.json` explicitly rejects `form1-dashboard` from the insert/edit/view clique, scoring its pairwise composites at 46–51 — below the 60-point cluster threshold — specifically because it is "a separate reporting concern." The fine capability is therefore kept as its own disposition unit rather than merged into the records-management rat-cap.
- **Confidence:** 0.8 — the separation from the CRUD cluster is directly evidenced by a below-threshold score on every pairwise comparison against the three CRUD screens.

## Splits

none

## Open questions

- Governed capability vocabulary has no student-records-specific entry; `personnel-records-management` (and the "Student Personnel Records Management" rat-cap's name/external_id) are being used as the closest available proxy for person-record CRUD. A strategy-of-record owner should confirm this binding, or supply the correct catalog entry, on review.
- Governing-profile discrepancy flagged upstream, not asserted here as fact: this task's governing client profile is declared as `faa`, but the staged `business-logic.json`, `redundancy-matrix.json`, and `integration-graph.json` each independently report that the in-scope application (Student Management System, VB.NET) has no aviation/NAS/airman/certification content and is a generic single-developer academic admin tool. This clustering pass does not adopt an alternative profile and did not find any FAA strategy-of-record catalog to bind `external_id` against; the mismatch remains open for the engagement/profile owner to resolve.
