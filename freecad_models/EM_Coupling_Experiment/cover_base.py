############################################################################
# This script generates the bottom of the sheet metal cover in which the
# EM Coupling Experiment will be housed. It has holes is the side faces,
# on which the mounting rod (mount.fcstd) will be mount using screws.
# On the top flanges, the cover's top (cover_top.fcstd) will be mounted
# using 4 screws.
############################################################################


import sys
sys.path.insert(0, "${HOME}/.FreeCAD/Mod/SheetMetal")
import SheetMetalCmd

import sys
sys.path.insert(0, "${HOME}/Downloads/BNC\ conn/code")

from experiment_params import *

######################################
## Create a new empty document and set it to be the active document in Freecad

App.newDocument("cover_base")
App.setActiveDocument("cover_base")
App.ActiveDocument=App.getDocument("cover_base")
Gui.ActiveDocument=Gui.getDocument("cover_base")

######################################
##Base Flange

Gui.activateWorkbench("PartWorkbench")
box = App.ActiveDocument.addObject("Part::Box","Box")
box.Label = "Cube"

Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxometric()

box.Height = sheet_thickness
box.Length = base_length
box.Width  = base_width

App.ActiveDocument.recompute()

######################################
## Side walls

## Left Wall

Gui.SendMsgToActiveView("ViewFit")
Gui.activateWorkbench("SMWorkbench")

bend1 = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Bend")
bend1.Label = "Left Wall"

# What is referenced by Face1 here?
FreeCADGui.Selection.clearSelection()
FreeCADGui.Selection.addSelection(box, "Face1")

SheetMetalCmd.SMBendWall(bend1)
SheetMetalCmd.SMViewProviderTree(bend1.ViewObject)
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_base").getObject("Bend").radius = bend_radius
FreeCAD.getDocument("cover_base").getObject("Bend").length = wall_height
App.ActiveDocument.recompute()

######################################

## Right Wall

bend2 = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Bend001")
bend2.Label = "Right Wall"

# Again?
FreeCADGui.Selection.clearSelection()
FreeCADGui.Selection.addSelection(bend1, "Face14")

SheetMetalCmd.SMBendWall(bend2)
SheetMetalCmd.SMViewProviderTree(bend2.ViewObject)
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_base").getObject("Bend001").radius = bend_radius
FreeCAD.getDocument("cover_base").getObject("Bend001").length = wall_height
App.ActiveDocument.recompute()

######################################
##Top Flanges

## Left Flange

bend3 = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Bend002")
bend3.Label = "Top Left Flange"

FreeCADGui.Selection.clearSelection()
FreeCADGui.Selection.addSelection(bend2, "Face22")

SheetMetalCmd.SMBendWall(bend3)
SheetMetalCmd.SMViewProviderTree(bend3.ViewObject)
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_base").getObject("Bend002").radius = bend_radius
FreeCAD.getDocument("cover_base").getObject("Bend002").length = top_flange_width
App.ActiveDocument.recompute()

######################################

## Right Flange

bend4 = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Bend003")
bend4.Label = "Top Right Flange"

FreeCADGui.Selection.clearSelection()
FreeCADGui.Selection.addSelection(bend3, "Face30")

SheetMetalCmd.SMBendWall(bend4)
SheetMetalCmd.SMViewProviderTree(bend4.ViewObject)
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_base").getObject("Bend003").radius = bend_radius
FreeCAD.getDocument("cover_base").getObject("Bend003").length = top_flange_width
App.ActiveDocument.recompute()

######################################
## Holes for mounting support rod for cores

Gui.activateWorkbench("PartWorkbench")
App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
App.ActiveDocument.ActiveObject.Label = "Core Mount"

FreeCAD.getDocument("cover_base").getObject("Cylinder").Radius = screw_diameter/2
FreeCAD.getDocument("cover_base").getObject("Cylinder").Height = base_length + 2*(sheet_thickness+bend_radius)
FreeCAD.getDocument("cover_base").getObject("Cylinder").Placement = \
    App.Placement(App.Vector(-(sheet_thickness+bend_radius),base_width/2,wall_height/2),App.Rotation(App.Vector(0,1,0),90))

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Make Hole

