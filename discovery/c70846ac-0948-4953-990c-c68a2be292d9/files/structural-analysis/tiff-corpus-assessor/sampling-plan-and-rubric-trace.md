# Sampling Plan, Rubric Trace & Engine Decision Trace

Companion to `tiff-corpus-assessment.json`. Application
`c70846ac-0948-4953-990c-c68a2be292d9` — Student Management System (VB.NET).
Governing profile: **faa** (authoritative, per task declaration).

> **Headline: there is no image corpus.** This application contains **zero
> scanned-document images**. The assessment artifact is a *negative
> determination* — a scope-exclusion record — not a feasibility plan. No OCR,
> sampling, or content-migration spend is justified against this application.

---

## 1. Population (census, not sample)

| Item | Value |
|---|---|
| Corpus ID | `c70846ac-student-management-system-vbnet-no-image-corpus-2026-10` |
| Scanned-document pages | **0** |
| Total raster assets (the actual population) | **35**, confidence `exact` |
| Raster footprint | 450,118 B ≈ 0.00045 GB; avg 12.6 KB |
| Working tree (excl. `.git`) | 2,557,226 B |
| Year range | 2023–2023 (sole commit `206eedb`, 2023-09-15) |
| Growth rate | 0 — no network, web, batch, or image-ingestion path |

Population was **enumerated exhaustively**, so there is no sampling error.

## 2. Strata — 100% sampling fraction in every stratum

| # | Stratum | Selector | Pop. | Examined |
|---|---|---|---|---|
| 1 | On-disk rasters | `find -iregex '.*\.(tif\|tiff\|png\|jpg\|jpeg\|bmp\|gif\|ico\|jp2)$'` | 4 | 4 |
| 2 | Embedded `.resx` bytearrays | base64-decode every `bytearray.base64` `<value>` in 5 `.resx` | 37 payloads → **31 PNG** + 6 non-image stubs | 37 |
| 3 | PDF-embedded rasters | filter/XObject analysis of the 28-page report | 0 scanned pages | all |
| 4 | Database BLOBs | magic-marker scan of all 802,816 B of `studentDB.accdb` | 0 | all |

Stratum 1 detail: `Student Management(1..3).png` (103,870 / 43,627 / 35,262 B,
truecolor ~1600×790 screen captures) + `graduates.ico` (4,286 B).
Stratum 2 detail: `Form1.resx` 26, `ViewForm.resx` 4, `InsertForm.resx` 3,
`EditForm.resx` 3, `Resources.resx` 1.

## 3. Confidence and margin of error

Recorded `confidence_level: 0.95` (schema default) and it is **formally
meaningless here** — a census has a margin of error of zero by construction.

**`sample_size: 100` is a schema floor, not a measurement.** The schema sets
`minimum: 100`; the whole population is 35. True examined n = **35 of 35**.

## 4. Method

`stratified-random` is recorded as the closest enum member: a census is the
limiting case of stratified-random at a 100% sampling fraction. `pure-random`
was rejected (it requires a prior stratification study and would understate the
rigour actually applied). No enum member expresses "census".

## 5. Access-path validation

The worksheet's 25-image round-trip through a production access path **does not
apply** — there is no vendor image-workflow system, no proprietary wrapper, and
no viewer. Access is a direct file-system read of the staged working tree
(`access_method: file-share`, never `unknown`). Verified by magic bytes:

```
studentDB.accdb  802,816 B  -> no image magic (0 TIFF, 0 JPEG, 0 PNG, 0 BMP, 0 GIF, 0 PDF, 0 OLE)
.resx payloads   37 decoded -> 31 PNG, 6 non-image stubs, 0 TIFF
Project report   867,592 B  -> Word 2013 producer; 0 CCITTFaxDecode, 0 JBIG2Decode, 0 JPXDecode
Repo-wide        0 TIFF (II*\0 / MM\0*), 0 Group IV, 0 CCITT, 0 microfiche
```

Git history across all refs: one commit, zero deletions — nothing was removed.

**Caveat on an earlier probe:** a shell `grep` for `$'II\x2a\x00'` appeared to
hit ten markdown files. That was a false positive — bash stripped the NUL,
collapsing the pattern to the regex `II*` ("I" followed by zero-or-more "I").
The binary re-verification above supersedes it. One stray `MM\0*` inside the
PDF's Flate-compressed streams is 4-byte coincidence, not a TIFF header: the
PDF declares **zero** CCITT/JBIG2/JPX image filters.

## 6. Observer protocol

**Not run, and could not be.** The two-reviewer blind scoring with Cohen's
kappa ≥ 0.75 presupposes scoreable scanned pages. There were none, so
`sample-scoring.jsonl` was not produced. Any future artifact claiming rubric
scores for this application must first produce a genuine sample.

---

## 7. OCR-readiness rubric trace

All 8 documented factors, documented weights, every score at the floor of 1 —
**not** as measured degradation but as the marker for *absence of scoreable
material*.

