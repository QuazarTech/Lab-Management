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
computer_table = importPart.importPart(filename = '../models/Table.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Fix the position and orientation of computer_table
computer_table.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))

###############################################################################
# Import computer_monitor
computer_monitor = importPart.importPart(filename = '../models/monitor.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Fix the position and orientation of computer_monitor with respect to computer_table

# Place on table place
Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_monitor, "Face701")
Gui.Selection.addSelection(computer_table  , "Face010")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

# Right Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_monitor, "Face499")
Gui.Selection.addSelection(computer_table  , "Face005")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint02").offset = -250
App.ActiveDocument.recompute()

# Front Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_monitor, "Face671")
Gui.Selection.addSelection(computer_table  , "Face007")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint03").offset = -600
App.ActiveDocument.recompute()

###############################################################################
# Import computer_keyboard
computer_keyboard = importPart.importPart(filename = '../models/Keyboard.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Fix the position and orientation of computer_keyboard with respect to computer_table
Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_keyboard, "Face242")
Gui.Selection.addSelection(computer_table  , "Face010")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

# Right Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_keyboard, "Face064")
Gui.Selection.addSelection(computer_table  , "Face005")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint05").offset = 380
App.ActiveDocument.recompute()


Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_keyboard, "Face063")
Gui.Selection.addSelection(computer_table  , "Face003")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint06").offset = 400
App.ActiveDocument.recompute()

###############################################################################
# Import computer_cpu
computer_cpu = importPart.importPart(filename = '../models/CPU.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Fix the position and orientation of computer_cpu with respect to computer_table
Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_cpu, "Face114")
Gui.Selection.addSelection(computer_table  , "Face010")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_cpu, "Face142")
Gui.Selection.addSelection(computer_table  , "Face003")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint08").offset = 10
App.ActiveDocument.recompute()

# Right Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_cpu, "Face113")
Gui.Selection.addSelection(computer_table  , "Face005")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint09").offset = 850
App.ActiveDocument.recompute()

################################################################################
##Gui.Selection.getSelectionEx()[0].FullName
