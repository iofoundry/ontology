# Competency tests — implementation proposal (for review)

Status: draft for review, nothing built yet. Branch `competency_tests_for_202604`.

## Intent

Hygiene tests (`etc/scripts/hygiene_runner.py`) check that IOF is well-formed and
consistent. Competency tests check that IOF *does the job*: load a worked example
(e.g. the Fastener/bolt slots example) on top of the release, entail it with HermiT,
and assert that the expected inferences and conformance results come out. A
regression in IOF that breaks an example's inferences should fail the build.

## Layout

```
etc/scripts/
  ontology_closure.py      # NEW shared lib: catalog parsing, import closure, merge, HermiT
  hygiene_runner.py        # refactored to import ontology_closure (no behaviour change)
  competency_runner.py     # NEW runner
competency                 # NEW wrapper script at repo root, like ./hygiene
etc/testing/competency/
  provisional/             # suites that need Provisional (AboutIOFDev) modules — failures are warnings
  release/                 # suites over Release (AboutIOFProd) modules — failures are errors
    slots/                 # one directory = one suite
      Fastener.ttl         # test ontologies: every *.ttl / *.rdf at the suite's top level
      FastenerExample.ttl
      catalog-v001.xml     # OPTIONAL overlay, only if a suite needs extra local mappings
      tests/
        BoltTypes.shapes.ttl            # SHACL test: must conform
        SpecConformance.rq              # SPARQL test ...
        SpecConformance.expected.csv    # ... compared against static results
        BoltInference.rq
        BoltInference.expected.csv
```

The suite's tier is its parent directory (`release/` or `provisional/`). The slots
suite moves to `etc/testing/competency/release/slots/`: it does not import the
provisional InformationSlot module (see Decisions), and everything it does import
(Core, AnnotationVocabulary, BFO, SupplyChain, four Biopharma modules) is in
`AboutIOFProd`'s closure — checked.

Convention over configuration: no per-suite manifest. Anything `*.ttl|*.rdf` at the
suite root is loaded as a test ontology; `tests/*.shapes.ttl` are SHACL tests;
`tests/*.rq` with a sibling `*.expected.csv` are SPARQL tests. (A small `suite.ttl`
manifest can be added later if a suite needs options such as "no reasoning".)

## Loading — catalog only, never the web

1. Read the repo-root `catalog-v001.xml` (+ the suite overlay, if any).
2. Register each suite file under its own `owl:Ontology` IRI (read from the file), so
   suites don't need their own catalog for their own files.
3. Walk `owl:imports` transitively from the suite files. **Any import IRI not in the
   catalog is a hard error** (`::error`), never fetched. This is the same resolution
   the hygiene runner already does — factor it into `ontology_closure.py` rather than
   copying it (and drop the `.rdf`-only filter so `.ttl` resolves too).
4. Merge with rdflib, strip `owl:imports`, apply the existing `rdf:langString →
   rdf:PlainLiteral` fix (`reasoner_input`), write one N-Triples file.

**Imports stay minimal.** A suite loads only its own files and what they
transitively import — never all of `AboutIOFDev`/`AboutIOFProd`, which would make
HermiT do far more work than the test needs.

