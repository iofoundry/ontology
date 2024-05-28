import unittest
from utility import TestUtilities as tu

class TestCQ3(unittest.TestCase):

    query = """
    prefix maint: <https://spec.industrialontologies.org/ontology/maintenance/Maintenance/>
    prefix core: <https://spec.industrialontologies.org/ontology/core/Core/>
    prefix bfo: <http://purl.obolibrary.org/obo/>

    SELECT (SUM(?cost) as ?TotalCost)
    WHERE {
        ?mwo a maint:MaintenanceWorkOrderRecord .
        ?mwo core:describes ?activity .
        ?activity bfo:BFO_0000167 ?item .
        ?item maint:hasMaintenanceState ?state .
        ?state a maint:FailedState .
        ?mwo maint:hasActualCost ?cost .
    } 
    """

    def setUp(self):
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None

    # What is the total cost of failures on the maintainable item ⟨A⟩ which should have no failures under its scheduled restoration maintenance strategy? 
    def test_failure_cost(self):

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

            # assert that the value found is 1683
            self.assertEqual(result[0][0], 1683)

        namespace.destroy()

if __name__ == '__main__':
    unittest.main()
