from complex_functions import *
from wrapper_functions import *

name = "CV_isothermal"

def run ():

    address, Sample, Sample_Box, sample_description = get_sample_info()
    test_object = select_test_object()
    prepare_sample (Sample, Sample_Box, test_object)
    
    switch_on_PQMS_modules()
    set_up_pump()
    
    is_the_sample_loaded (Sample, Sample_Box, test_object)

    temperature_set_point,voltage_set_point,initial_frequency,final_frequency,frequency_step,reference_amplitude,reference_frequency,reference_phase,run_mode = get_experimental_parameters_CV_isothermal()

    turn_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    
    need_liquid_nitrogen()


    ###################
    init_XTCON_isothermal ("Insert_RT_Old")
    set_XTCON_temperature (temperature_set_point)

    init_XSMU_constant_volatge("Insert_RT_Old")
    set_XSMU_voltage(voltage_set_point)

    init_XLIA_isothermal_constant_voltage("Insert_RT_Old")
    set_XLIA_isothermal_constant_voltage(initial_frequency,final_frequency,frequency_step,reference_amplitude,reference_frequency,reference_phase,run_mode)

    ###################

    release_PQMS_vaccum ()
    switch_off_PQMS_modules()
    turn_off_computer()

#####################################################################################
    




