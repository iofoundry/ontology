import unittest
from utility import TestUtilities as tu


class TestCQ2(unittest.TestCase):

    query = """
    prefix maint: <https://spec.industrialontologies.org/ontology/maintenance/Maintenance/>
    prefix core: <https://spec.industrialontologies.org/ontology/core/Core/>

    SELECT distinct ?mwo ?cum_hours ?activity ?strategy
    WHERE {
        ?mwo a maint:MaintenanceWorkOrderRecord .
        ?mwo core:describes ?activity .
        ?activity core:prescribedBy ?strategy .
        {
            ?strategy a maint:ScheduledReplacement .
        }
        UNION
        {
            ?strategy a maint:ScheduledRestoration .
        }
        ?mwo maint:hasCumulativeUtilizedHours ?cum_hours.FILTER(?cum_hours<16000) .
    } 
    """

    def setUp(self):
        self.ontologies = tu.load_ontology()

    def tearDown(self):
        self.ontologies = None

    # Did any scheduled repairs or restoration occur before the target interval of ⟨x⟩ operating hours?
    def test_premature_repairs(self):

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
            
            # Assert that list has three entries
            self.assertEqual(len(result), 3)

            # assert that the MWOs found are MWO_6, MWO_15, MWO_17
            self.assertEqual(result[0][0], namespace.MaintenanceWorkOrderRecord("MWO_6"))
            self.assertEqual(result[1][0], namespace.MaintenanceWorkOrderRecord("MWO_15"))
            self.assertEqual(result[2][0], namespace.MaintenanceWorkOrderRecord("MWO_17"))

        namespace.destroy()

if __name__ == '__main__':
    unittest.main()
