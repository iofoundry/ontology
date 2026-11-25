"""Entail a competency suite's closure with HermiT, caching the result by input hash.

HermiT runs through owlready2 in a worker subprocess (``--worker``) in its own process
group, so a timeout kills the JVM too. The result is a Dataset of three named graphs
(default graph = their union):

    <urn:asserted>   the input triples
    <urn:inferred>   what HermiT adds
    <urn:closure>    every named superclass of each type (owlready keeps only the most
                     specific types, so '?x a iof:Quality' would otherwise miss subclasses)

The cache lives in <cache_dir>/entailed.nq + result.json, keyed by the content of every
input file; a failed run is never cached.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from rdflib import BNode, Dataset, Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS

from ontology_closure import merge, reasoner_input

ASSERTED, INFERRED, CLOSURE = URIRef('urn:asserted'), URIRef('urn:inferred'), URIRef('urn:closure')
INFERENCE_ONTOLOGY = 'http://inferrences/'     # where owlready2 stores what the reasoner adds
REPO_ROOT = Path(__file__).resolve().parents[2]
CACHE_SCHEMA = '1'
# The entailment code is part of the cache key: changing how the input is prepared or how
# triples are split into graphs must invalidate every cached result.
CODE_FILES = [Path(__file__).resolve(), Path(__file__).resolve().parent / 'ontology_closure.py']


@dataclass
class EntailResult:
    dataset: Dataset | None
    unsatisfiable: list[str]
    failure: str | None      # 'inconsistent' | 'timeout' | 'error: <detail>'
    seconds: float
    cached: bool


def cache_key(files: list[Path], property_values: bool) -> str:
    import owlready2
    digest = hashlib.sha256()
    for name, content in sorted((os.path.relpath(Path(f).resolve(), REPO_ROOT),
                                 hashlib.sha256(Path(f).read_bytes()).hexdigest()) for f in files):
        digest.update(f'{name}\0{content}\n'.encode())
    for code in CODE_FILES:
        digest.update(hashlib.sha256(Path(code).read_bytes()).digest())
    digest.update(f'owlready2={owlready2.VERSION}\0pv={property_values}\0schema={CACHE_SCHEMA}'.encode())
    return digest.hexdigest()


def asserted_dataset(files: list[Path]) -> Dataset:
    """The input triples alone, in <urn:asserted> (no reasoner): for questions with
    '# reasoning: false'. Parsed from the files, so it does not depend on whether HermiT ran."""
    ds = Dataset(default_union=True)
    asserted = ds.graph(ASSERTED)
    for triple in merge(files):
        asserted.add(triple)
    return ds


def _load(path: Path) -> Dataset:
    ds = Dataset(default_union=True)
    ds.parse(str(path), format='nquads')
    return ds


def entail(files: list[Path], cache_dir: Path, *, timeout: float, memory: str,
           property_values: bool = True, use_cache: bool = True) -> EntailResult:
    start = time.monotonic()
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = cache_key(files, property_values)
    result_file, nq = cache_dir / 'result.json', cache_dir / 'entailed.nq'
    if use_cache and result_file.exists() and nq.exists():
        previous = json.loads(result_file.read_text())
        if previous.get('key') == key and previous.get('failure') is None:
            return EntailResult(_load(nq), previous['unsatisfiable'], None, time.monotonic() - start, True)

    result_file.unlink(missing_ok=True)
    nq.unlink(missing_ok=True)
    closure = cache_dir / 'closure.nt'
    reasoner_input(merge(files), closure)
    command = [sys.executable, str(Path(__file__).resolve()), '--worker', str(closure), str(cache_dir),
               '--memory', memory] + ([] if property_values else ['--no-property-values'])
    worker = subprocess.Popen(command, start_new_session=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True)
    try:
        output, _ = worker.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(worker.pid, signal.SIGKILL)
        worker.communicate()
        return EntailResult(None, [], 'timeout', time.monotonic() - start, False)

    report_file = cache_dir / 'worker.json'
    if worker.returncode != 0 or not report_file.exists():
        detail = next((line for line in reversed(output.splitlines()) if line.strip()), 'no output')
        return EntailResult(None, [], 'error: ' + detail, time.monotonic() - start, False)
    report = json.loads(report_file.read_text())
    report_file.unlink()
    seconds = time.monotonic() - start
    if report['failure']:
        return EntailResult(None, [], report['failure'], seconds, False)
    result_file.write_text(json.dumps({'key': key, 'unsatisfiable': report['unsatisfiable'],
                                       'failure': None, 'seconds': round(seconds, 1)}, indent=1))
    return EntailResult(_load(nq), report['unsatisfiable'], None, seconds, False)


# --- worker (runs in its own process) ---------------------------------------------------

def _split(world, source: Graph) -> Dataset:
    """Asserted vs inferred triples, as in ConnectSpec/bolt/sparql_shell.py."""
    everything = world.as_rdflib_graph()
    inference_onto = world.get_ontology(INFERENCE_ONTOLOGY)
    inferred = {t for t in everything.get_context(inference_onto) if str(t[0]) != INFERENCE_ONTOLOGY}

    # owlready writes some inferences (inverse property values) into the loaded ontology,
    # not the inference one, so every ground triple not in the input also counts as
    # inferred. Literals compare by text: owlready changes some datatypes and language tags.
    def key(t):
        return tuple(str(x) if isinstance(x, Literal) else x for x in t)
    in_input = {key(t) for t in source if not any(isinstance(x, BNode) for x in t)}

    ds = Dataset(default_union=True)
    asserted, inferred_g = ds.graph(ASSERTED), ds.graph(INFERRED)
    for t in everything:
        if str(t[0]) == INFERENCE_ONTOLOGY:
            continue
        ground = not any(isinstance(x, BNode) for x in t)
        (inferred_g if t in inferred or (ground and key(t) not in in_input) else asserted).add(t)

    closure = ds.graph(CLOSURE)
    for x, c in list(ds.subject_objects(RDF.type)):
        if isinstance(c, URIRef) and c != OWL.NamedIndividual:
            for sup in ds.transitive_objects(c, RDFS.subClassOf):
                if isinstance(sup, URIRef) and sup != OWL.Thing and (x, RDF.type, sup) not in ds:
                    closure.add((x, RDF.type, sup))
    return ds


def _memory_mb(memory: str) -> int:
    units = {'g': 1024, 'm': 1}
    return int(memory[:-1]) * units[memory[-1].lower()] if memory[-1].lower() in units else int(memory)


def _worker(closure: Path, cache_dir: Path, memory: str, property_values: bool) -> None:
    import owlready2
    owlready2.reasoning.JAVA_MEMORY = _memory_mb(memory)
    world = owlready2.World()
    # format given explicitly: owlready guesses wrongly when the first line is long
    world.get_ontology('file://' + str(closure.resolve())).load(format='ntriples')
    report = {'failure': None, 'unsatisfiable': []}
    try:
        owlready2.sync_reasoner_hermit(world, infer_property_values=property_values, debug=0)
    except owlready2.OwlReadyInconsistentOntologyError:
        report['failure'] = 'inconsistent'
    else:
        report['unsatisfiable'] = sorted(c.iri for c in world.inconsistent_classes())
        _split(world, Graph().parse(str(closure), format='nt')).serialize(
            str(cache_dir / 'entailed.nq'), format='nquads', encoding='utf-8')
    (cache_dir / 'worker.json').write_text(json.dumps(report))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HermiT entailment worker (internal)')
    parser.add_argument('--worker', nargs=2, metavar=('CLOSURE_NT', 'CACHE_DIR'), required=True)
    parser.add_argument('--memory', default='4g')
    parser.add_argument('--no-property-values', action='store_true')
    args = parser.parse_args()
    _worker(Path(args.worker[0]), Path(args.worker[1]), args.memory, not args.no_property_values)
