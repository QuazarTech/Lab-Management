############################################################################
# This script generates the top part for the sheet metal cover in which the
# EM Coupling Experiment will be housed. It has holes on the top, using
# which it will be mounted on the cover's bottom part (cover_base.fcstd)
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

from experiment_params import sheet_thickness
from experiment_params import screw_diameter

# App and Gui are modules internal to FreeCAD:
# App's methods give you access to defining the properties of shapes
# Gui's methods can be used to change the way you want to represent the shape.

######################################
# Create a new document for the CAD model

App.newDocument("cover_top")
App.setActiveDocument("cover_top")
App.ActiveDocument=App.getDocument("cover_top")
Gui.ActiveDocument=Gui.getDocument("cover_top")

# Tells the GUI to fit the object inside the screen
Gui.SendMsgToActiveView("ViewFit")

# Sets the view to axonometric- Isometric
Gui.activeDocument().activeView().viewAxometric()

############################################################################
# Create the Base Flange

# Activate the Part workbench
Gui.activateWorkbench("PartWorkbench")

base_flange = App.ActiveDocument.addObject("Part::Box","Box")
base_flange.Label = "Base Flange"

base_flange.Height = sheet_thickness
base_flange.Length = base_length
base_flange.Width  = base_width

# Recompute the document
App.ActiveDocument.recompute()

############################################################################
# Create the front and back walls using the sheetmetal workbench

# Activate Sheet Metal Workbench
Gui.activateWorkbench("SMWorkbench")

######################################
# Front wall
front_wall = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Bend")
front_wall.Label = "Front Wall"

# The Selection submodule is a part of the FreeCADGui module.
# https://www.freecadweb.org/wiki/Selection_API

# Clear the selection
FreeCADGui.Selection.clearSelection()
# Select the face on base_flange on from which front wall is to be created
FreeCADGui.Selection.addSelection(base_flange, "Face3")

# Create a Sheetmetal bend
SheetMetalCmd.SMBendWall(front_wall)
SheetMetalCmd.SMViewProviderTree(front_wall.ViewObject)

# Invert the bend to go in downward direction
FreeCAD.getDocument("cover_top").getObject("Bend").invert = True
# Set length of front wall
FreeCAD.getDocument("cover_top").getObject("Bend").length = wall_height + sheet_thickness

# Recompute the document
App.ActiveDocument.recompute()

######################################
## Back Wall
back_wall = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Bend001")
back_wall.Label = "Back Wall"

# Clear the selection
FreeCADGui.Selection.clearSelection()
# Select the face on base_flange on from which front wall is to be created
FreeCADGui.Selection.addSelection(front_wall, "Face14")

# Create a Sheetmetal bend
SheetMetalCmd.SMBendWall(back_wall)
SheetMetalCmd.SMViewProviderTree(back_wall.ViewObject)

# Invert the bend to go in downward direction
FreeCAD.getDocument("cover_top").getObject("Bend001").invert = True
# Set length of back wall
FreeCAD.getDocument("cover_top").getObject("Bend001").length = wall_height + sheet_thickness

# Recompute the document
App.ActiveDocument.recompute()

############################################################################
# Holes to Mount cover_bottom with screws

######################################
# Top Hole 1
top_hole_tool_1 = App.ActiveDocument.addObject("Part::Cylinder","Cylinder001")
top_hole_tool_1.Label = "Top Hole Tool 1"

# Recompute and fit to screen
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

top_hole_tool_1.Placement = \
    App.Placement(App.Vector(top_flange_width/2,base_width/4,0),App.Rotation(App.Vector(0,0,1),0))

top_hole_tool_1.Radius = screw_diameter/2
top_hole_tool_1.Height = sheet_thickness

######################################
# Cut the hole
cover_top_1_hole = App.activeDocument().addObject("Part::Cut","Cut001")

cover_top_1_hole.Base = back_wall
cover_top_1_hole.Tool = top_hole_tool_1

