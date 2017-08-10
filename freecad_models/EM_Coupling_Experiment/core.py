#####################################################################
# This script generates a cylindrical core, that fits on the coil
# winding machine at Quazar Tech. It has threads inside, so that it 
# can be mounted on a threaded bolt (mount.fcstd). Rotating the core
# when it is mounted on the threaded bolt will cause translation.

# A coil will be wound on this core.
#####################################################################

# What is the need to import math
import math

from FreeCAD import Base

# Why is PartGui needed?
import Part,PartGui

import sys
# Why insert this directory into the PYTHONPATH?
sys.path.insert(0, "${HOME}/Downloads/susceptibility_experiment/code")

from experiment_params import *

# App and Gui are modules internal to FreeCAD:
# App's methods give you access to defining the properties of shapes
# Gui's methods can be used to change the way you want to represent the shape.

App.newDocument("core")
App.setActiveDocument("core")
App.ActiveDocument=App.getDocument("core")
Gui.ActiveDocument=Gui.getDocument("core")

# Tells the GUI to fit the object inside the screen
Gui.SendMsgToActiveView("ViewFit")

# Sets the view to axonometric
# What specifically? - Dimetric, Trimetric, Isometric
Gui.activeDocument().activeView().viewAxometric()

#######################
# Steps to create Cylinder 1
# Initializing the cylinder using the primitive object defined in FreeCAD
App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
App.ActiveDocument.ActiveObject.Label = "Cylinder"

# Could you explain the purpose of the label since the declared object
# is later referenced by Cylinder, Cylinder001 and not the assigned label

# Recomputes the document - and updates all properties that have been changed 
# inside the document.
App.ActiveDocument.recompute()
# Tells the GUI to fit the object inside the screen
Gui.SendMsgToActiveView("ViewFit")

# Assigning the properties of the object as the user declares in params
FreeCAD.getDocument("core").getObject("Cylinder").Radius = core_radius
FreeCAD.getDocument("core").getObject("Cylinder").Height = core_height

# Recomputing and fitting:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Placement property consists of 3 things
# The position of the base (vector)
# The axis about which the object is to be rotated 
# In the above code it is the z axis (0, 0, 1) because x and y are 0, and z is 1
# Rotation Angle - This rotates the object by the specified angle along the axis 
# specified above (Below the angle is 0 : final argument of App.Placement()).

# What does the position vector here point to?
# For a sphere is it the center? Cylinder base or center? 
# Box is it one of the faces or center

FreeCAD.getDocument("core").getObject("Cylinder").Placement = \
App.Placement(App.Vector(0,0,base_height),App.Rotation(App.Vector(0,0,1),0))

#######################
# Steps to create Cylinder 2 - Base:
# Adding primitive object:
App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
App.ActiveDocument.ActiveObject.Label = "Cylinder"

# Recomputing and fitting:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Setting the parameters of the object as needed by the user:
# Where is Cylinder001 coming from?
FreeCAD.getDocument("core").getObject("Cylinder001").Radius = core_radius + coil_thickness
FreeCAD.getDocument("core").getObject("Cylinder001").Height = base_height

# Since this cylinder is the base, we set its position vector to (0, 0, 0):
FreeCAD.getDocument("core").getObject("Cylinder001").Placement = \
App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))

# Recomputing and fitting:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

#######################
# Steps to create Cylinder 3

# Adding primitive object:
App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
App.ActiveDocument.ActiveObject.Label = "Cylinder"

# Recomputing and fitting:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Setting the parameters of the object as needed by the user:
# Again, where is Cylinder002 coming from?
# Can't understand what is naming convention carried throughout
FreeCAD.getDocument("core").getObject("Cylinder002").Radius = core_radius + coil_thickness
FreeCAD.getDocument("core").getObject("Cylinder002").Height = top_height

# This cylinder comes above Cylinders 1 and 2: 
FreeCAD.getDocument("core").getObject("Cylinder002").Placement = \
App.Placement(App.Vector(0,0,base_height + core_height),App.Rotation(App.Vector(0,0,1),0))

# Recomputing and fitting:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

#################################
## Fuse all subparts into one

# Fusion will create a new object which is a union of the above defined cylinders:
# The name of this newly created object is fusion:
App.activeDocument().addObject("Part::MultiFuse","Fusion")
App.activeDocument().Fusion.Shapes = \
[App.activeDocument().Cylinder,App.activeDocument().Cylinder002,App.activeDocument().Cylinder001,]

# After creating the new object, we toggle the visibility of the parts
# that compose the object to false:
Gui.activeDocument().Cylinder.Visibility=False
Gui.activeDocument().Cylinder002.Visibility=False
Gui.activeDocument().Cylinder001.Visibility=False

