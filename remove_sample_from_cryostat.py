from complex_functions import *
from wrapper_functions import *

name = "remove_sample_from_cryostat"

def run (Sample, Sample_Box, sample_description, address):


	#####################
	#select the test object and mount the sample on it
    
	test_object = select_test_object()
        cryostat    = select_cryostat()

	#####################
	#disconnecting cables
        write   ("execute : Ensure that the cryostat is at room temp (read temperature controller screen). If cold, abort experiment. If hot, set TCON heater setpoint to 300 K and start isothermal.")
        write   ("execute : Ensure that the cryostat is at atmospheric pressure (read pirani guage screen), If not, open Pump.Release_Valve")
	cables_disconnected_check (test_object, cryostat)
    
	#####################    
	
	#removing insert
	
	unclamp()
	write  ("execute : remove insert from the cryostat")
	write  ("execute : Leave insert on table")

	##################### 

	#removing cryostat to extract sample
	write  ("execute : Keep a soft tissue paper on the table near the "+ cryostat + "crysotat")
	write  ("execute : Remove all helium/vaccum connections from the cryostat")
	write  ("execute : Unscrew the " + cryostat + " cryostat nuts that screw it to the PQMS frame")
	write  ("execute : Pull the " + cryostat + " cryostat upwards from the frame")
	write  ("execute : Take cryostat to the table ")
	write  ("execute : Tilt the " + cryostat + " cryostat keeping its mouth over the tissue")
	write  ("execute : Replace the " + cryostat + " cryostat back to its frame")
	
	#####################    
	
	#storing sample
	write   ("execute : Wear gloves to handle the sample ")
	write   ("execute : Hold tweezers")
	write   ("execute : Use the tweezers to put the sample in its cover ")
	write   ("execute : Store the cover along with sample in the Dessicant ")

	#####################    
	
	

















