# Application Catalog Entry — Student Management System (VB.NET)

**Application ID:** `c70846ac-0948-4953-990c-c68a2be292d9`
**Governing client profile (authoritative, per task declaration):** `faa`

> ⚠️ **Profile/content mismatch flagged for gate review.** The governing
> profile for this Discovery run is `faa` (Federal Aviation Administration
> legacy modernization program — NAS safety, air traffic, pilot
> certification, etc., per `profiles/faa/profile.yaml`). The source tree
> itself, however, is a small, self-contained **student record management**
> desktop application with no detectable aviation, NAS, or FAA business
> content anywhere in the code, README, or project report. This catalog
> entry is produced strictly from what the repository actually contains;
> it does **not** restate the FAA framing as fact and does not fabricate
> aviation relevance to fit the profile. See **Open Questions** below —
> this should be confirmed with the engagement owner before the entry is
> used for FAA-specific gating (safety tiering, NAS impact assessment,
> compliance mapping, etc.).

## Summary

A standalone Windows desktop (WinForms) application, originally published
by its author as *"Student Management System Using VB.Net And Microsoft
Access."* A dashboard form (`Form1`) shows counts of students by gender,
course, and academic year; three companion forms (`InsertForm`,
`EditForm`, `ViewForm`) let a user add, search/view, edit, and delete
individual student records. All data lives in a single `students` table
inside a local Microsoft Access database file (`studentDB.accdb`) that
ships inside the repository. The README and the author's bundled project
report both frame this as a single-developer academic/portfolio project.

## Technology Stack

| Category    | Values |
|-------------|--------|
| Language    | Visual Basic .NET (100% of source) |
| Framework   | Windows Forms (WinForms) |
| Runtime     | .NET Framework 4.8 (`TargetFrameworkVersion` in the `.vbproj`) |
| Database    | Microsoft Access — Jet/ACE OLEDB provider, `.accdb` file |
| Build tools | MSBuild, Visual Studio Solution (`.sln`) |
| CI/CD       | None found — no workflow/pipeline files in the tree |

## Architecture

- **Archetype:** `desktop` (see rationale below)
- **Evidence:**
  - `.vbproj` declares `OutputType=WinExe` and `MyType=WindowsForms`.
  - Four `Form` classes wired together by direct control manipulation and
    panel-swapping (`Panel5.Controls.Add(...)`), not HTTP routing.
  - All persistence is inline OleDb SQL (`SELECT` / `INSERT` / `UPDATE` /
    `DELETE` against one table, `students`) issued directly from form
    code — no API layer, no service layer, no ORM.
  - DB connection string in `Module1.vb` points at a local, hardcoded
    file-system path to the bundled `.accdb` — no server, no listener, no
    scheduler entry point.
- **Taxonomy gap:** the suggested archetype set for this artifact
  (`web-app`, `batch`, `hybrid`, `service`, `headless`, `cli`, `library`,
  `mainframe`, `embedded`) has no bucket for a GUI desktop thick-client.
  None of `web-app`/`api`-like/`batch`/`headless`/`cli` apply — the app
  has an interactive GUI, no HTTP surface, and no scheduler. `desktop` is
  used here as the closest honest label rather than forcing a mismatched
  category; flagged below for the taxonomy owner.
- **Major components:** one WinForms project (`Flat Design`) containing a
  dashboard form that hosts three child forms in a panel; a shared
  `Module1.vb` holds the single `OleDbConnection`; no distinct data-access
  layer.

## Size & Complexity

| Metric | Value |
|---|---|
| LOC (total, VB) | 2,787 |
| — of which Designer-generated | ~2,326 (83%) |
| — of which hand-written | ~461 (17%) |
| Module count | 1 (single `.vbproj`) |
| File count (source-relevant) | 24 |
| Endpoint count | n/a (no HTTP surface) |
| Table count | 1 (`students`, inferred from embedded SQL — see note) |
| **Complexity tier** | **simple** (LOC ≪ 10k, modules ≤ 10, per profile-default thresholds — no FAA-specific override found) |

## Safety Tier

**Not set — `null`.** No authoritative safety classification input was
supplied at onboarding or by a prior Discovery run, and the methodology
explicitly forbids inferring safety tier from code patterns alone. For
reviewer context only: the FAA profile's own qualitative signal table
(`profiles/faa/README.md`) would lean this toward **T3** given an
"Admin"-type domain, no external interfaces, and a small user base — but
that is a signal, not a classification, and must come from stakeholder /
Safety Board input.

## Business Domain

Set to **"Admin"** — the closest general match from the FAA profile's
documented domain taxonomy (Air Traffic, Flight Safety, Aviation Safety,
Certification, Workforce, Finance, Admin, Travel, Timesheet). Neither the
repository nor its docs state an actual business owner or sponsoring
office, and the application's content does not resemble an FAA system at
all — see the mismatch warning above.

## User-Facing

**Yes** — this is an interactive, directly-operated GUI application.

## Open Questions

1. **Profile/content mismatch.** Governing profile is `faa`, but the
   application has no aviation/NAS/FAA relevance. Confirm with the
   engagement owner before using this entry for FAA-specific gates.
2. **Safety tier unconfirmed.** No authoritative input provided; flagged
   rather than guessed.
3. **Business domain is a best-general-match guess** (`Admin`) against
   the FAA taxonomy, not a confirmed value.
4. **No CMDB export or ownership documentation** was provided; business
   owner and operational criticality are unconfirmed.
5. **`fixtures/default.json` found inside the application's own source
   tree** is a QA/test fixture for the `catalog-application` skill itself
   (its payload describes an unrelated fictitious "Fixture Application"
   with a C#/ASP.NET WebForms/SQL Server stack). It was disregarded as a
   source of facts about this real application; its presence inside the
   source tree (rather than test infrastructure) may indicate
   repository/fixture cross-contamination worth investigating upstream.
6. **No modernization target defined.** The FAA profile's legacy
   technology mapping (`profiles/faa/technology.yaml`) covers ASP.NET /
   C# / WCF under `.NET` but has no entry for VB.NET WinForms + MS Access.
7. **Archetype taxonomy gap.** No listed archetype cleanly covers a
   desktop GUI thick-client; `desktop` was used as the closest honest
   label. Recommend the taxonomy owner add an explicit category.
8. **Table/schema count is SQL-text-derived, not DDL-derived.** The
   `.accdb` is a binary file that couldn't be parsed with text tooling;
   Pass 1 (Structural Analysis) should confirm the real schema.

## Out of Scope (per skill contract)

This entry intentionally does **not** include a module map, call graph,
database schema, or dependency analysis — those are Pass 1 (Structural &
Dependency Mapping) deliverables.
