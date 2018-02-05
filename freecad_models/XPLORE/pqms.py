# Importing standard libs
import sys

# Insert this directory into the PYTHONPATH to import experimental parameters from experiment_params.py
sys.path.insert(0, "${HOME}/work/git/Lab-Management/freecad_models/EM_Coupling_Experiment/code")

# Insert this directoryinto the PYTHONPATH to import Assembly 2 module
sys.path.append('${HOME}/.FreeCAD/Mod/FreeCAD_assembly2')

# Importing Assembly 2 libraries
# Assembly2 is an additional FreeCAD workbench (https://github.com/hamish2014/FreeCAD_assembly2)
import importPart
import planeConstraint
import axialConstraint

# Importing experiment specific parameters

###############################################################################
# Create and open a new file for assembly

assembly_file = App.newDocument("pqms")
App.setActiveDocument(assembly_file.Name)
App.ActiveDocument = App.getDocument(assembly_file.Name)
Gui.ActiveDocument = Gui.getDocument(assembly_file.Name)

###############################################################################
# Import computer_table_setup
computer_table_setup = importPart.importPart(filename = '../computer/models/computer_table_setup.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

###############################################################################
# Import PQMS Electronics Boxes

xplore_electronics = importPart.importPart(filename = 'models/xpl_electronics.fcstd')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Fix the position and orientation of xplore electronics with respect to the computer_table_setup

# Place the xplore electronics boxes on the table surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(xplore_electronics  , "Face030")
Gui.Selection.addSelection(computer_table_setup, "Face010")

selection = Gui.Selection.getSelectionEx()
xpl_electronics_table_surface = planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.recompute()


# Right offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(xplore_electronics  , "Face634")
Gui.Selection.addSelection(computer_table_setup, "Face009")

selection = Gui.Selection.getSelectionEx()
xpl_electronics_table_side = planeConstraint.parseSelection(selection, objectToUpdate=None)

xpl_electronics_table_side.offset = -150

App.ActiveDocument.recompute()


# Front Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(xplore_electronics  , "Face650")
Gui.Selection.addSelection(computer_table_setup, "Face003")

selection = Gui.Selection.getSelectionEx()
xpl_electronics_table_front = planeConstraint.parseSelection(selection, objectToUpdate=None)

xpl_electronics_table_front.offset = '200 mm'
App.ActiveDocument.recompute()

###############################################################################
# Import Pirani Guage

pirani_guage = importPart.importPart(filename = 'models/Pirani_Guage.STEP')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


# Place the pirani_guage on the table surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(pirani_guage  , "Face051")
Gui.Selection.addSelection(computer_table_setup, "Face010")

selection = Gui.Selection.getSelectionEx()
pirani_guage_table_surface = planeConstraint.parseSelection(selection, objectToUpdate=None)

pirani_guage_table_surface.directionConstraint = u"opposed"
App.ActiveDocument.recompute()

# Right offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(pirani_guage  , "Face050")
Gui.Selection.addSelection(computer_table_setup, "Face005")

selection = Gui.Selection.getSelectionEx()
pirani_guage_table_side = planeConstraint.parseSelection(selection, objectToUpdate=None)

pirani_guage_table_side.offset = -100
App.ActiveDocument.recompute()


# front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(pirani_guage  , "Face037")
Gui.Selection.addSelection(computer_table_setup, "Face003")

selection = Gui.Selection.getSelectionEx()
pirani_guage_table_front = planeConstraint.parseSelection(selection, objectToUpdate=None)

pirani_guage_table_front.offset = 200
App.ActiveDocument.recompute()

###############################################################################
# Import Xplore vaccum pump
xpl_vaccum_pump = importPart.importPart(filename = 'models/Pump.STEP')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place the pump on the ground surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(xpl_vaccum_pump  , "Face025")
Gui.Selection.addSelection(computer_table_setup, "Face022")

selection = Gui.Selection.getSelectionEx()
pump_ground_surface = planeConstraint.parseSelection(selection, objectToUpdate=None)

xpl_vaccum_pump.Placement = App.Placement(App.Vector(1500,0,-494.6),App.Rotation(App.Vector(1,1.66533e-16,-1.69938e-32),90))
App.ActiveDocument.recompute()

###############################################################################
# Import vaccum manifold
vaccum_manifold = importPart.importPart(filename = 'models/vaccum_manifold.fcstd')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place the manifold on the table surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vaccum_manifold     , "Face012")
Gui.Selection.addSelection(computer_table_setup, "Face010")

