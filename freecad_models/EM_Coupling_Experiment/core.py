#####################################################################
# This script generates a cylindrical core, that fits on the coil
# winding machine at Quazar Tech. It has threads inside, so that it 
# can be mounted on a threaded bolt (mount.fcstd). Rotating the core
# when it is mounted on the threaded bolt will cause translation.

# A coil will be wound on this core.
#####################################################################

# Importing standard libraries
import sys

# Insert this directory into the PYTHONPATH to import experimental parameters from experiment_params.py
sys.path.insert(0, "${HOME}/work/git/Lab-Management/freecad_models/EM_Coupling_Experiment/code")

# Importing FreeCAD libraries
from FreeCAD import Base
import Part,PartGui

# Importing experiment specific variables from file
from experiment_params import core_height
from experiment_params import core_radius
from experiment_params import total_core_height

from experiment_params import base_height
from experiment_params import base_cut
from experiment_params import top_height
from experiment_params import coil_thickness

from experiment_params import hole_diameter
from experiment_params import thread_pitch
from experiment_params import chamfer_length
from experiment_params import epsilon

# App and Gui are modules internal to FreeCAD:
# App's methods give you access to defining the properties of shapes
# Gui's methods can be used to change the way you want to represent the shape.

#####################################################################

# Create a new document for the CAD model
App.newDocument("core")
App.setActiveDocument("core")
App.ActiveDocument=App.getDocument("core")
Gui.ActiveDocument=Gui.getDocument("core")

# Tells the GUI to fit the object inside the screen
Gui.SendMsgToActiveView("ViewFit")

# Sets the view to axonometric- Isometric
Gui.activeDocument().activeView().viewAxometric()

#####################################################################
# Workbenches contain all the functionality in FreeCAD. 
# Depending on what you want to do, you need to use a different workbench
# Here, to create a Part::Box, we need the part workbench.
Gui.activateWorkbench("PartWorkbench")

# The core is made up of 3 cylinders - cylinder_base, cylinder_center
# and cylinder_top, fused together to form one part.
# The coil is wound around cylinder_center
# The coil winding machine will hold cylinder_base in a clamp
# cylinder_top has a chamfered hole through which the coil winding
# machine will support the core.

#####################################
# Steps to create cylinder_center
# Initializing the cylinder using the primitive object defined in FreeCAD
cylinder_center       = App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
cylinder_center.Label = "Cylinder Center"

# Recomputes the document - and updates all properties that have been changed 
# inside the document.
App.ActiveDocument.recompute()
# Tells the GUI to fit the object inside the screen
Gui.SendMsgToActiveView("ViewFit")

# Assigning the properties of the object as the user declares in params
cylinder_center.Radius = core_radius
cylinder_center.Height = core_height

# Recomputing and fitting to screen:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Placement property consists of 3 things
# 1. Position = (x,y,z) is a Vector describing the point from which the object's
# geometry will be calculated (in effect, a "local origin" for the object).
# 2. Yaw-Pitch-Roll = (y,p,r) is a tuple that specifies the attitude of the object.
# Values for y,p,r specify degrees of rotation about each of the z,y,x axis (see note). 
# In the above code it is the z axis (0, 0, 1) because x and y are 0, and z is 1
# 3. Rotation Angle - This rotates the object by the specified angle along the axis 
# specified above (Below the angle is 0 : final argument of App.Placement())

cylinder_center.Placement = \
App.Placement(App.Vector(0, 0, base_height), App.Rotation(App.Vector(0, 0, 1), 0))

#####################################
# Steps to create cylinder_base:
# Adding primitive object:
cylinder_base = App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
cylinder_base.Label = "Cylinder Base"

# Recomputing and fitting:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Setting the parameters of the object as needed by the user:
cylinder_base.Radius = core_radius + coil_thickness
cylinder_base.Height = base_height

# Since this cylinder is the base, we set its position vector to (0, 0, 0):
cylinder_base.Placement = \
App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 0))

# Recomputing and fitting:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

#####################################
# Steps to create cylinder_top

# Adding primitive object:
cylinder_top = App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
cylinder_top.Label = "Cylinder Top"

