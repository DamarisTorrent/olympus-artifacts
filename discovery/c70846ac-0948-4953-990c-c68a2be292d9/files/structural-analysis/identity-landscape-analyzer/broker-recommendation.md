# Broker-Federation Recommendation

**Application:** `c70846ac-0948-4953-990c-c68a2be292d9` — Student Management System (VB.NET)
**Source skill:** `identity-landscape-analyzer`
**Governing client profile:** `faa` (authoritative per task declaration)
**Analyzed:** 2026-10-02
**Companion artifact:** `identity-landscape.json` → `broker_recommendation`

> **Scope.** This skill ran as a per-application Discovery augmentation (LD-10), so it
> saw exactly one application's identity model. Everything below is scoped to that
> application. Where a judgement would require portfolio-wide counts, it is marked as
> un-evaluable at this scope rather than asserted. A portfolio-level rollup remains a
> separate, future step.

> **Two reading cautions before acting on this document.**
>
> 1. `profiles/faa/` was **not readable** from this sandbox — it lies outside the
>    permitted working directories. The profile's IDP inventory, user-class taxonomy,
>    and risk-tier AAL floors could not be consulted. No concrete FAA IDP name appears
>    anywhere below; the gaps are left explicit rather than filled by guesswork.
> 2. The catalog's own open questions flag that this application shows **no detectable
>    aviation, NAS, or FAA business relevance**. The catalog does not claim a different
>    governing profile, so there is no conflict with the `faa` declaration — the
>    discrepancy is one of scope fit. Confirm the application belongs in the portfolio
>    before funding any of this.

---

## 1. Recommended Pattern

**Selected: `broker-staff-only`**

| Pattern | Verdict for this application |
|---|---|
| `broker-all` | Rejected at this scope — no public user class exists to front. |
| `broker-public-only` | Rejected — same reason; there is no public surface at all. |
| **`broker-staff-only`** | **Selected.** |
| `keep-separate` | Rejected — this *is* the status quo, and it is what the retire recommendations exist to dismantle. |

This application has exactly one user class: the local workstation operator, an
internal staff-equivalent class. The catalog records archetype `desktop` with no HTTP
listener, no API surface, and no network component, and source confirms it — there is no
listener, no federation code, and no second user population anywhere in the tree. With
no public class, `broker-all` and `broker-public-only` are ruled out on this
application's own evidence.

`keep-separate` deserves the explicit rejection rather than silence: keeping apps
separate is precisely the current state — ambient Windows trust plus a credential-less
data path — and neither half can be hardened in place.

**Portfolio caveat.** This is the per-application contribution to the pattern decision.
The portfolio-wide pattern must be set by the rollup, and may well land on `broker-all`
once public-facing applications are in view. Nothing here should be read as a portfolio
determination.

---

## 2. Broker Technology

**Recommended: Keycloak (current supported release) — *provisional, subject to profile confirmation*.**

Decision drivers:

- **License model:** open-source, avoiding a new commercial dependency for a single
  small application.
- **Protocol support required:** OIDC (authorization-code + PKCE) for the desktop
  client; SAML 2.0 and X.509 for the existing Windows directory.
- **Downstream consistency:** `keycloak-realm-designer` declares a dependency on this
  skill's output, so a Keycloak recommendation keeps the Discovery chain coherent.
- **Deployment target:** **not determined.** The profile's cloud/hosting target was not
  readable from this sandbox.

**Why provisional.** Beyond the unreadable profile, the catalog records that
`profiles/faa/technology.yaml` → `modernization_targets.dotnet` covers only
ASP.NET / C# / WCF and defines **no** target for a VB.NET WinForms + MS Access stack.
No profile-sanctioned platform target currently applies to this application. Ratify the
broker choice against the profile and the engagement's standing identity platform before
any build work.

---

## 3. Fronted IDPs

| IDP | User class | Protocol | AAL contribution |
|---|---|---|---|
| The Windows directory this app consumes ambiently today — **local SAM or AD domain, not determinable from source** | `local-workstation-operator` | SAML 2.0 or OIDC (to be decided once the directory type is confirmed) | Target **AAL2** minimum. Current contribution at the app boundary is **below-AAL1**. |