selection = Gui.Selection.getSelectionEx()
manifold_table_surface = planeConstraint.parseSelection(selection, objectToUpdate=None)

manifold_table_surface.directionConstraint = u"opposed"
App.ActiveDocument.recompute()

# Right Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vaccum_manifold     , "Face016")
Gui.Selection.addSelection(computer_table_setup, "Face007")

selection = Gui.Selection.getSelectionEx()
manifold_table_side = planeConstraint.parseSelection(selection, objectToUpdate=None)


# Front Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vaccum_manifold     , "Face021")
Gui.Selection.addSelection(computer_table_setup, "Face005")

selection = Gui.Selection.getSelectionEx()
manifold_table_front = planeConstraint.parseSelection(selection, objectToUpdate=None)

#manifold_table_front.offset = '-500 mm'
App.ActiveDocument.recompute()

##############################################################################
# Import vaccum bellow
bellow = importPart.importPart(filename = 'models/Pump_Bellow.STEP')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Mate to manifold (planar)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vaccum_manifold, "Face1378")
Gui.Selection.addSelection(bellow         , "Face351")

selection = Gui.Selection.getSelectionEx()
bellow_manifold_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)

bellow_manifold_planar.directionConstraint = u"opposed"
App.ActiveDocument.recompute()
# Mate to manifold (axial)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vaccum_manifold, "Face1378")
Gui.Selection.addSelection(bellow         , "Face351")

selection = Gui.Selection.getSelectionEx()
bellow_manifold_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)

# Mate to pump
Gui.Selection.clearSelection()
Gui.Selection.addSelection(xpl_vaccum_pump, "Face239")
Gui.Selection.addSelection(bellow         , "Face356")

selection = Gui.Selection.getSelectionEx()
bellow_pump_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)

###############################################################################
# Import Vaccum pipe
vaccum_pipe = importPart.importPart(filename = 'models/vaccum_pipe.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place on manifold (axial)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vaccum_pipe    , "Face004")
Gui.Selection.addSelection(vaccum_manifold, "Face637")

selection = Gui.Selection.getSelectionEx()
pipe_manifold_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)

pipe_manifold_axial.directionConstraint = u"opposed"
App.ActiveDocument.recompute()

# Place on manifold (planar)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vaccum_pipe    , "Face004")
Gui.Selection.addSelection(vaccum_manifold, "Face637")

selection = Gui.Selection.getSelectionEx()
pipe_manifold_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)

###############################################################################
# Import Xplore steel cryostat
steel_cryostat = importPart.importPart(filename = 'models/Steel_Cryostat.fcstd')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place vaccum pipe on steel cryostat
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vaccum_pipe   , "Face003")
Gui.Selection.addSelection(steel_cryostat, "Face694")

selection = Gui.Selection.getSelectionEx()
pipe_steel_cryostat_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)

pipe_steel_cryostat_axial.directionConstraint = u"aligned"
App.ActiveDocument.recompute()

# Change orientation of steel_cryostat
steel_cryostat.Placement = App.Placement(App.Vector(300.44,-802.099,-350),App.Rotation(App.Vector(-0.2, -0.71, -0.71),180))
App.ActiveDocument.recompute()

#  Mate Pipe with steel_cryostat (planar)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vaccum_pipe   , "Face003")
Gui.Selection.addSelection(steel_cryostat, "Face692")

selection = Gui.Selection.getSelectionEx()
pipe_steel_cryostat_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)

