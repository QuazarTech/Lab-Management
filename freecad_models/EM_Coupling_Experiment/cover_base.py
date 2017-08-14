############################################################################
# This script generates the bottom of the sheet metal cover in which the
# EM Coupling Experiment will be housed. It has holes is the side faces,
# on which the mounting rod (mount.fcstd) will be mount using screws.
# On the top flanges, the cover's top (cover_top.fcstd) will be mounted
# using 4 screws.
############################################################################

# Importing standard libraries
import sys
sys.path.insert(0, "${HOME}/work/git/Lab-Management/freecad_models/models")
sys.path.insert(0, "${HOME}/.FreeCAD/Mod/SheetMetal")

# Importing FreeCAD libraries
from FreeCAD import Base
import Part,PartGui

# Sheet Metal Workbench, needs to be installed from https://github.com/shaise/FreeCAD_SheetMetal
import SheetMetalCmd

# Importing experiment specific variables from file
from experiment_params import base_length
from experiment_params import base_width
from experiment_params import wall_height
from experiment_params import top_flange_width
from experiment_params import bend_radius

from experiment_params import coax_radius
from experiment_params import coax_base_width
from experiment_params import coax_bottom_distance
from experiment_params import coax_side_distance

from experiment_params import sheet_thickness
from experiment_params import screw_diameter

# App and Gui are modules internal to FreeCAD:
# App's methods give you access to defining the properties of shapes
# Gui's methods can be used to change the way you want to represent the shape.

############################################################################
# Create a new document for the CAD model

App.newDocument("cover_base")
App.setActiveDocument("cover_base")
App.ActiveDocument=App.getDocument("cover_base")
Gui.ActiveDocument=Gui.getDocument("cover_base")

# Tells the GUI to fit the object inside the screen
Gui.SendMsgToActiveView("ViewFit")

# Sets the view to axonometric- Isometric
Gui.activeDocument().activeView().viewAxometric()

############################################################################
# Create the Base Flange

# Activate the Part workbench
Gui.activateWorkbench("PartWorkbench")

base_flange = App.ActiveDocument.addObject("Part::Box","Box")
base_flange.Label = "Cube"

base_flange.Height = sheet_thickness
base_flange.Length = base_length
base_flange.Width  = base_width

# Recompute the document
App.ActiveDocument.recompute()

############################################################################
# Create the side walls using the sheetmetal workbench

# Activate Sheet Metal Workbench
Gui.activateWorkbench("SMWorkbench")

######################################
# Left Wall
left_wall = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Bend")
left_wall.Label = "Left Wall"

# The Selection submodule is a part of the FreeCADGui module.
# https://www.freecadweb.org/wiki/Selection_API

# Clear the selection
FreeCADGui.Selection.clearSelection()
# Select the face on base_flange on from which left wall is to be created
FreeCADGui.Selection.addSelection(base_flange, "Face1")

# Create a Sheetmetal bend
SheetMetalCmd.SMBendWall(left_wall)
SheetMetalCmd.SMViewProviderTree(left_wall.ViewObject)

# Set Bend radius and wall height
left_wall.radius = bend_radius
left_wall.length = wall_height

# Recompute the document and fir to view
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

######################################
# Right Wall
right_wall = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Bend001")
right_wall.Label = "Right Wall"

# Clear Selection and select the Face from which wall is to be created
FreeCADGui.Selection.clearSelection()
FreeCADGui.Selection.addSelection(left_wall, "Face14")

# Create a Sheetmetal bend
SheetMetalCmd.SMBendWall(right_wall)
SheetMetalCmd.SMViewProviderTree(right_wall.ViewObject)

# Set bend radius and wall height
right_wall.radius = bend_radius
right_wall.length = wall_height

# Recompute the document
App.ActiveDocument.recompute()

############################################################################
#Create the flanges at the top for screwing on cover_top

######################################
# Top Left Flange
top_left_flange = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Bend002")
top_left_flange.Label = "Top Left Flange"

