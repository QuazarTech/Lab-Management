#####################################################################
# This script generates a cylindrical core, that fits on the coil
# winding machine at Quazar Tech. It has threads inside, so that it 
# can be mounted on a threaded bolt (mount.fcstd). Rotating the core
# when it is mounted on the threaded bolt will cause translation.

# A coil will be wound on this core.
#####################################################################


import math

from FreeCAD import Base
import Part,PartGui

import sys
sys.path.insert(0, "${HOME}/Downloads/susceptibility_experiment/code")

from experiment_params import *

App.newDocument("core")
App.setActiveDocument("core")
App.ActiveDocument=App.getDocument("core")
Gui.ActiveDocument=Gui.getDocument("core")

Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxometric()

#######################
#Cylinder 1
App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
App.ActiveDocument.ActiveObject.Label = "Cylinder"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("core").getObject("Cylinder").Radius = core_radius
FreeCAD.getDocument("core").getObject("Cylinder").Height = core_height

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("core").getObject("Cylinder").Placement = App.Placement(App.Vector(0,0,base_height),App.Rotation(App.Vector(0,0,1),0))

#######################
#Cylinder 2 - Base
App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
App.ActiveDocument.ActiveObject.Label = "Cylinder"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("core").getObject("Cylinder001").Radius = core_radius + coil_thickness
FreeCAD.getDocument("core").getObject("Cylinder001").Height = base_height

FreeCAD.getDocument("core").getObject("Cylinder001").Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

#######################
# Cylinder 3
App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
App.ActiveDocument.ActiveObject.Label = "Cylinder"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("core").getObject("Cylinder002").Radius = core_radius + coil_thickness
FreeCAD.getDocument("core").getObject("Cylinder002").Height = top_height

FreeCAD.getDocument("core").getObject("Cylinder002").Placement = App.Placement(App.Vector(0,0,base_height + core_height),App.Rotation(App.Vector(0,0,1),0))

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

#################################
## Fuse all subparts into one

App.activeDocument().addObject("Part::MultiFuse","Fusion")
App.activeDocument().Fusion.Shapes = [App.activeDocument().Cylinder,App.activeDocument().Cylinder002,App.activeDocument().Cylinder001,]
#Gui.activeDocument().Cylinder004.Visibility=False
#Gui.activeDocument().Cylinder003.Visibility=False
Gui.activeDocument().Cylinder.Visibility=False
Gui.activeDocument().Cylinder002.Visibility=False
Gui.activeDocument().Cylinder001.Visibility=False
Gui.ActiveDocument.Fusion.ShapeColor=Gui.ActiveDocument.Cylinder002.ShapeColor
Gui.ActiveDocument.Fusion.DisplayMode=Gui.ActiveDocument.Cylinder002.DisplayMode
App.ActiveDocument.recompute()

##############################################################

Gui.activateWorkbench("PartWorkbench")

App.ActiveDocument.addObject("Part::Box","Box")
App.ActiveDocument.ActiveObject.Label = "Cube"

FreeCAD.getDocument("core").getObject("Box").Length = core_radius + coil_thickness
FreeCAD.getDocument("core").getObject("Box").Width = 2*(core_radius + coil_thickness)
FreeCAD.getDocument("core").getObject("Box").Height = base_cut

FreeCAD.getDocument("core").getObject("Box").Placement = \
    App.Placement(App.Vector((core_radius+coil_thickness)/2+chamfer_length,-(core_radius+coil_thickness),0),App.Rotation(App.Vector(0,0,1),0))

#cut the part

App.activeDocument().addObject("Part::Cut","Cut")
App.activeDocument().Cut.Base = App.activeDocument().Fusion
App.activeDocument().Cut.Tool = App.activeDocument().Box
Gui.activeDocument().hide("Fusion")
Gui.activeDocument().hide("Box")
Gui.ActiveDocument.Cut.ShapeColor=Gui.ActiveDocument.Fusion.ShapeColor
Gui.ActiveDocument.Cut.DisplayMode=Gui.ActiveDocument.Fusion.DisplayMode

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")


###############################################################

App.ActiveDocument.addObject("Part::Box","Box")
App.ActiveDocument.ActiveObject.Label = "Cube"

FreeCAD.getDocument("core").getObject("Box001").Length = core_radius + coil_thickness
FreeCAD.getDocument("core").getObject("Box001").Width = 2*(core_radius + coil_thickness)
FreeCAD.getDocument("core").getObject("Box001").Height = base_cut

FreeCAD.getDocument("core").getObject("Box001").Placement = \
    App.Placement(App.Vector(-3*(core_radius+coil_thickness)/2-chamfer_length,-(core_radius+coil_thickness),0),App.Rotation(App.Vector(0,0,1),0))

App.activeDocument().addObject("Part::Cut","Cut001")
App.activeDocument().Cut001.Base = App.activeDocument().Cut
App.activeDocument().Cut001.Tool = App.activeDocument().Box001
Gui.activeDocument().Cut.Visibility=False
Gui.activeDocument().Box001.Visibility=False
Gui.ActiveDocument.Cut001.ShapeColor=Gui.ActiveDocument.Cut.ShapeColor
Gui.ActiveDocument.Cut001.DisplayMode=Gui.ActiveDocument.Cut.DisplayMode
App.ActiveDocument.recompute()

