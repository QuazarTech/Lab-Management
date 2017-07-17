import WebGui
from StartPage import StartPage

from FreeCAD import Base
import Part,PartGui

WebGui.openBrowserHTML(StartPage.handle(),'file://' + App.getResourceDir() + 'Mod/Start/StartPage/','Start page')
App.newDocument("Unnamed")
App.setActiveDocument("Unnamed")
App.ActiveDocument=App.getDocument("Unnamed")
Gui.ActiveDocument=Gui.getDocument("Unnamed")

#User Input Parameters
wire_radius = 0.10
core_height = 10.00
core_radius = 5.00
gap         = 0.01

###############################################################################
#Create Hlical Structures joined by spiral structures

#Activate aPart Workbench
Gui.activateWorkbench("PartWorkbench")

# Innermost helix parameters
App.ActiveDocument.addObject("Part::Helix","Helix")
App.ActiveDocument.Helix.Pitch  = 1 * wire_radius
App.ActiveDocument.Helix.Height = core_height/2
App.ActiveDocument.Helix.Radius = core_radius + wire_radius + gap
App.ActiveDocument.Helix.Angle  = 0.00
App.ActiveDocument.Helix.LocalCoord = 0 #Helix direction
App.ActiveDocument.Helix.Style      = 1 #Don't Know what this does
App.ActiveDocument.Helix.Placement=Base.Placement(Base.Vector(0.00,0.00,0.00),Base.Rotation(0.00,0.00,0.00,1.00))
App.ActiveDocument.Helix.Label='Helix'

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

#Spiral to seamlessly join the inner and outer coils
App.ActiveDocument.addObject("Part::Spiral","Spiral")
App.ActiveDocument.Spiral.Growth    = 2*wire_radius
App.ActiveDocument.Spiral.Rotations = 1.00
App.ActiveDocument.Spiral.Radius    = core_radius + wire_radius + gap
App.ActiveDocument.Spiral.Placement=Base.Placement(Base.Vector(0.00,0.00,5.00),Base.Rotation(0.00,0.00,0.00,1.00))
App.ActiveDocument.Spiral.Label='Spiral'

App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

#2nd from innermost helix parameters
App.ActiveDocument.addObject("Part::Helix","Helix001")
App.ActiveDocument.Helix001.Pitch  = 1 * wire_radius
App.ActiveDocument.Helix001.Height = core_height/2
App.ActiveDocument.Helix001.Radius = core_radius + (3*wire_radius) + gap
App.ActiveDocument.Helix001.Angle  = 0.00
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

Gui.getDocument('Unnamed').resetEdit()
App.getDocument('Unnamed').recompute()

#Sweep helix 1 with Sketch
Gui.activateWorkbench("PartWorkbench")

App.getDocument('Unnamed').addObject('Part::Sweep','Sweep')
App.getDocument('Unnamed').ActiveObject.Sections=[App.getDocument('Unnamed').Sketch, ]

spine = []

App.getDocument('Unnamed').ActiveObject.Spine=(App.ActiveDocument.Helix,[])
App.getDocument('Unnamed').ActiveObject.Solid=False
App.getDocument('Unnamed').ActiveObject.Frenet=True
App.getDocument('Unnamed').recompute()

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

Gui.getDocument('Unnamed').resetEdit()
App.getDocument('Unnamed').recompute()

#Sweep helix 2 with Sketch
Gui.activateWorkbench("PartWorkbench")

App.getDocument('Unnamed').addObject('Part::Sweep','Sweep')
App.getDocument('Unnamed').ActiveObject.Sections=[App.getDocument('Unnamed').Sketch001, ]
App.getDocument('Unnamed').ActiveObject.Spine=(App.ActiveDocument.Helix001,[])
App.getDocument('Unnamed').ActiveObject.Solid=False
App.getDocument('Unnamed').ActiveObject.Frenet=True
App.getDocument('Unnamed').recompute()

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

App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,core_height/2)) 
App.ActiveDocument.recompute()

App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,core_radius + wire_radius + gap)) 
App.ActiveDocument.recompute()

Gui.getDocument('Unnamed').resetEdit()
App.getDocument('Unnamed').recompute()

#sweep spiral with sketch
App.getDocument('Unnamed').addObject('Part::Sweep','Sweep')
App.getDocument('Unnamed').ActiveObject.Sections=[App.getDocument('Unnamed').Sketch002, ]
App.getDocument('Unnamed').ActiveObject.Spine=(App.ActiveDocument.Spiral,[])
App.getDocument('Unnamed').ActiveObject.Solid=False
App.getDocument('Unnamed').ActiveObject.Frenet=True

App.getDocument('Unnamed').recompute()

