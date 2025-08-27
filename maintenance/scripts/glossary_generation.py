from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery


def get_list_of_classes(ontology_path):
    g = Graph()
    g.parse(ontology_path, format="xml")
    query_str = """
        PREFIX iof-av: <https://spec.industrialontologies.org/ontology/core/meta/AnnotationVocabulary/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?class_name ?definition
        WHERE {
            ?class a owl:Class .
            ?class iof-av:naturalLanguageDefinition ?definition .
            ?class rdfs:label ?class_name .
        }
    """
    q = prepareQuery(query_str)
    return g.query(q)


def get_list_of_properties(ontology_path):
    g = Graph()
    g.parse(ontology_path, format="xml")
    query_str = """
        PREFIX iof-av: <https://spec.industrialontologies.org/ontology/core/meta/AnnotationVocabulary/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?property_name ?definition
        WHERE {
            ?prop a owl:ObjectProperty .
            ?prop iof-av:naturalLanguageDefinition ?definition .
            ?prop rdfs:label ?property_name .
        }
    """
    q = prepareQuery(query_str)
    return g.query(q)


def construct_html(template_filepath, output_filepath, classes, properties):

    # read template
    with open(template_filepath, "r") as f:
        html_template = f.read()

        class_section = ""
        for index, cl in enumerate(classes):
            class_section += construct_html_row(cl, index)

        # replace {{CLASSES}} with class_section in html_template
        html_template = html_template.replace("{{CLASSES}}", class_section)

        property_section = ""
        for index, pr in enumerate(properties):
            property_section += construct_html_row(pr, index)

        # replace {{PROPERTIES}} with property_section in html_template
        html_template = html_template.replace(
            "{{PROPERTIES}}", property_section)

        # replace {{DATE}} with current date in html_template
        html_template = html_template.replace("{{DATE}}", get_date())

        # write html_template to output
        with open(output_filepath, "w") as f:
            f.write(html_template)


def get_date():
    # get the current date in the form "December 28th, 2022"
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%B %d, %Y")


def construct_html_row(row, index):
    entity_name = row[0]
    definition = row[1]

    return f'''<tr class="row{index}">
        <td class="column0 style0 s">&nbsp;{entity_name}</td>
        <td class="column1 style0 s">{definition}</td>
    </tr>'''


if __name__ == "__main__":
    # Get the list of classes
    properties = get_list_of_properties("Maintenance.rdf")
    classes = get_list_of_classes("Maintenance.rdf")

    construct_html("scripts/glossary_template.html",
                   "scripts/index.html", classes, properties)