# Make hole through which core will recieve support when mounted into the cover_base

#########################

App.ActiveDocument.addObject("Part::Cylinder","Cylinder003")
App.ActiveDocument.ActiveObject.Label = "Hole Left"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("core").getObject("Cylinder003").Radius = hole_diameter/2
FreeCAD.getDocument("core").getObject("Cylinder003").Height = total_core_height
FreeCAD.getDocument("core").getObject("Cylinder003").Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))

App.activeDocument().addObject("Part::Cut","Cut002")
App.activeDocument().Cut002.Base = App.activeDocument().Cut001
App.activeDocument().Cut002.Tool = App.activeDocument().Cylinder003
Gui.activeDocument().Cut001.Visibility=False
Gui.activeDocument().Cylinder003.Visibility=False
Gui.ActiveDocument.Cut002.ShapeColor=Gui.ActiveDocument.Cut001.ShapeColor
Gui.ActiveDocument.Cut002.DisplayMode=Gui.ActiveDocument.Cut001.DisplayMode
App.ActiveDocument.recompute()


##########################################################################
## Make Threads in the hole

# Add a helix to form the base spine

Gui.activateWorkbench("PartWorkbench")

App.ActiveDocument.addObject("Part::Helix","Helix")
App.ActiveDocument.Helix.Pitch =thread_pitch
App.ActiveDocument.Helix.Height=total_core_height-2*chamfer_length
App.ActiveDocument.Helix.Radius=hole_diameter/2
App.ActiveDocument.Helix.Angle=0.00
App.ActiveDocument.Helix.LocalCoord=0
App.ActiveDocument.Helix.Style=1
App.ActiveDocument.Helix.Placement=Base.Placement(Base.Vector(0.00,0.00,chamfer_length),Base.Rotation(0.00,0.00,0.00,1.00))
App.ActiveDocument.Helix.Label='Helix'
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Add a sketch to sweep the helix with

Gui.activateWorkbench("SketcherWorkbench")
App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))
#App.activeDocument().Sketch.MapMode = "Deactivated"

Gui.activeDocument().setEdit('Sketch')

App.ActiveDocument.Sketch.addGeometry(Part.LineSegment(App.Vector(3.669230,4.655583,0),App.Vector(3.787592,3.037965,0)),False)
App.ActiveDocument.Sketch.addGeometry(Part.LineSegment(App.Vector(3.787592,3.037966,0),App.Vector(5.799752,3.984863,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,2)) 
App.ActiveDocument.Sketch.addGeometry(Part.LineSegment(App.Vector(3.748140,4.537220,0),App.Vector(5.799752,3.984864,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,0,1)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,1,2)) 

App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',0)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',2,1)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Angle',2,2,1,2,1.0472)) # 60 degrees  

App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2,hole_diameter/2 - 0.1)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,1,2,hole_diameter/2 + 0.25))
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,1,2,chamfer_length+base_height)) 
Gui.getDocument("core").resetEdit()

App.getDocument("core").recompute()

#Sweep Helix to form solid thread

Gui.activateWorkbench("PartWorkbench")
from FreeCAD import Base
import Part
App.getDocument("core").addObject('Part::Sweep','Sweep')
App.getDocument("core").ActiveObject.Sections=[App.getDocument("core").Sketch, ]
App.getDocument("core").ActiveObject.Spine=(App.ActiveDocument.Helix,[])
App.getDocument("core").ActiveObject.Solid=True
App.getDocument("core").ActiveObject.Frenet=True

Gui.getDocument("core").getObject("Helix").Visibility=False
Gui.getDocument("core").getObject("Sketch").Visibility=False
App.ActiveDocument.recompute()

# Cut the Thread into the cylinder

App.activeDocument().addObject("Part::Cut","Cut003")
App.activeDocument().Cut003.Base = App.activeDocument().Cut002
App.activeDocument().Cut003.Tool = App.activeDocument().Sweep
Gui.activeDocument().Cut002.Visibility=False
Gui.activeDocument().Sweep.Visibility=False
Gui.ActiveDocument.Cut003.ShapeColor=Gui.ActiveDocument.Cut002.ShapeColor
Gui.ActiveDocument.Cut003.DisplayMode=Gui.ActiveDocument.Cut002.DisplayMode
App.ActiveDocument.recompute()


##############################################################

## Chamfer the holes in the cylinder

## Code Not working - (Need to Chamfer Manually through GUI)

chamfer = FreeCAD.ActiveDocument.addObject("Part::Chamfer","Chamfer")
chamfer.Base = FreeCAD.ActiveDocument.Cut003
__fillets__ = []
__fillets__.append((15,chamfer_length-0.5,chamfer_length-0.5)) #left
__fillets__.append((46,chamfer_length-0.5,chamfer_length-0.5)) #right
chamfer.Edges = __fillets__
del __fillets__
FreeCADGui.ActiveDocument.Cut003.Visibility = False

Gui.ActiveDocument.Chamfer.LineColor=Gui.ActiveDocument.Cut003.LineColor
Gui.ActiveDocument.Chamfer.PointColor=Gui.ActiveDocument.Cut003.PointColor
Gui.activeDocument().resetEdit()

FreeCAD.getDocument("core").getObject("Chamfer").Placement = App.Placement(App.Vector(-1,0,0),App.Rotation(App.Vector(0,0,1),0))
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")