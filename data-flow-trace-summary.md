# Data Flow Trace — Summary

**Application:** Student Management System (VB.NET) · `c70846ac-0948-4953-990c-c68a2be292d9`
**Skill:** `legacy-data-flow-tracer` · **Artifact:** `data-flow-trace.json` (authoritative)
**Next:** `extraction` (Discovery Step 3 Pass 2), gate `G-DC`

---

## What this application is, data-wise

One table. Ten columns. One local Microsoft Access file. No HTTP surface, no scheduler, no
queue, no SFTP route, no file-drop pipeline — the entire ingress surface is an operator at a
keyboard on two WinForms. 2,787 LOC, ~83% of it Designer-generated; the real logic is ~461
lines across five hand-written files.

That makes this an unusually clean trace, and it means the findings below are not "legacy
sprawl" findings. They are concentrated, specific, and almost all fixable at a single site.

## Flows

| Flow | Element | Class | Stores | Boundary | Headline |
|---|---|---|---|---|---|
| DF-SMS-001 | `student_roll_number` | pii | 3 | system | De facto PK, no uniqueness constraint asserted anywhere |
| DF-SMS-002 | `student_name` (fname, lname) | pii | 3 | system | Only unparameterized query in the app searches on this |
| DF-SMS-003 | `father_name` | pii | 3 | system | Third-party PII, no notice/consent/purpose record |
| DF-SMS-004 | `student_mobile_numbers` | pii | 3 | system | Published contact list; no format validation at all |
| DF-SMS-005 | `date_of_birth` | pii | 3 | system | Stored as a locale-rendered **string**, not a date |
| DF-SMS-006 | `gender` | pii | 3 | system | Dashboard never counts the third value the form offers |
| DF-SMS-007 | `course` + `yoa` | sensitive | 3 | system | Cannot record any cohort admitted after 2023 |
| DF-SMS-008 | `host_and_database_user_identity` | pii | 2 | system + **identity** | Provider lock file; the app's only access record |

28 transformations traced, **24 of them implicit** — runtime side effects, not business rules.
That ratio is the single most important number in this artifact: five-sixths of what happens to
this data is invisible in the source as written.

## The five things that matter

**1. The database is published. (CFF-001 — critical)**
`Flat Design/studentDB.accdb`, 802,816 bytes, is committed to a public Git repository.
`Form1.vb:156` hard-codes this repository's own public github.com URL, which is how we know it
is public; neither `.gitignore` nor `.gitattributes` excludes `*.accdb` or `*.laccdb`. Every
flow in this trace terminates in an egress that leaves the trust boundary and is retained
permanently in Git history — unreachable by the application's own `DELETE`. The committed
`studentDB.laccdb` additionally discloses the host name `SIDDHARTH-WIND` and the Jet account
`Admin`. **Remediate independently of any modernization work.**

**2. Date of birth is a locale-rendered string. (DF-SMS-005 — high)**
`dtpDOB.Text` is bound, not `dtpDOB.Value` — on both the insert (`InsertForm.vb:23`) and the
update (`EditForm.vb:62`) path. No `Format`/`CustomFormat` is set on the control on either form,
so it falls back to `DateTimePickerFormat.Long` and persists the OS locale's **long date
string**. Read-back is `DateTime.Parse` with no `IFormatProvider` (`EditForm.vb:30`), re-parsing
under the *reading* host's culture. Write on one locale, edit on another, and day and month
silently exchange. Each save re-encodes, so drift compounds rather than settling. Migration
cannot assume a single parseable format — profile the real column before writing a conversion.

**3. Edit round-trips silently damage adjacent fields. (CFF-009 — high)**
`EditForm.btnSave_Click` rewrites all nine mutable columns unconditionally, so every read-back
defect becomes a write defect. Opening a record to fix one field can damage three others:
`DBNull` → `String.Empty` on the text columns; `SelectedItem` lookups that fail silently against
hard-coded `Items` lists; DOB re-encoded through the editing host's locale. **This is the
highest-value target for Pass 2 business-rule extraction.**

**4. Nobody is accountable for any write. (CFF-003 — high)**
No login form, no user or role table, no owner column, no owner filter, no audit log — a grep
across all hand-written `.vb` for auth and logging constructs returns nothing. The connection
string carries no credentials, so every operation by every operator is the shared Jet `Admin`
account. The actor dimension of every flow in this trace is empty, and no evidence exists from
which to reconstruct it.