# Recomputing and fitting:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Setting the parameters of the object as needed by the user:
cylinder_top.Radius = core_radius + coil_thickness
cylinder_top.Height = top_height

# This cylinder comes above Cylinders 1 and 2: 
cylinder_top.Placement = \
App.Placement(App.Vector(0, 0, base_height + core_height), App.Rotation(App.Vector(0, 0, 1), 0))

# Recomputing and fitting:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

#####################################
## Fuse all 3 cylinders into one part

# Fusion will create a new object which is a union of the above defined cylinders:
# The name of this newly created object is fusion:
fused_cylinder = App.activeDocument().addObject("Part::MultiFuse","Fusion")
fused_cylinder.Label  = "Fused Cylinders" 
fused_cylinder.Shapes = \
[App.activeDocument().Cylinder,App.activeDocument().Cylinder002,App.activeDocument().Cylinder001,]

# After creating the new fused object, we toggle the visibility of the subparts
# that compose the object to false:
Gui.activeDocument().Cylinder.Visibility=False
Gui.activeDocument().Cylinder002.Visibility=False
Gui.activeDocument().Cylinder001.Visibility=False

# Setting the visual properties of the new part generated to the old part which
# was used for fusion
Gui.ActiveDocument.Fusion.ShapeColor=Gui.ActiveDocument.Cylinder002.ShapeColor
Gui.ActiveDocument.Fusion.DisplayMode=Gui.ActiveDocument.Cylinder002.DisplayMode
App.ActiveDocument.recompute()

##############################################################
# Adding the box as primitive object to cut the base to make grip
right_cut_tool = App.ActiveDocument.addObject("Part::Box","Box")
App.ActiveDocument.ActiveObject.Label = "Cube"

# Setting the parameters of the object as needed by the user:
right_cut_tool.Length = core_radius + coil_thickness
right_cut_tool.Width = 2 * (core_radius + coil_thickness)
right_cut_tool.Height = base_cut

# Parameters for right_cut_tool placement obtained by trial and error
right_cut_tool.Placement = \
App.Placement(App.Vector((core_radius+coil_thickness)/2 + chamfer_length,
                        -(core_radius+coil_thickness), 0),
                         App.Rotation(App.Vector(0, 0, 1), 0)
             )

#####################################
# Cut the base of the fused_cylinder part
# We perform the cut by doing Boolean operations:
# Here the base for the cut is the fused_cylinder, while
# right_cut_tool is the tool (which is the segment we intend to remove)
right_cut = App.activeDocument().addObject("Part::Cut","Cut")
right_cut.Base = fused_cylinder
right_cut.Tool = right_cut_tool

# Hiding the base and tool for the cut after creating new object right_cut:
Gui.activeDocument().hide("Fusion")
Gui.activeDocument().hide("Box")

# Setting the visual properties of the new part generated to be the same as
# the old part which was the base of the cut
Gui.ActiveDocument.Cut.ShapeColor=Gui.ActiveDocument.Fusion.ShapeColor
Gui.ActiveDocument.Cut.DisplayMode=Gui.ActiveDocument.Fusion.DisplayMode

# Recomputing and fitting:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

###############################################################
# Add the primitive object Box:
left_cut_tool = App.ActiveDocument.addObject("Part::Box","Box")
left_cut_tool.Label = "Cube"

# Setting parameters as defined by the user:
left_cut_tool.Length = core_radius + coil_thickness
left_cut_tool.Width = 2*(core_radius + coil_thickness)
left_cut_tool.Height = base_cut

# Parameters for left_cut_tool placement obtained by trial and error
left_cut_tool.Placement = \
App.Placement(App.Vector(-3*(core_radius + coil_thickness)/2 - chamfer_length,
                           -(core_radius+coil_thickness), 0),
                            App.Rotation(App.Vector(0, 0, 1), 0)
             )

#####################################
# Performing a cutting operation:
# With the base being the earlier right_cut object, and tool being the
# newly defined left_cut_tool
left_cut = App.activeDocument().addObject("Part::Cut","Cut001")
left_cut.Base = right_cut
left_cut.Tool = left_cut_tool

