from complex_functions import *

TEST_OBJECTS    = ["Insert_Susceptibility", "Insert_RT_Puck", "Insert_RT_Old", "Puck_Board"]
CRYOSTATS       = ["Quartz", "Double_Walled_Steel"]
CHAMBERS        = ["Sample_Chamber", "Heater_Chamber"]

###############################################################################

def get_experimental_parameters_XL():

    step_size                   = raw_input("Enter step size : \n")
    max_depth                   = raw_input("Enter max_depth : \n")
  
    return step_size, max_depth

def get_experimental_parameters_XT_linear_ramp():

    frequency                = raw_input("Enter frequency (Hz) : \n")
    amplitude                = raw_input("Enter amplitude (mV) : \n")
    phase                    = raw_input("Enter phase     (degrees) : \n")
    
    initial_temperature      = float(raw_input("Enter Initial Temperature (K) : \n"))
    final_temperature        = float(raw_input("Enter Final Setpoint Temperature (K) : \n"))
    ramp_rate                = raw_input("Enter Ramp rate : \n")
    return initial_temperature, final_temperature, ramp_rate, frequency, amplitude, phase
    
def get_experimental_parameters_IV_stepped_ramp():

    V_range                  = raw_input("Enter Voltage Sweep Max (mV) : \n")
    V_step                   = raw_input("Enter Voltage Step Size (mV) : \n")
    I_range                  = raw_input("Enter Current Sweep Max (uA) : \n")
    I_step                   = raw_input("Enter Current Step Size (uA) : \n")
    max_power                = raw_input("Enter Max Power (mW): \n")
    
    initial_temperature      = float(raw_input("Enter Initial Temperature (K) : \n"))
    final_temperature        = float(raw_input("Enter Final Setpoint Temperature (K) : \n"))
    temperature_step         = float(raw_input("Enter Temperature Step (K) : \n"))
    return initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power

def get_experimental_parameters_RT_stepped_ramp():
    
    V_range                  = raw_input("Enter Voltage Sweep Max (mV) : \n")
    I_range                  = raw_input("Enter Current Sweep Max (uA) : \n")
    max_power                = raw_input("Enter Max Power (mW): \n")
    
    initial_temperature      = float(raw_input("Enter Initial Temperature (K) : \n"))
    final_temperature        = float(raw_input("Enter Final Setpoint Temperature (K) : \n"))
    temperature_step         = float(raw_input("Enter Temperature Step (K) : \n"))
    return initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power
    

def get_experimental_parameters_R_Time_isothermal():

    run_mode                 = raw_input("Which mode do you want to do the run in (constant current/voltage):\n")
    V_range                  = raw_input("Enter Voltage Sweep Max (mV) : \n")
    I_range                  = raw_input("Enter Current Sweep Max (uA) : \n")
    max_power                = raw_input("Enter Max Power (mW): \n")
    temperature_set_point    = float(raw_input("Enter Heater Setpoint Temperature (K) : \n"))
    
    return temperature_set_point, V_range, I_range, max_power, run_mode

def get_experimental_parameters_R_Time_linear_ramp():
   
    run_mode                  = raw_input("Enter the R-Time run mode (current/voltage):\n")
    ramp_rate                 = raw_input("Enter Ramp rate : \n")
    initial_temperature       = float(raw_input("Enter the starting temperature (K):\n"))
    final_temperature         = float(raw_input("Enter the ending temperature (K):\n"))
    V_range                   = raw_input("Enter Voltage Sweep Max (mV) : \n")
    I_range                   = raw_input("Enter Current Sweep Max (uA) : \n")
    max_power                 = raw_input("Enter Max Power (mW): \n")
    
    return initial_temperature, final_temperature, ramp_rate, run_mode, I_range, V_range, max_power, ramp_rate

def get_experimental_parameters_CV_isothermal():
    run_mode                  = raw_input("Enter the CV run mode (V-Time / ):\n")
    initial_frequency         = float(raw_input("Enter the starting frequency (Hz):\n"))
    final_frequency           = float(raw_input("Enter the ending frequency (Hz):\n"))
    frequency_step            = raw_input("Enter frequency Step Size (Hz) : \n")
    reference_amplitude       = raw_input("Enter the amplitude of the sine wave signal generated across the terminals of the REF OUT port. Its range is 0 - 1000mV : \n")
    reference_frequency       = raw_input("Enter the frequency of the sine wave signal generated across the terminals of the REF OUT port. Its range in 10 - 10000 Hz : \n")
    reference_phase           = raw_input("Enter the phase difference in degrees of the sine wave signal generated across the terminals of the REF OUT port with respect to the internal reference. : \n")
    temperature_set_point    = float(raw_input("Enter Heater Setpoint Temperature (K) : \n"))
    

