# Broker-Federation Recommendation

**Application:** `d634afdb-97cc-4589-a080-5766d4f377d5` — "Gilded Rose Refactoring Kata"
**Governing profile:** `faa`
**Source skill:** `identity-landscape-analyzer`
**Analyzed:** 2026-09-28
**Companion artifact:** `identity-landscape.json` (field `broker_recommendation`)

---

## 0. Headline

**This application has no identity model.** It performs no authentication, holds no
accounts, issues no sessions, and integrates no identity provider. The correct broker
recommendation is therefore `keep-separate` — not because a broker was weighed and
rejected, but because there is no authentication flow for a broker to intercept.

Everything below documents how that conclusion was reached, what was checked and ruled
out, and which four data-quality questions a reviewer must resolve before this artifact
is consumed downstream.

**Scope note (skill scope rule LD-10).** This is a *per-application* invocation. It sees
one application. It does not and cannot decide the FAA portfolio's broker posture, and
nothing here should be read as dissent from a portfolio-level decision.

---

## 1. Recommended Pattern

**Selected: `keep-separate`**

| Pattern | Applicable here? | Why |
|---|---|---|
| `broker-all` | No | Requires an authentication redirect to intercept. None exists. |
| `broker-public-only` | No | No public interface; `user_facing: false`. |
| `broker-staff-only` | No | No staff interface, no staff directory binding. |
| `keep-separate` | **Yes, by default** | Closest available member — though note it is defined as "apps integrate directly with each IDP", and this app integrates with *zero* IDPs. |

A broker works by intercepting an authentication redirect and exchanging an assertion for
a session. This application's only entry point is a console `Main()` that seeds a
hardcoded list of fictional inventory items and exits:

- `src/GildedRose.Console/Program.cs:8` — `static void Main(string[] args)`
- `src/GildedRose.Console/Program.cs:14-27` — hardcoded in-memory item list
- `src/GildedRose.Console/Program.cs:33` — `System.Console.ReadKey()`, then exit

Fronting this with Keycloak is not a deferred improvement. It is architecturally
undefined.

---

## 2. Broker Technology

**For the current architecture: none.**

**Conditionally, if re-platformed as a networked multi-user service:** Keycloak 24.x on
AWS GovCloud, per the FAA profile default (`references/faa-identity-providers.md:47-48`).

This is recorded as a conditional target, not a recommendation to deploy. No broker is
recommended for, or deployable against, the console executable that exists today.

### Relationship to the FAA profile default — read this carefully

The FAA profile default is `broker-all` **unless an application opts out with ATO
evidence** (`references/faa-identity-providers.md:45-46`).

**That opt-out clause is expressly NOT being invoked.** No ATO evidence was supplied and
none is claimed. This is a finding of *architectural inapplicability*, not an exemption
and not a waiver. If the application is modernized into a networked service, it should
join `broker-all` on the profile's ordinary terms.

---

## 3. Fronted IDPs

**`fronted_idps: []` — empty, deliberately.**

Zero upstream IDPs are or could be fronted for this application in its present form. The
empty array is a measured result, **not** a placeholder awaiting the profile's default
pair. Do not populate it by inheritance.

For reference only, the profile bindings that *would* apply after a hypothetical
re-platform (`references/faa-identity-providers.md:11-25`):

| IDP | User class | IAL / AAL / FAL | Phishing-resistant | Status here |
|---|---|---|---|---|
| Login.gov | public-user | IAL2 / AAL2 / FAL2 | false (default issuance) | **Not integrated. Conditional target only.** |
| PIV via MyAccess (on-card, PIN-unlocked) | agency-staff | IAL3 / AAL3 / FAL2+ | true | **Not integrated. Conditional target only.** |

Per the profile, PIV reaches AAL3 only when the key is on-card and PIN-unlocked; a
software cert in the OS keystore degrades to AAL2 at best. That distinction is recorded
so it is not lost if this table is ever acted on.

---

## 4. Apps in Scope

One application. No migration waves are assignable, because there is no authentication to
cut over.

