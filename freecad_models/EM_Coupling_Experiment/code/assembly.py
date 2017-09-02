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
from experiment_params import base_height
from experiment_params import base_width
from experiment_params import base_length
from experiment_params import wall_height
from experiment_params import coil_height

###############################################################################
# Create and open a new file for assembly

assembly_file = App.newDocument("experiment_assembly")
App.setActiveDocument(assembly_file.Name)
App.ActiveDocument = App.getDocument(assembly_file.Name)
Gui.ActiveDocument = Gui.getDocument(assembly_file.Name)

###############################################################################
# Import all parts into the assembly

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
bnc_conn_1 = importPart.importPart(filename = '../models/std/BNC_Conn.fcstd', partName = None, doc_assembly = assembly_file)
bnc_conn_2 = importPart.importPart(filename = '../models/std/BNC_Conn.fcstd', partName = None, doc_assembly = assembly_file)

# Recompute and fit to screen
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Set view to axonometric - Isometric
Gui.activeDocument().activeView().viewAxonometric()

###############################################################################
raw_input('All parts imported. Press Enter to assemble the Core Mounting Rod on the Cover Base.')
###############################################################################

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

Gui.Selection.clearSelection()
Gui.Selection.addSelection(core_1    , "Face001")
Gui.Selection.addSelection(cover_base, "Face040")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

Gui.Selection.clearSelection()
Gui.Selection.addSelection(core_2    , "Face001")
Gui.Selection.addSelection(cover_base, "Face021")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

###############################################################################
raw_input('Cores assembled. Press Enter to Mount the Coaxial Cable Connectors onto the Cover Base.')
###############################################################################
## Mount the Coaxial cable Connectors onto the cover_base walls

Gui.Selection.clearSelection()
Gui.Selection.addSelection(bnc_conn_1, "Face004")
Gui.Selection.addSelection(cover_base, "Face019")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint04").directionConstraint = u"opposed"
FreeCAD.ActiveDocument.recompute()


Gui.Selection.clearSelection()
Gui.Selection.addSelection(bnc_conn_2, "Face004")
Gui.Selection.addSelection(cover_base, "Face038")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint05").directionConstraint = u"aligned"
FreeCAD.ActiveDocument.recompute()

Gui.Selection.clearSelection()
Gui.Selection.addSelection(bnc_conn_1, "Face069")
Gui.Selection.addSelection(cover_base, "Face011")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


Gui.Selection.clearSelection()
Gui.Selection.addSelection(bnc_conn_2, "Face069")
Gui.Selection.addSelection(cover_base, "Face031")

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
Gui.Selection.addSelection(cover_base, "Face001")

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
Gui.Selection.addSelection(cover_base, "Face052")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint07").directionConstraint = u"aligned"
FreeCAD.ActiveDocument.recompute()

###############################################################################
raw_input('Cover Top assembled. Press Enter to assemble the M3 rivet nuts')
###############################################################################
## Assemble Rivet nuts on the cover base

rivet_nut_1 = importPart.importPart(filename = '../models/std/M3_rivet_nut.STEP', partName = None, doc_assembly = assembly_file)
rivet_nut_2 = importPart.importPart(filename = '../models/std/M3_rivet_nut.STEP', partName = None, doc_assembly = assembly_file)
rivet_nut_3 = importPart.importPart(filename = '../models/std/M3_rivet_nut.STEP', partName = None, doc_assembly = assembly_file)
rivet_nut_4 = importPart.importPart(filename = '../models/std/M3_rivet_nut.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

#################
# Nut 1


Gui.Selection.clearSelection()
Gui.Selection.addSelection(rivet_nut_1 , "Face005")
Gui.Selection.addSelection(cover_base  , "Face052")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint08").directionConstraint = u"aligned"
FreeCAD.ActiveDocument.recompute()


Gui.Selection.clearSelection()
Gui.Selection.addSelection(rivet_nut_1 , "Face013")   
Gui.Selection.addSelection(cover_base  , "Face050")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)
FreeCAD.ActiveDocument.recompute()

#################
# Nut 2

Gui.Selection.clearSelection()
Gui.Selection.addSelection(rivet_nut_2 , "Face005")
Gui.Selection.addSelection(cover_base  , "Face051")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint09").directionConstraint = u"aligned"
FreeCAD.ActiveDocument.recompute()


Gui.Selection.clearSelection()
Gui.Selection.addSelection(rivet_nut_2 , "Face013")   
Gui.Selection.addSelection(cover_base  , "Face050")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)
FreeCAD.ActiveDocument.recompute()

#################
# Nut 3

Gui.Selection.clearSelection()
Gui.Selection.addSelection(rivet_nut_3 , "Face005")
Gui.Selection.addSelection(cover_base  , "Face008")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint10").directionConstraint = u"aligned"
FreeCAD.ActiveDocument.recompute()


Gui.Selection.clearSelection()
Gui.Selection.addSelection(rivet_nut_3 , "Face013")   
Gui.Selection.addSelection(cover_base  , "Face009")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)
FreeCAD.ActiveDocument.recompute()


#################
# Nut 4

Gui.Selection.clearSelection()
Gui.Selection.addSelection(rivet_nut_4 , "Face005")
Gui.Selection.addSelection(cover_base  , "Face013")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint11").directionConstraint = u"aligned"
FreeCAD.ActiveDocument.recompute()


Gui.Selection.clearSelection()
Gui.Selection.addSelection(rivet_nut_4 , "Face013")   
Gui.Selection.addSelection(cover_base  , "Face009")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)
FreeCAD.ActiveDocument.recompute()


###############################################################################
raw_input('Rivet Nuts assembled. Press Enter to assemble the M4 * 10 Washer Head Screws')
###############################################################################
## Assemble Screws on the side of cover base to hold the mounting rod in Place

M4_WH_screw_1 = importPart.importPart(filename = '../models/std/M4_10_WH_Screw.STEP', partName = None, doc_assembly = assembly_file)
M4_WH_screw_2 = importPart.importPart(filename = '../models/std/M4_10_WH_Screw.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


###########
# Screw 1

Gui.Selection.clearSelection()
Gui.Selection.addSelection(M4_WH_screw_1, "Face005")
Gui.Selection.addSelection(cover_base   , "Face020")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint12").directionConstraint = u"aligned"
FreeCAD.ActiveDocument.recompute()

Gui.Selection.clearSelection()
Gui.Selection.addSelection(M4_WH_screw_1 , "Face013")   
Gui.Selection.addSelection(cover_base    , "Face011")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)
FreeCAD.ActiveDocument.recompute()


###########
# Screw 2

Gui.Selection.clearSelection()
Gui.Selection.addSelection(M4_WH_screw_2, "Face005")   
Gui.Selection.addSelection(cover_base   , "Face039")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

FreeCAD.getDocument("experiment_assembly").getObject("axialConstraint13").directionConstraint = u"opposed"
FreeCAD.ActiveDocument.recompute()


Gui.Selection.clearSelection()
Gui.Selection.addSelection(M4_WH_screw_2 , "Face013")   
Gui.Selection.addSelection(cover_base    , "Face031")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)
FreeCAD.ActiveDocument.recompute()