# Toggling visibility of the older objects:
Gui.activeDocument().Bend001.Visibility=False
Gui.activeDocument().Cylinder001.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut
Gui.ActiveDocument.Cut001.ShapeColor=Gui.ActiveDocument.Bend001.ShapeColor
Gui.ActiveDocument.Cut001.DisplayMode=Gui.ActiveDocument.Bend001.DisplayMode

# Recompute the document
App.ActiveDocument.recompute()

######################################
# Top Hole 2
top_hole_tool_2 = App.ActiveDocument.addObject("Part::Cylinder","Cylinder002")
top_hole_tool_2.Label = "Top Hole Tool 2"

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

top_hole_tool_2.Placement = \
    App.Placement(App.Vector(top_flange_width/2,3*base_width/4,0),App.Rotation(App.Vector(0,0,1),0))

top_hole_tool_2.Radius = screw_diameter/2
top_hole_tool_2.Height = sheet_thickness

######################################
# Cut the hole
cover_top_2_hole = App.activeDocument().addObject("Part::Cut","Cut002")

cover_top_2_hole.Base = cover_top_1_hole
cover_top_2_hole.Tool = top_hole_tool_2

# Toggling visibility of the older objects:
Gui.activeDocument().Cut001.Visibility=False
Gui.activeDocument().Cylinder002.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut
Gui.ActiveDocument.Cut002.ShapeColor=Gui.ActiveDocument.Cut001.ShapeColor
Gui.ActiveDocument.Cut002.DisplayMode=Gui.ActiveDocument.Cut001.DisplayMode

App.ActiveDocument.recompute()

######################################
# Top Hole 3
top_hole_tool_3 = App.ActiveDocument.addObject("Part::Cylinder","Cylinder003")
top_hole_tool_3.Label = "Top Hole Tool 3"

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

top_hole_tool_3.Placement = \
    App.Placement(App.Vector(base_length-top_flange_width/2,base_width/4,0),App.Rotation(App.Vector(0,0,1),0))

top_hole_tool_3.Radius = screw_diameter/2
top_hole_tool_3.Height = sheet_thickness

######################################
# Cut the hole
cover_top_3_hole = App.activeDocument().addObject("Part::Cut","Cut003")

cover_top_3_hole.Base = cover_top_2_hole
cover_top_3_hole.Tool = top_hole_tool_3

# Toggling visibility of the older objects:
Gui.activeDocument().Cut002.Visibility=False
Gui.activeDocument().Cylinder003.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut
Gui.ActiveDocument.Cut003.ShapeColor=Gui.ActiveDocument.Cut002.ShapeColor
Gui.ActiveDocument.Cut003.DisplayMode=Gui.ActiveDocument.Cut002.DisplayMode

App.ActiveDocument.recompute()

######################################
# Top Hole 4
top_hole_tool_4 = App.ActiveDocument.addObject("Part::Cylinder","Cylinder004")
top_hole_tool_4.Label = "Cover Bottom Mount"

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

top_hole_tool_4.Placement = \
    App.Placement(App.Vector(base_length-top_flange_width/2,3*base_width/4,0),App.Rotation(App.Vector(0,0,1),0))

top_hole_tool_4.Radius = screw_diameter/2
top_hole_tool_4.Height = sheet_thickness

######################################
# Cut the hole
cover_top_4_hole = App.activeDocument().addObject("Part::Cut","Cut004")

cover_top_4_hole.Base = cover_top_3_hole
cover_top_4_hole.Tool = top_hole_tool_4

# Toggling visibility of the older objects:
Gui.activeDocument().Cut003.Visibility=False
Gui.activeDocument().Cylinder004.Visibility=False

# Setting the visual properties of the new generated part to be the same
# as that of the base of the cut
Gui.ActiveDocument.Cut004.ShapeColor=Gui.ActiveDocument.Cut003.ShapeColor
Gui.ActiveDocument.Cut004.DisplayMode=Gui.ActiveDocument.Cut003.DisplayMode

App.ActiveDocument.recompute()

# Make the cover_top 80% Transparent
FreeCADGui.getDocument("cover_top").getObject("Cut004").Transparency = 80
######################################