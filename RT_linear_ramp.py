from complex_functions import *
from wrapper_functions import *

name = "linear_ramp"

def run (Sample, Sample_Box, sample_description, address):
   
    
    test_object = select_test_object()
    prepare_sample (Sample, Sample_Box, test_object)
    is_the_sample_loaded (Sample, Sample_Box, test_object)
    
    switch_on_PQMS_modules()
    set_up_pump()
    
    switch_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    
    previous_run_temperature = ""
    initial_temperature, final_temperature, ramp_rate, run_mode, I_range, V_range, max_power, ramp_rate = get_experimental_parameters_R_Time_linear_ramp()
    current_run_temperature = initial_temperature
    reset_cryostat_environment (previous_run_temperature, current_run_temperature)
    
    need_liquid_nitrogen()
    
    #####################
    
    create_vaccum("Heater_Chamber")
    PQMS_RT_run_linear_ramp (initial_temperature, final_temperature, ramp_rate, run_mode, I_range, V_range, max_power)
    
    #####################
    
    release_PQMS_vaccum ()
    
    switch_off_PQMS_modules()
    switch_off_computer()