App.activeDocument().addObject("Part::Cut","Cut")
App.activeDocument().Cut.Base = App.activeDocument().Bend003
App.activeDocument().Cut.Tool = App.activeDocument().Cylinder
Gui.activeDocument().Bend003.Visibility=False
Gui.activeDocument().Cylinder.Visibility=False
Gui.ActiveDocument.Cut.ShapeColor=Gui.ActiveDocument.Bend003.ShapeColor
Gui.ActiveDocument.Cut.DisplayMode=Gui.ActiveDocument.Bend003.DisplayMode
App.ActiveDocument.recompute()

######################################
## Holes on top to mount cover_top

App.ActiveDocument.addObject("Part::Cylinder","Cylinder001")
App.ActiveDocument.ActiveObject.Label = "Cover Top Mount"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_base").getObject("Cylinder001").Placement = \
    App.Placement(App.Vector(top_flange_width/2,base_width/4,wall_height+sheet_thickness+2*(bend_radius)),App.Rotation(App.Vector(0,0,1),0))

FreeCAD.getDocument("cover_base").getObject("Cylinder001").Radius = screw_diameter/2
FreeCAD.getDocument("cover_base").getObject("Cylinder001").Height = sheet_thickness

App.activeDocument().addObject("Part::Cut","Cut001")
App.activeDocument().Cut001.Base = App.activeDocument().Cut
App.activeDocument().Cut001.Tool = App.activeDocument().Cylinder001
Gui.activeDocument().Cut.Visibility=False
Gui.activeDocument().Cylinder001.Visibility=False
Gui.ActiveDocument.Cut001.ShapeColor=Gui.ActiveDocument.Cut.ShapeColor
Gui.ActiveDocument.Cut001.DisplayMode=Gui.ActiveDocument.Cut.DisplayMode
App.ActiveDocument.recompute()

######################################

App.ActiveDocument.addObject("Part::Cylinder","Cylinder002")
App.ActiveDocument.ActiveObject.Label = "Cover Top Mount"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_base").getObject("Cylinder002").Placement = \
    App.Placement(App.Vector(top_flange_width/2,3*base_width/4,wall_height+sheet_thickness+2*(bend_radius)),App.Rotation(App.Vector(0,0,1),0))

FreeCAD.getDocument("cover_base").getObject("Cylinder002").Radius = screw_diameter/2
FreeCAD.getDocument("cover_base").getObject("Cylinder002").Height = sheet_thickness

App.activeDocument().addObject("Part::Cut","Cut002")
App.activeDocument().Cut002.Base = App.activeDocument().Cut001
App.activeDocument().Cut002.Tool = App.activeDocument().Cylinder002
Gui.activeDocument().Cut001.Visibility=False
Gui.activeDocument().Cylinder002.Visibility=False
Gui.ActiveDocument.Cut002.ShapeColor=Gui.ActiveDocument.Cut001.ShapeColor
Gui.ActiveDocument.Cut002.DisplayMode=Gui.ActiveDocument.Cut001.DisplayMode
App.ActiveDocument.recompute()


######################################

App.ActiveDocument.addObject("Part::Cylinder","Cylinder003")
App.ActiveDocument.ActiveObject.Label = "Cover Top Mount"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_base").getObject("Cylinder003").Placement = \
    App.Placement(App.Vector(base_length-top_flange_width/2,base_width/4,wall_height+sheet_thickness+2*(bend_radius)),App.Rotation(App.Vector(0,0,1),0))

FreeCAD.getDocument("cover_base").getObject("Cylinder003").Radius = screw_diameter/2
FreeCAD.getDocument("cover_base").getObject("Cylinder003").Height = sheet_thickness

App.activeDocument().addObject("Part::Cut","Cut003")
App.activeDocument().Cut003.Base = App.activeDocument().Cut002
App.activeDocument().Cut003.Tool = App.activeDocument().Cylinder003
Gui.activeDocument().Cut002.Visibility=False
Gui.activeDocument().Cylinder003.Visibility=False
Gui.ActiveDocument.Cut003.ShapeColor=Gui.ActiveDocument.Cut002.ShapeColor
Gui.ActiveDocument.Cut003.DisplayMode=Gui.ActiveDocument.Cut002.DisplayMode
App.ActiveDocument.recompute()

