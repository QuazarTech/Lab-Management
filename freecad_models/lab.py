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

assembly_file = App.newDocument("lab")
App.setActiveDocument(assembly_file.Name)
App.ActiveDocument = App.getDocument(assembly_file.Name)
Gui.ActiveDocument = Gui.getDocument(assembly_file.Name)

###############################################################################
# Import PQMS

pqms = importPart.importPart(filename = 'XPLORE/pqms.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

###############################################################################
# Import VSTM
vstm = importPart.importPart(filename = 'VSTM/VSTM.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place the VSTM table on the ground
Gui.Selection.clearSelection()
Gui.Selection.addSelection(pqms, "Face039")
Gui.Selection.addSelection(vstm, "Face021")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

# Side offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(pqms, "Face009")
Gui.Selection.addSelection(vstm, "Face038")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

# Front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(pqms, "Face007")
Gui.Selection.addSelection(vstm, "Face036")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

################################################################################
# Import AFM and STM
microscopes = importPart.importPart(filename = 'STM/stm.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place the STM/AFM table on the ground
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vstm        , "Face043")
Gui.Selection.addSelection(microscopes, "Face1067")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

# Right Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vstm       , "Face036")
Gui.Selection.addSelection(microscopes, "Face1050")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint05_mirror").directionConstraint = u"opposed"
App.ActiveDocument.recompute()

# Front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(vstm       , "Face034")
Gui.Selection.addSelection(microscopes, "Face1052")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

###############################################################################
# Import GC and QSAW
gc = importPart.importPart(filename = 'GC/gc.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place the STM table on the ground
Gui.Selection.clearSelection()
Gui.Selection.addSelection(microscopes, "Face1084")
Gui.Selection.addSelection(gc         , "Face022")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

# Right Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(microscopes, "Face1054")
Gui.Selection.addSelection(gc         , "Face005")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint08_mirror").directionConstraint = u"opposed"
App.ActiveDocument.recompute()

# Front offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(microscopes, "Face1052")
Gui.Selection.addSelection(gc         , "Face007")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

#############################################################################

# Import CVD
cvd = importPart.importPart(filename = 'CVD/cvd.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()


# Place the CVD on the ground
Gui.Selection.clearSelection()
Gui.Selection.addSelection(gc , "Face039")
Gui.Selection.addSelection(cvd, "Face5663")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


# Right offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(gc , "Face009")
Gui.Selection.addSelection(cvd, "Face3649")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

App.ActiveDocument.getObject("planeConstraint11").offset = -500
App.ActiveDocument.getObject("planeConstraint11").directionConstraint = u"opposed"
App.ActiveDocument.recompute()

# Front Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(gc , "Face007")
Gui.Selection.addSelection(cvd, "Face241")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)

#############################################################################

# Import DAQ
daq = importPart.importPart(filename = 'QM9/qm9.fcstd', partName = None, doc_assembly = assembly_file)

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()

# Place the DAQ on the ground
Gui.Selection.clearSelection()
Gui.Selection.addSelection(daq , "Face039")
Gui.Selection.addSelection(pqms, "Face039")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)


# Right offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(daq , "Face9")
Gui.Selection.addSelection(pqms, "Face5")

selection = Gui.Selection.getSelectionEx()
daq_pqms_side = planeConstraint.parseSelection(selection, objectToUpdate=None)
#daq_pqms_side.offset = -500 

# Front Offset
Gui.Selection.clearSelection()
Gui.Selection.addSelection(daq , "Face007")
Gui.Selection.addSelection(pqms, "Face007")

selection = Gui.Selection.getSelectionEx()
planeConstraint.parseSelection(selection, objectToUpdate=None)