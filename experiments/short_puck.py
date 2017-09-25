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
    # Remove enamel coating from ends
    
    ######### Take Precautions while performing following steps ##########
    move ("E-SOL Enamel remover flask's cap away from experiment")
    leave ("E-SOL Enamel remover flask's cap")
    
    write ("execute : Using toothpick, carefully exctract 2 drops of enamel remover onto a glass slide")
    move ("Flask's cap", "Flask's opening")
    
    hold ("tweezers")
    hold ("copper_wire")
    
    touch ("copper_wire.tip_1", "E-SOL Enamel Remover")
    hold ("Balled up Tissue Paper")
    touch ("copper_wire.tip_1", "Balled up Tissue Paper")
    
    touch ("copper_wire.tip_2", "E-SOL Enamel Remover")
    hold ("Balled up Tissue Paper")
    touch ("copper_wire.tip_2", "Balled up Tissue Paper")
    
##########################################################################
    # Mount on Sample Stage
    prepare_sample (Sample, Sample_Box, test_object)

##########################################################################
##########################################################################