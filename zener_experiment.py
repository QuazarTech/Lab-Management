from complex_functions import *

TEST_OBJECTS = ["Insert_RT_Puck", "Insert_RT_Old", "Puck_Board"]
CHAMBERS = ["Sample_Chamber", "Heater_Chamber"]
name = "zener_experiment"

def run (Sample, Sample_Box, sample_description, address):
    
    test_object = select_test_object()
    prepare_sample (Sample, Sample_Box, test_object)
    load_sample (Sample, Sample_Box, test_object)
    
    print("\nGenerating procedural steps for experiment.  .  .  .\n")
    
    switch_on_PQMS_modules()
    set_up_pump()
    
    flush_helium ("Sample_Chamber")
    flush_helium ("Heater_Chamber")
    
    switch_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    temperature_set_point, V_range, V_step, I_range, I_step, max_power = get_experimental_parameters()
    
    pour_liquid_nitrogen()
    init_XTCON_isothermal (test_object)
    
  #  while (True):
        
    PQMS_IV_run (temperature_set_point, V_range, V_step, I_range, I_step, max_power)
  #      response = raw_input("Do you want to do another run? : y/n \n")
        
  #      if (response == 'n'):
  #          break

    stop_XTCON_run()
    release_PQMS_vaccum ()
    switch_off_PQMS_modules()
        
    unload_sample (Sample, Sample_Box, test_object)
    remove_sample (Sample, Sample_Box, test_object)
    
    switch_off_computer()
    
    print("\nProcedure has been created. Filename : " + procedure)
    print ("\nReady for execution.\n")

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

    set_XTCON_temp (temperature_set_point)
    start_IV_run (V_range, V_step, I_range, I_step, max_power)

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

def release_PQMS_vaccum ():
    
    print ("\nIt is NOT reccomended to release vaccum if there is still liquid nitrogen left in the cryocan.")
    response = raw_input ("Do you want to release vaccum? : y/n\n")
    
    while ((response != 'y') and (response != 'n')):
        print ("\nIt is NOT reccomended to release vaccum if there is still liquid nitrogen left in the cryocan.")
        response = raw_input ("Do you want to release vaccum? : y/n\n")
        
        if (response == 'y'):
            for chamber in CHAMBERS :
                sure = raw_input ("\nAre you SURE you want to release vaccum in " + chamber + " ? : y/n\n")
                while ((sure != 'y') and (sure != 'n')):
                    sure = raw_input ("\nAre you SURE you want to release vaccum in " + chamber + " ? : y/n\n")
                    if (sure == 'y'):
                        release_vaccum (chamber)
                        
        elif (response == 'n'):
            break