# What is the need for these lines?:
# There has been no declaration of the ShapeColor and DisplayMode for Cylinder2
# Why is the declaration needed for the Fusion object?
# Won't it just use default ShapeColor and DisplayMode?
Gui.ActiveDocument.Fusion.ShapeColor=Gui.ActiveDocument.Cylinder002.ShapeColor
Gui.ActiveDocument.Fusion.DisplayMode=Gui.ActiveDocument.Cylinder002.DisplayMode
App.ActiveDocument.recompute()

##############################################################
# Workbenches contain all the functionality in FreeCAD. 
# Depending on what you want to do, you need to use a different workbench
# Here, to create a Part::Box, we need the part workbench.
Gui.activateWorkbench("PartWorkbench")

# Adding the box primitive object:
App.ActiveDocument.addObject("Part::Box","Box")
App.ActiveDocument.ActiveObject.Label = "Cube"

# Setting the parameters of the object as needed by the user:
FreeCAD.getDocument("core").getObject("Box").Length = core_radius + coil_thickness
FreeCAD.getDocument("core").getObject("Box").Width = 2*(core_radius + coil_thickness)
FreeCAD.getDocument("core").getObject("Box").Height = base_cut

# Can't understand the reason why the parameters are used in this fashion?
FreeCAD.getDocument("core").getObject("Box").Placement = \
App.Placement(App.Vector((core_radius+coil_thickness)/2+chamfer_length,\
                        -(core_radius+coil_thickness),0),\
                         App.Rotation(App.Vector(0,0,1),0)
             )

# Cut the part
# We perform the cut by doing Boolean operations:
# Here Base is the fusion object, while
# Box is the tool (which is the segment we intend to remove)
App.activeDocument().addObject("Part::Cut","Cut")
App.activeDocument().Cut.Base = App.activeDocument().Fusion
App.activeDocument().Cut.Tool = App.activeDocument().Box

# Hiding the older parts after creating new object Cut:
Gui.activeDocument().hide("Fusion")
Gui.activeDocument().hide("Box")

# Again, why does this need to to specified:
Gui.ActiveDocument.Cut.ShapeColor=Gui.ActiveDocument.Fusion.ShapeColor
Gui.ActiveDocument.Cut.DisplayMode=Gui.ActiveDocument.Fusion.DisplayMode

# Recomputing and fitting:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

###############################################################
# Add the primitive object Box:
App.ActiveDocument.addObject("Part::Box","Box")
App.ActiveDocument.ActiveObject.Label = "Cube"

# Setting parameters as defined by the user:
FreeCAD.getDocument("core").getObject("Box001").Length = core_radius + coil_thickness
FreeCAD.getDocument("core").getObject("Box001").Width = 2*(core_radius + coil_thickness)
FreeCAD.getDocument("core").getObject("Box001").Height = base_cut

# Don't understand why parameters have been formulated this way:
FreeCAD.getDocument("core").getObject("Box001").Placement = \
App.Placement(App.Vector(-3*(core_radius+coil_thickness)/2-chamfer_length,\
                           -(core_radius+coil_thickness),0),\
                            App.Rotation(App.Vector(0,0,1),0)
             )

# Performing a cutting operation:
# With the base being the earlier cut object, and tool being the
# newly defined box
App.activeDocument().addObject("Part::Cut","Cut001")
App.activeDocument().Cut001.Base = App.activeDocument().Cut
App.activeDocument().Cut001.Tool = App.activeDocument().Box001

# Toggling visibility of the older objects to false:
Gui.activeDocument().Cut.Visibility=False
Gui.activeDocument().Box001.Visibility=False

# Once again. Why is this needed:
Gui.ActiveDocument.Cut001.ShapeColor=Gui.ActiveDocument.Cut.ShapeColor
Gui.ActiveDocument.Cut001.DisplayMode=Gui.ActiveDocument.Cut.DisplayMode
App.ActiveDocument.recompute()

# Steps used to make hole through which core will recieve support 
# when mounted into the cover_base

# Refining the tool object we will use to drill:
App.ActiveDocument.addObject("Part::Cylinder","Cylinder003")
App.ActiveDocument.ActiveObject.Label = "Hole Left"

# Recomputing and fitting: 
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Setting the parameters as needed by the user:
FreeCAD.getDocument("core").getObject("Cylinder003").Radius = hole_diameter/2
FreeCAD.getDocument("core").getObject("Cylinder003").Height = total_core_height

# Placing at origin:
FreeCAD.getDocument("core").getObject("Cylinder003").Placement = \
App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))

# Performing the cut:
App.activeDocument().addObject("Part::Cut","Cut002")
App.activeDocument().Cut002.Base = App.activeDocument().Cut001
App.activeDocument().Cut002.Tool = App.activeDocument().Cylinder003

