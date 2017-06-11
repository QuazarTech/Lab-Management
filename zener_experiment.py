from complex_functions import *
name = "zener_experiment"

def run (Sample, Sample_Box, sample_description, address):
    
    test_object = select_test_object()
    prepare_sample (Sample, Sample_Box, test_object)
    load_sample (Sample, Sample_Box, test_object)
    
    print("\nGenerating procedural steps for experiment.  .  .  .\n")
   
    
    temperature_set_point, V_range, V_step, I_range, I_step, max_power = get_experimental_parameters_IV()
    
    flush_helium ("Sample_Chamber")
    
    if(check_temperature(temperature_set_point) == 'n'):
    	flush_helium ("Heater_Chamber")
    else:
    	create_vaccum("Heater_Chamber")
    
    switch_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    
    need_liquid_nitrogen()
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
    while (response != 'y' and response != 'n'):
    	response = raw_input("Do you want to do another run? : y/n \n")
    if (response == 'y'):
    	 temperature_set_point, V_range, V_step, I_range, I_step, max_power = get_experimental_parameters_IV()
    	 if(check_temperature(temperature_set_point) == "same"):
    	 	create_vaccum("Heater_Chamber")
    	 PQMS_IV_run(temperature_set_point, V_range, V_step, I_range, I_step, max_power)



def check_temperature(temperature_set_point):
	if(float(temperature_set_point) > 150.0):
		return 'y'
        elif(float(temperature_set_point) == 150.0):
        	return "same"
        else:
        	return 'n'
