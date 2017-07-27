import sys
sys.path.insert(0, "${HOME}/.FreeCAD/Mod/SheetMetal")
import SheetMetalCmd

import sys
sys.path.insert(0, "${HOME}/Downloads/BNC\ conn/code")

from experiment_params import *

######################################
## Create a new empty document and set it to be the active document in Freecad

App.newDocument("cover_top")
App.setActiveDocument("cover_top")
App.ActiveDocument=App.getDocument("cover_top")
Gui.ActiveDocument=Gui.getDocument("cover_top")

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
## Front and Back walls

## Front Wall

Gui.SendMsgToActiveView("ViewFit")
Gui.activateWorkbench("SMWorkbench")

bend1 = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Bend")
bend1.Label = "Front Wall"

FreeCADGui.Selection.clearSelection()
FreeCADGui.Selection.addSelection(box, "Face3")

SheetMetalCmd.SMBendWall(bend1)
SheetMetalCmd.SMViewProviderTree(bend1.ViewObject)
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_top").getObject("Bend").invert = True
FreeCAD.getDocument("cover_top").getObject("Bend").length = wall_height + sheet_thickness
App.ActiveDocument.recompute()


## Back Wall

Gui.SendMsgToActiveView("ViewFit")
Gui.activateWorkbench("SMWorkbench")

bend2 = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Bend001")
bend2.Label = "Back Wall"

FreeCADGui.Selection.clearSelection()
FreeCADGui.Selection.addSelection(bend1, "Face14")

SheetMetalCmd.SMBendWall(bend2)
SheetMetalCmd.SMViewProviderTree(bend2.ViewObject)
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_top").getObject("Bend001").invert = True
FreeCAD.getDocument("cover_top").getObject("Bend001").length = wall_height + sheet_thickness
App.ActiveDocument.recompute()

######################################

## Holes to Mount cover_bottom with screws

App.ActiveDocument.addObject("Part::Cylinder","Cylinder001")
App.ActiveDocument.ActiveObject.Label = "Cover Bottom Mount"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_top").getObject("Cylinder001").Placement = \
    App.Placement(App.Vector(top_flange_width/2,base_width/4,0),App.Rotation(App.Vector(0,0,1),0))

FreeCAD.getDocument("cover_top").getObject("Cylinder001").Radius = screw_diameter/2
FreeCAD.getDocument("cover_top").getObject("Cylinder001").Height = sheet_thickness

App.activeDocument().addObject("Part::Cut","Cut001")
App.activeDocument().Cut001.Base = App.activeDocument().Bend001
App.activeDocument().Cut001.Tool = App.activeDocument().Cylinder001
Gui.activeDocument().Bend001.Visibility=False
Gui.activeDocument().Cylinder001.Visibility=False
Gui.ActiveDocument.Cut001.ShapeColor=Gui.ActiveDocument.Bend001.ShapeColor
Gui.ActiveDocument.Cut001.DisplayMode=Gui.ActiveDocument.Bend001.DisplayMode
App.ActiveDocument.recompute()

######################################

App.ActiveDocument.addObject("Part::Cylinder","Cylinder002")
App.ActiveDocument.ActiveObject.Label = "Cover Bottom Mount"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_top").getObject("Cylinder002").Placement = \
    App.Placement(App.Vector(top_flange_width/2,3*base_width/4,0),App.Rotation(App.Vector(0,0,1),0))

FreeCAD.getDocument("cover_top").getObject("Cylinder002").Radius = screw_diameter/2
FreeCAD.getDocument("cover_top").getObject("Cylinder002").Height = sheet_thickness

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
App.ActiveDocument.ActiveObject.Label = "Cover Bottom Mount"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_top").getObject("Cylinder003").Placement = \
    App.Placement(App.Vector(base_length-top_flange_width/2,base_width/4,0),App.Rotation(App.Vector(0,0,1),0))

FreeCAD.getDocument("cover_top").getObject("Cylinder003").Radius = screw_diameter/2
FreeCAD.getDocument("cover_top").getObject("Cylinder003").Height = sheet_thickness

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
App.ActiveDocument.ActiveObject.Label = "Cover Bottom Mount"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("cover_top").getObject("Cylinder004").Placement = \
    App.Placement(App.Vector(base_length-top_flange_width/2,3*base_width/4,0),App.Rotation(App.Vector(0,0,1),0))

