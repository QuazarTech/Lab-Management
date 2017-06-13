from complex_functions import *
from wrapper_functions import *
name = "linear_ramp"

def run(Sample,Sample_Box, sample_description, address):
    test_object = select_test_object()
    prepare_sample (Sample, Sample_Box, test_object)
    switch_on_PQMS_modules()
    set_up_pump()
    is_the_sample_loaded (Sample, Sample_Box, test_object)
    
    print("\nGenerating procedural steps for experiment.  .  .  .\n")
    
    previous_run_temperature = ""
    final_temperature, ramp_rate, run_mode, I_range, V_range, max_power, ramp_rate = get_experimental_parameters_linear_ramp()
    
    is_helium_flushed(previous_run_temperature, final_temperature)
    
    switch_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    init_XTCON_isothermal(test_object)
    need_liquid_nitrogen()
    set_XTCON_temperature(final_temperature)
    

    create_vaccum("Heater_Chamber")
    stop_XTCON_run()
    
    init_linear_ramp(final_temperature, ramp_rate, run_mode, I_range, V_range, max_power)
    start_linear_ramp()

    release_PQMS_vaccum ()
    switch_off_PQMS_modules()
        
    unload_sample (Sample, Sample_Box, test_object)
    remove_sample (Sample, Sample_Box, test_object)
    
    switch_off_computer()
    
    print("\nProcedure has been created. Filename : " + procedure)
    print ("\nReady for execution.\n")

####################################################################################################