**Deliberately incomplete.** No further upstream IDP is named, because
`profiles/faa/technology.yaml` and `profiles/faa/config/identity-landscape-analyzer.yaml`
could not be read. Naming concrete FAA IDPs would be fabrication. **This table must be
completed from the `faa` profile before the broker design is acted on.**

Confirm the directory type first: the project references no `System.DirectoryServices`,
no domain name, and no LDAP or Kerberos configuration, so whether the principal is a
local machine account or a domain account is genuinely unknown from source. The answer
changes the federation protocol and the enrolment work.

---

## 4. Apps in Scope

| Wave | Apps | Target IDP via broker |
|---|---|---|
| 1 | `c70846ac-0948-4953-990c-c68a2be292d9` | Broker-fronted staff IDP, **cut over together with the data-tier migration** |

There is no wave 2 at this scope. The two retirements are a single cutover — see
§5 Sequencing for why they cannot be split.

---

## 5. Migration Complexity

**Overall: `medium`** — consistent with both entries in `retire_recommendations[]`.

Scored against the rubric in `references/retire-recommendations.md`, where the drivers
genuinely pull in opposite directions:

| Driver | Points to | Why |
|---|---|---|
| User volume | `low` | Well under 1k users; single-workstation desktop tool. |
| Account linkage | `low` | **No existing account store at all.** No credential corpus to re-hash, no directory merge. Linkage is a one-time map of each Windows principal (SID / UPN) to a broker subject. |
| Data scope | `low` | One table (`students`), ~461 lines of hand-written logic. |
| Legacy auth library | `high` | **There is no authentication library.** The `.vbproj` references no `System.DirectoryServices`, `System.Security`, or `System.IdentityModel`. An OIDC flow is net-new code in a thick client, not a protocol swap. |
| Data-tier platform | `high` | The `.accdb` file database must move to a server-hosted RDBMS in the same effort; inline `OleDb` calls need a data-access layer that propagates identity. |
| Directory retirement / cross-class merge | not applicable | Neither migration retires a directory or merges user classes — this is what keeps the score off `high`. |

Net: `medium`. Low volume and absent linkage offset net-new auth code plus a data-tier
platform move; nothing here reaches the `very-high` drivers.

Per-app complexity drivers:

- **Account linkage across existing directories:** none to perform. Map Windows
  principals to broker subjects and enrol them; staff re-provisioning is a one-time
  enrolment.
- **Session federation timeout and step-up:** both are net-new. There is no session
  concept today — a single module-level `OleDbConnection` is opened on dashboard load and
  held for the process lifetime, so there is no timeout, lifetime, or re-auth interval to
  migrate. Step-up for delete/edit must be designed from scratch.
- **Legacy auth library compatibility:** no library to be compatible with. Choose an
  OIDC pattern appropriate to a WinForms desktop client (authorization-code + PKCE via
  system browser; **not** the deprecated embedded-webview or resource-owner-password
  flows).
- **Downtime tolerance:** a single-workstation interactive tool with no batch or
  integration dependents — a maintenance window is cheap. The data-tier migration, not
  the auth change, sets the window length.

### Sequencing — the one non-negotiable

**Retire the credential-less data-tier model *before or with* the ambient-Windows model.
Never after.**

The `.accdb` is reachable at a known path by any OLEDB client, or by Microsoft Access
itself, with no credential. While that path survives, **any authentication added to the
WinForms client is bypassable** and delivers no real assurance. Client-side
authentication is worth nothing until the data tier enforces identity. Hence: one
cutover, data tier included.

---

