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

    #####################

    set_up_pump(cryostat)
    is_the_sample_loaded (Sample, Sample_Box, test_object, cryostat)
    cables_connected_check (test_object, cryostat)

    #####################
    # Check resistance of sample PT100 using SMU while measuring Sample Temp

    goto  ('Qrius Main Window')

    click ('Modules Manager -> IV Source and Measurement Unit')
    click ('Run Mode -> R-Time')
    click ('Start')

    click ('Modules Manager -> Temperature Controller')
    click ('Run Mode -> Monitor')
    click ('Start')

    write ('execute : Wait for 300 seconds')
    click ('IV Source and Measurement Unit -> Finish')
    click ('Temperature Controller -> Finish')

    click ('Exit Qrius')

    #####################

    write ('execute : Set Multimeter to resistance mode')

    touch ('Multimeter probes', 'Sample PT100 terminals')
    sample_PT100_res = float(raw_input ('What is the resistance of sample PT100?'))
    write ('Sample PT100 Resistance : ', sample_PT100_res)

    touch ('Multimeter probes', 'PQMS PT100 terminals')
    PQMS_PT100_res = float(raw_input ('What is the resistance of PQMS PT100?'))
    write ('PQMS PT100 Resistance : ', PQMS_PT100_res)

    print ('Difference : ', abs(sample_PT100_res - PQMS_PT100_res))

    #####################