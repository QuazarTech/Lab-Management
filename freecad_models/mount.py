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
FreeCAD.getDocument("mount").getObject("Cylinder").Height = 2*(total_core_height + length_margin + bend_radius + sheet_thickness)
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