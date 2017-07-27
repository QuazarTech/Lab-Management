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

FreeCAD.getDocument("cover_base").getObject("Cylinder").Radius = hole_diameter/2
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

######################################
#/////////////////Does not work in v0.17/////////////////////

## Holes on top to screw on cover_top


### Create a sketch for 2 screw holes (left)
#Gui.activateWorkbench("SketcherWorkbench")
#hole1_sketch = App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
#hole1_sketch.Support = (bend4,["Face37"])
#App.activeDocument().recompute()

#Gui.activeDocument().setEdit(hole1_sketch.Name)

#hole1_sketch.addGeometry(Part.Circle(App.Vector(4.604599,49.614052,0),App.Vector(0,0,1),1.991505))
#App.ActiveDocument.recompute()
#hole1_sketch.addGeometry(Part.Circle(App.Vector(4.200179,22.113937,0),App.Vector(0,0,1),3.139092))
#App.ActiveDocument.recompute()

#hole1_sketch.addConstraint(Sketcher.Constraint('DistanceX',0,3,1,3,0.00)) 
#App.ActiveDocument.recompute()

#hole1_sketch.addConstraint(Sketcher.Constraint('Equal',0,1)) 
#App.ActiveDocument.recompute()

#hole1_sketch.addConstraint(Sketcher.Constraint('Radius',0,hole_diameter/2)) 
#App.ActiveDocument.recompute()

#hole1_sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,1,3,top_flange_width/2)) 
#App.ActiveDocument.recompute()

#hole1_sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,1,3,base_width/4)) 
#App.ActiveDocument.recompute()

#hole1_sketch.addConstraint(Sketcher.Constraint('DistanceY',0,3,1,3,-base_width/2))
#App.ActiveDocument.recompute()

#Gui.getDocument('cover_base').resetEdit()
#App.getDocument('cover_base').recompute()

## Create 2 screw holes

#Gui.activateWorkbench("PartDesignWorkbench")
#hole1 = App.activeDocument().addObject("PartDesign::Pocket","Pocket")
#hole1.Sketch = hole1_sketch
#App.ActiveDocument.recompute()

#Gui.activeDocument().hide(hole1_sketch.Name)
#Gui.activeDocument().hide(bend4.Name)

#Gui.activeDocument().setEdit(hole1.Name)
#Gui.ActiveDocument.Pocket.ShapeColor=Gui.ActiveDocument.Bend003.ShapeColor
#Gui.ActiveDocument.Pocket.LineColor=Gui.ActiveDocument.Bend003.LineColor
#Gui.ActiveDocument.Pocket.PointColor=Gui.ActiveDocument.Bend003.PointColor

#hole1.Length = sheet_thickness
#hole1.UpToFace = None
#hole1.Type = 0

#App.ActiveDocument.recompute()
#Gui.activeDocument().resetEdit()

#######################################

### Create a sketch for 2 screw holes (right)
#Gui.activateWorkbench("SketcherWorkbench")
#hole2_sketch = App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
#hole2_sketch.Support = (hole1,["Face5"])
#App.activeDocument().recompute()

#Gui.activeDocument().setEdit(hole2_sketch.Name)

#hole2_sketch.addGeometry(Part.Circle(App.Vector(95.134468,50.632896,0),App.Vector(0,0,1),2.805983))
#hole2_sketch.addGeometry(Part.Circle(App.Vector(94.397575,21.894218,0),App.Vector(0,0,1),3.846672))

#hole2_sketch.addConstraint(Sketcher.Constraint('DistanceX',0,3,1,3,0.00))
#hole2_sketch.addConstraint(Sketcher.Constraint('Equal',1,0)) 
#hole2_sketch.addConstraint(Sketcher.Constraint('Radius',0,hole_diameter/2)) 
#hole2_sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,1,3,base_length-top_flange_width/2)) 
#App.ActiveDocument.recompute()

#App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',1,3,0,3,base_width/2))
#App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',-1,1,1,3,base_width/4)) 
#App.ActiveDocument.recompute()

#Gui.getDocument('cover_base').resetEdit()
#App.getDocument('cover_base').recompute()

## Create 2 screw holes

#Gui.activateWorkbench("PartDesignWorkbench")
#hole2 = App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
#hole2.Sketch = hole2_sketch
#App.ActiveDocument.recompute()

#Gui.activeDocument().hide(hole2_sketch.Name)
#Gui.activeDocument().hide(hole1.Name)