# Clear Selection and select the face from which flange is to be created
FreeCADGui.Selection.clearSelection()
FreeCADGui.Selection.addSelection(right_wall, "Face22")

# Create a Sheetmetal bend
SheetMetalCmd.SMBendWall(top_left_flange)
SheetMetalCmd.SMViewProviderTree(top_left_flange.ViewObject)

# Set bend radius and wall height
top_left_flange.radius = bend_radius
top_left_flange.length = top_flange_width

# Recompute the document
App.ActiveDocument.recompute()

######################################
# Top Right Flange

top_right_flange = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Bend003")
top_right_flange.Label = "Top Right Flange"

# Clear Selection and select the face from which flange is to be created
FreeCADGui.Selection.clearSelection()
FreeCADGui.Selection.addSelection(top_left_flange, "Face30")

# Create a Sheetmetal bend
SheetMetalCmd.SMBendWall(top_right_flange)
SheetMetalCmd.SMViewProviderTree(top_right_flange.ViewObject)

# Set bend radius and wall height
top_right_flange.radius = bend_radius
top_right_flange.length = top_flange_width

# Recompute the document
App.ActiveDocument.recompute()

############################################################################
# Create holes for mounting support rod for cores

# Activate Part Workbench
Gui.activateWorkbench("PartWorkbench")

core_mount_hole_tool = App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
core_mount_hole_tool.Label = "Core Mounting Hole Tool"

core_mount_hole_tool.Radius = screw_diameter/2
core_mount_hole_tool.Height = base_length + 2*(sheet_thickness+bend_radius)

# Placement property consists of 3 things
# 1. Position = (x,y,z) is a Vector describing the point from which the object's
# geometry will be calculated (in effect, a "local origin" for the object).
# 2. Yaw-Pitch-Roll = (y,p,r) is a tuple that specifies the attitude of the object.
# Values for y,p,r specify degrees of rotation about each of the z,y,x axis (see note). 
# In the above code it is the z axis (0, 0, 1) because x and y are 0, and z is 1
# 3. Rotation Angle - This rotates the object by the specified angle along the axis 
# specified above (Below the angle is 0 : final argument of App.Placement())

core_mount_hole_tool.Placement = \
    App.Placement(App.Vector(-(sheet_thickness+bend_radius),base_width/2,wall_height/2),App.Rotation(App.Vector(0,1,0),90))

# Recompute and fit to screen
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

######################################
# Make holes to mount the mounting rod

cover_core_holes = App.activeDocument().addObject("Part::Cut","Cut")

# Set the base as top_right_flange
cover_core_holes.Base = top_right_flange
# Set the tool as core_mount_hole_tool
cover_core_holes.Tool = core_mount_hole_tool

# Toggling visibility of the older objects:
Gui.activeDocument().Bend003.Visibility=False
Gui.activeDocument().Cylinder.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut.
Gui.ActiveDocument.Cut.ShapeColor=Gui.ActiveDocument.Bend003.ShapeColor
Gui.ActiveDocument.Cut.DisplayMode=Gui.ActiveDocument.Bend003.DisplayMode

# Recompute the document
App.ActiveDocument.recompute()

############################################################################
## Holes on top to mount cover_top

######################################
# Top Hole 1
top_hole_tool_1 = App.ActiveDocument.addObject("Part::Cylinder","Cylinder001")
top_hole_tool_1.Label = "Top Hole Tool 1"

# Recompute and fit to screen
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Position to hole tool
top_hole_tool_1.Placement = \
    App.Placement(App.Vector(top_flange_width/2,base_width/4,wall_height+sheet_thickness+2*(bend_radius)),App.Rotation(App.Vector(0,0,1),0))

top_hole_tool_1.Radius = screw_diameter/2
top_hole_tool_1.Height = sheet_thickness

######################################
# Cut the hole
cover_base_1_hole = App.activeDocument().addObject("Part::Cut","Cut001")

cover_base_1_hole.Base = cover_core_holes
cover_base_1_hole.Tool = top_hole_tool_1

