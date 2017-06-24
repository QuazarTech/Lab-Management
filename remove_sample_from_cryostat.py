from complex_functions import *
from wrapper_functions import *

name = "remove_sample_from_cryostat"

def run (Sample, Sample_Box, sample_description, address):


	#####################
	#select the test object and mount the sample on it
    
	test_object = select_test_object()
        cryostat    = select_cryostat()
    
        prepare_sample (Sample, Sample_Box, test_object)
    

	#####################
	#disconnecting cables

	disconnect_cable ("HT_Cable")
	disconnect_cable ("RT_Cable")
	
    
	#####################    
	
	#removing insert
	
	unload_sample(Sample, Sample_Box, test_object, cryostat)

	##################### 

	#removing cryostat to extract sample
	write   ("execute : Keep a soft tissue paper on the table near the "+ cryostat + "crysotat")
	write   ("execute : Unscrew the " + cryostat + " cryostat nuts")
	write   ("execute : Remove the " + cryostat + " cryostat from the frame and take it to the table ")
	write   ("execute : Tilt the " + cryostat + " cryostat keeping the mouth over the tissue")
	write   ("execute : Keep the " + cryostat + " cryostat back in its coordinates")
	
	#####################    
	
	#storing sample
	write   ("execute : Wear gloves to handle the sample ")
	write   ("execute : Locate tweezers and hold it")
	write   ("execute : Locate sample cover, hold it and come back to the table")
	write   ("execute : Use the tweezers to put the sample in its cover ")
	write   ("execute : Store the cover in the Dessicant ")

	#####################    
	
	

















