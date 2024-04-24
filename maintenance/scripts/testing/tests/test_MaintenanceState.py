import unittest
import utility.TestUtilities as tu

class TestMaintenanceState(unittest.TestCase):

    def setUp(self):
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None
   
    # testing equivalence relationship 
    def test_equivalence_case(self):

        namespace = self.ontologies["maint"].get_namespace("https://spec.industrialontologies.org/ontology/maintenance/Maintenance/")
    
        # Arrange 
        with namespace:
            # maintenance_state1 = namespace.MaintenanceState("maintenance_state1") #TODO?
            degraded_state = namespace.DegradedState("degraded_state")
            failed_state = namespace.FailedState("failed_state")
            operating_state = namespace.OperatingState("operating_state")
            equivalent_classes = [namespace.DegradedState, namespace.FailedState, namespace.OperatingState]

            # run reasoner 
            tu.run_hermit_reasoner()

            # Act
            result = namespace.MaintenanceState.instances()

            # Assert that every instance of MaintenanceState is either degraded, failed, or operating state
            for instance in result:
                instance_type = instance.is_a
                self.assertIn(instance_type[0], equivalent_classes)

        namespace.destroy()

        

if __name__ == '__main__':
    unittest.main()