## Has to be manually rotated through the GUI
raw_input("Manually rotate the cryostat and press enter to continue.")

pipe_steel_cryostat_axial.directionConstraint = u"aligned"
App.ActiveDocument.recompute()


###############################################################################
# Import Xplore quartz cryostat
quartz_cryostat = importPart.importPart(filename = 'models/Quartz_Cryostat.fcstd')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place the cryostat on the ground surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(quartz_cryostat  , "Face021")
Gui.Selection.addSelection(computer_table_setup, "Face022")

selection = Gui.Selection.getSelectionEx()
quartz_cryostat_ground_surface = planeConstraint.parseSelection(selection, objectToUpdate=None)

quartz_cryostat.Placement =  App.Placement(App.Vector(-300,-900,-609.6),App.Rotation(App.Vector(1,0,0),90))
App.ActiveDocument.recompute()

## Has to be manually rotated through the GUI
raw_input("Manually rotate the cryostat and press enter to continue.")

################################################################################
## Import insert stand
#insert_stand = importPart.importPart(filename = 'models/insert_stand.fcstd')

#App.ActiveDocument.recompute()
#Gui.SendMsgToActiveView("ViewFit")
#Gui.activeDocument().activeView().viewAxonometric()

## Place on ground
#Gui.Selection.clearSelection()
#Gui.Selection.addSelection(insert_stand  , "Face034")
#Gui.Selection.addSelection(computer_table_setup, "Face022")

#selection = Gui.Selection.getSelectionEx()
#insert_stand_ground_surface = planeConstraint.parseSelection(selection, objectToUpdate=None)


## Front Offset
#Gui.Selection.clearSelection()
#Gui.Selection.addSelection(insert_stand        , "Face026")
#Gui.Selection.addSelection(computer_table_setup, "Face003")

#selection = Gui.Selection.getSelectionEx()
#insert_stand_table_front = planeConstraint.parseSelection(selection, objectToUpdate=None)

#insert_stand_table_front.offset = -200
#App.ActiveDocument.recompute()


## Side Offset
#Gui.Selection.clearSelection()
#Gui.Selection.addSelection(insert_stand  , "Face031")
#Gui.Selection.addSelection(computer_table_setup, "Face005")

#selection = Gui.Selection.getSelectionEx()
#insert_stand_table_side = planeConstraint.parseSelection(selection, objectToUpdate=None)

#insert_stand_table_side.offset = 150
#App.ActiveDocument.recompute()

################################################################################
## Import mgps insert
#mgps_insert = importPart.importPart(filename = 'models/MGPS_Insert.fcstd')

#App.ActiveDocument.recompute()
#Gui.SendMsgToActiveView("ViewFit")
#Gui.activeDocument().activeView().viewAxonometric()


## Mount on insert stand
#Gui.Selection.clearSelection()
#Gui.Selection.addSelection(insert_stand, "Face001")
#Gui.Selection.addSelection(mgps_insert , "Face228")

#selection = Gui.Selection.getSelectionEx()
#mgps_insert_stand_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)

#mgps_insert_stand_planar.directionConstraint = u"opposed"
#App.ActiveDocument.recompute()


## Make concentric
#Gui.Selection.clearSelection()
#Gui.Selection.addSelection(insert_stand, "Face012")
#Gui.Selection.addSelection(mgps_insert , "Face228")

#selection = Gui.Selection.getSelectionEx()
#mgps_insert_stand_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)

################################################################################
## Import sus insert
#sus_insert = importPart.importPart(filename = 'models/Susceptibility_Insert.fcstd')

#App.ActiveDocument.recompute()
#Gui.SendMsgToActiveView("ViewFit")
#Gui.activeDocument().activeView().viewAxonometric()


## Mount on insert stand
#Gui.Selection.clearSelection()
#Gui.Selection.addSelection(insert_stand, "Face001")
#Gui.Selection.addSelection(sus_insert , "Face048")

#selection = Gui.Selection.getSelectionEx()
#sus_insert_stand_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)

