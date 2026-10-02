# Capability Catalog — Student Management System (VB.NET)

**Application ID:** `c70846ac-0948-4953-990c-c68a2be292d9`
**Discovery skill:** `capability-extraction` (Discovery Step 3e)
**Governing client profile declared for this task:** `faa` — see **Finding 0** below before reading anything else in this document as FAA-domain fact.

---

## 0. Read this first: governing-profile discrepancy

The task context asserts `faa` as the authoritative governing client profile. **Nothing about this application
supports that scope.** It is a single-developer VB.NET WinForms desktop tool for managing student academic
records (name, course, year of admission, gender, contact numbers, date of birth) over a local Microsoft Access
file, GPL-licensed, with a public GitHub origin, one commit, and an author-credited project report. Both prior
Discovery passes independently flagged the same mismatch:

- Pass 0 (`application-catalog-entry.json`): *"this application's source, README, and project report describe a
  generic student-record-management desktop tool with no detectable aviation, NAS, or FAA business relevance."*
- Pass 1 (`structural-analysis.json`, Finding 0): *"Nothing in this application's source supports that scope... no
  aviation, NAS, air-traffic or certification artifact of any kind."*

This skill **does not adopt an alternative governing profile** and does not restate `faa` as settled fact about
this application's business ownership. The catalog below is written as a faithful extraction of what the
application *actually does*, bound only to the governed capability vocabulary available to this skill. **The
engagement owner must resolve this discrepancy before any FAA-specific gate** (safety tiering, NAS impact
assessment, compliance mapping, or Rationalization's consolidation of this system against real FAA
strategy-of-record systems) consumes the rows this artifact produces.

## 1. Input availability

| Input | Status | Notes |
|---|---|---|
| `application-catalog-entry.json` | available | Pass 0 output, read in full |
| `structural-analysis.json` | available | Pass 1 output, read in full (interface-inventory + database-schema-summary sections) |
| `data-domains.json` | **not available** | Required per the dispatch contract; the sibling `discovery-data-domain-discovery` task's work log showed 0/4 checklist items complete and its output directory was empty at execution time. This catalog proceeds without it — see open question below. |
| `interface-inventory` | available | Embedded as a section of `structural-analysis.json`, not a standalone file |
| Client-profile capability/system reference catalog (`faa` strategy-of-record identifiers) | **not available** | No such catalog was reachable from this skill's working directories; no `external_id` binding was attempted anywhere in this artifact |

## 2. Legacy system binding

**Name:** Student Management System (standalone VB.NET/Access application)
**External ID:** none — this application does not cleanly belong to, nor was it possible to check against, any
strategy-of-record system family. It is a bespoke, single-assembly desktop tool with no network, web, batch, or
integration surface.
**Role:** `primary` — the sole realization of this ad hoc "system."

**Rationale:** Structural Analysis independently confirmed a single build project, a single deployment surface,
one database table, and zero outbound integrations other than a dead hyperlink. There is no evidence anywhere in
the source, README, or project report connecting this application to any system family, FAA or otherwise.

## 3. Business domains

| Domain | Description |
|---|---|
| **Student Records Administration** | Internal administrative management of individual student academic and contact records plus basic population statistics. Corresponds to the Pass 0 catalog's free-text `business_domain` of `"Admin"` — itself a forced fit, since the application documents no actual business owner or sponsoring office. |

Only one domain was extracted. With no `data-domains.json` to cluster against and a single 10-column table backing
every screen in the application, there is no structural basis for splitting into additional domains.

## 4. Capabilities

### 4.1 `personnel-records-management` — confidence 0.60

**What it does:** Create, read, update, and delete operations on individual student records — roll number, name,
father's name, two contact numbers, gender, course, year of admission, and date of birth — all against the single
`students` table. Implemented across three WinForms screens (`InsertForm`, `EditForm`, `ViewForm`) with inline,
mostly-parameterized OleDb SQL and no data-access or service layer.

**Business domain:** Student Records Administration

**Evidence:**
- `structural-analysis.json:database-schema-summary.tables[students]`
- `structural-analysis.json:interface-inventory.interfaces[InsertForm — new student record entry]`
- `structural-analysis.json:interface-inventory.interfaces[EditForm — existing student record editor]`
- `structural-analysis.json:interface-inventory.interfaces[ViewForm — student record grid, search and delete]`

**Why confidence is 0.60, not higher:** The *existence* of this CRUD capability in the application is
unambiguous and directly evidenced — if this were a free-text label the confidence would be ~0.95. The discount is
because the governed capability vocabulary offers no entry for generic academic/student-records management, and
`personnel-records-management` is a proxy borrowed from an adjacent, FAA-oriented sense of "personnel." A
reviewer who maintains the vocabulary may want a better-fitting label.

### 4.2 `reporting-and-analytics` — confidence 0.75

**What it does:** Ten `COUNT(*)` aggregate tiles on the `Form1` dashboard, breaking the student population down
by gender (Male/Female), course (BCA/MCA/IIMCA), and five academic-year buckets computed from a hardcoded
`currentYear = 2023`. Read-only; derives entirely from the same single `students` table.

**Business domain:** Student Records Administration

**Evidence:**
- `structural-analysis.json:interface-inventory.interfaces[Form1 — dashboard, navigation shell and statistics view]`
- `structural-analysis.json:architecture.major_components[Form1 (dashboard shell / MDI-style host)]`

**Why confidence is 0.75:** Direct, well-evidenced capability and a reasonably good vocabulary fit (it genuinely
is a counts/dashboard reporting surface). Not higher because the underlying tiles are known-defective (year
baseline frozen at 2023; gender tiles exclude the "Other" value from the sum) per Structural Analysis §4 — the
capability's *existence* is solid, its *correctness* is not, and that distinction matters to anyone consuming this
confidence score downstream.

### Not modeled as capabilities

- **The "Report" button / GitHub PDF link.** Structural Analysis records that this control launches a hardcoded
  public GitHub URL in the default browser and generates nothing. It is not a reporting capability — it is a
  mislabeled, unimplemented one — and is excluded rather than fabricated.
- **The `studentDB.accdb` file.** Modeled as the persistence substrate underlying `personnel-records-management`
  (see `legacy_system`), not as a capability in its own right.

## 5. Open questions for the reviewer

1. **Governing-profile discrepancy** (see §0) — needs engagement-owner resolution before this catalog is used for
   any FAA-specific gate.
2. **`data-domains.json` was unavailable** at execution time (upstream task incomplete). This catalog was built
   from `application-catalog-entry.json` and `structural-analysis.json` alone. Recommend re-running this skill
   once that artifact exists, to confirm or refine the domain/capability split above — the persist layer's natural
   keys mean a clean re-run should land on the same rows rather than duplicate them, provided names are not changed.
3. **No `faa` strategy-of-record reference catalog was reachable**, so no `external_id` was set anywhere in this
   artifact (`legacy_system`, `business_domains[]`, `capabilities[]` all bind on name only for now).
4. **Vocabulary fit.** `personnel-records-management` is a borrowed label for student-records CRUD; there is no
   governed capability for generic academic-records administration. Flag to the vocabulary owner if more
   non-FAA/non-aviation applications are expected to flow through this pipeline.
