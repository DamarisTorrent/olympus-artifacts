# UX & Accessibility Baseline — Gilded Rose Refactoring Kata (`d634afdb-97cc-4589-a080-5766d4f377d5`)

**Assessment date:** 2026-09-28
**Governing profile:** `faa` (authoritative per task declaration — see Scope caveat below)
**Discovery pass:** Pass 4 — ux-accessibility-assessor

## Scope caveat — read this first

This assessment runs under the governing `faa` client profile, as directed. But the repository under
review is the publicly published, MIT-licensed **"Gilded Rose Refactoring Kata"** — a 172-line C#
console application that models a fictional inn's nightly inventory update (README.md, attributed to
[@TerryHughes](https://twitter.com/TerryHughes) and [@NotMyself](https://twitter.com/NotMyself),
`https://github.com/NotMyself/GildedRose`). It has no HTTP listener, no database, no scheduler, and no
GUI. `src/GildedRose.Console/Properties/AssemblyInfo.cs` separately asserts `AssemblyCompany("DSHS")`
and `Copyright "DSHS 2015"` — a **third**, non-FAA attribution embedded in the shipped assembly
metadata.

Discovery's Pass 0 catalog entry and Pass 1 structural-analysis both already flagged this mismatch
independently and recommended stakeholder confirmation before this application_id is used downstream.
This artifact does not resolve that question. Every persona, adoption, training, and accessibility
figure below is conditional on it, and the mandatory `personas-confirmed` review ask below restates it
for a reviewer.

**A second, separate gap:** this skill's methodology directs composition with the `accessibility-checker`
sub-skill via a "Sub-Skill Output Contract" that is supposed to be reproduced verbatim (exact output
path + schema) inside this producing agent's own system prompt. That section was not present in the
system prompt actually supplied for this run. Rather than invent a path or schema for a sub-skill this
agent cannot correctly invoke, the accessibility section below is this assessor's own direct,
transparent read of the one discovered UI surface — **not** `accessibility-checker` output — flagged
throughout as pending a real checker composition.

## 1. UI surface inventory

| Surface | Platform / Technology | Users | Screens in repo |
|---|---|---|---|
| `console-entry-point` — `GildedRose.Console.exe` interactive session | Windows character-mode console, .NET Framework 4.5; `System.Console.WriteLine`/`ReadKey` only, no GUI toolkit, no web framework | Single local operator per invocation; no roles, no auth | 1 |

