from owlready2 import *
import owlready2
from owlready2 import default_world

if __name__ == "__main__":

    print("start program")
    onto = get_ontology("https://spec.industrialontologies.org/ontology/wheel")
    core_onto = get_ontology("https://raw.githubusercontent.com/iofoundry/ontology/refs/heads/slot/core/Core.rdf").load()
    onto.imported_ontologies.append(core_onto)

    core = onto.get_namespace("https://spec.industrialontologies.org/ontology/core/Core/")
    bfo = onto.get_namespace("http://purl.obolibrary.org/obo/")

    with onto:

    #     # create Tire specification containing two Tire beads
        TireBead = types.new_class("TireBead", (core.MaterialArtifact, ))
        TireBeadSlot = types.new_class("TireBeadSlot", (core.ComponentSlot, ))
        TireBeadSlot.equivalent_to.append(core.ComponentSlot 
                                          & core.filledBy.some(core.DesignSpecification #& core.prescribes.only(TireBead)
                                                               ))
        Tire = types.new_class("Tire", (core.MaterialArtifact, ))
        TireSpec = types.new_class("TireSpecification", (core.DesignSpecification,))
        TireSpec.equivalent_to.append(core.DesignSpecification #& core.prescribes.only(Tire)
                                       & core.hasSlot.exactly(2, TireBeadSlot))

        # # create Wheel specification containing the TireMountingRim and 5 mounting holes
        TireMountingRim = types.new_class("TireMountingRimSpecification", (core.DesignSpecification,)) #& core.prescribes.only(TireMountingRim)
        TireMountingRimSlot = types.new_class("TireMountingRimSlot", (core.ComponentSlot, ))
        TireMountingRimSlot.equivalent_to.append(core.ComponentSlot & core.filledBy.some(TireMountingRim 
                                                                                         ))
        MountingHole = types.new_class("MountingHoleSpecification", (core.DesignSpecification,)) #& core.prescribes.only(MountingHole)
        MountingHoleSlot = types.new_class("MountingHoleSlot", (core.ComponentSlot, ))
        MountingHoleSlot.equivalent_to.append(core.ComponentSlot & core.filledBy.some(MountingHole 
                                                                                      ))
        AllDisjoint([TireMountingRim, MountingHole])
        Wheel = types.new_class("Wheel", (core.MaterialArtifact, ))
        WheelSpec = types.new_class("WheelSpecification", (core.DesignSpecification,))
        WheelSpec.equivalent_to.append(core.DesignSpecification #& core.prescribes.only(Wheel)
                                        & core.hasSlot.exactly(2, TireMountingRimSlot)
                                        & core.hasSlot.exactly(5, MountingHoleSlot))

        # create WheelAssembly design spec class (each having a tire and a wheel as component)
        WheelSlot = types.new_class("WheelSlot", (core.ComponentSlot, ))
        WheelSlot.equivalent_to.append(core.ComponentSlot & core.filledBy.some(WheelSpec))
        TireSlot = types.new_class("TireSlot", (core.ComponentSlot, ))
        TireSlot.equivalent_to.append(core.ComponentSlot & core.filledBy.some(TireSpec))
        WheelAssemblySpec = types.new_class("WheelAssemblySpecification", (core.DesignSpecification,))
        WheelAssemblySpec.equivalent_to.append(core.DesignSpecification & core.prescribes.some(core.Assembly) 
                                              & core.hasSlot.exactly(1, WheelSlot) # one tire per assembly
                                              & core.hasSlot.exactly(1, TireSlot)) # one wheel per assembly



        # create Hub specification with 5 bolt-holes
        BoltHole = types.new_class("BoltHole", (bfo.BFO_0000040,))
        BoltHoleSlot = types.new_class("BoltHoleSlot", (core.ComponentSlot, ))
        BoltHoleSlot.equivalent_to.append(core.ComponentSlot & core.filledBy.some(core.DesignSpecification #& core.prescribes.only(BoltHole)
                                                                                  ))
        HubSpec = types.new_class("HubSpecification", (core.DesignSpecification,))
        HubSpec.equivalent_to.append(core.DesignSpecification & core.hasSlot.exactly(5, BoltHoleSlot))



        # # create a Lugbolt specification
        LugBolt = types.new_class("Lugbolt", (core.MaterialArtifact,))
        LugBoltSpec = types.new_class("LugboltSpecification", (core.DesignSpecification,))
        # LugBoltSpec.equivalent_to.append(core.DesignSpecification & core.prescribes.only(LugBolt))

        # # create Wheel Hub Assembly
        AllDisjoint([LugBoltSpec, HubSpec])
        WheelHubAssemblySpec = types.new_class("WheelHubAssemblySpecification", (core.DesignSpecification,))
        WheelAssemblySlot = types.new_class("WheelAssemblySlot", (core.ComponentSlot, ))
        WheelAssemblySlot.equivalent_to.append(core.ComponentSlot & core.filledBy.some(WheelAssemblySpec))
        WheelHubAssemblySpec.equivalent_to.append(core.DesignSpecification #& core.prescribes.only(core.Assembly) 
                                              & core.hasSlot.exactly(1, WheelAssemblySlot)
                                              & core.hasSlot.exactly(1, core.InformationSlot & core.filledBy.some(HubSpec))
                                              & core.hasSlot.exactly(5, core.InformationSlot & core.filledBy.some(LugBoltSpec))
                                              )

        # The two tire beads are snapped against the rim of the wheel.
        # Each of the five mounting holes of on the wheel is connected to each bolt holes on the hub with a lugbolt
        # Both cases involves fastening type of joints e.g., the tire beads acts as a fastener to connect the tire to the wheel.
        #   There are two connections each having the tire and the wheel as connected parts and one of the bead as the fastener.
        # Similarly, there are five connections each connecting the wheel-assemby to the hub with one lugbolt as the faster

        # in a simpler form connection among two specs can be made with connection slot.

        ##############################Data##############################################

        core.hasSlot.python_name = "hasSlot"
        core.filledBy.python_name = "filledBy"

        def relate_specs_with_slot(ice1, ice2, slot):
            ice1.hasSlot.append(slot)
            slot.filledBy.append(ice2)


        # # create Tire specification containing two Tire beads
        tire_bead1 = core.DesignSpecification("tire-bead-spec")
        tire_spec1 = TireSpec("tire-spec-1")
        tire_bead_slot_1 = TireBeadSlot("tire-bead-slot-1")
        tire_bead_slot_2 = TireBeadSlot("tire-bead-slot-2")
        AllDifferent([tire_bead_slot_1, tire_bead_slot_2])
        relate_specs_with_slot(tire_spec1, tire_bead1, tire_bead_slot_1)
        relate_specs_with_slot(tire_spec1, tire_bead1, tire_bead_slot_2)

        # # # create Wheel specification containing the TireMountingRim and 5 mounting holes
        wheel_spec1 = core.DesignSpecification("wheel-spec-1")
        tire_mounting_rim1 = core.DesignSpecification("tire-mounting-rim-1")
        tire_mounting_hole1 = core.DesignSpecification("tire-mounting-hole-1")
        tire_mounting_rim_slot_1 = TireMountingRimSlot("tire-mounting-rim-slot-1")
        tire_mounting_rim_slot_2 = TireMountingRimSlot("tire-mounting-rim-slot-2")
        relate_specs_with_slot(wheel_spec1, tire_mounting_rim1, tire_mounting_rim_slot_1)
        relate_specs_with_slot(wheel_spec1, tire_mounting_rim1, tire_mounting_rim_slot_2)
        mounting_hole_slot_1 = MountingHoleSlot("mounting-hole-slot-1")
        mounting_hole_slot_2 = MountingHoleSlot("mounting-hole-slot-2")
        mounting_hole_slot_3 = MountingHoleSlot("mounting-hole-slot-3")
        mounting_hole_slot_4 = MountingHoleSlot("mounting-hole-slot-4")
        mounting_hole_slot_5 = MountingHoleSlot("mounting-hole-slot-5")      
        AllDifferent([mounting_hole_slot_1, mounting_hole_slot_2, mounting_hole_slot_3, mounting_hole_slot_4, mounting_hole_slot_5])  
        relate_specs_with_slot(wheel_spec1, tire_mounting_hole1, mounting_hole_slot_1)
        relate_specs_with_slot(wheel_spec1, tire_mounting_hole1, mounting_hole_slot_2)
        relate_specs_with_slot(wheel_spec1, tire_mounting_hole1, mounting_hole_slot_3)
        relate_specs_with_slot(wheel_spec1, tire_mounting_hole1, mounting_hole_slot_4)
        relate_specs_with_slot(wheel_spec1, tire_mounting_hole1, mounting_hole_slot_5)

        # # # create WheelAssembly design spec class (each having a tire and a wheel as component)
        # AllDifferent([wheel_spec1, tire_spec1])
        wheel_assembly_spec1 = WheelAssemblySpec("wheel-assembly-spec-1")
        relate_specs_with_slot(wheel_assembly_spec1, wheel_spec1, WheelSlot("wheel-slot-1"))
        relate_specs_with_slot(wheel_assembly_spec1, tire_spec1, TireSlot("tire-slot-1"))

        # # # create Hub specification with 5 bolt-holes
        hub_spec1 = HubSpec("hub-spec-1")
        bolt_hole1 = core.DesignSpecification("bolt-hole-1")
        bolt_hole_slot_1 = BoltHoleSlot("bolt-hole-slot-1")
        bolt_hole_slot_2 = BoltHoleSlot("bolt-hole-slot-2")
        bolt_hole_slot_3 = BoltHoleSlot("bolt-hole-slot-3")
        bolt_hole_slot_4 = BoltHoleSlot("bolt-hole-slot-4")
        bolt_hole_slot_5 = BoltHoleSlot("bolt-hole-slot-5")
        AllDifferent([bolt_hole_slot_1, bolt_hole_slot_2, bolt_hole_slot_3, bolt_hole_slot_4, bolt_hole_slot_5])
        relate_specs_with_slot(hub_spec1, bolt_hole1, bolt_hole_slot_1)
        relate_specs_with_slot(hub_spec1, bolt_hole1, bolt_hole_slot_2)
        relate_specs_with_slot(hub_spec1, bolt_hole1, bolt_hole_slot_3)
        relate_specs_with_slot(hub_spec1, bolt_hole1, bolt_hole_slot_4)
        relate_specs_with_slot(hub_spec1, bolt_hole1, bolt_hole_slot_5)

        # # # create a Lugbolt specification
        lug_bolt_spec1 = LugBoltSpec("lug-bolt-spec-1")

        # # # create Wheel Hub Assembly
        wheel_hub_assembly_spec1 = WheelHubAssemblySpec("wheel-hub-assembly-spec-1")
        relate_specs_with_slot(wheel_hub_assembly_spec1, wheel_assembly_spec1, core.ComponentSlot("wheel-assembly-slot-1"))
        relate_specs_with_slot(wheel_hub_assembly_spec1, hub_spec1, core.ComponentSlot("hub-slot-1"))
        lug_bolt_slot_1 = core.ComponentSlot("lug-bolt-slot-1")
        lug_bolt_slot_2 = core.ComponentSlot("lug-bolt-slot-2")
        lug_bolt_slot_3 = core.ComponentSlot("lug-bolt-slot-3")
        lug_bolt_slot_4 = core.ComponentSlot("lug-bolt-slot-4")
        lug_bolt_slot_5 = core.ComponentSlot("lug-bolt-slot-5")
        AllDifferent([lug_bolt_slot_1, lug_bolt_slot_2, lug_bolt_slot_3, lug_bolt_slot_4, lug_bolt_slot_5])
        relate_specs_with_slot(wheel_hub_assembly_spec1, lug_bolt_spec1, core.ComponentSlot("lug-bolt-slot-1"))
        relate_specs_with_slot(wheel_hub_assembly_spec1, lug_bolt_spec1, core.ComponentSlot("lug-bolt-slot-2"))
        relate_specs_with_slot(wheel_hub_assembly_spec1, lug_bolt_spec1, core.ComponentSlot("lug-bolt-slot-3"))
        relate_specs_with_slot(wheel_hub_assembly_spec1, lug_bolt_spec1, core.ComponentSlot("lug-bolt-slot-4"))
        relate_specs_with_slot(wheel_hub_assembly_spec1, lug_bolt_spec1, core.ComponentSlot("lug-bolt-slot-5"))

        # # connect each tire bead to the tire mounting rim using ConnectionSlots
        relate_specs_with_slot(tire_bead1, tire_mounting_rim1, core.ConnectionSlot("connection-slot-1"))

        # # connect each tire mounting hole to bolt hole using a lug bolt (Joint specification)
        joint_spec = types.new_class("FastenedJointSpecification", (core.DesignSpecification,))
        relate_specs_with_slot(joint_spec, lug_bolt_spec1, core.FastenerSlot("fastener-slot-1"))
        relate_specs_with_slot(joint_spec, bolt_hole1, core.InformationSlot("connected-part-slot-1"))
        relate_specs_with_slot(joint_spec, tire_mounting_hole1, core.InformationSlot("connected-part-slot-2"))

    onto.save(file = "wheel.owl", format = "rdfxml")

    owlready2.JAVA_EXE = r"C:\Program Files\Java\jdk-17\bin\java.exe"

    try:
        # close_world(onto)
        with onto:
            sync_reasoner(infer_property_values = True)
        print("Reasoning completed successfully.")
        
    except OwlReadyInconsistentOntologyError as e:
        print("Inconsistency detected in the ontology!")
        print(e)
        print(*list(default_world.inconsistent_classes()))