import argparse
import os
import sys
import xml.etree.ElementTree as ET

from rdflib import Graph

def parse_catalog(catalog_file_path: str):
    resolution = dict()
    print('Parsing', catalog_file_path)
    catalog = ET.parse(catalog_file_path)
    for uri in catalog.getroot().findall('{urn:oasis:names:tc:entity:xmlns:xml:catalog}uri'):
        ontology_path = uri.attrib['uri']
        if ontology_path.endswith('.rdf'):
            resolution[uri.attrib['name']] = ontology_path
    return resolution

def parse_about(about_file_path: str, resolution: dict):
  ontologies = list()
  print('Parsing', about_file_path)
  graph = Graph()
  graph.parse(source=about_file_path)
  
  query = '''
  PREFIX owl:   <http://www.w3.org/2002/07/owl#>
  PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  SELECT ?iri WHERE {
    ?ontology a owl:Ontology .
    ?ontology owl:imports ?iri .
  }'''
  results = graph.query(query)
  for result in results:
    iri = str(result.iri)
    if iri in resolution:
      ontologies.append(resolution[iri])
      print('Found ontology:', resolution[iri])
    else:
      print('WARNING: Could not find ontology for IRI:', iri)
      
  return ontologies

def find_ontologies(about_file: str):
  abs_path_about_file = os.path.abspath(about_file)
  print('About file absolute path:', abs_path_about_file)
  folder = os.path.dirname(abs_path_about_file)
  print('Folder:', folder)
  resolution = parse_catalog(os.path.join(folder, 'catalog-v001.xml'))
  return parse_about(abs_path_about_file, resolution)

def run_hygiene(
        folder_with_hygiene_tests: str,
        parameter_input_value: str,
        parameter_output_value: str,
        error_label='::error',
        error_output='::error',  
        files: list[str] = []) -> bool:
    ontology_is_clean = True
    ontology = Graph()
    for file in files:
        ontology.parse(source=file)
    for root, subfolder_paths, file_names in os.walk(folder_with_hygiene_tests):
        for file_name in file_names:
            if 'sparql' in file_name:
                print('Running', file_name)
                input_file_path = os.path.join(folder_with_hygiene_tests, file_name)
                input_file = open(input_file_path, 'r')
                input_file_content = input_file.read()
                input_file_content = input_file_content.replace(parameter_input_value, '"'+parameter_output_value+'"')
                results = ontology.query(input_file_content)
                # print('Results found:', list(results))
                for result in results:
                    result.warning = result.warning.replace(error_label, error_output)
                    result.warning = result.warning.replace("::critical", "::error")
                    print(result.warning)
                    if result.warning.startswith('::error'):
                        ontology_is_clean = False
    return ontology_is_clean


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run hygiene tests')
    parser.add_argument('--about_file', help='Path to About rdf file', metavar='ABOUT')
    parser.add_argument('--folder_with_hygiene_tests', help='Path to folder with hygiene tests', metavar='HYGIENE', default='etc/testing/hygiene_parameterized')
    parser.add_argument('--error_label', help='Error label', metavar='ERROR_LABEL', default='::error')
    parser.add_argument('--error_output', help='Error label', metavar='ERROR_OUTPUT', default='::error')
    parser.add_argument('--parameter_input_value', help='Hygiene test filter constant', metavar='HYGIENEPLACEHOLDER', default='<HYGIENE_TESTS_FILTER_PARAMETER>')
    parser.add_argument('--parameter_output_value', help='Hygiene test filter variable', metavar='HYGIENEPLACEHOLDER', default='industrialontologies')
    args, rest = parser.parse_known_args()

    ontologies = find_ontologies(args.about_file)
    
    ontology_is_clean = \
        run_hygiene(
            folder_with_hygiene_tests=args.folder_with_hygiene_tests,
            error_label=args.error_label,
            error_output=args.error_output,
            parameter_input_value=args.parameter_input_value,
            parameter_output_value=args.parameter_output_value, 
            files=ontologies)
    
    if ontology_is_clean:
        sys.exit(0)
    sys.exit(-1)
