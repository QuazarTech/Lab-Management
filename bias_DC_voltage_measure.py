from complex_functions import *
from wrapper_functions import *

name = "bias_DC_voltage_measure"

def run (Sample, Sample_Box, sample_description, address):
    
    switch_on_PQMS_modules()
    

    voltage_set_point = get_experimental_parameters_bias_DC_voltage_measure()

    turn_on_computer()
    

    ###################
    
    write       ("execute : Goto Multimeter.Coordinates")
    write       ("execute : Hold Multimeter.Coordinates")
    write       ("execute : Goto PQMS.XSMU")
    write       ("execute : Ensure that RT and HT cables are not connected to any cryostat")
    write       ("execute : Insert Multimeter.Positive terminal to XSMU.Source.Positive terminal")
    write       ("execute : Insert Multimeter.Negative terminal to XSMU.Source.Negative terminal")
    write       ("execute : Put the Multimeter to appropriate mode")
    write       ("execute : Open Terminal")
    write       ("execute : change directory to work/svn/XPLORE/Qrius/tag/latest/ppsel/Capacitance/")
    write       ("execute : run capacitance.py")

    ###################
    switch_off_PQMS_modules()
    turn_off_computer()

#####################################################################################