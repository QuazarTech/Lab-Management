import sys
sys.path.append('${HOME}/.FreeCAD/Mod/FreeCAD_assembly2')

import importPart
import planeConstraint

# Create and open a new file for assembly
assembly_file = App.newDocument("lab_assembly")
App.setActiveDocument(assembly_file.Name)
App.ActiveDocument = App.getDocument(assembly_file.Name)
Gui.ActiveDocument = Gui.getDocument(assembly_file.Name)

###############################################################################
## Import all parts into the assembly

# import Computer_Table Assembly
computer_assembly = importPart.importPart(filename = 'models/Computer_Assembly.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# import EM_coupling_experiment Assembly
EM_coupling_experiment = importPart.importPart(filename = 'models/experiment_assembly.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

###############################################################################
raw_input('All parts imported. Press Enter to assemble the experiment_assembly on the computer table.')
###############################################################################

# Place the experiment setup on the table surface
Gui.Selection.clearSelection()                                   # Clear the selection list, no items selected
Gui.Selection.addSelection(computer_assembly     , "Face1397")   # Select the face on computer_assembly to create a planar mate on (must be a plane face)
Gui.Selection.addSelection(EM_coupling_experiment, "Face026")    # Select the face on EM_coupling_experiment to create a planar mate on (must be a plane face)

selection = Gui.Selection.getSelectionEx()                       # Get the selected items from FreeCAD Gui
planeConstraint.parseSelection(selection, objectToUpdate=None)   # Create a Planar mate on the selected faces

# Mate from side
Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_assembly     , "Face1012")
Gui.Selection.addSelection(EM_coupling_experiment, "Face034")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


#Mate back surfaces
Gui.Selection.clearSelection()
Gui.Selection.addSelection(computer_assembly     , "Face894")
Gui.Selection.addSelection(EM_coupling_experiment, "Face967")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

