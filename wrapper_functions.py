from complex_functions import *

TEST_OBJECTS    = ["Insert_Susceptibility", "Insert_RT_Puck", "Insert_RT_Old", "Puck_Board"]
CRYOSTATS       = ["Cryostat_Quartz", "Cryostat_Steel"]
CHAMBERS        = ["Sample_Chamber", "Heater_Chamber"]

###############################################################################

def get_sample_info():

    sample_box = raw_input("\nSelect Sample box : (Box_Zener, Box_Resistor, Dessicator)\n")
    while((sample_box != "Box_Zener") and (sample_box != "Box_Resistor") and (sample_box != "Dessicator")):
        sample_box = raw_input("\nSelect Sample box : (Box_Zener, Box_Resistor, Dessicator)\n")

    if(sample_box=="Box_Zener"):
        sample = raw_input("\nSelect sample : (Zener_1, Zener_2, Zener_3)\n")
        while((sample != "Zener_1") and (sample != "Zener_2") and (sample != "Zener_3")):
            sample = raw_input("\nSelect sample : (Zener_1, Zener_2, Zener_3)\n")

    elif(sample_box=="Box_Resistor"):
        sample = raw_input("\nSelect sample : (Res_1,Res_2,Res_3,Res_4,Res_5,Res_6,Res_7, Res_8,Res_9,Res_10,Res_11,Res_12,Res_13,Res_14,Res_15,Res_16,Res_17,Res_18)\n")
        while((sample != "Res_1") and (sample != "Res_2") and (sample != "Res_3") and \
            (sample != "Res_4") and (sample != "Res_5") and (sample != "Res_6") and \
            (sample != "Res_7") and (sample != "Res_8") and (sample != "Res_9") and \
            (sample != "Res_10") and (sample != "Res_11") and (sample != "Res_12") and \
            (sample != "Res_13") and (sample != "Res_14") and (sample != "Res_15") and \
            (sample != "Res_16") and (sample != "Res_17") and (sample != "Res_18")):
            sample = raw_input("\nSelect sample : (Res_1,Res_2,Res_3,Res_4,Res_5,Res_6,Res_7, Res_8,Res_9,Res_10,Res_11,Res_12,Res_13,Res_14,Res_15,Res_16,Res_17,Res_18)\n")

    elif (sample_box == "Dessicator"):
        sample = raw_input("\nSelect sample : (YBCO_2, YBCO_1_A , YBCO_1_B, copper_wire)\n")
        while((sample != "YBCO_1") and (sample != "YBCO_2")and (sample != "YBCO_1_A")and (sample != "YBCO_1_B") and (sample != "copper_wire")):
            sample = raw_input("\nSelect sample : (YBCO_2,YBCO_1_A , YBCO_1_B, copper_wire)\n")
            
    sample_description  = raw_input("\nGive a brief sample desciption: \n")
    address             = raw_input("\nGive the path where you want to store experimental data : \n")
    return address, sample, sample_box, sample_description

def get_experimental_parameters_XL():

    step_size                   = raw_input("Enter step size : \n")
    max_depth                   = raw_input("Enter max_depth : \n")

    return step_size, max_depth

def get_lockin_aquisition_settings():

    drive_mode                  = raw_input("Enter the drive mode (current/voltage) : \n")
    drive_value                 = raw_input("Enter the " + drive_mode + " value : \n")
    delay                       = raw_input("Enter the delay time : \n")
    filter_length               = raw_input("Enter the filter length: \n")

    return drive_mode, drive_value, delay, filter_length

def get_experimental_parameters_XT_linear_ramp():

    frequency                = raw_input("Enter frequency (Hz) : \n")
    amplitude                = raw_input("Enter amplitude (mV) : \n")
    phase                    = raw_input("Enter phase     (degrees) : \n")

    initial_temperature      = float(raw_input("Enter Initial Temperature (K) : \n"))
    final_temperature        = float(raw_input("Enter Final Setpoint Temperature (K) : \n"))
    ramp_rate                = raw_input("Enter Ramp rate : \n")
    return initial_temperature, final_temperature, ramp_rate, frequency, amplitude, phase

def get_experimental_parameters_IV_stepped_ramp():

    V_range                  = raw_input("Enter Voltage Sweep Max (mV) : \n")
    V_step                   = raw_input("Enter Voltage Step Size (mV) : \n")
    I_range                  = raw_input("Enter Current Sweep Max (uA) : \n")
    I_step                   = raw_input("Enter Current Step Size (uA) : \n")
    max_power                = raw_input("Enter Max Power (mW): \n")

    initial_temperature      = float(raw_input("Enter Initial Temperature (K) : \n"))
    final_temperature        = float(raw_input("Enter Final Setpoint Temperature (K) : \n"))
    temperature_step         = float(raw_input("Enter Temperature Step (K) : \n"))
    return initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power

