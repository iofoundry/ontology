
from owlready2 import *

#PascalCase
def to_pascal_case(text):
    text = text.replace('_', ' ').replace('-', ' ')
    words = text.split()
    return ''.join([word.capitalize() for word in words])
#camelCase
def to_camel_case(prop_name):
    words = prop_name.replace("_", " ").split()
    return words[0].lower() + "".join(word.capitalize() for word in words[1:]) if words else ""

def rdf_to_puml(data, output_puml):
    iofcore = get_namespace("https://spec.industrialontologies.org/ontology/core/Core/")
    bfo = get_namespace("http://purl.obolibrary.org/obo/")
    
    classes = {}
    individuals = {}
    properties = []

    for ind in data.individuals():
        individuals[ind.name] = ind
        if ind.is_a:
            for ind_type in ind.is_a:
                try:
                    ns = bfo if ind_type.name.startswith("BFO") else iofcore
                    class_label = to_pascal_case(ns[ind_type.name].label[0])
                    classes[class_label] = ind_type
                    properties.append((ind, "typeOf", class_label))
                except:
                    continue
        
        for prop in ind.get_properties():
            for value in prop[ind]:
                ns = bfo if prop.name.startswith("BFO") else iofcore
                properties.append((ind, to_camel_case(ns[prop.name].label[0]), value))
    print('classes',classes,'\n', 'individuals',individuals,'\n', properties)

    with open(output_puml, "w") as f:
        f.write("@startuml\n")
        f.write("!include https://raw.githubusercontent.com/iofoundry/ontopuml/main/iof.iuml\n")

        # Declare classes first with appropriate prefixes
        class_map = {}
        for idx, (cls_label, cls) in enumerate(classes.items(), start=1):
            ns_prefix = "bfo:" if cls.name.startswith("BFO") else "iof:"
            formatted_label = f"{ns_prefix}{cls_label}"
            class_map[cls_label] = f"c{idx}"
            f.write(f"class({class_map[cls_label]}, {formatted_label})\n")

        # Declare individuals with ns1: prefix
        individual_map = {}
        for idx, (ind_name, ind) in enumerate(individuals.items(), start=1):
            individual_map[ind_name] = f"i{idx}"
            f.write(f"individual({individual_map[ind_name]}, ns1:{ind_name})\n")

        # Add typeOf relationships
        for s, p, o in properties:
            if p == "typeOf" and o in class_map:
                f.write(f"typeOf({individual_map[s.name]}, {class_map[o]})\n")

        # Add properties
        for s, p, o in properties:
            if p != "typeOf" and o.name in individual_map:
                f.write(f"property({individual_map[s.name]}, {p}, {individual_map[o.name]})\n")

        f.write("@enduml\n")