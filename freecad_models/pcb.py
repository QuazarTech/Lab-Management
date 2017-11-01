########################################################################################
########################################################################################
# Dimensions in mm

pcb_entry_half_width  = 10
pcb_outer_half_width  = 25
pcb_connecter_length  = 20
pcb_total_length      = 90
pcb_thickness         = 3
hole_radius           = 4

App.ActiveDocument = App.getDocument('py_pcb')
Gui.ActiveDocument = Gui.getDocument('py_pcb')
App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(0,0,0,1))
Gui.activeDocument().setEdit('Sketch')

# The Base Sketch
########################################################################################
########################################################################################

# The vertical line that represents the part of the pcb that is going to be inserted
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector\
	(0,pcb_entry_half_width,0),App.Vector(0,-pcb_entry_half_width,0)),False)

App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-2)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-2)) 

# The horizontal "bridge" lines that connect the edge to the sample platform
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector\
	(0,pcb_entry_half_width,0),App.Vector(pcb_connecter_length,pcb_entry_half_width,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,1)) 

# The parallel horizontal line to the above, and a constraint to ensure that the two lines 
# are exactly the same, only parallely shifted
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector\
	(0.000000,-pcb_entry_half_width,0),App.Vector(pcb_connecter_length,-pcb_entry_half_width,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,0,2)) 

# Vertical Shoulder Lines
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector\
	(pcb_connecter_length,pcb_entry_half_width,0),App.Vector(pcb_connecter_length,pcb_outer_half_width,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,1,2)) 
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector\
	(pcb_connecter_length,-pcb_entry_half_width,0),App.Vector(pcb_connecter_length,-pcb_outer_half_width,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4,1,2,2)) 

# Creating the sides of the sample platform, and constraining them so that they are of the same length
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector\
	(pcb_connecter_length,pcb_outer_half_width,0),App.Vector(pcb_total_length,pcb_outer_half_width,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',5,1,3,2)) 
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector\
	(pcb_connecter_length,-pcb_outer_half_width,0),App.Vector(pcb_total_length,-pcb_outer_half_width,0)),False)

# The other end of the PCB, the one at the base.
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector\
	(pcb_total_length,pcb_outer_half_width,0),App.Vector(pcb_total_length,-pcb_outer_half_width,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',7,1,5,2)) 
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',7,2,6,2))
Gui.getDocument('py_pcb').resetEdit()
App.getDocument('py_pcb').recompute()

# Extrusion
########################################################################################
########################################################################################

FreeCAD.getDocument("py_pcb").addObject("Part::Extrusion","Extrude")
FreeCAD.getDocument("py_pcb").Extrude.Base       = FreeCAD.getDocument("py_pcb").Sketch
FreeCAD.getDocument("py_pcb").Extrude.Dir        = (0,0,pcb_thickness)
FreeCAD.getDocument("py_pcb").Extrude.Solid      = (True)
FreeCAD.getDocument("py_pcb").Extrude.TaperAngle = (0)
FreeCADGui.getDocument("py_pcb").Sketch.Visibility  = False
FreeCAD.getDocument("py_pcb").Extrude.Label      = 'Extrude'

Gui.ActiveDocument.Extrude.ShapeColor = Gui.ActiveDocument.Sketch.ShapeColor
Gui.ActiveDocument.Extrude.LineColor  = Gui.ActiveDocument.Sketch.LineColor
Gui.ActiveDocument.Extrude.PointColor = Gui.ActiveDocument.Sketch.PointColor

########################################################################################
########################################################################################
# Making Screw Holes

App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
App.activeDocument().Sketch002.Support = (App.ActiveDocument.Extrude,["Face9"])
App.activeDocument().recompute()
Gui.activeDocument().setEdit('Sketch002')

App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(25,15,0),App.Vector(0,0,1),4),False)
App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(25,-15,0),App.Vector(0,0,1),4),False)
App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(85,-15,0),App.Vector(0,0,1),4),False)
App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(85,15,0),App.Vector(0,0,1),4),False)

Gui.getDocument('py_pcb').resetEdit()
App.getDocument('py_pcb').recompute()

# Negative Extrusion for the Holes

App.activeDocument().addObject("PartDesign::Pocket","Pocket")
App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch002
Gui.activeDocument().setEdit('Pocket',0)
App.ActiveDocument.Pocket.Length = 3.000000
App.ActiveDocument.Pocket.Type = 0
App.ActiveDocument.Pocket.UpToFace = None
App.ActiveDocument.recompute()
Gui.activeDocument().resetEdit()
Gui.getDocument("py_pcb").getObject("Sketch002").Visibility=False

########################################################################################
########################################################################################
# Making the PCB connecting terminals sketch

App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
App.activeDocument().Sketch003.Support = (App.ActiveDocument.Pocket,["Face4"])
App.activeDocument().recompute()
Gui.activeDocument().setEdit('Sketch003')

