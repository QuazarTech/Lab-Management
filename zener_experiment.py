from complex_functions import *

def run(Sample, Sample_Box, V_range_array, V_step_array, set_point_array, sample_description, address):
    zener_run(Sample, Sample_Box, V_range_array, V_step_array, set_point_array, sample_description, address)


def zener_run(Sample, Sample_Box, V_range_array, V_step_array, set_point_array, sample_description, address):
     print("Generating procedural steps for experiment.  .  .  .")
     load_sample(Sample, Sample_Box)
     switch_on_PQMS_modules()
     switch_on_computer()
     set_save_folder(Sample_Box, Sample, sample_description, address)
     set_up_PQMS_modules()
     
     for i in range(len(V_range_array)):
         write("##############################################################")
         write("                   Run "  + str(i+1) + " starts\n")
         write("##############################################################")
         
         configure_XTCON(set_point_array[i])
         start_IV_run(V_range_array[i], V_step_array[i])
         
         write("##############################################################")
         write("                   Run: " + str(i+1) + " ends\n")
         write("##############################################################")
     
     switch_off_PQMS_modules()
     unload_sample(Sample, Sample_Box)
     
     print("Procedure has been created. Filename : " + log)
     print ("Ready for execution.")