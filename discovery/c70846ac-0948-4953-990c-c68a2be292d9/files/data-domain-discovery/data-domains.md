# Data Domain Boundaries — Student Management System (VB.NET)

**Application:** `c70846ac-0948-4953-990c-c68a2be292d9` · **Governing profile:** `faa` ·
**Grain:** single-application Discovery · **Machine-readable model:** `data-domains.json`

---

## Read this first: the scale

The entire data surface of this application is **one table, ten columns, two live
rows, and 461 hand-written lines of logic**. There is no second table, no view, no
stored procedure, no trigger and no foreign key — those are measured zeros from a
direct parse of the database file, not unfilled fields.

That matters for how the boundaries below should be read. Three domains across ten
columns is not an argument that this application should be split into three
services. It is a target-state *logical* model, drawn so that the governance gaps
inside that single row become visible to the people who have to design the
replacement schema. Nothing in this document argues for any particular
modernization disposition.

A physical-table-per-domain reading would have emitted one trivial domain and told
you nothing. So the boundaries were drawn at the level of the **logical entities
the code actually manipulates** — eight of them, recovered from the SQL statements,
the dropdown value lists, and the dashboard aggregates.

---

## The three domains

### 1. Student Identity and Contact — eight of the ten columns

Owns the person: roll number, given and family name, gender, date of birth, two
telephone numbers, and the father's name. This is where all of the directly
identifying personal data lives, and it is the application's aggregate root.

Three heuristics agree on keeping these together and they agree strongly. Every one
of these columns is written by a single `INSERT`, rewritten by a single `UPDATE`,
destroyed by a single physical `DELETE`, and has the same (absent) owner. No
transaction, query or lifecycle anywhere in the application ever touches a subset of
them independently.

Two structures inside the domain are worth a reviewer's attention:

- **The identifier is write-once by accident, not by design.** The `UPDATE`
  statement rewrites nine columns and uses the roll number only as its `WHERE`
  predicate, so the key is never modified. That is the one genuine mutation-profile
  split in the whole schema. But the key itself does not hold: it is declared as
  255-character text that permits the empty string, and nothing checks for
  duplicates on insert. Two students can share a roll number, in which case the
  editor binds the first match while update and delete silently hit *all* of them.
  This is the most severe defect carried forward.
- **The father's name is personal data about someone who is not the record
  subject.** It sits inside the student's row with no identity of its own, no
  consent basis and no independent erasure path. A separate related-party domain was
  genuinely defensible on security grounds and was rejected as over-engineering at
  one column — but the obligation is recorded explicitly rather than absorbed
  silently, and promoting it later is cheap because the column is isolated.

### 2. Student Enrolment — the remaining two columns

Owns the academic placement: which programme the student is admitted to, and in
which intake year.

This is the artifact's **weakest boundary** and the one put to you as a decision.
The case for splitting it out is specific: these two columns are the sole read-set
of eight of the ten dashboard figures, they are never touched by the search path,
and the inherited data-flow trace classified them differently from every other
column in the same row — the only classification line any upstream pass drew inside
this table. Conceptually they describe a *relationship* between a person and a
programme, with a cardinality the single-table schema simply cannot express.

The case against is that they are written by the same two statements as everything
in domain 1 and share its lifecycle and its absent owner. The reason that
counter-argument did not win is that **with exactly one table, "changes together"
cannot discriminate between any two columns** — it is an artifact of the table
shape, not evidence about the business — so it should not outvote heuristics that
can discriminate. That reasoning is a judgment, not a measurement, which is why it
is yours to settle.

Whichever way you decide, one question has to be answered before the target schema
is drawn: **may a student hold more than one enrolment?** The legacy schema pins it
to exactly one, but only because one table cannot say anything else. No business
rule anywhere states the constraint.

### 3. Academic Reference Data — no columns at all, and that is the finding

Owns the three closed code lists the student record depends on: programme codes
(BCA, MCA, IIMCA), gender codes (Male, Female, Other), and admissible intake years
(2019 through 2023).

This domain deliberately owns zero physical columns. The distinction is strict and
no column is assigned twice: the *column* holding a student's course belongs to
domain 2; the *list of admissible course values* belongs here.

It is carved out because leaving these as column constraints would bury the single
most consequential thing in this artifact: **these three code lists have no system
of record anywhere.** They exist only as duplicated literals in two designer files
and in the dashboard's SQL. The database enforces none of them — no validation
rule, no lookup, no check. And two of the three are already in active contradiction
with the code that reads them:

- The capture form offers three genders; **the dashboard counts only two.** A
  student recorded as "Other" is stored, is listed in the grid, and is counted in no
  tile — so the gender figures cannot sum to the population, and no total is
  displayed that would let anyone notice.
- The intake-year list stops at 2023, and the dashboard derives its five year
  buckets from a baseline hardcoded to 2023. **No intake after 2023 can be
  captured, and every intake-year figure shown to users has been wrong since
  1 January 2024.**

This is not theoretical. Deleted rows recovered from the database file carry course
values of `2` and `3` and intake-year values of `A` and `B` — the gap has already
been exercised with junk data.

---

## What crosses a boundary

Four cross-domain references were recorded. Three are ordinary: enrolment points at
its student, and both domains must resolve their coded values against the reference
lists.