# Toggling visibility of the older objects to false:
Gui.activeDocument().Cut.Visibility=False
Gui.activeDocument().Box001.Visibility=False

# Setting the visual properties of the new part generated to be the same as
# the old part which was the base of the cut
Gui.ActiveDocument.Cut001.ShapeColor=Gui.ActiveDocument.Cut.ShapeColor
Gui.ActiveDocument.Cut001.DisplayMode=Gui.ActiveDocument.Cut.DisplayMode
App.ActiveDocument.recompute()

###############################################################
# Steps used to make hole through which core will recieve support 
# when mounted onto the mounting rod

# Defining the tool object we will use to drill:
hole_tool = App.ActiveDocument.addObject("Part::Cylinder","Cylinder003")
hole_tool.Label = "Hole Left"

# Recomputing and fitting: 
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Setting the parameters as needed by the user:
hole_tool.Radius = hole_diameter/2
hole_tool.Height = total_core_height

# Placing at origin:
hole_tool.Placement = \
App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))

#####################################
# Performing the cut:
App.activeDocument().addObject("Part::Cut","Cut002")
App.activeDocument().Cut002.Base = left_cut
App.activeDocument().Cut002.Tool = hole_tool

# Toggling visibility of the older objects:
Gui.activeDocument().Cut001.Visibility=False
Gui.activeDocument().Cylinder003.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut.
Gui.ActiveDocument.Cut002.ShapeColor=Gui.ActiveDocument.Cut001.ShapeColor
Gui.ActiveDocument.Cut002.DisplayMode=Gui.ActiveDocument.Cut001.DisplayMode
App.ActiveDocument.recompute()

##########################################################################
# Steps to make internal threads in the hole

#####################################
# Add a helix to form the base spine for the internal threads
thread_spine = App.ActiveDocument.addObject("Part::Helix","Helix")
thread_spine.Label='Helix'

# Adding parameters as given by the user:
thread_spine.Pitch      = thread_pitch
thread_spine.Height     = total_core_height - 2*chamfer_length
thread_spine.Radius     = hole_diameter/2
thread_spine.Angle      = 0.00 # Angle of the helix
thread_spine.LocalCoord = 0    # RIght-handed
thread_spine.Style      = 1    # Clockwise

thread_spine.Placement  = \
Base.Placement(Base.Vector(0.00, 0.00, chamfer_length), Base.Rotation(0.00, 0.00, 0.00, 1.00))

# Recomputing and fitting:
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

#####################################
# Add a sketch to sweep the helix with

# Changing to Sketcher Workbench
Gui.activateWorkbench("SketcherWorkbench")

thread_profile = App.activeDocument().addObject('Sketcher::SketchObject','Sketch')


thread_profile.Placement = \
App.Placement(App.Vector(0.000000,0.000000,0.000000), App.Rotation(-0.707107,0.000000,0.000000,-0.707107))

# Open the sketch in edit mode
Gui.activeDocument().setEdit(thread_profile.Name)

# Add 3 line segments to create a triangular profile for the thread
thread_profile.addGeometry(Part.LineSegment(App.Vector(3.669230,4.655583,0),\
                                                       App.Vector(3.787592,3.037965,0)),\
                                                       False
                                                      )
thread_profile.addGeometry(Part.LineSegment(App.Vector(3.787592,3.037966,0),\
                                                       App.Vector(5.799752,3.984863,0)),\
                                                       False)

thread_profile.addGeometry(Part.LineSegment(App.Vector(3.748140,4.537220,0),\
                                                       App.Vector(5.799752,3.984864,0)),\
                                                       False
                                                      )

# Adding constraints to the line segments:

# The point-on-point constraints are of the form : 
# Sketch.addConstraint(Sketcher.Constraint('Coincident',LineFixed,PointOfLineFixed,LineMoving,PointOfLineMoving))
# where,
#    Sketch is a sketch object
#    LineFixed is the number of the line, that will not move by applying the constraint
#    PointOfLineFixed is the number of the vertex of the line LineFixed that has to fulfilled the constraint
#    LineMoving is the number of the line, that will move by applying the constraint
#    PointOfLineMoving is the number of the line LineMoving, that has to fulfilled the constraint

