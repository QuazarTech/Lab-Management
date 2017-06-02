from complex_functions import *

TEST_OBJECTS = ["Insert_RT_Puck", "Puck_Board"]

def run (Sample, Sample_Box, sample_description, address):
        
    mount_sample_on_puck (Sample, Sample_Box)
    
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
    
    load_sample (Sample, Sample_Box, test_object)
    
    print("\nGenerating procedural steps for experiment.  .  .  .\n")
    
    switch_on_PQMS_modules()
    switch_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    
    while (True):
        
        temperature_set_point, V_range, V_step, I_range, I_step, max_power = get_experimental_parameters()
        PQMS_IV_run (temperature_set_point, V_range, V_step, I_range, I_step, max_power)
        response = raw_input("Do you want to do another run? : y/n \n")
        
        if (response == 'n'):
            break
    
    switch_off_PQMS_modules()
    
    print("\nProcedure has been created. Filename : " + log)
    print ("\nReady for execution.\n")
        
    unload_sample (Sample, Sample_Box, test_object)
    unmount_sample_from_puck (Sample, Sample_Box)
    

###############################################################################


def get_experimental_parameters():
    V_range                    = raw_input("Enter Voltage Sweep Max (mV) : \n")
    V_step                   = raw_input("Enter Voltage Step Size (mV) : \n")
    I_range                    = raw_input("Enter Current Sweep Max (uA) : \n")
    I_step                   = raw_input("Enter Current Step Size (uA) : \n")
    max_power                    = raw_input("Enter Max Power (mW): \n")
    temperature_set_point           = raw_input("Enter Heater Setpoint Temperature (K) : \n")

    return temperature_set_point, V_range, V_step, I_range, I_step, max_power


def PQMS_IV_run (temperature_set_point, V_range, V_step, I_range, I_step, max_power):
    
    write("\n##############################################################")
    write("                   Run starts")
    write("##############################################################\n")
    
    configure_XTCON(temperature_set_point)
    start_IV_run(V_range, V_step, I_range, I_step, max_power)
    
    write("\n##############################################################")
    write("                   Run ends")
    write("##############################################################\n")

            