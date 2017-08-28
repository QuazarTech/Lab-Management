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

assembly_file = App.newDocument("stm")
App.setActiveDocument(assembly_file.Name)
App.ActiveDocument = App.getDocument(assembly_file.Name)
Gui.ActiveDocument = Gui.getDocument(assembly_file.Name)

###############################################################################
# Import STM_base

stm_base = importPart.importPart(filename = 'models/STM_base.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

stm_base.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))

###############################################################################
# Import STM_VIB

stm_VIB = importPart.importPart(filename = 'models/STM_VIB.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place on STM_base
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_base, "Face012")
Gui.Selection.addSelection(stm_VIB , "Face288")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


# Side offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_base, "Face002")
Gui.Selection.addSelection(stm_VIB , "Face480")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint02_mirror").offset = -70
App.ActiveDocument.recompute()


# Front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_base, "Face004")
Gui.Selection.addSelection(stm_VIB , "Face220")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint03_mirror").offset = -100
App.ActiveDocument.recompute()

###############################################################################
# Import STM_shroud

stm_shroud = importPart.importPart(filename = 'models/STM_shroud.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


# Place on STM VIB
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_shroud, "Face043")
Gui.Selection.addSelection(stm_VIB   , "Face403")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint04").directionConstraint = u"aligned"
App.ActiveDocument.recompute()


# Align Rear Hole
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_shroud, "Face079")
Gui.Selection.addSelection(stm_VIB   , "Face119")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)

# Align Front hole
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_shroud, "Face046")
Gui.Selection.addSelection(stm_VIB   , "Face120")

selection = Gui.Selection.getSelectionEx()
axialConstraint.parseSelection(selection, objectToUpdate=None)


###############################################################################
# Import STM_table

stm_table = importPart.importPart(filename = '../computer/models/Table.STEP', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place STM on table
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_table, "Face010")
Gui.Selection.addSelection(stm_base   , "Face010")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

# Right Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_table, "Face005")
Gui.Selection.addSelection(stm_base   , "Face006")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint06").offset = '800 mm'
App.ActiveDocument.recompute()

# Front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_table, "Face003")
Gui.Selection.addSelection(stm_base   , "Face008")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint07").offset = '200 mm'
App.ActiveDocument.recompute()

###############################################################################
# Import STM_electronics boxes

stm_electronics = importPart.importPart(filename = 'models/STM_electronics.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

#Place on table surface
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_base       , "Face010")
Gui.Selection.addSelection(stm_electronics, "Face910")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


# Front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_base       , "Face008")
Gui.Selection.addSelection(stm_electronics, "Face274")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


#Side offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(stm_base       , "Face002")
Gui.Selection.addSelection(stm_electronics, "Face1232")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint10_mirror").offset = '50 mm'
App.ActiveDocument.recompute()

###############################################################################
# Import AFM base

afm_base = importPart.importPart(filename = '../AFM/models/AFM_base.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place on AFM_Table
Gui.Selection.clearSelection()
Gui.Selection.addSelection(afm_base , "Face012")
Gui.Selection.addSelection(stm_table, "Face010")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

# Side Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(afm_base , "Face007")
Gui.Selection.addSelection(stm_table, "Face005")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint12").offset = '50 mm'
App.ActiveDocument.recompute()

# Front Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(afm_base, "Face009")
Gui.Selection.addSelection(stm_base, "Face008")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

###############################################################################
# Import AFM_electronics
afm_electronics = importPart.importPart(filename = '../AFM/models/AFM_electronics.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place on AFM_Table
Gui.Selection.clearSelection()
Gui.Selection.addSelection(afm_electronics, "Face1081")
Gui.Selection.addSelection(stm_table      , "Face010")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

#Right Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(afm_electronics, "Face377")
Gui.Selection.addSelection(afm_base       , "Face003")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


App.ActiveDocument.getObject("planeConstraint15").offset = '-50 mm'
App.ActiveDocument.recompute()

# Front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(afm_electronics, "Face1487")
Gui.Selection.addSelection(stm_base       , "Face008")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


###############################################################################