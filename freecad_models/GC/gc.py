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

assembly_file = App.newDocument("computer_table_setup")
App.setActiveDocument(assembly_file.Name)
App.ActiveDocument = App.getDocument(assembly_file.Name)
Gui.ActiveDocument = Gui.getDocument(assembly_file.Name)

###############################################################################
# Import computer_table
table = importPart.importPart(filename = '../computer/models/Table.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Fix the position and orientation of computer_table
table.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))

################################################################################
# Import QSAW

qsaw = importPart.importPart(filename = '../QSAW/models/QSAW.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


#Place on table surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(table, "Face010")
Gui.Selection.addSelection(qsaw , "Face007")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

# Right offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(table, "Face005")
Gui.Selection.addSelection(qsaw , "Face006")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint02").offset = '100 mm'
App.ActiveDocument.recompute()

#Front Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(table, "Face007")
Gui.Selection.addSelection(qsaw , "Face498")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint03").offset = '300 mm'
App.ActiveDocument.recompute()

##############################################################################
# Import GC
gc = importPart.importPart(filename = '../GC/models/GC.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place on table surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(table, "Face010")
Gui.Selection.addSelection(gc   , "Face2783")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


# Right offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(table, "Face005")
Gui.Selection.addSelection(gc   , "Face1091")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint05").offset = '600 mm'
App.ActiveDocument.recompute()


#Front Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(table, "Face007")
Gui.Selection.addSelection(gc   , "Face654")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint06").offset = '300 mm'
App.ActiveDocument.recompute()