#sus_insert_stand_planar.directionConstraint = u"opposed"
#App.ActiveDocument.recompute()


## Make concentric
#Gui.Selection.clearSelection()
#Gui.Selection.addSelection(insert_stand, "Face022")
#Gui.Selection.addSelection(sus_insert , "Face048")

#selection = Gui.Selection.getSelectionEx()
#sus_insert_stand_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)

################################################################################
## Import RT insert
#RT_insert = importPart.importPart(filename = 'models/RT_Insert.fcstd')

#App.ActiveDocument.recompute()
#Gui.SendMsgToActiveView("ViewFit")
#Gui.activeDocument().activeView().viewAxonometric()


## Mount on insert stand
#Gui.Selection.clearSelection()
#Gui.Selection.addSelection(insert_stand, "Face001")
#Gui.Selection.addSelection(RT_insert , "Face070")

#selection = Gui.Selection.getSelectionEx()
#RT_insert_stand_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)

#RT_insert_stand_planar.directionConstraint = u"opposed"
#App.ActiveDocument.recompute()


## Make concentric
#Gui.Selection.clearSelection()
#Gui.Selection.addSelection(insert_stand, "Face017")
#Gui.Selection.addSelection(RT_insert , "Face070")

#selection = Gui.Selection.getSelectionEx()
#RT_insert_stand_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)

################################################################################
## Import Hires insert
#hires_insert = importPart.importPart(filename = 'models/Hires_Insert.fcstd')

#App.ActiveDocument.recompute()
#Gui.SendMsgToActiveView("ViewFit")
#Gui.activeDocument().activeView().viewAxonometric()


## Mount on insert stand
#Gui.Selection.clearSelection()
#Gui.Selection.addSelection(insert_stand, "Face001")
#Gui.Selection.addSelection(hires_insert , "Face244")

#selection = Gui.Selection.getSelectionEx()
#hires_insert_stand_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)

#hires_insert_stand_planar.directionConstraint = u"opposed"
#App.ActiveDocument.recompute()


## Make concentric
#Gui.Selection.clearSelection()
#Gui.Selection.addSelection(insert_stand, "Face009")
#Gui.Selection.addSelection(hires_insert , "Face244")

#selection = Gui.Selection.getSelectionEx()
#hires_insert_stand_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)



##############################################################################
# Import table clamp
table_clamp = importPart.importPart(filename = 'models/table_clamp.fcstd')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Mate to table surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_table_setup, "Face001")
Gui.Selection.addSelection(table_clamp         , "Face321")

selection = Gui.Selection.getSelectionEx()
table_clamp_table_surface = planeConstraint.parseSelection(selection, objectToUpdate=None)

#Side offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_table_setup, "Face007")
Gui.Selection.addSelection(table_clamp         , "Face098")

selection = Gui.Selection.getSelectionEx()
table_clamp_table_side = planeConstraint.parseSelection(selection, objectToUpdate=None)

table_clamp_table_side.directionConstraint = u"aligned"
App.ActiveDocument.recompute()

# Front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_table_setup, "Face005")
Gui.Selection.addSelection(table_clamp         , "Face115")

selection = Gui.Selection.getSelectionEx()
table_clamp_table_front = planeConstraint.parseSelection(selection, objectToUpdate=None)

table_clamp_table_front.offset = 300
App.ActiveDocument.recompute()


##############################################################################
# Import VSM

vsm = importPart.importPart(filename = '../VSM/models/VSM.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place on Table
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vsm                 , "Face025")
Gui.Selection.addSelection(computer_table_setup, "Face010")

selection = Gui.Selection.getSelectionEx()
vsm_table_surface = planeConstraint.parseSelection(selection, objectToUpdate=None)

# Right offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vsm                 , "Face016")
Gui.Selection.addSelection(computer_table_setup, "Face005")

selection = Gui.Selection.getSelectionEx()
vsm_table_side = planeConstraint.parseSelection(selection, objectToUpdate=None)

