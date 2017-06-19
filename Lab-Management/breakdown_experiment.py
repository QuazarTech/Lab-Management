from complex_functions import *
name = "breakdown_experiment"

def run(Sample, Sample_Box, sample_description, address):
    test_object = select_test_object()
    prepare_sample (Sample, Sample_Box, test_object)
    load_sample (Sample, Sample_Box, test_object)
    
    print("\nGenerating procedural steps for experiment.  .  .  .\n")
    
    switch_on_PQMS_modules()
    set_up_pump()
    
    temperature_set_point, V_range, V_step, I_range, I_step, max_power = get_experimental_parameters()
    experimental_temperature = temperature_set_point
    
    flush_helium ("Sample_Chamber")
    create_vaccum("Heater_Chamber")
    
    switch_on_computer()
    set_save_folder(Sample_Box, Sample, sample_description, address)
    set_up_PQMS_modules()
    init_XTCON_isothermal ("Insert_RT_Old")
    do_break_down_run(experimental_temperature, V_range, V_step, I_range, I_step, max_power)
    set_upper_temperature()
    do_break_down_run(experimental_temperature, V_range, V_step, I_range, I_step, max_power)

def set_iterations():
  iterations = raw_input("How many iterations do you want to do for the 1 set_point?")
  return int(iterations)

def repeated_IV_run(V_range, V_step, I_range, I_step, max_power, iterations):
    for i in range(0, iterations):
      start_IV_run (V_range, V_step, I_range, I_step, max_power)

def do_break_down_run(temperature_set_point, V_range, V_step, I_range, I_step, max_power):
    need_liquid_nitrogen()
    set_XTCON_temp (temperature_set_point)
    iterations = set_iterations()
    repeated_IV_run(V_range, V_step, I_range, I_step, max_power, iterations)

def set_upper_temperature():
  temperature_set_point = raw_input("Set a upper set-point to cool down from:\n")
  set_XTCON_temp(temperature_set_point)