import unittest
import utility.TestUtilities as tu

class TestDispositionToExhibitUndesirableBehavior(unittest.TestCase):

    def setUp(self):
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
   
    # testing subclass relationship 
    def test_subclass(self):

        namespace = self.ontologies["maint"].get_namespace("https://spec.industrialontologies.org/ontology/maintenance/Maintenance/")
 
        # Arrange 
        with namespace:
            disposition_exhibit_undesirable_behavior1 = namespace.DispositionToExhibitUndesirableBehavior("disposition_exhibit_undesirable_behavior1")

            # run reasoner 
            tu.run_hermit_reasoner()

            # Act
            result = namespace.UndesireableDisposition.instances()
            
            # Assert that list has one entry
            self.assertEqual(len(result), 1)

            # Assert that the resource found is the disposition_exhibit_undesirable_behavior1
            self.assertEqual(result[0], disposition_exhibit_undesirable_behavior1)

        namespace.destroy()

if __name__ == '__main__':
    unittest.main()
