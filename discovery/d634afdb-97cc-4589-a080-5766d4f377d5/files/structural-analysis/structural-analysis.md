# Structural Analysis — Gilded Rose Refactoring Kata

**Application ID:** `d634afdb-97cc-4589-a080-5766d4f377d5`
**Discovery pass:** Pass 1 — `legacy-architecture-mapper`
**Governing client profile:** `faa` (authoritative for this task)
**Source root:** `/workspace/discovery-d634afdb-97cc-4589-a080-5766d4f377d5-01a0e90cffd0/source`
**Date:** 2026-09-28

---

## 1. Executive summary

This application is a **single-assembly .NET Framework console monolith of 172 lines of C#**. One
executable, two projects, zero HTTP endpoints, zero database tables, zero external integrations,
zero configuration bindings, and zero authentication. Everything it does happens in one 124-line
file, and 75 of those lines — the method `Program.UpdateQuality()` — are the entire business logic.

Three structural facts should drive everything downstream:

1. **There are no module boundaries to inherit.** The entry point, the business rules and the domain
   model are the same type in the same file (`src/GildedRose.Console/Program.cs:5-122`). Downstream
   lines that expect a "rules engine module" will not find one; §7 proposes where to cut instead.
2. **There is no behavioural baseline.** The solution contains a test project, but it declares **no
   reference to the code under test** and its single test asserts `Assert.True(true)`
   (`src/GildedRose.Tests/GildedRose.Tests.csproj:42-58`, `src/GildedRose.Tests/TestAssemblyTests.cs:7-11`).
   Coverage of the rules engine is 0%, so any transformation is currently unverifiable.
3. **The identity of this application is unresolved.** The tree is the publicly published Gilded Rose
   Refactoring Kata (a retail-inn inventory exercise) with no aviation or FAA content, while the
   shipped assembly metadata asserts a *third-party* agency attribution. See §9 — this is recorded as
   a discrepancy, not adopted.

## 2. Scope of the walk, and what it excluded

The source root contains **53 files, but only 22 belong to the application.** The other 31 —
`references/` (22 Markdown files on ADABAS, VB6, Classic ASP, Unisys InfoImage, NIST 800-63…),
`assets/` (7 output templates), `scripts/classify_procs_template.sql`, and `fixtures/default.json` —
are Discovery-skill reference and template material staged into the source root by the harness. Every
one of them is **untracked in git**, while all 22 application files are tracked, which is how the two
sets were separated (`git ls-files` vs `git status --untracked-files=all`).

They are excluded from every count in this analysis. Counting them would inflate a 172-line console
app into a 53-file system and — via `classify_procs_template.sql` and the Unisys/ADABAS references —
invent a database and a document-imaging corpus that **do not exist in this repository**.

**Method.** Read-only static walk: all 4 C# files, both `.csproj`, the `.sln`, all 4 NuGet configs,
`app.config`, `build.bat` and `tasks.ps1` read in full. Nothing was built, restored or executed.
Dependency edges come from MSBuild `<Reference>`/`<Import>` elements, `packages.config`, and
`using`/qualified-type references in source. **Absence claims are grep-derived, not assumed:** a
case-insensitive search of all tracked files for `connectionstring|Data Source=|Initial Catalog|SqlConnection|OleDb|Odbc|EntityFramework|System.Data.SqlClient|HttpClient|WebRequest|Soap|WCF|ServiceModel|Authenticate|Login|Identity|Principal|appSettings|ConfigurationManager|Environment.GetEnvironmentVariable`
returned **zero matches**, and `<ProjectReference>` returned zero matches.

**No fan-out.** The skill fans out per module above 8 modules / 50 KLOC / 20 tables. This tree has 2
modules, 172 lines and 0 tables, so sub-agent coordination would have cost more than the walk.

