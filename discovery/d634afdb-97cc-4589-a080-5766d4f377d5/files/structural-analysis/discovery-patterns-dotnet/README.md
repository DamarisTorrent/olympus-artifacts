# .NET Discovery Patterns — d634afdb-97cc-4589-a080-5766d4f377d5

**Skill:** `discovery-patterns-dotnet`
**Governing client profile:** `faa` (asserted for this task; see Governance Gap below)
**Primary output:** [`dotnet-fingerprint.json`](./dotnet-fingerprint.json)

## Summary

This repository is the public **Gilded Rose Refactoring Kata** — a 172-LOC
C# solution with two legacy-style (`packages.config`) `.csproj` projects:

| Project | Style | TFM | Output | Role |
|---|---|---|---|---|
| `src/GildedRose.Console/GildedRose.Console.csproj` | legacy-csproj | net45 | Exe | Entry point, business logic, `Item` model |
| `src/GildedRose.Tests/GildedRose.Tests.csproj` | legacy-csproj | net451 | Library | xUnit scaffold (1 placeholder test, no real coverage) |

- **Archetype:** does not match any of the skill's 5-value enum
  (`web-app | batch-etl | api-service | scheduled-job | hybrid`). Flagged
  for manual review per Methodology step 3. Upstream `catalog.json` already
  recorded `architecture.archetype = "cli"`, which sits outside this skill's
  enum but is directionally consistent with the source evidence.
- **Hosting model:** `console` (interactive — blocks on `Console.ReadKey()`).
  No IIS, no Kestrel, no Windows Service, no Worker Service.
- **DI container:** `none`. Dependencies are constructed directly (`new
  Program()`).
- **Data access:** `none`. No database, no ORM, no connection strings
  anywhere in the repo (0 tables, matches upstream `catalog.json`).
- **NuGet:** all dependencies resolved via `packages.config` (no
  `PackageReference` anywhere, so no migration-conflict finding). 8
  project-level packages + 5 repo-level build-tooling packages in
  `.nuget/packages.config`. Two version-drift findings (target framework
  net45 vs net451; `GitVersionTask` 2.0.1 vs 3.4.1).
- **Secrets surface:** clean — no hardcoded connection strings or
  credentials found in any config file.
- **Companion stacks:** no Classic ASP or VB6 signals detected anywhere in
  the actual application source.

Full details, decision traces, and `{repo}:{file}:{line}` citations for
every claim are in `dotnet-fingerprint.json`.

## Governance gap (read before using this artifact downstream)

The task declared `faa` as the governing client profile and instructed
this skill to read `profiles/faa/risk-classification.yaml` for tier
banding. That file — and the `profiles/faa/` directory generally — was
**not reachable** from this session's working directories
(`.../source` and its parent). Severities in `dotnet-fingerprint.json`
therefore use this skill's own default bands, not FAA-specific tier
banding. See finding `dotnet-fingerprint.json:governance:F-101`.

## Domain-mismatch corroboration

Independently of the profile-availability gap above, the source code
itself gives no indication this is an FAA system: it is the well-known
public Gilded Rose kata, with no aviation/ATC/certification content, no
database, and no web surface. This corroborates — but does not resolve —
the `open_questions` already raised in the upstream `catalog.json`
(profile/domain mismatch, and the unrelated `fixtures/default.json` fixture
for a different Discovery skill that must not be mistaken for real
application documentation). See finding
`dotnet-fingerprint.json:governance:F-102`. Recommend stakeholder
confirmation of the application_id-to-real-system mapping before this
fingerprint is used for FAA rationalization decisions.

## Handoff

- `catalog-application` — fold `archetype` (flagged, no enum match),
  `tech_stack`, and `primary_runtime` (net45/net451) into the catalog
  entry; note the archetype enum gap (F-002) for schema owners.
- `dependency-mapper` — consume `nuget_dependency_inventory` and
  `hosting_model_findings`.
- Rationalization / **G-DC** gate — this fingerprint is complete for what
  the source contains, but the governance gap (F-101) and domain-mismatch
  corroboration (F-102) should block automatic gate pass-through pending
  stakeholder confirmation.
