from complex_functions import *
from wrapper_functions import *

name = "new_xsmu_test"

def run():

    write ("execute : Connect USB cable from XSMU_NANOVOLTMETER to CPU")
    write ("execute : Plug in the power cable to XSMU_NANOVOLTMETER")
    write ("execute : Turn on the power cable for XSMU_NANOVOLTMETER")
    write    ("Update_Database Lab_Space,PQMS,XSMU_NANOVOLTMETER,State,ON")
    
    write ('execute : Res_7 current measurement on pqms already running for 10mA range')
    goto ('Top Left Corner of the screen')
    click ('Power Button -> Service Engineer')
    write ('execute : Enter password')
    
    write ('execute : Open Terminal')
    goto  ('${HOME}')
    write ('execute : type python VM_getReading_3.py')
    write ('execute : Press enter')
    
    goto ('Top Left Corner of the screen')
    click ('Power Button -> PQMS')
    write ('execute : Enter password')
    
    response = raw_input ('Is the Res_7 current measurement run still running normally? : y/n')
    while ((response != 'y') and (response != 'n')):
        response = raw_input ('Is the Res_7 current measurement run still running normally? : y/n')
    
    if (response == 'y'):
        write ('execute : Both XSMU running simultaneously : Experiment Successful')
    else :
        write ('execute : Both XSMU not working simultaneously : Experiment Failed')
    
    goto ('Top Left Corner of the screen')
    click ('Power Button -> Service Engineer')
    write ('execute : Enter password')
    
    write ('Wait for run to end')
    
