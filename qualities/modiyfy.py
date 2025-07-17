from rdflib import Graph, RDF, OWL, RDFS, Namespace, Literal, URIRef
OBO=Namespace("http://purl.obolibrary.org/obo/")

# Load the old and new RDF files
def do_stuff():
    old_rdf_file = "Qualities-Morphologic.rdf"
    new_rdf_file = "new.rdf"
    g_old = Graph()
    g_new = Graph()
    g_old.parse(old_rdf_file)
    g_new.parse(new_rdf_file)

    # Copy all instance of type class from new.rdf to g that have the same iri
    for subject in g_old.subjects(predicate=RDF.type, object=OWL.Class):
        if subject in g_new.subjects():
            parentcls=next(g_old.objects(subject=subject,predicate=RDFS.subClassOf),None)
            g_old.remove((subject, None, None))
            g_old.remove((None, None, subject))
            for predicate, obj in g_new.predicate_objects(subject=subject):
                    if predicate!=RDFS.subClassOf:
                        g_old.add((subject, predicate, obj))
            for s,predicate in g_new.subject_predicates(object=subject):
                    if predicate!=RDFS.subClassOf:
                        g_old.add((s, predicate, subject))
            if parentcls:
                g_old.add((subject,RDFS.subClassOf,parentcls))
    # Serialize and save the modified graph to a new file
    g_old.serialize("modified.rdf", "pretty-xml")

def remove_labels_from_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    new_lines = []
    temp_buffer = []
    inside_class = False

    for line in lines:
        if '<owl:Class' in line:
            inside_class = True
            temp_buffer.clear()
        
        if inside_class and '<rdfs:label' in line:
            temp_buffer.append(line)
            if len(temp_buffer) > 4:
                new_lines.extend(temp_buffer)
                temp_buffer.clear()
        else:
            if temp_buffer:
                if len(temp_buffer) == 4:
                    new_lines.extend(temp_buffer[:1])  # Keep only the first two labels
                else:
                    new_lines.extend(temp_buffer)
                temp_buffer.clear()
            new_lines.append(line)
            
        if '</owl:Class>' in line:
            inside_class = False
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

from lxml import etree

def move_owl_classes_with_skos_definition(input_file, output_file):
    # Parse the input RDF/XML file
    tree = etree.parse(input_file)
    root = tree.getroot()

    # Namespace definitions
    namespaces = {
        'owl': 'http://www.w3.org/2002/07/owl#',
        'skos': 'http://www.w3.org/2004/02/skos/core#'
    }

    # Lists to hold the classes
    classes_to_move = []
    remaining_classes = []

    # Iterate through all owl:Class elements
    for owl_class in root.findall('owl:Class', namespaces):
        # Check if it has a skos:definition
        if owl_class.find('skos:definition', namespaces) is not None:
            classes_to_move.append(owl_class)
        else:
            remaining_classes.append(owl_class)

    # Remove classes that have skos:definition from the root
    for cls in classes_to_move:
        root.remove(cls)

    # Append the classes to move at the end of the root
    for cls in classes_to_move:
        root.append(cls)

    # Write the modified tree to the output file while preserving namespaces
    with open(output_file, 'wb') as file:
        file.write(etree.tostring(root, xml_declaration=True, encoding='UTF-8', pretty_print=True))


def merge_g(input_file, merge_file):
    g = Graph()
    g_tomerge = Graph()
    g.parse(input_file)
    g_tomerge.parse(merge_file)
    g+=g_tomerge
    g.serialize("merged.rdf",format="pretty-xml")

import re


def camel_case_to_snake_case(name):
    """Convert CamelCase string to snake_case."""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def add_rdfs_label_to_classes(input_file):
    # Load the graph from the input RDF file
    g = Graph()
    g.parse(input_file, format='xml')

    # Iterate through all owl:Class entities
    for owl_class in g.subjects(predicate=RDF.type, object=OWL.Class):
        # Check if the class already has an rdfs:label with lang='en'
       
        # Convert the URI to a class name
        class_name = owl_class.split('/')[-1]  # Extracts the last part of the URI
        # Convert the class name from snake_case to lower case with spaces
        label = camel_case_to_snake_case(class_name).replace('_', ' ')
        print(label)
        # Add the rdfs:label in English
        g.add((owl_class, RDFS.label, Literal(label, lang='en')))

    # Serialize the graph to the output file
    g.serialize(input_file, format='pretty-xml')

def restore_reference(input_file, backup_file):
    g_old = Graph()
    g_new = Graph()
    g_old.parse(backup_file)
    g_new.parse(input_file)
    adapted_from=URIRef("https://spec.industrialontologies.org/ontology/core/meta/AnnotationVocabulary/adaptedFrom")
    old_ref_prop=URIRef("http://purl.obolibrary.org/obo/IAO_0000412")
    # Copy all instance of type class from new.rdf to g that have the same iri
    for subject in g_old.subjects(predicate=RDF.type, object=OWL.Class):
        if subject in g_new.subjects():
            g_new.remove((subject,adapted_from, None))
            reference=next(g_old.objects(subject=subject,predicate=old_ref_prop),None)
            print(reference)
            if reference:
                g_new.add((subject,adapted_from,reference))
            else:
                print(subject)
    # Serialize and save the modified graph to a new file
    g_new.serialize("modified.rdf", "pretty-xml")
#merge_g("Qualities-Morphologic.rdf","Qualities-Morphologic copy.rdf")

#move_owl_classes_with_skos_definition('mod2.rdf', 'mod2-sort.rdf')
restore_reference("Qualities-Morphologic.rdf","morph_old.rdf")
#add_rdfs_label_to_classes("Qualities-Morphologic.rdf")
#remove_labels_from_file("merged.rdf", "merged2.rdf")
