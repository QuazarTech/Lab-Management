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
# Import EM_Coupling_Experiment setup
em_coupling_setup = importPart.importPart(filename = '../EM_Coupling_Experiment/models/assembly.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Fix the position and orientation of the experiment setup with respect to the computer_table_setup

# Right offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(em_coupling_setup   , "Face011")
Gui.Selection.addSelection(computer_table_setup, "Face005")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint01_mirror").offset = 1100
App.ActiveDocument.recompute()


# Front Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(em_coupling_setup   , "Face971")
Gui.Selection.addSelection(computer_table_setup, "Face003")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint02_mirror").offset = 500
App.ActiveDocument.recompute()


# Place on Table surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(em_coupling_setup   , "Face023")
Gui.Selection.addSelection(computer_table_setup, "Face010")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.recompute()

###############################################################################
# Import PQMS Electronics Box

xplore_electronics = importPart.importPart(filename = 'models/xpl_electronics.STEP')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Fix the position and orientation of xplore electronics with respect to the computer_table_setup

# Place the xplore electronics boxes on the table surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(xplore_electronics  , "Face012")
Gui.Selection.addSelection(computer_table_setup, "Face010")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.recompute()


# Right offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(xplore_electronics  , "Face599")
Gui.Selection.addSelection(computer_table_setup, "Face009")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint05").offset = -150

App.ActiveDocument.recompute()


# Front Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(xplore_electronics  , "Face656")
Gui.Selection.addSelection(computer_table_setup, "Face003")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

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
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.recompute()

# Right offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(pirani_guage  , "Face050")
Gui.Selection.addSelection(computer_table_setup, "Face005")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint08").offset = -50
App.ActiveDocument.recompute()


# front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(pirani_guage  , "Face037")
Gui.Selection.addSelection(computer_table_setup, "Face003")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint09").offset = 500
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
planeConstraint.parseSelection(selection, objectToUpdate=None)

xpl_vaccum_pump.Placement = App.Placement(App.Vector(1500,0,-494.6),App.Rotation(App.Vector(1,1.66533e-16,-1.69938e-32),90))
App.ActiveDocument.recompute()

###############################################################################
# Import Xplore quartz cryostat
quartz_cryostat = importPart.importPart(filename = 'models/Quartz_Cryostat.STEP')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place the cryostat on the ground surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(quartz_cryostat  , "Face019")
Gui.Selection.addSelection(computer_table_setup, "Face022")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

# Front Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(quartz_cryostat  , "Face223")
Gui.Selection.addSelection(computer_table_setup, "Face023")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

# Side Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(quartz_cryostat  , "Face020")
Gui.Selection.addSelection(computer_table_setup, "Face005")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint13").offset = 200
App.ActiveDocument.recompute()

###############################################################################
# Import Xplore steel cryostat
steel_cryostat = importPart.importPart(filename = 'models/Steel_Cryostat.STEP')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place the cryostat on the ground surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(steel_cryostat  , "Face019")
Gui.Selection.addSelection(computer_table_setup, "Face022")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

# Front Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(steel_cryostat  , "Face196")
Gui.Selection.addSelection(computer_table_setup, "Face023")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

# Side Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(steel_cryostat  , "Face020")
Gui.Selection.addSelection(computer_table_setup, "Face005")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint16").offset = 750
App.ActiveDocument.recompute()

###############################################################################
# Import insert stand
insert_stand = importPart.importPart(filename = 'models/insert_stand.fcstd')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place on table surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(insert_stand  , "Face034")
Gui.Selection.addSelection(computer_table_setup, "Face010")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


# Front Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(insert_stand  , "Face026")
Gui.Selection.addSelection(computer_table_setup, "Face003")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


# Side Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(insert_stand  , "Face037")
Gui.Selection.addSelection(computer_table_setup, "Face005")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint19_mirror").offset = -50
App.ActiveDocument.recompute()

###############################################################################
# Import mgps insert
mgps_insert = importPart.importPart(filename = 'models/MGPS_Insert.STEP')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


# Mount on insert stand
Gui.Selection.clearSelection()
Gui.Selection.addSelection(insert_stand, "Face001")
Gui.Selection.addSelection(mgps_insert , "Face020")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint20_mirror").directionConstraint = u"opposed"
App.ActiveDocument.recompute()


# Make concentric
Gui.Selection.clearSelection()
Gui.Selection.addSelection(insert_stand, "Face012")
Gui.Selection.addSelection(mgps_insert , "Face020")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

###############################################################################
# Import sus insert
sus_insert = importPart.importPart(filename = 'models/Susceptibility_Insert.STEP')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


# Mount on insert stand
Gui.Selection.clearSelection()
Gui.Selection.addSelection(insert_stand, "Face001")
Gui.Selection.addSelection(sus_insert , "Face012")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint21_mirror").directionConstraint = u"opposed"
App.ActiveDocument.recompute()


# Make concentric
Gui.Selection.clearSelection()
Gui.Selection.addSelection(insert_stand, "Face022")
Gui.Selection.addSelection(sus_insert , "Face012")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

###############################################################################
# Import RT insert
RT_insert = importPart.importPart(filename = 'models/RT_Insert.STEP')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


# Mount on insert stand
Gui.Selection.clearSelection()
Gui.Selection.addSelection(insert_stand, "Face001")
Gui.Selection.addSelection(RT_insert , "Face037")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint22_mirror").directionConstraint = u"opposed"
App.ActiveDocument.recompute()


# Make concentric
Gui.Selection.clearSelection()
Gui.Selection.addSelection(insert_stand, "Face017")
Gui.Selection.addSelection(RT_insert , "Face037")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

###############################################################################
# Import Hires insert
hires_insert = importPart.importPart(filename = 'models/Hires_Insert.STEP')

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


# Mount on insert stand
Gui.Selection.clearSelection()
Gui.Selection.addSelection(insert_stand, "Face001")
Gui.Selection.addSelection(hires_insert , "Face013")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint23_mirror").directionConstraint = u"opposed"
App.ActiveDocument.recompute()


# Make concentric
Gui.Selection.clearSelection()
Gui.Selection.addSelection(insert_stand, "Face009")
Gui.Selection.addSelection(hires_insert , "Face013")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

###############################################################################
#Gui.Selection.getSelectionEx()[0].FullName