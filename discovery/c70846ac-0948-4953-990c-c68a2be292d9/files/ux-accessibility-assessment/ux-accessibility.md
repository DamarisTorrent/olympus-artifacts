# UX & Accessibility Assessment — Student Management System (VB.NET)

**Application ID:** `c70846ac-0948-4953-990c-c68a2be292d9`
**Assessment date:** 2026-10-02
**Discovery pass:** 4 — UX & Accessibility Assessor, composed with the `accessibility-checker` sub-skill

---

## ⚠️ Governing-profile discrepancy (read this first)

The governing client profile declared for this task is **`faa`** (FAA legacy-modernization
program — NAS safety, air traffic, pilot certification). This application's source, its
README, its GPL license, its single-commit public GitHub history, and its author-credited
academic project report describe a **single-developer VB.NET WinForms student-records desktop
tool**, with no aviation, NAS, air-traffic, certification, or FAA-adjacent content anywhere in
the tree.

This is not a new finding — the Pass 0 catalog, the Pass 1 structural-analysis, and the
identity-landscape-analyzer each independently raised the same mismatch. This assessment
**corroborates it from the UX/accessibility angle and does not resolve it**: personas and
accessibility findings below are built strictly from this application's own evidence. The
FAA profile's accessibility-checker reference material (contrast guidance for operational
dashboards) was used only for its generic methodology, never as a claim that this is an FAA
system. **The engagement owner must resolve this before any FAA-specific gating — safety
tiering, NAS impact assessment, or Rationalization's `user_experience_readiness` scoring —
consumes this artifact.**

---

## 1. UI surface inventory

A standalone Windows desktop WinForms application (.NET Framework 4.8, single x86 EXE,
manually installed per workstation). No web layer, no HTTP endpoint, no API, no green-screen
or CLI surface — the Pass 1 structural map confirmed this via a full-tree, no-fan-out read
(2,787 LOC total, 1 build project, 1 database table — three independent "do not fan out"
thresholds).

