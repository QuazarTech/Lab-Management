###############################################################################
# This script contains code to create a threaded bolt on which the coil cores
# will be mounted. The threads inside the cores will cause a translation motion
# when the cores are rotated on the mount.

# The mount also contains 2 holes on the sides, using which it will be mounted
# on the cover' base part.
###############################################################################

# Importing standard libraries
import sys

# Insert this directory into the PYTHONPATH to import experimental parameters from experiment_params.py
sys.path.insert(0, "${HOME}/work/git/Lab-Management/freecad_models/EM_Coupling_Experiment/code")

# Importing FreeCAD libraries
from FreeCAD import Base
import Part,PartGui

# Importing experiment specific variables from file
from experiment_params import total_core_height

from experiment_params import screw_length
from experiment_params import screw_diameter

from experiment_params import hole_diameter
from experiment_params import thread_pitch
from experiment_params import chamfer_length

from experiment_params import sheet_thickness
from experiment_params import bend_radius

from experiment_params import length_margin

# App and Gui are modules internal to FreeCAD:
# App's methods give you access to defining the properties of shapes
# Gui's methods can be used to change the way you want to represent the shape.

###############################################################################

# Create a new document for the CAD model
App.newDocument("mount")
App.setActiveDocument("mount")
App.ActiveDocument=App.getDocument("mount")
Gui.ActiveDocument=Gui.getDocument("mount")

# Tells the GUI to fit the object inside the screen
Gui.SendMsgToActiveView("ViewFit")

# Sets the view to axonometric- Isometric
Gui.activeDocument().activeView().viewAxometric()

###############################################################################

# Add cylinder that will be the main part for the mount
mounting_rod = App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
mounting_rod.Label = "Mounting Rod"

# Recompute and fit model to screen
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

mounting_rod.Radius    = hole_diameter/2
mounting_rod.Height    = 2*(total_core_height + length_margin + bend_radius)
mounting_rod.Placement = App.Placement(App.Vector(0, 0, 0), App.Rotation(App.Vector(0, 0, 1), 0))

# Recompute and fit model to screen
Gui.SendMsgToActiveView("ViewFit")
App.ActiveDocument.recompute()

###############################################################################
## Make threads on the outer surface of the mounting_rod

##################################################
# Create Helix that serves as the spine for the threads

thread_spine            = App.ActiveDocument.addObject("Part::Helix","Helix")
thread_spine.Label      = 'Thread Spine'

thread_spine.Pitch      = thread_pitch
thread_spine.Height     = 2*(total_core_height + length_margin - chamfer_length)
thread_spine.Radius     = hole_diameter/2
thread_spine.Angle      = 0.00 
thread_spine.LocalCoord = 0    # Right-Handed Helix
thread_spine.Style      = 1    # Clockwise

thread_spine.Placement  = \
    Base.Placement(Base.Vector(0.00,0.00,chamfer_length),
                   Base.Rotation(0.00,0.00,0.00,1.00))

# Recompute and fit model to screen
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

##################################################
# Create a profile sketch to sweep Helix

#Activate the Sketcher Workbench
Gui.activateWorkbench("SketcherWorkbench")

thread_profile = App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
thread_profile.Placement = \
    App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))

# What is map mode?
#App.activeDocument().Sketch.MapMode = "Deactivated"

# Open thread_profile sketch in edit mode
Gui.activeDocument().setEdit(thread_profile.Name)

# Add 3 line segments to create a triangular profile for the thread
thread_profile.addGeometry(Part.LineSegment(App.Vector(3.669230,4.655583,0),App.Vector(3.787592,3.037965,0)),False)
thread_profile.addGeometry(Part.LineSegment(App.Vector(3.787592,3.037966,0),App.Vector(5.799752,3.984863,0)),False)
thread_profile.addGeometry(Part.LineSegment(App.Vector(3.748140,4.537220,0),App.Vector(5.799752,3.984864,0)),False)

# Add constraints to join the 3 line segments into a triangle
thread_profile.addConstraint(Sketcher.Constraint('Coincident',1,1,0,2)) 
thread_profile.addConstraint(Sketcher.Constraint('Coincident',2,1,0,1)) 
thread_profile.addConstraint(Sketcher.Constraint('Coincident',2,2,1,2)) 

# Make one side vertical
thread_profile.addConstraint(Sketcher.Constraint('Vertical',0)) 

# Make the triangle equilateral
thread_profile.addConstraint(Sketcher.Constraint('Equal',2,1)) 
thread_profile.addConstraint(Sketcher.Constraint('Angle',2,2,1,2,1.0472)) # 60 degrees  

