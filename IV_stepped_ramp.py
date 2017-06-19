from complex_functions import *
from wrapper_functions import *

name = "IV_stepped_ramp"

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
    initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power = get_experimental_parameters_IV_stepped_ramp()
    current_run_temperature = initial_temperature
    
    flush_helium("Sample_Chamber")
    if (cryostat == "Double_Walled_Steel"):
        flush_helium("Heater_Chamber")
    
    
    turn_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    
    need_liquid_nitrogen()
    reset_cryostat_environment (previous_run_temperature, current_run_temperature, cryostat)
    
    #####################
    #Actual measurements take place here
    PQMS_IV_run (initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power)
    
    #####################
    
    release_PQMS_vaccum (cryostat)
    
    switch_off_PQMS_modules()
    turn_off_computer()
    
