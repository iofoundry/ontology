import unittest
from utility import TestUtilities as tu

class TestCQ5(unittest.TestCase):

    query = """
    prefix maint: <https://spec.industrialontologies.org/ontology/maintenance/Maintenance/>
    prefix core: <https://spec.industrialontologies.org/ontology/core/Core/>

    SELECT (SUM(?cost) as ?TotalCost)
    WHERE {
        ?mwo a maint:MaintenanceWorkOrderRecord .
        ?mwo core:describes ?activity .
        ?activity core:prescribedBy ?strategy .
        ?strategy a maint:WorkFromInspection .
        ?mwo maint:hasActualCost ?cost .
    } 
    """

    def setUp(self):
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None

    # What is the cost of the work done initiated by an inspection?
    def test_inspection_cost(self):

        namespace = self.ontologies["maint"].get_namespace("https://spec.industrialontologies.org/ontology/maintenance/Maintenance/")
        core = self.ontologies["core"].get_namespace("https://spec.industrialontologies.org/ontology/core/Core/")
        bfo = self.ontologies["bfo"].get_namespace("http://purl.obolibrary.org/obo/bfo.owl#")

        # Arrange 
        with namespace:

            tu.create_application_model(namespace, core, bfo)  

            # run reasoner 
            tu.run_hermit_reasoner()

            # Act
            result = tu.run_query(self.query)
            
            # Assert that list has one entries
            self.assertEqual(len(result), 1)

            # assert that the value found is 19696
            self.assertEqual(result[0][0], 19696)

        namespace.destroy()

if __name__ == '__main__':
    unittest.main()