**What the walk could not reach.** `packages/` is not restored in this workspace, so `psake.net`'s
`Functions.psm1` — which supplies the `Build` and `Test` task bodies imported at `tasks.ps1:11` — was
**not read**. What the build actually executes is unverified (§6).

## 3. Sizing

| Metric | Value |
|---|---|
| Deployable surfaces | 1 (`GildedRose.Console.exe`) |
| Modules (code projects) | 2 |
| Tracked application files | 22 |
| C# source files | 4 |
| Lines of C# (total) | 172 |
| Lines in `Program.cs` | 124 |
| Lines in `UpdateQuality()` — all business logic | 75 |
| Classes / methods (excl. property accessors) | 3 / 3 |
| Internal project references | **0** |
| Dependency cycles | 0 |
| HTTP endpoints / queues / file exchanges | 0 / 0 / 0 |
| Database tables / procs / triggers / connection strings | 0 / 0 / 0 / 0 |
| Environment-variable or appSettings reads | **0** |
| Test methods / test methods covering business logic | 1 / **0** |
| Item-name string comparisons driving rules | 8 |
| Max nested conditional depth in `UpdateQuality()` | 5 |

## 4. Technology

| Concern | Finding | Evidence |
|---|---|---|
| Language | C#, 100% | `Program.cs:1` |
| Application framework | **None.** Bare BCL; no ASP.NET, MVC, WebForms or WCF anywhere | grep, §2 |
| Runtime (app) | .NET Framework **4.5** — Windows-only, past Microsoft end of support | `GildedRose.Console.csproj:12`, `app.config:4` |
| Runtime (tests) | .NET Framework **4.5.1** — skewed from the app it is meant to test | `GildedRose.Tests.csproj:15` |
| Test framework | xUnit 2.0.0 | `src/GildedRose.Tests/packages.config:3-8` |
| Build | MSBuild ToolsVersion 12.0 (VS 2013), NuGet `packages.config`-style, psake 4.4.1 + psake.net 0.1.3, GitVersion | `GildedRose.sln:3`, `tasks.ps1:11`, `build.bat` |
| CI/CD | **None in repo** — no workflow, pipeline, Jenkinsfile or buildspec | measured absence |
| Persistence | **None** | §5 |

The end-of-support dates for .NET Framework 4.5/4.5.1 should be re-verified against Microsoft's
current lifecycle policy before being cited at a gate; the *structural* fact that matters here and
needs no lifecycle lookup is that **neither project targets .NET Core / .NET 5+**, so nothing in this
tree runs in a Linux container without a port.

## 5. Data: there is none

The application has **no database, no file store, and no persistence of any kind**. All state is an
in-memory `IList<Item>` built from six hard-coded literals at `Program.cs:14-27` and discarded when
the process exits. `app.config` contains only a `<startup>` element — no `<connectionStrings>`
(`src/GildedRose.Console/app.config:1-6`). There are no `.sql` files, DDL, migrations or ORM packages
among the tracked files.

This is why **no `db-schema.json` was written**: emitting an empty schema file would assert that a
walk which found nothing had found a schema. The finding is recorded instead in the
`database-schema-summary` section of `structural-analysis.json`, with the grep evidence behind it.

Two consequences worth carrying forward: the documented invariants (*Quality never negative, never
above 50, Sulfuras fixed at 80*) are enforced **nowhere but inside one loop**, and a night's
inventory run leaves **no audit trail or durable record**. If the real production system persists this
inventory somewhere outside this repository, that store is invisible to this walk (§9).

## 6. Interfaces, integrations and the build chain

**One interface exists:** launching `GildedRose.Console.exe`. It parses no arguments (the `args`
parameter at `Program.cs:8` is never read), writes one line to stdout, and blocks on a keypress
(`Program.cs:33`). There is **no authentication of any kind** — the only access control is OS-level
permission to run the file.

The interface inventory records its `kind` as `unknown` deliberately. The run is *batch-shaped* (one
pass over the whole inventory, then exit) but it is **not schedulable**, because `Console.ReadKey()`
blocks forever without an interactive console. Recording it as `batch` or `scheduled-job` would
assert a capability the application does not have; `ui-page` would assert a page that does not exist.

