from complex_functions import *
from wrapper_functions import *

name = "test_run"

def run():

	address, Sample, Sample_Box, sample_description = get_sample_info()
    #####################
    #select the test object and mount the sample on it
    
    test_object = select_test_object()
    cryostat    = select_cryostat()
    
    prepare_sample (Sample, Sample_Box, test_object)
    
    #####################
    #switch on and set up systems
    turn_on_computer()
    
    turn_on_PQMS_modules()
    set_up_pump()
    
    #####################
    
    is_the_sample_loaded (Sample, Sample_Box, test_object, cryostat)
    cables_connected_check (test_object, cryostat)
   
	goto  ('work/git/XPLORE/Qrius/ppsel/capacitance')
	write ('execute : Open Terminal')
	write ('execute : type python current_measurement_w_tcon.py')
	write ('execute : press enter')

	write ('execute : set temperature setpoint as 310')
	write ('execute : set tolerance as 0.05')    
	write ('execute : press enter')
	
	write ('execute : Wait for temperature to stabilize')
	
	write('execute :  goto Qrius') 
	write('execute :  goto Modules Manager->IV Source and Measurement')
	write('execute :  set run control to IV')
	move_cursor ('Toolbar')
	click('Settings->IV_Measurement Settings')
	write('execute :  Set Voltage Range as 1000')
	write('execute :  Set Voltage Step as 100')
	write('execute :  Set Bipolar as No')
	move_cursor('Toolbar')
	write('execute :  click file->apply') 
	write('execute :  click on start button')
	write('execute :  Press finish when required data is obtained')
	
	write ('execute : Go to terminal window again')
	write ('execute : press enter, y and enter again')
	
	write ('execute : Exit Terminal')
	
