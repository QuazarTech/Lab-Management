from complex_functions import *
from wrapper_functions import *

name = "RT_stepped_ramp"

def run (Sample, Sample_Box, sample_description, address):
    
    
    #####################
    #select the test object and mount the sample on it
    
    test_object = select_test_object()
    cryostat    = select_cryostat()

    prepare_sample (Sample, Sample_Box, test_object)
    
    #####################
    #switch on and set up systems
    turn_on_computer()
    set_save_folder (Sample_Box, Sample, sample_description, address)
    
    turn_on_PQMS_modules()
    set_up_PQMS_modules()
    set_up_pump()
    
    #####################
    
    is_the_sample_loaded (Sample, Sample_Box, test_object, cryostat)
    cables_connected_check (test_object, cryostat)
    
    previous_run_temperature = ""
    initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power = get_experimental_parameters_RT_stepped_ramp()
    
    pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance = get_step_ramp_details()
    
    current_run_temperature = initial_temperature
    
    reset_cryostat_environment (previous_run_temperature, current_run_temperature, cryostat)
    need_liquid_nitrogen()
    
    
    #####################
    #Actual measurements take place here
    PQMS_RT_run_stepped_ramp (initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance)
    
    #####################

    cables_disconnected_check (test_object, cryostat)    
    create_vaccum("Sample_Chamber")
    if (cryostat == "Double_Walled_Steel"):
        create_vaccum ("Heater_Chamber")
    
    turn_off_PQMS_modules()
    turn_off_computer()
    