## 6. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| **Auth added to the GUI while the `.accdb` path survives** | The headline risk. Delivers the *appearance* of an authentication boundary with none of the assurance; an auditor finding this later discredits the whole remediation. | Treat the data-tier migration as a precondition, not a follow-on. Do not ship client authentication alone. |
| Committed database file distributes live PII | `studentDB.accdb` (802 KB) and its `.laccdb` lock file are committed to the repository, so student PII — DOB, father's name, two mobile numbers — reaches every clone with no credential barrier. | Purge both files from the working tree **and from git history**; rotate nothing (there is no secret), but treat the exposure as already-occurred and scope notification accordingly. |
| Broker choice is unratified | Rework if the engagement's standing identity platform differs, compounded by the profile defining no modernization target for this stack. | Ratify against `profiles/faa/` before build. Keep the application's integration to standard OIDC so the broker remains swappable. |
| Risk tier returns Tier 1 or Tier 2 | The AAL2 floor recommended here becomes insufficient — Tier 1 demands phishing-resistant AAL3 (FIDO2, or on-card PIN-unlocked PIV), and the three `high` gaps escalate to `critical`. | Obtain authoritative classification **before** selecting the authenticator, so the choice is made once. |
| Email-code MFA adopted as the "AAL2" second factor | A common and audit-fatal shortcut: NIST 800-63B §5.1.3.3 excludes the email channel from out-of-band authenticators, so an emailed 6-digit code remains **AAL1** however the vendor markets it. | Specify TOTP or better in the requirement, and FIDO2/PIV if Tier 1 returns. Reject email-code explicitly in the design record. |
| Single-broker outage blast radius | With one app at this scope the radius is small, but it grows with every onboarded application, and this application becomes unusable during a broker outage where previously it needed nothing. | Deploy the broker HA from the start. Define an explicit break-glass procedure for this application rather than leaving a fallback to ambient Windows trust in place. |
| Skill QA fixture inside the source tree | `fixtures/default.json` is a fixture for **this very skill**, containing a ready-to-emit synthetic landscape for a fictitious three-app portfolio (`fixture-portfolio`, 12,500 users, PIV/AAL3 staff, email+password public). A future run could emit it wholesale and describe applications that do not exist. | Disregarded entirely here — none of its IDPs, user classes, assurance levels, or counts appear in either output. Remove it from the application source tree and verify no prior Discovery artifact absorbed fixture content. |

---

## 7. Identity Models Found (summary)

Full detail, including per-field assurance evidence, is in `identity-landscape.json`.

| Model | Type | IAL | AAL | FAL | Phishing-resistant | MFA |
|---|---|---|---|---|---|---|
| Ambient Windows interactive-logon identity (`AuthenticationMode.Windows`) | `on-prem-directory` | `unknown` | `below-AAL1` | `not-applicable` | `false` | `none` |
| Credential-less ACE OLEDB access to bundled `studentDB.accdb` | `custom-app-specific` | `IAL1` | `below-AAL1` | `not-applicable` | `false` | `none` |

The central finding: **this application performs no authentication of any kind.** There
is no login form, no credential store, and no users table — every SQL statement in the
tree targets the single `students` table. `Form1_Load` opens the database and renders the
dashboard immediately, and all four forms expose unrestricted insert / view / search /
edit / delete over PII. It is not that a second factor is missing; there is no *first*
factor at the application boundary.

Why the levels are not collapsed into one number — AAL is authenticator-scoped, IAL is
proofing-scoped, FAL is federation-scoped, and per NIST 800-63-3 they are independent:

- **`nist_ial: unknown`** on the Windows model is deliberate, not an omission. Proofing
  strength is wholly inherited from the issuance policy of the Windows account — a host
  or domain administration artifact that this application's source does not reveal. Per
  the mapping reference, emitted as `unknown` rather than guessed.
- **`nist_ial: IAL1`** on the data-tier model is the enum floor, applied with a caveat:
  *no* subject identity is asserted to the data tier, which is weaker than self-asserted,
  but the IAL enum has no `below-IAL1` member. Recorded as the floor with the caveat
  rather than as a misleading `unknown`, because this was fully observed.
- **`below-AAL1`** on both models is the assurance the *application boundary* enforces,
  which is none. `AuthenticationMode.Windows` populates `My.User`, but no code path ever
  reads or verifies it, so any interactive desktop session on the host — including a
  shared or kiosk account — reaches full CRUD. The strength of the upstream Windows
  authenticator is a separate and unknown question.