This is the application's *only* interface of any kind (Pass 1 interface-inventory: `total: 1,
human_facing: 1, machine_facing: 0`). It writes one banner line (`"OMGHAI!"`) to stdout, then blocks
indefinitely on `System.Console.ReadKey()` until a key is pressed, then exits. There is no page, form,
menu, or navigable screen — six hard-coded inventory items are processed identically on every run.

Evidence: `src/GildedRose.Console/Program.cs:8-35`.

## 2. Personas

Only **one** persona could be derived from source, and it is derived, not measured:

### `local-console-operator` — Local console operator (kata participant / build verifier)

- **Estimated headcount:** unknown. No telemetry, login system, or role model exists to count distinct
  users; every invocation is a single interactive process run by whoever executes the compiled EXE at
  a terminal.
- **Evidence:** `Program.cs:8-35` — the only entry point is a console `Main()` with no argument parsing
  (`args` is declared but never read, `Program.cs:8`), no authentication or authorization of any kind
  (a grep for `Authenticate|Login|Identity|Principal` across all tracked files returned zero matches,
  per `structural-analysis.json`), and a blocking `Console.ReadKey()` (`Program.cs:33`) that requires
  one human physically present at an interactive terminal per run. README.md frames the whole
  repository as a coding-kata exercise ("Your task is to add the new feature to our system...") rather
  than an operational business role.
- **Typical workflow:** clone the repo, run `build.bat`, execute the compiled EXE, observe the banner
  and (typically in a debugger, per the kata's intent) the six seeded `Item` values before/after
  `UpdateQuality()` runs once, press any key to exit. No repeat-usage session model, no navigation, no
  data entry — the same hard-coded list (`Program.cs:14-27`) runs identically every time.

**No other persona is evidenced.** There is no access model, no distinct role for an "administrator,"
"reviewer," or "supervisor" — the access-control surface is OS-level permission to execute the binary,
which is outside this repository.

## 3. Adoption baseline

**Every figure below is an explicit instrumentation gap, not a measured zero.** No logging framework,
database, analytics call, or persisted state of any kind exists anywhere in the tracked source — all
state is an in-memory `IList<Item>` created at `Program.cs:14-27` and lost at process exit
(`structural-analysis.json` database-schema-summary).

| Metric | `local-console-operator` |
|---|---|
| Active users (30d) | unmeasured, instrumentation gap |
| Feature-usage frequency | unmeasured, instrumentation gap — every invocation is behaviorally identical |
| Session duration | unmeasured, instrumentation gap — bounded only by how long a human waits before pressing a key at `Program.cs:33` |

Per the Constraints in this skill's methodology: absence of a signal is recorded as "no
instrumentation present," never asserted as "no usage."

## 4. Training & documentation state

| Item | Finding |
|---|---|
| User guide present | Yes — `README.md` doubles as onboarding narrative and build instructions; no separate user guide exists |
| Last updated | 2017-03-28 (commit `1daba207`, "Update README.md") — the repository holds exactly **one** commit total, so there is no revision history to compare against |
| LMS completion data | Not applicable / instrumentation gap — no LMS, training curriculum, or completion-tracking reference exists anywhere in scope |
| Training materials catalog | `README.md` (kata narrative + build steps); `images/build_output.png` (expected build-output screenshot, embedded via markdown) |

**Staleness note:** README.md's narrative (a fictional inn run by "a friendly innkeeper named Allison")
and the `AssemblyInfo.cs` "DSHS 2015" attribution both predate, and are unrelated to, the FAA governing
profile this task runs under. There is no FAA-specific training or documentation artifact anywhere in
scope against which Rationalization can score documentation debt for this application.

Per the methodology's anti-pattern warning: this assessment does **not** infer training completion
from any login/usage signal — there is no usage signal to infer from, and none is claimed.

## 5. Accessibility findings (Section 508 / WCAG 2.1 AA)

**Standards evaluated against:** Section 508 (36 CFR Part 1194, ICT Final Rule); WCAG 2.1 AA as
referenced by that rule.

**Gate decision: undetermined.** Findings count: **0**. This is *not* a compliance pass — it is the
absence of a real `accessibility-checker` run (see Scope caveat). Do not treat "0 findings" as "this
surface complies."

**Why 0 findings, not a checker-composed count:** Methodology §4 of this skill requires dispatching
`accessibility-checker` against a discovered UI surface and writing its output under a path defined by
a "Sub-Skill Output Contract" that is supposed to be folded verbatim into this agent's system prompt.
That contract (path + schema) was absent from the system prompt supplied for this run. Rather than
fabricate one, this assessor performed its own direct review of the single surface and is reporting
that review transparently as a substitute, not as checker output.

**What that direct review found:**

- No images are rendered anywhere in this application → WCAG 1.1.1 (non-text content) has no rendered
  target.
- No color is used to convey information — the surface is unstyled default-terminal monochrome text →
  WCAG 1.4.1 (use of color) has no applicable target.
- No form controls, labels, or input fields exist (`Program.cs` never reads `args` or stdin except one
  `ReadKey()` to exit) → WCAG 1.3.1 / 4.1.2 (label, name-role-value) have no applicable target.
- No timing-based content, auto-refresh, or session timeout exists (the process blocks indefinitely on
  `Console.ReadKey()`) → WCAG 2.2.1 (timing adjustable) has no applicable target.

**Still open, and flagged for manual review rather than decided here:** whether Section 508/WCAG apply
*at all* to a character-mode console surface with no page, form, or rendered GUI. Pass 1's
interface-inventory already raised this and deferred it to "the accessibility reviewer's ruling, not
this walk's guess" — this assessment defers to the same judgment call, now compounded by the missing
checker contract.

## 6. Review ask for the human reviewer

This artifact carries one mandatory review ask, **`personas-confirmed`** (action: `verify`), addressed
to the application. It asks the reviewer to confirm the single inferred persona above — and, because
the two questions cannot be meaningfully separated for this application, it also surfaces the
governing-profile/application-scope discrepancy in its `assessment` field, so a reviewer confirming
personas is not unknowingly confirming an inference over a fixture-shaped application. See the JSON
artifact's `review_asks[0]` for the full assessment, reasoning, and evidence references.

## 7. Open questions carried into this artifact

1. **Governing-profile / application-scope discrepancy** (recorded, not adopted) — no FAA/aviation/NAS
   content in source; a third, unrelated "DSHS" attribution in `AssemblyInfo.cs`. Already independently
   flagged by `catalog.json` and `structural-analysis.json`.
2. **Missing Sub-Skill Output Contract** for `accessibility-checker` composition — this run could not
   dispatch the checker per Methodology §4 because the contract naming its output path/schema was not
   supplied to this agent.
3. **WCAG/Section 508 applicability to a character-mode console surface is undetermined** — carried
   forward from Pass 1; needs an accessibility-compliance reviewer's ruling.
4. **Zero instrumentation, not zero usage** — every adoption/training figure above is an instrumentation
   gap. If a business owner holds out-of-repo usage records for this application_id, they are invisible
   to this assessment and should be supplied before any post-cutover adoption comparison relies on this
   baseline.
