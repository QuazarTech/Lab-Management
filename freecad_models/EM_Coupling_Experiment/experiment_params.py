###############################################################################
# This script contains the user Input Parameters for the EM coupling experiment
# CAD model. Changing a parameter here, and executing the other python files in
# this folder inside FreeCAD will create the parts with the modifier parameters.
###############################################################################

#####################
## Core Parameters
core_radius      = 10.0 #mm
core_height      = 40.0 #mm

# Core-Coil Winding Machine Mount Parameters
top_height       = 5.00 #mm
base_height      = 15.0 #mm
base_cut         = 10.0 #mm
coil_thickness   = 5.00 #mm

# Core-Experimental Setup Mount Parameters
hole_diameter    = 8.50 #mm
thread_pitch     = 1.50 #mm
chamfer_length   = 4.00 #mm

#####################
## Coil Parameters
wire_radius      = 0.711/2                         # SWG 27 -> wire_radius = 0.711/2
gap              = 0.00                            #mm  
coil_height      = core_height                     # Coil height will be modified slightly to accomodate an integral number of turns
coil_radius      = core_radius + wire_radius + gap # This is the radius of the inner most helix of the coil

#####################
## Cover Parameters
top_flange_width = 10.0 #mm
side_margin      = 25.0 #mm
length_margin    = 25.0 #mm

sheet_thickness  = 2.00 #mm
bend_radius      = 1.00 #mm
screw_diameter   = 2.00 #mm
screw_length     = 10.0 #mm

#Coaxial connector parameters
coax_side_distance   = 5.00 #mm
coax_bottom_distance = 55.0 #mm
coax_base_width      = 5.75 #mm
coax_radius          = 4.90 #mm

###############################################
## Calculated Parameters

total_core_height = base_height + core_height + top_height

base_width  = 2*(core_radius + side_margin)
base_length = 2*(total_core_height + length_margin)
wall_height = 2*(core_radius + side_margin)