| Surface | Screens | Role |
|---|---|---|
| `form1-dashboard` | 1 | Startup form, navigation shell, child-form host, **and** the only statistics/reporting view (10 COUNT(\*) aggregate tiles). 1,211-line Designer file, 77 controls — the largest and most structurally overloaded surface in the app. |
| `insert-form` | 1 | New-student entry: 10 fields, parameterized INSERT, no validation. |
| `edit-form` | 1 | Existing-student edit, keyed by roll number; the one form with a non-default constructor. |
| `view-form` | 1 | Grid of all students (DataGridView, `AutoGenerateColumns=True`), free-text search (the app's one SQL-injection point), Delete, and the launch point for Edit. |

One additional human-facing interface recorded upstream — an outbound "Project Report" button
that shells out to a hardcoded public GitHub URL via `Process.Start` — is **not** an
application-rendered UI surface and is excluded from the inventory and from the accessibility
audit's scope.

## 2. Personas and adoption baseline

**One persona was found, and only one `review_asks` entry accompanies it** — a `verify` ask,
because this is a genuine inference from code structure that only a stakeholder can confirm
or refute, not something this pass could resolve on its own:

> **Student-Records Operator (sole user class)** — no role or permission model exists anywhere
> in source. `AuthenticationMode.Windows` is declared but `My.User` is never read by any form;
> there is no login screen, no users/credentials table, and no role or audit column on the
> single `students` table. All four screens are reachable by anyone who launches the EXE, with
> full CRUD over all student PII. Estimated headcount: **unknown** — no CMDB export, org chart,
> or usage figure exists for this application anywhere in the onboarding package.

### Adoption baseline — instrumentation gap, not a measured zero

No telemetry source exists for this application: no logging framework, no analytics call, no
usage-tracking table, and no audit columns on its one table. Per the methodology's explicit
rule, this is reported as **"unmeasured, instrumentation gap"** for every one of the three
required adoption metrics (active-user count, feature-usage frequency, session-duration
distribution) — **not** as "zero usage observed." This assessment makes no claim, measured or
inferred, about whether the application has ever run outside its original author's development
machine.

### Training and documentation state

No help pages, tooltips, user guide, or LMS record exist anywhere. The only user-facing
documents are `README.md` (a developer-oriented feature list, not task instructions) and
`Siddharth Jain Project Report.pdf` (868 KB, **not parsed** by this pass or any prior Discovery
pass — its content, and whether it carries any training material, is an open evidence gap).
Both are effectively undated: the repository's entire history is one git commit, so neither
document has had the opportunity to go stale relative to a changing application. Training
completion is **unmeasured** — there is no account concept to attach a completion record to,
and per methodology this is tracked separately from (and not inferred from) the equally-absent
login signal.

## 3. Accessibility findings (composed with `accessibility-checker`)

The `accessibility-checker` skill's normal workflow — `axe-core` against a built, hosted
URL — **does not apply**: this is a desktop WinForms app with no DOM, no URL, and no buildable
artifact in this sandbox. The checker adapted its methodology to a **manual, source-code-based
audit** of all four `*.Designer.vb` files (control-level `AccessibleName`,
`AccessibleDescription`, `TabIndex`, `BackColor`/`ForeColor` properties), cross-referenced
against the application's three screenshots. This is a lower-confidence method than even a
standard automated DOM scan (which itself catches only ~30–40% of issues), and the checker
flagged exactly that in its own output.

**Verdict: `FAIL`** — 1 critical, 2 serious, 4 moderate, 2 minor findings (9 total). A critical
violation forces the fail verdict under the checker's own schema invariant.

| ID | WCAG | Level | Surface | Finding |
|---|---|---|---|---|
| A11Y-001 | 4.1.2 | A | `form1-dashboard` (all 4 forms) | **Critical.** Zero `AccessibleName`/`AccessibleDescription` across all 137 controls in the application — a measured zero across a full-file read, corroborating Pass 1. The only non-visual access mechanism this app has is entirely absent. |
| A11Y-002 | 1.3.1 | A | `view-form` | Grid column headers are raw DB field names (`FName`, `YOA`, …) — `AutoGenerateColumns=True` with no `HeaderText` override. |
| A11Y-003 | 1.4.1 | A | `form1-dashboard` | The five "Year Wise" tiles share the identical caption "Year Students"; only an unlabelled, color-differentiated numeral image distinguishes them. |
| A11Y-004 | 2.4.3 | A | `form1-dashboard` | Duplicate `TabIndex` values on the primary nav rail (two pairs) make keyboard focus order ambiguous. |
| A11Y-005 | 1.3.2 | A | `form1-dashboard` | Two leftover duplicate dashboard panels overlap real tiles and sit in the tab order with no sensible content. |
| A11Y-006 | 1.4.3 | AA | `form1-dashboard` | The "Male Students" tile and the grid background use theme-dependent `SystemColors.ActiveCaption` rather than a fixed, pre-validated color — contrast is not fixed or verifiable at design time. Qualitative flag; no pixel-measured ratio taken. |
| A11Y-007 | 3.3.2 | A | `insert-form` | No `MaxLength` and no field-level validation on any of the 10 data-entry fields; errors surface as one generic `MsgBox`, not tied to a field. |
| A11Y-008 | 2.1.1 | A | `form1-dashboard` | No keyboard mnemonics (`&`) on any button in any form. |
| A11Y-009 | 2.4.6 | AA | `form1-dashboard` | Generic internal control names (`Label1`…`Label27`) rarely leak to users, since visible `.Text` captions are mostly descriptive — low priority relative to A11Y-001. |

Full per-finding evidence (file:line citations, remediation code, and the checker's complete
method note) is in `accessibility-checker/accessibility-audit.json`, written verbatim into
`accessibility_findings` with no severity re-classification, per the skill's constraint that
compliance determinations are the checker's alone.

**What this audit could not verify** (flagged for manual follow-up): live screen-reader
behavior (NVDA/JAWS/Narrator) against a compiled build; pixel-measured contrast ratios; and
whether the duplicate-TabIndex/overlapping-panel issues produce an actual keyboard trap in live
interaction versus merely an inefficient tab order.

## 4. What this baseline is for

Per the skill's purpose, this artifact is the pre-cutover anchor the `adoption-analytics`
Deployment sibling will compare against. Given the instrumentation gaps above, that comparison
will have **no baseline numbers to compare to** on usage — only the accessibility FAIL verdict
and the single-persona model are measurable anchors today. If this application proceeds toward
modernization, retrofitting basic usage telemetry before cutover (even a simple login/action
log) would be the single highest-leverage fix for making any future adoption comparison
meaningful at all.

## 5. Open questions carried into Rationalization

1. Governing-profile mismatch (above) — unresolved, engagement owner's to adjudicate.
2. `Siddharth Jain Project Report.pdf` unparsed by every Discovery pass to date — unknown
   whether it contains user-facing training content.
3. No live assistive-technology testing performed — all 9 findings rest on source + screenshot
   review only.
4. No CMDB, business owner, or operational-criticality classification exists, which is the root
   cause of every adoption/training instrumentation gap above.
5. `safety_tier` is null upstream and is explicitly a stakeholder decision, not a code
   inference. This assessment recommends Rationalization treat the accessibility FAIL as
   tier-independent — a critical WCAG violation fails at any tier — rather than waiting on tier
   resolution to act on it.
