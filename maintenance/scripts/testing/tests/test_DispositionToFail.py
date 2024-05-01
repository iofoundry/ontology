import unittest
import utility.TestUtilities as tu

class TestDispositionToFail(unittest.TestCase):

    def setUp(self):
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
   
    # testing subclass relationship 
    def test_subclass(self):

        namespace = self.ontologies["maint"].get_namespace("https://spec.industrialontologies.org/ontology/maintenance/Maintenance/")
 
        # Arrange 
        with namespace:
            disposition_to_fail1 = namespace.DispositionToFail("disposition_to_fail1")

            # run reasoner 
            tu.run_hermit_reasoner()

            # Act
            result = namespace.UndesireableDisposition.instances()
            
            # Assert that list has one entry
            self.assertEqual(len(result), 1)

            # Assert that the resource found is the disposition_to_fail1
            self.assertEqual(result[0], disposition_to_fail1)

        namespace.destroy()

if __name__ == '__main__':
    unittest.main()
