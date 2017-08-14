###############################################################################
# This script creates a coil made up of two concentric helixes, one inside
#  the other. Both the helixes are joined using a spiral, whose radius 
# transitions from the radius of the inner helix to the radius of the outer helix
# over one complete rotation.
#
# TODO : Write a program to take in an arbitrary number of turns and generate
# the required number of helixes depending on the specified length of the coil,
# and the radius of the wire.
###############################################################################
# Importing standard libraries
import math
import sys

# Insert this directory into the PYTHONPATH to import experimental parameters from experiment_params.py
sys.path.insert(0, "${HOME}/work/git/Lab-Management/freecad_models/EM_Coupling_Experiment/code")

# Importing FreeCAD libraries
from FreeCAD import Base
import Part,PartGui

# Importing experiment specific variables from file
from experiment_params import coil_radius
from experiment_params import coil_height
from experiment_params import wire_radius
from experiment_params import gap

from experiment_params import core_height
from experiment_params import core_radius

# App and Gui are modules internal to FreeCAD:
# App's methods give you access to defining the properties of shapes
# Gui's methods can be used to change the way you want to represent the shape.

###############################################################################
# Create a new document for the CAD model

coil_winding = App.newDocument('coil')
App.setActiveDocument('coil')
App.ActiveDocument=App.getDocument('coil')
Gui.ActiveDocument=Gui.getDocument('coil')

###############################################################################
# Modification of coil_height to accomodate an integral number of turns

conversion_factor = math.floor((core_height)/(2*wire_radius)) #Integral number of turns that can be accomodated in each coil
coil_height = conversion_factor * (2*wire_radius)

###############################################################################
# Create Helical Structures joined by spiral structure

#Activate Part Workbench
Gui.activateWorkbench("PartWorkbench")

# Creating the spine for the innermost helix
helix_1_spine = App.ActiveDocument.addObject("Part::Helix","Helix")
helix_1_spine.Pitch      = 2 * (wire_radius + gap)
helix_1_spine.Height     = coil_height
helix_1_spine.Radius     = coil_radius
helix_1_spine.Angle      = 0.00 # Not Tapered
helix_1_spine.LocalCoord = 0    # Right-Handed
helix_1_spine.Style      = 1    # Clockwise
helix_1_spine.Placement  = Base.Placement(Base.Vector(0.00,0.00,0.00),Base.Rotation(0.00,0.00,0.00,1.00))
helix_1_spine.Label      = 'Innermost Helix'

# Recompute and fit to screen
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

# Creating a spine for a spiral that seamlessly joins the inner and outer helixes
spiral_1_spine = App.ActiveDocument.addObject("Part::Spiral","Spiral")
spiral_1_spine.Growth    = 2*(wire_radius + gap)
spiral_1_spine.Rotations = 1.00
spiral_1_spine.Radius    = coil_radius
spiral_1_spine.Placement = Base.Placement(Base.Vector(0.00,0.00,coil_height),Base.Rotation(0.00,0.00,0.00,1.00))
spiral_1_spine.Label     = 'Spiral'

# Recompute and fit to screen
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

#2nd from innermost helix parameters
helix_2_spine = App.ActiveDocument.addObject("Part::Helix","Helix001")
helix_2_spine.Pitch      = 2 * (wire_radius + gap)
helix_2_spine.Height     = coil_height
helix_2_spine.Radius     = coil_radius + 1*(wire_radius + gap)
helix_2_spine.Angle      = 0.00 # Not Tapered
helix_2_spine.LocalCoord = 1    # Right-Handed
helix_2_spine.Style      = 1    # Clockwise
helix_2_spine.Placement=Base.Placement(Base.Vector(0.00,0.00,0.00),Base.Rotation(0.00,0.00,0.00,1.00))
helix_2_spine.Label='Helix'

# Recompute and fit to screen
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

raw_input ('Joined Helixes complete : Press enter to continue')

###############################################################################
# Create profile of the wire to be swept along the helix_1_spine created above

# Activate Sketcher Workbench
Gui.activateWorkbench("SketcherWorkbench")

# Create Sketch object and place it at one end of helix_1_spine
helix_1_profile = App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
helix_1_profile.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))

# Open helix_1_profile sketch in edit mode
Gui.activeDocument().setEdit(helix_1_profile.Name)

# Create a circular profile for the wire
helix_1_profile.addGeometry(Part.Circle(App.Vector(1.286811,-0.212345,0),App.Vector(0,0,1),0.158677))

# Fix radius
helix_1_profile.addConstraint(Sketcher.Constraint('Radius',0,wire_radius)) 

# Set positional constraints
helix_1_profile.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,0.00)) 
helix_1_profile.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,core_radius + wire_radius + gap)) 

# Exit edit mode and recompute
Gui.getDocument('coil').resetEdit()
App.getDocument('coil').recompute()