def get_experimental_parameters_bias_DC_voltage_measure():
    voltage_set_point    = float(raw_input("Enter Voltage Setpoint : \n"))

    return voltage_set_point

def get_experimental_parameters_AC_volatage_measure():
    reference_amplitude       = raw_input("Enter the amplitude of the sine wave signal generated across the terminals of the REF OUT port. Its range is 0 - 1000mV : \n")
    reference_frequency       = raw_input("Enter the frequency of the sine wave signal generated across the terminals of the REF OUT port. Its range in 10 - 10000 Hz : \n")
    reference_phase           = raw_input("Enter the phase difference in degrees of the sine wave signal generated across the terminals of the REF OUT port with respect to the internal reference. : \n")
    
    return reference_amplitude,reference_frequency,reference_phase


###############################################################################

def PQMS_IV_run (initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power):
    
    write("\n##############################################################")
    write("                   Run starts")
    write("##############################################################\n")
    
    start_IV_step_ramp_run  (initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power)

    write("\n##############################################################")
    write("                   Run ends")
    write("##############################################################\n")
    
    #previous_run_temperature = temperature_set_point
    
    #response = raw_input("Do you want to do another run? : y/n \n")
    #while (response != 'y' and response != 'n'):
    	#response = raw_input("Do you want to do another run? : y/n \n")
    
    #if (response == 'y'):
    	 
    	 #temperature_set_point, V_range, V_step, I_range, I_step, max_power = get_experimental_parameters()
    	 #cryostat_environment_setup (previous_run_temperature, temperature_set_point)
    	 
    	 #PQMS_IV_run(temperature_set_point, V_range, V_step, I_range, I_step, max_power)

def PQMS_RT_run_stepped_ramp (initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power):
    
    write("\n##############################################################")
    write("                   Run starts")
    write("##############################################################\n")
    
    start_RT_step_ramp_run  (initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power)

    write("\n##############################################################")
    write("                   Run ends")
    write("##############################################################\n")

def PQMS_R_Time_run_isothermal (run_mode,  I_range, V_range, max_power, temperature_set_point, number_of_measurements):
    
    for i in range(number_of_measurements):

	    write("\n##############################################################")
	    write("                   Run starts")
	    write("##############################################################\n")
	    
	    set_XTCON_temperature (temperature_set_point)
	    start_R_Time_isothermal( I_range, V_range, max_power,  run_mode)

	    write("\n##############################################################")
	    write("                   Run ends")
	    write("##############################################################\n")

def PQMS_RT_run_linear_ramp (initial_temperature, final_temperature, ramp_rate, run_mode, I_range, V_range, max_power):
    
    write("\n##############################################################")
    write("                   Run starts")
    write("##############################################################\n")
    
    start_RT_linear_ramp (initial_temperature, final_temperature, ramp_rate, run_mode, I_range, V_range, max_power)
    
    write("\n##############################################################")
    write("                   Run ends")
    write("##############################################################\n")


###############################################################################

def select_test_object ():

    print "\n\n Available Test Objects : "
    print "______________________________\n"
    
    for item in TEST_OBJECTS:
        print item
    
    print "______________________________\n"
    test_object = raw_input ("Load Sample to which test_object? : \n")    
    
    while (test_object not in TEST_OBJECTS):
        
        print "\n\n Available Test Objects : "
        print "______________________________\n"
        
        for item in TEST_OBJECTS:
            print item
        
        print "______________________________\n"
        test_object = raw_input ("Load Sample to which test_object? : \n")
        
    return test_object


def select_cryostat ():

    print "\n\n Available Cryostats : "
    print "______________________________\n"
    
    for item in CRYOSTATS:
        print item
    
    print "______________________________\n"
    cryostat = raw_input ("Load Insert to which Cryostat? : \n")    
    
    while (cryostat not in CRYOSTATS):
        
        print "\n\n Available Cryostats : "
        print "______________________________\n"
        
        for item in CRYOSTATS:
            print item
        
        print "______________________________\n"
        cryostat = raw_input ("Load Insert to which Cryostat? : \n")
        
    return cryostat


def prepare_sample (Sample, Sample_Box, test_object):
    
    '''Asks the user if the sample is already soldered onto the test_object or is to be mounted during procedure'''
    
    mounted = raw_input( "\nIs the sample mounted on the puck? : y/n \n")
    while ((mounted != 'y') and (mounted != 'n')):
        mounted = raw_input( "\nIs the sample mounted on the puck? : y/n \n")
        
    if (mounted == 'n'):
        mount_sample (Sample, Sample_Box, test_object)
        
    elif (mounted == 'y'):
        print ("\nSample already mounted. Continue to next step.\n")
        sample_is_mounted()