**Outbound integrations: zero.** No `HttpClient`, `WebRequest`, `ServiceModel`, SOAP, queue or file
export. `integration_points` is an empty array as *measured*, not as a gap in the walk.

**The build, however, is heavily coupled outward** — and it is the one part of this system that
reaches the internet:

- `tasks.ps1` defines **no task bodies**. It calls `Get-DefaultPropertiesFile` and
  `Import-DefaultTasks Version, Clean, Build, Test`, all supplied by the out-of-repo `psake.net`
  package (`tasks.ps1:5`, `tasks.ps1:11`). What `Build` and `Test` do is invisible in this repo.
- `build.bat` **downloads `NuGet.exe` from the public internet** when absent (`build.bat:26-28`),
  restores from the deprecated NuGet **v2** feed (`NuGet.config:7`), hard-requires `cmd` plus Windows
  PowerShell ≥ 3.0 (`build.bat:10`), and shells out to `GitVersion.exe` (`build.bat:42`).

That combination is both a reproducibility problem and a supply-chain exposure, and it is the reason
"what the build executes" appears in the open questions rather than in the findings.

## 7. Coupling — and where to cut

Directories do not tell the truth here: the two projects look decoupled and are, but the *single*
project that matters is internally fused. The seven coupling indicators in
`structural-analysis.json` reduce to four that change downstream work:

1. **God type (high).** Entry point + seed data + rules engine + domain model in one file, one
   namespace (`Program.cs:5-122`). No seam exists to test or replace.
2. **Magic-string dispatch (high).** All 8 rule branches select on `Item.Name` literals — several
   *negated* and nested inside each other (`Program.cs:85-91` nests three name comparisons four levels
   deep). Behaviour is coupled to exact data values, case- and whitespace-sensitive, with no
   normalisation: **renaming an inventory item silently changes its business rules.**
3. **The missing test edge (high).** Covered in §1 and §8 — the most consequential finding here is an
   *absent* dependency, which a reader counting "two projects, xUnit referenced" would assume is
   present.
4. **Shared mutable state (medium).** `Item` has public unguarded setters (`Program.cs:117-121`) and
   `UpdateQuality` mutates caller-owned objects in place across ~25 `Items[i]` accesses. A subtle
   ordering dependency hides in it: `SellIn` is decremented at line 80 and then re-read at line 83,
   so the expiry branch tests the **already-decremented** value — invisible from either line alone.

**Recommended boundaries** (all *intra-assembly*; see `recommended_decomposition_boundaries`):

| Boundary | What it is | Why |
|---|---|---|
| `inventory-rules-domain` | Extract `Item` + per-item-type rules into a referencable library with a public entry point | **Cut this first.** While the rules live on an internal class's instance method reading a private field (`Program.cs:5,7,37`), *nothing* outside the assembly can call them |
| `inventory-run-host` | What remains of `Program`: composition, seed data, invocation | Isolates the two things that block any orchestrated deployment: the blocking `ReadKey()` and the hard-coded six items |
| `inventory-rules-tests` | Re-point the orphaned test project at the extracted library; write characterisation tests | A **precondition**, not a follow-up — pin today's observed behaviour before changing it |
| `no-service-decomposition-warranted` | Stated explicitly | 172 lines, one deployable, no endpoints, no shared database. There is no microservice split here, and saying so prevents a downstream line from inventing one |

## 8. Risk notes for downstream lines

- **Zero regression safety net.** 75 lines of branching business logic, one tautological test. Every
  downstream transformation starts blind.
- **A documented rule is not implemented.** `README.md` specifies that *"Conjured" items degrade in
  Quality twice as fast*, and a `Conjured Mana Cake` is seeded at `Program.cs:26` — but the string
  `Conjured` **appears nowhere** in `UpdateQuality()`. Conjured items currently degrade at the normal
  rate. Business-rule extraction must decide whether to record this as specified-but-absent (§9).
