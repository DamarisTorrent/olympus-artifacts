# Compliance Citation Mapping — Student Management System (VB.NET)

**Application ID:** `c70846ac-0948-4953-990c-c68a2be292d9`
**Governing profile (authoritative, per task declaration):** `faa`
**Assessed date:** 2026-10-02
**Result:** `compliance-citations.json` — **0 citations detected** (passes schema validation)

This note records the Pass 2 (catalog cross-check) reasoning behind the
empty result, since a zero-citation artifact is called out in the skill's
own Handoff Summary as "a red flag" worth explaining rather than emitting
silently.

## 1. Governing-profile discrepancy (recorded as a finding, not adopted)

The task's governing client profile is **`faa`** (authoritative, per the
task declaration), so Pass 2 read the citation catalog from
`profiles/faa/skills/compliance-citation-mapper/references/faa-citation-catalog.md`.
That catalog is curated entirely around FAA aviation-regulatory
obligations — 49 USC Subtitle VII (aviation programs, airman
certificates, aircraft recordation), 14 CFR parts 47/49/61/63/65/67/91/183,
FAA Orders, and related Public Laws/EOs — and explicitly scopes itself to
the ATLAS mock applications (`rms-mock`, `iacra-mock`, `medxpress-mock`,
`dms-mock`).

The scanned application is, per its own README, project report, `.sln`
name, and single-author GPL-licensed GitHub history, a **standalone
VB.NET WinForms "Student Management System"** (insert/view/edit/delete
student records in a local MS Access `.accdb` file). It has no aviation,
NAS, air-traffic, certification, or FAA-adjacent subject matter of any
kind, and the application catalog entry (`catalog.json`) and the prior
structural-analysis pass both independently flagged this same
scope/profile mismatch as an open question for the engagement owner.

This skill does **not** adopt an alternative governing profile and does
not restate one as fact — per instruction, the `faa` declaration governs
policy/catalog selection for this run regardless. The mismatch is logged
here as a finding for the engagement owner to resolve before any
FAA-specific gating (safety tiering, NAS impact assessment, compliance
mapping, OSCAL control mapping) consumes this artifact.

## 2. Source-tree contamination excluded from the scan

`scripts/scan_citations.py` was run against the full staged source tree.
A raw, unfiltered run (`--min-confidence low`) returned 26 raw hits, but
**all 26 were located in exactly two files**:

- `references/citation-patterns.md`
- `scripts/scan_citations.py`

Both are **this skill's own reference documentation and detection
script** (the same files bundled under `/app/skills/compliance-citation-mapper/`),
present in the staged tree as `git`-untracked files alongside `assets/`,
`fixtures/`, and `schemas/`. `git status` / `git ls-files` confirm none of
these five directories are part of the application's own one-commit
GitHub history — they are Olympus Discovery skill-scaffolding assets that
leaked into the same staging directory as the real application checkout.
The application catalog entry independently flagged one such file
(`fixtures/default.json`) as cross-contamination to disregard, and the
structural-analysis pass extended that finding to all four/five
directories. This pass concurs and excludes them on the same basis: the
26 raw hits are the skill's own worked examples of citation syntax
(e.g. `49 USC §44107`, `14 CFR §49.17`, `EO 13526` used as regex-pattern
documentation), not citations encoded by the application under
assessment. Including them would misrepresent the Student Management
System as having FAA regulatory linkage it does not have.

After excluding the contamination paths, the scan was re-run scoped to
the application's actual code root, `Flat Design/` (the single `.vbproj`
WinForms project — `Form1`, `InsertForm`, `EditForm`, `ViewForm`,
`Module1`, plus Designer-generated files), and to the top-level
`README.md`. **Zero USC / CFR / PL / FR / EO / agency-order citations**
were found in either location — consistent with an application whose
business logic is four inline-SQL CRUD forms against a single `students`
table in a local Access file, with no regulatory text in code or
comments.

## 3. Why zero is the correct result here, not a re-scan trigger

The skill's Handoff Summary flags a zero result as suspicious only "for
any application whose business-domain tags indicate regulatory scope
(transportation, defense, health, treasury, tax)." This application's
catalog entry sets `business_domain: "Admin"` (itself a forced best-fit
against the FAA domain taxonomy, since the app has no real FAA business
owner) and the architecture is a disconnected desktop tool with no
external interfaces. Lowering `--min-confidence` would not change the
result — the raw low-confidence pass already found nothing in the actual
application files. No re-scan was triggered.

## 4. Recommendation (upstream, outside this skill's scope)

Per the structural-analysis pass's recommendation, the workspace-staging
process that produces the `source/` checkout for Discovery passes should
separate Olympus skill scaffolding (`scripts/`, `schemas/`, `references/`,
`fixtures/`, `assets/`) from the customer's actual source checkout, so
future runs of this and other detection skills don't need to re-derive
this exclusion by hand.