# The first terminal, essentially four lines
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(0,8,0),App.Vector(8,8,0)),False) 
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(8,8,0),App.Vector(8,6,0)),False)
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(8,6,0),App.Vector(0,6,0)),False)
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(0,6,0),App.Vector(0,8,0)),False)

# The copy of these lines, but shifted, to form the other three terminals
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(0,4,0),App.Vector(8,4,0)),False) 
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(8,4,0),App.Vector(8,2,0)),False)
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(8,2,0),App.Vector(0,2,0)),False)
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(0,2,0),App.Vector(0,4,0)),False)

#-------

App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(0,-2,0),App.Vector(8,-2,0)),False)
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(8,-2,0),App.Vector(8,-4,0)),False)
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(8,-4,0),App.Vector(0,-4,0)),False)
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(0,-4,0),App.Vector(0,-2,0)),False)

#------

App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(0,-6,0),App.Vector(8,-6,0)),False) 
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(8,-6,0),App.Vector(8,-8,0)),False)
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(8,-8,0),App.Vector(0,-8,0)),False)
App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(0,-8,0),App.Vector(0,-6,0)),False)


Gui.getDocument('py_pcb').resetEdit()
App.getDocument('py_pcb').recompute()

########################################################################################
########################################################################################
# Extrude the sketch to make the terminals

FreeCAD.getDocument("py_pcb").addObject("Part::Extrusion","Extrude001")
FreeCAD.getDocument("py_pcb").Extrude001.Base         = FreeCAD.getDocument("py_pcb").Sketch003
FreeCAD.getDocument("py_pcb").Extrude001.Dir          = (0,0,-1)
FreeCAD.getDocument("py_pcb").Extrude001.Solid        = (True)
FreeCAD.getDocument("py_pcb").Extrude001.TaperAngle   = (0)
FreeCADGui.getDocument("py_pcb").Sketch003.Visibility = False
FreeCAD.getDocument("py_pcb").Extrude001.Label        = 'Extrude001'

Gui.ActiveDocument.Extrude001.ShapeColor = Gui.ActiveDocument.Sketch003.ShapeColor
Gui.ActiveDocument.Extrude001.LineColor  = Gui.ActiveDocument.Sketch003.LineColor
Gui.ActiveDocument.Extrude001.PointColor = Gui.ActiveDocument.Sketch003.PointColor

########################################################################################
########################################################################################
# Making the pathway/groove for laying the copper wire

# Making the sketch
App.activeDocument().addObject('Sketcher::SketchObject','Sketch004')
App.activeDocument().Sketch004.Support = (App.ActiveDocument.Pocket,["Face4"])
App.activeDocument().recompute()
Gui.activeDocument().setEdit('Sketch004')
App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(30,19,0),App.Vector(30,-19,0)),False)
App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(30,-19,0),App.Vector(57,-19,0)),False)
App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(57,-19,0),App.Vector(57,17,0)),False)
App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(57,17,0),App.Vector(78,17,0)),False)
App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(78,17,0),App.Vector(78,-19,0)),False)
App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(78,-19,0),App.Vector(80,-19,0)),False)
App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(80,-19,0),App.Vector(80,19,0)),False)
App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(80,19,0),App.Vector(55,19,0)),False)
App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(55,19,0),App.Vector(55,-17,0)),False)
App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(55,-17,0),App.Vector(32,-17,0)),False)
App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(32,-17,0),App.Vector(32,19,0)),False)
App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(32,19,0),App.Vector(30,19,0)),False)
App.activeDocument().recompute()
Gui.activeDocument().resetEdit()

#
App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch004
App.activeDocument().Pocket001.Length = 0.5
App.ActiveDocument.recompute()

########################################################################################
########################################################################################
# Making the foam layer base sketch

App.activeDocument().addObject('Sketcher::SketchObject','Sketch005')
App.activeDocument().Sketch005.Support = (App.ActiveDocument.Pocket001,["Face4"])
App.activeDocument().recompute()
Gui.activeDocument().setEdit('Sketch005')

geoList = []
geoList.append(Part.Line(App.Vector(20,25,0),App.Vector(90,25,0)))
geoList.append(Part.Line(App.Vector(90,25,0),App.Vector(90,-25,0)))
geoList.append(Part.Line(App.Vector(90,-25,0),App.Vector(20,-25,0)))
geoList.append(Part.Line(App.Vector(20,-25,0),App.Vector(20, 25,0)))
App.ActiveDocument.Sketch005.addGeometry(geoList,False)

App.activeDocument().recompute()
Gui.activeDocument().resetEdit()

########################################################################################
########################################################################################
# Merging the screw hole sketch, the copper groove sketch and the above sketch 
# so that it can be extruded together to form the foam layer