#############################################
#Sweep helix 1 with helix_1_profile sketch

# Activate Part Workbench
Gui.activateWorkbench("PartWorkbench")

helix_1 = App.getDocument('coil').addObject('Part::Sweep','Sweep')

# Select the cross-sectional profile to sweep
helix_1.Sections=[helix_1_profile, ]

# Select the spine along which to sweep
helix_1.Spine=(helix_1_spine,[])

# "Solid=True" creates a solid if the profiles are of closed geometry
helix_1.Solid=True

# The "Frenet" property controls how the profile orientation changes as it follows along the sweep path.
# If "Frenet" is "false", the orientation of the profile is kept consistent from point to point. 
# The resulting shape has the minimum possible twisting. Unintuitively, when a profile is swept along a helix,
# this results in the orientation of the profile slowly creep (rotate) as it follows the helix.
# Setting "Frenet" to true prevents such a creep.
helix_1.Frenet=True

# Recompute the document
App.getDocument('coil').recompute()

raw_input ('Inner Sweep complete : Press enter to continue')

###############################################################################
# Create profile of the wire to be swept along the helix_2_spine created above

#Activate Sketcher Workbench
Gui.activateWorkbench("SketcherWorkbench")

# Create Sketch object and place it at one end of helix_2_spine
helix_2_profile = App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
helix_2_profile.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))

# Open helix_2_profile sketch in edit mode
Gui.activeDocument().setEdit(helix_2_profile.Name)

# Create a circular profile for the wire
helix_2_profile.addGeometry(Part.Circle(App.Vector(1.286811,-0.212345,0),App.Vector(0,0,1),0.158677))

# Fix Radius
helix_2_profile.addConstraint(Sketcher.Constraint('Radius',0,wire_radius)) 

# Set positional constraints
helix_2_profile.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,0.00)) 
helix_2_profile.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,core_radius + 3*wire_radius + gap)) 

# Exit edit mode and recompute
Gui.getDocument('coil').resetEdit()
App.getDocument('coil').recompute()

#############################################
#Sweep helix 1 with helix_1_profile sketch

# Activate Part Workbench
Gui.activateWorkbench("PartWorkbench")

helix_2 = App.getDocument('coil').addObject('Part::Sweep','Sweep')

# Select the cross-sectional profile to sweep
helix_2.Sections=[helix_2_profile, ]

# Select the spine along which to sweep
helix_2.Spine=(helix_2_spine,[])

# Set Solid and Frenet properties to "True"
helix_2.Solid =True
helix_2.Frenet=True

# Recompute the document
App.getDocument('coil').recompute()

raw_input ('Outer Sweep complete : Press enter to continue')

###############################################################################

#Activate Sketcher Workbench
Gui.activateWorkbench("SketcherWorkbench")

# Create Sketch object and place it at one end of spiral_1_spine
spiral_1_profile = App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
spiral_1_profile.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))

# Open spiral_1_profile sketch in edit mode
Gui.activeDocument().setEdit(spiral_1_profile.Name)

# Create a circular profile for the wire
spiral_1_profile.addGeometry(Part.Circle(App.Vector(1.286811,0.212345,0),App.Vector(0,0,1),0.158677))

# Fix radius
spiral_1_profile.addConstraint(Sketcher.Constraint('Radius',0,wire_radius)) 

# Set positional constraints
spiral_1_profile.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,coil_height)) 
spiral_1_profile.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,core_radius + wire_radius + gap)) 

# Exit edit mode and recompute
Gui.getDocument('coil').resetEdit()
App.getDocument('coil').recompute()

#############################################
# Sweep spiral with spiral_1_profile

# Activate Part Workbench
Gui.activateWorkbench("PartWorkbench")

spiral_1 = App.getDocument('coil').addObject('Part::Sweep','Sweep')

# Select the cross-sectional profile to sweep
spiral_1.Sections=[spiral_1_profile, ]

# Select the spine along which to sweep
spiral_1.Spine=(spiral_1_spine,[])

# Setting Solid and Frenet properties to "True"
spiral_1.Solid=True
spiral_1.Frenet=True

# Recompute the document
App.getDocument('coil').recompute()

# Set spines to be invisible
Gui.getDocument('coil').getObject("Helix").Visibility=False
Gui.getDocument('coil').getObject("Spiral").Visibility=False
Gui.getDocument('coil').getObject("Helix001").Visibility=False

# Set sketches to be invisible
Gui.getDocument('coil').getObject("Sketch").Visibility=False
Gui.getDocument('coil').getObject("Sketch001").Visibility=False
Gui.getDocument('coil').getObject("Sketch002").Visibility=False

# Convert all separate objects into one compund object
Gui.activateWorkbench("PartWorkbench")
App.activeDocument().addObject("Part::Compound","Compound")
App.activeDocument().Compound.Links = [helix_1, helix_2, spiral_1,]
App.ActiveDocument.recompute()
