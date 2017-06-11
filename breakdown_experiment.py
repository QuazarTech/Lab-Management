from complex_functions import *
name = "breakdown_experiment"

def run(Sample, Sample_Box, sample_description, address):
    test_object = select_test_object()
    prepare_sample (Sample, Sample_Box, test_object)
    load_sample (Sample, Sample_Box, test_object)
    
    print("\nGenerating procedural steps for experiment.  .  .  .\n")

    
    run_mode, value_of_constant_source, temperature_set_point = get_experimental_parameters_R_Time()
    
    flush_helium ("Sample_Chamber")
    if(check_set_point(temperature_set_point) == True):
    	flush_helium("Heater_Chamber")
    else:
        create_vaccum("Heater_Chamber")
    
    need_liquid_nitrogen()
    switch_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    init_XTCON_isothermal ("Insert_RT_Old")
    PQMS_R_Time_Run(run_mode, value_of_constant_source, temperature_set_point)
    
    stop_XTCON_run()
    release_PQMS_vaccum ()
    switch_off_PQMS_modules()
        
    unload_sample (Sample, Sample_Box, test_object)
    remove_sample (Sample, Sample_Box, test_object)
    
    switch_off_computer()
    
    print("\nProcedure has been created. Filename : " + procedure)
    print ("\nReady for execution.\n")

####################################################################################################

def PQMS_R_Time_Run(run_mode, value_of_constant_source, temperature_set_point):
    
    write("\n##############################################################")
    write("                   Run starts")
    write("##############################################################\n")
    
    set_XTCON_temp (temperature_set_point)
    previous_set_point = temperature_set_point
    start_R_Time(value_of_constant_source, run_mode)

    write("\n##############################################################")
    write("                   Run ends")
    write("##############################################################\n")
    
    response = raw_input("Do you want to do another run? : y/n \n")
    while (response != 'y' and response != 'n'):
    	response = raw_input("Do you want to do another run? : y/n \n")
    if (response == 'y'):
    	 run_mode,value_of_constant_source,temperature_set_point = get_experimental_parameters_R_Time()
    	 if(check_set_point(temperature_set_point) == True and check_set_point(previous_set_point) == False):
    	 	flush_helium("Heater_Chamber")
    	 elif(check_set_point(temperature_set_point) == False and check_set_point(previous_set_point) == True):
    	 	create_vacuum("Heater_Chamber")
    	 PQMS_R_Time_Run(run_mode, value_of_constant_source, temperature_set_point)
    	 

def check_set_point(temperature_set_point):
    if(float(temperature_set_point) < 150.0):
    	return True
    else:
    	return False
