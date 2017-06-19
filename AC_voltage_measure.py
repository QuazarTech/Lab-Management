from complex_functions import *
from wrapper_functions import *

name = "AC_voltage_measure"

def run (Sample, Sample_Box, sample_description, address):
    
    switch_on_PQMS_modules()
    

    reference_amplitude,reference_frequency,reference_phase = get_experimental_parameters_AC_volatage_measure()
    turn_on_computer()
    set_up_PQMS_modules()
    

    ###################

    write       ("execute : Goto Oscilloscope.Coordinates")
    write       ("execute : Hold Oscilloscope.Probes")
    write       ("execute : Goto PQMS.XLIA")
    write       ("execute : Connect Oscilloscope to PQMS.XLIA")
    write       ("execute : Put the Oscilloscope to appropriate mode")
    write       ("execute : Press ctrl+alt+T")
    write       ("execute : Change directory to the folder containing 'work/svn/XPLORE/Qrius/tag/latest/ppsel/Capacitance'")
    write       ("execute : type 'python capacitance.py'")


    ###################
    switch_off_PQMS_modules()
    turn_off_computer()

#####################################################################################