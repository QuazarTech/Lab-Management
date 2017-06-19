from complex_functions import *
from wrapper_functions import *

name = "AC_voltage_measure"

def run (Sample, Sample_Box, sample_description, address):
    
    switch_on_PQMS_modules()
    

    reference_amplitude,reference_frequency,reference_phase = get_experimental_parameters_AC_volatage_measure()
    switch_on_computer()
    set_up_PQMS_modules()
    

    ###################

    write       ("execute : Goto Oscilloscope.Coordinates")
    write       ("execute : Hold Oscilloscope.Coordinates")
    write       ("execute : Goto PQMS.XSMU")
    write       ("execute : Connect Oscilloscope to PQMS.XLIA")
    write       ("execute : Put the Oscilloscope to appropriate mode")
    write       ("execute : Press ctrl+alt+T")
    write       ("execute : Change directory to the folder containing 'capacitance.py'")
    write       ("execute : type 'python capacitance.py'")


    ###################
    switch_off_PQMS_modules()
    switch_off_computer()

#####################################################################################