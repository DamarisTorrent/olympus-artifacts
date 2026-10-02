# Shared Database Analysis — Student Management System (VB.NET)

**Application:** `c70846ac-0948-4953-990c-c68a2be292d9` · **Wave:** unassigned ·
**Governing profile:** `faa` (see *Scope discrepancy* below) ·
**Structured artifact:** `shared-db-analysis.json`

## The headline

This application's database is not shared with anything. It owns one Microsoft
Access file containing one table of student records, and it is that table's only
writer. There are no shared tables, no cross-database links, no reports, feeds or
scheduled jobs reaching into the data, and no second application anywhere in the
delivered code.

That matters because shared databases are normally the biggest single constraint
on migration scheduling — they force applications to be moved together or to
carry a temporary bridging layer. Neither applies here. This application
constrains no other application's timing, and no other application constrains
its.

## What the store actually is

A single Microsoft Access file, `studentDB.accdb`, holding one table called
`students` with ten columns: roll number, first and last name, father's name, two
mobile numbers, gender, course, year of admission and date of birth. The database
engine runs inside the application's own process through a 32-bit add-on
component; there is no database server, no instance, no network listener and no
login. Access to the entire dataset is governed by file permissions alone — the
file carries no password and is not encrypted.

The whole data layer is one connection string hard-coded on line 7 of
`Module1.vb`, opened by a single connection object that all four screens share.
No configuration file binds the database at all: the application's `App.config`
has no connection-strings section and its settings file is empty.

## How the "not shared" conclusion was reached

Four independent checks, all pointing the same way:

**The build.** The solution declares exactly one project, producing one Windows
executable, with no project references and no class library, service or second
program. There is no other piece of software in the delivery that could be
sharing anything.

**The code's database statements.** All fifteen of them — twelve reads, one
insert, one update, one delete — address the same unqualified table name. Not one
uses a cross-database or cross-server name, a pass-through query, a linked
server, a synonym, or Access's own syntax for reaching into a second database
file. The one dynamically assembled statement was checked and resolves to the
same table, so nothing is hidden from the inventory by runtime string building.

**The database file's own contents.** Read directly, the file contains one user
table and nothing else of substance: no stored procedures, no views, no saved
queries, no data macros or trigger equivalents, no embedded code modules, and no
user-defined relationships. There is therefore no database-resident logic through
which a second consumer could be coupled in. Both of the earlier database passes
independently recorded the table as shared with no other applications.

**The integration surface.** There isn't one. No web endpoints, no APIs, no
message queues, no scheduled jobs, no batch entry point, no file import or
export, no email, no network file paths. The only outbound network call in the
entire application opens a document URL in the user's browser. So there is no
channel through which another system could reach this data even if it wanted to.

Write ownership is consequently already singular and needs no resolution — the
usual hard part of decomposing a shared database simply does not arise. Within
the application, inserts, updates and deletes come from three different screens,
but those are modules of one program, not independent writers.

## The one thing this cannot prove

A file-based database keeps no record of who opens it. There is no server, so
there is no audit trail. A person or a tool opening `studentDB.accdb` directly in
Microsoft Access would bypass the application entirely and leave no trace that
any amount of code analysis could find.

This is the single material gap behind the conclusion above, and it is closeable
only by asking the business owner whether anyone does that. It is carried as the
first review ask. The same point cuts the other way too: the one piece of
positive evidence we do have — a lock file left behind in version control — names
a single workstation and the default database account, so the only session ever
observed holding the file open was the original developer's own.

Two related exposures are worth separating from the sharing question, because they
are real but are not other applications using the data. First, the database file
and its lock file are committed to a **public** code repository, so every clone is
an uncontrolled copy of the student records outside any access control, and the
repository's history retains it even if it were deleted today. Second, the
application permits multiple instances to run at once, so if the file were ever
placed on a shared network drive, several workstations would contend for it under
file-level locking with no transactions anywhere in the code. Whether that ever
happened is unverified.

## What actually blocks a migration

Not the decomposition — the data. Seven risks are ranked in the JSON artifact;
three of them are the ones that matter.

