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

assembly_file = App.newDocument("daq")
App.setActiveDocument(assembly_file.Name)
App.ActiveDocument = App.getDocument(assembly_file.Name)
Gui.ActiveDocument = Gui.getDocument(assembly_file.Name)

###############################################################################
# Import computer_table
computer_table = importPart.importPart(filename = '../computer/models/Table.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Fix the position and orientation of computer_table
computer_table.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))

################################################################################
# Import QM9 Data Acquisition System base

daq_base = importPart.importPart(filename = 'models/QM9_base.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


# Place on table
Gui.Selection.clearSelection()
Gui.Selection.addSelection(daq_base      , "Face227")                        
Gui.Selection.addSelection(computer_table, "Face010")

selection = Gui.Selection.getSelectionEx()
daq_base_table_surface = planeConstraint.parseSelection(selection, objectToUpdate=None)

daq_base_table_surface.directionConstraint = u"opposed"
App.ActiveDocument.recompute()


# Side offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(daq_base      , "Face232")                        
Gui.Selection.addSelection(computer_table, "Face005")

selection = Gui.Selection.getSelectionEx()
daq_base_table_side = planeConstraint.parseSelection(selection, objectToUpdate=None)

daq_base_table_side.offset = 500
App.ActiveDocument.recompute()

# Front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(daq_base      , "Face236")                        
Gui.Selection.addSelection(computer_table, "Face007")

selection = Gui.Selection.getSelectionEx()
daq_base_table_front = planeConstraint.parseSelection(selection, objectToUpdate=None)

daq_base_table_front.offset = -200
App.ActiveDocument.recompute()

################################################################################
# Import QM9 Data Acquisition System top

daq_top = importPart.importPart(filename = 'models/QM9_top.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


# Place on daq base
Gui.Selection.clearSelection()
Gui.Selection.addSelection(daq_base, "Face265")                        
Gui.Selection.addSelection(daq_top , "Face126")

selection = Gui.Selection.getSelectionEx()
daq_base_top = planeConstraint.parseSelection(selection, objectToUpdate=None)

daq_base_top.directionConstraint = u"opposed"
App.ActiveDocument.recompute()


# Side mate
Gui.Selection.clearSelection()
Gui.Selection.addSelection(daq_base, "Face242")                        
Gui.Selection.addSelection(daq_top , "Face133")

selection = Gui.Selection.getSelectionEx()
daq_base_top_side = planeConstraint.parseSelection(selection, objectToUpdate=None)

# Front mate
Gui.Selection.clearSelection()
Gui.Selection.addSelection(daq_base, "Face226")                        
Gui.Selection.addSelection(daq_top , "Face157")

selection = Gui.Selection.getSelectionEx()
daq_base_top_front = planeConstraint.parseSelection(selection, objectToUpdate=None)

