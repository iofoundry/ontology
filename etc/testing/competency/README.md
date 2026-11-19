# Competency tests

Competency tests check that IOF does the job: a worked example is loaded on top of the
IOF modules it imports, entailed with HermiT, and its expected inferences and
conformance results are checked. (Hygiene tests, in `etc/testing/hygiene_shapes`,
check that IOF is well-formed.)

## Layout

```
etc/testing/competency/
  release/<suite>/        failures are errors: they block the build
  provisional/<suite>/    failures are warnings
    *.ttl, *.rdf          the suite's ontologies (examples)
    catalog-v001.xml      optional: extra IRI → file mappings for this suite only
    tests/
      <name>.shapes.ttl   SHACL test: the entailed graph must conform
      <name>.rq           SPARQL test, compared with ...
      <name>.expected.csv ... these results (header row, then rows; order ignored)
```

- **Imports.** A suite loads only its own files and what they `owl:imports`,
  resolved through the repo-root `catalog-v001.xml` (plus the suite's overlay). An
  import that is not in a catalog is an error; nothing is fetched from the web. Keep
  imports to the minimum the example needs — every extra module makes HermiT slower.
- **Tiers.** A `release/` suite may only import modules that are part of
  `AboutIOFProd.rdf`; importing a provisional module is an error (move the suite to
  `provisional/`).
- **Graphs.** Queries see three named graphs, and the default graph is their union:
  `<urn:asserted>` (the files), `<urn:inferred>` (what HermiT adds) and
  `<urn:closure>` (every named superclass of each type). Use `GRAPH ?g { … }` to tell
  asserted from inferred.
- **SHACL or SPARQL?** Use SHACL Core when it can say it (e.g. "Bolt01 has type X":
  `sh:targetNode` + `sh:class`). If the check would only be a `sh:sparql` wrapper — or
  needs `GRAPH` — write a `.rq` with an `.expected.csv`.
- **Expected CSV.** IRIs are written with the query's own `PREFIX`es (otherwise in
  full), literals by their text, unbound values as empty cells. An `ASK` query has the
  column `ask` and the row `true` or `false`.

## Running

```bash
./competency                                   # every suite
./competency provisional                       # one tier
./competency provisional/slots                 # one suite
./competency provisional/slots --no-cache      # force HermiT
./competency provisional/slots --update-expected   # (re)write the .expected.csv files
python -m unittest discover -s etc/scripts/tests -t etc/scripts   # the runner's own tests
```

HermiT results are cached in `build/competency/<tier>/<suite>/` keyed on the content
of every file in the suite's import closure, so re-running after changing only
`tests/` takes seconds. (Pre-entailing IOF and layering an example on top does not
help: HermiT has no incremental mode and re-classifies everything from the axioms — on
the slots suite, 185 s with IOF's entailments preloaded vs 192 s from scratch.) After
`--update-expected`, review the CSV diff before committing: it is the test.

## Suites

- **provisional/slots** — the ConnectSpec Fastener example (an M6×25 button head socket
  cap bolt and its design specification built with information slots). Checks that the
  bolt's type is inferred from its parts (`BoltTypes.shapes.ttl`, `BoltInference.rq`)
  and that every prescribed quality conforms to its specification
  (`SpecConformance.rq`). `Fastener.ttl` imports the provisional InformationSlot
  module, so the suite is provisional while that module is only in `AboutIOFDev.rdf`.
  HermiT takes about 5½ min on it (about 3 min without the module). It took 33 min
  while `time slot` was defined with `has filler only (temporal duration value
  expression or temporal instant value expression)`: a union inside a universal
  restriction makes HermiT branch at every slot. The module now restricts fillers to
  one named parent, `temporal value expression`. Keep unions out of `only` fillers.
