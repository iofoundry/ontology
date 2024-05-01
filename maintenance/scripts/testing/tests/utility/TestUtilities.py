
from owlready2 import *
import rdflib
import os

# Loads ontologies 
def load_ontology():
    bfo = owlready2.get_ontology("cache/bfo/2020/bfo.rdf")
    bfo.load()
    annotation_vocabulary = owlready2.get_ontology("core/meta/AnnotationVocabulary.rdf")
    annotation_vocabulary.load()
    core = owlready2.get_ontology("core/Core.rdf")
    core.load()
    ontology = owlready2.get_ontology("maintenance/Maintenance.rdf")
    ontology.load()

    # add imported ontologies
    core.imported_ontologies.append(bfo)
    core.imported_ontologies.append(annotation_vocabulary)
    ontology.imported_ontologies.append(core)

    ontologies = {
        "bfo": bfo,
        "annotation_vocabulary": annotation_vocabulary,
        "core": core,
        "maint": ontology
    }
    return ontologies

# runs a Hermit reasoner on the ontology with owlready 2
def run_hermit_reasoner():
    sync_reasoner(infer_property_values = True, debug = 0)


def run_query(query):
    results = default_world.sparql(query)
    return list(results)

# clear test/ staging file
def clear_staging():
    for filename in os.listdir("test/staging"):
        os.remove("test/staging/"+filename)


