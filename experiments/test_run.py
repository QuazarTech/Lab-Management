from complex_functions import *
from wrapper_functions import *

name = "test_run"

def run():

    turn_on_computer()
    
    test_object = select_test_object()
    cryostat    = select_cryostat()
    
    cables_connected_check (test_object, cryostat)
    
    goto  ('I-V Source and Measurement Unit')
    move_cursor ('Toolbar')
    click ('Settings->Acquisition Settings')
    write ('execute : Set filter length as 1')
    write ('execute : Set delay as 0')
    move_cursor('File->Apply')
    goto  ('Run control')
    click ('Drop down menu')
    click ('I-V Time Resolved')
    click ('Start Button')
    write ('execute : click finish when required results are obtained')