FreeCAD.getDocument("cover_top").getObject("Cylinder004").Radius = screw_diameter/2
FreeCAD.getDocument("cover_top").getObject("Cylinder004").Height = sheet_thickness

App.activeDocument().addObject("Part::Cut","Cut004")
App.activeDocument().Cut004.Base = App.activeDocument().Cut003
App.activeDocument().Cut004.Tool = App.activeDocument().Cylinder004
Gui.activeDocument().Cut003.Visibility=False
Gui.activeDocument().Cylinder004.Visibility=False
Gui.ActiveDocument.Cut004.ShapeColor=Gui.ActiveDocument.Cut003.ShapeColor
Gui.ActiveDocument.Cut004.DisplayMode=Gui.ActiveDocument.Cut003.DisplayMode
App.ActiveDocument.recompute()

# Make Transparent
FreeCADGui.getDocument("cover_top").getObject("Cut004").Transparency = 80
######################################
#/////////////////Does not work in v0.17/////////////////////

## Holes for mounting onto cover_top using screws

#Gui.activateWorkbench("SketcherWorkbench")
#hole_sketch = App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
#hole_sketch.Support = (App.ActiveDocument.Bend001,["Face12"])
#App.activeDocument().recompute()

#Gui.activeDocument().setEdit(hole_sketch.Name)

#App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(8.998930,58.524132,0),App.Vector(0,0,1),4.869736))
#App.ActiveDocument.recompute()
#App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(10.538872,14.250669,0),App.Vector(0,0,1),5.236382))
#App.ActiveDocument.recompute()
#App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(87.536179,59.294102,0),App.Vector(0,0,1),5.019615))
#App.ActiveDocument.recompute()
#App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(89.846107,17.330564,0),App.Vector(0,0,1),5.019611))
#App.ActiveDocument.recompute()

## Radii of all holes set equal
#App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',0,2)) 
#App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',2,3)) 
#App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',3,1)) 
#App.ActiveDocument.recompute()


#App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',2,screw_diameter/2)) 
#App.ActiveDocument.recompute()

#App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',0,3,1,3,0.00)) 
#App.ActiveDocument.recompute()

#App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',1,3,3,3,0.00)) 
#App.ActiveDocument.recompute()

#App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',2,3,0,3,0.00)) 
#App.ActiveDocument.recompute()

#App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',2,3,3,3,0.00)) 
#App.ActiveDocument.recompute()

#App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,1,3,top_flange_width/2)) 
#App.ActiveDocument.recompute()

#App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,1,3,base_width/4)) 
#App.ActiveDocument.recompute()

#App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',1,3,3,3,base_length-top_flange_width)) 
#App.ActiveDocument.recompute()

#App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',0,3,1,3,-base_width/2)) 
#App.ActiveDocument.recompute()

#Gui.getDocument('cover_top').resetEdit()
#App.getDocument('cover_top').recompute()

### Create Holes for screws
#Gui.activateWorkbench("PartDesignWorkbench")
#holes = App.activeDocument().addObject("PartDesign::Pocket","Pocket")
#App.activeDocument().Pocket.Sketch = hole_sketch
#App.activeDocument().Pocket.Length = sheet_thickness
#App.ActiveDocument.recompute()

#Gui.activeDocument().hide(hole_sketch.Name)
#Gui.activeDocument().hide(bend2.Name)

#Gui.activeDocument().setEdit(holes.Name)
#Gui.ActiveDocument.Pocket.ShapeColor=Gui.ActiveDocument.Bend001.ShapeColor
#Gui.ActiveDocument.Pocket.LineColor=Gui.ActiveDocument.Bend001.LineColor
#Gui.ActiveDocument.Pocket.PointColor=Gui.ActiveDocument.Bend001.PointColor
#App.ActiveDocument.Pocket.Type = 0
#App.ActiveDocument.Pocket.UpToFace = None
#App.ActiveDocument.recompute()
#Gui.activeDocument().resetEdit()

#Gui.activeDocument().activeView().viewAxometric()
#FreeCADGui.getDocument("cover_top").getObject(holes.Name).Transparency = 80