**5. The dashboard reconciles with nothing. (CFF-007 — medium)**
Gender counters omit `Other`; course counters enumerate three hard-coded codes; the five
academic-year buckets are anchored to a literal `currentYear = 2023` (`Form1.vb:59`) instead of
the system clock, so they have not advanced since the code was written. No query displays a
total row count, so none of the three dimensions can be checked and the shortfalls are invisible
to the operator. Treat every number on this screen as unverified.

## Two things the trace deliberately does *not* claim

**Access column types are unresolved, not assumed.** The `.accdb` is a binary ACE database;
column names are UTF-16LE and no interpreter or `strings(1)` was executable in this sandbox, so
no DDL and no row data could be recovered. Every write in the application is an untyped
`AddWithValue` bind against an undeclared column type, and the project compiles with
`OptionStrict Off`. The type-coercion findings in DF-SMS-001, -004, -005 and -007 are therefore
**unresolved rather than ruled out** — several resolve in *opposite* directions depending on
whether `rollno`, `yoa`, `mobno`, `altmobno` and `dob` are Text, Number or Date/Time.
→ **`legacy-database-archaeologist` must dump the `students` DDL before these can be closed or
any migration mapping written.** For the same reason, no claim is made about what rows the
committed database contains; at 802 KB it is larger than an empty ACE database, so it is treated
as potentially holding live student records until a row inspection proves otherwise.

**There is no reporting capability.** The dashboard's "Report" button does not generate a
report — `Form1.vb:155-158` calls `Process.Start` on a hard-coded github.com URL pointing at the
author's PDF. The only data exits in the entire application are the on-screen grid, the on-screen
dashboard counters, and the committed database file. Module design should not assume a report,
print, export, or email path exists to be migrated.

## Governing-profile discrepancy (CFF-008)

The governing profile for this task is declared as **`faa`** and that declaration governs. The
application's source, README and project report describe a generic student-records desktop tool
with no aviation, NAS, or FAA content; the staged catalog entry records the same mismatch in its
`open_questions`. Separately, `profiles/faa/` was not reachable from this sandbox, so
`profiles/faa/compliance.yaml` could not be consulted — **all `pii_classification` values were
assigned from the generic enum definitions in `references/pii-phi-tracking.md`** and must be
re-validated against the real profile rules before any compliance gate relies on them. The
engagement owner should confirm the application-to-profile assignment before FAA-specific gating
is applied to this application at all.

## Validation status — read this

`validate-data-flow-trace.js` in this directory implements the binding schema
(`schemas/discovery/data-flow-trace.schema.json`: `type`, `required`, `additionalProperties`,
`enum`, `pattern`, `minLength`, `minItems`, `minimum`) plus the skill's Quality Rules as
executable gate checks. **It could not be executed here** — this sandbox denies all interpreter
invocation (`python3` and `node` both refused beyond `node --version`). Run it at the gate:

```
node validate-data-flow-trace.js data-flow-trace.json
```

In its place the artifact was audited by exhaustive pattern extraction, which confirmed:

- every key name in the document is within the schema's allowed sets — no `additionalProperties`
  violations, and no key outside the declared `$schema`/`generated`/`methodology_notes` escape hatches;
- zero `null`, `"None"`, and `""` values anywhere (the stated hard-failure mode);
- every `pii_classification`, `interface` (both directions), `operation`, `store_type`,
  `severity` and `category` value is a legal member of its enum;
- all 8 `flow_id`s match `^DF-[A-Z0-9]+-[0-9]{3}$`, are unique, and every `flows_involved`
  reference resolves to a flow that exists;
- exactly 8 `source_of_truth: true` across 8 flows — **one per flow**, no split-brain;
- every flow carries ≥1 persistence point, ≥1 exit point, ≥1 transformation, a retention value
  on every persistence point, and ≥1 risk finding;
- every PII-classified flow that exits the trust boundary carries a ≥medium finding;
- `has_implicit_transformations` agrees with the `implicit` flags beneath it in all 8 flows, and
  every `implicit: true` step names the runtime behaviour that caused it.

The one check that genuinely requires execution is JSON well-formedness. Head and tail were read
back and the brace/comma structure verified by hand, but a parser should confirm it at the gate.