---

## 5. Migration Complexity

**Overall: `low`** — in the specific and narrow sense that **there is no migration to
perform.**

`retire_recommendations` is an empty array. No identity model exists to retire. Each
retire criterion from `references/retire-recommendations.md` was evaluated explicitly:

| Criterion | Fires? | Evidence |
|---|---|---|
| #1 Below required AAL for user class | No | No user class and no authenticator exist. The AAL floor applies to an authenticated subject; there is none. Also, no authoritative risk tier was supplied, so no floor is even established (see §7). |
| #2 Blocks zero-trust | No | **Checked explicitly, because an IWA retire recommendation would have been mandatory rather than optional.** No IWA/NTLM, no Kerberos, no Basic Auth, no direct LDAP bind, and no shared service accounts exist anywhere in the tree. |
| #3 Not phishing-resistant with Tier 1 dependency | No | No authenticator to classify, and no Tier 1 dependency established. |
| #4 Superseded by federation | No | No app-specific model exists to be superseded. |

Complexity drivers that would push this into medium/high/very-high are all absent: there
are no accounts to link, no directories to merge, no cross-class merge, and no users to
re-badge. The user population is zero.

If a future re-platform introduces authentication, complexity must be re-scored **then**,
against the real user population. It cannot be meaningfully scored against a population
of zero now.

---

## 6. Proliferation Analysis

**`proliferation_findings: []` — empty.** This is a deliberate scoping decision, not an
unexamined one. All six heuristics in `references/proliferation-patterns.md` were
evaluated:

| Heuristic | Result | Reason |
|---|---|---|
| `same-user-multiple-accounts` | Does not fire | Requires accounts. There are none. |
| `same-app-multiple-models` | Does not fire | Requires 2+ models for one user class. There is one "model", and it is the *absence* of authentication. |
| `redundant-federation` | Does not fire | Requires two federation IDPs at equal assurance. There are zero. |
| `legacy-directory-without-sso` | Does not fire | Requires a direct `ldap://` bind, NTLM/Kerberos IWA, or a local `users` table. Grep found none. |
| `no-broker-federation` | Does not fire | Requires 3+ distinct providers in the observed set. There are zero. |
| `identity-model-per-app` | **Not computable at this scope** | See below. |

### On `identity-model-per-app` — the portfolio claim this invocation declines to make

This heuristic is a ratio of distinct models to apps, which is only computable at
portfolio scope. Per LD-10, a portfolio-wide count **must not** be asserted from a single
application's evidence.

The FAA reference records that the Phase 1 portfolio scored above the 0.6 threshold and
that CAIS, AADOCS, IACRA, and MedXPress each integrate their own IDP with no common
broker (`references/faa-identity-providers.md:37-40`). **That is profile background, not
something this invocation measured.** Emitting it here as a finding would produce an
`affected_apps[]` listing applications outside this scope, attributed to evidence this
run never saw. It is therefore not emitted.

A portfolio-level rollup remains a legitimate and valuable future step — but it is a
different step, with different inputs.

---

## 7. Assurance Findings and the Provisional Severity

One assurance gap is recorded, with two honest imprecisions flagged on its face.

**Gap type `no-mfa`, severity `low`.**

**Imprecision 1 — the label understates the condition.** The application performs no
authentication *at all*: no primary factor, no registration, no session, no authorization
check on any path. The `gap_type` enum has no member meaning "no authentication layer
whatsoever", so `no-mfa` is the closest available value and it **understates** reality.
A reader who sees `no-mfa` and infers "has auth, lacks a second factor" would be wrong.

**Imprecision 2 — the severity is provisional.** The skill's quality rule requires
severity to be pinned to the application's risk tier. **No authoritative risk tier was
available.** The catalog entry records `safety_tier: null` and notes that
`profiles/faa/risk-classification.yaml` explicitly prohibits inferring safety tier from
code patterns alone (`catalog.json:56,61`).