**Tier check (proposed, my call).** For a `release/` suite, every module in the
import closure must also be in `AboutIOFProd`'s closure. A release suite that pulls
in a Provisional-only module is an `::error` ("release suite depends on provisional
module X — move the suite to provisional/"). Provisional suites may import anything
in the catalog. This keeps the release/provisional split honest without loading
either About file into HermiT (the About closures are only walked as RDF, ~1 s).

Spike: the slots suite resolves to 10 files / 17.7k triples in 1.5 s, no misses.

## Entailment

Run HermiT through owlready2 (`sync_reasoner_hermit(..., infer_property_values=True)`),
the same way `ConnectSpec/bolt/sparql_shell.py` does, and keep its three-graph dataset:

| graph | contents |
|---|---|
| `<urn:asserted>` | suite files + IOF imports |
| `<urn:inferred>` | what HermiT adds (incl. inverse values owlready writes into the source ontology) |
| `<urn:closure>`  | every named superclass of each type (owlready keeps only the most specific) |

Default graph = union. SPARQL tests can use `GRAPH ?g` to tell asserted from inferred
(BoltInference needs this); SHACL tests validate the union.

Write the dataset to `build/competency/<suite>/entailed.nq` — useful as a CI artifact
and for debugging a failing test locally.

### Does pre-entailing IOF and layering the examples on top save time? — No.

Measured on the slots suite (M-series Mac, Java 27, owlready2 0.48):

| run | HermiT time |
|---|---|
| A. IOF closure + examples, from scratch | **192 s** |
| B. IOF closure alone (the part we could cache) | 54 s |
| C. IOF's entailments pre-loaded as asserted triples + examples | **185 s** |
| A without `infer_property_values` (`-Y`) | 160 s |

HermiT has no incremental mode: it always rebuilds its tableau and re-classifies the
whole TBox from axioms. Pre-entailed triples are just more (redundant) axioms to it, so
C ≈ A. And the examples aren't "just ABox" — `Fastener.ttl` adds defined classes
(the bolt taxonomy by head/drive), which forces IOF to be re-classified with them
anyway. ~3× the IOF-only cost comes from the examples, not from IOF.

What *does* save time:

1. **Cache the entailed result, keyed by content hash** of every file in the closure
   (+ HermiT/owlready version). Unchanged inputs → load `entailed.nq` in < 1 s and go
   straight to the tests. In CI, `actions/cache` on `build/competency/` keyed on that
   hash; PRs that only touch shapes/queries/expected results skip HermiT entirely, and
   local iteration on a test is instant. `--no-cache` forces a re-run.
2. **Run suites in parallel** (one JVM per suite, `--jobs N`).
3. **Keep suite imports minimal.** Fastener imports Biopharma attributes/material; if
   it only needs a few terms, importing less shrinks every run.
4. Make `-Y` (property-value inference) a per-suite option: ~30 s here; only needed
   when a test checks inferred property values.

Not recommended: substituting a rule reasoner (OWL RL/`owlrl`) on a pre-classified IOF
for speed. It's incomplete for exactly the defined-class inferences (bolt types)
these tests exist to check.

## Validation — SHACL first, SPARQL when it's really SPARQL

Rule of thumb (your preference): if the check can be written in **SHACL Core**, it's a
shapes file. If the SHACL would just wrap a `sh:sparql` query, write the query directly
and compare to static results.

**SHACL tests** (`tests/*.shapes.ttl`) — validated against the entailed union with
pySHACL (`inference='none'`; HermiT already did it). Pass = no `sh:Violation`.
Warnings/Info print as annotations. Good for:

```turtle
ex:Bolt01Shape a sh:NodeShape ;
    sh:targetNode ex:Bolt01 ;
    sh:class fst:ButtonHeadSocketCapBolt ;          # expected inferred type
    sh:message "Bolt01 should be inferred to be a button head socket cap bolt" .

ex:ValueSlotFilled a sh:NodeShape ;
    sh:targetClass iof:ValueSlot ;
    sh:property [ sh:path iof:hasFiller ; sh:minCount 1 ] .
```

**SPARQL tests** (`tests/X.rq` + `tests/X.expected.csv`):

- `SpecConformance.rq` → SPARQL. Its comparison crosses two paths (quality's value vs
  the spec's value-slot filler) and computes a status; SHACL Core's `sh:equals` can't
  express that, so it would be SHACL-SPARQL anyway. Expected file: today it yields 6
  rows, all `ok`. A future negative example (a deliberately non-conforming bolt)
  would show up as a `value mismatch` row in the expected file — negative tests for
  free.
- `BoltInference.rq` → SPARQL. It distinguishes asserted vs inferred via `GRAPH ?g`,
  which SHACL can't see. (The plain "Bolt01 has type X" part could be SHACL as above.)
- `ASK` queries: expected file contains `true`/`false`.

Comparison: run the query on the dataset, render each row as CSV (IRIs compacted with
the query's prefixes, literals by lexical form, blank nodes as `_:b`), and compare as
an **unordered multiset** of rows. On mismatch print a row diff (missing / unexpected)
as `::error` annotations. `competency_runner.py --update-expected` regenerates the
`.expected.csv` files so changes are reviewed as a normal diff in the PR.

Why CSV over SPARQL-JSON results: readable and diffable in review; the loss of
literal datatypes doesn't matter for these checks (use `STR()`/`DATATYPE()` in the
query if a test cares).

## Result handling by tier

| tier | test failure | HermiT inconsistent / unsatisfiable / timeout |
|---|---|---|
| `release/` | `::error` — blocks the build | `::error` |
| `provisional/` | `::warning` — reported, does not block | `::warning` |

Same model as the hygiene runner's maturity handling (`annotation_level`).
Runner-level problems (an import missing from the catalog, a malformed test file, a
missing `.expected.csv`) are `::error` in both tiers — those are broken tests, not
findings.

## Runner & CI

```
./competency                                  # all suites, both tiers
./competency release                          # one tier
./competency release/slots --no-cache     # one suite, force HermiT
./competency release/slots --update-expected
```

Output follows the hygiene runner: GitHub `::group::`/`::error`/`::notice`
annotations with `file=` pointing at the failing test file; exit 1 on any failure.
An inconsistent example or an unsatisfiable class is itself a failure.

CI: a `competency-tests` job in `build.yml` alongside hygiene (paths: `**/*.rdf`,
`etc/testing/competency/**`, `etc/scripts/*.py`), Java 21 + `actions/cache` for
`build/competency`. No new dependencies — owlready2, rdflib, pyshacl are already in
`etc/scripts/requirements.txt`.

## Decisions

1. Release suites block the build; provisional suites report warnings (see the
   table above).
2. Tier is set by directory (`release/` / `provisional/`). Imports come only from
   the suite's own `owl:imports`, kept to the minimum; About files are never loaded.
3. Biopharma stays if Fastener needs it — same minimal-imports rule applies.

4. **InformationSlot is not imported for now.** `Fastener.ttl` keeps its local
   stand-in declarations of `iof:ValueSlot` etc. (parent class only), because the
   full module makes HermiT ~10× slower (~30 min). Consequence, accepted: the slots
   suite tests the Fastener example on Release IOF, not the InformationSlot module.
   The suite is a **release** suite until this is re-evaluated.
5. **Revisit when InformationSlot is ready** (reasons in reasonable time): refactor
   `Fastener.ttl` to import the module and drop the stand-ins, then re-time HermiT and
   re-decide the tier — the tier check will force it to `provisional/` while
   InformationSlot is still only in `AboutIOFDev`.

## Left to the builder

Exact CSV rendering of literals; parallelism mechanics; the cache-key file format;
whether `ontology_closure.py` also absorbs `check_module_iris.py`'s catalog parsing.