def get_experimental_parameters_RT_stepped_ramp():

    V_range                  = raw_input("Enter Voltage Sweep Max (mV) : \n")
    I_range                  = raw_input("Enter Current Sweep Max (uA) : \n")
    max_power                = raw_input("Enter Max Power (mW): \n")

    initial_temperature      = float(raw_input("Enter Initial Temperature (K) : \n"))
    final_temperature        = float(raw_input("Enter Final Setpoint Temperature (K) : \n"))
    temperature_step         = float(raw_input("Enter Temperature Step (K) : \n"))
    return initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power


def get_step_ramp_details():

    pre_stabilization_delay   = float(raw_input("Enter the pre-stabilization delay (in s):\n "))
    post_stabilization_delay  = float(raw_input("Enter the post-stabilization delay (in s):\n "))
    monitoring_period         = float(raw_input("Enter the monitoring period (in s):\n "))
    tolerance                 = float(raw_input("Enter the temperature tolerance (in K):\n "))

    return pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance

def get_experimental_parameters_R_Time_isothermal():

    run_mode                 = raw_input("Which mode do you want to do the run in (constant current/voltage):\n")
    V_range                  = raw_input("Enter Voltage Sweep Max (mV) : \n")
    I_range                  = raw_input("Enter Current Sweep Max (uA) : \n")
    max_power                = raw_input("Enter Max Power (mW): \n")
    temperature_set_point    = float(raw_input("Enter Heater Setpoint Temperature (K) : \n"))

    return temperature_set_point, V_range, I_range, max_power, run_mode

def get_experimental_parameters_R_Time_linear_ramp():

    run_mode                  = raw_input("Enter the R-Time run mode (current/voltage):\n")
    ramp_rate                 = raw_input("Enter Ramp rate : \n")
    initial_temperature       = float(raw_input("Enter the starting temperature (K):\n"))
    final_temperature         = float(raw_input("Enter the ending temperature (K):\n"))
    V_range                   = raw_input("Enter Voltage Sweep Max (mV) : \n")
    I_range                   = raw_input("Enter Current Sweep Max (uA) : \n")
    max_power                 = raw_input("Enter Max Power (mW): \n")

    return initial_temperature, final_temperature, ramp_rate, run_mode, I_range, V_range, max_power, ramp_rate

def get_experimental_parameters_CV_isothermal():
    run_mode                  = raw_input("Enter the CV run mode (V-Time / ):\n")
    initial_frequency         = float(raw_input("Enter the starting frequency (Hz):\n"))
    final_frequency           = float(raw_input("Enter the ending frequency (Hz):\n"))
    frequency_step            = raw_input("Enter frequency Step Size (Hz) : \n")
    reference_amplitude       = raw_input("Enter the amplitude of the sine wave signal generated across the terminals of the REF OUT port. Its range is 0 - 1000mV : \n")
    reference_frequency       = raw_input("Enter the frequency of the sine wave signal generated across the terminals of the REF OUT port. Its range in 10 - 10000 Hz : \n")
    reference_phase           = raw_input("Enter the phase difference in degrees of the sine wave signal generated across the terminals of the REF OUT port with respect to the internal reference. : \n")
    temperature_set_point    = float(raw_input("Enter Heater Setpoint Temperature (K) : \n"))


def get_experimental_parameters_bias_DC_voltage_measure():
    voltage_set_point    = float(raw_input("Enter Voltage Setpoint : \n"))

    return voltage_set_point

def get_experimental_parameters_AC_volatage_measure():
    reference_amplitude       = raw_input("Enter the amplitude of the sine wave signal generated across the terminals of the REF OUT port. Its range is 0 - 1000mV : \n")
    reference_frequency       = raw_input("Enter the frequency of the sine wave signal generated across the terminals of the REF OUT port. Its range in 10 - 10000 Hz : \n")
    reference_phase           = raw_input("Enter the phase difference in degrees of the sine wave signal generated across the terminals of the REF OUT port with respect to the internal reference. : \n")

    return reference_amplitude,reference_frequency,reference_phase


###############################################################################

def PQMS_IV_run (initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance):

    write("\n##############################################################")
    write("                   Run starts")
    write("##############################################################\n")

    start_IV_step_ramp_run  (initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance)

    write("\n##############################################################")
    write("                   Run ends")
    write("##############################################################\n")


