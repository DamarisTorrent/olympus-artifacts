# .NET Discovery Patterns — Application c70846ac-0948-4953-990c-c68a2be292d9

**Application:** Student Management System (VB.NET) — single WinForms desktop project
**Repo:** Student-Management-System-VB.Net (`Flat Design/` subfolder holds the actual app)
**Full structured output:** `dotnet-fingerprint.json` (this directory)

## Governing profile note
This task's governing profile is declared as `faa`, but no `profiles/` directory
exists in this checkout for this pass to read directly. This is not a new
finding — the upstream `catalog.json` (Discovery.catalog) already flags the
same thing as its lead open question: the application is a generic
student-record desktop tool with no detectable FAA/NAS/aviation relevance,
and the FAA profile's `.NET` modernization-target mapping only covers
ASP.NET/C#/WCF, not a VB.NET WinForms + MS Access desktop stack. This pass
defers to that finding rather than restating or resolving it.

## Project fingerprint (1 project, 1 solution)
| Field | Value | Citation |
|---|---|---|
| project_path | `Flat Design/Student Management System Siddharth Jain.vbproj` | — |
| project_style | `legacy-csproj` (no `Sdk=` attribute, explicit `<Compile Include>`) | vbproj:2 |
| target_framework | `net48` (raw `v4.8`) | vbproj:14 |
| language | `vbnet` | — |
| output_type | `WinExe` | vbproj:8 |
| startup | `My.MyApplication` → `MainForm=Form1` | vbproj:9, Application.myapp:4 |

## NuGet dependency inventory
**Zero.** No `packages.config` anywhere in the repo; no `<PackageReference>`
elements in the `.vbproj`. All 10 `<Reference>` entries are .NET Framework
GAC assemblies (`System.Windows.Forms`, `System.Data`, etc.), not NuGet
packages. (vbproj:76-85)

## Archetype classification: **no match — manual review required**
Evaluated against the catalog enum (`web-app | batch-etl | api-service |
scheduled-job | hybrid`) in order; none fire. Per the methodology's explicit
fallback ("if none match... flag for manual review — do not guess"), no
enum value is forced. This independently confirms the upstream catalog
entry's own "Archetype taxonomy gap" open question (it used an out-of-enum
`desktop` label for the same reason). **Recommendation:** the catalog
taxonomy owner should add a `desktop`/`thick-client` archetype value.

## Hosting model: **no match — manual review required**
No `Program.cs`/`Startup.cs`, no `web.config` (none exists in the repo),
no `ServiceBase`/`BackgroundService`. Actual hosting is a locally
double-click-launched WinForms GUI process (VB `My.Application` bootstrap).
None of the given enum values (`iis-aspnet | iis-aspnet-core-module |
kestrel-selfhost | windows-service | worker-service | console`) accurately
describe this; `console` is the closest but wrong (GUI message loop, not a
console host).

## DI container: `none`
No `ConfigureServices`/`ContainerBuilder`/`UnityContainer`/`StandardKernel`
instantiation anywhere in the 5 hand-written `.vb` files. Forms are
constructed with plain `New InsertForm()` / `New EditForm(rollNo)` calls.

## Data access: `ado-net` (single project)
Direct `System.Data.OleDb` usage (`OleDbConnection`, `OleDbCommand`,
`OleDbDataAdapter`, `OleDbDataReader`) against a single Module-level shared
connection, backed by Microsoft Access (`.accdb`) via
`Microsoft.ACE.OLEDB.12.0`. No ORM anywhere in the solution.

## Config / secrets surface
- `App.config` has no `<connectionStrings>` — only a `<startup>` runtime
  pin. The real connection string lives **in source code**
  (`Module1.vb:7`), a 5th non-standard location beyond the usual four
  (web.config / app.config / appsettings.json / user-secrets).
- No credentials embedded (Access file auth has none), but the data source
  is a **hardcoded absolute developer-machine path**
  (`D:\PROGRAMING\Visual Basic\Flat Design\...`) — the app cannot connect
  on any other machine without a source edit + rebuild.

## Findings summary (see `dotnet-fingerprint.json.findings[]` for full citations)
| ID | Severity | Summary |
|---|---|---|
| F-002 | informational | Archetype enum gap (confirms catalog's own open question) |
| F-003 | informational | Hosting-model enum gap (no WinForms-desktop value) |
| F-004 | **security-high** | SQL-injection vector in `ViewForm.LoadSData` (string-concatenated search query) — contrasts with correctly parameterized Insert/Edit/Delete paths |
| F-005 | medium | Hardcoded absolute dev-machine DB path in `Module1.vb:7` |
| F-006 | medium | `.vbproj` references a ClickOnce signing `.pfx` that does not exist in the repo — signed-manifest build is not reproducible from a clean checkout |
| F-007 | low | Access lock file `studentDB.laccdb` committed to source control |
| F-008 | low | `fixtures/default.json` and `references/`, `assets/`, `scripts/` at repo root are unrelated Discovery-skill QA/reference artifacts, not part of the application — corroborates the same contamination the catalog entry already flagged |
| F-009 | informational | `faa` profile declared but not present in this checkout; deferred to catalog's existing scope-mismatch finding |

## Handoff
- `catalog-application`: fold `project_style=legacy-csproj`,
  `target_framework=net48`, zero NuGet dependencies, and the archetype/
  hosting enum-gap findings into the catalog entry's `tech_stack` /
  `primary_runtime`. Catalog's `archetype: "desktop"` is corroborated,
  not contradicted, by this pass.
- `dependency-mapper`: NuGet inventory is empty — nothing to graph on the
  package side; the only external dependency is the local `.accdb` file.
- Security-scan-review: prioritize F-004 (SQL injection) and the
  hardcoded-path finding (F-005) if this app is ever moved off a
  single-developer machine.
- Rationalization: no profile-driven modernization target currently
  applies (per catalog's own open question); this pass found nothing to
  change that.
