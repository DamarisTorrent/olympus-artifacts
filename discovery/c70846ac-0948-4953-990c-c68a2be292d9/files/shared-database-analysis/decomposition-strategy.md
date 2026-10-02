# Decomposition Strategy — Student Management System (VB.NET)

**Target:** `c70846ac-0948-4953-990c-c68a2be292d9` · **Service:** `system` ·
**Relationship:** `rearchitect` *(provisional — see below)* ·
**Pattern:** database-per-service ·
**Structured artifact:** `decomposition-strategy.json`

## Read this first: the target binding is provisional

This skill is meant to work from an approved target plan entry that tells it what
is being built and from which source applications. No such entry existed when
this ran — Discovery runs before the architecture target plan is produced. The
four binding fields in the structured artifact were therefore **derived, not
received**, and none of them is an approved decision:

- the target is recorded as the source application itself, standing in for its own
  target at this stage;
- the service identifier is `system`, reflecting that no service decomposition has
  been established for what is a single-assembly program;
- the relationship is recorded as *rearchitect* because that is the closest fit on
  the technical evidence, **not** because anyone has decided to rebuild it.

The decision itself is the first review ask, and it is genuinely open. Treat these
fields as placeholders and re-bind the artifact when a real target plan exists.

## The decision, and why it was easy

Because this application's database is used by nothing else, there is no
entanglement to unpick. The approach is the decisive one: the replacement system
gets its own dedicated database and becomes its sole owner, the student data is
migrated in a single scheduled switchover, and the old Access file is retired
immediately afterwards with nothing left reading it.

The decision tree stopped at its first option. A dedicated database per service is
the default wherever the participating applications can be switched over together
— and here that condition is met trivially, because there is only one application.
Ownership of the data is already held by a single writer, so there is nothing to
negotiate. The behaviour to verify after the switchover is one table's create,
read, update, delete and search, plus five summary tiles on a dashboard: all of it
local and synchronous, with no asynchronous or integration behaviour to reproduce.

## Why the two slower options were rejected

Both alternatives exist to manage databases shared between several applications.
Neither has anything to work on here, and each would leave behind a component that
itself has to be removed later.

**Gradually redirecting traffic over several rounds** is an exception requiring one
of three specific justifications, and none holds. There are no applications that
cannot be switched over together, because there is only one and no organisational
or compliance boundary splits it. There is no regulatory obligation to run old and
new side by side. And the switchover window is not hard to find: this is a
manually installed desktop program with no server, no scheduler, no service-level
commitment and — on the evidence of the lock file — a single user, so the window is
whenever the operator is not using it. The justification field in the structured
artifact is deliberately left empty rather than filled with a non-reason; its
emptiness is the finding.

**Putting a temporary service layer in front of the old database** is reserved for
the genuinely hard case of four or more applications sharing a database across
different migration waves. There is one application and no cross-wave hazard.
Introducing a bridging layer in front of a single-table, single-user file database
would be strictly worse than the thing it replaces, and it would need a firm
retirement date to avoid becoming permanent.

No temporary layer and no dual-write period are proposed. The target shape is
sole ownership of a dedicated store, which is an end-state shape, so there is no
retirement date to track and none is recorded. That absence is deliberate.

**Keeping the current platform** was also considered and is not viable. The
Microsoft Access database engine went out of support in October 2017. Its driver
is a separately installed 32-bit component that pins the build to 32-bit Windows
and will not run on a 64-bit-only or non-Windows host. And a file-based database
mediates concurrency through a lock file with no transactions anywhere in the
code, which does not survive a multi-user deployment.

## Where the real work is

Not in the decomposition — in the data. The decomposition is degenerate in the
best way: there is nothing coupled to separate, so the only substantive work is
migrating one small table and proving the migration was faithful. Three
prerequisites gate that, in order.

**Confirm which copy of the database is authoritative.** The hard-coded database
path points at a three-deep nested folder on the original developer's D: drive,
which exists on no machine and does not match where the file sits in the delivered
code. The copy we have therefore has no code that opens it, and the copy the
running application uses is somewhere we have not seen, with no deployment step or
reconciliation job anywhere in the source to bridge them. The copy we do have is
additionally suspect: Access only leaves its lock file behind when a database is
copied while still open, so it may be an incomplete snapshot. Compact-and-repair
it and take a row count before trusting it.

**Read the real schema through a database engine.** Column names are known; their
declared types, lengths and nullability are not, and the application cannot be
used to infer them because strict typing is off and every value is passed through
as text. The decision-critical unknown is the roll number: every single-row read,
update and delete selects by it, but the insert path performs no duplicate check,
and the two earlier passes disagree on whether a primary key is even declared. If
duplicates exist, de-duplication has to precede migration or records will be lost
or merged. The same sitting also settles whether any rows still carry the
superseded column layout the file retains, and what the actual row count is.