# Set position perpendicular to the Helix starting point
thread_profile.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2, hole_diameter/2 + 0.1)) 
thread_profile.addConstraint(Sketcher.Constraint('DistanceX',-1,1,1,2, hole_diameter/2 - 0.25))
thread_profile.addConstraint(Sketcher.Constraint('DistanceY',-1,1,1,2, chamfer_length)) 

# Exit edit mode of thread_profile
Gui.getDocument("mount").resetEdit()

# Recompute the document
App.getDocument("mount").recompute()

##################################################
#Sweep Helix to form solid thread

# Activate Part Workbench
Gui.activateWorkbench("PartWorkbench")

thread_tool = App.getDocument("mount").addObject('Part::Sweep','Sweep')
thread_tool.Sections=[thread_profile, ]
thread_tool.Spine=(thread_spine,[])

# "Solid=True" creates a solid if the profiles are of closed geometry
thread_tool.Solid=True

# The "Frenet" property controls how the profile orientation changes as it follows along the sweep path.
# If "Frenet" is "false", the orientation of the profile is kept consistent from point to point. 
# The resulting shape has the minimum possible twisting. Unintuitively, when a profile is swept along a helix,
# this results in the orientation of the profile slowly creep (rotate) as it follows the helix.
# Setting "Frenet" to true prevents such a creep.

thread_tool.Frenet=True

# Toggle Visibility of older subparts to false
Gui.getDocument("mount").getObject("Helix").Visibility=False
Gui.getDocument("mount").getObject("Sketch").Visibility=False

# Recompute the document
App.ActiveDocument.recompute()

##################################################
# Cut the threads on the mounting rod

threaded_rod = App.activeDocument().addObject("Part::Cut","Cut")

# Set the base of the cut to be mounting_rod
threaded_rod.Base = mounting_rod

# Set the cut tool as thread_tool
threaded_rod.Tool = thread_tool

# Toggle Visibility of older subparts to false
Gui.activeDocument().Cylinder.Visibility=False
Gui.activeDocument().Sweep.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut.
Gui.ActiveDocument.Cut.ShapeColor=Gui.ActiveDocument.Cylinder.ShapeColor
Gui.ActiveDocument.Cut.DisplayMode=Gui.ActiveDocument.Cylinder.DisplayMode

# Recompute the document
App.ActiveDocument.recompute()

###############################################################################
## Add Holes on the side of the threaded_rod to mount the rod onto the cover

##################################################
# Create a profile sketch for hole
hole_1_profile = App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')

# Map the sketch onto the side face of threaded_rod
hole_1_profile.MapMode = "FlatFace"
hole_1_profile.Support = [(App.getDocument('mount').Cut,'Face329')]

# Recompute the document
App.activeDocument().recompute()

# Open the hole_1_profile sketch in edit mode
Gui.activeDocument().setEdit(hole_1_profile.Name)

# Add a circular profile for the hole
hole_1_profile.addGeometry(Part.Circle(App.Vector(-0.834407,-0.768209,0),App.Vector(0,0,1),0.758518),False)

# Make the center of the circle coincident to the origin (and also center of the threaded_rod)
hole_1_profile.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1))

# Set the Radius of the hole as per user defined params
hole_1_profile.addConstraint(Sketcher.Constraint('Radius',0,screw_diameter/2)) 

# Exit the edit mode for hole_1_profile sketch
Gui.getDocument('mount').resetEdit()

# Recompute the document
App.getDocument('mount').recompute()

##################################################
# Extrude profile Sketch to create hole cut tool

# Switch to part workbench
Gui.activateWorkbench("PartWorkbench")

# Create a tool which will cut out the hole from the threaded_rod
hole_1_tool = FreeCAD.getDocument('mount').addObject('Part::Extrusion', 'Extrude')
hole_1_tool.Label = "Hole 1 Tool"

# hole_1_tool properties

# Set profile sketch to hole_1_profile
hole_1_tool.Base = hole_1_profile
hole_1_tool.DirMode = "Normal"
hole_1_tool.DirLink = None
# Length of the hole should be equal to screw_length
hole_1_tool.LengthFwd = screw_length
hole_1_tool.LengthRev = 0.0
hole_1_tool.Solid = True
# Reversed is set to True so that hole cuts into the surface of the threaded_rod 
hole_1_tool.Reversed = True
hole_1_tool.Symmetric = False
hole_1_tool.TaperAngle = 0.0
hole_1_tool.TaperAngleRev = 0.0