- **Target-runtime gap under the `faa` profile.** This app is Windows-only .NET Framework 4.5; the
  profile's substrate is Amazon ECS on Fargate in AWS GovCloud
  (`profiles/faa/config/common.yaml`) and its .NET codegen configuration targets .NET 8
  (`profiles/faa/config/code-generation-dotnet.yaml`). There is **no in-place path** — a runtime port
  plus removal of the blocking `ReadKey()` is the minimum.
- **Nothing for OKTA to attach to.** No identity, authentication or authorization code exists, so
  there is no identity model to migrate to the profile's `identity_provider`.
- **Dead weight in the build graph.** `NUnit.Runners 2.6.4` restored with no NUnit reference anywhere;
  `GitVersionTask 2.0.1` declared by the console project but never imported; four template BCL
  references (`System.Data`, `System.Data.DataSetExtensions`, `System.Xml`, `System.Xml.Linq`) unused.
  Three GitVersion versions participate in one build.

## 9. Discrepancies and open questions

Two discrepancies are recorded here **as observations about the input artifacts, not adopted as
fact**:

- **Governing-profile mismatch.** The authoritative governing profile for this task is **`faa`**, and
  this analysis is written under it. The source tree contains no aviation, NAS or certification
  content — it is the public Gilded Rose kata, attributed in `README.md` to @TerryHughes/@NotMyself at
  `github.com/NotMyself/GildedRose`. Separately, the shipped assembly metadata asserts
  `AssemblyCompany("DSHS")` and `Copyright "DSHS 2015"`
  (`src/GildedRose.Console/Properties/AssemblyInfo.cs:11,13`) — a **different agency attribution**
  embedded in the binary. That attribution is *not* treated as this task's governing profile. A
  stakeholder must confirm whether this `application_id` maps to a real FAA-owned system before any
  downstream line consumes these boundaries.
- **Input-artifact mismatch.** The staged catalog entry states that `fixtures/default.json` describes
  an *"ASP.NET WebForms 4.8 / SQL Server 2016 system, ~68,400 LOC, eligibility-certification"*. The
  file present at **this** dispatch contains something different: a `legacy-data-flow-tracer` fixture
  for a fabricated *"Fixture Certification Portal"*. Both are synthetic, and the file is untracked in
  both cases — so the conclusion (disregard it) is unchanged, but its contents evidently vary per
  dispatch. **Nothing downstream should cite `fixtures/default.json` as evidence about this
  application.**

The remaining open questions are carried in full in `structural-analysis.json` → `open_questions`:
the Conjured gap (intended kata state, or a real defect?), who signs off the characterisation tests
(particularly the self-cancelling `Quality = Quality - Quality` at `Program.cs:99` and whether the
50-cap is meant to bind the 2nd/3rd backstage increments at `Program.cs:61-71`), the unread
`psake.net` build bodies, whether an external CI pipeline exists, the single-commit git history with
no remote, whether a persistent store exists outside this repository, and whether porting is in scope
at all versus retire/replace.

## 10. Artifacts produced

| File | Contents |
|---|---|
| `structural-analysis.json` | Module map, coupling indicators, duplication map, decomposition boundaries, plus the `database-schema-summary` and `interface-inventory` sections |
| `structural-analysis.md` | This narrative |
| `call-graph.json` | Method/member-grain call and mutation graph; 12 nodes, 14 edges, 0 cycles |

`db-schema.json` was **deliberately not written** — the application has no database (§5). The sibling
Discovery artifacts declared for this pass (`sqlserver-object-inventory`, `language-detection`,
`db-archaeology`, `data-flow-trace`, `identity-landscape`, `tiff-corpus-assessment`) are produced by
their own skills in their own dispatches; on the evidence above, most are inapplicable to this
application.
