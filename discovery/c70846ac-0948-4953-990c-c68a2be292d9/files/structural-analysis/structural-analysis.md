# Structural Analysis — Student Management System (VB.NET)

**Application ID:** `c70846ac-0948-4953-990c-c68a2be292d9`
**Discovery Pass:** 1 — Structural Analysis (`legacy-architecture-mapper`)
**Source root:** `Flat Design/`
**Governing client profile:** `faa` (see [Finding 0](#finding-0--governing-profile-discrepancy))

---

## 1. Executive summary

This is a **single-assembly VB.NET WinForms thick client** over a **file-based Microsoft Access database**, with
**one user table**, **four screens**, and **461 lines of hand-written logic**. It has no web tier, no API, no
batch component, no scheduled job, no message queue, no authentication, no tests and no CI.

The headline structural fact is that **the module boundaries visible in the file tree are not real boundaries.**
Four form classes sit in four files and look independent; in fact they are joined by a single process-wide
mutable `OleDbConnection`, they contain all 16 SQL statements inline in their event handlers, and three
dependency cycles run between them. The nominal data-access layer is 13 lines long and contains no queries.

The second headline fact is a **live correctness defect at a module boundary**: the forms refresh each other
through VB's default-instance mechanism, which resolves to *different objects* than the ones on screen. After a
successful insert, the application updates a dashboard and a grid the user is not looking at.

| Metric | Value |
|---|---|
| Build projects / solutions / deployment surfaces | 1 / 1 / 1 |
| Logical modules | 6 |
| Total VB LOC | 2,787 |
| — hand-written | **461** (17%) |
| — WinForms Designer-generated | 2,326 (83%) |
| Largest single file | `Form1.Designer.vb` — 1,211 lines, 77 controls |
| Database tables / columns | **1 / 10** |
| Stored procedures / views / triggers / FKs | **0 / 0 / 0 / 0** |
| Inline SQL statements | 16, across 4 of 6 modules |
| — unparameterized | 6 (1 takes raw user input) |
| HTTP endpoints / jobs / queues | 0 / 0 / 0 |
| Outbound integrations | 1 (a hardcoded GitHub URL) |
| Authentication mechanisms | **0** |
| Dependency cycles | **3** |
| `AccessibleName` annotations across 137 controls | **0** |
| CI/CD pipelines / tests / commits in history | 0 / 0 / 1 |

### Why there was no fan-out

The skill's fan-out rule names this an explicit **do-not-fan-out** case on three independent counts: 1 top-level
build module (threshold >8), 2,787 LOC (threshold >50 KLOC), 1 database table (threshold >20). Sub-agent
coordination would have cost more than the walk. Every one of the 13 `.vb` files, the `.vbproj`, the `.sln` and all
four config/manifest files was read **in full**, not sampled.

---

## 2. Technology

| Layer | Finding | Evidence |
|---|---|---|
| Language | Visual Basic .NET, 100% of source | `*.vbproj:183` |
| UI framework | Windows Forms (`MyType=WindowsForms`, `OutputType=WinExe`) | `*.vbproj:8,13` |
| Data access | Raw ADO.NET `System.Data.OleDb` — no ORM, no EF, no DataSet designer | `Module1.vb:1` |
| Runtime | .NET Framework 4.8, Windows-only | `*.vbproj:14`, `App.config:4` |
| Database | Microsoft Access (ACE), single `.accdb` file | `Module1.vb:7`, `studentDB.accdb` header |
| Provider | `Microsoft.ACE.OLEDB.12.0` — an out-of-band per-workstation prerequisite, **not** an assembly reference | `Module1.vb:7` |
| Build | MSBuild legacy non-SDK VB project; all 10 references are GAC assemblies, **zero** NuGet packages | `*.vbproj:2,76-85` |
| Packaging | ClickOnce with `PublishUrl` pinned to the author's `D:\PROGRAMING` path | `*.vbproj:18` |
| CI/CD | **none** | — |

Release builds pin `PlatformTarget` to **x86** (`*.vbproj:35`), which is consistent with the 32-bit ACE provider
and is a hard deployment constraint, not an incidental setting.

---

## 3. Module decomposition

All six modules compile into **one** assembly (`Student Management System.exe`) and ship as **one** deployment
surface. The decomposition below is *logical*, offered because a single-node map would give downstream passes
nothing to work with — but the single-assembly fact is what governs deployment.

| Module `id` | Path | LOC | Role | Inline SQL |
|---|---|---|---|---|
| `form1-dashboard` | `Flat Design/Form1.vb` | 1,371 | Startup form, navigation shell **and** statistics dashboard | 10 × `SELECT COUNT(*)` |
| `insert-form` | `Flat Design/InsertForm.vb` | 434 | Create path | 1 × `INSERT` |
| `edit-form` | `Flat Design/EditForm.vb` | 447 | Update path | `SELECT` + `UPDATE` |
| `view-form` | `Flat Design/ViewForm.vb` | 313 | Read / search / delete | 2 × `SELECT`, 1 × `DELETE` |
| `module1-db-connection` | `Flat Design/Module1.vb` | **13** | The *entire* data-access layer | **none** |
| `my-project-infrastructure` | `Flat Design/My Project/` | 209 | Generated app plumbing, default-instance provider | none |

LOC reconciles exactly with the Pass 0 catalog (2,787 = 461 hand-written + 2,326 generated) — computed
independently here, so this is corroboration rather than a copy.

### Dependency graph

```
my-project-infrastructure
        │ startup (MainForm)
        ▼
   form1-dashboard ◄──────────────┐◄────────────────┐
     │   │   │                    │ default-inst.   │ default-inst.
     │   │   └──► insert-form ─────┘                 │
     │   │             │ default-inst.               │
     │   │             └──► view-form ───────────────┘
     │   └──────────────────► view-form ──► edit-form
     │                                         │ default-inst.
     │                                         └──► form1-dashboard
     └──┬──────────┬──────────┬──────────┐
        ▼          ▼          ▼          ▼
    ┌──────────────────────────────────────┐
    │  module1-db-connection               │  ◄── fan-in 4, holds ZERO SQL
    │  Public dbcon  (ONE shared instance) │
    └──────────────────┬───────────────────┘
                       ▼
            studentDB.accdb → students (1 table, 10 cols)
                       ▲
        all four forms also reach the table directly
```

**Three cycles**, all through the shell: `Form1 ↔ InsertForm`, `Form1 ↔ ViewForm`, and
`Form1 → ViewForm → EditForm → Form1`. No form is a leaf. **There is no acyclic extraction order among the four
UI modules as they stand.**

---

## 4. Coupling indicators

Ranked. Full evidence lists are in `structural-analysis.json` → `coupling_indicators`.

### 4.1 Shared global connection — *critical*

`Public dbcon As New OleDb.OleDbConnection` (`Module1.vb:4`) is a process-wide singleton with **no ownership
discipline**: four modules open it, `ViewForm` closes it (`ViewForm.vb:94`), nobody disposes it, and there is
**not one `Using` block in the application**. This is the single tightest coupling present, and every
decomposition boundary in §6 must cut this edge first.

### 4.2 Default-instance aliasing — *critical, and a live defect*

`Form1` displays children it builds with `New InsertForm()` / `New ViewForm()` (`Form1.vb:104,141`), but
`InsertForm` and `EditForm` refresh their siblings through VB's **bare default-instance properties**
(`InsertForm.vb:27,28`; `EditForm.vb:67`), and `ViewForm` hosts `EditForm` inside the *default* `Form1`'s
`Panel5` (`ViewForm.vb:72`).

Two parallel object graphs therefore exist at runtime, and post-write refreshes land on the invisible one:
**after an insert, the on-screen dashboard and grid keep showing stale data.**

This is not stylistic. It is a defect, and it is a migration trap twice over: a naïve port preserves it, and a
port to C# *cannot* translate it at all, because C# has no default-instance feature. The real navigation and
refresh contract has to be **re-specified, not read off the code** — the code does not express what the UI
appears to do.

### 4.3 Unsafe SQL construction — *high*

6 of 16 statements are string-concatenated. Five (`Form1.vb:62,67,72,77,82`) interpolate an integer and are not
currently exploitable. One is:

```vb
query += " WHERE rollno = '" + searchQuery + "' OR fname LIKE '%" + searchQuery + "%'"   ' ViewForm.vb:50
```

Raw keystrokes from `txtSearch`, bound straight to the grid — a **live injection and data-disclosure vector**,
and the only statement in the application that takes untrusted input without binding it.

### 4.4 UI owns all SQL — *high*

All 16 statements sit in UI event handlers across 4 of 6 modules; the nominal DAL is 13 lines with no queries.
There is **no seam** at which to intercept, test, retarget or audit data access. Pass 2 business-logic
extraction must read form event handlers. Any re-platforming **creates** this layer rather than porting it.

### 4.5 Hardcoded environment binding — *high*

Zero externalized configuration. The database is bound by one string literal:

```
data source=D:\PROGRAMING\Visual Basic\Flat Design\Flat Design\Flat Design\studentDB.accdb   ' Module1.vb:7
```

The `.accdb` actually ships at `Flat Design/studentDB.accdb`, so **a clean clone cannot connect on any machine
but the author's.** `App.config` declares no `connectionStrings`; `Settings.settings` is empty; no environment
variable is read anywhere. Changing the path requires a recompile.

### 4.6 Shared-file database concurrency — *high*

A file database plus `SingleInstance=false` (`Application.myapp:5`) means multiple instances contend for one file
with only ACE page locking. **There are no transactions anywhere** — each `INSERT`/`UPDATE`/`DELETE` is a bare
`ExecuteNonQuery`. A committed `studentDB.laccdb` lock file proves the DB was open in Access at commit time.

### 4.7 No automated verification — *high*

No test project, no test file, no CI, no build script, **one commit** in history. Nothing executable specifies
current behaviour, so no migration can be verified by regression.

### 4.8 Unprotected PII in public source control — *high*

The committed `studentDB.accdb` holds **real data** (the decode recovered surname and gender values from data
pages), and the record shape is itself personal data: first/last name, **father's name**, two mobile numbers,
date of birth. No database password, no application authentication, public GitHub origin. **A live dataset of
students' PII is in public source control.** This pass records the structural fact and stops — classification is
a data-protection decision, not a code inference. Route to the data-protection reviewer **independently of
modernization sequencing**; a public exposure should not wait on a migration plan.

### 4.9 Other indicators

| Indicator | Severity | One-line |
|---|---|---|
| Circular form dependencies | high | 3 cycles, all through `Form1`; no leaf modules |
| Insert/Edit near-duplication | medium | Identical 24-control layouts (373 vs 371 lines); 10-field mapping written twice |
| Unenforced identity | medium | `rollno` is the de-facto key; **no PK/unique index found**, no duplicate check on insert |
| `OptionStrict Off` + late binding | medium | `*.vbproj:51`; column contract resolved at runtime, not compile time |
| Accessibility surface unannotated | medium | **0** `AccessibleName`/`AccessibleDescription` across 137 controls |
| Broken clean-clone build | medium | Signing against a gitignored, absent `.pfx`; Debug config maps to Release |
| Hardcoded URL as "reporting" | low | The Report button `Process.Start`s a GitHub PDF — no reporting is implemented |

---

## 5. Database

Decoded **directly from the binary** `studentDB.accdb` (ACE table-definition records), not inferred from SQL
text. Pass 0 inferred one table and explicitly asked Pass 1 to confirm against the real file; this pass did, and
**confirms it**, adding the real column names and on-disk casing.

**`students`** — the only user table. 10 columns:

| Column | Notes |
|---|---|
| `RollNo` | De-facto key for every single-row op. **No PK or unique index found; no duplicate check on insert.** |
| `FName`, `LName` | PII. Free text, no `MaxLength`, no required check. `FName` is the search `LIKE` target. |
| `FatherName` | PII **about a third party who is not the record subject.** |
| `MobNo`, `AltMobNo` | Contact PII. No numeric or phone-format validation. |
| `Gender` | App-enforced domain `Male`/`Female`/**`Other`** — but the dashboard counts only Male and Female. |
| `Course` | App-enforced domain `BCA`/`MCA`/`IIMCA`, hardcoded in two Designer files *and* in `Form1`'s SQL. |
| `YOA` | Year of admission. Static combo list `2019`–`2023`; stored and compared **as a string**. |
| `DOB` | PII. Written as a culture-formatted display string, read back with a culture-free `DateTime.Parse`. |

**Zero stored procedures, views, triggers, relationships and database links** — confirmed from the file's own
catalog, which contains only Access system objects and empty `Forms`/`Reports` containers. Unusually for a
legacy application, **there is no logic hiding in the database.** Those zeros are measured findings, not
unfilled fields.

### What the database walk could *not* establish

The `.accdb` was read as a **file**, never opened through an engine. Deliberately **not guessed**:

- **Column data types, NULL-ability, declared widths, validation rules** — in binary type bytes this decode did
  not resolve. The application is no guide: `OptionStrict Off` plus `AddWithValue` from string controls means
  even `DOB` and `YOA` may be stored as text.
- **Primary keys and indexes** — treat as *not established* rather than *absent*. No PK and no autonumber were
  recovered (`ID` does not occur in the file at all), but 62 `Index` string hits were not resolved to
  definitions. **Confirming this is a migration prerequisite** — if duplicate roll numbers exist, `UPDATE`
  silently rewrites every match and `DELETE` removes every match.
- **Row counts** — not measured, so no `row_count_estimate` is reported rather than a fabricated one.

One ODBC/ACE session against the file closes all three.

### Two schema findings worth carrying forward

1. **Superseded layout retained in the file.** A second `students` definition carries `ClassN` and `Sec` where
   the live one carries `Course` and `YOA` — dead residue from an earlier revision. Check whether any rows still
   carry the old shape; nothing in the application would read them.
2. **Casing differs between schema and code.** The DB declares PascalCase (`RollNo`, `FatherName`,
   `AltMobNo`); every SQL statement and reader lookup uses lowercase. Harmless on case-insensitive Jet —
   **breaks on PostgreSQL**, and breaks precisely in the runtime-resolved places (`stReader("fname")`,
   `Cells("rollno")`).

Also absent: **no audit, soft-delete or provenance column** — no timestamp, no user stamp, no row version.
With no authentication either, **no change to a student record can be attributed or reconstructed**, and
`DELETE` is physical and immediate. That history is already unrecoverable.

---

## 6. Recommended decomposition boundaries

These are offered for whichever disposition is chosen — they are **not** an argument that transformation is the
right one (see [Finding 4](#finding-4--should-this-be-modernized-at-all)).

1. **`student-record-crud-service`** — `module1-db-connection`, `insert-form`, `edit-form`, `view-form`
   The one genuine business capability. The SQL exists but must be **lifted out of four form event handlers**;
   there is no DAL to extract. Requires fixing §4.1 first (connection-per-operation, real transactions) and
   declaring `rollno` as an enforced key. **Validation is a new requirement, not a port** — the insert path has
   none — and the search path must be reparameterized to close §4.3.

2. **`student-statistics-read-model`** — `form1-dashboard`
   The ten aggregates are read-only and separate cleanly. Two defects are **requirements questions, not
   bugs to port**: the hardcoded `currentYear = 2023` (`Form1.vb:59`), which has made every academic-year tile
   wrong since 2024; and gender tiles counting only Male/Female against a three-value domain, so **the tiles do
   not sum to the row count**. The current SQL is evidence of intent, not a specification.

3. **`ui-shell-and-navigation`** — `form1-dashboard`, `my-project-infrastructure`
   Deliberately **overlaps boundary 2 on `form1-dashboard`, and that overlap is the finding**: `Form1` is
   simultaneously shell, child-form host and dashboard, so the two concerns cannot be assigned to disjoint
   module sets at current granularity — splitting the 1,211-line Designer file is itself a work item. Owns the
   three cycles and the §4.2 aliasing defect.

4. **`persistence-platform-replacement`** — `module1-db-connection`
   Not a service boundary but an unavoidable infrastructure item, listed so it is not lost. A file database
   over a 32-bit provider at a hardcoded absolute path cannot be rehosted as-is: it caps concurrency, forces
   x86, needs a per-workstation redistributable, has no credential or encryption story over a PII dataset, and
   **binds the DB with a literal no clean clone can resolve**. Externalizing configuration is a prerequisite
   for *every* other boundary, including a like-for-like rehost.

---

## 7. Findings requiring an owner's decision

### Finding 0 — Governing-profile discrepancy

The authoritative governing profile for this task is **`faa`**, and this pass read policy only from
`profiles/faa/`. **Nothing in this application's source supports that scope**: a single-developer VB.NET
WinForms student-records tool, GPL-licensed, public GitHub origin, one commit, author-credited project report,
and **no aviation, NAS, air-traffic or certification artifact of any kind**. Pass 0 raised the same mismatch
independently.

This pass does **not** adopt any alternative governing profile and does not restate one as fact. It maps the
application as found and flags the discrepancy for the engagement owner **before** any FAA-specific gating
(safety tiering, NAS impact assessment, compliance mapping) consumes these boundaries.

### Finding 1 — Source-tree contamination is wider than Pass 0 reported

Pass 0 flagged one stray file. This pass finds **26 untracked files across four directories** — `assets/`,
`references/`, `scripts/`, `fixtures/` — whose contents are Olympus Discovery-skill assets and reference docs
(ADABAS DDM parsing, classic ASP patterns, NIST 800-63 mapping, OCR readiness rubrics, stored-proc
classification SQL). Confirmed non-application by `git status -uall` (untracked) against 35 tracked files, with
mtimes matching workspace staging rather than the source commit.

They are **excluded from every metric** in this document. But their presence in a customer source tree is
exactly how a later pass silently inflates a file count, "detects" ADABAS or SQL Server in a VB.NET/Access
application, or treats a template as evidence. **Recommend the workspace-staging owner separate skill
scaffolding from the source checkout** — this is an upstream pipeline defect, not a property of the application.

### Finding 2 — Two sibling Discovery artifacts are inapplicable

The dispatch contract declares eight output schemas; six belong to sibling skills dispatched separately to their
own output directories. Two of those are **inapplicable on the evidence**:

- `sqlserver-object-inventory` — describes SQL Server objects; this application uses a file-based Access
  database with zero procedures, views and triggers.
- `tiff-corpus-assessment` — describes an image corpus; this tree holds three PNG screenshots and **no TIFF**.

Emitting either would mean fabricating a server and a corpus that do not exist. Flagging them as not-applicable
is the honest answer and the gate should read it as one.

### Finding 3 — No behavioural baseline, which constrains everything downstream

With no tests, no CI and one commit, several findings here are **ambiguous between bug and intent** — the 2023
year baseline, the Male/Female-only dashboard against a three-value gender domain, the post-insert refresh
landing on off-screen instances. Those need **stakeholder adjudication, not a code reading**. Characterization
tests against the current build are the prerequisite for any transformation beyond a lift-and-shift — and note
that the build itself does not currently reconstruct from a clean clone (§4.5, §4.9).

### Finding 4 — Should this be modernized at all?

**461 lines of hand-written logic, one table, ten columns, three closed value domains, four screens, one genuine
capability.** That is comfortably inside the range where rewriting on a current stack costs less than
transforming. Pass 0 additionally recorded that the active profile defines **no modernization target** for a
VB.NET WinForms + Access stack. **Retire/replace deserves explicit consideration by the disposition owner**, and
the boundaries in §6 should not be read as a recommendation against it.

---

## 8. Artifacts produced

| File | Status |
|---|---|
| `structural-analysis.json` | Authoritative structural map, including the governed `database-schema-summary` and `interface-inventory` **sections** |
| `structural-analysis.md` | This narrative |
| `call-graph.json` | Module-grain call/dependency graph: 9 nodes, 19 edges, 3 cycles |
| `db-schema.json` | **Non-authoritative mirror** of the `database-schema-summary` section — see below |

`db-schema.json` is a byte-equivalent copy of the governed section, written only because this skill's artifact
list names it, while the `structural-analysis` schema states the database schema is a **section** of the parent
and warns that giving it a file path manufactures an undeclared file. Nothing in it diverges. **If the contract
owner must choose one, keep the section.**

### Traceability

Every finding above cites `{file}:{line}` against a repo-relative path. No claim rests on a sampled read: the
whole tree was read. Where a fact could not be established — Access column types, primary keys, row counts — it
is reported as **unknown rather than guessed**, and §5 names the one action (an ODBC/ACE session) that would
close all three.
