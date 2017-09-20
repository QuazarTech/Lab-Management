# Lab-Management Animation Primitives
#
# This program contains primitives required for performing any step in Lab-Management.


# Modules necessary for operation
import sys
import numpy as np
import FreeCAD
import functools
from PySide import QtCore

timer   = QtCore.QTimer()
timer_1 = QtCore.QTimer()
# Define a timer object which will have a particular timeout

# The no of animation steps, currently set at 200
SAMPLES = "200"

########################################################################################
########################################################################################
# Move Functions

def get_current_position(obj):

	p = FreeCAD.ActiveDocument.getObjectsByLabel(obj)[0].Placement.Base
	return p.x, p.y, p.z

def change_position(new_pos, obj):

	new_x, new_y, new_z = new_pos
	FreeCAD.ActiveDocument.getObjectsByLabel(obj)[0].Placement.Base.x = new_x
	FreeCAD.ActiveDocument.getObjectsByLabel(obj)[0].Placement.Base.y = new_y
	FreeCAD.ActiveDocument.getObjectsByLabel(obj)[0].Placement.Base.z = new_z

def update_position(initParams):

	obj    , unit, final_pos    = initParams
	unit_x , unit_y , unit_z    = unit
	x_final, y_final, z_final   = final_pos
	x      , y      , z         = get_current_position(obj)

	if np.abs(x - x_final) < 0.1 and np.abs(y - y_final) < 0.1 and np.abs(z - z_final) < 0.1:
		timer.stop()

	change_position(( x + unit_x ,\
	                  y + unit_y , \
	                  z + unit_z ), obj)


def get_units(obj, final_pos, samples):

	x_final, y_final, z_final = final_pos
	x, y, z = get_current_position(obj)

	unit = ((x_final - x)/samples,\
		    (y_final - y)/samples,\
		    (z_final - z)/samples)

	return unit

def translate(obj, final_x, final_y, final_z, samples):

	
	x_current, y_current, z_current = get_current_position(obj)

	final_pos = (float(final_x), float(final_y), float(final_z))
	units     = get_units(obj, final_pos ,float(samples))

	initParams    = (obj , units , final_pos)
	timerCallback = functools.partial(update_position, initParams)
	timer.timeout.connect(timerCallback)
	timer.start(1)

########################################################################################
########################################################################################
#Rotation Functions

def get_current_euler_angles(obj):
	p = FreeCAD.ActiveDocument.getObjectsByLabel(obj)[0].Placement.Rotation
	return p.toEuler()

def rotate_along_direction (obj, roll_x, yaw_z, pitch_y):
	rot = FreeCAD.Rotation(yaw_z, pitch_y, roll_x)
	FreeCAD.ActiveDocument.getObjectsByLabel(obj)[0].Placement.Rotation = rot

def update_rotation (initParams):
	obj, final_angles, unit                  = initParams
	yaw_current, pitch_current, roll_current = get_current_euler_angles(obj)
	unit_roll, unit_pitch, unit_yaw          = unit
	roll_x, yaw_z, pitch_y                   = final_angles

	if np.abs(roll_current  - roll_x ) < 0.1 and np.abs(yaw_current - yaw_z) < 0.1 and np.abs(roll_current - roll_x) < 0.1:
		timer_1.stop()
	
	rotate_along_direction(obj, (roll_current  + unit_roll),\
	 (yaw_current + unit_yaw), (pitch_current + unit_pitch))


def get_units_rotation(obj, samples, final_angles):
	yaw_current, pitch_current, roll_current = get_current_euler_angles(obj)
	roll_x, yaw_z, pitch_y                   = final_angles

	if np.abs(roll_x - roll_current) < 0.01:
		roll_x = roll_current
	if np.abs(yaw_z - yaw_current) < 0.01:
		yaw_z  = yaw_current
	if np.abs(pitch_y - pitch_current) < 0.01:
		pitch_y = pitch_current
				
	unit_roll  = ((roll_x  - roll_current)) /samples
	unit_yaw   = ((yaw_z   - yaw_current)) /samples
	unit_pitch = ((pitch_y - pitch_current))/samples    

	return (unit_roll, unit_pitch, unit_yaw)

def rotate(obj, x_rotation, y_rotation, z_rotation, samples):

	
	final_angles = (float(x_rotation), float(z_rotation), float(y_rotation))
	unit    = get_units_rotation(obj, float(samples), final_angles)
	initParams = (obj, final_angles, unit)
	timerCallback = functools.partial(update_rotation, initParams)
	timer_1.timeout.connect(timerCallback)
	timer_1.start(1)

########################################################################################
########################################################################################