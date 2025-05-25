import ssl

# Disable SSL certificate verification to avoid SSL errors when loading ontologies
ssl._create_default_https_context = ssl._create_unverified_context

from owlready2 import get_ontology, get_namespace
from .utils import to_pascal_case, to_camel_case


class RdfToPumlConverter:
    def __init__(self, **kwargs):
        self.namespaces = {key: get_namespace(value) for key, value in kwargs.items()}

        self.classes = {}
        self.individuals = {}
        self.properties = []

    # def get_namespace_for_type(self, name):
    #     for key, ns in self.namespaces.items():
    #         if name.startswith(key.upper()):
    #             return ns
    #     return None

    def load_data(self, input_rdf):
        data = get_ontology(input_rdf).load()

        for ind in data.individuals():
            self.individuals[ind.name] = ind

            if ind.is_a:
                for ind_type in ind.is_a:
                    try:
                        class_label = to_pascal_case(ind_type.label[0])
                        self.classes[class_label] = ind_type
                        self.properties.append((ind, "typeOf", class_label))
                    except:
                        continue

            for prop in ind.get_properties():
                for value in prop[ind]:
                    if (value, to_camel_case(prop.inverse.label[0]), ind) in self.properties:
                        continue
                    else:    
                        self.properties.append((ind, to_camel_case(prop.label[0]), value))
    
    def generate_puml(self, output_puml):
        with open(output_puml, "w") as f:
            f.write("@startuml\n")
            f.write("!include https://raw.githubusercontent.com/iofoundry/ontopuml/main/iof.iuml\n")

            class_map = {cls_label: f"c{idx}" for idx, cls_label in enumerate(self.classes, start=1)}
            individual_map = {ind_name: f"i{idx}" for idx, ind_name in enumerate(self.individuals, start=1)}

            for cls_label, cls in self.classes.items():
                ns_prefix = "bfo:" if cls.name.startswith("BFO") else "iof:"
                f.write(f"class({class_map[cls_label]}, {ns_prefix}{cls_label})\n")

            for ind_name in self.individuals:
                f.write(f"individual({individual_map[ind_name]}, ns1:{ind_name})\n")

            for s, p, o in self.properties:
                if p == "typeOf" and o in class_map:
                    f.write(f"typeOf({individual_map[s.name]}, {class_map[o]})\n")
                elif p != "typeOf" and o.name in individual_map:
                    f.write(f"property({individual_map[s.name]}, {p}, {individual_map[o.name]})\n")

            f.write("@enduml\n")

    def reset(self):
        self.classes.clear()
        self.individuals.clear()
        self.properties.clear()

    def convert(self, input_rdf, output_puml):
        self.reset()
        self.load_data(input_rdf)
        self.generate_puml(output_puml)

        print(f"PUML file saved as {output_puml}")
