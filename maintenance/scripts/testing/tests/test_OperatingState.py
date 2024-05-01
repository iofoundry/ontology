import unittest
import utility.TestUtilities as tu

class TestOperatingState(unittest.TestCase):

    def setUp(self):
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None

    # testing subclass relationship 
    def test_subclass(self):

        namespace = self.ontologies["maint"].get_namespace("https://spec.industrialontologies.org/ontology/maintenance/Maintenance/")
 
        # Arrange 
        with namespace:
            operating_state1 = namespace.OperatingState("operating_state1")

            # run reasoner 
            tu.run_hermit_reasoner()

            # Act
            result = namespace.MaintenanceState.instances()
            
            # Assert that list has one entry
            self.assertEqual(len(result), 1)

            # Assert that the resource found is the operating_state1
            self.assertEqual(result[0], operating_state1)

        namespace.destroy()

        # testing disjoint relationship 
    def test_disjointness(self):

        namespace = self.ontologies["maint"].get_namespace("https://spec.industrialontologies.org/ontology/maintenance/Maintenance/")
 
        # Arrange 
        with namespace:
            operating_state1 = namespace.OperatingState("operating_state1")
            failed_state1 = namespace.FailedState("failed_state1")
            degraded_state1 = namespace.DegradedState("degraded_state1")

            # run reasoner 
            tu.run_hermit_reasoner()

            # Act using owlready 
            # result = tu.run_query(self.query)
            disjoint_with_failed = all(instance not in namespace.FailedState.instances() for instance in namespace.OperatingState.instances())
            disjoint_with_degraded = all(instance not in namespace.DegradedState.instances() for instance in namespace.OperatingState.instances())

            # Assert that instances of OperatingState are disjoint from FailedState and OperatingState            
            self.assertTrue(disjoint_with_failed)
            self.assertTrue(disjoint_with_degraded)


            # OR Act using query 
            query = """
            PREFIX maint: <https://spec.industrialontologies.org/ontology/maintenance/Maintenance/>

            SELECT ?OperatingState
            WHERE {
                ?OperatingState a maint:OperatingState .
                FILTER EXISTS {
                    ?OperatingState a ?otherState .
                    FILTER (?otherState = maint:FailedState || ?otherState = maint:DegradedState)
                }
            }
            """
            result = tu.run_query(query)

            # Assert that instances of OperatingState are disjoint from FailedState and DegradedState
            self.assertFalse(result, "Some instances of OperatingState are also instances of FailedState or DegradedState")

        namespace.destroy()
    

if __name__ == '__main__':
    unittest.main()
