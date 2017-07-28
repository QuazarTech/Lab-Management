import math

from FreeCAD import Base
import Part,PartGui

import sys
sys.path.insert(0, "${HOME}/Downloads/BNC\ conn/code")

from experiment_params import *

App.newDocument("mount")
App.setActiveDocument("mount")
App.ActiveDocument=App.getDocument("mount")
Gui.ActiveDocument=Gui.getDocument("mount")

#################################################

Gui.activeDocument().activeView().viewAxometric()


App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
App.ActiveDocument.ActiveObject.Label = "Cylinder"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

FreeCAD.getDocument("mount").getObject("Cylinder").Radius = hole_diameter/2
FreeCAD.getDocument("mount").getObject("Cylinder").Height = 2*(total_core_height + length_margin + bend_radius)
FreeCAD.getDocument("mount").getObject("Cylinder").Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))

Gui.SendMsgToActiveView("ViewFit")
App.ActiveDocument.recompute()

##################################################

## Make threads

# Create Helix that serves as the spine for the threads

App.ActiveDocument.addObject("Part::Helix","Helix")
App.ActiveDocument.Helix.Pitch=thread_pitch
App.ActiveDocument.Helix.Height=2*(total_core_height + length_margin - chamfer_length)
App.ActiveDocument.Helix.Radius=hole_diameter/2
App.ActiveDocument.Helix.Angle=0.00
App.ActiveDocument.Helix.LocalCoord=0
App.ActiveDocument.Helix.Style=1
App.ActiveDocument.Helix.Placement=Base.Placement(Base.Vector(0.00,0.00,chamfer_length+sheet_thickness+bend_radius),Base.Rotation(0.00,0.00,0.00,1.00))
App.ActiveDocument.Helix.Label='Helix'

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Create a Sketch to sweep Helix

Gui.activateWorkbench("SketcherWorkbench")
App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))
App.activeDocument().Sketch.MapMode = "Deactivated"

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

App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2,hole_diameter/2 + 0.1)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,1,2,hole_diameter/2 - 0.25))
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,1,2,chamfer_length+sheet_thickness+bend_radius)) 
Gui.getDocument("mount").resetEdit()

App.getDocument("mount").recompute()

#Sweep Helix to form solid thread

Gui.activateWorkbench("PartWorkbench")

App.getDocument("mount").addObject('Part::Sweep','Sweep')
App.getDocument("mount").ActiveObject.Sections=[App.getDocument("mount").Sketch, ]
App.getDocument("mount").ActiveObject.Spine=(App.ActiveDocument.Helix,[])
App.getDocument("mount").ActiveObject.Solid=True
App.getDocument("mount").ActiveObject.Frenet=True

Gui.getDocument("mount").getObject("Helix").Visibility=False
Gui.getDocument("mount").getObject("Sketch").Visibility=False
App.ActiveDocument.recompute()

# Cut the threads

App.activeDocument().addObject("Part::Cut","Cut")
App.activeDocument().Cut.Base = App.activeDocument().Cylinder
App.activeDocument().Cut.Tool = App.activeDocument().Sweep
Gui.activeDocument().Cylinder.Visibility=False
Gui.activeDocument().Sweep.Visibility=False
Gui.ActiveDocument.Cut.ShapeColor=Gui.ActiveDocument.Cylinder.ShapeColor
Gui.ActiveDocument.Cut.DisplayMode=Gui.ActiveDocument.Cylinder.DisplayMode
App.ActiveDocument.recompute()


################################################
## Side Holes to mount the rod onto the cover

# Sketch for hole
App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
App.activeDocument().Sketch001.MapMode = "FlatFace"
App.activeDocument().Sketch001.Support = [(App.getDocument('mount').Cut,'Face329')]
App.activeDocument().recompute()
Gui.activeDocument().setEdit('Sketch001')
ActiveSketch = App.ActiveDocument.getObject('Sketch001')

App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(-0.834407,-0.768209,0),App.Vector(0,0,1),0.758518),False)
App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',0,screw_diameter/2)) 

Gui.getDocument('mount').resetEdit()
App.getDocument('mount').recompute()

