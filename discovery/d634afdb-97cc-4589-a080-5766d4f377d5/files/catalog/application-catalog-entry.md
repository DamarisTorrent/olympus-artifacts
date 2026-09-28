# Application Catalog Entry — Discovery Pass 1

**Application ID:** `d634afdb-97cc-4589-a080-5766d4f377d5`
**Application name (inferred):** Gilded Rose Refactoring Kata
**Governing client profile:** `faa` (per task declaration — see ⚠️ Profile/Domain Mismatch below)

## ⚠️ Profile/Domain Mismatch — read first

The cloned source tree is the well-known **"Gilded Rose Refactoring Kata"**: a
teaching exercise about an inn that buys and sells goods (`README.md`, item
names like "Aged Brie", "Sulfuras, Hand of Ragnaros", "Backstage passes to a
TAFKAL80ETC concert"). Nothing in the code, manifests, or docs references air
traffic, aviation, NAS operations, aircraft certification, or any other FAA
business concern. It also does not present as a real production system: it is
a single 124-line `UpdateQuality` method with a fixed in-memory item list, run
once from a console `Main()`.

Compounding this, `fixtures/default.json` in the repository self-identifies as
a **test fixture for the Discovery `catalog-application` skill itself**
("Default fixture for Discovery Step 1 (Catalog)... SKILL.md, contract
artifact_filename, and this fixture") and contains a *different, fabricated*
application record (an ASP.NET WebForms 4.8 / SQL Server 2016 system,
~68,400 LOC, `business_domain: eligibility-certification`) that does not
describe the actual repository contents. That fixture record was **not** used
to populate this catalog entry — it is flagged here only so a reviewer can
confirm it should keep being disregarded, and does not itself declare a
different governing profile.

Per the governing-profile instructions for this task, the `faa` profile
declaration stands regardless of this content, so archetype/complexity
classification below uses `faa`-profile defaults where applicable (none of
the FAA-specific thresholds were actually overridden — see Methodology
Notes). `business_domain` is left as a generic placeholder rather than
fabricated; see Open Questions.

## Description

A small C#/.NET Framework console application implementing the classic
"Gilded Rose" inventory kata: each simulated day, item `SellIn` and `Quality`
values are updated according to item-specific rules (normal goods degrade,
"Aged Brie" and "Backstage passes" improve with age up to a cap of 50,
"Sulfuras" never changes, and "Conjured" items — mentioned in the README but
not yet implemented in `Program.cs` — should degrade twice as fast). The
solution has no HTTP surface, no database, and no scheduler; it prints a
banner, runs `UpdateQuality()` once, and waits for a keypress before exiting.
An `xUnit`-based test project exists but currently contains only a placeholder
assertion (`Assert.True(true)`), i.e. no real coverage of the business logic.

## Technology Stack

| Category    | Findings |
|-------------|----------|
| Languages   | C# — 100% (172 LOC, all files) |
| Frameworks  | None (application); xUnit 2.0.0 (test project only) |
| Runtimes    | .NET Framework 4.5 (`GildedRose.Console`), .NET Framework 4.5.1 (`GildedRose.Tests`) |
| Databases   | None found |
| Build tools | MSBuild, NuGet, psake (via `tasks.ps1` / `build.bat`), GitVersionTask (semantic versioning) |
| CI/CD       | None found in-repo (no GitHub Actions / Azure Pipelines / Jenkinsfile) |

Versions are taken directly from `packages.config` and the `.csproj`
`TargetFrameworkVersion` elements — the only manifests present (there is no
`pom.xml`, `package.json`, `pyproject.toml`, etc., consistent with a
single-solution .NET Framework repo from ~2013–2016 vintage tooling,
Visual Studio 2013 solution format).

## Archetype Classification: `cli`

**Evidence:**
- Single entry point: `static void Main(string[] args)` in
  `src/GildedRose.Console/Program.cs`, which builds a fixed `Item` list,
  calls `UpdateQuality()` once, and blocks on `Console.ReadKey()` before
  exiting.
- No HTTP server, route table, or UI templates/SPA bundle anywhere in the
  tree → rules out `web-app` and `service`.
- No route table producing machine-readable-only responses → rules out `api`.
- No cron/scheduler/DBMS_SCHEDULER definition and no long-running listener →
  rules out `batch` / `scheduled-job`.
- Not packaged as a reusable library (it is an `Exe` `OutputType` per the
  `.csproj`) → rules out `library`.

`cli` is the closest match in this schema's archetype vocabulary
(`web-app | batch | hybrid | service | headless | cli | library | mainframe |
embedded`).

## Size Metrics

| Metric | Value | Basis |
|--------|-------|-------|
| LOC (total) | 172 | Sum of all `.cs` files (`Program.cs` 124, `GildedRose.Console/Properties/AssemblyInfo.cs` 36, `GildedRose.Tests/TestAssemblyTests.cs` 12, `GildedRose.Tests/Properties/AssemblyInfo.cs` 0/empty) |
| LOC by language | C#: 172 | Only language present |
| Module count | 2 | Two `.csproj` projects under `src/`, matching the two non-solution-folder `Project` entries in `GildedRose.sln` |
| File count | 22 | All tracked, non-`.git` files in the repository |
| Endpoint count | null | No HTTP routes/controllers exist |
| Table count | null | No connection strings, ORM config, or DB drivers found |
| Stored procedure count | null | No database access at all |
| DDL files in source | 0 | None found |

## Complexity Tier: `simple`

Using the default thresholds (the `faa` profile does not override
complexity-tier thresholds anywhere in `profiles/faa/`): LOC (172) is well
under 10k, module count (2) is ≤ 10, and endpoint count is 0/null. Every
dimension lands in `simple`, so `simple` is reported (never averaged, per
methodology).

## Safety Tier: unresolved (open question)

`profiles/faa/risk-classification.yaml` requires an authoritative safety
classification, or explicit stakeholder/Safety Board confirmation, before a
tier is assigned — code patterns alone must not be used to infer it. No such
input was supplied at onboarding for this application. `safety_tier` is
therefore `null` in the JSON artifact, and stakeholder confirmation is listed
in Open Questions.

## User-Facing: `false`

The application is a one-shot console demo with no persistent UI, web
front-end, or API — it is not a system with end users in the enterprise
sense.

## Open Questions

1. **Profile/domain mismatch** — this source tree shows no relationship to
   FAA/NAS/aviation business domains. `business_domain` was set to the
   generic placeholder `unclassified` rather than fabricated against the FAA
   taxonomy (Air Traffic, Flight Safety, Certification, Workforce, Finance,
   Logistics, Admin/Travel/Timesheet/Internal). Recommend confirming with
   stakeholders whether this `application_id` is correctly mapped to this
   repository before any downstream pass (Structural Analysis, Rationalization,
   etc.) builds on this catalog entry.
2. **Fixture artifact in-repo** — `fixtures/default.json` contains a fabricated
   catalog record for an unrelated ASP.NET WebForms/SQL Server application; it
   was disregarded when producing this entry but is flagged for reviewer
   awareness in case it was placed there by mistake or is expected to be
   consumed by tooling.
3. **Safety tier** — no authoritative classification was provided; needs
   stakeholder/Safety Board confirmation per `profiles/faa/risk-classification.yaml`.
4. **CI/CD** — no pipeline configuration was found in-repo; confirm whether
   build/test/deploy is handled by an external, not-checked-in pipeline.
5. **Business owner / criticality** — no CMDB export or architecture
   documentation was provided at onboarding to independently confirm these.

## Methodology Notes

- Complexity-tier thresholds: defaults from the catalog-application skill
  were used; `profiles/faa/` config was checked (`profile.yaml`,
  `technology.yaml`, `risk-classification.yaml`, `scoring.yaml`,
  `config/common.yaml`, `objectives.yaml`) and none override LOC/module/
  endpoint thresholds.
- Archetype taxonomy: the catalog-application `SKILL.md` describes
  `web-app | batch | api | scheduled-job | hybrid`, but the binding output
  schema (`application-catalog-entry.schema.json`) declares a different,
  broader vocabulary (`web-app | batch | hybrid | service | headless | cli |
  library | mainframe | embedded`) and is authoritative for validation; `cli`
  was chosen from the schema's list as the closest match.
- No CMDB export or pre-existing architecture documentation was provided as
  Discovery input for this run.