vsm_table_side.offset = '-400 mm'
App.ActiveDocument.recompute()

# Front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vsm                 , "Face021")
Gui.Selection.addSelection(computer_table_setup, "Face007")

selection = Gui.Selection.getSelectionEx()
vsm_table_front = planeConstraint.parseSelection(selection, objectToUpdate=None)

vsm_table_front.offset = '-400 mm'
App.ActiveDocument.recompute()

###############################################################################
# Add valve knobs to cryostats

# Heater chamber Evacuation valve
heater_chamber_evacuation_valve = importPart.importPart(filename = 'models/Knob.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Mate heater_chamber_evacuation_valve to steel_cryostat (axial)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(heater_chamber_evacuation_valve, "Face011")
Gui.Selection.addSelection(steel_cryostat                 , "Face532")

selection = Gui.Selection.getSelectionEx()
steel_cryostat_heater_chamber_evacuation_valve_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)


# Mate sample_chamber_evacuation_valve to steel_cryostat (planar)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(heater_chamber_evacuation_valve, "Face011")
Gui.Selection.addSelection(steel_cryostat                 , "Face532")

selection = Gui.Selection.getSelectionEx()
steel_cryostat_heater_chamber_evacuation_valve_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)

##############################################
# Sample chamber Evacuation valve
sample_chamber_evacuation_valve = importPart.importPart(filename = 'models/Knob.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Mate sample_chamber_evacuation_valve to steel_cryostat (axial)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(sample_chamber_evacuation_valve, "Face011")
Gui.Selection.addSelection(steel_cryostat                 , "Face787")

selection = Gui.Selection.getSelectionEx()
steel_cryostat_sample_chamber_evacuation_valve_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)


# Mate sample_chamber_evacuation_valve to steel_cryostat (planar)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(sample_chamber_evacuation_valve, "Face011")
Gui.Selection.addSelection(steel_cryostat                 , "Face787")

selection = Gui.Selection.getSelectionEx()
steel_cryostat_sample_chamber_evacuation_valve_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)

##############################################
# Sample chamber flush valve
sample_chamber_flush_valve = importPart.importPart(filename = 'models/Knob.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Mate sample_chamber_flush_valve to steel_cryostat (axial)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(sample_chamber_flush_valve, "Face011")
Gui.Selection.addSelection(steel_cryostat            , "Face1735")

selection = Gui.Selection.getSelectionEx()
steel_cryostat_sample_chamber_flush_valve_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)

steel_cryostat_sample_chamber_flush_valve_axial.directionConstraint = u"opposed"
App.ActiveDocument.recompute()

# Mate sample_chamber_flush_valve to steel_cryostat (planar)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(sample_chamber_flush_valve, "Face011")
Gui.Selection.addSelection(steel_cryostat            , "Face1735")

selection = Gui.Selection.getSelectionEx()
steel_cryostat_sample_chamber_flush_valve_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)

##############################################
# Heater chamber flush valve
heater_chamber_flush_valve = importPart.importPart(filename = 'models/Knob.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Mate heater_chamber_flush_valve to steel_cryostat (axial)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(heater_chamber_flush_valve, "Face011")
Gui.Selection.addSelection(steel_cryostat            , "Face1644")

selection = Gui.Selection.getSelectionEx()
steel_cryostat_heater_chamber_flush_valve_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)


# Mate heater_chamber_flush_valve to steel_cryostat (planar)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(heater_chamber_flush_valve, "Face011")
Gui.Selection.addSelection(steel_cryostat            , "Face1644")

selection = Gui.Selection.getSelectionEx()
steel_cryostat_heater_chamber_flush_valve_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)


# TODO : Add quartz cryostat valve knobs


###############################################################################
# Add KF-25 O-ring

o_ring_steel_cryostat = importPart.importPart(filename = 'models/KF-25_O-ring.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Mate O-ring to steel_cryostat (axial)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(o_ring_steel_cryostat, "Face007")
Gui.Selection.addSelection(steel_cryostat       , "Face294")

selection = Gui.Selection.getSelectionEx()
steel_cryostat_o_ring_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)

