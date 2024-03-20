import unittest
import utility.TestUtilities as tu

class TestDegradedState(unittest.TestCase):

    query = """
    prefix maint: <https://spec.industrialontologies.org/ontology/maintenance/Maintenance/>

    SELECT ?state
    WHERE {
        ?state a maint:MaintenanceState
    } 
    """

    def setUp(self):
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None

    # testing subclass relationship 
    def test_subclass_case(self):

        namespace = self.ontologies["maint"].get_namespace("https://spec.industrialontologies.org/ontology/maintenance/Maintenance/")
 
        # arrage 
        with namespace:
            degraded_state1 = namespace.DegradedState("degraded_state1")

            # run reasoner 
            tu.run_hermit_reasoner()
            #print("Instances -----", namespace.MaintenanceState.instances())

            # act
            result = tu.run_query(self.query)

            print(result)
            
            # assert that list has one entry
            self.assertEqual(len(result), 1)

            # assert that the resource found is the degraded_state1
            self.assertEqual(result[0][0], degraded_state1)

        namespace.destroy()


if __name__ == '__main__':
    unittest.main()