thread_profile.addConstraint(Sketcher.Constraint('Coincident',1,1,0,2)) 
thread_profile.addConstraint(Sketcher.Constraint('Coincident',2,1,0,1)) 
thread_profile.addConstraint(Sketcher.Constraint('Coincident',2,2,1,2)) 

thread_profile.addConstraint(Sketcher.Constraint('Vertical',0)) 
thread_profile.addConstraint(Sketcher.Constraint('Equal',2,1)) 
thread_profile.addConstraint(Sketcher.Constraint('Angle',2,2,1,2,1.0472)) # 60 degrees  
thread_profile.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2,hole_diameter/2 - 0.1)) 
thread_profile.addConstraint(Sketcher.Constraint('DistanceX',-1,1,1,2,hole_diameter/2 + 0.25))
thread_profile.addConstraint(Sketcher.Constraint('DistanceY',-1,1,1,2,chamfer_length+base_height)) 

# Exit the edit mode for the thread_profile sketch
Gui.getDocument("core").resetEdit()

# Recompute the document
App.getDocument("core").recompute()

#####################################
# Sweep Helix to form solid helical shape to act as thread cutting tool
# Activating PartWorkbench:
Gui.activateWorkbench("PartWorkbench")

thread = App.getDocument("core").addObject('Part::Sweep','Sweep')
thread.Sections=[App.getDocument("core").Sketch, ] # Add cross-section profile
thread.Spine=(App.ActiveDocument.Helix,[])         # Add spine

# "Solid=True" creates a solid if the profiles are of closed geometry
thread.Solid=True

# The "Frenet" property controls how the profile orientation changes as it follows along the sweep path.
# If "Frenet" is "false", the orientation of the profile is kept consistent from point to point. 
# The resulting shape has the minimum possible twisting. Unintuitively, when a profile is swept along a helix,
# this results in the orientation of the profile slowly creep (rotate) as it follows the helix.
# Setting "Frenet" to true prevents such a creep.
thread.Frenet=True

# Toggling Visibility of the older objects:
Gui.getDocument("core").getObject("Helix").Visibility=False
Gui.getDocument("core").getObject("Sketch").Visibility=False
App.ActiveDocument.recompute()

#####################################
# Cut the Thread into the cylinder
threaded_core = App.activeDocument().addObject("Part::Cut","Cut003")
threaded_core.Base = App.activeDocument().Cut002
threaded_core.Tool = App.activeDocument().Sweep

# Toggling Visibility of the older objects:
Gui.activeDocument().Cut002.Visibility=False
Gui.activeDocument().Sweep.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut.
Gui.ActiveDocument.Cut003.ShapeColor=Gui.ActiveDocument.Cut002.ShapeColor
Gui.ActiveDocument.Cut003.DisplayMode=Gui.ActiveDocument.Cut002.DisplayMode

# Recompute
App.ActiveDocument.recompute()

##############################################################

# Chamfer the hole's edges in the cylinder
chamfer = FreeCAD.ActiveDocument.addObject("Part::Chamfer","Chamfer")
chamfer.Base = FreeCAD.ActiveDocument.Cut003

# Select the edges to chamfer
chamfer_edges = []
chamfer_edges.append((15, chamfer_length-epsilon, chamfer_length-epsilon)) #left
chamfer_edges.append((46, chamfer_length-epsilon, chamfer_length-epsilon)) #right

# Perform the chamfer operation on the select
chamfer.Edges = chamfer_edges
del chamfer_edges

# Toggle Visibility of of older part
FreeCADGui.ActiveDocument.Cut003.Visibility = False

# Setting the visual properties of the new generated part to be the same
# as that of old part on which chamfer operation was performed.
Gui.ActiveDocument.Chamfer.LineColor=Gui.ActiveDocument.Cut003.LineColor
Gui.ActiveDocument.Chamfer.PointColor=Gui.ActiveDocument.Cut003.PointColor
Gui.activeDocument().resetEdit()

# Recompute and fit to screen
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")