# Toggling visibility of the older objects:
Gui.activeDocument().Cut.Visibility=False
Gui.activeDocument().Cylinder001.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut
Gui.ActiveDocument.Cut001.ShapeColor=Gui.ActiveDocument.Cut.ShapeColor
Gui.ActiveDocument.Cut001.DisplayMode=Gui.ActiveDocument.Cut.DisplayMode

# Recompute the document
App.ActiveDocument.recompute()

######################################
# Top Hole 2
top_hole_tool_2 = App.ActiveDocument.addObject("Part::Cylinder","Cylinder002")
top_hole_tool_2.Label = "Top Hole Tool 2"

# Recompute and fit to screen
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

top_hole_tool_2.Placement = \
    App.Placement(App.Vector(top_flange_width/2,3*base_width/4,wall_height+sheet_thickness+2*(bend_radius)),App.Rotation(App.Vector(0,0,1),0))

top_hole_tool_2.Radius = screw_diameter/2
top_hole_tool_2.Height = sheet_thickness

######################################
# Cut the hole
cover_base_2_hole = App.activeDocument().addObject("Part::Cut","Cut002")

cover_base_2_hole.Base = cover_base_1_hole
cover_base_2_hole.Tool = top_hole_tool_2

# Toggling visibility of the older objects:
Gui.activeDocument().Cut001.Visibility=False
Gui.activeDocument().Cylinder002.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut
Gui.ActiveDocument.Cut002.ShapeColor=Gui.ActiveDocument.Cut001.ShapeColor
Gui.ActiveDocument.Cut002.DisplayMode=Gui.ActiveDocument.Cut001.DisplayMode

# Recompute the document
App.ActiveDocument.recompute()

######################################
# Top Hole 3
top_hole_tool_3 = App.ActiveDocument.addObject("Part::Cylinder","Cylinder003")
top_hole_tool_3.Label = "Top Hole Tool 3"

# Recompute and fit to screen
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

top_hole_tool_3.Placement = \
    App.Placement(App.Vector(base_length-top_flange_width/2,base_width/4,wall_height+sheet_thickness+2*(bend_radius)),App.Rotation(App.Vector(0,0,1),0))

top_hole_tool_3.Radius = screw_diameter/2
top_hole_tool_3.Height = sheet_thickness

######################################
# Cut the hole
cover_base_3_hole = App.activeDocument().addObject("Part::Cut","Cut003")

cover_base_3_hole.Base = cover_base_2_hole
cover_base_3_hole.Tool = top_hole_tool_3

# Toggling visibility of the older objects:
Gui.activeDocument().Cut002.Visibility=False
Gui.activeDocument().Cylinder003.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut
Gui.ActiveDocument.Cut003.ShapeColor=Gui.ActiveDocument.Cut002.ShapeColor
Gui.ActiveDocument.Cut003.DisplayMode=Gui.ActiveDocument.Cut002.DisplayMode

# Recompute the document
App.ActiveDocument.recompute()

######################################
# Top Hole 4
top_hole_tool_4 = App.ActiveDocument.addObject("Part::Cylinder","Cylinder004")
top_hole_tool_4.Label = "Top Hole Tool 4"

# Recompute and fit to screen
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

top_hole_tool_4.Placement = \
    App.Placement(App.Vector(base_length-top_flange_width/2,3*base_width/4,wall_height+sheet_thickness+2*(bend_radius)),App.Rotation(App.Vector(0,0,1),0))

top_hole_tool_4.Radius = screw_diameter/2
top_hole_tool_4.Height = sheet_thickness

######################################
# Cut the hole
cover_base_4_hole = App.activeDocument().addObject("Part::Cut","Cut004")

cover_base_4_hole.Base = cover_base_3_hole
cover_base_4_hole.Tool = top_hole_tool_4

# Toggling visibility of the older objects:
Gui.activeDocument().Cut003.Visibility=False
Gui.activeDocument().Cylinder004.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut
Gui.ActiveDocument.Cut004.ShapeColor=Gui.ActiveDocument.Cut003.ShapeColor
Gui.ActiveDocument.Cut004.DisplayMode=Gui.ActiveDocument.Cut003.DisplayMode

