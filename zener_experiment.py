from complex_functions import *

def run(Sample, Sample_Box, V_range, V_step, set_point, sample_description, address):
    zener_run(Sample, Sample_Box, V_range, V_step, set_point, sample_description, address)

def zener_run(Sample, Sample_Box, V_range, V_step, set_point, sample_description, address):
     print("Generating procedural steps for experiment.  .  .  .")
     load_sample(Sample, Sample_Box)
     switch_on_PQMS_modules()
     switch_on_computer()
     set_save_folder(Sample_Box, Sample, sample_description, address)
     set_up_PQMS_modules()
     configure_XTCON(set_point)
     configure_SMU(V_range, V_step)
     start_run()
     switch_off_PQMS_modules()
     unload_sample(Sample, Sample_Box)
     print("Procedure has been created. Filename : " + log)
     print ("Ready for execution.")