from complex_functions import *

TEST_OBJECTS = ["Insert_RT_Puck", "Insert_RT_Old", "Puck_Board"]

def run (Sample, Sample_Box, sample_description, address):
    
    test_object = select_test_object()
    prepare_sample (Sample, Sample_Box, test_object)
    load_sample (Sample, Sample_Box, test_object)
    
    print("\nGenerating procedural steps for experiment.  .  .  .\n")
    
    switch_on_PQMS_modules()
    switch_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    temperature_set_point, V_range, V_step, I_range, I_step, max_power = get_experimental_parameters()
    configure_XTCON(temperature_set_point)
    
  #  while (True):
        
    PQMS_IV_run (temperature_set_point, V_range, V_step, I_range, I_step, max_power)
  #      response = raw_input("Do you want to do another run? : y/n \n")
        
  #      if (response == 'n'):
  #          break
    
    switch_off_PQMS_modules()
    
    print("\nProcedure has been created. Filename : " + log)
    print ("\nReady for execution.\n")
        
    unload_sample (Sample, Sample_Box, test_object)
    
    remove_sample (Sample, Sample_Box, test_object)
    
    switch_off_computer()

###############################################################################


def get_experimental_parameters():
    V_range                  = raw_input("Enter Voltage Sweep Max (mV) : \n")
    V_step                   = raw_input("Enter Voltage Step Size (mV) : \n")
    I_range                  = raw_input("Enter Current Sweep Max (uA) : \n")
    I_step                   = raw_input("Enter Current Step Size (uA) : \n")
    max_power                = raw_input("Enter Max Power (mW): \n")
    temperature_set_point    = raw_input("Enter Heater Setpoint Temperature (K) : \n")

    return temperature_set_point, V_range, V_step, I_range, I_step, max_power


def PQMS_IV_run (temperature_set_point, V_range, V_step, I_range, I_step, max_power):
    
    write("\n##############################################################")
    write("                   Run starts")
    write("##############################################################\n")
    
    start_TCON_run(temperature_set_point)
    start_IV_run(V_range, V_step, I_range, I_step, max_power)
        
    write("\n##############################################################")
    write("                   Run ends")
    write("##############################################################\n")
    
    response = raw_input("Do you want to do another run? : y/n \n")
    if (response == 'y'):
    	 temperature_set_point, V_range, V_step, I_range, I_step, max_power = get_experimental_parameters()
    	 PQMS_IV_run(temperature_set_point, V_range, V_step, I_range, I_step, max_power)


def prepare_sample (Sample, Sample_Box, test_object):
    
    mounted = raw_input( "\nIs the sample mounted on the puck? : y/n \n")
    while ((mounted != 'y') and (mounted != 'n')):
        
        mounted = raw_input( "\nIs the sample mounted on the puck? : y/n \n")
        
    if (mounted == 'n'):
        mount_sample (Sample, Sample_Box, test_object)
        
    elif (mounted == 'y'):
        print ("\nSample already mounted. Continue to next step.\n")
        sample_is_mounted()
        

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


def remove_sample (Sample, Sample_Box, test_object):
    
    unmount = raw_input ("\nDo you want to unmount the sample from the Puck after the measurements? : y/n \n")
    while ((unmount != 'y') and (unmount != 'n')):
        
        unmount = raw_input ("\nDo you want to unmount the sample from the Puck after the measurements? : y/n\n")
        
    if (unmount == 'n'):
        print ("\n Not unmounting the sample from the puck.\n")
        do_not_unmount()
        
    elif (unmount == 'y'):
        unmount_sample (Sample, Sample_Box, test_object)
