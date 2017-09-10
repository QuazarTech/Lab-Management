# Lab-Management Animation Primitives
#
# This program contains primitives required for performing any step in Lab-Management.

import functools
import numpy as np
import FreeCAD
import time
from PySide import QtCore

# Define a timer object which will have a particular timeout
timer = QtCore.QTimer()

########################################################################################
########################################################################################
# Move Functions

def get_current_position(obj):

	p = FreeCAD.ActiveDocument.getObject(obj).Placement.Base
	return p.x, p.y, p.z

def change_position(new_pos, obj):

	new_x, new_y, new_z = new_pos
	FreeCAD.ActiveDocument.getObject(obj).Placement.Base.x = new_x
	FreeCAD.ActiveDocument.getObject(obj).Placement.Base.y = new_y
	FreeCAD.ActiveDocument.getObject(obj).Placement.Base.z = new_z

def update_position(initParams):

	obj    , unit, final_pos    = initParams
	unit_x , unit_y , unit_z    = unit
	x_final, y_final, z_final   = final_pos
	x      , y      , z         = get_current_position(obj)

	if np.abs(x - x_final) < 0.01 \
	and np.abs(y - y_final) < 0.01 \
	and np.abs(z - z_final) < 0.01:
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

def move():
	obj       = raw_input("Enter the object you wanna move in this Active Document:\n")
	samples   = raw_input("Enter the unit steps to move:\n")
	final_x   = raw_input("Enter the final x:\n")
	final_y   = raw_input("Enter the final y:\n")
	final_z   = raw_input("Enter the final z:\n")

	final_pos = (float(final_x), float(final_y), float(final_z))
	units     = get_units(obj, final_pos ,float(samples))

	initParams    = (obj , units , final_pos)
	timerCallback = functools.partial(update_position, initParams)
	timer.timeout.connect(timerCallback)
	timer.start(1)

########################################################################################
########################################################################################
#Rotation Functions

def euler2Quaternion(roll_x, yaw_z, pitch_y):
	a = np.cos(roll_x/2)*np.cos(pitch_y/2)*np.cos(yaw_z/2) + np.sin(roll_x/2)*np.sin(pitch_y/2)*np.sin(yaw_z/2)
	b = np.sin(roll_x/2)*np.cos(pitch_y/2)*np.cos(yaw_z/2) - np.cos(roll_x/2)*np.sin(pitch_y/2)*np.sin(yaw_z/2)
	c = np.cos(roll_x/2)*np.sin(pitch_y/2)*np.cos(yaw_z/2) + np.sin(roll_x/2)*np.cos(pitch_y/2)*np.sin(yaw_z/2)
	d = np.cos(roll_x/2)*np.cos(pitch_y/2)*np.sin(yaw_z/2) - np.sin(roll_x/2)*np.sin(pitch_y/2)*np.cos(yaw_z/2)
	return (a, b, c, d)

def get_current_euler_angles(obj):
	p = FreeCAD.ActiveDocument.getObject(obj).Placement.Rotation
	return p.toEuler()

def rotate_along_direction (obj, roll_x, yaw_z, pitch_y):
	quaternion = euler2Quaternion(roll_x, yaw_z, pitch_y)
	FreeCAD.ActiveDocument.getObject(obj).Placement.Rotation.Q = quaternion

def update_rotation (initParams):
	obj, final_angles, unit                  = initParams
	yaw_current, pitch_current, roll_current = get_current_euler_angles(obj)
	unit_roll, unit_pitch, unit_yaw          = unit
	roll_x, yaw_z, pitch_y                   = final_angles

	if  np.abs(yaw_current   - yaw_z  ) < 0.01 \
	and np.abs(roll_current  - roll_x ) < 0.01 \
	and np.abs(pitch_current - pitch_y) < 0.01:
		timer.stop()

	rotate_along_direction(obj, roll_current  + unit_roll, yaw_current + unit_yaw, pitch_current + unit_pitch)


def get_units_rotation(obj, samples, final_angles):
	yaw_current, pitch_current, roll_current = get_current_euler_angles(obj)
	roll_x, yaw_z, pitch_y                   = final_angles

	unit_roll  = (roll_x  - roll_current) /samples
	unit_yaw   = (yaw_z   - yaw_current ) /samples
	unit_pitch = (pitch_y - pitch_current)/samples    

	return (unit_roll, unit_pitch, unit_yaw)

def rotate():
	obj        = raw_input("Enter the object you wanna move in this Active Document:\n")
	x_rotation = raw_input("Enter the x rotation (roll):\n")
	y_rotation = raw_input("Enter the y rotation (pitch):\n")
	z_rotation = raw_input("Enter the z rotation (yaw):\n")
	samples    = raw_input("Enter the no of steps:\n")

	final_angles = (float(x_rotation), float(z_rotation), float(y_rotation))
	unit    = get_units_rotation(obj, float(samples), final_angles)
	initParams = (obj, final_angles, unit)
	timerCallback = functools.partial(update_rotation, initParams)
	timer.timeout.connect(timerCallback)
	timer.start(1)

rotate()
