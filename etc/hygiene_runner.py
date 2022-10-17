import argparse
import os
import sys

from rdflib import Graph


def run_hygiene(
        folder_with_hygiene_tests: str,
        ontology_path: str,
        parameter_input_value: str,
        parameter_output_value: str,
        error_label='Warning:') -> bool:
    ontology_is_clean = True
    ontology = Graph()
    ontology.parse(source=ontology_path)
    for root, subfolder_paths, file_names in os.walk(folder_with_hygiene_tests):
        for file_name in file_names:
            if 'sparql' in file_name:
                print('Running', file_name)
                input_file_path = os.path.join(folder_with_hygiene_tests, file_name)
                input_file = open(input_file_path, 'r')
                input_file_content = input_file.read()
                input_file_content = input_file_content.replace(parameter_input_value, '"'+parameter_output_value+'"')
                results = ontology.query(input_file_content)
                for result in results:
                    print(result.warning)
                    if result.warning.startswith(error_label):
                        ontology_is_clean = False
    return ontology_is_clean


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run hygiene tests')
    parser.add_argument('--folder_with_hygiene_tests', help='Path to folder with hygiene tests', metavar='HYGIENE')
    parser.add_argument('--ontology_path', help='Path to ontology file', metavar='ONTOLOGY')
    parser.add_argument('--error_label', help='Error label', metavar='ERROR')
    parser.add_argument('--parameter_input_value', help='Hygiene test filter constant', metavar='HYGIENEPLACEHOLDER')
    parser.add_argument('--parameter_output_value', help='Hygiene test filter variable', metavar='HYGIENEPLACEHOLDER')
    args = parser.parse_args()
    
    ontology_is_clean = \
        run_hygiene(
            folder_with_hygiene_tests=args.folder_with_hygiene_tests,
            ontology_path=args.ontology_path,
            error_label=args.error_label,
            parameter_input_value=args.parameter_input_value,
            parameter_output_value=args.parameter_output_value)
    
    if ontology_is_clean:
        sys.exit(0)
    sys.exit(-1)
