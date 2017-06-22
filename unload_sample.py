from complex_functions import *
from wrapper_functions import *

name="unload_sample"

def run(Sample, Sample_Box, sample_description, address):
    
    test_object = select_test_object()
    cryostat = select_cryostat()
    
    turn_on_PQMS_modules()
    set_up_pump()
    cables_disconnected_check(test_object, cryostat)
    
    release_PQMS_vaccum(cryostat)
    
    unload_sample (Sample, Sample_Box, test_object)
    liquid_nitrogen_remaining()
    turn_off_PQMS_modules()
    
    remove_sample (Sample, Sample_Box, test_object)
    