`low` reflects the current architecture, not the label: a non-user-facing console
executable with no HTTP listener, no database, no scheduler, no network egress, no
persistence, and no PII or PHI in scope, where access is fully delegated to host-OS
execute permission — a defensible control for a single-run local CLI.

> **If a risk tier is subsequently assigned, this severity MUST be re-pinned.** A Tier 1
> designation would make a below-AAL1 model `critical`, not `low`.

### Why IAL is `unknown` but AAL is `below-AAL1`

These are recorded independently, per NIST 800-63-3, and the difference is intentional:

- **AAL = `below-AAL1`.** The authenticator configuration *was* determined: there is no
  authenticator of any kind, which is by definition weaker than the single-factor AAL1
  floor. This is a measured value, not a gap in knowledge.
- **IAL = `unknown`.** The condition is *inapplicability, not indeterminacy*. No user
  identity is ever collected, so no proofing process exists to grade. NIST 800-63A IAL1
  ("self-asserted, no proofing") still presupposes an asserted identity, which this
  application never receives. The `nist_ial` enum has no `not-applicable` member, so
  `unknown` is the only expressible honest value.
- **FAL = `not-applicable`**, per the mapping reference's rule for local-accounts-only.
  This application has neither local accounts nor federation.
- **`model_type` is omitted entirely.** The enum has no member meaning "no identity
  mechanism present". Selecting `custom-app-specific` would falsely assert that this
  application built its own authentication; it built none. The field is optional, so it
  is left out rather than guessed.

---

## 8. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| A downstream consumer reads `keep-separate` as an approved standing exemption from `broker-all` | Application silently escapes the portfolio broker mandate if it is ever modernized | §2 states the ATO opt-out is **not** invoked. Re-run this skill as a gate on any re-platform that introduces a network interface. |
| `gap_type: no-mfa` is read as "has auth, lacks second factor" | Remediation scoped to adding MFA to an app that has no primary factor either | §7 flags the understatement on the finding's face; the gap `description` in the JSON carries the same warning. |
| `severity: low` is treated as a pinned, tier-backed rating | A Tier 1 workload's critical gap is triaged as low | §7 marks it provisional; obtain the risk tier and re-pin. This is the highest-value open action. |
| `fronted_idps: []` is "helpfully" populated with the profile default pair | Artifact falsely asserts Login.gov / PIV federation that does not exist | §3 states the empty array is a measured result, not a placeholder. |
| The FAA profile bindings in §3 are mistaken for observed configuration | Fabricated assurance levels enter the compliance record | Every profile binding in this document is labelled "conditional target only". None was observed in this repository. |
| Identity conclusions are applied to the wrong system | Analysis of a public refactoring kata is filed against a real FAA system | §9 open question 4. Confirm the `application_id` mapping before consumption. |

---

## 9. Open Questions for the Reviewer

1. **Risk tier is missing.** `safety_tier: null` in the catalog, and tier inference from
   code patterns is prohibited by the profile. The `low` severity in §7 cannot be
   confirmed until a tier is supplied. **Highest-priority action.**
2. **`portfolio_id` is UNKNOWN.** No portfolio identifier was supplied in the dispatch
   context. Rather than invent one — a fabricated id silently fails to bind downstream —
   the field carries an explicit self-describing `UNKNOWN` string. Supply the real
   portfolio id if this artifact is to be rolled up.
3. **`profiles/faa/` was not materialized in this workspace.** The only profile material
   available was the bundled `references/faa-identity-providers.md`. No citation is made
   to `profiles/faa/compliance.yaml` or
   `profiles/faa/config/identity-landscape-analyzer.yaml`, even though the reference's
   citation-format section prefers that form — only files actually read are cited.
4. **This application is outside the profile reference's declared scope, and has no FAA
   nexus.** `references/faa-identity-providers.md:5` declares
   `applies-to: [iacra, cais, aadocs, medxpress, dms, rms, ims]`; this application is not
   among them. The source tree is the public "Gilded Rose Refactoring Kata" — an inn
   inventory exercise — with no aviation or FAA content, which the catalog entry
   independently flags (`catalog.json:59-60`). Whether this `application_id` maps to a
   genuine FAA system is unconfirmed and should be settled before consumption.
