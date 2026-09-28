# Shared Database Analysis — Gilded Rose Refactoring Kata

**Application ID:** `d634afdb-97cc-4589-a080-5766d4f377d5`
**Governing profile:** `faa`
**Analysis date:** 2026-09-28
**Structured artifact:** `shared-db-analysis.json`

## The finding in one line

This application has no database, so it participates in no shared-database cluster and imposes no shared-data constraints on any other application's migration wave.

That is the whole result. What follows explains why it is a measured conclusion rather than a scan that came back empty, and what would have to be true for it to be wrong.

## Why this is a negative result, not a gap

A shared-database analysis that reports nothing is indistinguishable, on its face, from one that failed. This one did not fail, and the distinction matters enough to document.

The application's entire state is six inventory items written as literals into its source code. They are built into a list in memory when the program starts, adjusted once by the nightly-update routine, and lost when the process exits. There is no read from, and no write to, anything outside the process. The only place the starting values persist is the source repository itself.

To confirm that first-hand rather than inherit it, every one of the 22 files the application actually tracks in version control was swept for the markers a data tier cannot hide: connection strings, SQL Server and ODBC and OLE DB client types, Entity Framework and other object-relational mappers, Oracle references, schema definition files, and migration scripts. All returned nothing. The application's configuration file binds only a runtime version and contains no connection-strings section at all. There is no schema file, no migration, and no object-relational model anywhere in the tracked tree.

One signal in the project file superficially looks like a data tier: the project references the `System.Data` assembly. It is an unused Visual Studio template default with no corresponding code anywhere — worth naming explicitly, because a naive keyword search would re-derive a database tier from it that does not exist.

Four upstream Discovery analyses reached the same conclusion independently: the database archaeology pass recorded no database engine present; the SQL Server object inventory returned an explicit null result with every inventory empty; the structural analysis counted zero tables, procedures, triggers and connection strings; and the data-lineage trace found that every data flow terminates in either the source repository or process memory, with no external system appearing in any flow. Agreement across five independent derivations is the basis for stating this with confidence.

## FAA shared-database guidance does not apply here

The FAA-specific guidance for this work is built around Oracle RAC clusters, and around the coupling patterns that make them hard to untangle: PL/SQL packages holding cross-domain business logic, triggers that let one application's write silently mutate another's data, materialized views used as de-facto integration layers, and database links creating opaque cross-schema dependencies. It also sets the expectation that the practical unit of decomposition is the schema rather than the instance.

None of it is applicable. There is no Oracle dependency, no PL/SQL, no cluster, and no engine of any kind. No part of that guidance was used to populate the analysis, and this is stated so its absence reads as a deliberate judgment rather than an oversight.

## What could make this finding wrong

One thing, and it is worth taking seriously.

The conclusion is bounded by this repository. If this application record actually denotes a production system that keeps its inventory in a store owned by some *other* application, that store is invisible to a static reading of this code and the analysis would be understating coupling all the way to zero. A false-negative here is precisely the failure mode that causes late wave slippage, because co-waving constraints discovered after sequencing has been agreed are expensive to unwind.

There is a reason to ask rather than assume. An application with no durability, no audit trail, and no record of its nightly run is an unusual thing to find under portfolio management. The technical evidence is unambiguous; the contextual oddity is what makes the question worth putting to the business owner explicitly. Until it is answered, this application should not be treated as unconstrained for wave-sequencing purposes.

## Two further risks worth a reviewer's attention

**There is no behavioural baseline, which removes the precondition for a decisive cutover.** This platform's stated bias is toward decisive decomposition, but that bias is explicitly conditional on the target being behaviour-verifiable. It is not verifiable here. The application's only business logic is a 75-line routine that is mechanically unreachable from outside its own assembly: it is an instance method on an internal class reading a private field. The accompanying test project declares no reference to the production project at all, and its single test asserts that true is true. So the coverage is not merely thin — the regression safety net is structurally absent. Anything that transforms this application starts with no executable definition of correct behaviour, including for two known oddities: a documented rule for "Conjured" items that is seeded in the data but implemented nowhere, and a branch that zeroes a value by subtracting it from itself.

**Fixture material in the working tree could contaminate a downstream reading.** An untracked file in the source root describes a fabricated, unrelated application complete with a SQL Server schema, named tables and a trigger. It is test-harness material, not documentation of this application. A consumer that scans the source root instead of the tracked file set could manufacture both a database tier and a phantom shared cluster from it — inverting this analysis's central finding. The safeguard is simple and should be inherited by every downstream data-layer pass: treat only version-controlled paths as application source. The four staged tooling directories, including the only SQL-suffixed file in the tree (a deliberately non-executable template querying dictionary views for an engine this application lacks), are excluded on exactly that basis. No cluster, table, application name or risk recorded in the structured artifact derives from fixture content — including from this skill's own example scenario.

## Two scope gaps in the inputs, recorded for the file

**No wave was supplied.** This pass ran with no wave assignment, no target plan entry, and no portfolio-wide database cluster map — consistent with a Discovery-grain pass that runs before waves are assigned. Because the output format requires a wave value, a clearly-labelled placeholder was recorded rather than a plausible-looking wave number. The analysis is unaffected: an application with no database cannot be entangled with any wave through shared data. It should be rebound once a real wave is assigned.

Relatedly, no portfolio-grain cluster map was available to cross-check against. For this application the omission is immaterial — an application with no database cannot appear as a write owner on any cluster — but it does mean the "no other application shares a store with this one" direction of the finding rests on this application's own evidence rather than on a portfolio-wide join.

**A declared input was not staged where expected.** The dispatch declared the structural analysis as a required input, but the staged input directory contained only the dispatch context file. The artifact was read instead from the sibling producer directory, and the second declared input was read from the schema-summary block embedded within it. Both inputs were therefore obtained and used; the staging gap is recorded so it is visible and not mistaken for an unread input.

## Portfolio-membership discrepancy

The governing profile for this task is FAA and has been applied as instructed. The source code, however, is a publicly published programming exercise about an inn's inventory, with no aviation, air-traffic or certification content whatsoever. The application's own compiled metadata additionally credits a different agency entirely.

This is recorded as a discrepancy, not resolved. The FAA profile was not overridden, and nothing in the analysis was reshaped to match the code's apparent origin. The catalog and structural-analysis passes raised the same question independently, which makes it a consistent portfolio-level issue rather than an artifact of one reading. Confirmation that this application record genuinely belongs to the FAA portfolio should be obtained before downstream lines consume any of this work.

## Reviewer asks

Four asks are attached to the structured artifact, in order of consequence: confirm whether an out-of-repository data store exists; confirm the application's FAA portfolio membership; note the absent wave binding; and record the no-decomposition-required outcome for the register. The first is the only one that could change the analysis's conclusion.

Full cluster inventory, verification method, corroborating artifacts, structured risks and open questions are in `shared-db-analysis.json`. The target-grain companion, which records that no decomposition tactic applies and that no database projections should be written, is in `decomposition-strategy.json` with its own narrative in `decomposition-strategy.md`.