def PQMS_RT_run_stepped_ramp (initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance):

    write("\n##############################################################")
    write("                   Run starts")
    write("##############################################################\n")

    start_RT_step_ramp_run  (initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance)

    write("\n##############################################################")
    write("                   Run ends")
    write("##############################################################\n")

def PQMS_R_Time_run_isothermal (run_mode,  I_range, V_range, max_power, temperature_set_point, number_of_measurements):

    for i in range(number_of_measurements):

	    write("\n##############################################################")
	    write("                   Run starts")
	    write("##############################################################\n")

	    set_XTCON_temperature (temperature_set_point)
	    start_R_Time_isothermal( I_range, V_range, max_power,  run_mode)

	    write("\n##############################################################")
	    write("                   Run ends")
	    write("##############################################################\n")

def PQMS_RT_run_linear_ramp (initial_temperature, final_temperature, ramp_rate, run_mode, I_range, V_range, max_power):

    write("\n##############################################################")
    write("                   Run starts")
    write("##############################################################\n")

    start_RT_linear_ramp (initial_temperature, final_temperature, ramp_rate, run_mode, I_range, V_range, max_power)

    write("\n##############################################################")
    write("                   Run ends")
    write("##############################################################\n")


###############################################################################

def select_test_object ():

    print "\n\n Available Test Objects : "
    print "______________________________\n"

    for item in TEST_OBJECTS:
        print item

    print "______________________________\n"
    test_object = raw_input ("Load Sample to which test_object? : \n")

    while (test_object not in TEST_OBJECTS):

        print "\n\n Available Test Objects : "
        print "______________________________\n"

        for item in TEST_OBJECTS:
            print item

        print "______________________________\n"
        test_object = raw_input ("Load Sample to which test_object? : \n")

    return test_object


def select_cryostat ():

    print "\n\n Available Cryostats : "
    print "______________________________\n"

    for item in CRYOSTATS:
        print item

    print "______________________________\n"
    cryostat = raw_input ("Load Insert to which Cryostat? : \n")

    while (cryostat not in CRYOSTATS):

        print "\n\n Available Cryostats : "
        print "______________________________\n"

        for item in CRYOSTATS:
            print item

        print "______________________________\n"
        cryostat = raw_input ("Load Insert to which Cryostat? : \n")

    return cryostat


def prepare_sample (Sample, Sample_Box, test_object):

    '''Asks the user if the sample is already soldered onto the test_object or is to be mounted during procedure'''

    mounted = raw_input( "\nIs the sample mounted on the puck? : y/n \n")
    while ((mounted != 'y') and (mounted != 'n')):
        mounted = raw_input( "\nIs the sample mounted on the puck? : y/n \n")

    if (mounted == 'n'):
        mount_sample (Sample, Sample_Box, test_object)

    elif (mounted == 'y'):
        print ("\nSample already mounted. Continue to next step.\n")
        sample_is_mounted()


def is_the_sample_loaded (Sample, Sample_Box, test_object, cryostat):

    '''Asks the user if the sample with the insert is already loaded in the cryostat or is to be loaded during procedure'''

    response = raw_input ("\nIs the insert with sample loaded into the cryostat? : y/n \n")
    while ((response != 'y') and (response != 'n')):
        response = raw_input ("\nIs the insert with sample loaded into the cryostat? : y/n \n")
    if (response == 'n'):
        load_sample (Sample, Sample_Box, test_object, cryostat)

