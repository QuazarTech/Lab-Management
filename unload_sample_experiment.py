from complex_functions import *
name="unload_sample_experiment"

def run(Sample, Sample_Box, sample_description, address):
    test_object = select_test_object()
    switch_on_PQMS_modules()
    set_up_pump()
    unload_sample (Sample, Sample_Box, test_object)
    remove_sample (Sample, Sample_Box, test_object)
    print("\nProcedure has been created. Filename : " + procedure)
    print ("\nReady for execution.\n")

