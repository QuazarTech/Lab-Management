from complex_functions import *
from wrapper_functions import *

name = "zener_experiment"

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
    initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power = get_experimental_parameters_IV_stepped_ramp()
    current_run_temperature = initial_temperature
    reset_cryostat_environment (previous_run_temperature, current_run_temperature)
    
    need_liquid_nitrogen()
    
    #####################
      
    PQMS_IV_run (initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power)
    
    #####################
    
    release_PQMS_vaccum ()
    
    switch_off_PQMS_modules()
    switch_off_computer()
    