def cables_connected_check (test_object, cryostat):

    response = raw_input ("Are the required cables already connected? : y/n\n")

    while (response != 'y' and response != 'n'):
        response = raw_input ("Are the required cables already connected? : y/n\n")

    if (response == 'n'):

        if (test_object == "Insert_RT_Puck"):

             conn = raw_input("Are the cables connected elsewhere?")

             while (conn != 'y' and conn != 'n'):
		      conn = raw_input ("Are the required cables already connected? : y/n\n")

             if (conn == 'n'):
            	connect_cable('RT_Cable', test_object)
            	connect_cable('HT_Cable', test_object)

             else:
            	disconnect_cable("RT_Cable")
            	disconnect_cable("HT_Cable")
            	connect_cable('RT_Cable', test_object)
            	connect_cable('HT_Cable', test_object)

        elif (test_object == "Puck_Board"):

            conn = raw_input("Are the cables connected elsewhere?")

            while (conn != 'y' and conn != 'n'):
		      conn = raw_input ("Are the required cables already connected? : y/n\n")

            if (conn == 'n'):
            	connect_cable('RT_Cable', test_object)

            else:
            	disconnect_cable("RT_Cable")
            	connect_cable('RT_Cable', test_object)


        elif (test_object == "Insert_RT_Old"):


            if (cryostat == "Cryostat_Steel"):
                conn = raw_input("Are the cables connected elsewhere?")

                while (conn != 'y' and conn != 'n'):
			conn = raw_input ("Are the required cables already connected? : y/n\n")

                if (conn == 'n'):
                	connect_cable('HT_Cable', cryostat + " cryostat's HT connector")
                	connect_cable('RT_Cable', cryostat + " cryostat's RT connector")

                else:
                	disconnect_cable("HT_Cable")
                	connect_cable('HT_Cable', cryostat + " cryostat's HT connector")
                	disconnect_cable("RT_Cable")
                	connect_cable('RT_Cable', cryostat + " cryostat's RT connector")


            elif (cryostat == "Quartz" ):
                throw_exception ("Can't use heater with " + cryostat + " cryostat and " + test_object)

            connect_cable('RT_Cable', test_object)

        elif (test_object == "Insert_Susceptibility"):

            if (cryostat == "Cryostat_Steel"):
                connect_cable('HT_Cable', cryostat + " cryostat's HT connector")

            elif (cryostat == "Quartz" ):
                throw_exception ("Can't use heater with " + cryostat + " cryostat and " + test_object)

            connect_cable('RT_Cable', test_object + "RT_Terminal")
            connect_cable('XLIA_Sus_Cable', test_object + "XLIA_Sus_Terminal")

def cables_disconnected_check (test_object, cryostat):

    response = raw_input ("Do you want to disconnect all cables after the experiment? : y/n\n")

    while (response != 'y' and response != 'n'):
    	response = raw_input ("Do you want to disconnect all cables after the experiment? : y/n\n")

    if (response == 'y'):

        if ((test_object == "Insert_RT_Puck") or (test_object == "Insert_RT_Old")):
            disconnect_cable("RT_Cable")
            disconnect_cable("HT_Cable")

        elif (test_object == "Puck_Board"):
            disconnect_cable ("Puck_Board")

        elif (test_object == "Insert_Susceptibility"):
            disconnect_cable("RT_Cable")
            disconnect_cable("HT_Cable")
            disconnect_cable("XLIA_Sus_Cable")


def remove_sample (Sample, Sample_Box, test_object):

    '''Asks the user if the sample the sample is to be desoldered from the test_object after completion of the procedure'''

    unmount = raw_input ("\nDo you want to unmount the sample from the " + test_object + " after the measurements? : y/n \n")
    while ((unmount != 'y') and (unmount != 'n')):

        unmount = raw_input ("\nDo you want to unmount the sample from the " + test_object + " after the measurements? : y/n\n")

    if (unmount == 'n'):
        print ("\n Not unmounting the sample from the " + test_object + ".\n")
        do_not_unmount()

    elif (unmount == 'y'):
        unmount_sample (Sample, Sample_Box, test_object)

###############################################################################

def need_liquid_nitrogen ():
    response = raw_input ("\nDo you want to pour liquid nitrogen? : y/n\n")
    while ((response!='y') and (response!='n')):
        response = raw_input ("\nDo you want to pour liquid nitrogen? : y/n\n")
    if (response == 'y'):
        pour_liquid_nitrogen()


def double_walled_steel_cryostat_environment_setup (previous_run_temperature, current_run_temperature, cryostat):

    flush_helium("Sample_Chamber", cryostat)
    flush_helium("Heater_Chamber", cryostat)

    if (previous_run_temperature == "" and current_run_temperature > 150):
        create_vaccum ("Heater_Chamber", cryostat)

    #switch cases
    elif (previous_run_temperature <=150 and current_run_temperature > 150):
        create_vaccum ("Heater_Chamber", cryostat)


def quartz_cryostat_environment_setup(previous_run_temperature, current_run_temperature, cryostat):

    flush_helium("Sample_Chamber", cryostat)

    if (previous_run_temperature == "" and current_run_temperature > 150):
        create_vaccum ("Sample_Chamber", cryostat)

    #switch cases
    elif (previous_run_temperature <=150 and current_run_temperature > 150):
        create_vaccum ("Sample_Chamber")



