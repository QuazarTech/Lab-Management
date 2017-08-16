###############################################################################
# This script contains the user Input Parameters for the EM coupling experiment
# CAD model. Changing a parameter here, and executing the other python files in
# this folder inside FreeCAD will create the parts with the modifier parameters.
###############################################################################

epsilon          = 0.50 #mm                        # Small parameter, tolerance of manufacturing

#####################
## Core Parameters
core_radius      = 10.0 #mm                        # Radius of core's cylinder on which coil will be wound
core_height      = 40.0 #mm                        # Height of core's cylinder on which coil will be wound

# Core-Coil Winding Machine Mount Parameters
top_height       = 5.00 #mm                        # Height of core top cylinder
base_height      = 15.0 #mm                        # Height of core base cylinder
base_cut         = 10.0 #mm                        # Length of grip cut in the core base
coil_thickness   = 5.00 #mm                        # Thickness of the coil with some margin

# Core-Experimental Setup Mount Parameters
hole_diameter    = 8.50 #mm                        # Diameter of hole in cores, diameter of mounting rod
thread_pitch     = 1.50 #mm                        # Pitch of inner thread
chamfer_length   = 4.00 #mm                        # Actual Chamfer length will be chamfer_length - epsilon

#####################
## Coil Parameters
wire_radius      = 0.711/2                         # SWG 27 -> wire_radius = 0.711/2
gap              = 0.00 #mm                        # Gap between consecutive helix turns, and consecutive helices
coil_height      = core_height                     # Coil height will be modified slightly to accomodate an integral number of turns
coil_radius      = core_radius + wire_radius + gap # This is the radius of the inner most helix of the coil

#####################
## Cover Parameters
top_flange_width = 10.0 #mm
side_margin      = 25.0 #mm                       # Margin from side flange of cover accomodate wiring and connectors
length_margin    = 25.0 #mm                       # Margin for relative movement of cores

sheet_thickness  = 2.00 #mm                       # Sheet metal thickness
bend_radius      = 1.00 #mm                       # Sheet metal bend radius
screw_diameter   = 4.50 #mm                       # Diameter of screw used
screw_length     = 10.0 #mm                       # Length of screw used
csk_diameter     = 5.00 #mm                       # Diameter of Countersunk screw
csk_chamfer      = 1.00 #mm                       # Chamfer length of Countersunk screw

#Coaxial connector parameters
coax_side_distance   = 5.00 #mm                   # Distance of coax connector from the side flange of cover
coax_bottom_distance = 55.0 #mm                   # Distance of coax connector from the base flange of cover
coax_base_width      = 5.75 #mm                   # Base Length of coax cable connector
coax_radius          = 4.90 #mm                   # Radius of coax cable connector

###############################################
## Calculated Parameters

total_core_height = base_height + core_height + top_height  # Total height of the complete core

base_width  = 2*(core_radius + side_margin)                 # Width of cover
base_length = 2*(total_core_height + length_margin)         # Length of cover
wall_height = 2*(core_radius + side_margin)                 # Height of cover