from complex_functions import *
from wrapper_functions import *

name = "AC_voltage_measure"

def run (Sample, Sample_Box, sample_description, address):
    
    turn_on_computer()
    turn_on_PQMS_modules()
    set_up_PQMS_modules()
    
    voltage_set_point = get_experimental_parameters_bias_DC_voltage_measure()
    reference_amplitude,reference_frequency,reference_phase = get_experimental_parameters_AC_volatage_measure()
    
    
    write        ("execute : connect PQMS.Voltage_Adder_Cable 5 pin connector to XSMU")
    write        ("execute : connect PQMS.Voltage_Adder_Cable 1 pin connector to Lockin Ref Out")
    
    ###################

    goto        ("Oscilloscope.Coordinates")
    write       ("execute : Hold Oscilloscope.Probes")
    goto        ("PQMS.Voltage_Adder_Cable 8 pin connector")
    write       ("execute : Put the Oscilloscope to appropriate mode")
    write       ("execute : Connect Oscilloscope to Pin number")
    write       ("execute : Open Terminal")
    write       ("execute : Change directory to 'work/svn/XPLORE/Qrius/tag/latest/ppsel/Capacitance'")
    write       ("execute : type 'python capacitance.py'")
    
    ###################
    
    measured_DC_V  = raw_input ("What is the DC offset of the signal? \n")
    measured_AC_V  = raw_input ("What is the AC amplitude? \n")
    measured_freq  = raw_input ("What is the measured frequency? \n")
    measured_phase = raw_input ("What is the measured phase? \n")

    ###################
    
    write("Measured DC V : " + measured_DC_V ) 
    write("Measured AC V : " + measured_AC_V )
    write("Measured freq : " + measured_freq )
    write("Measured phase: " + measured_phase)
   
    ###################
   
    turn_off_PQMS_modules()
    turn_off_computer()

#####################################################################################