- **`not-applicable`** for both FAL values: no SAML, no OIDC, no assertion, no token
  exists anywhere in the tree. The absence of federation is total, which is also why the
  "SSO enabled implies FAL2" trap does not arise here.

---

## 8. Evidence Citations

- `student-management-system:Flat Design/My Project/Application.Designer.vb:26` — `MyBase.New(AuthenticationMode.Windows)`
- `student-management-system:Flat Design/My Project/Application.myapp:8` — `<AuthenticationMode>0</AuthenticationMode>`, confirming the designer-persisted intent
- `student-management-system:Flat Design/Module1.vb:7` — ACE OLEDB connection string with no `User ID`, no `Password`, and no `Jet OLEDB:Database Password`
- `student-management-system:Flat Design/Module1.vb:4` — `Public dbcon`, the single process-lifetime connection
- `student-management-system:Flat Design/Form1.vb:15` — `Form1_Load` → `connectDB()` → `LoadData()` with no auth gate
- `student-management-system:Flat Design/ViewForm.vb:83` — delete path gated only by a Yes/No `MessageBox`
- `student-management-system:Flat Design/Student Management System Siddharth Jain.vbproj:76` — reference list containing no authentication library
- `student-management-system:Flat Design/studentDB.accdb` — database binary committed to the repository
- `student-management-system:Flat Design/studentDB.laccdb` — Access lock file committed, evidencing multi-user record locking
- `student-management-system:fixtures/default.json:1` — QA fixture for this skill, disregarded as a source of fact
- `application-catalog-entry:open_questions` — FAA-relevance mismatch, null `safety_tier`, absent CMDB, fixture contamination, and no `.dotnet` modernization target for this stack
- `application-catalog-entry:architecture` — archetype `desktop`, no listener, no API surface

**Negative-evidence note.** Two load-bearing claims rest on absence rather than
presence, and are flagged as such for the reviewer:

1. *The `.accdb` has no database password.* ACE OLEDB cannot open a password-protected
   `.accdb` without a `Jet OLEDB:Database Password` token. The token's absence in
   `Module1.vb:7` establishes the file carries no database password, so access control
   over the PII reduces entirely to NTFS permissions on the file.
2. *There is no credential or users table.* `studentDB.accdb` is a binary MS Access file
   and no Access or ODBC tooling was available in this sandbox to enumerate its schema.
   The claim rests on exhaustive source evidence — every SQL statement across all four
   forms targets `students`, and no authentication library is referenced — not on DDL
   inspection. Well supported, but worth confirming against the real schema, as the
   catalog also recommends for its table count.

---

## 9. Handoff

- **`disposition-recommender`** — consume `retire_recommendations[]` (2 entries, both
  `medium` complexity, both citing Criterion 2 *blocks zero-trust* with Criterion 1
  *below required AAL* in corroboration) and `proliferation_findings[]` (1 confirmed:
  `legacy-directory-without-sso`; 2 recorded with explicit scope caveats whose thresholds
  are not evaluable from a single application). The two retirements must be sequenced as
  **one** cutover, not two waves — see §5.
- **`security-posture-analyzer`** — fold the six `assurance_gaps[]` into the per-app
  Zero-Trust and control-mapping work. All six severities are **provisional**, pinned to
  the catalog's explicitly non-authoritative T3 lean. Note that the two `high` AAL
  findings do not depend on the tier question: at `below-AAL1` the application fails the
  Tier 3 `AAL1` floor, the weakest in the rubric.
- **Gate `G-DC` (Discovery Completeness)** — clear before advancing to Rationalization.
  Three items are **open, not closed**, and should be weighed at the gate rather than
  waved through: (1) `profiles/faa/` unreadable, leaving `fronted_idps` deliberately
  incomplete and the tier floors sourced from skill references rather than the profile;
  (2) risk tier unestablished, leaving all six gap severities provisional; (3) the
  application's FAA relevance unconfirmed — an application that does not belong in the
  portfolio should not be remediated into it.
