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
  
  maturity = 'unknown'
  maturity_query = '''
  PREFIX iof-av: <https://spec.industrialontologies.org/ontology/annotation/>
  PREFIX owl:   <http://www.w3.org/2002/07/owl#>
  PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  SELECT ?maturity WHERE {
    ?ontology a owl:Ontology .
    ?ontology iof-av:maturity ?maturity .
  }'''
  results = graph.query(maturity_query)
  try:
    maturity = str(next(iter(results)).maturity). \
      replace('https://spec.industrialontologies.org/ontology/individual/', '')
    print('Maturity level: ', maturity)
  except StopIteration:
    print('WARNING: Could not find maturity level in about file.')
    sys.exit(1)
  
  imports = '''
  PREFIX iof-av: <https://spec.industrialontologies.org/ontology/annotation/>
  PREFIX owl:   <http://www.w3.org/2002/07/owl#>
  PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  SELECT ?iri WHERE {
    ?ontology a owl:Ontology .
    ?ontology owl:imports ?iri .
  }'''
  results = graph.query(imports)
  for result in results:
    iri = str(result.iri)
    if iri in resolution:
      ontologies.append(resolution[iri])
      print('Found ontology:', resolution[iri], ' for IRI:', iri)
    else:
      print('WARNING: Could not find ontology for IRI:', iri)
      
  return ontologies, maturity

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
        files: list[str] = [],
        maturity: str = 'unknown') -> bool:
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
                test_name = file_name.replace('testHygiene_', '').replace('.sparql', '').replace('_', ' ')
                input_file_content = input_file_content.replace('<HYGIENE_TEST_NAME>', test_name)
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
    parser.add_argument('--folder_with_hygiene_tests', help='Path to folder with hygiene tests', metavar='HYGIENE', default='etc/testing/hygiene_parameterized')
    parser.add_argument('--parameter_input_value', help='Hygiene test filter constant', metavar='HYGIENEPLACEHOLDER', default='<HYGIENE_TESTS_FILTER_PARAMETER>')
    parser.add_argument('--parameter_output_value', help='Hygiene test filter variable', metavar='HYGIENEPLACEHOLDER', default='industrialontologies')
    args, rest = parser.parse_known_args()

    ontology_is_clean = True
    for about_file in rest:
      print("========================================")
      print("::group::Running tests:", about_file)
      ontologies, maturity = find_ontologies(about_file)
      print("::notice title=" + about_file + " Maturity::" + about_file + " has maturity:", maturity)
      
      if maturity == 'Provisional':
        error_output = "::warning"
      else:
        error_output = "::error"
      clean = \
        run_hygiene(
            folder_with_hygiene_tests=args.folder_with_hygiene_tests,
            error_output=error_output,
            parameter_input_value=args.parameter_input_value,
            parameter_output_value=args.parameter_output_value, 
            files=ontologies,
            maturity=maturity)
      if not clean:
        ontology_is_clean = False
      print("::endgroup::")
      if clean:
        print("::notice title=" + about_file + "::Hygiene tests passed for about file:", about_file)
      else:
        print("::error title=" + about_file + "::Hygiene tests failed for about file:", about_file)
    
    if not ontology_is_clean:
      print ("::error title=Hygiene Tests::some hygiene tests failed.")
      sys.exit(1)
    else:
      print ("::notice title=Hygiene Tests::all hygiene tests passed.")
      sys.exit(0)
