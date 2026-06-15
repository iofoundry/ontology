import re
import argparse
import xml.etree.ElementTree as ET
import os
from itertools import groupby

CACHED_ONTOLOGIES = {
    "http://purl.obolibrary.org/obo/bfo/2020/bfo.owl": "./cache/bfo/2020/bfo.rdf",
    "https://spec.industrialontologies.org/ontology/cache/bfo/2020/bfo.rdf": "./cache/bfo/2020/bfo.rdf",
    "https://www.omg.org/spec/Commons/AnnotationVocabulary/": "./cache/CMNS/AnnotationVocabulary.rdf",
    "https://spec.industrialontologies.org/ontology/cache/CMNS/AnnotationVocabulary/": "./cache/CMNS/AnnotationVocabulary.rdf",
    "https://www.omg.org/spec/Commons/AnnotationVocabulary.rdf": "./cache/CMNS/AnnotationVocabulary.rdf",
    "https://spec.industrialontologies.org/ontology/cache/CMNS/AnnotationVocabulary.rdf": "./cache/CMNS/AnnotationVocabulary.rdf",
    "https://www.omg.org/spec/Commons/TextDatatype/": "./cache/CMNS/TextDatatype.rdf",
    "https://spec.industrialontologies.org/ontology/cache/CMNS/TextDatatype/": "./cache/CMNS/TextDatatype.rdf",
    "https://www.omg.org/spec/Commons/TextDatatype.rdf": "./cache/CMNS/TextDatatype.rdf",
    "https://spec.industrialontologies.org/ontology/cache/CMNS/TextDatatype.rdf": "./cache/CMNS/TextDatatype.rdf",
    "https://www.omg.org/spec/Commons/Collections/": "./cache/CMNS/Collections.rdf",
    "https://spec.industrialontologies.org/ontology/cache/CMNS/Collections/": "./cache/CMNS/Collections.rdf",
    "https://www.omg.org/spec/Commons/Collections.rdf": "./cache/CMNS/Collections.rdf",
    "https://spec.industrialontologies.org/ontology/cache/CMNS/Collections.rdf": "./cache/CMNS/Collections.rdf",
    "https://www.omg.org/spec/Commons/Designators/": "./cache/CMNS/Designators.rdf",
    "https://spec.industrialontologies.org/ontology/cache/CMNS/Designators/": "./cache/CMNS/Designators.rdf",
    "https://www.omg.org/spec/Commons/Designators.rdf": "./cache/CMNS/Designators.rdf",
    "https://spec.industrialontologies.org/ontology/cache/CMNS/Designators.rdf": "./cache/CMNS/Designators.rdf",
    "https://www.omg.org/spec/Commons/Identifiers/": "./cache/CMNS/Identifiers.rdf",
    "https://spec.industrialontologies.org/ontology/cache/CMNS/Identifiers/": "./cache/CMNS/Identifiers.rdf",
    "https://www.omg.org/spec/Commons/Identifiers.rdf": "./cache/CMNS/Identifiers.rdf",
    "https://spec.industrialontologies.org/ontology/cache/CMNS/Identifiers.rdf": "./cache/CMNS/Identifiers.rdf",
}

def collect_imports(ontology_path: str, resolution: dict):
  print('::notice file=' + ontology_path + ',title=Collect Imports::Parsing file ', ontology_path)
  about = ET.parse(ontology_path)
  for onto in about.getroot().findall('{http://www.w3.org/2002/07/owl#}Ontology'):
    iri = onto.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']
    if iri in resolution:
      return
    
    resolution[iri] = ontology_path
    print('::notice file=' + ontology_path + ',title=Collect Imports::Found ontology with IRI:', iri)
    
    version_iri = onto.find('{http://www.w3.org/2002/07/owl#}versionIRI')
    if version_iri is not None:
      version_iri_value = version_iri.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
      resolution[version_iri_value] = ontology_path
      print('::notice file=' + ontology_path + ',title=Collect Imports::Found versionIRI with IRI:', version_iri_value)
    
    for imports in onto.findall('{http://www.w3.org/2002/07/owl#}imports'):
      import_iri = imports.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
      
      # Transform the import IRI into a file name
      if not (re.search(r'^https://spec.industrialontologies.org/ontology/([0-9]{6}/)?cache', import_iri) or 
              import_iri in resolution or import_iri in CACHED_ONTOLOGIES):
        match = re.search(r'^https://spec.industrialontologies.org/ontology/([0-9]{6}/)?(.+)', import_iri)
        if match:
          file = match.group(2)
          if file.endswith('/'):
            file = file[:-1] + '.rdf'
          if not file.startswith('./'):
            file = './' + file
          print("::notice file=" + ontology_path + ",title=Collect Imports::Found import with IRI: " + import_iri + " with file name: " + file)
          if os.path.exists(file):               
            collect_imports(file, resolution)
          else:
            print('::warning file=' + ontology_path + ',title=Collect Imports::Could not find file ' + file)

def recreate_catalog_file(version: str):
  print('::notice title=Recreate Catalog::Recreating catalog file with versioned and non-versioned IRIs')
  resolution = dict()
  collect_imports('./AboutIOFDev.rdf', resolution)
  collect_imports('./AboutIOFProd.rdf', resolution)
  
  catalog_file_path = 'catalog-v001.xml'
  with open(catalog_file_path, 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
    f.write('<catalog prefer="public" xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">\n')
    f.write('  <!-- Cached Ontologies -->\n')
    for name, path in CACHED_ONTOLOGIES.items():
      f.write(f'    <uri id="Cached Ontology Resolution" name="{name}" uri="{path}"/>\n')
      match = re.search(r'^(https://spec.industrialontologies.org/ontology/)(cache/.+)$', name)
      if match:
        f.write(f'    <uri id="Cached Ontology Resolution" name="{match.group(1)}{version}/{match.group(2)}" uri="{path}"/>\n')
    f.write('\n  <!-- IOF Ontologies -->\n')
    ontologies = sorted(resolution.items(), key=lambda x: os.path.dirname(x[1]))
    for domain, files in groupby(ontologies, key=lambda x: os.path.dirname(x[1])):
      if domain == '.':
        domain = '  Top Level'
      f.write(f'\n    <!-- {domain[2:]} -->\n')
      for name, path in files:
        f.write(f'      <uri id="IRI Resolution" name="{name}" uri="{path}"/>\n')
    f.write('</catalog>\n')
  print('::notice file=' + catalog_file_path + ',title=Recreate Catalog::Catalog file recreated with versioned and non-versioned IRIs')

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Recreate the catalog file with versioned and non-versioned IRIs')
  parser.add_argument("version", type=str, help='The version to use for versioned IRIs')
  args = parser.parse_args()
  recreate_catalog_file(args.version)