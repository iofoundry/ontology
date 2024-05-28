import unittest
from utility import TestUtilities as tu

class TestCQ1(unittest.TestCase):

    query = """
    prefix maint: <https://spec.industrialontologies.org/ontology/maintenance/Maintenance/>

    SELECT (count(?failure) as ?failureCount)
    WHERE {
        ?failure a maint:FailureEvent 
    } 
    """

    def setUp(self):
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None

    # How many breakdown work orders were executed?
    def test_nbreakdown_mwos(self):

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
            
            # Assert that list has one entry
            self.assertEqual(len(result), 1)

            # assert that the count found is 4
            self.assertEqual(result[0][0], 4)

        namespace.destroy()

if __name__ == '__main__':
    unittest.main()
