# compliance-citation-mapper — scan notes

**Application ID:** `d634afdb-97cc-4589-a080-5766d4f377d5`
**Governing profile (per task declaration):** `faa`
**Assessed date:** 2026-09-28

## What was scanned

Per the application catalog entry (`discovery-catalog/catalog.json`), this
application's actual git-tracked contents are the public **"Gilded Rose
Refactoring Kata"** — a 172-LOC C#/.NET console app with no HTTP surface,
database, or regulatory business logic. `git ls-files` in the source repo
confirms the tracked tree is exactly: `.gitattributes`, `.gitignore`,
`.nuget/*`, `GildedRose.sln`, `MIT-LICENSE.txt`, `NuGet.config`, `README.md`,
`build.bat`, `images/build_output.png`, `src/GildedRose.Console/**`,
`src/GildedRose.Tests/**`, `tasks.ps1`.

The scan (`scan_citations.py` from the `compliance-citation-mapper` skill
bundle) was run against a copy of exactly that git-tracked file set.

## Directories deliberately excluded from the scan

The working directory also contains `fixtures/`, `references/`, `schemas/`,
`scripts/`, and `assets/` — all **untracked** (`git status` confirms; not
part of any commit in this repo). These are Discovery skill-bundle
materials (this skill's own `scan_citations.py`, its output schema, its
`citation-patterns.md` / `faa-citation-catalog.md` reference docs, and a
`fixtures/default.json` test fixture) that ended up co-located in the
working tree rather than being the application's own source. The
application catalog entry already flagged `fixtures/default.json` itself as
a test fixture describing a fabricated, unrelated application and
explicitly excluded it from the catalog entry.

Diagnostic run: scanning the full working directory (including those
untracked directories) produces 75 citation hits (54 unique) purely because
`references/faa-citation-catalog.md`, `references/citation-patterns.md`,
and other skill-documentation files are themselves full of USC/CFR/FAA
Order example citations. None of those citations originate in the actual
application; including them would misattribute the skill's own reference
material to this app's compliance footprint. They were excluded from
`compliance-citations.json` for that reason.

## Result

Zero citations were found in the actual application source (git-tracked
files only). This is expected, not a red flag: the catalog entry sets
`business_domain: "unclassified"` and explicitly could not ground this
application in any FAA business domain (Air Traffic, Flight Safety,
Certification, Workforce, Finance, Logistics, Admin/Travel/Timesheet) —
the repository shows no discernible aviation or FAA regulatory content.
The Handoff Summary's "zero citations for an obviously-regulatory app is a
red flag" check does not apply here, since this app is not tagged as
regulatory-domain.

## Profile discrepancy note

The task's governing-profile declaration for this run is `faa`, and per
instructions that declaration is authoritative regardless of what the
input artifacts state or imply. The application catalog entry itself
already raised, as an open question, whether this `application_id`
genuinely corresponds to an FAA-owned system at all — the repository
content (a generic retail-inventory kata) gives no independent evidence
either way. This note simply carries that discrepancy forward; it is not
resolved here and no FAA-specific citation content was fabricated to fill
the gap.

## Pass 2 (catalog cross-check)

Not applicable — `citations[]` is empty, so there are no unique citations
to reconcile against `profiles/faa/skills/compliance-citation-mapper/references/faa-citation-catalog.md`,
and no proposed catalog additions.

## Pass 3 (schema validation)

`compliance-citations.json` was validated against
`schemas/discovery/compliance-citations.schema.json` (draft 2020-12) with
zero errors.
