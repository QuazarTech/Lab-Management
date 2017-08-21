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
# Import STM_base

stm_base = importPart.importPart(filename = 'models/STM_base.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

stm_base.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))

###############################################################################
# Import STM_VIB

stm_VIB = importPart.importPart(filename = 'models/STM_VIB.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place on STM_base
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_base, "Face012")
Gui.Selection.addSelection(stm_VIB , "Face041")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


# Side offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_base, "Face002")
Gui.Selection.addSelection(stm_VIB , "Face266")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint02_mirror").offset = -70
App.ActiveDocument.recompute()


# Front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_base, "Face004")
Gui.Selection.addSelection(stm_VIB , "Face297")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint03_mirror").offset = -100
App.ActiveDocument.recompute()

###############################################################################
# Import STM_shroud

stm_shroud = importPart.importPart(filename = 'models/STM_shroud.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


# Align Rear Hole
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_shroud, "Face140")
Gui.Selection.addSelection(stm_VIB   , "Face114")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("axialConstraint01").directionConstraint = u"aligned"
App.ActiveDocument.recompute()

# Align Front hole
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_shroud, "Face125")
Gui.Selection.addSelection(stm_VIB   , "Face148")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

# Place on STM VIB
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_shroud, "Face043")
Gui.Selection.addSelection(stm_VIB   , "Face177")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