**Build a baseline to verify against.** The table carries no created or modified
timestamp, no user stamp and no row version; the application has no login, so no
change can be attributed; deletion is immediate and physical; and the row count
was never measured. There is no history to reconstruct a baseline from, so one has
to be built from a confirmed extract plus a behavioural specification derived from
the recorded screen behaviour. Replay verification is the premise of the decisive
path, and it currently has nothing to replay against.

For rollback, hold the confirmed legacy file read-only and unmodified after
switchover. That is cheap here — one small table — and it is the only rollback
source available, precisely because the legacy system records no change history of
its own.

## Data-model decisions deliberately deferred

Three things are left to the target design rather than inherited from the legacy
shape.

Gender, course and year of admission are closed value lists enforced only in two
user-interface layout files. They disagree with the rest of the system: "Other" is
storable as a gender but invisible in every dashboard statistic, and the year list
runs 2019 to 2023 against a hard-coded current year of 2023, so it cannot express
any later intake. These belong in reference tables with real constraints in the
target — which is the one place the target schema legitimately gains relationships
the legacy single-table design has none of.

Conversely, **do not** retrofit foreign keys onto the legacy shape. The absence of
foreign keys there is correct by construction: with one table, there is nothing to
relate. Both earlier passes flagged this explicitly so that "no foreign keys" is
not misread as undiscovered coupling.

Capitalisation needs deciding once, deliberately. The database declares names in
one convention and every line of code that reads it uses another. Access does not
care; a case-sensitive target will, and the failures will appear at runtime rather
than at build time, in exactly the places resolved dynamically.

Finally, pin the migration to the ten live columns. The file retains an earlier
table definition carrying two dead columns in the positions where course and year
of admission now live, so a generic catalog read could pick up the wrong shape.

## Risks that do not change the strategy

An **undetectable consumer of the old file** is possible in principle: a file-based
database keeps no audit trail, so someone opening it directly in Access bypasses
the application entirely and leaves no trace. One question to the business owner
closes this, and it is carried on the companion shared-database artifact. Note
that even if such a consumer were found, it would be a reader — servable from the
target store or a published read model, not a reason to adopt a bridging layer.

**Silent data change at migration** is likely around dates. Access stores
date-and-time values as a serial number with no timezone and permits a time
component on what is semantically a date-only field; date of birth is written as a
locale-formatted display string and read back with a locale-free parse, so
day-and-month transposition is possible across workstations and may already be
present in the stored data. Map it to a date type deliberately, record the dropped
time component as an intended change, and inspect the stored values rather than
assuming the legacy data is clean.

**The student data is currently exposed.** Names, a parent's name, two phone
numbers, a date of birth and gender sit in an unencrypted, password-less file with
no authentication over the application, committed to a public code repository
whose history retains it. No decomposition choice fixes this; every copy of the
file must be handled as personal data, and the exposure needs escalating through
the engagement's data-protection route independently.

## Two omissions, both deliberate

**No co-wave constraints artifact was emitted.** The step normally produces one,
but this dispatch declared no schema for it, and writing a file against an unseen
schema risks a hard validation failure. The substantive answer is the meaningful
empty one: zero constraints, because this target participates in no
multi-application cluster and so constrains nobody.

**No consolidation breakdown was emitted.** The relationship is not a
consolidation and there is a single source application, so the per-source
absorption rules do not apply.

One caution for whoever consumes the projected database row: a shared-cluster row
will exist for this application even though the cluster is **not** shared — it has
one participating application and one write owner. The presence of a row must not
be read as cross-application coupling.

## The question upstream of all of this

Whether this application should be modernised at all is still open, and it
determines whether anything in this artifact matters. It delivers one capability —
student-record create, read, update, delete and search, plus five dashboard tiles
— in roughly 461 lines of hand-written logic; the other 2,326 of its 2,787 lines
are generated screen layout. No business owner, criticality rating, user
population or data volume was supplied at onboarding, and the earlier structural
analysis left the disposition explicitly open. Buying an off-the-shelf
student-records product, or simply retiring the application, are both credible
alternatives to rebuilding it.

The data-layer facts stand either way, which is why this artifact was produced:
whatever is decided, there is nothing shared to untangle, and the prerequisites
for moving the data are the same.

## Scope discrepancy

The governing profile for this task is declared as `faa` and governs how this pass
ran, but nothing in the application supports it — it is a college student-records
desktop tool with no aviation, air-traffic, certification or safety content. Three
earlier Discovery passes raised the same mismatch independently. No alternative
profile was adopted and no programme-specific decomposition policy was applied;
upstream analysis records that the profile's own technology mapping defines no
modernization target for this application's stack in any case. The engagement
owner should settle the application-to-profile assignment before
programme-specific gating consumes this artifact.

---

The full decision-tree trace, the cluster strategy with its deferred data-model
decisions, the seven risks with mitigations, the inputs consumed and deliberately
disregarded, and the five review asks are in `decomposition-strategy.json`. The
shared-database topology this strategy rests on is in `shared-db-analysis.json`,
with its narrative in `shared-db-analysis.md`.
