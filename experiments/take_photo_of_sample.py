from complex_functions import *
from wrapper_functions import *

name = "take_photo_of_sample"

def run ():

#################################################################
    address, Sample, Sample_Box, sample_description = get_sample_info()
    
    take_photo_of_sample(Sample,Sample_Box)

#################################################################