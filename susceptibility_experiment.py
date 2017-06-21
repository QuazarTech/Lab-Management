from complex_functions import *
from wrapper_functions import *

name = "susceptibility_experiment"

def run (Sample, Sample_Box, sample_description, address):
    
    
    #####################
    #select the test object and mount the sample on it
    
    test_object = select_test_object()
    cryostat = select_cryostat()
    prepare_sample (Sample, Sample_Box, test_object)
    
    #####################
    #switch on PQMS
    
    switch_on_PQMS_modules()
    set_up_pump()
    
    #####################
    
    is_the_sample_loaded (Sample, Sample_Box, test_object, cryostat)
    
    previous_run_temperature = ""
    step_size, max_depth  = get_experimental_parameters_XL()
    initial_temperature, final_temperature, ramp_rate, frequency, amplitude, phase  = get_experimental_parameters_XT_linear_ramp()
    drive_mode, drive_value, delay, filter_length   = get_lockin_aquisition_settings()
    current_run_temperature = initial_temperature
    
    
    turn_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    
    need_liquid_nitrogen()
    reset_cryostat_environment (previous_run_temperature, current_run_temperature, cryostat)
    
    ###
    set_XTCON_temperature(80)
    init_XTCON_isothermal(test_object)
    
    is_XL_run_needed(final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value)
    start_XT_linear_ramp_run(final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value)
    ###
    
    create_vaccum("Sample_Chamber")
    if (cryostat == "Double_Walled_Steel"):
        create_vaccum ("Heater_Chamber")
    
    switch_off_PQMS_modules()
    turn_off_computer()
  