# Toggling visibility of the older objects:
Gui.activeDocument().Cut001.Visibility=False
Gui.activeDocument().Cylinder003.Visibility=False

# Once again. Why?
Gui.ActiveDocument.Cut002.ShapeColor=Gui.ActiveDocument.Cut001.ShapeColor
Gui.ActiveDocument.Cut002.DisplayMode=Gui.ActiveDocument.Cut001.DisplayMode
App.ActiveDocument.recompute()

##########################################################################
# Steps to make threads in the hole

# Why again?
Gui.activateWorkbench("PartWorkbench")

# Add a helix to form the base spine
App.ActiveDocument.addObject("Part::Helix","Helix")
App.ActiveDocument.Helix.Label='Helix'

# Adding parameters as given by the user:
App.ActiveDocument.Helix.Pitch =thread_pitch
App.ActiveDocument.Helix.Height=total_core_height-2*chamfer_length
App.ActiveDocument.Helix.Radius=hole_diameter/2
App.ActiveDocument.Helix.Angle=0.00

# What are the following 2 lines?
App.ActiveDocument.Helix.LocalCoord=0
App.ActiveDocument.Helix.Style=1

App.ActiveDocument.Helix.Placement=\
Base.Placement(Base.Vector(0.00,0.00,chamfer_length),Base.Rotation(0.00,0.00,0.00,1.00))

# Recomputing and fitting:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Add a sketch to sweep the helix with

# Changing to Sketcher Workbench
Gui.activateWorkbench("SketcherWorkbench")
App.activeDocument().addObject('Sketcher::SketchObject','Sketch')

# Why these numbers?
App.activeDocument().Sketch.Placement = \
App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))

#App.activeDocument().Sketch.MapMode = "Deactivated"

# Why is this needed?
Gui.activeDocument().setEdit('Sketch')

# My understanding is that arguments refer to LineSegment(start, end).
# What is the last argument of addGeometry?
# Why these numbers?
# Where are these lines referred to?
App.ActiveDocument.Sketch.addGeometry(Part.LineSegment(App.Vector(3.669230,4.655583,0),\
                                                       App.Vector(3.787592,3.037965,0)),\
                                                       False
                                                      )
App.ActiveDocument.Sketch.addGeometry(Part.LineSegment(App.Vector(3.787592,3.037966,0),\
                                                       App.Vector(5.799752,3.984863,0)),\
                                                       False)

# Adding constraints:
# What are the arguments in addConstraint?
# Constraining what objects?
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,2)) 
App.ActiveDocument.Sketch.addGeometry(Part.LineSegment(App.Vector(3.748140,4.537220,0),\
                                                       App.Vector(5.799752,3.984864,0)),\
                                                       False
                                                      )
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,0,1)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,1,2)) 

# Adding constraints:
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',0)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',2,1)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Angle',2,2,1,2,1.0472)) # 60 degrees  
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2,hole_diameter/2 - 0.1)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,1,2,hole_diameter/2 + 0.25))
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,1,2,chamfer_length+base_height)) 

# What is this?
Gui.getDocument("core").resetEdit()

App.getDocument("core").recompute()

# Sweep Helix to form solid thread
# Activating PartWorkbench:
Gui.activateWorkbench("PartWorkbench")

# Why are you importing again?
from FreeCAD import Base
import Part

App.getDocument("core").addObject('Part::Sweep','Sweep')
App.getDocument("core").ActiveObject.Sections=[App.getDocument("core").Sketch, ]
App.getDocument("core").ActiveObject.Spine=(App.ActiveDocument.Helix,[])
# What are the following 2 args?:
App.getDocument("core").ActiveObject.Solid=True
App.getDocument("core").ActiveObject.Frenet=True

# Toggling Visibility of the older objects:
Gui.getDocument("core").getObject("Helix").Visibility=False
Gui.getDocument("core").getObject("Sketch").Visibility=False
App.ActiveDocument.recompute()

# Cut the Thread into the cylinder
App.activeDocument().addObject("Part::Cut","Cut003")
App.activeDocument().Cut003.Base = App.activeDocument().Cut002
App.activeDocument().Cut003.Tool = App.activeDocument().Sweep
# Toggling Visibility of the older objects:
Gui.activeDocument().Cut002.Visibility=False
Gui.activeDocument().Sweep.Visibility=False

# Again. Why?
Gui.ActiveDocument.Cut003.ShapeColor=Gui.ActiveDocument.Cut002.ShapeColor
Gui.ActiveDocument.Cut003.DisplayMode=Gui.ActiveDocument.Cut002.DisplayMode
App.ActiveDocument.recompute()

##############################################################

# Chamfer the holes in the cylinder
# Code Not working - (Need to Chamfer Manually through GUI)
# Is there any significance to keeping this code?

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