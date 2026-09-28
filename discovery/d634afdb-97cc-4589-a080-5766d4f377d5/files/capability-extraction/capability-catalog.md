# Capability Catalog — Gilded Rose Refactoring Kata (`d634afdb-97cc-4589-a080-5766d4f377d5`)

## Read this before the G-DC gate

This application's capability grain is **low-confidence and contested at
the source**. Every upstream Discovery artifact for this app (catalog.json,
structural-analysis.json) has independently flagged the same discrepancy:
the repository is the publicly published **Gilded Rose Refactoring Kata** —
a 172-line C# console program that models a retail inn's nightly inventory
update — not an application with any observed aviation, NAS, certification,
or FAA business content. `catalog.json` sets `business_domain` to
`"unclassified"` for exactly this reason.

This skill's job is to extract capability/system/domain grain regardless,
so the persist step has *something* referentially consistent to write. What
follows is a best-effort technical mapping onto the governed capability
vocabulary, not a claim that this is a real FAA capability. **The
reviewer's primary decision at this gate is whether this application_id
belongs in the FAA portfolio at all** — everything below is downstream of
that unresolved question.

## Legacy system binding

- **Name:** Gilded Rose Inventory Kata (Unclassified / Non-FAA-Mapped System)
- **External ID:** `null` — no strategy-of-record system family fits; no
  client-profile reference catalog was even available in this workspace
  to bind against (see Open Questions).
- **Rationale:** The app is a single-assembly console monolith with no
  HTTP surface, no database, no scheduler, and no integration points
  (structural-analysis.json summary_metrics: `http_endpoints: 0`,
  `database_tables: 0`, `external_integration_points: 0`). There is no
  other application in this portfolio slice known to share this "system,"
  so it is carried as its own standalone, unbound system pending
  stakeholder confirmation.
- **Role:** `primary` — it is the only application realizing this system.

## Business domains

| Domain | Description |
|---|---|
| Unclassified / Non-Aviation Inventory Exercise | A standalone nightly inventory quality and sell-in revaluation exercise with no observed mapping to any FAA business domain (Air Traffic, Flight Safety, Certification, Workforce, Finance, Logistics, Admin/Travel) in the reference taxonomy. |

Only one domain was extracted. `data-domains.json` — the methodology's
strongest signal for domain clustering — was **not available** for this
application (see Open Questions), so this domain is derived solely from
`catalog.json`'s `business_domain: "unclassified"` field and
`structural-analysis.json`'s architecture/coupling narrative.

## Capabilities

### asset-and-inventory-management

- **Description:** Applies a per-item-type rules engine that adjusts each
  stocked item's remaining sell-in days and quality level once per night
  (normal goods, Aged Brie, Sulfuras, Backstage passes, and an
  unimplemented Conjured-item rule), enforcing quality bounds in-process.
  Invoked by a single interactive operator running the console
  executable; there is no other caller, scheduler, or upstream/downstream
  integration.
- **Business domain(s):** Unclassified / Non-Aviation Inventory Exercise
- **External ID:** `null` — no strategy-of-record capability row fits;
  no reference catalog was available to check against.
- **Confidence:** 0.4 — the *technical* description of what the code does
  (an inventory quality/sell-in rules engine) is directly evidenced and
  not in doubt. The confidence is held down because (a) this is the
  closest-fit label in a 22-entry governed vocabulary built for FAA
  domains (personnel certification, airspace management, flight planning,
  etc.), none of which describe a retail inventory kata particularly
  well, and (b) whether this capability belongs in an FAA capability
  catalog at all is unresolved.
- **Evidence:**
  - `structural-analysis.json:modules[gildedrose-console]` — the module
    housing `UpdateQuality()`, the entire business-rules engine.
  - `structural-analysis.json:interface-inventory.interfaces[0]` — the
    only interface, whose `capability_hint` reads "Nightly inventory
    revaluation: adjust each stocked item's remaining sell-in days and
    quality per item-specific rules."
  - `structural-analysis.json:coupling_indicators.magic_string_dispatch` —
    detail on the 8 item-name-literal comparisons that implement the
    per-item rules.

No other capability was extracted. With zero endpoints, zero tables, and
one console entry point, there is exactly one thing this application does.

## Open questions for reviewer follow-up

1. **Governing-profile discrepancy.** The task's governing profile is
   `faa`, but the source tree has no aviation/NAS/FAA content whatsoever
   — it is the generic Gilded Rose kata. The single capability above is
   emitted as a best-effort mapping onto the governed vocabulary, not a
   validated FAA capability claim. **A stakeholder must confirm whether
   this application_id genuinely maps to an FAA-owned production system**
   before Rationalization consumes this grain for consolidation
   recommendations.
2. **Missing required input.** `data-domains.json` (Discovery's strongest
   capability signal, per this skill's own methodology) was not produced
   for this application in this dispatch — its output directory is empty.
   This catalog was built from `application-catalog-entry.json` and
   `structural-analysis.json` (which embeds `interface-inventory`) alone.
   Re-run this skill if `data-domains.json` becomes available, to
   corroborate or expand the single capability recorded here.
3. **No client-profile reference catalog was available.** No
   `profiles/faa/` capability/system strategy-of-record catalog existed
   in this workspace, so none of `legacy_system.external_id`,
   `business_domains[].external_id`, or `capabilities[].external_id`
   could be bound — all are `null` for that reason, not because a binding
   attempt failed on ambiguity.
4. **Agency-attribution discrepancy (observed, not adopted).** The
   shipped assembly metadata (`AssemblyInfo.cs`) asserts a `DSHS`
   copyright/company — a different, non-FAA agency — which is a further
   signal against this being an FAA system. Reported here per
   `structural-analysis.json:open_questions[0]`; not treated as this
   task's governing profile.
5. **Unimplemented "Conjured" rule.** README.md documents a Conjured-item
   degradation rule that the code does not implement. Whether the
   capability description above should describe Conjured handling as
   in-scope-but-broken or out-of-scope depends on a product answer this
   walk cannot give.
