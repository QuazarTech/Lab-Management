from complex_functions import *
from wrapper_functions import *

name = "RT_linear_ramp"

def run ():
   
    address, Sample, Sample_Box, sample_description = get_sample_info()
    test_object = select_test_object()
    cryostat    = select_cryostat()
    
    prepare_sample (Sample, Sample_Box, test_object)
    
    switch_on_PQMS_modules()
    set_up_pump()
    
    is_the_sample_loaded (Sample, Sample_Box, test_object, cryostat)
    
    previous_run_temperature = ""
    initial_temperature, final_temperature, ramp_rate, run_mode, I_range, V_range, max_power, ramp_rate = get_experimental_parameters_R_Time_linear_ramp()
    current_run_temperature = initial_temperature
    reset_cryostat_environment (previous_run_temperature, current_run_temperature, cryostat)
    
    turn_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    
    need_liquid_nitrogen()
      
    #####################
    if (cryostat == "Double_Walled_Steel"):
        create_vaccum("Heater_Chamber")
    PQMS_RT_run_linear_ramp (initial_temperature, final_temperature, ramp_rate, run_mode, I_range, V_range, max_power)
    
    #####################
    
    release_PQMS_vaccum (cryostat)
    
    switch_off_PQMS_modules()
    turn_off_computer()
