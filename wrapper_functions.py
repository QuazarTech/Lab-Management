from complex_functions import *

TEST_OBJECTS    = ["Insert_RT_Puck", "Insert_RT_Old", "Puck_Board"]
CHAMBERS        = ["Sample_Chamber", "Heater_Chamber"]

###############################################################################

def get_experimental_parameters():

    V_range                  = raw_input("Enter Voltage Sweep Max (mV) : \n")
    V_step                   = raw_input("Enter Voltage Step Size (mV) : \n")
    I_range                  = raw_input("Enter Current Sweep Max (uA) : \n")
    I_step                   = raw_input("Enter Current Step Size (uA) : \n")
    max_power                = raw_input("Enter Max Power (mW): \n")
    temperature_set_point    = float(raw_input("Enter Heater Setpoint Temperature (K) : \n"))
    
    return temperature_set_point, V_range, V_step, I_range, I_step, max_power

def get_experimental_parameters_R_Time():

    run_mode                 = raw_input("Which mode do you want to do the run in (constant current/voltage):\n")
    V_range                  = raw_input("Enter Voltage Sweep Max (mV) : \n")
    I_range                  = raw_input("Enter Current Sweep Max (uA) : \n")
    max_power                = raw_input("Enter Max Power (mW): \n")
    temperature_set_point    = float(raw_input("Enter Heater Setpoint Temperature (K) : \n"))
    
    return temperature_set_point, V_range, I_range, max_power, run_mode

def get_experimental_parameters_linear_ramp():
   
    run_mode                  = raw_input("Enter the R-Time run mode (current/voltage):\n")
    ramp_rate                 = raw_input("Enter Ramp rate : \n")
    final_temperature       = float(raw_input("Enter the ending temperature (K):\n"))
    V_range                   = raw_input("Enter Voltage Sweep Max (mV) : \n")
    I_range                   = raw_input("Enter Current Sweep Max (uA) : \n")
    max_power                 = raw_input("Enter Max Power (mW): \n")
    
    return final_temperature, ramp_rate, run_mode, I_range, V_range, max_power, ramp_rate

def PQMS_IV_run (temperature_set_point, V_range, V_step, I_range, I_step, max_power):
    
    write("\n##############################################################")
    write("                   Run starts")
    write("##############################################################\n")
    
    #check_peak_temperature  (temperature_set_point, "Heater_Chamber")
    set_XTCON_temp          (temperature_set_point)
    start_IV_run            (V_range, V_step, I_range, I_step, max_power)

    write("\n##############################################################")
    write("                   Run ends")
    write("##############################################################\n")
    
    previous_run_temperature = temperature_set_point
    
    response = raw_input("Do you want to do another run? : y/n \n")
    while (response != 'y' and response != 'n'):
    	response = raw_input("Do you want to do another run? : y/n \n")
    
    if (response == 'y'):
    	 
    	 temperature_set_point, V_range, V_step, I_range, I_step, max_power = get_experimental_parameters()
    	 cryostat_environment_setup (previous_run_temperature, temperature_set_point)
    	 
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


def need_liquid_nitrogen ():
    response = raw_input ("\nDo you want to pour liquid nitrogen? : y/n\n")
    while ((response!='y') and (response!='n')):
        response = raw_input ("\nDo you want to pour liquid nitrogen? : y/n\n")
    if (response == 'y'):
        pour_liquid_nitrogen()
        

def cryostat_environment_setup(previous_run_temperature, current_run_temperature):
    
    #first run cases
    if   (previous_run_temperature == "" and current_run_temperature <= 150):
        
        flush_helium ("Sample_Chamber")
        flush_helium ("Heater_Chamber")
        
    elif (previous_run_temperature == "" and current_run_temperature > 150):
        flush_helium ("Sample_Chamber")
        create_vaccum ("Heater_Chamber")
    
    #switch cases
    elif (previous_run_temperature <=150 and current_run_temperature > 150):
        create_vaccum ("Heater_Chamber")
    
    elif (previous_run_temperature > 150 and current_run_temperature <= 150):
        flush_helium ("Heater_Chamber")        


def init_linear_ramp(initial_temperature, ramp_rate, run_mode, I_range, V_range, max_power):
    click       ('Measurement Mode settings')
    click       ('Electrical DC Conductivity')
    move_cursor ('Run control')
    click       ('drop down menu')
    click       ('R-T (linear ramp)')
    move_cursor ('Toolbar')
    click       ('Settings->Temperature controller')
    click       ('Linear ramp settings')
    write       ("execute : Set Initial Temperature to " + str(initial_temperature))
    write       ("execute : Set Ramp rate to " + ramp_rate + " K/min")
    click       ('File->Apply')
    move_cursor ('Toolbar')
    click       ('Settings->I-V Source and Measurement Unit')
    click       ("Settings->Source Parametres")
    write       ("execute : Set mode as constant " + run_mode)
    move_cursor ("Top Menu")
    click       ("File->Done")
    move_cursor ("Top Menu")
    click       ("Settings->Resistance Measurement Settings")
    write       ("execute : Set voltage limit as " + V_range)
    write       ("execute : Set current limit as " + I_range)
    write       ("execute : Set max_power as " + max_power)
    write       ("execute : Set Bipolar as No")
    move_cursor ("Top Menu")
    click       ('File->Done')

def start_linear_ramp():
    click       ('Electrical DC Conductivity Window')
    write       ("Update_Database Lab_Space,PQMS,XSMU,Mode,R-Time")
    move_cursor ('Run Control')
    click       ('Start')
    write       ("Update_Database Lab_Space,PQMS,XTCON,Running,True")
    write       ("Update_Database Lab_Space,PQMS,XSMU,Running,True")
    write       ("execute : Wait until graph comes to an end")
    write       ("Update_Database Lab_Space,PQMS,XTCON,Running,False")
    write       ("Update_Database Lab_Space,PQMS,XSMU,Running,False")
    save_graph()

def is_the_sample_loaded (Sample, Sample_Box, test_object):
  
  response = raw_input ("\nIs the insert with sample loaded into the cryostat? : y/n \n")
  while ((response != 'y') and (response != 'n')):
    response = raw_input ("\nIs the insert with sample loaded into the cryostat? : y/n \n")
    if (response == 'n'):
      load_sample (Sample, Sample_Box, test_object)

def is_helium_flushed(previous_run_temperature, temperature_set_point):

  response = raw_input("Do you want to reset the cryostat environment?\n")
  while ((response != 'y') and (response != 'n')):
    response = raw_input ("Do you want to reset the cryostat environment?\n")
  if(response == 'y'):
  	cryostat_environment_setup(previous_run_temperature, temperature_set_point)
