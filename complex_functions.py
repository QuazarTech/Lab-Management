import time
from primitive_functions import *

#####################################################################
#general user functions

def set_option (parameter, menu, parameter_value):
    move_cursor(parameter + " " + menu)
    click (menu)
    type_text (parameter_value)
    type_text ('Enter')

def open_valve (valve, direction):
    rotate(valve, "maximum possible turns", direction)
    update_database(valve + ",State,OPEN")

def close_valve (valve, direction):
    goto(valve)
    rotate(valve, "maximum possible turns", direction)
    update_database(valve + ",State,CLOSED")

def open_slightly (valve, direction):
    rotate(valve, "minimum no of turns", direction)
    update_database(valve + ",State,OPEN")

def move(obj, position):
    '''Move obj to position'''
    goto(obj)
    hold(obj)
    goto(position)

def remove(obj1, obj2):
    '''Removes/separates obj1 from obj2'''

    read_state ('Lab_Space,Sample_Table')

    goto(obj2 + "." + obj1)
    hold(obj2 + "." + obj1)

    hold(obj2)
    move(obj1, " away from " + obj2)

def hold_sample(Sample, Sample_Box):
    '''Correctly hold a sample using tweezers'''

    goto('Tweezers')
    hold('Tweezers')

    goto(Sample + ".Home_Coordinates")
    hold(Sample + ".Terminal_1")
    goto("Sample_Mounting_Coordinates")

    update_database ("Lab_Space,Sample_Table,Sample_Boxes," + Sample_Box + "," + Sample + ",State,IN_USE")

def close_lid(obj):
    '''close lid of object'''
    move(obj + ".lid", obj)

    update_database ("Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,CLOSED")

def take_photo(obj):
    '''Capture photograph of obj'''
    move ("Camera", "camera_focal_length distance from " + obj)
    face ("Camera", obj)
    click("Capture Button")


#####################################################################
#runtime database checking functions

def wait(obj, condition):

    check(obj, condition)
    response = raw_input ("Is the " + obj + " " + condition + "? : y/n\n")

    while ((response != 'y') and (response != 'n')):
        response = raw_input ("Is the " + obj + " " + condition + "? : y/n\n")

    if (response == 'n'):
        write("\n########### WAITING ###########\n")
        write("Waiting for " + obj + "->" + condition)
        raw_input ("Press enter when the wait is complete")
        write("\n######### WAIT COMPETE ########\n")

def ensure(key, value):
	print ("Test : " + key + " --> " + value + "\n")
	print ("Checking...........................\n")

	if check_database (key, value):
		write(key + " is " + value + " : Check Passed\n")
	else:
		throw_exception (key + " is not " + value + " : Check Failed\n")

###############################################################################

def rapid_movement():
    write("***********Next few steps have to be performed rapidly********************")

def end_rapid_movement():
    write("***********Rapid Movement period is over, steps can be performed at normal speed****************")

###############################################################################
#soldering iron related functions

def set_up_soldering_iron():
    '''Set up soldering space and iron for use'''

    goto('Soldering_Iron')
    wait("Soldering_Iron", "Free")
    leave("test_object")

    switch_on("Soldering_Iron")
    update_database ("Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,ON")
    wait("soldering iron LED", "blinking.")

def solder (terminal_a, terminal_b):
    '''Solder terminal_b onto terminal_b, given Sample from Sample_Box'''

    update_database ("Lab_Space,Sample_Table,Soldering,Soldering_Iron,State,IN_USE")

    move ("Soldering_Iron", "Flux.Home_Coordinates")
    touch("Soldering_Iron.Tip", "Flux")

    goto ("Solder_Wire.Tip")
    touch("Soldering_Iron.Tip", "Solder_Wire.Tip")

    goto("Juntion of " + terminal_a + " and " + terminal_b)
    wait("soldering between " + terminal_a + " and " + terminal_b, "complete")

    goto ('Cleaning_Pad.Home_Coordinates')
    touch("Soldering_Iron.Tip", "Cleaning_Pad")

    goto ('Soldering_Iron.Home_Coordinates')
    leave('Soldering_Iron')

    update_database ("Lab_Space,Sample_Table,Soldering,Soldering_Iron,State,NOT_IN_USE")

def desolder(terminal, Sample, Sample_Box):
    '''Desolder terminal of Sample'''

    update_database ("Lab_Space,Sample_Table,Soldering,Soldering_Iron,State,IN_USE")

    move ("Soldering_Iron", "Flux.Home_Coordinates")
    touch("Soldering_Iron.Tip", "Flux")


    goto(Sample + "." + terminal)
    wait("desoldering", "complete")

    goto ("Cleaning_Pad.Home_Coordinates")
    touch("Soldering_Iron.Tip", "Cleaning_Pad")

    update_database ("Lab_Space,Sample_Table,Sample_Boxes," + Sample_Box + "," + Sample + ",Terminal_1,Soldered,NO")
    update_database ("Lab_Space,PQMS,Insert_RT_Puck,Puck,Terminal_1,Soldered,NO")
    update_database ("Lab_Space,Sample_Table,Soldering,Soldering_Iron,State,NOT_IN_USE")


#####################################################################
#clamp related functions


def clamp():
    '''Clamp PQMS insert to Cryostat'''

    read_state ('Lab_Space,PQMS,Clamp')
    move       ('Clamp.Home_Coordinates', 'PQMS.Clamp_Coordinates')
    write      ("execute : Use the other hand to revolve the clamp till 180 degrees")
    write      ("execute : Revolve the screw of the clamp till it is in closing position")
    rotate     ('Clamp Screw','required turns','clockwise')
    update_database ("Lab_Space,PQMS,Clamp,State,LOCKED")

def unclamp():
    '''Unclamp the PQMS insert to Cryostat'''

    read_state("Lab_Space,PQMS,Clamp")
    read_state("Lab_Space,PQMS,Insert_RT_Puck")

    goto  ("Clamp.Current_Coordinates")
    hold  ("the clamp with one hand")
    rotate("Clamp Screw", "required turns", "anti-clockwise")
    write ("execute : Revolve the screw of the clamp till it is in opening position")
    write ("execute : Use the other hand to revolve the clamp till it's straight.")

    update_database ("Lab_Space,PQMS,Clamp,State,UNLOCKED")

    goto        ("Clamp.Home_Coordinates")
    leave       ("Clamp")


