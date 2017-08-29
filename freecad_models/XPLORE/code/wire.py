# Importing standard libraries
import math
import sys

# Insert this directory into the PYTHONPATH to import experimental parameters from experiment_params.py
sys.path.insert(0, "${HOME}/work/git/Lab-Management/freecad_models/EM_Coupling_Experiment/code")

# Importing FreeCAD libraries
from FreeCAD import Base
import Part,PartGui

# App and Gui are modules internal to FreeCAD:
# App's methods give you access to defining the properties of shapes
# Gui's methods can be used to change the way you want to represent the shape.

###############################################################################
# Create a new document for the CAD model

doc = App.newDocument('wire')
App.setActiveDocument(doc.Name)
App.ActiveDocument=App.getDocument(doc.Name)
Gui.ActiveDocument=Gui.getDocument(doc.Name)

###############################################################################

upper_wire_length = 100
lower_wire_length = 100
bend_length       = 40
wire_radius       = 2

###############################################################################
Gui.activateWorkbench("SketcherWorkbench")

upper_wire_spine = App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
upper_wire_spine.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))

upper_wire_spine.MapMode = "Deactivated"
Gui.activeDocument().setEdit(upper_wire_spine.Name)

upper_wire_spine.addGeometry(Part.LineSegment(App.Vector(-13.951353,81.584480,0),App.Vector(-13.697935,20.512848,0)),False)
upper_wire_spine.addConstraint(Sketcher.Constraint('Vertical',0)) 
upper_wire_spine.addConstraint(Sketcher.Constraint('DistanceY',0,1,0,2, upper_wire_length)) 

upper_wire_spine.addConstraint(Sketcher.Constraint('DistanceY',0,1,-1,1, -bend_length/2))
upper_wire_spine.addConstraint(Sketcher.Constraint('DistanceX',0,1,-1,1, bend_length/2))

Gui.getDocument(doc.Name).resetEdit()
App.ActiveDocument.recompute()

############################################################################### 
# Bend upper spine sketch 

bend_upper_spine = App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')

bend_upper_spine.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
bend_upper_spine.MapMode = "Deactivated"

Gui.activeDocument().setEdit('Sketch001')

bend_upper_spine.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(-6.630920,3.297301,0),App.Vector(0,0,1),7.405491),2.092624,5.821731),False)
bend_upper_spine.addConstraint(Sketcher.Constraint('Coincident',0,2,-1,1)) 

bend_upper_spine.addConstraint(Sketcher.Constraint('DistanceX',0,1,-1,1, bend_length/2)) 
bend_upper_spine.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,1, bend_length/2)) 
bend_upper_spine.addConstraint(Sketcher.Constraint('DistanceX',0,3,-1,1, 0))

Gui.getDocument(doc.Name).resetEdit()
App.getDocument(doc.Name).recompute()

################################################################################
# Add profile for wire at bend

wire_profile_bend = App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')

wire_profile_bend.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.500000,0.500000,0.500000,0.500000))
wire_profile_bend.MapMode = "Deactivated"

Gui.activeDocument().setEdit(wire_profile_bend.Name)

wire_profile_bend.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0),App.Vector(0,0,1),4.277175),False)

wire_profile_bend.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
wire_profile_bend.addConstraint(Sketcher.Constraint('Radius',0, wire_radius))

Gui.getDocument('wire').resetEdit()
App.getDocument('wire').recompute()
 
################################################################################
# Add profile for straight wire 
 
wire_profile = App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')

wire_profile.Placement = App.Placement(App.Vector(0.000000,bend_length/2,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))
wire_profile.MapMode = "Deactivated"

Gui.activeDocument().setEdit(wire_profile.Name)

wire_profile.addGeometry(Part.Circle(App.Vector(-5.565041,4.064911,0),App.Vector(0,0,1),1.546428),False)

wire_profile.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3, 0.00))
wire_profile.addConstraint(Sketcher.Constraint('DistanceX',0,3,-1,1, bend_length/2)) 
wire_profile.addConstraint(Sketcher.Constraint('Radius',0, wire_radius)) 

