from complex_functions import *
from wrapper_functions import *

name = "test_run"

def run():

    address, Sample, Sample_Box, sample_description = get_sample_info()
    #####################
    #Connect the sample with BNC Male pins

    take_photo  (Sample)

    move (Sample, 'Soldering Station')
    solder ("BNC1.Wire (I+)", Sample + ".Terminal_1(Outer)")
    solder ("BNC2.Wire (I-)", Sample + ".Terminal_2(Outer)")
    solder ("BNC3.Wire (V+)", Sample + ".Terminal_1(Inner)")
    solder ("BNC4.Wire (V-)", Sample + ".Terminal_2(Inner)")

    take_photo  (Sample)

    #####################
    #Connect with SMU
    press ("BNC1_Conn into SMU I+")
    press ("BNC2_Conn into SMU I-")
    press ("BNC3_Conn into SMU V+")
    press ("BNC4_Conn into SMU V-")

    #####################
    #switch on and set up systems
    turn_on_computer()
    turn_on_PQMS_modules()

    #####################
    # Check IV of sample using SMU

    goto  ('Qrius Main Window')
    click ('Modules Manager -> IV Source and Measurement Unit')

    click ('Run Mode -> IV')
    click ('Settings->IV Measurement Settings')
    write ('execute : Set V : 10000 mV')
    write ('execute : Set I : 10000 uA')
    write ('execute : Set V_step : 100 mV')
    write ('execute : Set I_step : 100 uA')

    click ('Start')
    write ('execute : Wait for run to finish')
    click ('Exit Qrius')

    #####################