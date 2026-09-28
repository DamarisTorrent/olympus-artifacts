# Decomposition Strategy — Gilded Rose Refactoring Kata

**Target application ID:** `d634afdb-97cc-4589-a080-5766d4f377d5`
**Target service:** `system` (derived — no target service decomposition defined)
**Relationship:** `replatform` *(provisional — see below)*
**Governing profile:** `faa`
**Structured artifact:** `decomposition-strategy.json`

## The strategy is that there is no strategy to select

The decomposition decision tree ran and terminated at its first step. That step asks which shared-database clusters this target participates in, and the answer is none — verified first-hand and corroborated by four independent Discovery analyses, as documented in `shared-db-analysis.md`.

All three tactics are therefore vacuous rather than rejected on their merits:

**Database-per-service** presupposes a database to split per service. There is no database, and there is only one deployable, so there is nothing to give a database to.

**Strangler fig** presupposes a legacy data store to redirect traffic away from. There is none, so no strangler justification is required or offered. This matters because the platform treats strangler-fig as an exception needing a named justification — and here the tactic is not being declined for convenience, it simply has no referent.

**Database facade** exists to mediate a shared database across waves that cannot be co-waved. With zero sharing applications and zero shared tables, there is nothing to put a facade in front of. **No facade is proposed, so no facade sunset date is owed.** That is stated explicitly rather than left silent, because an undated facade is the specific failure this rule guards against, and a reviewer should be able to see the rule satisfied by absence rather than by omission.

Selecting a tactic here would assert a shared-database decomposition with no subject. The artifact declines to do that.

## Where the real decomposition work actually lives

The most useful thing this analysis can say is that the work is real but belongs to someone else.

This application does have a genuine decomposition problem — it is simply not a data problem. One 124-line file holds the process entry point, the seed data, the complete business-rules engine, and the domain model, all in a single class and namespace. There is no layering to preserve and no existing seam to cut, so any restructuring begins by inventing boundaries that do not exist yet. Every rule branch is selected by comparing an item's name against a hard-coded string literal, so renaming an inventory item silently changes its business rules.

The structural analysis named three intra-module boundaries and one explicit non-boundary: extract the item rules and domain model into a separately-referencable library (cut this first — it unblocks the others); leave composition, seed-data acquisition and invocation behind as a host concern; re-point the orphaned test assembly at the extracted library with real characterisation tests before any refactor; and — stated explicitly so it is not read as a microservice plan — no service decomposition is warranted at 172 lines, one deployable, zero endpoints, zero integrations and zero tables.

That work is owned by the code-structure line. The risk worth flagging is that a data-line artifact reporting "nothing to do" could be read as "nothing to do anywhere," and the intra-assembly boundaries get dropped between the two lines.

## The precondition for decisive cutover is not met

This platform biases toward decisive decomposition rather than slow incremental migration, on the grounds that targets can be regenerated quickly and verified at machine speed. That bias is recorded here for completeness, but it is worth being direct about something: the bias is explicitly *conditional* on the target being behaviour-verifiable, and that condition currently fails.

The application's only business logic is a 75-line routine with zero executable coverage. The gap is structural rather than merely thin. The test project declares no reference at all to the production project, and its single test asserts that true is true — so a reader who counts two projects and a test framework would reasonably assume coverage exists, and would be wrong. Worse, the edge cannot simply be added: the routine is an instance method on an internal class reading a private field, so it is mechanically uncallable from any other assembly. The rules must first be made reachable before any test can touch them.

Two known behavioural oddities make this sharper. A rule documented in the README — that "Conjured" items degrade twice as fast — is seeded in the data but implemented nowhere, so those items currently degrade at the normal rate. And one branch zeroes a value by subtracting it from itself rather than assigning zero. Characterisation tests must pin today's *observed* behaviour, including both of these, before anything is transformed. Whether the unimplemented rule is the exercise's intended starting state or a defect to carry forward is a question for the business, not for this analysis.

## What must not be written to the database after approval

This is the one place where an empty result could cause active harm if handled carelessly.

After gate approval, an automated step normally records a data pattern against the application and one row per database cluster the target participates in. For this application the correct outcome is that **nothing is written**: no data pattern, and no cluster rows.

The reason is that every value in the permitted data-pattern vocabulary — database-per-service, strangler-fig, db-facade, dedicated, shared-read-only — asserts some relationship to a database. This application has none, so all five would be false. The right action is to leave the field unset rather than pick the least-wrong token.