steel_cryostat_o_ring_axial.directionConstraint = u"opposed"
App.ActiveDocument.recompute()

# Mate O-ring to steel_cryostat (planar)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(o_ring_steel_cryostat, "Face007")
Gui.Selection.addSelection(steel_cryostat       , "Face294")

selection = Gui.Selection.getSelectionEx()
steel_cryostat_o_ring_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)

# TODO : Add O-ring for quartz cryostat

##############################################################################
# Import mgps insert
mgps_insert = importPart.importPart(filename = 'models/MGPS_Insert.fcstd')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


# Mount on steel_cryostat (planar)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(o_ring_steel_cryostat, "Face011")
Gui.Selection.addSelection(mgps_insert          , "Face228")

selection = Gui.Selection.getSelectionEx()
mgps_insert_steel_cryostat_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)

mgps_insert_steel_cryostat_planar.directionConstraint = u"opposed"
App.ActiveDocument.recompute()


# Make concentric
Gui.Selection.clearSelection()
Gui.Selection.addSelection(o_ring_steel_cryostat, "Face011")
Gui.Selection.addSelection(mgps_insert          , "Face228")

selection = Gui.Selection.getSelectionEx()
mgps_insert_steel_cryostat_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)

##############################################################################
# Import clamps
clamp_steel_cryostat = importPart.importPart(filename = 'models/clamp.fcstd')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


# Mount on steel_cryostat (planar)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(clamp_steel_cryostat, "Face012")
Gui.Selection.addSelection(steel_cryostat      , "Face294")

selection = Gui.Selection.getSelectionEx()
clamp_steel_cryostat_planar = planeConstraint.parseSelection(selection, objectToUpdate=None)

clamp_steel_cryostat_planar.offset = 13
App.ActiveDocument.recompute()

# Make concentric
Gui.Selection.clearSelection()
Gui.Selection.addSelection(clamp_steel_cryostat, "Face235")
Gui.Selection.addSelection(steel_cryostat      , "Face284")

selection = Gui.Selection.getSelectionEx()
clamp_steel_cryostat_axial = axialConstraint.parseSelection(selection, objectToUpdate=None)

###############################################################################
### Import EM_Coupling_Experiment setup
##em_coupling_setup = importPart.importPart(filename = '../EM_Coupling_Experiment/models/assembly.fcstd', partName = None, doc_assembly = assembly_file)

##App.ActiveDocument.recompute()
##Gui.SendMsgToActiveView("ViewFit")
##Gui.activeDocument().activeView().viewAxonometric()

### Fix the position and orientation of the experiment setup with respect to the computer_table_setup

### Right offset
##Gui.Selection.clearSelection()
##Gui.Selection.addSelection(em_coupling_setup   , "Face011")
##Gui.Selection.addSelection(computer_table_setup, "Face005")

##selection = Gui.Selection.getSelectionEx()
##planeConstraint.parseSelection(selection, objectToUpdate=None)

##App.ActiveDocument.getObject("planeConstraint01_mirror").offset = 1100
##App.ActiveDocument.recompute()


### Front Offset
##Gui.Selection.clearSelection()
##Gui.Selection.addSelection(em_coupling_setup   , "Face971")
##Gui.Selection.addSelection(computer_table_setup, "Face003")

##selection = Gui.Selection.getSelectionEx()
##planeConstraint.parseSelection(selection, objectToUpdate=None)

##App.ActiveDocument.getObject("planeConstraint02_mirror").offset = 500
##App.ActiveDocument.recompute()


### Place on Table surface
##Gui.Selection.clearSelection()
##Gui.Selection.addSelection(em_coupling_setup   , "Face023")
##Gui.Selection.addSelection(computer_table_setup, "Face010")

##selection = Gui.Selection.getSelectionEx()
##planeConstraint.parseSelection(selection, objectToUpdate=None)

##App.ActiveDocument.recompute()