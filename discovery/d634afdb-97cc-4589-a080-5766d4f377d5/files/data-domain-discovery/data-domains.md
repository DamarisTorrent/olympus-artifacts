# Data Domain Boundaries — Gilded Rose Refactoring Kata

**Application:** `d634afdb-97cc-4589-a080-5766d4f377d5`
**Governing profile:** `faa`
**Derived:** 2026-09-28 · Discovery line, data-domain-patterns
**Machine-readable model:** `data-domains.json` (this directory) — entity-to-domain matrix, cross-domain references, arbitration record

---

## What we were working with

This application is 172 lines of C# in a single console executable. It declares exactly one
type — `Item`, with three properties — seeds six of them from hardcoded literals, runs one
nightly-update method over them, and exits. It has no database, no file I/O, no queue, no
HTTP surface and no user concept. Three earlier Discovery steps each verified that absence
independently rather than assuming it.

Two things about the inputs are worth stating up front, because they shaped the method.

First, **nothing was inherited to refine.** This step is normally handed an upstream domain
artifact and a database schema summary and asked to sharpen them. Neither was staged: the
step's input directory held only the dispatch context, and the declared schema-summary input
does not address a file — correctly, since there is no schema to summarise. Rather than emit a
model that mirrors that emptiness, the domains below were derived first-hand from the source.
A small domain set is the right answer for an application this size, but it is a *derived*
small set, not a stub.

Second, **the working tree contains harness test fixtures, and one of them is a ready-made
answer for this exact step.** `fixtures/domain-boundary-ambiguous.json` is a pre-baked domain
model for an application called `fixture-app`, asserting a target service of `S1` and three
domains — Accounts, Billing, Reporting — over entities like User, Invoice and Dashboard. None
of those entities exist anywhere in this source tree. The file states its own purpose as a
mock for the data-domain-patterns skill. It was read only far enough to identify it, and
contributed nothing: no domain, entity, owner or option key in our model comes from it. Two
prior Discovery steps reached the same exclusion about its sibling fixtures on independent
grounds. We are asking you to confirm that exclusion stands.

## The two domains

**Inventory Stock Item** holds the item and the run-scoped collection that contains it — an
item's name, the days left to sell it, and its quality score. This boundary is firm. The
sell-in and quality values are written inside a single loop iteration with no commit boundary
between them, and every rule in the application reads name, sell-in and quality together as
one tuple before writing anything. Changes-together and queried-together both point the same
way, and there is no second declared type to couple to. Confidence here is high.

**Item Quality Rule Set** holds the item's classification and the rules that move its quality
over time: ordinary goods decay, Aged Brie appreciates, backstage passes accelerate then go
worthless, and Sulfuras is exempt from everything. The 0–50 quality band and the fixed 80 for
Sulfuras live here too. This domain is *latent* — it has no class, no enum, no lookup table
and no configuration file. It exists only as literal string comparisons and numeric guards
inlined into the control flow of one 74-line method.

## Why the boundary falls there — and why it is genuinely arguable

Of the five boundary heuristics, only three did any work on this application.

Lifecycle is what separates the two domains, and it separates them cleanly: sell-in and
quality are rewritten on every run, while the item's name and every rule threshold are fixed
at compile time. Business owner points the same way in principle — merchandising policy and
inventory operations would plausibly sit with different units — but we could not evidence
either owner, so that signal is suggestive rather than load-bearing. Queried-together pulls
the other way, and hard: every rule is read in the same statement as the item it applies to.
Security classification did no work at all, because there is no PII, no credential and no
authorization anywhere in the application, so there is no access-control seam to find.

That leaves the domain count genuinely unsettled — two heuristics separating, one unifying,
two silent — which is why we are putting it to you rather than deciding it. We recorded the
two-domain shape as the provisional answer at low confidence. The one-domain shape, treating
the rules as behaviour of the stock item rather than data of their own, is equally defensible
on this evidence and is closer both to the as-built code and to this kata's conventional
refactoring. The decision matters because it determines whether the target design needs a
rule-lookup interface the legacy code never had.

One deliberate non-split is worth flagging. `Item.Name` does double duty as display label,
natural key and classification discriminator, which makes it tempting to move into the rule
set. We did not, because splitting one entity's attributes across two domains breaks the
one-entity-one-domain rule. Instead the rule set owns the *category* concept that a name
resolves to, and the stock-item domain references it. That reference — matching a mutable
display string against hardcoded literals, with no referential integrity whatsoever — is the
single seam between the domains, and in a target design it becomes a category-lookup data
product with the stock item carrying a category identifier instead of matching on text.

## What the Data line should know

Neither domain has a physical footprint. There is no table, file, queue or blob behind either
of them; the only storage is an in-memory list discarded at process exit. **There is no data
to migrate here, only data to start keeping** — any target design must add persistence and
egress this application never had, which is build work rather than a migration.

Two of the four carried-forward boundary violations are high severity. The rule-set domain has
no representation in the code at all, so there is no seam at which it could be separately
owned, tested or changed without a rebuild — materializing it is a precondition for treating
it as a domain. And the application discards every value it computes: the update method mutates
the list, then the entry point exits without printing, returning or persisting anything, so no
legacy output format, retention rule or archival schedule exists to preserve.

Two smaller items for the business owner. A rule documented in the README has no
implementation — "Conjured" items are supposed to decay twice as fast, and a Conjured Mana Cake
is among the seeded items, but no branch matches it, so it is silently processed as an ordinary
good. The as-built rule set and its documentation disagree, and downstream lines must treat the
code as authoritative. Separately, the sell-in read/write ordering inside the loop is
load-bearing and unguarded: backstage rules read sell-in *before* its decrement while
past-sell-date rules read it *after*, so the most natural cleanup a developer would make
silently changes outcomes on the boundary days. The only test in the repository asserts
`true`, so nothing detects it. Capture a characterization test over the seeded items before
touching these rules.

## Open asks

The blocking one is the domain count: **two domains or one**, with a third option to defer
until owners are known. Beyond that we need the **business owner for each domain** — both are
recorded as unknown rather than guessed, which is why this step could not produce the
ownership assignment it is meant to.

We also need the **target binding confirmed**. This is a Discovery-line dispatch with no
architecture-target-plan entry, so no target service and no modernization disposition have
been decided. The schema requires both, so we recorded the cross-cutting umbrella service and
a single-source `refactor` relationship as the least-asserting placeholders available. Neither
is a decision. We specifically did *not* adopt the `S1` that the harness fixture asserts for a
different application.

Underneath that sits a question two earlier steps already raised and which remains open: the
source tree is the public Gilded Rose retail-inventory kata, with no NAS, aviation or
certification content anywhere in it, and no domain here could be grounded in an FAA business
taxonomy. The domains are named from the application's own vocabulary as a result. Whether
this application ID genuinely maps to an FAA-owned system decides whether these boundaries are
worth carrying into an FAA target-state design at all.