# Extrude Sketch
Gui.activateWorkbench("PartWorkbench")
f = FreeCAD.getDocument('mount').addObject('Part::Extrusion', 'Extrude')
f = App.getDocument('mount').getObject('Extrude')
f.Base = App.getDocument('mount').getObject('Sketch001')
f.DirMode = "Normal"
f.DirLink = None
f.LengthFwd = screw_length
f.LengthRev = 0.000000000000000
f.Solid = True
f.Reversed = True
f.Symmetric = False
f.TaperAngle = 0.000000000000000
f.TaperAngleRev = 0.000000000000000
Gui.ActiveDocument.Extrude.ShapeColor=Gui.ActiveDocument.Sketch001.ShapeColor
Gui.ActiveDocument.Extrude.LineColor=Gui.ActiveDocument.Sketch001.LineColor
Gui.ActiveDocument.Extrude.PointColor=Gui.ActiveDocument.Sketch001.PointColor
f.Base.ViewObject.hide()
App.ActiveDocument.recompute()

# Cut the hole
Gui.getDocument("mount").getObject("Cut").Visibility=False
Gui.getDocument("mount").getObject("Cut").Visibility=True
App.activeDocument().addObject("Part::Cut","Cut001")
App.activeDocument().Cut001.Base = App.activeDocument().Cut
App.activeDocument().Cut001.Tool = App.activeDocument().Extrude
Gui.activeDocument().Cut.Visibility=False
Gui.activeDocument().Extrude.Visibility=False
Gui.ActiveDocument.Cut001.ShapeColor=Gui.ActiveDocument.Cut.ShapeColor
Gui.ActiveDocument.Cut001.DisplayMode=Gui.ActiveDocument.Cut.DisplayMode
App.ActiveDocument.recompute()

# Sketch for hole 2
Gui.activateWorkbench("SketcherWorkbench")
App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
App.activeDocument().Sketch002.MapMode = "FlatFace"
App.activeDocument().Sketch002.Support = [(App.getDocument('mount').Cut001,'Face5')]
App.activeDocument().recompute()
Gui.activeDocument().setEdit('Sketch002')
ActiveSketch = App.ActiveDocument.getObject('Sketch002')

App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(1.084989,-1.715090,0),App.Vector(0,0,1),0.740006),False)
App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',0,screw_diameter/2))
Gui.getDocument('mount').resetEdit()
App.getDocument('mount').recompute()

#Extrude
Gui.activateWorkbench("PartWorkbench")
f = FreeCAD.getDocument('mount').addObject('Part::Extrusion', 'Extrude001')
f = App.getDocument('mount').getObject('Extrude001')
f.Base = App.getDocument('mount').getObject('Sketch002')
f.DirMode = "Normal"
f.DirLink = None
f.LengthFwd = screw_length
f.LengthRev = 0.000000000000000
f.Solid = True
f.Reversed = True
f.Symmetric = False
f.TaperAngle = 0.000000000000000
f.TaperAngleRev = 0.000000000000000
Gui.ActiveDocument.Extrude001.ShapeColor=Gui.ActiveDocument.Sketch002.ShapeColor
Gui.ActiveDocument.Extrude001.LineColor=Gui.ActiveDocument.Sketch002.LineColor
Gui.ActiveDocument.Extrude001.PointColor=Gui.ActiveDocument.Sketch002.PointColor
f.Base.ViewObject.hide()
App.ActiveDocument.recompute()

#Cut
App.activeDocument().addObject("Part::Cut","Cut002")
App.activeDocument().Cut002.Base = App.activeDocument().Cut001
App.activeDocument().Cut002.Tool = App.activeDocument().Extrude001
Gui.activeDocument().Cut001.Visibility=False
Gui.activeDocument().Extrude001.Visibility=False
Gui.ActiveDocument.Cut002.ShapeColor=Gui.ActiveDocument.Cut001.ShapeColor
Gui.ActiveDocument.Cut002.DisplayMode=Gui.ActiveDocument.Cut001.DisplayMode
App.ActiveDocument.recompute()
