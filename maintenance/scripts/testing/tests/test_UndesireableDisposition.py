import unittest
import utility.TestUtilities as tu

class TestUndesireableDisposition(unittest.TestCase):

    def setUp(self):
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
   
    # testing equivalence relationship 
    def test_equivalence(self):

        namespace = self.ontologies["maint"].get_namespace("https://spec.industrialontologies.org/ontology/maintenance/Maintenance/")
    
        # Arrange 
        with namespace:
            disposition_exhibit_undesirable_behavior1 = namespace.DispositionToExhibitUndesirableBehavior("disposition_exhibit_undesirable_behavior1")
            disposition_to_fail1 = namespace.DispositionToFail("disposition_to_fail1")
            equivalent_classes = [namespace.DispositionToExhibitUndesirableBehavior, namespace.DispositionToFail]

            # run reasoner 
            tu.run_hermit_reasoner()

            # Act - get instances of undesirable dissposition 
            result = namespace.UndesireableDisposition.instances()

            # Assert that every instance of UndesireableDisposition is either degraded, failed, or operating state
            for instance in result:
                instance_type = instance.is_a
                self.assertIn(instance_type[0], equivalent_classes)

        namespace.destroy()

        

if __name__ == '__main__':
    unittest.main()