5. **`fixtures/default.json` was disregarded.** It self-identifies as a test fixture for
   the `legacy-data-flow-tracer` skill and describes a different, fabricated application.
   It was not used as evidence for any statement in this analysis. Confirm it should keep
   being disregarded.

---

## 10. Evidence Citations

Only files actually read in this run are cited.

- `src/GildedRose.Console/Program.cs:8` — sole entry point, `static void Main(string[] args)`
- `src/GildedRose.Console/Program.cs:14-27` — hardcoded in-memory item list; no user input, no identity
- `src/GildedRose.Console/Program.cs:33` — `System.Console.ReadKey()` then exit; no session lifecycle
- `src/GildedRose.Console/app.config:1-6` — entire file is one `<startup>` element; no `<system.web>`, `<authentication>`, `<authorization>`, `<identity>`, `<membership>`, or `<connectionStrings>` section
- `src/GildedRose.Console/GildedRose.Console.csproj:8` — `<OutputType>Exe</OutputType>`
- `src/GildedRose.Console/GildedRose.Console.csproj:35-41` — references limited to System, System.Core, System.Xml.Linq, System.Data.DataSetExtensions, Microsoft.CSharp, System.Data, System.Xml; no System.Web, System.DirectoryServices, System.IdentityModel, System.Security.Claims, Owin, or IdentityServer
- `src/GildedRose.Console/packages.config:1-4` — only NuGet package is GitVersionTask 2.0.1, a build-time dependency
- `src/GildedRose.Tests/GildedRose.Tests.csproj:46,50,54` — the only three matches for the auth-term sweep across `src/`, all the literal string `PublicKeyToken` in xUnit assembly references
- `input-artifacts/discovery-identity-landscape-analyzer/discovery/d634afdb-97cc-4589-a080-5766d4f377d5/catalog.json:36` — `archetype: cli`, no HTTP route/controller/scheduler/MQ listener
- `.../catalog.json:56,57` — `safety_tier: null`, `user_facing: false`
- `.../catalog.json:59-61` — profile/domain mismatch, disregarded fixture, and prohibition on inferring safety tier
- `references/faa-identity-providers.md:5` — `applies-to` list excluding this application
- `references/faa-identity-providers.md:11-25` — public-user and agency-staff IDP bindings
- `references/faa-identity-providers.md:37-40` — portfolio proliferation patterns (cited as background, not as a finding of this run)
- `references/faa-identity-providers.md:45-48` — `broker-all` default, ATO opt-out clause, Keycloak 24.x on AWS GovCloud
- `references/nist-800-63-mapping.md` — IAL/AAL/FAL independence, `not-applicable` rule for local-accounts-only, `unknown` handling
- `references/proliferation-patterns.md` — all six heuristics evaluated in §6
- `references/retire-recommendations.md` — all four retire criteria evaluated in §5, and the complexity rubric

---

## 11. Handoff

- **`disposition-recommender`** — consumes `retire_recommendations[]` and
  `proliferation_findings[]`. Both are **empty arrays: evaluated, nothing found**, not
  unevaluated. No Retire or Consolidate disposition is supportable on identity grounds.
  There is no identity debt here to retire.
- **`security-posture-analyzer`** — the Zero-Trust input is that no trust boundary exists
  to evaluate. Access control is entirely host-OS execute permission. Critically, **no
  IWA/NTLM, Kerberos, Basic Auth, direct LDAP bind, or shared service account exists**,
  so the mandatory zero-trust-blocker retire recommendation does not fire.
- **Gate `G-DC` (Discovery Completeness)** — this artifact is *evaluable but not fully
  determined*. Two inputs are genuinely missing and both are recorded rather than
  papered over: the risk tier (§9.1, blocks severity pinning) and the portfolio
  identifier (§9.2). The application-identity question in §9.4 should be resolved before
  this artifact informs any FAA compliance record.
