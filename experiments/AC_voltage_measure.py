from complex_functions import *
from wrapper_functions import *

name = "AC_voltage_measure"

def run ():
    
    
    turn_on_computer()
    turn_on_PQMS_modules()
    
    ##################
    
    voltage_set_point = get_experimental_parameters_bias_DC_voltage_measure()
    reference_amplitude,reference_frequency,reference_phase = get_experimental_parameters_AC_volatage_measure()
    
    ##################
    
    write        ("execute : Disconnect the XSMU R_Cable")
    write        ("execute : Disconnect the Lock-In Ref Out Cable")
    
    ##################
    
    move         ("PQMS.Voltage_Adder_Cable", "XSMU")
    write        ("execute : connect PQMS.Voltage_Adder_Cable 5 pin connector to XSMU")
    write        ("execute : connect PQMS.Voltage_Adder_Cable 1 pin connector to XLIA Ref Out") 
    
    ###################
    
    write       ("execute : Open Terminal")
    write       ("execute : Change directory to 'work/svn/XPLORE/Qrius/tag/latest/ppsel/Capacitance'")
    write       ("execute : type 'python capacitance.py'")

    write       ("execute : Enter the DC Voltage to apply")
    write       ("execute : Enter the AC Voltage Amplitude to apply")
    write       ("execute : Enter the AC Voltage frequency to apply")
    write       ("execute : Enter the phase of the AC Voltage")
    
    ####################
    
    goto        ("Oscilloscope.Coordinates")
    write       ("execute : Hold Oscilloscope.Probes")
    goto        ("PQMS.Voltage_Adder_Cable 8 pin connector")
    write       ("execute : Put the Oscilloscope to appropriate mode")
    
    ####################
    
    write       ("execute : Connect positive probe of the oscilloscope to Pin number 1 of the 8 pin connector")
    write       ("execute : Connect the negative probe of the oscilloscope to Pin number 5 of the 8 pin connector")
    
    write       ("execute : Oscilloscope should give an AC signal with desired settings shifted by a DC offset")
    take_photo  ('Oscilloscope Screen')
    write       ("execute : If yes, enter 'end' and abort the program. If no, do the following checks")
    
    AC_voltage_measure_checks()
    
    ###################
    #
    # measured_DC_V  = raw_input ("What is the DC offset of the signal? \n")
    # measured_AC_V  = raw_input ("What is the AC amplitude? \n")
    # measured_freq  = raw_input ("What is the measured frequency? \n")
    # measured_phase = raw_input ("What is the measured phase? \n")
    #
    ###################
    #
    # write("Measured DC V : " + measured_DC_V ) 
    # write("Measured AC V : " + measured_AC_V )
    # write("Measured freq : " + measured_freq )
    # write("Measured phase: " + measured_phase)
    #   
    ###################
   
    turn_off_PQMS_modules()
    turn_off_computer()

#####################################################################################

def AC_voltage_measure_checks():
    
    write     ("execute : Unplug the PQMS Voltage Adder 1 pin cable from XLIA Ref Out")
    write     ("execute : Unplug the PQMS Voltage Adder 5 pin cable from XSMU R_terminal")
    
    XSMU_check()
    XLIA_check()
    
    DC_cable_check()
    AC_cable_check()
    
    write     ("The checks have been complete, if you have reached this step, then there is no problem in the source or cable")

def XSMU_check():
    
    move      ("Multimeter", "XSMU")
    write     ("execute : Connect positive probe of multimeter to the XSMU R_Terminal V+ pin (the pin that corresponds to pin no 1 of PQMS Voltage Adder Cable 5 pin connector")
    write     ("execute : Connect negative probe of multimeter to the XSMU R_Terminal V- pin (the pin that corresponds to pin no 5 of PQMS Voltage Adder Cable 5 pin connector")
    
    write     ("execute : Check the multimeter reading, it should correspond to the DC Voltage Value set previously. If not, abort the program")
    take_photo('Multimeter Reading')
    write     ("execute : Disconnect the probes")
    move      ("Multimeter", "Multimeter.Rest_Coordinates")

def XLIA_check():

    goto      ("Oscilloscope.Coordinates")
    write     ("Connect the positive probe of the oscilloscope to the outer terminal of the XLIA Ref Out")
    write     ("Connect the negative probe of the oscilloscope to the inner terminal of the XLIA Ref Out")
    
    write     ("execute : The oscilloscope should recreate the AC signal which the lock in amplifier is generating. If not, abort the program")
    take_photo('Oscilloscope screen')
    write     ("execute : Disconnect the probes")

def DC_cable_check():

    write     ("execute : Connect the PQMS Voltage Adder 5 pin cable to XSMU R_Terminal")
    
    move      ("Multimeter", "PQMS Voltage Adder 8 pin cable")
    write     ("execute : Connect positive probe of multimeter to the PQMS Voltage Adder 8 pin cable Terminal 6")
    write     ("execute : Connect negattive probe of multimeter to the PQMS Voltage Adder 8 pin cable Terminal 7")
    
    write     ("execute : Check the multimeter reading, it should correspond to the DC Voltage Value set previously. If not, abort the program")
    take_photo('Multimeter Reading')
    write     ("execute : Disconnect the probes")
    move      ("Multimeter", "Multimeter.Rest_Coordinates") 
    
def AC_cable_check():

    write     ("execute : Unplug the PQMS Voltage Adder 5 pin cable from XSMU R_terminal")
    write     ("execute : Connect the PQMS Voltage Adder 1 pin cable to XLIA Ref Out")
    
    goto      ("Oscilloscope.Coordinates")
    write     ("execute : Connect the positive probe of the oscilloscope to the PQMS Voltage Adder 5 pin connector Terminal 4")
    write     ("execute : Connect the negative probe of the oscilloscope to the PQMS Voltage Adder 8 pin connector Terminal 7")
    
    write     ("execute : The oscilloscope should recreate the AC signal which the lock in amplifier is generating. If not, abort the program")
    take_photo('Oscilloscope screen')
    write     ("execute : Disconnect the probes")
    
