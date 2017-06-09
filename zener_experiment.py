from complex_functions import *
from wrapper_functions import *

name = "zener_experiment"

def run (Sample, Sample_Box, sample_description, address):
    
    
    test_object = select_test_object()
    prepare_sample (Sample, Sample_Box, test_object)
    load_sample (Sample, Sample_Box, test_object)
    
    switch_on_PQMS_modules()
    set_up_pump()
    
    
    switch_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    
    previous_run_temperature = ""
    temperature_set_point, V_range, V_step, I_range, I_step, max_power = get_experimental_parameters()
    cryostat_environment_setup (previous_run_temperature, temperature_set_point)
    
    need_liquid_nitrogen()
    init_XTCON_isothermal (test_object)
        
    PQMS_IV_run (temperature_set_point, V_range, V_step, I_range, I_step, max_power)
    
    stop_XTCON_run()
    release_PQMS_vaccum ()
    switch_off_PQMS_modules()
        
    unload_sample (Sample, Sample_Box, test_object)
    remove_sample (Sample, Sample_Box, test_object)
    
    switch_off_computer()
    