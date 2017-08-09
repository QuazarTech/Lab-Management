import sys
sys.path.append('${HOME}/.FreeCAD/Mod/FreeCAD_assembly2')

from experiment_params import *

# Create and open a new file for assembly
assembly_file = App.newDocument("experiment_assembly")
App.setActiveDocument(assembly_file.Name)
App.ActiveDocument = App.getDocument(assembly_file.Name)
Gui.ActiveDocument = Gui.getDocument(assembly_file.Name)

###############################################################################
## Import all parts into the assembly

import importPart

# import cover_bottom
cover_base = importPart.importPart(filename = '../models/cover_base.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# import mounting rod
mount = importPart.importPart(filename = '../models/mount.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# import cores
core_1 = importPart.importPart(filename = '../models/core.fcstd', partName = None, doc_assembly = assembly_file)
core_2 = importPart.importPart(filename = '../models/core.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# import coils
coil_1 = importPart.importPart(filename = '../models/coil.fcstd', partName = None, doc_assembly = assembly_file)
coil_2 = importPart.importPart(filename = '../models/coil.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# import cover_top
cover_top = importPart.importPart(filename = '../models/cover_top.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# import BNC Connectors
bnc_conn_1 = importPart.importPart(filename = '../models/BNC_Conn.fcstd', partName = None, doc_assembly = assembly_file)
bnc_conn_2 = importPart.importPart(filename = '../models/BNC_Conn.fcstd', partName = None, doc_assembly = assembly_file)

#import Lockin Amplifier
xlia = importPart.importPart(filename = '../models/Lockin_base.STEP', partName = None, doc_assembly = assembly_file) 

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

###############################################################################
raw_input('All parts imported. Press Enter to assemble the Core Mounting Rod on the Cover Base.')
###############################################################################
import axialConstraint

## Mate Mounting rod to cover_bottom

Gui.Selection.clearSelection()                       # Clear the selection list, no items selected
Gui.Selection.addSelection(mount     , "Face005")    # Select the curved face on mounting rod to create an axial mate (must be a curved face)
Gui.Selection.addSelection(cover_base, "Face020")    # Select the curved face on cover base to create an axial mate (must be a curved face)

selection = Gui.Selection.getSelectionEx()           # Get the selection list from the FreeCAD Gui
axialConstraint.parseSelection(selection, objectToUpdate=None) # Create axial mate between the selected surfaces

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint01").directionConstraint = u"aligned" # Set property of mate to 'aligned'.
FreeCAD.ActiveDocument.recompute()                   # Recompute the document

###############################################################################
raw_input('Core Mounting Rod assembled. Press Enter to Mount the Core onto the rod.')
###############################################################################
## Mate to mount cores onto the mounting rod

Gui.Selection.clearSelection()
Gui.Selection.addSelection(mount , "Face005")
Gui.Selection.addSelection(core_1, "Face003")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint02").directionConstraint = u"aligned"
FreeCAD.ActiveDocument.recompute()



Gui.Selection.clearSelection()
Gui.Selection.addSelection(mount , "Face005")
Gui.Selection.addSelection(core_2, "Face003")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint03").directionConstraint = u"opposed"
FreeCAD.ActiveDocument.recompute()

## Add plane constraint to fix the cores against the cover_base walls

import planeConstraint

Gui.Selection.clearSelection()
Gui.Selection.addSelection(core_1    , "Face001")
Gui.Selection.addSelection(cover_base, "Face032")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


Gui.Selection.clearSelection()
Gui.Selection.addSelection(core_2    , "Face001")
Gui.Selection.addSelection(cover_base, "Face013")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

###############################################################################
raw_input('Cores assembled. Press Enter to Mount the Coaxial Cable Connectors onto the Cover Base.')
###############################################################################
## Mount the Coaxial cable Connectors onto the cover_base walls

Gui.Selection.clearSelection()
Gui.Selection.addSelection(bnc_conn_1, "Face898")
Gui.Selection.addSelection(cover_base, "Face019")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint04").directionConstraint = u"opposed"
FreeCAD.ActiveDocument.recompute()


Gui.Selection.clearSelection()
Gui.Selection.addSelection(bnc_conn_2, "Face898")
Gui.Selection.addSelection(cover_base, "Face038")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint05").directionConstraint = u"aligned"
FreeCAD.ActiveDocument.recompute()


Gui.Selection.clearSelection()
Gui.Selection.addSelection(bnc_conn_1, "Face1831")
Gui.Selection.addSelection(cover_base, "Face015")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


Gui.Selection.clearSelection()
Gui.Selection.addSelection(bnc_conn_2, "Face1831")
Gui.Selection.addSelection(cover_base, "Face034")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

###############################################################################
raw_input('Coaxial Cable Connectors assembled. Press Enter to assemble the coils on respective cores')
###############################################################################
## Mount coils onto respective cores

FreeCAD.getDocument("experiment_assembly").getObject("coil_01").Placement = App.Placement(App.Vector(base_height, base_width/2, wall_height/2),App.Rotation(App.Vector(0,1,0),90))

FreeCAD.getDocument("experiment_assembly").getObject("coil_02").Placement = App.Placement(App.Vector(base_length-base_height-coil_height, base_width/2, wall_height/2),App.Rotation(App.Vector(0,1,0),90))

###############################################################################
raw_input('Coils assembled. Press Enter to assemble the Cover Top over the Cover Base')
###############################################################################
## Mount cover_top over cover_base

Gui.Selection.clearSelection()
Gui.Selection.addSelection(cover_top , "Face010")   
Gui.Selection.addSelection(cover_base, "Face045")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)
FreeCAD.ActiveDocument.recompute()


Gui.Selection.clearSelection()
Gui.Selection.addSelection(cover_top , "Face015")
Gui.Selection.addSelection(cover_base, "Face008")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint06").directionConstraint = u"aligned"
FreeCAD.ActiveDocument.recompute()


Gui.Selection.clearSelection()
Gui.Selection.addSelection(cover_top , "Face018")
Gui.Selection.addSelection(cover_base, "Face048")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint07").directionConstraint = u"aligned"
FreeCAD.ActiveDocument.recompute()

###############################################################################
raw_input('Cover Top assembled. Press Enter to assemble the Lockin Amplifier')
###############################################################################
## Mount cover_top over cover_base

Gui.Selection.clearSelection()
Gui.Selection.addSelection(xlia , "Face520")
Gui.Selection.addSelection(cover_base, "Face026")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)
FreeCAD.ActiveDocument.recompute()


Gui.Selection.clearSelection()
Gui.Selection.addSelection(xlia , "Face200")
Gui.Selection.addSelection(cover_base, "Face015")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)
FreeCAD.ActiveDocument.recompute()


Gui.Selection.clearSelection()
Gui.Selection.addSelection(xlia , "Vertex1070")
Gui.Selection.addSelection(cover_base, "Face004")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)
FreeCAD.ActiveDocument.recompute()
