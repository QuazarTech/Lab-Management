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

assembly_file = App.newDocument("cvd")
App.setActiveDocument(assembly_file.Name)
App.ActiveDocument = App.getDocument(assembly_file.Name)
Gui.ActiveDocument = Gui.getDocument(assembly_file.Name)

###############################################################################
# Import cvd_electronics
cvd_electronics = importPart.importPart(filename = 'models/CVD_electronics.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

cvd_electronics.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))

###############################################################################
# Import cvd_oven
cvd_oven = importPart.importPart(filename = 'models/CVD_oven.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place on cvd_electronics top
Gui.Selection.clearSelection()
Gui.Selection.addSelection(cvd_electronics, "Face1391")
Gui.Selection.addSelection(cvd_oven       , "Face037")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint01").directionConstraint = u"opposed"
App.ActiveDocument.recompute()

# Front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(cvd_electronics, "Face3109")
Gui.Selection.addSelection(cvd_oven       , "Face296")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

###############################################################################
# Import pump
cvd_pump = importPart.importPart(filename = 'models/Pump.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place on ground
Gui.Selection.clearSelection()
Gui.Selection.addSelection(cvd_electronics, "Face1630")
Gui.Selection.addSelection(cvd_pump       , "Face025")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

cvd_pump.Placement = App.Placement(App.Vector(470,150,114),App.Rotation(App.Vector(0.57735,0.57735,0.57735),120))
App.ActiveDocument.recompute()
