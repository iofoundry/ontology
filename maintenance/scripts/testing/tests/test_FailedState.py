import unittest
import utility.TestUtilities as tu

class TestFailedState(unittest.TestCase):

    def setUp(self):
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None

    # testing subclass relationship 
    def test_subclass_case(self):

        namespace = self.ontologies["maint"].get_namespace("https://spec.industrialontologies.org/ontology/maintenance/Maintenance/")
 
        # Arrange 
        with namespace:
            failed_state1 = namespace.FailedState("failed_state1")

            # run reasoner 
            tu.run_hermit_reasoner()

            # Act
            result = namespace.MaintenanceState.instances()
            
            # Assert that list has one entry
            self.assertEqual(len(result), 1)

            # Assert that the resource found is the failed_state1
            self.assertEqual(result[0], failed_state1)

        namespace.destroy()

        # testing disjoint relationship 
    def test_disjoint_case(self):

        namespace = self.ontologies["maint"].get_namespace("https://spec.industrialontologies.org/ontology/maintenance/Maintenance/")
 
        # Arrange 
        with namespace:
            failed_state1 = namespace.FailedState("failed_state1")
            operating_state1 = namespace.OperatingState("operating_state1")
            degraded_state1 = namespace.DegradedState("degraded_state1")

            # run reasoner 
            tu.run_hermit_reasoner()

            # Act using owlready 
            # result = tu.run_query(self.query)
            disjoint_with_operating = all(instance not in namespace.OperatingState.instances() for instance in namespace.FailedState.instances())
            disjoint_with_degraded = all(instance not in namespace.DegradedState.instances() for instance in namespace.FailedState.instances())

            # Assert that instances of FailedState are disjoint from OperatingState and DegradedState            
            self.assertTrue(disjoint_with_operating)
            self.assertTrue(disjoint_with_degraded)


            # OR Act using query 
            query = """
            PREFIX maint: <https://spec.industrialontologies.org/ontology/maintenance/Maintenance/>

            SELECT ?FailedState
            WHERE {
                ?FailedState a maint:FailedState .
                FILTER EXISTS {
                    ?FailedState a ?otherState .
                    FILTER (?otherState = maint:OperatingState || ?otherState = maint:DegradedState)
                }
            }
            """
            result = tu.run_query(query)

            # Assert that instances of FailedState are disjoint from OperatingState and DegradedState
            self.assertFalse(result, "Some instances of FailedState are also instances of OperatingState or DegradedState")

        namespace.destroy()
    

if __name__ == '__main__':
    unittest.main()
