from complex_functions import *
from wrapper_functions import *
name = "breakdown_experiment"

def run(Sample, Sample_Box, sample_description, address):
    test_object = select_test_object()
    prepare_sample (Sample, Sample_Box, test_object)
    switch_on_PQMS_modules()
    set_up_pump()
    is_the_sample_loaded (Sample, Sample_Box, test_object)
    
    print("\nGenerating procedural steps for experiment.  .  .  .\n")

    previous_run_temperature = ""
    temperature_set_point, V_range, I_range, max_power, run_mode  = get_experimental_parameters_R_Time()
    
    is_helium_flushed(previous_run_temperature, temperature_set_point)
    
    need_liquid_nitrogen()
    switch_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    init_XTCON_isothermal ("Insert_RT_Old")
    response = raw_input("How many more iterations do you want to do?")
    PQMS_R_Time_Run(run_mode,  I_range, V_range, max_power, temperature_set_point, response)
    
    stop_XTCON_run()
    release_PQMS_vaccum ()
    switch_off_PQMS_modules()
        
    unload_sample (Sample, Sample_Box, test_object)
    remove_sample (Sample, Sample_Box, test_object)
    
    switch_off_computer()
    
    print("\nProcedure has been created. Filename : " + procedure)
    print ("\nReady for execution.\n")

####################################################################################################

def PQMS_R_Time_Run(run_mode,  I_range, V_range, max_power, temperature_set_point, response):
    
    for i in range(0, int(response)):
	    write("\n##############################################################")
	    write("                   Run starts")
	    write("##############################################################\n")
	    
	    set_XTCON_temp (temperature_set_point)
	    previous_set_point = temperature_set_point
	    start_R_Time( I_range, V_range, max_power,  run_mode)

	    write("\n##############################################################")
	    write("                   Run ends")
	    write("##############################################################\n")
	 
    	    temperature_set_point, V_range, I_range, max_power, run_mode  = get_experimental_parameters_R_Time()
    	    if(check_set_point(temperature_set_point) == True and check_set_point(previous_set_point) == False):
    	 	 flush_helium("Heater_Chamber")
    	    elif(check_set_point(temperature_set_point) == False and check_set_point(previous_set_point) == True):
    	 	create_vacuum("Heater_Chamber")
    	 

def check_set_point(temperature_set_point):
    if(float(temperature_set_point) < 150.0):
    	return True
    else:
    	return False

def is_the_sample_loaded (Sample, Sample_Box, test_object):
  
  response = raw_input ("\nIs the insert with sample loaded into the cryostat? : y/n \n")
  while ((response != 'y') and (response != 'n')):
    response = raw_input ("\nIs the insert with sample loaded into the cryostat? : y/n \n")
    if (response == 'n'):
      load_sample (Sample, Sample_Box, test_object)

def is_helium_flushed(previous_run_temperature, temperature_set_point):

  previous_run_temperature = ""
  response = raw_input("Do you want to reset the cryostat environment?\n")
  while ((response != 'y') and (response != 'n')):
    response = raw_input ("Do you want to reset the cryostat environment?\n")
  if(response == 'y'):
  	cryostat_environment_setup(previous_run_temperature, current_run_temperature)
  	
  	