The fourth is the real one. **The dashboard's population statistics is this
application's one genuine data product.** Its ten `COUNT(*)` aggregates read gender
from domain 1 and programme and intake year from domain 2, which makes it the single
access pattern that genuinely spans two domains. It is modelled as a read-only
product consuming published interfaces from both, rather than as a fourth domain —
it owns no entity and persists no byte, so promoting it would have forced a column
to be owned twice.

That decision also settled the one real contest over a column. Gender is read by
exactly the same aggregate pass as programme and intake year, so a mechanical
reading of "queried together" would score it into the enrolment cluster. It stays
with the person, because the dashboard groups those three only insofar as all three
are rendered as tiles — and letting a tile layout draw a business data boundary is
precisely the failure this method is meant to avoid. The dashboard is a *consumer*,
not an owner.

---

## The constraint that outranks every boundary here

**These three domains are logically separable and physically indivisible.**

All three compile into one executable, read one Microsoft Access file, and transact
through one process-wide database connection that four modules open, one module
closes mid-session, and nobody disposes. No statement anywhere runs in a
transaction.

Until that shared connection is replaced with a connection-per-operation seam, no
domain here can be extracted, retargeted or independently deployed. Everything
above is a target-state design, not a description of a separable present state.

Three further constraints compound it: the database is bound by a hardcoded absolute
path on the original author's `D:` drive that does not match where the file actually
ships, so a clean clone cannot reach the data at all; the engine is a file-based
Access database behind a 32-bit out-of-support provider that cannot be rehosted; and
there is no test, no pipeline and no working debug build, so no boundary here can be
verified by regression against current behaviour.

---

## Boundaries that were considered and rejected

Recorded so a later reviewer does not have to rediscover them: a separate
related-party domain for the father's name (rejected — one column); a reporting or
statistics domain (rejected — owns no entity, and promoting it would double-assign a
column); and folding the code lists back into column constraints (rejected — it
would hide an active governance gap that has already produced wrong figures and junk
data).

---

## What this artifact does not claim

It does not claim a disposition, a target service, a business owner, a safety tier,
or a PII classification ruling. Two fields the output contract requires —
`target_service_id` and `relationship` — are **placeholders**, because no target
plan exists at this grain and neither value was derivable. `target_service_id` is
emitted as the literal `unassigned` rather than a plausible-looking service number,
specifically so the gap fails visibly instead of being trusted and routed on.

Domain ownership is recorded as unassigned on all three domains. There is no
organisational signal to read: the application has no authentication, no user
concept, no roles, and the table has no user-stamp column, so not even an implicit
custodian can be recovered. The fifth boundary heuristic — same business owner —
contributed nothing to these boundaries, which means they rest on four heuristics
rather than five.

---

## Two things to route onward, independently of modernization

**Deleting a student does not erase them.** The delete path issues a physical SQL
delete with no tombstone and no audit entry, and because nothing compacts the file,
six deleted records remain fully readable in page slack with all ten field values
intact — names, both telephone numbers, gender, date of birth. In this particular
file those rows are keyboard-mash test data, so nothing is exposed today; the
finding is the mechanism, which would apply unchanged to real records. Combined with
the complete absence of audit columns, no change to any student record can be
attributed or reconstructed, and whatever history mattered is already gone.

**The application does not look like it belongs to this engagement.** The governing
profile is `faa` and has been honoured here — policy was read only from that
profile, and no alternative has been adopted or restated as fact. But the domains
derived above are students, guardians, course enrolments and academic code lists.
There is no aviation, air-traffic, certification or NAS data anywhere in ten columns
across one table. Two earlier Discovery passes raised the same mismatch
independently and it remains open, so it is escalated here as a scope decision for
the engagement owner rather than carried forward as a fourth open question. If the
answer is that the application is out of scope, every boundary in this document is
moot.

---

## Method, briefly

No prior data-domain model existed for this application, so nothing was refined —
the five boundary heuristics were applied from first principles to the logical
entities recovered from source, then cross-checked against the parsed database. All
five hand-written VB files were read in full first-hand rather than taken on trust,
so every claim above traces to the statement that writes or reads the column in
question.

The analysis was deliberately **not** fanned out to sub-agents: with three domain
candidates, one application and ten columns, it sits below every fan-out threshold
on every count, and the work that actually mattered — arbitrating gender, the
father's name, and the code lists — is synthesis that cannot be delegated.

Three upstream artifacts disagreed on load-bearing facts about the same table: the
existence of a primary key, the declared column types, and the row count. Each
conflict is resolved explicitly in the JSON with the losing claim named, so the
choice can be audited rather than taken on faith. One of those conflicts turned out
to be the defect itself — the telephone columns are declared as four-byte integers
while the application binds text into them, which means a valid ten-digit mobile
number cannot be stored at all.

Finally, a staging note: the inputs this step declares as required were not present
in its own staged input directory and were read from the sibling step's output
directory in the same workspace. Nothing was missing, only unstaged. Separately,
four untracked directories of tool scaffolding are sitting inside the customer
source checkout, including a QA fixture for this very skill describing a fictitious
application; none of it was treated as evidence.

---

*Full entity-to-domain assignment matrix, the five arbitration decisions, the seven
carried-forward boundary violations, and all evidence citations are in
`data-domains.json`.*
