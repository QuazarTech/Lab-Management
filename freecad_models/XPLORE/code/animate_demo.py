import FreeCAD
import time
from PySide import QtCore

i = 55

def insert_update():
	global i
	FreeCAD.getDocument("pqms").getObject("MGPS_Insert_01").Placement = \
	App.Placement(App.Vector(89.05,-906.513,i),App.Rotation(App.Vector(0.99974,-1.94442e-16,-0.0227888),92.2714))
	i += 10
	if i >= 540:
		timer.stop()

timer = QtCore.QTimer()
timer.timeout.connect(insert_update)
timer.start(1)