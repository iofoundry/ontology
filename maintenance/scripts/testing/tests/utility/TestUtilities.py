
from owlready2 import *
import pandas as pd
import rdflib
import os

# Loads ontologies 
def load_ontology():
    bfo = owlready2.get_ontology("cache/bfo/2020/bfo.rdf")
    bfo.load()
    annotation_vocabulary = owlready2.get_ontology("core/meta/AnnotationVocabulary.rdf")
    annotation_vocabulary.load()
    core = owlready2.get_ontology("core/Core.rdf")
    core.load()
    ontology = owlready2.get_ontology("maintenance/Maintenance.rdf")
    ontology.load()


    # add imported ontologies
    core.imported_ontologies.append(bfo)
    core.imported_ontologies.append(annotation_vocabulary)
    ontology.imported_ontologies.append(core)

    ontologies = {
        "bfo": bfo,
        "annotation_vocabulary": annotation_vocabulary,
        "core": core,
        "maint": ontology
    }
    return ontologies

def create_application_model(maint, core, bfo):

    # import MWO data
    mwo_df = pd.read_csv("maintenance/scripts/testing/data/ROMAIN_paper_data_original_modified4IOFCQs.csv")

    # select data for TK001 engine
    mwo_df = mwo_df[mwo_df['Asset_ID'] == "TK001"]

    # Arrange 
    with maint:

        # firstly create two new data properties - hasActualCost & hasCumulativeUtilisedHours

        # Data Property to connect MWO with associated cost
        class hasActualCost(DataProperty):
            domain   = [maint.MaintenanceWorkOrderRecord]
            range    = [int]

        # Data Property to connect MWO with number of hours cost - I think this is wrong ! it would be the engine at that point in time?
        class hasCumulativeUtilizedHours(DataProperty):
            domain   = [core.MaintainableMaterialItem]
            range    = [int]

        # New subclasses of maintenanceStrategy
        class ScheduledReplacement(maint.MaintenanceStrategy):
            pass
        class ScheduledRestoration(maint.MaintenanceStrategy):
            pass
        class WorkFromInspection(maint.MaintenanceStrategy):
            pass
        class WorkFromBreakdown(maint.MaintenanceStrategy):
            pass

        # iterate through the MWO records and add to the applicatin ontology 
        for n, row in mwo_df.iterrows():

            # create maintenanceWorkOrderRecord instance 
            mwo = maint.MaintenanceWorkOrderRecord(f"MWO_{n + 1}")

            # create MaintainableMaterialItem instance
            maintenanceItem = core.MaintainableMaterialItem(f"{row['Asset_ID']}_{row['Asset_subsystem']}_{n + 1}")

            # create maintenanceActivity instance
            activity = maint.MaintenanceActivity(f'unknown_{n + 1}' if pd.isna(row['Activity']) else f"{row['Activity']}_{n + 1}")

            # create maintenanceStrategy instance
            if row['Work_Order_Initiator'] == 'OperationalIssue':
                strategy = maint.WorkFromBreakdown(f'WorkFromBreakdown_{n + 1}')
                activity.prescribedBy.append(strategy)
            elif row['Work_Order_Initiator'] == 'WorkFromInspection':
                strategy = maint.WorkFromInspection(f'WorkFromInspection_{n + 1}')
                activity.prescribedBy.append(strategy)
            elif row['Work_Order_Initiator'] == 'FixedIntervalRestoration':
                strategy = maint.ScheduledRestoration(f'ScheduledRestoration_{n + 1}')
                activity.prescribedBy.append(strategy)
            elif row['Work_Order_Initiator'] == 'FixedIntervalReplacement':
                strategy = maint.ScheduledReplacement(f'ScheduledReplacement_{n + 1}')
                activity.prescribedBy.append(strategy)

            # BFO_0000167 - "has participant at all times"
            activity.BFO_0000167.append(maintenanceItem) 

            # add property connecting maintenanceWorkOrderRecord to maintenanceActivity
            mwo.describes.append(activity)
            mwo.isInputOf.append(activity)

            # indicates failure
            if row['Work_Order_Initiator'] == 'OperationalIssue':
                # create failedState instance 
                failedState = maint.FailedState(f"failed_{row['Asset_subsystem']}_{n + 1}")

                # create failureEvent instance 
                failureEvent = maint.FailureEvent(f"{row['State']}_{n + 1}")

                # add property connecting failureEvent to failedState
                failureEvent.initiates.append(failedState)

                # add property connecting MaintainableMaterialItem to failedState
                maintenanceItem.hasMaintenanceState.append(failedState)
            

            # DATA PROPERTIES
            # add number of cumulative hours 
            maintenanceItem.hasCumulativeUtilizedHours.append(0 if pd.isna(row['Cum_Utilized_Hours']) else int(row['Cum_Utilized_Hours']))

            # add actual cost 
            # whats the best way to deal with this? it wasnt actually exeucted so costs would be 0?
            if not pd.isna(row['Actual_Costs']):
                if row['Actual_Costs'].strip() == '-':
                    mwo.hasActualCost.append(0)
                else:
                    mwo.hasActualCost.append(int(row['Actual_Costs']))
            else:
                mwo.hasActualCost.append(0)
            
    
    maint.save(file = "maintenance/scripts/testing/data/application_ontology.rdf", format = "rdfxml")


# runs a Hermit reasoner on the ontology with owlready 2
def run_hermit_reasoner():
    sync_reasoner(infer_property_values = True, debug = 0)


def run_query(query):
    results = default_world.sparql(query)
    return list(results)

# clear test/ staging file
def clear_staging():
    for filename in os.listdir("test/staging"):
        os.remove("test/staging/"+filename)