######################################

App.ActiveDocument.addObject("Part::Cylinder","Cylinder004")
App.ActiveDocument.ActiveObject.Label = "Cover Top Mount"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_base").getObject("Cylinder004").Placement = \
    App.Placement(App.Vector(base_length-top_flange_width/2,3*base_width/4,wall_height+sheet_thickness+2*(bend_radius)),App.Rotation(App.Vector(0,0,1),0))

FreeCAD.getDocument("cover_base").getObject("Cylinder004").Radius = screw_diameter/2
FreeCAD.getDocument("cover_base").getObject("Cylinder004").Height = sheet_thickness

App.activeDocument().addObject("Part::Cut","Cut004")
App.activeDocument().Cut004.Base = App.activeDocument().Cut003
App.activeDocument().Cut004.Tool = App.activeDocument().Cylinder004
Gui.activeDocument().Cut003.Visibility=False
Gui.activeDocument().Cylinder004.Visibility=False
Gui.ActiveDocument.Cut004.ShapeColor=Gui.ActiveDocument.Cut003.ShapeColor
Gui.ActiveDocument.Cut004.DisplayMode=Gui.ActiveDocument.Cut003.DisplayMode
App.ActiveDocument.recompute()

########################################
## Create holes for Coaxial connector

Gui.activateWorkbench("SketcherWorkbench")
App.activeDocument().addObject('Sketcher::SketchObject','Sketch')

# What is MapMode and Support
App.activeDocument().Sketch.MapMode = "FlatFace"
App.activeDocument().Sketch.Support = [(App.getDocument('cover_base').Cut004,'Face15')]
App.activeDocument().recompute()
Gui.activeDocument().setEdit('Sketch')

#import Show.TempoVis

# Add base line
ActiveSketch = App.ActiveDocument.getObject('Sketch')

App.ActiveDocument.Sketch.addGeometry(Part.LineSegment(App.Vector(51.036247,57.121452,0),App.Vector(6.999034,57.816776,0)),False)

App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',0)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2,coax_side_distance)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,1,coax_side_distance+coax_base_width)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,2,coax_bottom_distance)) 

# Add Arc
App.ActiveDocument.Sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(7.922558,56.798874,0),App.Vector(0,0,1),4.818108),6.245304,3.288062),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',1,coax_radius)) 

App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,0,2)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,1)) 

Gui.getDocument('cover_base').resetEdit()
App.getDocument('cover_base').recompute()

# Extrude
Gui.activateWorkbench("PartWorkbench")
f = FreeCAD.getDocument('cover_base').addObject('Part::Extrusion', 'Extrude')
f = App.getDocument('cover_base').getObject('Extrude')
f.Base = App.getDocument('cover_base').getObject('Sketch')
f.DirMode = "Normal"
f.DirLink = None
f.LengthFwd = base_length + 2*bend_radius + 2*sheet_thickness
f.LengthRev = 0
f.Solid = True
f.Reversed = True
f.Symmetric = False
f.TaperAngle = 0.000000000000000
f.TaperAngleRev = 0.000000000000000
Gui.ActiveDocument.Extrude.ShapeColor=Gui.ActiveDocument.Sketch.ShapeColor
Gui.ActiveDocument.Extrude.LineColor=Gui.ActiveDocument.Sketch.LineColor
Gui.ActiveDocument.Extrude.PointColor=Gui.ActiveDocument.Sketch.PointColor
f.Base.ViewObject.hide()
App.ActiveDocument.recompute()

# Cut

App.activeDocument().addObject("Part::Cut","Cut005")
App.activeDocument().Cut005.Base = App.activeDocument().Cut004
App.activeDocument().Cut005.Tool = App.activeDocument().Extrude
Gui.activeDocument().Cut004.Visibility=False
Gui.activeDocument().Extrude.Visibility=False
Gui.ActiveDocument.Cut005.ShapeColor=Gui.ActiveDocument.Cut004.ShapeColor
Gui.ActiveDocument.Cut005.DisplayMode=Gui.ActiveDocument.Cut004.DisplayMode
App.ActiveDocument.recompute()
