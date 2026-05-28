import re
import sys
from pathlib import Path
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


def update_owl_imports(file_path: str, release_number: str, skip_imports: bool) -> None:
  """
  Update owl:import elements in an RDF XML file to use version IRIs with release numbers.
  
  Args:
    file_path: Path to the RDF XML file
    release_number: Release number to append to version IRIs
  """
  file_path = Path(file_path)
  
  # Read the file
  with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
  
  def replace_import(match):
    prefix = match.group(1)
    root = match.group(2)
    iri = match.group(3)
    suffix = match.group(4)
    
    if re.match(r'^\d{6}', iri):
      if iri.startswith(release_number):
        print(f"::notice title=Replace Import::Skipping already versioned IRI: {iri}")
        return match.group(0)
      else:
        print(f"::notice title=Replace Import::Updating release number in IRI: {iri} to {release_number}")
        iri = re.sub(r'^\d{6}', release_number, iri)
        new_iri = f"{prefix}{root}{iri}{suffix}"
      return match.group(0)  # Already versioned, skip
    else:
      new_iri = f"{prefix}{root}{release_number}/{iri}{suffix}"
      print(f"::notice title=Replace Import::Replacing import IRI: {match.group(0)} with {new_iri}")
      return new_iri
  
  def correct_version_iri(match):
    prefix = match.group(1)
    root = match.group(2)
    version = match.group(3)
    iri = match.group(4)
    suffix = match.group(5)
    
    if version == release_number:
      print(f"::notice title=Correct Version IRI::Skipping already versioned versionIRI: {match.group(0)}")
      return match.group(0)
    else:
      new_iri = f"{prefix}{root}{release_number}{iri}{suffix}"
      print(f"::notice title=Correct Version IRI::Replacing versionIRI: {match.group(0)} with {new_iri}")
      return new_iri
  
  updated_content = content
  
  if not skip_imports:
    # Replace all matches
    # Pattern to match owl:import elements with rdf:resource attributes
    # Matches: <owl:import rdf:resource="https://spec.industrialontologies.org/ontology/"/>
    pattern = r'(<owl:imports\s+rdf:resource=[\'"]{1})(https://spec.industrialontologies.org/ontology/)([^"\']+)(["\']{1})'  
    updated_content = re.sub(pattern, replace_import, updated_content)
  
  # Pattern to match owl:versionIRI elements with rdf:resource attributes
  # Matches: <owl:versionIRI rdf:resource="https://spec.industrialontologies.org/ontology/<version>/..."/>
  pattern = r'(<owl:versionIRI\s+rdf:resource=[\'"]{1})(https://spec.industrialontologies.org/ontology/)(\d{6})(/[^"\']+)(["\']{1})'  
  updated_content = re.sub(pattern, correct_version_iri, updated_content)
  
  # Update copyright year if present
  pattern = r'(<iof-av:copyright>Copyright \(c\))[0-9, ]+(Open Applications Group</iof-av:copyright>)'
  updated_content = re.sub(pattern, rf'\1 2022, 2023, 2024, 2025, 2026 \2', updated_content)

  # Write back to file
  with open(file_path, 'w', encoding='utf-8') as f:
    f.write(updated_content)
  
  print(f"::notice title=Update OWL Imports::Updated {file_path} with version IRIs for release number {release_number}")


if __name__ == "__main__":
  # Parse command line arguments, expect a release number and an optional switch to turn off update of imports
  parser = argparse.ArgumentParser(description="Version IRI import updater for RDF XML files")
  parser.add_argument("release", help="release number")              # positional
  parser.add_argument("-s", "--skip_imports", action="store_true", help="skip updating imports")

  args = parser.parse_args()
    
  release_number = args.release
  skip_imports = args.skip_imports
    
  # Recurse all .rdf files in the current and subdirectories
  rdf_files = Path('.').rglob('*.rdf')
  for file_path in rdf_files:
    print("::notice title=Main::Processing: ", file_path)
    update_owl_imports(file_path, release_number, skip_imports)
    
  # Recreate the catalog file with all versioned and non-versioned IRIs
  recreate_catalog_file(release_number)
