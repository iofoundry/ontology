import argparse
import os
import sys

from rdflib import Graph


def run_hygiene(
        folder_with_hygiene_tests: str,
        parameter_input_value: str,
        parameter_output_value: str,
        error_label='PRODERROR:',
        files: list[str] = []) -> bool:
    ontology_is_clean = True
    ontology = Graph()
    ontology.parse(source='cache/bfo/2020/bfo.rdf')
    ontology.parse(source='core/meta/AnnotationVocabulary.rdf')
    ontology.parse(source='core/commonstocoremapping/meta/MappingAnnotationVocabularyToCommons.rdf')
    ontology.parse(source='core/commonstocoremapping/MappingCommonsToIOF.rdf')
    ontology.parse(source='core/Core.rdf')
    for file in files:
        ontology.parse(source=file)
    for root, subfolder_paths, file_names in os.walk('biopharma/'):
      for file_name in file_names:
          if file_name.endswith('.rdf'):
              file_path = os.path.join(root, file_name)
              ontology.parse(source=file_path)
        
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
                    print(result.warning)
                    if result.warning.startswith(error_label):
                        ontology_is_clean = False
    return ontology_is_clean


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run hygiene tests')
    parser.add_argument('--folder_with_hygiene_tests', help='Path to folder with hygiene tests', metavar='HYGIENE', default='etc/testing/hygiene_parameterized')
    parser.add_argument('--error_label', help='Error label', metavar='ERROR', default='PRODERROR')
    parser.add_argument('--parameter_input_value', help='Hygiene test filter constant', metavar='HYGIENEPLACEHOLDER', default='<HYGIENE_TESTS_FILTER_PARAMETER>')
    parser.add_argument('--parameter_output_value', help='Hygiene test filter variable', metavar='HYGIENEPLACEHOLDER', default='industrialontologies')
    args, rest = parser.parse_known_args()
    
    ontology_is_clean = \
        run_hygiene(
            folder_with_hygiene_tests=args.folder_with_hygiene_tests,
            error_label=args.error_label,
            parameter_input_value=args.parameter_input_value,
            parameter_output_value=args.parameter_output_value, files=rest)
    
    if ontology_is_clean:
        sys.exit(0)
    sys.exit(-1)