def reset_cryostat_environment (previous_run_temperature, temperature_set_point, cryostat):

  response = raw_input("Do you want to reset the cryostat environment?\n")
  while ((response != 'y') and (response != 'n')):
    response = raw_input ("Do you want to reset the cryostat environment?\n")
  if(response == 'y') and (cryostat == "Cryostat_Steel"):
  	double_walled_steel_cryostat_environment_setup(previous_run_temperature, temperature_set_point, cryostat)
  if(response == 'y') and (cryostat == "Quartz"):
  	quartz_cryostat_environment_setup(previous_run_temperature, temperature_set_point, cryostat)


def release_PQMS_vaccum (cryostat):

    print ("\nIt is NOT reccomended to release vaccum if there is still liquid nitrogen left in the cryocan.")
    response = raw_input ("Do you want to release vaccum? : y/n\n")

    if (cryostat == "Cryostat_Steel"):

        while ((response != 'y') and (response != 'n')):
            print ("\nIt is NOT reccomended to release vaccum if there is still liquid nitrogen left in the cryocan.")
            response = raw_input ("Do you want to release vaccum? : y/n\n")

        if (response == 'y'):
            for chamber in CHAMBERS[0:2] :
                sure = raw_input ("\nAre you SURE you want to release vaccum in " + chamber + " ? : y/n\n")
                while ((sure != 'y') and (sure != 'n')):
                    sure = raw_input ("\nAre you SURE you want to release vaccum in " + chamber + " ? : y/n\n")
                if (sure == 'y'):
                    release_pressure (chamber)

    elif (cryostat == "Quartz"):

        release_pressure ("Sample_Chamber")


def liquid_nitrogen_remaining (cryostat):

    response = raw_input ("Is liquid nitrogen left in the cryocan? : y/n\n")

    while ((response != 'y') and (response != 'n')):
        response = raw_input ("Is liquid nitrogen left in the cryocan? : y/n\n")

    if (response == 'y'):
        restore_vaccum (cryostat)

def turn_on_PQMS_modules():

    response = raw_input ("Is the PQMS already on? : y/n\n")

    while ((response != 'y') and (response != 'n')):
        response = raw_input ("Is the PQMS already on? : y/n\n")

    if (response == 'n'):
        switch_on_PQMS_modules()

def turn_off_PQMS_modules(cryostat):

    response = raw_input ("Do you want to turn off the PQMS? : y/n\n")

    while ((response != 'y') and (response != 'n')):
        response = raw_input ("Do you want to turn off the PQMS? : y/n\n")

    if (response == 'y'):
        switch_off_PQMS_modules(cryostat)

def turn_off_computer ():

    response = raw_input ("Do you want to turn off the computer? : y/n\n")

    while ((response != 'y') and (response != 'n')):
        response = raw_input ("Do you want to turn off the computer? : y/n\n")

    if (response == 'y'):
        switch_off_computer()

def turn_on_computer():

    response = raw_input ("Is the Computer already on? : y/n\n")

    while ((response != 'y') and (response != 'n')):
        response = raw_input ("Is the Computer already on? : y/n\n")

    if (response == 'n'):
        switch_on_computer()

def is_XL_run_needed(final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value):

    condition = raw_input("Do you want to do X-L run? (y/n): \n")
    if (condition == 'y'):
    	start_XL_run(final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value)

def take_photo_of_sample(Sample,Sample_Box):

    write       ("execute : Cut and put a fresh sheet of tracing paper on sample_photography_area")

    remove      ('cap',Sample_Box)
    write       ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+",State,OPEN")

    hold_sample (Sample, Sample_Box)
    close_lid   (Sample_Box)
    write       ("execute : Remove Sticky Tape from "+ Sample)
    write   ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+","+Sample+",State,NOT_IN_USE")


    goto        ('Sample_Photography_Area')
    leave       (Sample)
    write       ("execute : Light up the Sample_Photography_Area")
    write       ("execute : Put a meter scale on the side of the photo")

    take_photo  (Sample)
    write   ("execute : straighten sample")
    write   ("execute : put a sticky note on the sample")

    read_state("Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box)

    goto    (Sample_Box +"'s Cap")
    hold    ("The Cap")
    write   ("execute : With other hand hold the " + Sample_Box + " and keep it fixed")
    write   ("execute : Pull the cap, and separate it from sample_box")
    write   ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,OPEN")
    goto    (Sample+"_Terminal_1")
    hold    (Sample+"_terminal_1")
    goto    (Sample+".Home_Coordinates")
    leave   (Sample)

    write   ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+","+Sample+",State,NOT_IN_USE")
    write   ("execute : close the lid of the box")
    write   ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,CLOSED")
    goto    ("Tweezer.Home_Coordinates")
    leave   ("Tweezer")