The **source of record is ambiguous**. The hard-coded database path points at a
three-deep nested folder on the original developer's D: drive, which exists on no
machine and does not match where the file actually sits in the delivered code. So
the copy we have has no code that opens it, and the copy the running application
uses is somewhere we have not seen — with no deployment step, copy script or
reconciliation job anywhere in the source to bridge the two. The copy we do have
is additionally suspect: Access only leaves its lock file behind when a database
is copied while still open, so it may be an incomplete snapshot.

The **schema is not readable yet**. Column names were recovered, but the declared
data types, lengths, whether fields can be empty, and whether the roll number is
enforced as unique all sit in binary structures that the available tooling could
not resolve. The application is no help: strict typing is switched off and every
value is passed through as text, so even date of birth may be stored as a string.
Critically, the two earlier passes disagree on whether a record key exists at all
— one reports a primary key on roll number, the other reports none established.
Every single-row read, update and delete selects by roll number while the insert
path performs no duplicate check, so uniqueness is assumed by the code and may be
enforced nowhere. One query against a live database engine settles all of this,
and it must happen before any replacement schema is designed.

There is also **nothing to verify a migration against**. The table carries no
created or modified timestamp, no user stamp and no row version; the application
has no login, so no change can be attributed to anyone; deletion is immediate and
physical; and the row count was never measured. A baseline has to be built from a
confirmed extract, because the legacy system holds no history to reconstruct one
from.

Three lower-severity items round out the list: the file retains a superseded
column layout from an earlier revision (two dead columns sitting where course and
year of admission now live), column name capitalisation differs between the
database and every line of code that reads it — harmless on Access, a runtime
failure on a case-sensitive target — and the student records include names, a
parent's name, two phone numbers and a date of birth, stored unencrypted with no
authentication over them.

## Reading the cluster list correctly

One caution for anyone consuming the structured artifact. Its cluster list has one
entry, because the application does have a persistent store — **not** because that
store is shared. The entry names exactly one participating application and one
write owner, and records coupling severity as none. Treating a non-empty cluster
list as evidence of cross-application coupling, or deriving a scheduling
constraint from it, would be a false positive. The same caution applies to the
database row this eventually projects into.

## Caveats on the inputs

The dispatch named the structural analysis and the database schema summary as
required inputs but staged neither; both were read from the earlier passes' own
outputs instead, and the findings here were corroborated first-hand against the
source rather than inherited.

The earlier artifacts also **disagree with each other** on several details, and
those conflicts are left visible rather than quietly resolved: the logical
database name, the file size, whether a primary key exists, how severe the SQL
injection findings are, how many statements are unparameterised, whether the
column types are known, and how many dashboard aggregates there are. None of these
changes the sharing verdict — all are internal to a single-application,
single-table store — but none should be treated as settled either.

No wave had been assigned when this ran, and no portfolio-wide map of shared
databases existed to compare against, because Discovery runs before wave planning.
The wave field therefore carries an explicit placeholder rather than a plausible
-looking wave number, and the portfolio view was deliberately not re-derived here.

Finally, the repository working tree contains scaffolding that is not part of the
application, two pieces of which are actively misleading for this analysis
specifically: a generic Oracle/SQL Server/DB2 stored-procedure inventory template,
and this very skill's own test fixture describing a fictitious shared customer
database spread across two invented applications. Neither describes this
application and neither was used. Their presence inside a customer source tree is
exactly how a later pass could "detect" a shared SQL Server cluster in a
VB.NET-and-Access desktop program; it is worth fixing at the staging layer.

## Scope discrepancy

The governing profile for this task is declared as `faa`, and that declaration
governs how this pass ran. Nothing in the application supports it. This is a small
single-developer Windows desktop tool for managing college student records —
courses BCA, MCA and IIMCA, admission years 2019 to 2023 — published under an
open-source licence on a public code-sharing site, with no aviation, air-traffic,
certification or safety content of any kind.

Three earlier Discovery passes raised the same mismatch independently. No
alternative profile was adopted here and no programme-specific shared-database
policy was applied; upstream analysis separately records that the profile's own
technology mapping defines no modernization target for this application's stack,
so no profile-driven policy would have applied in any case. The engagement owner
should settle the application-to-profile assignment before any
programme-specific gating consumes this artifact.

---

The full cluster inventory, the cross-application sharing counts, the seven ranked
decomposition risks with their mitigations, and the six review asks are in
`shared-db-analysis.json`. The decomposition approach built on this topology is in
`decomposition-strategy.json`, with its narrative in `decomposition-strategy.md`.
