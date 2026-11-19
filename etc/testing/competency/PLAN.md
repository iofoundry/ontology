# Competency Tests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A `./competency` runner that loads each competency suite plus only its catalog-resolved imports, entails it with HermiT (cached by input hash), and validates the result with SHACL shapes and SPARQL-vs-expected-CSV tests, failing the build for `release/` suites and warning for `provisional/` suites.

**Architecture:** Catalog/closure/merge code moves out of `hygiene_runner.py` into a shared `ontology_closure.py`. Four new flat modules in `etc/scripts/` (matching the existing style, where scripts import each other by module name): suite discovery + tier check, entailment (HermiT via owlready2 in a killable subprocess, cached as N-Quads), checks (SHACL + SPARQL), and the CLI runner that maps findings to GitHub annotations by tier.

**Tech Stack:** Python 3.12, rdflib 7.1.4, owlready2 0.48 (bundled HermiT, needs Java), pySHACL 0.31.0, stdlib `unittest`. No new dependencies.

**Spec:** `etc/testing/competency/PROPOSAL.md` (read it first).

## Global Constraints

- Repo: `ontology`, branch `competency_tests_for_202604`. All paths below are relative to the repo root; run everything from the repo root.
- Never fetch from the web: every `owl:imports` IRI must resolve through `catalog-v001.xml` (root + optional suite overlay) or a suite file's own `owl:Ontology` IRI; anything else is a runner error. `owl:imports` triples are stripped before reasoning.
- Load only the suite's own import closure — never `AboutIOFDev.rdf`/`AboutIOFProd.rdf` into HermiT. `AboutIOFProd.rdf` is only walked as RDF for the tier check.
- Tier = parent directory: `etc/testing/competency/release/<suite>/` or `etc/testing/competency/provisional/<suite>/`.
- Severity: test failure or reasoner failure → `::error` in `release`, `::warning` in `provisional`. Runner-level problems (unresolved import, malformed test file, `.rq` without `.expected.csv`, tier violation) → `::error` in both. Exit 1 iff any `::error` was printed.
- Named graphs: `urn:asserted`, `urn:inferred`, `urn:closure`; default graph = union.
- HermiT defaults (same as hygiene): `--reasoner-timeout 3600` seconds, `--reasoner-memory 4g`; property-value inference (`-Y`) on.
- Cache dir: `build/competency/<tier>/<suite>/` holding `entailed.nq` and `result.json`; add `build/` to `.gitignore`.
- InformationSlot is **not** imported by the slots suite (it keeps `Fastener.ttl`'s stand-in declarations); slots is a `release` suite.
- `hygiene_runner.py` behaviour must not change: same annotations (order of `::notice` lines may differ), same exit status.
- No new dependencies: unit tests use stdlib `unittest`; run with `python -m unittest discover -s etc/scripts/tests -t etc/scripts`.

## Review Focus

- An import IRI missing from the catalog must be a clear runner error naming the IRI and the importing file — never a network fetch or an owlready hang. (Task 2 test `test_unresolved_import_is_error`.)
- An inconsistent example must report a tier-severity reasoner failure, skip that suite's tests, and let the other suites still run. (Task 3 `test_inconsistent_reports_failure`, Task 5 `test_inconsistent_suite_does_not_stop_others`.)
- A stale cache must never be used: changing any closure file (IOF module or suite ontology) changes the key; changing only `tests/` does not. (Task 3 `test_cache_key_*`.)
- pySHACL validates each named graph of a Dataset separately; shapes must see the union (a type in `urn:closure` + a property in `urn:asserted`). (Task 4 `test_shacl_sees_union`.)
- OPTIONAL-unbound cells and duplicate rows must compare correctly (empty cell; multiset, not set). (Task 4 `test_unbound_is_empty_cell`, `test_duplicate_rows_count`.)

---

### Task 1: Extract `ontology_closure.py` from the hygiene runner

**Files:**
- Create: `etc/scripts/ontology_closure.py`
- Modify: `etc/scripts/hygiene_runner.py` (replace `parse_catalog`, `find_imports`, `load_data`, `reasoner_input`, `HERMIT_DIR`/`HERMIT_CLASSPATH` with imports from the new module)
- Create: `etc/scripts/tests/__init__.py`, `etc/scripts/tests/test_ontology_closure.py`
- Create fixtures: `etc/scripts/tests/fixtures/closure/` — `catalog-v001.xml`, `A.ttl` (imports B), `B.ttl` (imports C), `C.rdf`, `Lang.ttl` (uses `rdf:langString` as an object)

**Interfaces:**
- Produces:
  - `CATALOG_NS = '{urn:oasis:names:tc:entity:xmlns:xml:catalog}'`
  - `load_catalog(path: Path) -> dict[str, Path]` — every `<uri>` entry (any suffix), values absolute, resolved against the catalog's folder.
  - `ontology_iri(path: Path) -> str` — the single `owl:Ontology` subject; raises `ClosureError` if zero or more than one.
  - `@dataclass Closure: iris: set[str]; files: list[Path]; missing: list[tuple[str, Path]]` — `missing` is `(import IRI, importing file)`.
  - `import_closure(root_iris: list[str], resolution: dict[str, Path]) -> Closure` — transitive `owl:imports` walk; each file parsed once; files in discovery order.
  - `merge(files: list[Path]) -> rdflib.Graph`
  - `reasoner_input(data: Graph, path: Path) -> None` (moved verbatim: drops `owl:imports`, `rdf:langString → rdf:PlainLiteral`, writes N-Triples)
  - `class ClosureError(Exception)`
  - `HERMIT_CLASSPATH: str` (moved verbatim)

- [ ] **Step 1: Capture hygiene baseline** — `python etc/scripts/hygiene_runner.py AboutIOFDev.rdf AboutIOFProd.rdf --no-reasoner > /tmp/hygiene_before.txt; echo $? >> /tmp/hygiene_before.txt`
- [ ] **Step 2: Write failing tests** in `test_ontology_closure.py`:

```python
def test_closure_follows_imports(self):
    res = load_catalog(FIX / 'catalog-v001.xml')
    c = import_closure([A_IRI], res)
    self.assertEqual({p.name for p in c.files}, {'A.ttl', 'B.ttl', 'C.rdf'})
    self.assertEqual(c.missing, [])

def test_missing_import_reported_with_importer(self):
    res = load_catalog(FIX / 'catalog-v001.xml'); del res[C_IRI]
    c = import_closure([A_IRI], res)
    self.assertEqual(c.missing, [(C_IRI, FIX / 'B.ttl')])

def test_ontology_iri_requires_exactly_one(self):
    self.assertEqual(ontology_iri(FIX / 'A.ttl'), A_IRI)
    with self.assertRaises(ClosureError):
        ontology_iri(FIX / 'NoHeader.ttl')   # add this fixture: triples, no owl:Ontology

def test_reasoner_input_strips_imports_and_langstring(self):
    g = merge([FIX / 'A.ttl', FIX / 'Lang.ttl']); out = TMP / 'x.nt'
    reasoner_input(g, out); r = Graph().parse(out)
    self.assertFalse(list(r.triples((None, OWL.imports, None))))
    self.assertFalse(list(r.triples((None, None, RDF.langString))))
```

- [ ] **Step 3: Run** `python -m unittest discover -s etc/scripts/tests -t etc/scripts -v` — expect ImportError (module missing).
- [ ] **Step 4: Implement `ontology_closure.py`** and rewire `hygiene_runner.py`: `find_ontologies` builds its old relative `resolution` as `{iri: os.path.relpath(p, folder) for iri, p in load_catalog(...).items() if p.suffix == '.rdf'}` (keeps the `.rdf` filter and the relative `file=` paths), calls `import_closure`, and prints the old `::notice`/`::warning` lines from `Closure.files`/`Closure.missing`.
- [ ] **Step 5: Run unit tests** — expect PASS.
- [ ] **Step 6: Re-run hygiene** into `/tmp/hygiene_after.txt`; `diff <(sort /tmp/hygiene_before.txt) <(sort /tmp/hygiene_after.txt)` — expect no output.
- [ ] **Step 7: Commit** `git add etc/scripts/ontology_closure.py etc/scripts/hygiene_runner.py etc/scripts/tests && git commit -m "Extract catalog/import-closure helpers into ontology_closure"`

### Task 2: Suite discovery, closure resolution and tier check

**Files:**
- Create: `etc/scripts/competency_suite.py`
- Create: `etc/scripts/tests/test_competency_suite.py`
- Create fixtures `etc/scripts/tests/fixtures/competency/`: `catalog-v001.xml`; `AboutProd.ttl` (imports `Core.ttl`); `Core.ttl`; `DevOnly.ttl` (not imported by AboutProd); suites `release/good/Example.ttl` (imports Core) + `tests/Types.shapes.ttl` + `tests/Q.rq` + `tests/Q.expected.csv`; `release/leaky/Example.ttl` (imports DevOnly); `release/unresolved/Example.ttl` (imports `https://example.org/nowhere/`); `provisional/dev/Example.ttl` (imports DevOnly)

**Interfaces:**
- Consumes: Task 1 `load_catalog`, `ontology_iri`, `import_closure`, `Closure`, `ClosureError`.
- Produces:
  - `TIERS = ('release', 'provisional')`
  - `@dataclass Suite: name: str  # e.g. 'release/slots'; tier: str; root: Path; ontology_files: list[Path]; shapes_tests: list[Path]; sparql_tests: list[Path]`
  - `discover_suites(base: Path, selectors: list[str]) -> list[Suite]` — `selectors` empty → all; `'release'` → a tier; `'release/slots'` → one suite. Ontologies = `*.ttl|*.rdf` directly in the suite root; `shapes_tests` = `tests/*.shapes.ttl`; `sparql_tests` = `tests/*.rq`. Sorted by name. Unknown selector → `SuiteError`.
  - `class SuiteError(Exception)` — runner-level (always `::error`).
  - `resolve_suite(suite: Suite, root_catalog: Path) -> Closure` — root catalog, then `suite.root / 'catalog-v001.xml'` overlay if present (overlay wins), then each suite file under `ontology_iri(file)`; roots = suite file IRIs. Raises `SuiteError` listing every `(iri, importer)` in `missing`.
  - `tier_violations(suite: Suite, closure: Closure, prod_about: Path, root_catalog: Path) -> list[str]` — `[]` for provisional; for release, sorted IRIs in `closure.iris` that are neither a suite file's IRI nor in the prod about file's closure (registered by its own `ontology_iri`).

- [ ] **Step 1: Write failing tests:** `test_discover_all_and_selectors` (all → 4 names sorted; `['release']` → 3; `['release/good']` → 1 with 1 shapes test and 1 sparql test; `['nope']` raises `SuiteError`), `test_resolve_good_suite` (closure files = Example.ttl + Core.ttl), `test_unresolved_import_is_error` (message contains `https://example.org/nowhere/` and `Example.ttl`), `test_release_leak_is_violation` (`tier_violations` → `[DEVONLY_IRI]`), `test_provisional_has_no_violations`.
- [ ] **Step 2: Run** — expect ImportError.
- [ ] **Step 3: Implement `competency_suite.py`.**
- [ ] **Step 4: Run** — expect PASS.
- [ ] **Step 5: Commit** `"Add competency suite discovery and tier check"`

### Task 3: Entailment worker with content-hash cache

**Files:**
- Create: `etc/scripts/competency_entail.py`
- Create: `etc/scripts/tests/test_competency_entail.py`
- Create fixtures `etc/scripts/tests/fixtures/entail/`: `Defined.ttl` — `:A ≡ :B and (:p some :C)`, `:x a :B ; :p :y`, `:y a :C`, `:B rdfs:subClassOf :Top`; `Inconsistent.ttl` — `:D owl:disjointWith :E`, `:z a :D, :E`

**Interfaces:**
- Consumes: Task 1 `merge`, `reasoner_input`.
- Produces:
  - `ASSERTED, INFERRED, CLOSURE = URIRef('urn:asserted'), URIRef('urn:inferred'), URIRef('urn:closure')`
  - `@dataclass EntailResult: dataset: rdflib.Dataset | None; unsatisfiable: list[str]; failure: str | None  # 'inconsistent' | 'timeout' | 'error: <detail>'; seconds: float; cached: bool`
  - `cache_key(files: list[Path], property_values: bool) -> str` — sha256 over sorted `(path relative to repo root, sha256(file bytes))` + `owlready2.VERSION` + `property_values` + schema `'1'`.
  - `entail(files: list[Path], cache_dir: Path, *, timeout: float, memory: str, property_values: bool = True, use_cache: bool = True) -> EntailResult` — on cache hit (`result.json` key matches and `failure` is null) loads `entailed.nq`; otherwise writes `reasoner_input` to `cache_dir/closure.nt`, runs `python etc/scripts/competency_entail.py --worker <closure.nt> <cache_dir> --memory M [--no-property-values]` via `subprocess.Popen(start_new_session=True)`, and on timeout kills the whole process group (`os.killpg`) so the HermiT JVM dies too. Writes `result.json` = `{key, unsatisfiable, failure, seconds}`; never caches a failure.
  - Worker (`__main__ --worker`): owlready2 `World`, load closure.nt with `format='ntriples'`, set `owlready2.reasoning.JAVA_MEMORY`, `sync_reasoner_hermit(world, infer_property_values=…)`; split into the three graphs exactly as `~/projects/IOF/ConnectSpec/bolt/sparql_shell.py` `entail()` + `add_closure()` do (copy that logic, including the "ground triple not in input → inferred" rule and literal-by-text comparison); `unsatisfiable` = IRIs of `world.inconsistent_classes()`; `OwlReadyInconsistentOntologyError` → `failure='inconsistent'`. Serialize dataset as N-Quads to `entailed.nq`.

- [ ] **Step 1: Write failing tests:** `test_defined_class_inferred` (`(:x, RDF.type, :A)` in INFERRED graph, not in ASSERTED; `(:x, RDF.type, :Top)` in CLOSURE), `test_inconsistent_reports_failure` (`failure == 'inconsistent'`, `dataset is None`), `test_cache_hit_skips_reasoner` (second call → `cached is True`, `seconds < 2`), `test_cache_key_changes_with_input` (copy fixture to tmp, append a triple → different key), `test_cache_key_ignores_other_files` (key over the same file list unchanged after writing an unrelated file in the folder), `test_timeout_kills_worker` (`timeout=0.5` → `failure == 'timeout'`, and no `HermiT` process left: `subprocess.run(['pgrep','-f','org.semanticweb.HermiT'])` returncode 1).
- [ ] **Step 2: Run** — expect ImportError.
- [ ] **Step 3: Implement `competency_entail.py`.**
- [ ] **Step 4: Run** — expect PASS (needs Java; ~10–20 s total).
- [ ] **Step 5: Add `build/` to `.gitignore`.**
- [ ] **Step 6: Commit** `"Add HermiT entailment worker with content-hash cache"`

### Task 4: SHACL and SPARQL checks

**Files:**
- Create: `etc/scripts/competency_checks.py`
- Create: `etc/scripts/tests/test_competency_checks.py` (builds small in-memory Datasets; no HermiT)

**Interfaces:**
- Consumes: Task 3 graph names.
- Produces:
  - `@dataclass Finding: kind: str  # 'failure' | 'warning' | 'info' | 'broken'; file: Path; title: str; message: str`
  - `union_graph(ds: Dataset) -> Graph` — a plain `Graph` of every quad's triple. **pySHACL must be given this, never the Dataset** (it validates each named graph separately).
  - `run_shacl(shapes: Path, ds: Dataset) -> list[Finding]` — `validate(union, shacl_graph=..., advanced=True, inference='none', allow_warnings=True)`; `sh:Violation` → `failure`, `sh:Warning` → `warning`, `sh:Info` → `info`; message = `sh:resultMessage` with focus node; title = shape `rdfs:label` or the file stem. Unparseable shapes → one `broken`.
  - `query_prefixes(text: str) -> dict[str, str]` — from `PREFIX p: <iri>` lines.
  - `render_term(term, prefixes) -> str` — `None` → `''`; IRI → `p:local` when it starts with a prefix IRI and `local` matches `[A-Za-z0-9_.-]*`, else the bare IRI; Literal → lexical form; BNode → `_:b`.
  - `run_sparql(query: Path, ds: Dataset) -> tuple[list[str], list[tuple[str, ...]]]` — header + rows; ASK → `(['ask'], [('true',)])` or `false`. Parse errors raise `ValueError`.
  - `compare_rows(expected: list[tuple], actual: list[tuple]) -> tuple[list[tuple], list[tuple]]` — `(missing, unexpected)` via `collections.Counter`.
  - `read_expected(path: Path) -> tuple[list[str], list[tuple]]` / `write_expected(path, header, rows)` — `csv` module, header row first, rows sorted.
  - `check_sparql(query: Path, ds: Dataset, update: bool) -> list[Finding]` — expected path = `query.with_suffix('.expected.csv')`; missing file and not `update` → `broken`; header mismatch → `failure`; one `failure` per missing/unexpected row (`"missing row: a, b"` / `"unexpected row: a, b"`); `update=True` writes the file and returns `[]`.

- [ ] **Step 1: Write failing tests:** `test_shacl_sees_union` (type in CLOSURE + `sh:property [sh:path ex:p; sh:minCount 1]` satisfied by a triple in ASSERTED → no findings), `test_shacl_violation_is_failure`, `test_unbound_is_empty_cell` (OPTIONAL var → `''`), `test_duplicate_rows_count` (expected 2× row, actual 1× → one missing), `test_render_compacts_with_query_prefixes`, `test_graph_names_visible` (`GRAPH ?g` query returns `urn:inferred`), `test_ask_true`, `test_missing_expected_is_broken`, `test_update_writes_sorted_csv`.
- [ ] **Step 2: Run** — expect ImportError.
- [ ] **Step 3: Implement `competency_checks.py`.**
- [ ] **Step 4: Run** — expect PASS.
- [ ] **Step 5: Commit** `"Add SHACL and SPARQL competency checks"`

### Task 5: Runner CLI, tier severity and wrapper

**Files:**
- Create: `etc/scripts/competency_runner.py`, `competency` (repo root, executable: `#!/bin/sh` / `python etc/scripts/competency_runner.py "$@"`)
- Create: `etc/scripts/tests/test_competency_runner.py` (runs `main()` against the Task 2 fixtures with `--base`, `--catalog`, `--prod-about`, `--build-dir` pointing at fixtures/tmp, captures stdout)

**Interfaces:**
- Consumes: Tasks 1–4.
- Produces:
  - CLI: `competency_runner.py [SELECTOR ...] [--no-cache] [--update-expected] [--jobs N (default 1)] [--reasoner-timeout 3600] [--reasoner-memory 4g] [--base etc/testing/competency] [--catalog catalog-v001.xml] [--prod-about AboutIOFProd.rdf] [--build-dir build/competency]`
  - `annotation_level(tier: str, kind: str) -> str` — `broken` → `::error`; `failure` → `::error` if release else `::warning`; `warning` → `::warning`; `info` → `::notice`.
  - `main(argv: list[str] | None = None) -> int` — per suite: `::group::<name>` → resolve (SuiteError → `::error`, skip suite) → tier check (each IRI → `::error title=Tier::release suite <name> depends on provisional module <iri> — move the suite to provisional/`) → entail (failure / each unsatisfiable class → `annotation_level(tier,'failure')`, skip tests when `dataset is None`) → every shapes test and sparql test → annotations with `file=<test path relative to repo root>` → `::endgroup::` → a per-suite pass/fail `::notice`. With `--jobs > 1`, entailment of different suites runs concurrently (`ThreadPoolExecutor` over `entail`, which already isolates work in subprocesses); output stays grouped per suite in name order. Returns 1 iff any `::error` printed.

- [ ] **Step 1: Write failing tests:** `test_release_failure_is_error` (fixture `release/good` with a deliberately wrong `Q.expected.csv` row → `::error` and exit 1), `test_provisional_failure_is_warning` (same wrong expectation under `provisional/dev` → `::warning`, exit 0), `test_leaky_release_is_tier_error`, `test_unresolved_import_is_error_and_others_run` (output still contains the `release/good` group), `test_inconsistent_suite_does_not_stop_others` (add fixture `release/broken/Example.ttl` with the Task 3 inconsistency → its `::error`, `release/good` still evaluated), `test_update_expected_writes_file`.
- [ ] **Step 2: Run** — expect ImportError.
- [ ] **Step 3: Implement `competency_runner.py` and `competency`.**
- [ ] **Step 4: Run** — expect PASS.
- [ ] **Step 5: Commit** `"Add competency test runner"`

### Task 6: Move the slots suite to `release/` and write its tests

**Files:**
- Move: `etc/testing/competency/slots/{Fastener.ttl,FastenerExample.ttl}` → `etc/testing/competency/release/slots/`
- Create: `etc/testing/competency/release/slots/tests/SpecConformance.rq`, `BoltInference.rq` (copied verbatim from `~/projects/IOF/ConnectSpec/bolt/fastener/`), `BoltTypes.shapes.ttl`, and the two generated `*.expected.csv`
- Create: `etc/testing/competency/README.md` — short how-to: suite layout, tiers, test kinds, `./competency` usage, `--update-expected`, the InformationSlot note (PROPOSAL decisions 4–5)

**Interfaces:**
- Consumes: the `./competency` CLI from Task 5.

- [ ] **Step 1: Move files and copy the two queries.**
- [ ] **Step 2: Write `BoltTypes.shapes.ttl`**: node shape targeting `ex:Bolt01` with `sh:class fst:ButtonHeadSocketCapBolt` (Bolt01 is asserted only `iof:MaterialArtifact`, so this proves the defined-class inference), and a shape `sh:targetClass iof:ValueSlot` with `sh:property [ sh:path iof:hasFiller ; sh:minCount 1 ]`; each with an `rdfs:label` and `sh:message`.
- [ ] **Step 3: Run** `./competency release/slots --update-expected` (first run ~3 min of HermiT). Expect: no `::error`, two `.expected.csv` files written.
- [ ] **Step 4: Review generated expectations**: `SpecConformance.expected.csv` has exactly 6 data rows, all with status `ok`; `BoltInference.expected.csv` contains a row with `fst:ButtonHeadSocketCapBolt` and source `inferred`. If not, stop and report — that is a real finding, not something to paper over.
- [ ] **Step 5: Run** `./competency release/slots` twice. Expect: both pass; second run reports a cache hit and finishes in seconds.
- [ ] **Step 6: Negative check**: temporarily change one value in `SpecConformance.expected.csv` → `./competency release/slots` exits 1 with a `missing row`/`unexpected row` `::error`; revert.
- [ ] **Step 7: Commit** `"Add release slots competency suite"`

### Task 7: CI job

**Files:**
- Modify: `.github/workflows/build.yml`

- [ ] **Step 1:** Add `etc/testing/competency/**` and `competency` to `on.push.paths`. Add job `competency-tests` (ubuntu-latest, Python 3.12, Temurin Java 21, `pip install -r ./etc/scripts/requirements.txt`) with steps: `python -m unittest discover -s etc/scripts/tests -t etc/scripts`; `actions/cache@v4` on `build/competency` with `key: competency-${{ hashFiles('**/*.rdf', 'etc/testing/competency/**/*.ttl', 'etc/testing/competency/**/*.rdf', 'catalog-v001.xml') }}` and `restore-keys: competency-` (the runner's own per-suite key decides validity); `./competency`.
- [ ] **Step 2: Validate** — `ruby -ryaml -e 'YAML.load_file(".github/workflows/build.yml")'` succeeds (pyyaml is not a dependency); after push, the job runs and passes (check the Actions tab).
- [ ] **Step 3: Commit** `"Run competency tests in CI"`
