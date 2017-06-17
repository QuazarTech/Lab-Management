from complex_functions import *
from wrapper_functions import *

name = "bias_DC_voltage_measure"

def run (Sample, Sample_Box, sample_description, address):
    
    switch_on_PQMS_modules()
    

    voltage_set_point = get_experimental_parameters_bias_DC_voltage_measure()

    switch_on_computer()
    set_up_PQMS_modules()
    

    ###################

    write       ("execute : Goto Multimeter.Coordinates")
    write       ("execute : Hold Multimeter.Coordinates")
    write       ("execute : Goto PQMS.XSMU")
    write       ("execute : Insert Multimeter.Positive terminal to XSMU.Source.Positive terminal")
    write       ("execute : Insert Multimeter.Negative terminal to XSMU.Source.Negative terminal")
    write       ("execute : Put the Multimeter to appropriate mode")
    write       ("execute : Press ctrl+alt+T")
    write       ("execute : Change directory to the folder containing 'capacitance.py'")
    write       ("execute : type 'python capacitance.py'")


    ###################
    switch_off_PQMS_modules()
    switch_off_computer()

#####################################################################################