Gui.getDocument('wire').resetEdit()
App.getDocument('wire').recompute()


################################################################################
# Sweep for straight wire 
Gui.activateWorkbench("PartWorkbench")

straight_wire = App.getDocument('wire').addObject('Part::Sweep','Sweep')

straight_wire.Sections=[wire_profile, ]
straight_wire.Spine=(upper_wire_spine,[])

straight_wire.Solid=True
straight_wire.Frenet=True

################################################################################
# Sweep for bend wire 
bend_wire = App.getDocument('wire').addObject('Part::Sweep','Sweep')

bend_wire.Sections=[wire_profile_bend, ]
bend_wire.Spine=(bend_upper_spine,[])

bend_wire.Solid=True
bend_wire.Frenet=True

App.ActiveDocument.recompute()

################################################################################
# Temp Mirror 

mirror_bend_temp = doc.addObject("Part::Mirroring")

mirror_bend_temp.Source=bend_wire
mirror_bend_temp.Label=u"temp mirror bend "

mirror_bend_temp.Normal=(1,0,0)
mirror_bend_temp.Base=(0,0,0)

Gui.ActiveDocument.ActiveObject.ShapeColor=Gui.ActiveDocument.Sweep001.ShapeColor
Gui.ActiveDocument.ActiveObject.LineColor=Gui.ActiveDocument.Sweep001.LineColor
Gui.ActiveDocument.ActiveObject.PointColor=Gui.ActiveDocument.Sweep001.PointColor



mirror_straight_temp = doc.addObject("Part::Mirroring")

mirror_straight_temp.Source = straight_wire
mirror_straight_temp.Label=u"temp straight bend"

mirror_straight_temp.Normal=(1,0,0)
mirror_straight_temp.Base=(0,0,0)

Gui.ActiveDocument.ActiveObject.ShapeColor=Gui.ActiveDocument.Sweep.ShapeColor
Gui.ActiveDocument.ActiveObject.LineColor=Gui.ActiveDocument.Sweep.LineColor
Gui.ActiveDocument.ActiveObject.PointColor=Gui.ActiveDocument.Sweep.PointColor

################################################################################
# Mirror 

lower_wire_straight = doc.addObject("Part::Mirroring")

lower_wire_straight.Source = mirror_straight_temp
lower_wire_straight.Label=u"Lower wire straight"

lower_wire_straight.Normal=(0,1,0)
lower_wire_straight.Base=(0,0,0)

Gui.ActiveDocument.ActiveObject.ShapeColor=Gui.ActiveDocument.Part__Mirroring001.ShapeColor
Gui.ActiveDocument.ActiveObject.LineColor=Gui.ActiveDocument.Part__Mirroring001.LineColor
Gui.ActiveDocument.ActiveObject.PointColor=Gui.ActiveDocument.Part__Mirroring001.PointColor



lower_wire_bend = doc.addObject("Part::Mirroring")

lower_wire_bend.Source = mirror_bend_temp
lower_wire_bend.Label=u"lower wire bend"

lower_wire_bend.Normal=(0,1,0)
lower_wire_bend.Base=(0,0,0)

Gui.ActiveDocument.ActiveObject.ShapeColor=Gui.ActiveDocument.Part__Mirroring.ShapeColor
Gui.ActiveDocument.ActiveObject.LineColor=Gui.ActiveDocument.Part__Mirroring.LineColor
Gui.ActiveDocument.ActiveObject.PointColor=Gui.ActiveDocument.Part__Mirroring.PointColor

################################################################################
# Hide unnecessary stuff

Gui.getDocument("wire").getObject("Sketch").Visibility=False
Gui.getDocument("wire").getObject("Sketch001").Visibility=False
Gui.getDocument("wire").getObject("Sketch003").Visibility=False
Gui.getDocument("wire").getObject("Sketch002").Visibility=False

Gui.getDocument("wire").getObject("Part__Mirroring001").Visibility=False
Gui.getDocument("wire").getObject("Part__Mirroring").Visibility=False

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()
 