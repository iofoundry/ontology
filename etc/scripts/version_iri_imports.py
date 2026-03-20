import re
import sys
from pathlib import Path
import argparse

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
        print(f"Skipping already versioned IRI: {iri}")
        return match.group(0)
      else:
        print(f"Updating release number in IRI: {iri} to {release_number}")
        iri = re.sub(r'^\d{6}', release_number, iri)
        new_iri = f"{prefix}{root}{iri}{suffix}"
      return match.group(0)  # Already versioned, skip
    else:
      new_iri = f"{prefix}{root}{release_number}/{iri}{suffix}"
      print(f"Replacing import IRI: {match.group(0)} with {new_iri}")
      return new_iri
  
  def correct_version_iri(match):
    prefix = match.group(1)
    root = match.group(2)
    version = match.group(3)
    iri = match.group(4)
    suffix = match.group(5)
    
    if version == release_number:
      print(f"Skipping already versioned versionIRI: {match.group(0)}")
      return match.group(0)
    else:
      new_iri = f"{prefix}{root}{release_number}{iri}{suffix}"
      print(f"Replacing versionIRI: {match.group(0)} with {new_iri}")
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
  
  print(f"Updated {file_path} with version IRIs for release number {release_number}")


if __name__ == "__main__":
  # Parse command line arguments, expect a release number and an optional switch to turn off update of imports
  parser = argparse.ArgumentParser(description="Version IRI Imort Updater for RDF XML files")
  parser.add_argument("release", help="release number")              # positional
  parser.add_argument("-s", "--skip_imports", action="store_true", help="skip updating import files")

  args = parser.parse_args()
    
  release_number = args.release
  skip_imports = args.skip_imports
  
  # Recurse all .rdf files in the current and subdirectories
  rdf_files = Path('.').rglob('*.rdf')
  for file_path in rdf_files:
    print("Processing: ", file_path)
    update_owl_imports(file_path, release_number, skip_imports)