def is_the_sample_loaded (Sample, Sample_Box, test_object, cryostat):
    
    '''Asks the user if the sample with the insert is already loaded in the cryostat or is to be loaded during procedure'''
  
    response = raw_input ("\nIs the insert with sample loaded into the cryostat? : y/n \n")
    while ((response != 'y') and (response != 'n')):
        response = raw_input ("\nIs the insert with sample loaded into the cryostat? : y/n \n")
    if (response == 'n'):
        load_sample (Sample, Sample_Box, test_object, cryostat)


def remove_sample (Sample, Sample_Box, test_object):
    
    '''Asks the user if the sample the sample is to be desoldered from the test_object after completion of the procedure'''
    
    unmount = raw_input ("\nDo you want to unmount the sample from the Puck after the measurements? : y/n \n")
    while ((unmount != 'y') and (unmount != 'n')):
        
        unmount = raw_input ("\nDo you want to unmount the sample from the Puck after the measurements? : y/n\n")
        
    if (unmount == 'n'):
        print ("\n Not unmounting the sample from the puck.\n")
        do_not_unmount()
        
    elif (unmount == 'y'):
        unmount_sample (Sample, Sample_Box, test_object)

###############################################################################

def need_liquid_nitrogen ():
    response = raw_input ("\nDo you want to pour liquid nitrogen? : y/n\n")
    while ((response!='y') and (response!='n')):
        response = raw_input ("\nDo you want to pour liquid nitrogen? : y/n\n")
    if (response == 'y'):
        pour_liquid_nitrogen()


def double_walled_steel_cryostat_environment_setup (previous_run_temperature, current_run_temperature):
    
        
    if (previous_run_temperature == "" and current_run_temperature > 150):
        create_vaccum ("Heater_Chamber")
    
    #switch cases
    elif (previous_run_temperature <=150 and current_run_temperature > 150):
        create_vaccum ("Heater_Chamber")
    

def quartz_cryostat_environment_setup(previous_run_temperature, current_run_temperature):
    
        
    if (previous_run_temperature == "" and current_run_temperature > 150):
        create_vaccum ("Sample_Chamber")
    
    #switch cases
    elif (previous_run_temperature <=150 and current_run_temperature > 150):
        create_vaccum ("Sample_Chamber")

    

def reset_cryostat_environment (previous_run_temperature, temperature_set_point, cryostat):

  response = raw_input("Do you want to reset the cryostat environment?\n")
  while ((response != 'y') and (response != 'n')):
    response = raw_input ("Do you want to reset the cryostat environment?\n")
  if(response == 'y') and (cryostat == "Double_Walled_Steel"):
  	double_walled_steel_cryostat_environment_setup(previous_run_temperature, temperature_set_point)
  if(response == 'y') and (cryostat == "Quartz"):
  	quartz_cryostat_environment_setup(previous_run_temperature, temperature_set_point)      


def release_PQMS_vaccum (cryostat):
    
    print ("\nIt is NOT reccomended to release vaccum if there is still liquid nitrogen left in the cryocan.")
    response = raw_input ("Do you want to release vaccum? : y/n\n")
    
    if (cryostat == "Double_Walled_Steel"):
        
        while ((response != 'y') and (response != 'n')):
            print ("\nIt is NOT reccomended to release vaccum if there is still liquid nitrogen left in the cryocan.")
            response = raw_input ("Do you want to release vaccum? : y/n\n")
        
        if (response == 'y'):
            for chamber in CHAMBERS[0:2] :
                sure = raw_input ("\nAre you SURE you want to release vaccum in " + chamber + " ? : y/n\n")
                while ((sure != 'y') and (sure != 'n')):
                    sure = raw_input ("\nAre you SURE you want to release vaccum in " + chamber + " ? : y/n\n")
                if (sure == 'y'):
                    release_pressure (chamber)
                    
    elif (cryostat == "Quartz"):
        
        release_pressure ("Sample_Chamber")
        
                        
 

def liquid_nitrogen_remaining ():
    
    response = raw_input ("Is liquid nitrogen left in the cryocan? : y/n\n")
    
    while ((response != 'y') and (response != 'n')):
        response = raw_input ("Is liquid nitrogen left in the cryocan? : y/n\n")
        
    if (response == 'y'):
        restore_vaccum ()

def turn_off_computer ():
    
    response = raw_input ("Do you want to turn off the computer? : y/n\n")
    
    while ((response != 'y') and (response != 'n')):
        response = raw_input ("Do you want to turn off the computer? : y/n\n")
        
    if (response == 'y'):
        switch_off_computer()
        
def turn_on_computer():
    
    response = raw_input ("Is the Computer already on? : y/n\n")
    
    while ((response != 'y') and (response != 'n')):
        response = raw_input ("Is the Computer already on? : y/n\n")
        
    if (response == 'n'):
        switch_on_computer()