For the same reason the cluster strategy list was left genuinely empty rather than filled with a placeholder entry. A placeholder would have satisfied the required format while quietly writing a phantom cluster record for a cluster that does not exist — which is precisely the error that making those fields mandatory was meant to prevent. Satisfying a contract's shape while corrupting its meaning is worse than leaving it empty.

The no-shared-write principle is satisfied verifiably rather than by assertion: with no cluster strategies there are no non-owning write roles, so no transitional pattern and no sunset marker is owed anywhere in this artifact. Write ownership is likewise vacuous — no tables means no contested ownership and no dual-write. Worth noting for later, though: the documented invariants (quality never negative, never above 50, the legendary item pinned at 80) live only as conditionals inside one loop, against a domain model with unguarded public setters. They are code-level constraints, not data-level ones. If a persistent store is ever introduced, they must be re-established as real data constraints.

## Two derived values a reviewer should not mistake for decisions

No target plan entry was supplied to this dispatch, so the four required target-binding fields could not be read from an authoritative source. Two were derived and need to be flagged.

**The relationship value is provisional.** No disposition has actually been ruled for this application. The format requires one of a fixed set of values, and `replatform` was recorded because it is the only one the measured evidence directly supports: the application targets a Windows-only framework that left Microsoft support in 2016, the target substrate is a Linux container platform on a modern runtime, and there is no in-place upgrade path. Recording `retain` would have actively contradicted that evidence.

But this is not a disposition decision by this skill, and it should not harden into one. At 172 lines, rebuilding may well cost less than porting — and that turns on whether the capability is still needed at all, which is a portfolio judgment no amount of code reading can settle. The retain / replatform / retire-or-replace ruling is raised as an explicit decision ask with four options, including deferring until portfolio ownership is confirmed.

**The target service is `system`,** not a numbered service, because no target service decomposition has been defined and the structural analysis explicitly concluded that none is warranted.

The wave binding is likewise a labelled placeholder: no wave assignment, target plan or portfolio cluster map was supplied. The strategy is unaffected — an application with no database cannot be entangled with any wave through shared data, so it constrains nobody and is constrained by nobody on data grounds. That empty constraint set is a meaningful finding, not a missing analysis. No separate co-wave constraints file is emitted, since this dispatch declared only the two artifacts and there was no wave to scope one to.

## FAA guidance reviewed and found inapplicable

The FAA shared-database guidance is built around Oracle RAC clusters and the coupling patterns that make them hard to untangle: PL/SQL packages carrying cross-domain logic, triggers that let one application's write silently mutate another's data, materialized views serving as de-facto integration layers, database links creating opaque cross-schema dependencies, and semantic-gap remediation at a facade boundary. It also expects the schema, not the instance, to be the practical unit of decomposition.

None of it applies. There is no Oracle dependency, no PL/SQL, no cluster, and no engine. No part of that guidance was used to populate the strategy, and that is recorded so its absence reads as a judgment rather than an oversight.

## Portfolio-membership discrepancy

The governing profile for this task is FAA and was applied as instructed. The source code is nonetheless a publicly published programming exercise about an inn's inventory, with no aviation, air-traffic or certification content, and the shipped assembly metadata credits a different agency. This is recorded as a discrepancy and not adopted — the profile was not overridden and no content was reshaped to match the code's apparent origin. The catalog and structural-analysis passes raised the same question independently. Confirmation of FAA ownership should be obtained before downstream lines consume this work.

## What would invalidate all of this

One premise carries the entire artifact: that this repository is the whole system. If this application record denotes a production system whose inventory persists in a store owned by some other application, that store is invisible to a static reading and this strategy would be resolving a decomposition problem that was never measured.

Because every conclusion here — the zero-row database projection, the vacuous write-ownership result, the empty co-wave constraint set — rests on that single premise, the artifact should be regenerated from scratch rather than amended if an out-of-repository store is ever identified.

## Reviewer asks

Three asks are attached to the structured artifact, in order of consequence: decide the migration disposition (the provisional relationship value); confirm that no database records should be written after approval; and record the no-decomposition-required outcome for the register.

Full decision-tree trace, risks, projection instructions, inputs consumed and open questions are in `decomposition-strategy.json`. The source-grain shared-database analysis this strategy rests on is in `shared-db-analysis.json`, with its narrative in `shared-db-analysis.md`.
