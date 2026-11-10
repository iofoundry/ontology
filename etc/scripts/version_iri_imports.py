import re
import sys
from pathlib import Path
import argparse
import xml.etree.ElementTree as ET
import os
from itertools import groupby
from recreate_catalog_file import recreate_catalog_file

def update_owl_imports(file_path: Path, release_number: str, import_release_number: str, skip_imports: bool) -> None:
  """
  Update owl:import elements in an RDF XML file to use version IRIs with release numbers.
  
  Args:
    file_path: Path to the RDF XML file
    release_number: Release number to append to version IRIs
    import_release_number: Release number to use for imports
  """  
  # Read the file
  with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
  
  def replace_import(match):
    prefix = match.group(1)
    root = match.group(2)
    iri = match.group(3)
    suffix = match.group(4)
    
    if re.match(r'^\d{6}', iri):
      if import_release_number == '':
        print(f"::notice title=Replace Import::Skipping already versioned IRI: {iri}")
        return match.group(0)
      elif iri.startswith(import_release_number):
        print(f"::notice title=Replace Import::Skipping already versioned IRI: {iri}")
        return match.group(0)
      else:
        print(f"::notice title=Replace Import::Updating release number in IRI: {iri} to {import_release_number}")
        iri = re.sub(r'^\d{6}', import_release_number, iri)
        new_iri = f"{prefix}{root}{iri}{suffix}"
        return new_iri
    elif import_release_number != '':
      new_iri = f"{prefix}{root}{import_release_number}/{iri}{suffix}"
      print(f"::notice title=Replace Import::Replacing import IRI: {match.group(0)} with {new_iri}")
      return new_iri
    else:
      print(f"::notice title=Replace Import::Skipping unversioned IRI: {iri}")
      return match.group(0)
  
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
  parser.add_argument("-n", "--unversion_imports", action="store_true", help="remove vesion from imports")

  args = parser.parse_args()
    
  release_number = args.release
  skip_imports = args.skip_imports
  import_release_number = release_number if not args.unversion_imports else ''
    
  # Recurse all .rdf files in the current and subdirectories
  rdf_files = Path('.').rglob('*.rdf')
  for file_path in rdf_files:
    print("::notice title=Main::Processing: ", file_path)
    update_owl_imports(file_path, release_number, import_release_number, skip_imports)
    
  # Recreate the catalog file with all versioned and non-versioned IRIs
  recreate_catalog_file(release_number)
