from complex_functions import *
from wrapper_functions import *

name = "new_xsmu_test"

def run():

    write ("execute : Connect USB cable from XSMU_NANOVOLTMETER to CPU")
    write ("execute : Plug in the power cable to XSMU_NANOVOLTMETER")
    
    write ("execute : Connect USB cable from XTCON_NANOVOLTMETER to CPU")
    write ("execute : Plug in the power cable to XTCON_NANOVOLTMETER")
    
    write ("execute : Turn on the power cable for XSMU_NANOVOLTMETER and XTCON_NANOVOLTMETER")
    write ("Update_Database Lab_Space,PQMS,XSMU_NANOVOLTMETER,State,ON")
    write ("Update_Database Lab_Space,PQMS,XTCON_NANOVOLTMETER,State,ON"
    
    goto  ('Top Right Corner of the screen')
    click ('Power Button -> Service Engineer')
    write ('execute : Enter password')
   
    goto  ("Qrius")
    click ("Settings->Global Settings")
    write ("execute : Set TCON Serial Number to 19A")
    click ("OK")
    click ("MOdules Manager -> Temperature Controller")
    goto  ("Run Control")
    click ("Drop Down Menu")
    click ("Isothermal")
    click ("Settings->Isothermal Settings")
    write ("execute : Set Isothermal Setpoint to 318K")
    click ("File->Apply")
    click ("Start")
    
    write ("execute : Wait for about 1 hour for temperature to stabilize. Press Enter when wait is over.")
   
    write ('execute : Open Terminal')
    goto  ('${HOME}')
    write ('execute : type python VM_getReading_3.py')
    write ('execute : Press enter')
            
    write ('Wait for run to end')
    