| Factor | Score | Weight | Contribution |
|---|---|---|---|
| scan-resolution | 1 | 0.15 | 0.15 |
| compression-artifacts | 1 | 0.10 | 0.10 |
| color-depth | 1 | 0.05 | 0.05 |
| skew-and-rotation | 1 | 0.10 | 0.10 |
| handwriting-presence | 1 | 0.20 | 0.20 |
| form-structure | 1 | 0.15 | 0.15 |
| language-consistency | 1 | 0.10 | 0.10 |
| text-density | 1 | 0.15 | 0.15 |
| **Composite** | | **1.00** | **round(1.00) = 1** |

Weights sum to exactly 1.0; composite reproduces to `1` = **reject**. "Reject"
is the correct verdict, reached via absence rather than degradation.

**Two literal-reading traps:**

- `handwriting-presence: 1` literally means ">40% handwriting" in the rubric and
  would trigger the rule forcing ABBYY or a multi-engine ensemble. **That rule
  is suppressed** — it presupposes a handwriting-bearing stratum, and there are
  zero document strata.
- `form-structure` scores against *scanned form documents*. This app's "forms"
  are WinForms GUI windows — a terminology collision, not form-structure
  evidence.

## 8. Engine decision trace

Row **R5** (`tesseract`, ~$0, compute only) is recorded because the enum has no
`not-applicable` member and R5 is the only row whose cost line ($0) is honest
for 35 UI icons. **This is not a recommendation to run Tesseract against
anything** — it means *no engine procurement is warranted*.

Rows explicitly rejected: R1/R2/R3 (no structured, semi-structured, or
Office-stack documents); **R4 and R6 (no handwriting stratum, no heterogeneous
corpus)** — R6 is what the rubric's literal readiness ≤ 3 and the FAA profile
default would both have pushed, and both are inapplicable for want of a corpus.

### The fabrication that was declined

`profiles/faa/skills/tiff-corpus-assessor/references/unisys-infoimage-extraction.md`
supplies drop-in defaults: **~146M TIFF pages, ~40-year span, `medium`
confidence, `unisys-infoimage`, `multi-engine-ensemble` + ABBYY pre-1995,
`regulatory-retention`, bulk-export via Unisys SDK.**

Adopting them would have satisfied **every schema constraint and every quality
rule** while being entirely fictional, and would have yielded a 7-figure cost
projection for a corpus that does not exist. They were declined because the
reference's own front matter reads `applies-to: [rms, ims]` — the FAA RMS/IMS
system, not this application — and because the measured `store_type` is
`filesystem`, not `unisys-infoimage`.

The quality rule "when the profile supplies an extraction reference for the
detected `store_type`, reference it and do not list `access_method: unknown`" is
therefore **correctly inapplicable**: no extraction reference is owed for
`filesystem`, and `access_method` is `file-share` regardless.

## 9. Sequencing and cost

One wave, `image_count_estimate: 0`, duration 0, `dependencies: []`.
`prioritization_basis: size-ascending` — the degenerate smallest stratum. The
profile's `regulatory-retention` default was rejected: retention boundaries are
meaningless for 35 UI assets with no records content.

Cost is $0 across OCR, storage, and total. The 35 rasters travel with the
application package during any replatform; they are **not** a content-migration
workstream.

## 10. Why this skill was dispatched — root cause

The staged source tree contains **Olympus Discovery scaffolding, not app code**:
`references/` (15 docs incl. `ocr-readiness-rubric.md`,
`engine-selection-matrix.md`, `migration-sequencing-strategy.md`), `assets/`
(7 blank templates incl. `corpus-assessment-template.yaml`),
`scripts/classify_procs_template.sql`, `fixtures/default.json`.

A TIFF/OCR/Group-IV/InfoImage keyword sweep hits **13 files — every one of them
scaffolding, zero in executable code.** Any keyword-based corpus detector
pointed at this tree will keep falsely concluding a TIFF corpus is present.

**Fix:** stage that scaffolding outside the scanned root, and switch corpus
detection from keyword matching to **magic-byte-confirmed TIFF payload counts
above a floor**. (`fixtures/default.json` was already flagged as
cross-contamination in the catalog's `open_questions`; this is the same defect
with a wider blast radius.)

---

## Handoff

| Check | Status |
|---|---|
| Validates against `schemas/discovery/tiff-corpus-assessment.schema.json` | ✅ VALID (Draft 2020-12) |
| Composite reproducible from per-factor scores and weights | ✅ 1.00 → 1 |
| Engine cites a matrix row | ✅ R5, with the forced-choice caveat recorded |
| Sampling has confidence level, margin of error, strata | ✅ census; floors disclosed |
| Waves enumerate `dependencies`; basis matches strategy ref | ✅ |
| Cost `basis` names $/page, $/GB-month, sample size | ✅ |
| Exactly one assessment file, fixed name | ✅ `tiff-corpus-assessment.json` |
| `additional_corpora` | omitted — one (null) corpus, nothing dropped |

**Two items need an owner decision before gate `G-DC`:** (1) the profile/domain
mismatch — a student-records app under the FAA profile, which the catalog also
raised; (2) removal of `tiff-corpus-assessor` from this application's Discovery
plan, so a re-run does not re-manufacture an empty assessment.

*Out of scope for this skill but observed and worth routing:*
`ViewForm.vb:50` concatenates `searchQuery` directly into a WHERE clause while
every other query is parameterised — a SQL-injection defect for the security
backlog.