# Recompute the document
App.ActiveDocument.recompute()

############################################################################
# Create holes for Coaxial connector

#Activate Sketcher Workbench
Gui.activateWorkbench("SketcherWorkbench")

coax_conn_profile = App.activeDocument().addObject('Sketcher::SketchObject','Sketch')

# Map the sketch on one of the side walls of the cover_base
coax_conn_profile.MapMode = "FlatFace"
coax_conn_profile.Support = [(cover_base_4_hole,'Face15')]

# Recompute the document
App.activeDocument().recompute()

# Open coax_conn_profile sketch in edit mode
Gui.activeDocument().setEdit('Sketch')

# Add coax_conn base line
coax_conn_profile.addGeometry(Part.LineSegment(App.Vector(51.036247,57.121452,0),App.Vector(6.999034,57.816776,0)),False)

# Add constraints
coax_conn_profile.addConstraint(Sketcher.Constraint('Horizontal',0)) 
coax_conn_profile.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2,coax_side_distance)) 
coax_conn_profile.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,1,coax_side_distance+coax_base_width)) 
coax_conn_profile.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,2,coax_bottom_distance)) 

# Add coax_conn arc
coax_conn_profile.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(7.922558,56.798874,0),App.Vector(0,0,1),4.818108),6.245304,3.288062),False)

coax_conn_profile.addConstraint(Sketcher.Constraint('Radius',1,coax_radius)) 
coax_conn_profile.addConstraint(Sketcher.Constraint('Coincident',1,1,0,1)) 
coax_conn_profile.addConstraint(Sketcher.Constraint('Coincident',1,2,0,2)) 

# Exit edit mode
Gui.getDocument('cover_base').resetEdit()

# Recompute the document
App.getDocument('cover_base').recompute()

######################################
# Extrude the coax_conn_profile to create coax_conn_cut_tool

# Activate the Part Workbench
Gui.activateWorkbench("PartWorkbench")

# Createcoax_conn_cut_tool
coax_conn_cut_tool = FreeCAD.getDocument('cover_base').addObject('Part::Extrusion', 'Extrude')

coax_conn_cut_tool.Base = App.getDocument('cover_base').getObject('Sketch')
coax_conn_cut_tool.DirMode = "Normal"
coax_conn_cut_tool.DirLink = None
# Set length such that it cuts both side walls
coax_conn_cut_tool.LengthFwd = base_length + 2*bend_radius + 2*sheet_thickness
coax_conn_cut_tool.LengthRev = 0
coax_conn_cut_tool.Solid = True
coax_conn_cut_tool.Reversed = True
coax_conn_cut_tool.Symmetric = False
coax_conn_cut_tool.TaperAngle = 0.0
coax_conn_cut_tool.TaperAngleRev = 0.0

Gui.ActiveDocument.Extrude.ShapeColor=Gui.ActiveDocument.Sketch.ShapeColor
Gui.ActiveDocument.Extrude.LineColor=Gui.ActiveDocument.Sketch.LineColor
Gui.ActiveDocument.Extrude.PointColor=Gui.ActiveDocument.Sketch.PointColor

coax_conn_cut_tool.Base.ViewObject.hide()

# Recompute the document
App.ActiveDocument.recompute()

######################################
# Cut the holes for coax connectors
cover_base_complete = App.activeDocument().addObject("Part::Cut","Cut005")

cover_base_complete.Base = cover_base_4_hole
cover_base_complete.Tool = coax_conn_cut_tool

# Toggling visibility of the older objects:
Gui.activeDocument().Cut004.Visibility=False
Gui.activeDocument().Extrude.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut
Gui.ActiveDocument.Cut005.ShapeColor=Gui.ActiveDocument.Cut004.ShapeColor
Gui.ActiveDocument.Cut005.DisplayMode=Gui.ActiveDocument.Cut004.DisplayMode

# Recompute the document
App.ActiveDocument.recompute()
