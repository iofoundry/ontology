import unittest
from utility import TestUtilities as tu

class TestDegradedState(unittest.TestCase):

    def setUp(self):
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None

    # testing subclass relationship 
    def test_subclass(self):

        namespace = self.ontologies["maint"].get_namespace("https://spec.industrialontologies.org/ontology/maintenance/Maintenance/")
 
        # Arrange 
        with namespace:
            degraded_state1 = namespace.DegradedState("degraded_state1")

            # run reasoner 
            tu.run_hermit_reasoner()

            # Act
            result = namespace.MaintenanceState.instances()
            
            # Assert that list has one entry
            self.assertEqual(len(result), 1)

            # Assert that the resource found is the degraded_state1
            self.assertEqual(result[0], degraded_state1)

        namespace.destroy()

        # testing disjoint relationship 
    def test_disjointness(self):

        namespace = self.ontologies["maint"].get_namespace("https://spec.industrialontologies.org/ontology/maintenance/Maintenance/")
 
        # Arrange 
        with namespace:
            degraded_state1 = namespace.DegradedState("degraded_state1")
            failed_state1 = namespace.FailedState("failed_state1")
            operating_state1 = namespace.OperatingState("operating_state1")

            # run reasoner 
            tu.run_hermit_reasoner()

            # Act using owlready 
            # result = tu.run_query(self.query)
            disjoint_with_failed = all(instance not in namespace.FailedState.instances() for instance in namespace.DegradedState.instances())
            disjoint_with_operating = all(instance not in namespace.OperatingState.instances() for instance in namespace.DegradedState.instances())

            # Assert that instances of DegradedState are disjoint from FailedState and OperatingState            
            self.assertTrue(disjoint_with_failed)
            self.assertTrue(disjoint_with_operating)


            # OR Act using query 
            query = """
            PREFIX maint: <https://spec.industrialontologies.org/ontology/maintenance/Maintenance/>

            SELECT ?degradedState
            WHERE {
                ?degradedState a maint:DegradedState .
                FILTER EXISTS {
                    ?degradedState a ?otherState .
                    FILTER (?otherState = maint:FailedState || ?otherState = maint:OperatingState)
                }
            }
            """
            result = tu.run_query(query)

            # Assert that instances of DegradedState are disjoint from FailedState and OperatingState
            self.assertFalse(result, "Some instances of DegradedState are also instances of FailedState or OperatingState")

        namespace.destroy()
    

if __name__ == '__main__':
    unittest.main()
