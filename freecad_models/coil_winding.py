import math

from FreeCAD import Base
import Part,PartGui

import sys
sys.path.insert(0, "${HOME}/Downloads/susceptibility_experiment/code")

from experiment_params import *

App.newDocument('coil')
App.setActiveDocument('coil')
App.ActiveDocument=App.getDocument('coil')
Gui.ActiveDocument=Gui.getDocument('coil')

###############################################################################
#Modification of core_height to an integral number of turns

conversion_factor = math.floor((core_height)/(2*wire_radius)) #Integral number of turns that can be accomodated in each coil
coil_height = conversion_factor * (2*wire_radius)

###############################################################################
#Create Helical Structures joined by spiral structures

#Activate aPart Workbench
Gui.activateWorkbench("PartWorkbench")

# Innermost helix parameters
App.ActiveDocument.addObject("Part::Helix","Helix")
App.ActiveDocument.Helix.Pitch      = 2 * (wire_radius + gap)
App.ActiveDocument.Helix.Height     = coil_height
App.ActiveDocument.Helix.Radius     = coil_radius
App.ActiveDocument.Helix.Angle      = 0.00
App.ActiveDocument.Helix.LocalCoord = 0 #Helix direction
App.ActiveDocument.Helix.Style      = 1 #Don't Know what this does
App.ActiveDocument.Helix.Placement  = Base.Placement(Base.Vector(0.00,0.00,0.00),Base.Rotation(0.00,0.00,0.00,1.00))
App.ActiveDocument.Helix.Label      = 'Helix'

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

#Spiral to seamlessly join the inner and outer coils
App.ActiveDocument.addObject("Part::Spiral","Spiral")
App.ActiveDocument.Spiral.Growth    = 2*(wire_radius + gap)
App.ActiveDocument.Spiral.Rotations = 1.00
App.ActiveDocument.Spiral.Radius    = coil_radius
App.ActiveDocument.Spiral.Placement = Base.Placement(Base.Vector(0.00,0.00,coil_height),Base.Rotation(0.00,0.00,0.00,1.00))
App.ActiveDocument.Spiral.Label     = 'Spiral'

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

#2nd from innermost helix parameters
App.ActiveDocument.addObject("Part::Helix","Helix001")
App.ActiveDocument.Helix001.Pitch      = 2 * (wire_radius + gap)
App.ActiveDocument.Helix001.Height     = coil_height
App.ActiveDocument.Helix001.Radius     = coil_radius + 1*(wire_radius + gap)
App.ActiveDocument.Helix001.Angle      = 0.00
App.ActiveDocument.Helix001.LocalCoord = 1 #Helix direction
App.ActiveDocument.Helix001.Style      = 1 #Don't Know what this does
App.ActiveDocument.Helix001.Placement=Base.Placement(Base.Vector(0.00,0.00,0.00),Base.Rotation(0.00,0.00,0.00,1.00))
App.ActiveDocument.Helix001.Label='Helix'

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

###############################################################################
raw_input ('Joined Helixes complete : Press enter to continue')

#Activate Sketcher Workbench to make sweep sketch
Gui.activateWorkbench("SketcherWorkbench")
App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))
Gui.activeDocument().setEdit('Sketch')

App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(1.286811,-0.212345,0),App.Vector(0,0,1),0.158677))
App.ActiveDocument.recompute()

App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',0,wire_radius)) 
App.ActiveDocument.recompute()

App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,0.00)) 
App.ActiveDocument.recompute()

App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,core_radius + wire_radius + gap)) 
App.ActiveDocument.recompute()

Gui.getDocument('coil').resetEdit()
App.getDocument('coil').recompute()

#Sweep helix 1 with Sketch
Gui.activateWorkbench("PartWorkbench")

App.getDocument('coil').addObject('Part::Sweep','Sweep')
App.getDocument('coil').ActiveObject.Sections=[App.getDocument('coil').Sketch, ]

App.getDocument('coil').ActiveObject.Spine=(App.ActiveDocument.Helix,[])
App.getDocument('coil').ActiveObject.Solid=True
App.getDocument('coil').ActiveObject.Frenet=True
App.getDocument('coil').recompute()

raw_input ('Inner Sweep complete : Press enter to continue')
###############################################################################

#Activate Sketcher Workbench to make sweep sketch
Gui.activateWorkbench("SketcherWorkbench")
App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
App.activeDocument().Sketch001.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))
Gui.activeDocument().setEdit('Sketch001')

App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(1.286811,-0.212345,0),App.Vector(0,0,1),0.158677))
App.ActiveDocument.recompute()

App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',0,wire_radius)) 
App.ActiveDocument.recompute()

App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,0.00)) 
App.ActiveDocument.recompute()

App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,core_radius + 3*wire_radius + gap)) 
App.ActiveDocument.recompute()

Gui.getDocument('coil').resetEdit()
App.getDocument('coil').recompute()

#Sweep helix 2 with Sketch
Gui.activateWorkbench("PartWorkbench")

App.getDocument('coil').addObject('Part::Sweep','Sweep')
App.getDocument('coil').ActiveObject.Sections=[App.getDocument('coil').Sketch001, ]
App.getDocument('coil').ActiveObject.Spine=(App.ActiveDocument.Helix001,[])
App.getDocument('coil').ActiveObject.Solid =True
App.getDocument('coil').ActiveObject.Frenet=True
App.getDocument('coil').recompute()

raw_input ('Outer Sweep complete : Press enter to continue')

###############################################################################

#Activate Sketcher Workbench to make sweep sketch
Gui.activateWorkbench("SketcherWorkbench")
App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
App.activeDocument().Sketch002.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))
Gui.activeDocument().setEdit('Sketch002')

App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(1.286811,0.212345,0),App.Vector(0,0,1),0.158677))
App.ActiveDocument.recompute()

App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',0,wire_radius)) 
App.ActiveDocument.recompute()

App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,coil_height)) 
App.ActiveDocument.recompute()

App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,core_radius + wire_radius + gap)) 
App.ActiveDocument.recompute()

Gui.getDocument('coil').resetEdit()
App.getDocument('coil').recompute()

#sweep spiral with sketch
App.getDocument('coil').addObject('Part::Sweep','Sweep')
App.getDocument('coil').ActiveObject.Sections=[App.getDocument('coil').Sketch002, ]
App.getDocument('coil').ActiveObject.Spine=(App.ActiveDocument.Spiral,[])
App.getDocument('coil').ActiveObject.Solid=True
App.getDocument('coil').ActiveObject.Frenet=True

App.getDocument('coil').recompute()

# Set sketches to be invisible
Gui.getDocument('coil').getObject("Helix").Visibility=False
Gui.getDocument('coil').getObject("Spiral").Visibility=False
Gui.getDocument('coil').getObject("Helix001").Visibility=False

Gui.getDocument('coil').getObject("Sketch").Visibility=False
Gui.getDocument('coil').getObject("Sketch001").Visibility=False
Gui.getDocument('coil').getObject("Sketch002").Visibility=False

# Convert all separate objects into one compund object
Gui.activateWorkbench("PartWorkbench")
App.activeDocument().addObject("Part::Compound","Compound")
App.activeDocument().Compound.Links = [App.activeDocument().Sweep,App.activeDocument().Sweep001,App.activeDocument().Sweep002,]
App.ActiveDocument.recompute()