Gui.ActiveDocument.Extrude.ShapeColor=Gui.ActiveDocument.Sketch001.ShapeColor
Gui.ActiveDocument.Extrude.LineColor=Gui.ActiveDocument.Sketch001.LineColor
Gui.ActiveDocument.Extrude.PointColor=Gui.ActiveDocument.Sketch001.PointColor

# Prevent hole_1_tool.Base from showing up in the view object tree
hole_1_tool.Base.ViewObject.hide()

# Recompute the document
App.ActiveDocument.recompute()

##################################################
# Cut the hole
hole_1 = App.activeDocument().addObject("Part::Cut","Cut001")
hole_1.Label = "Threaded Rod - 1 hole"

# Set the base of the cut as threaded_rod
hole_1.Base = threaded_rod
hole_1.Tool = hole_1_tool

# Toggling Visibility of the older objects:
Gui.activeDocument().Cut.Visibility=False
Gui.activeDocument().Extrude.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut.
Gui.ActiveDocument.Cut001.ShapeColor=Gui.ActiveDocument.Cut.ShapeColor
Gui.ActiveDocument.Cut001.DisplayMode=Gui.ActiveDocument.Cut.DisplayMode
App.ActiveDocument.recompute()

##################################################
# Activate Sketcher Workbench
Gui.activateWorkbench("SketcherWorkbench")

# Create profile sketch for hole 2
hole_2_profile = App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')

# Map the hole_2_profile sketch onto the side wall of rod
hole_2_profile.MapMode = "FlatFace"
hole_2_profile.Support = [(hole_1,'Face5')]

# Recompute the document
App.activeDocument().recompute()

# Open hole_2_profile sketch in edit mode
Gui.activeDocument().setEdit(hole_2_profile.Name)

# Add circular profile to hole_2_profile sketch
hole_2_profile.addGeometry(Part.Circle(App.Vector(1.084989,-1.715090,0),App.Vector(0,0,1),0.740006),False)

# Make the center of the circle coincident to the origin (and also center of the threaded_rod)
hole_2_profile.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 

# Set radius of hole as per user defined params
hole_2_profile.addConstraint(Sketcher.Constraint('Radius',0,screw_diameter/2))

# Exit edit mode of hole_2_profile sketch
Gui.getDocument('mount').resetEdit()

# Recompute the document
App.getDocument('mount').recompute()

##################################################
# Extrude profile Sketch to create hole cut tool

# Activate Part Workbench
Gui.activateWorkbench("PartWorkbench")

# Create a tool which will cut out the hole from the threaded_rod
hole_2_tool = FreeCAD.getDocument('mount').addObject('Part::Extrusion', 'Extrude001')
hole_2_tool.Label = "Hole 2 Tool"

# hole_2_tool properties

# Set profile sketch to hole_2_profile
hole_2_tool.Base = hole_2_profile
hole_2_tool.DirMode = "Normal"
hole_2_tool.DirLink = None
# Length of the hole should be equal to screw_length
hole_2_tool.LengthFwd = screw_length
hole_2_tool.LengthRev = 0.0
hole_2_tool.Solid = True
# Reversed is set to True so that hole cuts into the surface of the threaded_rod 
hole_2_tool.Reversed = True
hole_2_tool.Symmetric = False
hole_2_tool.TaperAngle = 0.0
hole_2_tool.TaperAngleRev = 0.0

Gui.ActiveDocument.Extrude001.ShapeColor=Gui.ActiveDocument.Sketch002.ShapeColor
Gui.ActiveDocument.Extrude001.LineColor=Gui.ActiveDocument.Sketch002.LineColor
Gui.ActiveDocument.Extrude001.PointColor=Gui.ActiveDocument.Sketch002.PointColor

# Prevent hole_1_tool.Base from showing up in the view object tree
hole_2_tool.Base.ViewObject.hide()

# Recompute the document
App.ActiveDocument.recompute()

##################################################
#Cut the hole into the rod's side wall
threaded_mounting_rod = App.activeDocument().addObject("Part::Cut","Cut002")
threaded_mounting_rod.Label = "Threaded Mounting Rod"

# Set the base of the cut as the threaded_rod with 1 hole
threaded_mounting_rod.Base = hole_1
threaded_mounting_rod.Tool = hole_2_tool

# Toggling Visibility of the older objects:
Gui.activeDocument().Cut001.Visibility=False
Gui.activeDocument().Extrude001.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut.
Gui.ActiveDocument.Cut002.ShapeColor=Gui.ActiveDocument.Cut001.ShapeColor
Gui.ActiveDocument.Cut002.DisplayMode=Gui.ActiveDocument.Cut001.DisplayMode

# Recompute the document
App.ActiveDocument.recompute()
