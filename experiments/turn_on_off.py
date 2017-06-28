from complex_functions import *
from wrapper_functions import *

name="turn_on_off"

def run():
    
    
    test_object = select_test_object()
    cryostat = select_cryostat()
    
    turn_on_PQMS_modules()
    turn_on_computer()
    
    cables_disconnected_check(test_object, cryostat)
   
    turn_off_PQMS_modules()
    turn_off_computer()