#Gui.activeDocument().setEdit(hole2.Name)
#Gui.ActiveDocument.Pocket001.ShapeColor=Gui.ActiveDocument.Pocket.ShapeColor
#Gui.ActiveDocument.Pocket001.LineColor=Gui.ActiveDocument.Pocket.LineColor
#Gui.ActiveDocument.Pocket001.PointColor=Gui.ActiveDocument.Pocket.PointColor

#hole2.Length = sheet_thickness
#hole2.Type = 0
#hole2.UpToFace = None

#App.ActiveDocument.recompute()
#Gui.activeDocument().resetEdit()

#######################################
### Create a sketch for hole to mount the coil core (right)

#Gui.activateWorkbench("SketcherWorkbench")
#side_hole_r_sketch = App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
#side_hole_r_sketch.Support = (hole2,["Face15"])
#App.activeDocument().recompute()

#Gui.activeDocument().setEdit(side_hole_r_sketch.Name)
#side_hole_r_sketch.addGeometry(Part.Circle(App.Vector(33.284668,41.694569,0),App.Vector(0,0,1),5.224906))
#App.ActiveDocument.recompute()

#side_hole_r_sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,base_width/2)) 
#App.ActiveDocument.recompute()

#side_hole_r_sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,wall_height/2)) 
#App.ActiveDocument.recompute()

#side_hole_r_sketch.addConstraint(Sketcher.Constraint('Radius',0,hole_diameter/2)) 
#App.ActiveDocument.recompute()

#######################################
#Gui.activateWorkbench("PartDesignWorkbench")
#side_hole_r = App.activeDocument().addObject("PartDesign::Pocket","Pocket002")
#side_hole_r.Sketch = side_hole_r_sketch
#App.ActiveDocument.recompute()

#Gui.activeDocument().hide(side_hole_r_sketch.Name)
#Gui.activeDocument().hide(hole2.Name)

#Gui.activeDocument().setEdit(side_hole_r.Name)
#Gui.ActiveDocument.Pocket002.ShapeColor=Gui.ActiveDocument.Pocket001.ShapeColor
#Gui.ActiveDocument.Pocket002.LineColor=Gui.ActiveDocument.Pocket001.LineColor
#Gui.ActiveDocument.Pocket002.PointColor=Gui.ActiveDocument.Pocket001.PointColor

#side_hole_r.Length = sheet_thickness
#side_hole_r.Type = 0
#side_hole_r.UpToFace = None

#App.ActiveDocument.recompute()
#Gui.activeDocument().resetEdit()

#######################################
### Create a sketch for hole to mount the coil core (left)

#Gui.activateWorkbench("SketcherWorkbench")
#side_hole_l_sketch = App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
#side_hole_l_sketch.Support = (side_hole_r,["Face32"])
#App.activeDocument().recompute()

#Gui.activeDocument().setEdit('Sketch003')
#side_hole_l_sketch.addGeometry(Part.Circle(App.Vector(-38.298714,37.472206,0),App.Vector(0,0,1),7.026811))
#App.ActiveDocument.recompute()

#side_hole_l_sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,-base_width/2)) 
#App.ActiveDocument.recompute()

#side_hole_l_sketch.addConstraint(Sketcher.Constraint('Radius',0,hole_diameter/2)) 
#App.ActiveDocument.recompute()

#side_hole_l_sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,wall_height/2)) 
#App.ActiveDocument.recompute()

#######################################
#Gui.activateWorkbench("PartDesignWorkbench")

#side_hole_l = App.activeDocument().addObject("PartDesign::Pocket","Pocket003")
#side_hole_l.Sketch = side_hole_l_sketch
#App.ActiveDocument.recompute()

#Gui.activeDocument().hide(side_hole_l_sketch.Name)
#Gui.activeDocument().hide(side_hole_r.Name)
#Gui.activeDocument().setEdit(side_hole_l.Name)

#Gui.ActiveDocument.Pocket003.ShapeColor=Gui.ActiveDocument.Pocket002.ShapeColor
#Gui.ActiveDocument.Pocket003.LineColor=Gui.ActiveDocument.Pocket002.LineColor
#Gui.ActiveDocument.Pocket003.PointColor=Gui.ActiveDocument.Pocket002.PointColor


#side_hole_l.Length = sheet_thickness
#side_hole_l.Type = 0
#side_hole_l.UpToFace = None

#App.ActiveDocument.recompute()
#Gui.activeDocument().resetEdit()

#/////////////////Does not work in v0.17/////////////////////

