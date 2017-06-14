from complex_functions import *
from wrapper_functions import *

name = "R_Time_isothermal"

def run (Sample, Sample_Box, sample_description, address):
    
    
    test_object = select_test_object()
    prepare_sample (Sample, Sample_Box, test_object)
    
    switch_on_PQMS_modules()
    set_up_pump()
    
    is_the_sample_loaded (Sample, Sample_Box, test_object)
    
    switch_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()

    previous_run_temperature = ""
    temperature_set_point, V_range, I_range, max_power, run_mode  = get_experimental_parameters_R_Time_isothermal()
    current_run_temperature = temperature_set_point
    reset_cryostat_environment (previous_run_temperature, current_run_temperature)
    
    need_liquid_nitrogen()
    
    #####################
    
    init_XTCON_isothermal ("Insert_RT_Old")

    number_of_measurements = int(raw_input("How many more iterations do you want to do?"))
    PQMS_R_Time_run_isothermal (run_mode,  I_range, V_range, max_power, temperature_set_point, number_of_measurements)
    
    stop_XTCON_run()

    #####################
    
    release_PQMS_vaccum ()
    
    switch_off_PQMS_modules()    
    switch_off_computer()
    
####################################################################################################

  	