#####################################################################
#cable related functions


def connect_cable (cable, test_object):
    '''Connects 'cable' to its respective connector on test_object.'''

    read_state('Lab_Space,PQMS,Cables,' + cable)
    move      (cable + ".Cryostat_End", test_object + "." + cable + "_Terminal")
    align     (cable + "'s connector", test_object + "'s connector")
    write     ("execute : Insert and fasten " + cable)
    leave     (cable)

    update_database ("Lab_Space,PQMS,Cables," + cable + ",State,CONNECTED")


def disconnect_cable (cable):
    '''Disconnects 'cable' from its respective connector on any test_object.'''

    read_state  ('Lab_Space,PQMS,Cables,' + cable)
    goto        (cable + ".Current_Coordinates")
    hold        (cable + ".Cryostat_End")

    write       ("execute : Unfasten and remove " + cable)
    goto        (cable + ".Home_Coordinates" )
    update_database ("Lab_Space,PQMS,Cables," + cable + ",State,DISCONNECTED")
    leave       (cable)


#####################################################################
#sample unloading and loading functions

def mount_sample (Sample, Sample_Box, test_object):
    '''Mount 'Sample' from 'Sample_Box' onto Sample Puck'''

    read_state  ('Lab_Space,Sample_Table')
    read_state  ('Lab_Space,PQMS')

    if ((test_object == "Insert_RT_Puck") or (test_object == "Puck_Board")):

        move        ('Puck_Board','Sample_Mounting_Coordinates')
        leave       ('Puck_Board')
        remove      ('cap',Sample_Box)
        update_database ("Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+",State,OPEN")

        hold_sample (Sample, Sample_Box)
        close_lid   (Sample_Box)
        write       ("execute : Remove Sticky Tape from " + Sample)

        #Photograph prior to mounting
        write       ("execute : Cut and put a fresh sheet of tracing paper on sample_photography_area")
        goto        ('Sample_Photography_Area')
        leave       (Sample)
        write       ("execute : Light up the Sample_Photography_Area")
        write       ("execute : Put a Scale on the side of the photo")

        take_photo  (Sample)
        write 		("execute : Take sample back to Sample_Mounting_Coordinates")
        write 		("execute : Take Scale back to Scale.Home_Coordinates")

        goto    ('Puck_Board')
        hold    ('Puck_Board')

        #SOLDERING PROCESS

        set_up_soldering_iron()

        move(Sample+'.Terminal_1', 'Insert_RT_Puck,Puck,Terminal_1')
        solder(Sample +',Terminal_1', 'Insert_RT_Puck,Puck,Terminal_1')

        write ("execute : Bend " + Sample + "'s terminals as required.")

        move  (Sample+"'s Terminal_2", "Insert_RT_Puck,Puck,Terminal_4")
        solder(Sample + "'s,Terminal_2", "Insert_RT_Puck,Puck,Terminal_4")

        ############# 4-probe vs 2-probe topology selection ##############
        response = raw_input ("Do you want to mount in 4-probe topology? : y/n")
        while ((response != 'y') and (response != 'n')):
            response = raw_input ("Do you want to mount in 4-probe topology? : y/n")

        if response == 'y':
            move ("copper_wire_1_terminal_1", "Insert_RT_Puck,Puck,Terminal_2")
            solder ("copper_wire_1_terminal_1", "Insert_RT_Puck,Puck,Terminal_2")
            move ("copper_wire_2_terminal_1", "Insert_RT_Puck,Puck,Terminal_3")
            solder ("copper_wire_2_terminal_1", "Insert_RT_Puck,Puck,Terminal_3")

            move ("copper_wire_1_terminal_2", Sample + ".Terminal_1_interior")
            solder ("copper_wire_1_terminal_2", Sample + ".Terminal_1_interior")
            move ("copper_wire_2_terminal_2", Sample + ".Terminal_2_interior")
            solder ("copper_wire_2_terminal_2", Sample + ".Terminal_2_interior")


        elif response == 'n':
            solder ("Insert_RT_Puck,Puck,Terminal_1", "Insert_RT_Puck,Puck,Terminal_2")
            solder ("Insert_RT_Puck,Puck,Terminal_3", "Insert_RT_Puck,Puck,Terminal_4")


        update_database ("Lab_Space,PQMS,Insert_RT_Puck,Puck,Sample_Mounted,YES")
        write("execute : Switch off the soldering iron")
        update_database ("Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,OFF")

        #SOLDERING PROCESS

        read_state('Lab_Space,Sample_Table')
        read_state('Lab_Space,PQMS')

        move ('Puck_Board', 'Puck_Board.Home_Coordinates')
        leave('Puck_Board')
        take_photo('Mounted Sample')

    elif (test_object == "Insert_RT_Old"):

        remove      ('cap',Sample_Box)
        update_database ("Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+",State,OPEN")

        hold_sample (Sample, Sample_Box)
        close_lid   (Sample_Box)
        write       ("execute : Remove Sticky Tape from "+ Sample)
        #####PHOTOGRAPH PRIOR TO MOUNTING
        write       ("execute : Cut and put a fresh sheet of tracing paper on sample_photography_area")

        goto        ('Sample_Photography_Area')
        leave       (Sample)
        write       ("execute : Light up the Sample_Photography_Area")
        write       ("execute : Put a meter scale on the side of the photo")

        take_photo  (Sample)
        write 		("execute : Take sample back to Sample_Mounting_Coordinates")



        goto    ("Insert_RT_Old")
        hold    ("Insert_RT_Old")

        #SOLDERING PROCESS
        set_up_soldering_iron()

        move(Sample+'.Terminal_1', 'Insert_RT_Old,Terminal_1')
        solder(Sample + ',Terminal_1', 'Insert_RT_Old,Terminal_1')

        write ("execute : Bend " + Sample + "'s terminals as required.")

        move(Sample+'.Terminal_2', 'Insert_RT_Old,Terminal_4')
        solder(Sample+',Terminal_2', 'Insert_RT_Old,Terminal_4')

        update_database ("Lab_Space,PQMS,Insert_RT_Old,Sample_Mounted,YES")
        write("execute : Switch off the soldering iron")
        update_database ("Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,OFF")
        #SOLDERING PROCESS

        write("execute : Stick " + Sample + "'s body to the mounting surface with Kapton tape")
        goto("Insert_RT_Old.Home_Coordinates")

    goto('Tweezers.Home_Coordinates')
    leave('Tweezers')
    take_photo('Mounted Sample')


def load_sample(Sample, Sample_Box, test_object, cryostat):

    write ("Insert is being loaded to " + cryostat + " cryostat...\n")

    if (test_object == "Insert_RT_Puck"):

        response = raw_input ("\nIs the puck connected to the insert? : y/n \n")
        while ((response != 'y') and (response != 'n')):
            response = raw_input ("\nIs the puck connected to the insert? : y/n \n")

        if (response == 'n'):
            remove          ('Puck','Puck_Board')
            update_database ("Lab_Space,PQMS,Insert_RT_Puck,Puck,Puck_Board_Connection,DISCONNECTED")

            goto('Puck_Screwing_Coordinates')
            leave('Puck')
            read_state('Lab_Space,PQMS,Insert_RT_Puck')
            move(test_object, 'Cryostat.Exit_Coordinates')
            goto('Puck_Screwing_Coordinates')
            hold ('Puck')
            align("Puck", "Insert_RT_Puck.Cavity")
            rotate('Puck','14 turns','clockwise')
            align ("Insert2Puck Cable", "Puck.Female_Connector")
            write("execute : Insert the pin_holes into the puck pins")
            update_database ("Lab_Space,PQMS,Insert_RT_Puck,Puck,Insert_Connection,CONNECTED")
            update_database ("Lab_Space,PQMS,Insert_RT_Puck,Insert2Puck_Cable,State,CONNECTED")

        flush_helium('Sample_Chamber', cryostat)
    	unclamp()

        move ('Cryostat_Cover', 'Cryostat_Cover.Home_Coordinates')
    	leave('Cryostat_Cover')
        move (test_object, 'Cryostat.Exit_Coordinates')
        goto('Cryostat.Home_Coordinates')

        clamp()


    elif (test_object == "Puck_Board"):

        write ("Sample Puck is already connected to Puck_Board")
        move ("Puck_Board", "PQMS.Home_Coordinates")

    elif (test_object == "Insert_RT_Old"):

        flush_helium('Sample_Chamber', cryostat)

    	unclamp()

        move ('Cryostat_Cover', 'Cryostat_Cover.Home_Coordinates')
    	leave('Cryostat_Cover')

        move(test_object, 'Cryostat.Exit_Coordinates')
        goto ("Cryostat.Home_Coordinates")

        clamp()

    elif (test_object == "Insert_Susceptibility"):

        flush_helium('Sample_Chamber', cryostat)

    	unclamp()

        move ('Cryostat_Cover', 'Cryostat_Cover.Home_Coordinates')
    	leave('Cryostat_Cover')

        move(test_object, 'Cryostat.Exit_Coordinates')
        goto ("Cryostat.Home_Coordinates")

        clamp()

        write("execute : Ensure that the sample positioner collar is in place")
        write("execute : Insert the " + test_object + " sample platform into the " + test_object + ", through the collar")
        move ("Collar_Screw, Sample_Positioner_Collar")
        write("execute : Fasten the collar screw with the LN Key")
        set_positioner(60)


def unmount_sample (Sample, Sample_Box, test_object):
    '''Unmount Sample from puck and replace in Sample_Box'''

    if ((test_object == "Insert_RT_Puck") or (test_object == "Puck_Board")):

        goto    ("Puck_Board", "Tweezers.Home_Coordinates")
        hold    ("Tweezers")

        # Desoldering process
        set_up_soldering_iron()

        goto    (Sample + ".Terminal_1")
        hold    (Sample + ".Terminal_1")
        desolder("Terminal_1", Sample, Sample_Box)

        goto    (Sample + ".Terminal_2")
        hold    (Sample + ".Terminal_2")
        desolder("Terminal_2", Sample, Sample_Box)

        goto   ('Soldering_Iron.Home_Coordinates')
        leave  ('Soldering_Iron')

        update_database ("Lab_Space,PQMS,Insert_RT_Puck,Puck,Sample_Mounted,NO")

        write   ("execute : Switch off Soldering Iron")
        update_database ("Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,OFF")
        #Desoldering Process

        move    ("Puck_Board", "Puck_Board.Home_Coordinates")
        leave   ("Puck_Board")

        goto    ("Sample_Table.Sample_Mounting_Coordinates")
        write   ("execute : straighten sample")
        write   ("execute : put a sticky note on the sample")
        leave   (Sample)

        read_state("Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box)

        goto    (Sample_Box +"'s Cap")
        hold    ("The Cap")
        write   ("execute : With other hand hold the " + Sample_Box + " and keep it fixed")
        write   ("execute : Pull the cap, and separate it from sample_box")
        update_database ("Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,OPEN")
        goto    (Sample+"_Terminal_1")
        hold    (Sample+"_terminal_1")
        goto    (Sample+".Home_Coordinates")
        leave   (Sample)

        update_database ("Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+","+Sample+",State,NOT_IN_USE")
        write   ("execute : close the lid of the box")
        update_database ("Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,CLOSED")
        goto    ("Tweezer.Home_Coordinates")
        leave   ("Tweezer")

    elif (test_object == "Insert_RT_Old"):

        goto    ("Insert_RT_Old")
        hold    ("Insert_RT_Old")
        goto    ("Tweezers.Home_Coordinates")
        hold    ("Tweezers")

        # Desoldering process
        set_up_soldering_iron()

        goto    (Sample + ".Terminal_1")
        hold    (Sample + ".Terminal_1")
        desolder("Terminal_1", Sample, Sample_Box)

        goto    (Sample + ".Terminal_2")
        hold    (Sample + ".Terminal_2")
        desolder("Terminal_2", Sample, Sample_Box)

        goto   ('Soldering_Iron.Home_Coordinates')
        leave  ('Soldering_Iron')

        update_database ("Lab_Space,PQMS,Insert_RT_Old,Sample_Mounted,NO")

        write   ("execute : Switch off Soldering Iron")
        update_database ("Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,OFF")
        #Desoldering Process

        write   ("execute : Remove tape from Zener Diode")

        move    ("Insert_RT_Old", "Insert_RT_Old.Home_Coordinates")

        goto    ("Sample_Table.Sample_Mounting_Coordinates")
        write   ("execute : straighten sample")
        write   ("execute : put a sticky note on the sample")
        leave   (Sample)


        goto    (Sample_Box +"'s Cap")
        hold    ("The Cap")
        write   ("execute : With other hand hold the " + Sample_Box + " and keep it fixed")
        write   ("execute : Pull the cap, and separate it from sample_box")
        update_database ("Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,OPEN")
        goto    (Sample + "_Terminal_1")
        hold    (Sample + "_terminal_1")
        goto    (Sample + ".Home_Coordinates")
        leave   (Sample)

        update_database ("Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+","+Sample+",State,NOT_IN_USE")
        write   ("execute : close the lid of the box")
        update_database ("Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,CLOSED")
        goto    ("Tweezer.Home_Coordinates")
        leave   ("Tweezer")


def unload_sample(Sample, Sample_Box, test_object, cryostat):

    if (test_object == "Insert_RT_Puck"):

        unclamp()

        move("Insert_RT_Puck", "Cryostat.Exit_Coordinates")
        hold("Insert_RT_Puck")

        move ("Cryostat.cover", "Cryostat Opening")
        leave("Cryostat.cover")

        create_vaccum ("Sample_Chamber", cryostat)
    	if (cryostat == "Cryostat_Steel"):
            create_vaccum('Heater_Chamber', cryostat)

        goto("Sample_Table.Puck_Screwing_Coordinates")
        remove("Insert2Puck_Cable", "Insert_RT_Puck")

        update_database ("Lab_Space,PQMS,Insert_RT_Puck,Puck,Insert_Connection,DISCONNECTED")
        update_database ("Lab_Space,PQMS,Insert_RT_Puck,Insert2Puck_Cable,State,DISCONNECTED")
        read_state("Lab_Space,PQMS,Insert_RT_Puck,Puck")

        goto("Puck")
        hold("Puck")
        rotate('Puck','14 turns','anticlockwise')
        leave("Puck")

        goto(test_object + ".Home_Coordinates")
        leave(test_object)

        goto("Sample_Table.Puck_Screwing_Coordinates")
        hold("Insert_RT_Puck.Puck")
        goto("Puck_Board.Home_Coordinates")
        align ("Puck.pins", "Puck_Board")
        write("execute : Insert Puck into Puck_Board")
        leave("Puck")

        clamp()

        update_database ("Lab_Space,PQMS,Insert_RT_Puck,Puck,Puck_Board_Connection,CONNECTED")

    elif (test_object == "Puck_Board"):

        move(test_object, test_object + ".Home_Coordinates")

    elif (test_object == "Insert_RT_Old"):

        flush_helium('Sample_Chamber', cryostat)

        unclamp()
        move (test_object, test_object + ".Exit_Coordinates")

        move ("Cryostat.cover", "Cryostat Opening")
        leave("Cryostat.cover")

        create_vaccum ("Sample_Chamber", cryostat)
    	if (cryostat == "Cryostat_Steel"):
            create_vaccum('Heater_Chamber', cryostat)

        clamp()

        goto (test_object + ".Home_Coordinates")


    elif (test_object == "Insert_Susceptibility"):

        flush_helium('Sample_Chamber', cryostat)

        move ("Collar_Screw, ", "away from Sample_Positioner_Collar")
        write("execute : Unfasten the collar screw with the LN Key")

    	unclamp()


    	################################

    	write ("execute : Attention : 2 ROBOTS needed to complete procedure below. ROBOT_2 Must wear gloves!")
    	write ("execute : ROBOT_2   : Place a tissue paper on the Sample Mounting coordinates ")

    	write("execute : ROBOT_1 : Hold the sample positioner collar")

        write("execute : ROBOT_1 : Remove the " + test_object + " sample platform from the " + test_object + ", through the collar\n")

        write("execute : ROBOT_1 : Hand Over the sample platform to ROBOT_2\n \
                         ROBOT_2 : Goto Sample Mounting coordinates and immediately dry the sample and insert by wrapping delicately in tissue wipe.\n \
                         ROBOT_1 : Remove the sample positioner collar\n \
                         ROBOT_1 : Move "  + test_object + "Cryostat.Exit_Coordinates\n \
                         ROBOT_1 : Place the cryostat cover on the opening ")

        create_vaccum ("Sample_Chamber", cryostat)
    	if (cryostat == "Cryostat_Steel"):
            create_vaccum('Heater_Chamber', cryostat)

        clamp()

        write ("execute : ROBOT_2 : Remove the sample from the sleeve by gently pulling with tweezer")

        write ("execute : ROBOT_1 : Open the Dessicator Lid \n \
ROBOT_2 : Leave sample stage, Place the sample in its pouch, put it the dessicator and close the lid of the dessicator")

        write ("execute : ROBOT_1 : Move insert to Insert_Susceptibility.Home_Coordinates")

    	write ("execute : ROBOT_2 move sample stage to Insert_Susceptibility.Home_Coordinates")

    	################################


#####################################################################
#PQMS setup functions

def switch_on_module(module):
    goto     (module + ",Power_Cable")
    switch_on(module)
    update_database ("Lab_Space,PQMS,"+module+",State,ON")

def switch_off_module(module):
    goto     (module + ",Power_Cable")
    switch_on(module)
    update_database ("Lab_Space,PQMS,"+module+",State,OFF")

def switch_on_PQMS_modules():

    switch_on_module('Stabilizer')
    switch_on_module('XPLORE_Power_Supply')

    update_database ("Lab_Space,PQMS,XSMU,State,ON")

    switch_on_module('XTCON')
    switch_on_module('XLIA')
    switch_on_module('Sample_Positioner')
    switch_on_module('Pump')
    switch_on_module('Pirani_Gauge')

def pc_connect(module):
    click (module)
    move_cursor ("File")
    click ("File")
    click ("Connect")

def set_up_PQMS_modules ():

    click ('Modules Manager')
    pc_connect ("Temperature Controller")
    pc_connect ("IV Source and Measurement")
    pc_connect ("Lockin Amplifier")
    pc_connect ("Sample Positioner")


def switch_off_PQMS_modules(cryostat):

    switch_off_module("XPLORE_Power_Supply")
    update_database ("Lab_Space,PQMS,XSMU,State,OFF")

    switch_off_module("XTCON")
    switch_off_module('XLIA')
    switch_off_module('Sample_Positioner')

    close_valve ("Lab_Space,PQMS,Pump,Main_Valve", "clockwise")

    pre_pumping_checks(cryostat)

    switch_off_module('Pump')
    switch_off_module('Pirani_Gauge')
    switch_off_module('Stabilizer')


###############################################################################
#Computer functions

def switch_on_computer():

    switch_on("Computer.Switch")
    press    ("CPU Power Button")
    switch_on("USB_Power_Adaptor")
    write    ("execute : Login to user account")
    write    ("execute : Open Qrius ")

def switch_off_computer():

    write     ("execute : Exit Qrius")
    goto      ("Top Right Corner of the screen")
    click     ("Power Button")
    click     ("Shut Down")
    switch_off("USB_Power_Adaptor")
    wait      ("computer", "Shutdown")
    switch_off("Computer")

###############################################################################
#Sample Positioner Functions

def set_positioner(position):

    click       ('Qrius Window->Modules Manager->Sample Positioner Window')
    move_cursor ('Toolbar')
    click       ('Tools')
    set_option  ('Move Absolute', 'Text Box', str(position))

###############################################################################
#Temperature controller functions

def init_XTCON_isothermal (test_object):

    click       ('Temperature Controller Window')
    move_cursor ('Control mode')
    click       ('drop down menu')
    click       ('Isothermal')
    move_cursor ('Instrument Control')
    click       ('Cryostat and Insert')
    click       ('Cryostat Type')
    write       ('execute : select appropriate cryostat')
    click       ('Insert Type')
    click       (test_object)
    click       ('File->Hide')
    click       ('Start Button')
    update_database ("Lab_Space,PQMS,XTCON,Running,True")

def set_XTCON_temperature (temperature_set_point):

    click       ('Temperature Controller Window')
    move_cursor ('Toolbar')
    click       ('Settings->Isothermal Settings')
    set_option  ('Heater Setpoint', 'Text Box', str(temperature_set_point))
    move_cursor ('Toolbar')
    click       ('File->Apply')
    update_database ("Lab_Space,PQMS,XTCON,Mode,ISOTHERMAL")
    wait ("Sample Temperature", "Stable")

def stop_XTCON_run():
    click       ('Temperature Controller Window')
    move_cursor ('Stop Button')
    click       ('Stop')
    update_database ("Lab_Space,PQMS,XTCON,Running,False")

def start_XTCON_monitor():
    click       ('Temperature Controller Window')
    move_cursor ('Control mode')
    click       ('drop down menu')
    click       ('Monitor')
    click       ('Start Button')
    update_database ("Lab_Space,PQMS,XTCON,Running,True")

def end_XTCON_monitor():
    click       ('Temperature Controller Window')
    move_cursor ('Finish Button')
    click       ('Finish')


##############################################################################
# CV_isothermal functions

def init_XSMU_constant_volatge (test_object):
    click       ('IV Source and Measureent Unit Window')
    move_cursor ('Run mode')
    click       ('drop down menu')
    click       ('V-Time')
    click       ('Start Button')
    update_database ("Lab_Space,PQMS,XSMU,Running,True")


def set_XSMU_constant_volatge(voltage_set_point):
    click       ('IV Source and Measureent Unit Window')
    move_cursor ('Toolbar')
    click       ('Settings->Source Parameters')
    move_cursor ("Source Mode Drop Down Menu")
    click       ("Drop Down Menu")
    click       ("Constant Voltage")
    move_cursor ("Top menu")
    set_option  ('Voltage Values', 'Text Box', str(voltage_set_point))
    move_cursor ('Toolbar')
    click       ('File->Apply')
    wait        ("Voltage", "Stable")

def init_XLIA_isothermal_constant_voltage(test_object):
    click('Lock-In Amplifier Window')
    move_cursor ('Run mode')
    click       ('drop down menu')
    click       ('V-F')


def set_XLIA_isothermal_constant_voltage(initial_frequency,final_frequency,frequency_step,reference_amplitude,reference_frequency,reference_phase,run_mode):
    click       ('Lock-In Amplifier Window')
    move_cursor ('Toolbar')
    click       ('Settings -> V-F Ramp Settings')
    set_option  ('Initial Frequency', 'Text Box', str(initial_frequency))
    set_option  ('Final Frequency', 'Text Box', str(final_frequency))
    set_option  ('Frequency Step', 'Text Box', str(frequency_step))
    click       ('File -> Apply')
    move_cursor ('Toolbar')
    click       ('Settings -> Reference Settings')
    set_option  ('Frequency', 'Text Box', str(reference_frequency))
    set_option  ('Amplitude', 'Text Box', str(reference_amplitude))
    set_option  ('Phase', 'Text Box', str(reference_phase))
    click       ('File -> Apply')
    move_cursor ('Run control')
    click       ('Start Button')

###############################################################################
#XT_step_ramp_functions

def set_XL_measurement_settings(final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value):

    move_cursor ('Run control')
    click       ('drop down menu')
    click       ('X-L')

    move_cursor ('Toolbar')
    click       ('Settings->XL Acquisition Settings')

    set_option  ("Max Depth", "Text Box" , max_depth)
    set_option  ("Step Size", "Text Box" , step_size)

    click       ('File->Apply')

    move_cursor ('Toolbar')
    click       ('Settings->Lock-In Amplifier->Reference Settings')
    set_option  ('Frequency', 'Text Box', frequency)
    set_option  ('Amplitude', 'Text Box', amplitude)
    set_option  ('Phase', 'Text Box', phase)
    click       ("\'File->Apply\'")

    move_cursor ("Toolbar")
    click       ('Settings->Lock-In Amplifier->Acquisition Settings')
    set_option  ('Delay', 'Text Box', delay)
    set_option  ('Filter_Length', 'Text Box', filter_length)
    set_option  ('Drive Mode', 'Text Box', drive_mode)
    set_option  (drive_mode, 'Text Box', drive_value)

    move_cursor ("Toolbar")
    click       ('Settings->Lock-In Amplifier->Measurement Settings')
    move_cursor ("Coupling Drop Down Menu")
    click       ("Drop Down Menu")
    click       ("AC")

    click       ("\'File->Apply\'")

    ################################


def set_XT_linear_ramp_measurement_settings(final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value):
    #####       set linear ramp settings here

    move_cursor ('Run control')
    click       ('drop down menu')
    click       ('X-T (linear ramp)')

    move_cursor ('Toolbar')
    click       ('Settings->Temperature controller')
    click       ('Linear ramp settings')
    set_option  ('Final Temperature', "Text Box", str(final_temperature))
    set_option  ('Ramp Rate', 'Text Box', str(ramp_rate))
    click       ('File->Apply')

    move_cursor ('Toolbar')
    click       ('Settings->Lock-In Amplifier->Reference Settings')
    set_option  ('Frequency', 'Text Box', frequency)
    set_option  ('Amplitude', 'Text Box', amplitude)
    set_option  ('Phase', 'Text Box', phase)
    click       ("\'File->Apply\'")

    move_cursor ("Toolbar")
    click       ('Settings->Lock-In Amplifier->Acquisition Settings')
    set_option  ('Delay', 'Text Box', delay)
    set_option  ('Filter_Length', 'Text Box', filter_length)
    set_option  ('Drive Mode', 'Text Box', drive_mode)
    set_option  (drive_mode, 'Text Box', drive_value)

    move_cursor ("Toolbar")
    click       ('Settings->Lock-In Amplifier->Measurement Settings')
    move_cursor ("Coupling Drop Down Menu")
    click       ("Drop Down Menu")
    click       ("AC")
    click       ("\'File->Apply\'")

    ################################



def start_XL_run (final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value):

    goto        ("Qrius Main Window")
    click       ('Measurement Mode settings')
    click       ('Magnetic AC Susceptibility')

    set_XL_measurement_settings(final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value)
    update_database ("Lab_Space,PQMS,XTCON,Mode,Linear_Ramp")

    click ('Start Button')
    update_database ("Lab_Space,PQMS,XLIA,Running,True")
    wait ("Run", "Finished")

    update_database ("Lab_Space,PQMS,XLIA,Running,False")

def start_XT_linear_ramp_run (final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value):

    goto        ("Qrius Main Window")
    click       ('Measurement Mode settings')
    click       ('Magnetic AC Susceptibility')

    set_XT_linear_ramp_measurement_settings(final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value)
    update_database ("Lab_Space,PQMS,XTCON,Mode,Linear_Ramp")

    click('Start Button')
    update_database ("Lab_Space,PQMS,XLIA,Running,True")
    wait ("Run", "Finished")

    update_database ("Lab_Space,PQMS,XSMU,Running,False")

###############################################################################
#IV_step_ramp functions functions

def set_IV_step_ramp_measurement_settings(initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance):

    move_cursor ('Run control')
    click       ('drop down menu')
    click       ('I-V (Step ramp)')

    move_cursor ('Toolbar')
    click       ('Settings->Temperature controller-Step ramp settings')

    #####       set step ramp settings here

    set_option ("Ramp Index", "Text Box", "0")
    set_option ("Initial Temperature", "Text Box", str(initial_temperature))
    set_option ("Final Temperature", "Text Box", str(final_temperature))
    set_option ("Temperature Step", "Text Box", str(temperature_step))
    set_option ("Pre-Stabilization Delay", "Text Box", str(pre_stabilization_delay))
    set_option ("Post-Stabilization Delay", "Text Box", str(post_stabilization_delay))
    set_option ("Temperature Tolerance", "Text Box", str(tolerance))
    set_option ("Monitoring Period", "Text Box", str(monitoring_period))

    ################################
    click       ('File->Apply')


    move_cursor ('Toolbar')
    click       ('Settings->I-V Source and Measurement Unit')
    click       ("Settings-IV Source and Meaurement Unit->IV Measurement Settings")
    set_option  ("Voltage Max", "Text Box", V_range)
    set_option  ("Voltage Step", "Text Box", V_step)
    set_option  ("Current Max", "Text Box", I_range)
    set_option  ("Current Step", "Text Box", I_step)
    set_option  ("Power Max", "Text Box", max_power)
    move_cursor ("Bipolar Drop Down Menu")
    click       ("Drop Down Menu")
    click       ("Yes")
    move_cursor ("Top menu")
    click       ("\'File->Done\'")


def start_IV_step_ramp_run (initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance):

    goto        ("Qrius Main Window")
    click       ('Measurement Mode settings')
    click       ('Electrical DC Conductivity')

    set_IV_step_ramp_measurement_settings(initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance)
    update_database ("Lab_Space,PQMS,XSMU,Mode,I-V")
    update_database ("Lab_Space,PQMS,XTCON,Mode,Stepped_Ramp")

    click ('Start Button')
    update_database ("Lab_Space,PQMS,XSMU,Running,True")
    wait ("Run", "Finished")

    update_database ("Lab_Space,PQMS,XSMU,Running,False")

###############################################################################
# RT_stepped ramp functions

def set_RT_step_ramp_measurement_settings(initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance):

    move_cursor('Run control')
    click      ('drop down menu')
    click      ('R-T (Step ramp)')

    move_cursor('Toolbar')
    click      ('Settings->Temperature controller-Step ramp settings')

    #####       set step ramp settings here

    set_option ("Ramp Index", "Text Box", "0")
    set_option ("Initial Temperature", "Text Box", str(initial_temperature))
    set_option ("Final Temperature", "Text Box", str(final_temperature))
    set_option ("Temperature Step", "Text Box", str(temperature_step))
    set_option ("Pre-Stabilization Delay", "Text Box", str(pre_stabilization_delay))
    set_option ("Post-Stabilization Delay", "Text Box", str(post_stabilization_delay))
    set_option ("Temperature Tolerance", "Text Box", str(tolerance))
    set_option ("Monitoring Period", "Text Box", str(monitoring_period))

    ################################
    click       ('File->Apply')


    move_cursor ('Toolbar')
    click       ('Settings->I-V Source and Measurement Unit')
    click       ("Settings-IV Source and Meaurement Unit->Resistance Measurement Settings")
    set_option  ("Voltage Max", "Text Box", V_range)
    set_option  ("Current Max", "Text Box", I_range)
    set_option  ("Power Max", "Text Box", max_power)
    move_cursor ("Bipolar Drop Down Menu")
    click       ("Drop Down Menu")
    click       ("Yes")
    move_cursor ("Top menu")
    click       ("\'File->Done\'")


def start_RT_step_ramp_run (initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance):

    goto ("Qrius Main Window")
    click('Measurement Mode Settings')
    click('Electrical DC Conductivity')

    set_RT_step_ramp_measurement_settings(initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance)
    update_database ("Lab_Space,PQMS,XSMU,Mode,R-T")
    update_database ("Lab_Space,PQMS,XTCON,Mode,Stepped_Ramp")

    click ('Start Button')
    update_database ("Lab_Space,PQMS,XSMU,Running,True")
    wait ("Run", "Finished")

    update_database ("Lab_Space,PQMS,XSMU,Running,False")




###############################################################################
#R_Tme_linear_ramp functions

def set_RT_linear_ramp_measurement_settings (final_temperature, ramp_rate, run_mode, I_range, V_range, max_power):

    move_cursor ('Run control')
    click       ('drop down menu')
    click       ('R-T (linear ramp)')

    move_cursor ('Toolbar')
    click       ('Settings->Temperature controller')
    click       ('Linear ramp settings')
    set_option  ('Final Temperature', "Text Box", str(final_temperature))
    set_option  ('Ramp Rate', 'Text Box', str(ramp_rate))
    click       ('File->Apply')

    move_cursor ('Toolbar')
    click       ('Settings->I-V Source and Measurement Unit')
    click       ("Settings->Source Parameters")
    move_cursor ("Mode Drop Down Menu")
    click       ("Drop Down Menu")
    click       ("Constant " + run_mode)
    move_cursor ("Top Menu")
    click       ("File->Done")

    move_cursor ("Top Menu")
    click       ("Settings->Resistance Measurement Settings")
    set_option  ("Voltage Max", "Text Box", V_range)
    set_option  ("Current Max", "Text Box", I_range)
    set_option  ("Power Max", "Text Box", max_power)
    move_cursor ("Bipolar Drop Down Menu")
    click       ("Drop Down Menu")
    click       ("Yes")
    move_cursor ("Top Menu")
    click       ('File->Done')

def start_RT_linear_ramp (initial_temperature, final_temperature, ramp_rate, run_mode, I_range, V_range, max_power):

    goto        ("Qrius Main Window")
    click       ('Measurement Mode settings')
    click       ('Electrical DC Conductivity')

    set_RT_linear_ramp_measurement_settings (final_temperature, ramp_rate, run_mode, I_range, V_range, max_power)
    update_database ("Lab_Space,PQMS,XSMU,Mode,RT")
    update_database ("Lab_Space,PQMS,XTCON,Mode,Linear_Ramp")

    wait("Heater temperature", str(initial_temperature) + " K")

    click       ('Start')
    update_database ("Lab_Space,PQMS,XTCON,Running,True")
    update_database ("Lab_Space,PQMS,XSMU,Running,True")

    wait("Run", "Finished")

    update_database ("Lab_Space,PQMS,XTCON,Running,False")
    update_database ("Lab_Space,PQMS,XSMU,Running,False")

###############################################################################
#R_Tme_isothermal functions


def set_R_Time_isothermal_measurement_settings (I_range, V_range, max_power, run_mode):
    move_cursor("Top Menu")
    click      ("Settings->Source Parameters")
    move_cursor ("Source Mode")
    click       ("Drop Down Menu")
    click       ("Constant " + run_mode)
    move_cursor("Top Menu")
    click("File->Done")
    move_cursor("Top Menu")
    click ("Settings->Resistance Measurement Settings")
    set_option ("Voltage Max", "Text Box", V_range)
    set_option ("Current Max", "Text Box", I_range)
    set_option ("Power Max", "Text Box", max_power)
    move_cursor("Bipolar Drop Down Menu")
    click      ("Drop Down Menu")
    click      ("Yes")
    move_cursor("Top Menu")
    click('File->Done')

def start_R_Time_isothermal( I_range, V_range, max_power, run_mode):

    click('I-V Source and measurement unit Window')
    move_cursor('Run Mode')
    click('Drop down menu')
    click('R-Time')
    set_R_Time_isothermal_measurement_settings( I_range, V_range, max_power, run_mode)
    update_database ("Lab_Space,PQMS,XSMU,Mode,R-Time")
    click ('Start Button')
    update_database ("Lab_Space,PQMS,XSMU,Running,True")
    wait ("Run", "Finished")
    update_database ("Lab_Space,PQMS,XSMU,Running,False")


###############################################################################
#cryostat environment control functions - Vacuum

def pre_pumping_checks(cryostat):

    ensure ("Lab_Space,PQMS,Clamp,State", "LOCKED")
    ensure ("Lab_Space,PQMS,Pump,Release_Valve,State", "CLOSED")
    ensure ("Lab_Space,PQMS,Pump,Main_Valve,State", "CLOSED")

    if (cryostat == 'Cryostat_Steel'):
    	ensure ("Lab_Space,PQMS," + cryostat + ",Sample_Chamber,Flush_Valve,State", "CLOSED")
    	ensure ("Lab_Space,PQMS," + cryostat + ",Heater_Chamber,Flush_Valve,State", "CLOSED")
    	ensure ("Lab_Space,PQMS," + cryostat + ",Sample_Chamber,Evacuation_Valve,State", "CLOSED")
    	ensure ("Lab_Space,PQMS," + cryostat + ",Heater_Chamber,Evacuation_Valve,State", "CLOSED")

    else:
    	ensure ("Lab_Space,PQMS," + cryostat + ",Sample_Chamber,Flush_Valve,State", "CLOSED")
    	ensure ("Lab_Space,PQMS," + cryostat + ",Sample_Chamber,Evacuation_Valve,State", "CLOSED")

def set_up_pump (cryostat):

    pre_pumping_checks(cryostat)
    open_valve ("Lab_Space,PQMS,Pump,Main_Valve", "anticlockwise")

def create_vaccum (chamber, cryostat):

    open_valve ("Lab_Space,PQMS," + cryostat + "," + chamber + ",Evacuation_Valve", "anticlockwise")
    wait ("Pirani Guage needle", "Stable")
    update_database ("Lab_Space,PQMS,Cryostat_Steel,Vaccum,YES")
    close_valve ("Lab_Space,PQMS," + cryostat + "," + chamber + ",Evacuation_Valve", "clockwise")

def release_pressure (chamber, cryostat):

    pre_pumping_checks(cryostat)
    close_valve ("Lab_Space,PQMS,Pump,Main_Valve", "clockwise")
    close_valve ("Lab_Space,PQMS,"+cryostat+","+ chamber + ",Evacuation_Valve", "clockwise")
    open_valve  ("Lab_Space,PQMS,Pump,Release_Valve", "anticlockwise")
    close_valve ("Lab_Space,PQMS,Pump,Release_Valve", "clockwise")
    open_valve  ("Lab_Space,PQMS,"+cryostat+","+chamber + ",Evacuation_Valve", "anticlockwise")
    open_valve  ("Lab_Space,PQMS,Pump,Main_Valve", "anticlockwise")
    update_database ("Lab_Space,PQMS,Cryostat_Steel,Vaccum,NO")
    update_database ("Lab_Space,PQMS,Cryostat_Steel,Helium,NO")

def restore_vaccum (cryostat):

    move         ("Cryostat Cover", "Cryostat opening")
    create_vaccum("Sample_Chamber", cryostat)
    create_vaccum("Heater_Chamber", cryostat)

    clamp()

###############################################################################
#cryostat environment control functions - Helium Flushing

def release_residual_pressure(chamber, cryostat):

    open_valve      ("Lab_Space,PQMS," + cryostat + "," + chamber + ",Flush_Valve", "anticlockwise")
    wait            ("Helium Pressure Gauge Reading", "0")
    close_valve     ("Lab_Space,PQMS," + cryostat + "," + chamber + ",Flush_Valve", "clockwise")
    update_database ("Lab_Space,PQMS,Helium,Main_Valve,Gauge_Reading,0")

def initialize_flushing(pressure):

    open_slightly ("Lab_Space,PQMS,Helium,Main_Valve", "anticlockwise")
    write         ("Pressure to be flushed is " + str(pressure))
    while True:
            open_slightly ("Lab_Space,PQMS,Helium,Pressure_Valve",  "clockwise")
            response = raw_input("What is the pressure gauge reading?")
            while (response == ""):
                response = raw_input("What is the pressure gauge reading?")

            update_database("Lab_Space,PQMS,Helium,Main_Valve,Gauge_Reading," + response)

            if (float(response) == pressure):
                break

def flushing_prerequisites(chamber, cryostat):

    create_vaccum (chamber, cryostat)
    close_valve ("Lab_Space,PQMS," + cryostat + "," + chamber + ",Evacuation_Valve" ,"clockwise")
    close_valve ("Lab_Space,PQMS,Pump,Main_Valve", "clockwise")
    pre_pumping_checks (cryostat)

    open_valve  ("Lab_Space,PQMS," + cryostat + "," + chamber + ",Evacuation_Valve","anticlockwise")
    ensure ("Lab_Space,PQMS,Helium,Pressure_Valve,State", "CLOSED")


def flush_helium (chamber, cryostat):

    flushing_prerequisites    (chamber, cryostat)

    release_residual_pressure (chamber, cryostat)
    initialize_flushing (10) #psi

    rapid_movement()

    open_valve  ("Lab_Space,PQMS," + cryostat + "," + chamber + ",Flush_Valve", "anticlockwise")
    close_valve ("Lab_Space,PQMS," + cryostat + "," + chamber + ",Flush_Valve", "clockwise")

    open_valve  ("Lab_Space,PQMS,Pump,Release_Valve",  "anticlockwise")
    close_valve ("Lab_Space,PQMS,Pump,Release_Valve",  "clockwise")

    close_valve ("Lab_Space,PQMS,Helium,Pressure_Valve", "anticlockwise")

    close_valve ("Lab_Space,PQMS," +cryostat+"," + chamber + ",Evacuation_Valve", "clockwise")
    open_valve  ("Lab_Space,PQMS,Pump,Main_Valve","anticlockwise")

    close_valve ("Lab_Space,PQMS,Helium,Main_Valve", "anticlockwise")

    end_rapid_movement()

    update_database ("Lab_Space,PQMS,Cryostat_Steel,Helium,YES")

###############################################################################

def pour_liquid_nitrogen ():

    ensure  ("Lab_Space,PQMS,Cryocan_BA11,Liquid_Nitrogen" , "PRESENT")

    start_XTCON_monitor()

    goto    ("Cryocan_BA11.Home_Coordinates")
    hold    ("Cryocan_BA11.Cap")
    write   ("execute : Remove the lid and cap from the cryocan")
    goto    ("Puck_Screwing_Coordinates")
    leave   ("Cryocan_BA11.Cap")


    hold    ("Cryocan_BA11")
    goto    ("PQMS.Funnel")
    write   ("execute : Tilt the cryocan onto the funnel to pour liquid nitrogen into the funnel")
    write   ("execute : Fill the required amount of Liquid nitrogen")

    update_database ("Lab_Space,PQMS,Cryostat_Steel,Cryocan,Liquid_Nitrogen,YES")

    goto    ("Cryocan_BA11.Home_Coordinates")
    leave   ("Cryocan_BA11")
    goto    ("Puck_Screwing_Coordinates")
    hold    ("Cryocan_BA11.Cap")
    goto    ("Cryocan_BA11.Home_Coordinates")
    write   ("execute : Replace _Ba11.Cap")
    end_XTCON_monitor()

#####################################################################
#misc qrius utilities

def save_graph(path, name):

    move_cursor("Toolbar below the graph")
    click      ("Save Icon")
    move_cursor('Path Text Box')
    click      ("Text Box")
    type_text  (path + " and" + name)
    click      ("'Save'")

def set_save_folder (sample_name, sample_number, sample_description, address):
    move_cursor ("Toolbar at the top of the Qrius Window")
    click ("'Settings, and then Global Settings'.")
    move_cursor ("'User Settings' section, next to the 'Data Folder' selection bar")
    click ("'Browse'")
    write ("execute : Select " + address + " as the path to store data.")
    click ("'OK'")
    click ("'OK'")
    click ("'Sample Settings'")
    move_cursor ("Top of the window")
    click ("'File->New'")
    set_option ('Sample Name', 'Text Box', sample_name)
    set_option ('Sample Number', 'Text Box', sample_number)
    set_option('Sample Description', 'Text Box', sample_description)
    click ("'File->Apply'")