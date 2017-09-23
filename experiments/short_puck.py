from complex_functions import *
from wrapper_functions import *

name = "short_puck"

##########################################################################

def run():

    #Select the test object and sample
    Sample = "copper_wire"
    Sample_Box = "Dessicator"
    test_object = select_test_object()

    wire_length = float(raw_input("Enter the desired length of wire (mm) : "))

##########################################################################
    # Prepare self for procedure
    write ("execute : Wear gloves")
    take_photo ("copper_wire")
    
##########################################################################
    # Straighten the copper wire piece for further operations
    for angle in range(0, 360, 90):
        press("copper_wire against a hard surface")
        rotate("copper_wire", "90 degrees", "clockwise")
    
    move ("Vernier_Calipers", "copper_wire")
    write ("execute : Open vernier calipers jaw " + str(wire_length) + " mm wide")
    write ("execute : Mark both the start and end points of the jaw on the wire using marker")

    take_photo ("copper_wire")
    
##########################################################################
    # Cut the wire to specified length
    move ("Vernier_Calipers", "copper_wire_start_mark")
    press("Wire cutter handle")
    
    move ("Vernier_Calipers", "copper_wire_end_mark")
    press("Wire cutter handle")
    
    take_photo ("copper_wire")
    
##########################################################################
    # Mount on Sample Stage
    prepare_sample (Sample, Sample_Box, test_object)

##########################################################################
##########################################################################