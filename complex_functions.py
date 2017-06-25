import time
import primitive_functions
from primitive_functions import *

#####################################################################
#general user functions

def move(obj, position):
    goto (obj)
    hold (obj)
    goto (position)

def remove (obj1, obj2):
    '''Removes/separates obj1 from obj2'''
    
    read_state ('Lab_Space,Sample_Table')

    goto (obj2 + "." + obj1)
    hold (obj2 + "." + obj1)

    write ("execute : With other hand hold " + obj2 + " and keep it fixed.")
    write ("execute : Pull the " + obj1 + " and separate from " + obj2)

def hold_sample(Sample, Sample_Box):
	
    goto  ('Tweezers')
    hold  ('Tweezers')

    write ("execute : Goto " + Sample + ".Home_Coordinates")
    write ("execute : Hold " + Sample + ".Terminal_1")
    goto  ("Sample_Mounting_Coordinates")

    write ("Update_Database Lab_Space,Sample_Table,Sample_Boxes," + Sample_Box + "," + Sample + ",State,IN_USE")

def close_lid(obj1):
    write ("execute : Close the lid of " + obj1)
    write ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,CLOSED")

#####################################################################
#runtime user response based functions

def sample_is_mounted():
    write ("Sample is already mounted. Continuing to next step...") 

def do_not_unmount():
    write ("Not unmounting the sample")
    
def throw_exception (error):
    write ("\n########### ERROR ###########\n")
    write (error)
    write ("\n#############################\n")
    
#####################################################################
#soldering iron related functions

def set_up_soldering_iron():
    '''Set up soldering space and iron for use'''
    
    goto('SOLDERING_STATION')
    write("execute : Check if soldering station is free or not")
    write("execute : If 'Free' then Leave test_object or else wait until it gets free and then Leave test_object")
    write("execute Switch On Soldering_Iron")
    write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,ON")
    write("execute : Wait for the soldering iron LED to start blinking.")
    
def solder (terminal_a, terminal_b):
    '''Solder terminal_b onto terminal_b, given Sample from Sample_Box'''
    
    write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,State,IN_USE")
    
    goto   ('Soldering_Iron.Home_Coordinates')
    hold   ('Soldering_Iron')
    
    goto   ('Flux.Home_Coordinates')
    write  ("execute : Plunge the Tip into the Flux")
    write  ("execute : Retract the Tip")
    
    goto   ('Solder.Home_Coordinates')
    write  ("execute : Move the Soldering_Iron along the Solder")
    
    write  ("execute : Goto juntion of " + terminal_a + " and " + terminal_b)
    write  ("execute : Wait until sensor deems soldering between " + terminal_a + " and " + terminal_b + " to be complete")
    
    goto   ('Cleaning_Pad.Home_Coordinates')
    write  ("execute : Plunge Tip in Cleaning Pad")
    write  ("execute : Retract Tip")
    
    goto   ('Soldering_Iron.Home_Coordinates')
    leave  ('Soldering_Iron')
    
    write  ("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,State,NOT_IN_USE")
    
def desolder(terminal, Sample, Sample_Box):
    '''Desolder terminal of Sample'''
    
    write       ("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,State,IN_USE")
    
    goto        ("Soldering_Iron")
    hold        ("Soldering_Iron")
    
    goto        ("Flux.Home_Coordinates")
    write       ("execute : Plunge the tip into the flux")
    write       ("execute : Retract the tip")
    
    goto        (Sample + "_" + terminal)
    write       ("execute : Wait until sensor deems desoldering complete")
    
    goto        ("Cleaning_Pad.Home_Coordinates")
    write       ("execute : Plunge tip in Cleaning_Pad")
    write       ("execute : Retract Tip")
    
    write       ("Update_Database Lab_Space,Sample_Table,Sample_Boxes," + Sample_Box + "," + Sample + ",Terminal_1,Soldered,NO")
    write       ("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Terminal_1,Soldered,NO")
    
    write       ("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,State,NOT_IN_USE")


#####################################################################
#clamp related functions


def clamp():
    '''Clamp PQMS insert to Cryostat'''
    
    read_state ('Lab_Space,PQMS,Clamp')
    move       ('Clamp.Home_Coordinates', 'PQMS.Clamp_Coordinates')    
    write      ("execute : Use the other hand to revolve the clamp till 180 degrees")
    write      ("execute : Revolve the screw of the clamp till it is in closing position")
    rotate     ('Screw','required turns','clockwise')
    write      ("Update_Database Lab_Space,PQMS,Clamp,State,LOCKED")
    
def unclamp():
    '''Unclamp the PQMS insert to Cryostat'''
    
    read_state  ("Lab_Space,PQMS,Clamp")
    read_state  ("Lab_Space,PQMS,Insert_RT_Puck")
    goto        ("Clamp.Current_Coordinates")
    hold        ("the clamp with one hand")
    write       ("execute : With other hand, Rotate the screw anti-clockwise for required number of turns")
    write       ("execute : Revolve the screw of the clamp till it is in opening position")
    write       ("execute : Use the other hand to revolve the clamp till it's straight.")
    write       ("Update_Database Lab_Space,PQMS,Clamp,State,UNLOCKED")
    goto        ("Clamp.Home_Coordinates")
    leave       ("Clamp")


#####################################################################
#cable related functions


def connect_cable (cable, test_object):
    '''Connects 'cable' to its respective connector on test_object.'''
    
    read_state  ('Lab_Space,PQMS,Cables,' + cable)
    move        (cable + ".Cryostat_End", test_object + "." + cable + "_Terminal")
    write       ("execute : Align " + cable + "'s connector with "  + test_object + "'s connector")
    write       ("execute : Insert and fasten " + cable)
    leave       (cable)
    write       ("Update_Database Lab_Space,PQMS,Cables," + cable + ",State,CONNECTED")
    

def disconnect_cable (cable):
    '''Disconnects 'cable' from its respective connector on any test_object.'''
    
    read_state  ('Lab_Space,PQMS,Cables,' + cable)
    goto        (cable + ".Current_Coordinates")
    hold        (cable + ".Cryostat_End")
    
    write       ("execute : Unfasten and remove " + cable)
    move        (cable + ".Cryostat_End", cable + ".Home_Coordinates" )
    write       ("Update_Database Lab_Space,PQMS,Cables," + cable + ",State,DISCONNECTED")
    leave       (cable)


#####################################################################
#sample unloading and loading functions

def mount_sample (Sample, Sample_Box, test_object):
    '''Mount 'Sample' from 'Sample_Box' onto Puck_Board'''
    
    read_state  ('Lab_Space,Sample_Table')
    read_state  ('Lab_Space,PQMS')
        
    if ((test_object == "Insert_RT_Puck") or (test_object == "Puck_Board")):

        move        ('Puck_Board','Sample_Mounting_Coordinates')
        leave       ('Puck_Board')
        remove      ('cap',Sample_Box)
        write       ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+",State,OPEN")

        hold_sample (Sample, Sample_Box)
        close_lid   (Sample_Box)

        write       ("execute : Remove Sticky Tape from "+ Sample)
        goto    ('Puck_Board')
        hold    ('Puck_Board')
        
        #SOLDERING PROCESS
        set_up_soldering_iron()
        
        move(Sample+'.Terminal_1', 'Insert_RT_Puck,Puck,Terminal_4')
        solder(Sample +',Terminal_1', 'Insert_RT_Puck,Puck,Terminal_4')
        
        write ("execute : Bend " + Sample + "'s terminals as required.")

        move(Sample+"'s Terminal_2", "Insert_RT_Puck,Puck,Terminal_1")
        solder(Sample + "'s,Terminal_2", "Insert_RT_Puck,Puck,Terminal_1")

        write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Sample_Mounted,YES")
        write("execute : Switch off the soldering iron")
        write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,OFF")
        #SOLDERING PROCESS

        read_state('Lab_Space,Sample_Table')
        read_state('Lab_Space,PQMS')
        
        move ('Puck_Board', 'Puck_Board.Home_Coordinates')
        leave('Puck_Board')
        
    elif (test_object == "Insert_RT_Old"):
        
        remove      ('cap',Sample_Box)
        write       ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+",State,OPEN")

        hold_sample (Sample, Sample_Box)
        close_lid   (Sample_Box)

        write       ("execute : Remove Sticky Tape from "+ Sample)
        
        goto    ("Insert_RT_Old")
        hold    ("Insert_RT_Old")
        
        #SOLDERING PROCESS
        set_up_soldering_iron()
        
        move(Sample+'.Terminal_1', 'Insert_RT_Old,Terminal_1')
        solder(Sample + ',Terminal_1', 'Insert_RT_Old,Terminal_1')
        
        write ("execute : Bend " + Sample + "'s terminals as required.")

        move(Sample+'.Terminal_2', 'Insert_RT_Old,Terminal_4')
        solder(Sample+',Terminal_2', 'Insert_RT_Old,Terminal_4')

        write("Update_Database Lab_Space,PQMS,Insert_RT_Old,Sample_Mounted,YES")
        write("execute : Switch off the soldering iron")
        write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,OFF")
        #SOLDERING PROCESS
        
        write("execute : Stick " + Sample + "'s body to the mounting surface with Kapton tape")
        goto("Insert_RT_Old.Home_Coordinates")
    
    goto('Tweezers.Home_Coordinates')
    leave('Tweezers')


def load_sample(Sample, Sample_Box, test_object, cryostat):
    
    write ("execute : Insert is being loaded to " + cryostat + " cryostat...")
    
    if (test_object == "Insert_RT_Puck"):
        
        response = raw_input ("\nIs the puck connected to the insert? : y/n \n")
        while ((response != 'y') and (response != 'n')):
            response = raw_input ("\nIs the puck connected to the insert? : y/n \n")
        
        if (response == 'n'):    
            remove('Puck','Puck_Board')
            write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Puck_Board_Connection,DISCONNECTED")

            goto('Puck_Screwing_Coordinates')
            leave('Puck')
            read_state('Lab_Space,PQMS,Insert_RT_Puck')
            move(test_object, 'Cryostat.Exit_Coordinates')
            goto('Puck_Screwing_Coordinates')
            hold('Puck')
            write("execute : Align Puck for screwing")
            rotate('Puck','14 turns','clockwise')
            write("execute : Align Insert2Puck Cable with Puck Pins")
            write("execute : Insert the pin_holes into the puck pins")
            write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Insert_Connection,CONNECTED")
            write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Insert2Puck_Cable,State,CONNECTED")
        
        flush_helium('Sample_Chamber')
        if (cryostat == "Double_Walled_Steel"):
            flush_helium('Heater_Chamber')
    	unclamp()
        
        write('execute : Remove Cryostat_Cover')
    	goto('Cryostat_Cover.Home_Coordinates')
    	leave('Cryostat_Cover')
        move (test_object, 'Cryostat.Exit_Coordinates')
        goto('Cryostat.Home_Coordinates')

        clamp()
        
        
    elif (test_object == "Puck_Board"):
        
        write ("Sample Puck is already connected to Puck_Board")
        move ("Puck_Board", "PQMS.Home_Coordinates")
    
    elif (test_object == "Insert_RT_Old"):
        
        flush_helium('Sample_Chamber')
        if (cryostat == "Double_Walled_Steel"):
            flush_helium('Heater_Chamber')
    	unclamp()
    	
        write('execute : Remove Cryostat_Cover')
    	goto('Cryostat_Cover.Home_Coordinates')
    	leave('Cryostat_Cover')
    	
        move(test_object, 'Cryostat.Exit_Coordinates')
        goto ("Cryostat.Home_Coordinates")
        
        clamp()
    
    elif (test_object == "Insert_Susceptibility"):
        
        flush_helium('Sample_Chamber')
        if (cryostat == "Double_Walled_Steel"):
            flush_helium('Heater_Chamber')
    	unclamp()
    	
        write('execute : Remove Cryostat_Cover')
    	goto('Cryostat_Cover.Home_Coordinates')
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
    
        goto    ("Puck_Board")
        hold    ("Puck_Board")
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
        
        write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Sample_Mounted,NO")
        
        write   ("execute : Switch off Soldering Iron")
        write   ("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,OFF")
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
        
        write("Update_Database Lab_Space,PQMS,Insert_RT_Old,Sample_Mounted,NO")
        
        write   ("execute : Switch off Soldering Iron")
        write   ("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,OFF")
        #Desoldering Process
        
        write   ("execute : Remove tape from Zener Diode")
        
        move    ("Insert_RT_Old", "Insert_RT_Old.Home_Coordinates")
        
        goto    ("Sample_Table.Sample_Mounting_Coordinates")
        write   ("execute : straighten sample")
        write   ("execute : put a sticky note on the sample")
        leave   (Sample)
        
        read_state("Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box)
        
        goto    (Sample_Box +"'s Cap")
        hold    ("The Cap")
        write   ("execute : With other hand hold the " + Sample_Box + " and keep it fixed")
        write   ("execute : Pull the cap, and separate it from sample_box")
        write   ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,OPEN")
        goto    (Sample + "_Terminal_1")
        hold    (Sample + "_terminal_1")
        goto    (Sample + ".Home_Coordinates")
        leave   (Sample)
        
        write   ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+","+Sample+",State,NOT_IN_USE")
        write   ("execute : close the lid of the box")
        write   ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,CLOSED")
        goto    ("Tweezer.Home_Coordinates")
        leave   ("Tweezer")


def unload_sample(Sample, Sample_Box, test_object, cryostat):
    
    if (test_object == "Insert_RT_Puck"):
        
        unclamp()
        
        goto("Insert_RT_Puck")
        hold("Insert_RT_Puck")
      
        goto("Cryostat.Exit_Coordinates")
        goto("Sample_Table.Puck_Screwing_Coordinates")
        remove("Insert2Puck_Cable", "Insert_RT_Puck")
        
        write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Insert_Connection,DISCONNECTED")
        write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Insert2Puck_Cable,State,DISCONNECTED")
        read_state("Lab_Space,PQMS,Insert_RT_Puck,Puck")
        
        goto("Puck")
        hold("Puck")
        rotate('Puck','14 turns','anticlockwise')
        leave("Puck")
        
        goto("Insert_RT_Puck.Home_Coordinates")
        leave("Insert_RT_Puck")
        
        goto("Sample_Table.Puck_Screwing_Coordinates")
        hold("Insert_RT_Puck.Puck")
        goto("Puck_Board.Home_Coordinates")
        write("execute : Align Puck pins with Puck_Board")
        write("execute : Insert Puck into Puck_Board")
        leave("Puck")
        
        write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Puck_Board_Connection,CONNECTED")
        
    elif (test_object == "Puck_Board"):
        
        move (test_object, test_object + ".Home_Coordinates")
        
    elif (test_object == "Insert_RT_Old"):
        
        unclamp()
        move (test_object, test_object + ".Home_Coordinates")
        
    elif (test_object == "Insert_Susceptibility"):
        
        flush_helium('Sample_Chamber')
        if (cryostat == "Double_Walled_Steel"):
            create_vaccum('Heater_Chamber')
    	
        
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
        
        create_vaccum ("Sample_Chamber")
    	if (cryostat == "Double_Walled_Steel"):
            create_vaccum('Heater_Chamber')
        
        clamp()
        
        write ("execute : ROBOT_2 : Remove the sample from the sleeve by gently pulling with tweezer")
        
        write ("execute : ROBOT_1 : Open the Dessicator Lid \n \
ROBOT_2 : Leave sample stage, Place the sample in its pouch, put it the dessicator and close the lid of the dessicator")
        
        write ("execute : ROBOT_1 : Move insert to Insert_Susceptibility.Home_Coordinates")
        
    	write ("execute : ROBOT_2 move sample stage to Insert_Susceptibility.Home_Coordinates")
    	
    	################################
        

#####################################################################
#PQMS setup functions

def switch_on_PQMS_modules():
    read_state("Lab_Space,PQMS")
    
    goto   ('Stabilizer.Power_Switch')
    write  ("execute : Switch On Stabilizer.Power_Switch")
    write  ("Update_Database Lab_Space,PQMS,Stabilizer,Power_Switch,State,ON")
    
    goto   ("PQMS.XPLORE_Power_Supply.Power_Cable")
    write  ("execute : Switch on XPLORE_Power_Supply.Power_Cable")
    write  ("Update_Database Lab_Space,PQMS,XPLORE_Power_Supply,State,ON")
    write  ("Update_Database Lab_Space,PQMS,XSMU,State,ON")
    
    goto   ("PQMS.XTCON.Power_Cable")
    write  ("execute : Switch on XTCON.Power_Cable")
    write  ("Update_Database Lab_Space,PQMS,XTCON,State,ON")
    
    goto   ("PQMS.XLIA.Power_Cable")
    write  ("execute : Switch on XLIA.Power_Cable")
    write  ("Update_Database Lab_Space,PQMS,XLIA,State,ON")
    
    goto   ("PQMS.Sample_Positioner.Power_Cable")
    write  ("execute : Switch on Sample_Positioner.Power_Cable")
    write  ("Update_Database Lab_Space,PQMS,Sample_Positioner,State,ON")
    
    goto    ("PQMS.Pump.Power_Cable")
    write   ("execute : Switch on Pump.Power_Cable")
    write   ("Update_Database Lab_Space,PQMS,Pump,State,ON")
    
    goto    ("PQMS.Pirani_Gauge.Power_Cable")
    write   ("execute : Switch on Pirani_Gauge.Power_Cable")
    write   ("Update_Database Lab_Space,PQMS,Pump,State,ON")

def set_up_PQMS_modules ():

    write ("execute : In the Qrius window, click on 'Modules Manager'.")
    
    click ("Temperature Controller")
    write("execute : Check if XTCON PC Connection has been established")
    write("execute : If No, then click on 'File->Connect'. If Yes, do nothing.")
   
    click ("IV Source and Measurement")
    write("execute : Check if XSMU PC Connection has been established")
    write("execute : If No, then click on 'File->Connect'. If Yes, do nothing.")

    click ("Lockin Amplifier")
    write("execute : Check if XLIA PC Connection has been established")
    write("execute : If No, then click on 'File->Connect'. If Yes, do nothing.")
    
    click ("Sample Positioner")
    write("execute : Check if Sample_Positioner PC Connection has been established")
    write("execute : If No, then click on 'File->Connect'. If Yes, do nothing.")
    

def switch_off_PQMS_modules():
    read_state ("Lab_Space,PQMS")

    goto   ("PQMS.XPLORE_Power_Supply.Power_Cable")
    write  ("execute : Switch off XPLORE_Power_Supply.Power_Cable")
    write  ("Update_Database Lab_Space,PQMS,XPLORE_Power_Supply,State,OFF")
    write  ("Update_Database Lab_Space,PQMS,XSMU,State,OFF")
    
    goto   ("PQMS.XTCON.Power_Cable")
    write  ("execute : Switch off XTCON.Power_Cable")
    write  ("Update_Database Lab_Space,PQMS,XTCON,State,OFF")
    
    goto   ("PQMS.XLIA.Power_Cable")
    write  ("execute : Switch off XLIA.Power_Cable")
    write  ("Update_Database Lab_Space,PQMS,XLIA,State,OFF")
    
    goto   ("PQMS.Sample_Positioner.Power_Cable")
    write  ("execute : Switch off Sample_Positioner.Power_Cable")
    write  ("Update_Database Lab_Space,PQMS,Sample_Positioner,State,OFF")
    
    write   ("execute : Ensure that Pump.Release_Valve, Pump.Main_Valve, Sample_Chamber.Flush_Valve, Sample_Chamber.Evacuation_Valve, \
                    Heater_Chamber.Flush_Valve, Heater_Chamber.Evacuation_Valve and all other valves connected to Helium_Cylinder are closed")
    
    goto   ("PQMS.Pump.Power_Cable")
    write  ("execute : Switch off Pump.Power_Cable")
    write  ("Update_Database Lab_Space,PQMS,Pump,State,OFF")
    write  ("Update_Database Lab_Space,PQMS,Pirani_Gauge,State,OFF")
    
    goto   ('Stabilizer.Power_Switch')
    write  ("execute : Switch OFF Stabilizer.Power_Switch")
    write  ("Update_Database Lab_Space,PQMS,Stabilizer,Power_Switch,State,OFF")
    
###############################################################################    
#Computer functions

def switch_on_computer():
    
    write ("execute : Switch on Computer.Switch")
    write("execute : Press CPU Power Button")
    write("execute : Switch on the USB_Power_Adaptor")
    write("execute : Login to user account")
    write("execute : Open Qrius ")
    
def switch_off_computer():
    
    write ("execute : Exit Qrius")
    write("execute : Shutdown Computer")
    write("execute : Switch off the USB_Power_Adaptor")
    write("execute : Wait for computer to Shutdown")
    write ("execute : Switch off Computer.Switch")
    
###############################################################################
#Sample Positioner Functions

def set_positioner(position):

    click       ('Qrius Window->Modules Manager->Sample Positioner Window')
    move_cursor ('Toolbar')
    click       ('Tools->Move Absolute')
    write       ('execute : Set the value to' + str(position))

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
    write       ("Update_Database Lab_Space,PQMS,XTCON,Running,True")

def set_XTCON_temperature (temperature_set_point):
    
    click       ('Temperature Controller Window')
    move_cursor ('Toolbar')
    click       ('Settings->Isothermal Settings')
    write       ("Update_Database Lab_Space,PQMS,XTCON,Mode,ISOTHERMAL")
    write       ("execute : Set 'Heater Set point' Temperature to " + str(temperature_set_point) + " K")
    move_cursor ('Toolbar')
    click       ('File->Apply')
    write       ("execute : Wait till sample temperature stabilizes")

def stop_XTCON_run():
    click       ('Temperature Controller Window')
    write       ("execute : Stop Temperature Controller Run")
    write       ("Update_Database Lab_Space,PQMS,XTCON,Running,False")

def start_XTCON_monitor():
    click       ('Temperature Controller Window')
    move_cursor ('Control mode')
    click       ('drop down menu')
    click       ('Monitor')
    click       ('Start Button')
    write       ("Update_Database Lab_Space,PQMS,XTCON,Running,True")

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
    write       ("Update_Database Lab_Space,PQMS,XSMU,Running,True")


def set_XSMU_constant_volatge(voltage_set_point):
    click       ('IV Source and Measureent Unit Window')
    move_cursor ('Toolbar')
    click       ('Settings->Source Parameters')
    write       ("execute : Set 'Source Mode'  to constant voltage")
    write       ("execute : Set 'Voltage Vakue'  to "+ str(voltage_set_point) +"mV")
    move_cursor ('Toolbar')
    click       ('File->Apply')
    write       ("execute : Wait till Voltage stabilizes")

def init_XLIA_isothermal_constant_voltage(test_object):
    click('Lock-In Amplifier Window')
    move_cursor ('Run mode')
    click       ('drop down menu')
    click       ('V-F')


def set_XLIA_isothermal_constant_voltage(initial_frequency,final_frequency,frequency_step,reference_amplitude,reference_frequency,reference_phase,run_mode):
    click       ('Lock-In Amplifier Window')
    move_cursor ('Toolbar')
    click       ('Settings -> V-F Ramp Settings')
    write       ("execute : Set 'Initial Frequency'  to " + str(initial_frequency) + " Hz" )
    write       ("execute : Set 'Final Frequency'  to "   + str(final_frequency)   + " Hz" )
    write       ("execute : Set 'Frequency step'  to "    + str(frequency_step)    + " Hz" )
    click       ('File -> Apply')
    move_cursor ('Toolbar')
    click       ('Settings -> Reference Settings')
    write       ("execute : Set 'Amplitude'  to " + str(reference_amplitude) + " mV" )    
    write       ("execute : Set 'Frequency'  to " + str(reference_frequency) + " Hz" )
    write       ("execute : Set 'Phase'  to "     + str(reference_phase)     + " degrees" )
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
    
    write       ("execute : Set max_depth as " + max_depth)
    write       ("execute : Set step_size as " + step_size)
    
    click       ('File->Apply')
    
    move_cursor ('Toolbar')
    click       ('Settings->Lock-In Amplifier->Reference Settings')
    write       ("execute : Set frequency as " + frequency + " Hz")
    write       ("execute : Set amplitude as " + amplitude + " mV")
    write       ("execute : Set phase as " + phase + " degrees")
    
    click       ('Settings->Lock-In Amplifier->Acquisition Settings')
    write       ("execute : Set delay as " + delay + " s")
    write       ("execute : Set filter_length as " + filter_length)
    write       ("execute : Set drive mode as " + drive_mode)
    write       ("execute : Set " + drive_mode + " value as " + drive_value)
    
    click       ('Settings->Lock-In Amplifier->Measurement Settings')
    write       ("execute : Set coupling as AC")
    
    move_cursor ("Top menu")
    click       ("\'File->Apply\'")    


def set_XT_linear_ramp_measurement_settings(final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value):
    #####       set linear ramp settings here
    
    move_cursor ('Run control')
    click       ('drop down menu')
    click       ('X-T (linear ramp)')
    
    move_cursor ('Toolbar')
    click       ('Settings->Temperature controller')
    click       ('Linear ramp settings')
    write       ("execute : Set Final Temperature to " + str(final_temperature))
    write       ("execute : Set Ramp rate to " + ramp_rate + " K/min")
    click       ('File->Apply')
    
    move_cursor ('Toolbar')
    click       ('Settings->Lock-In Amplifier->Reference Settings')
    write       ("execute : Set frequency as " + frequency + " Hz")
    write       ("execute : Set amplitude as " + amplitude + " mV")
    write       ("execute : Set phase as " + phase + " degrees")
    
    click       ("\'File->Apply\'")  
    
    move_cursor ("Top menu")
    click       ('Settings->Lock-In Amplifier->Acquisition Settings')
    write       ("execute : Set delay as " + delay + " s")
    write       ("execute : Set filter_length as " + filter_length)
    write       ("execute : Set drive mode as " + drive_mode)
    write       ("execute : Set " + drive_mode + " value as " + drive_value)
    
    click       ('Settings->Lock-In Amplifier->Measurement Settings')
    write       ("execute : Set coupling as AC")
    
    click       ("\'File->Apply\'")  
    
    ################################
    
    

def start_XL_run (final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value):
    
    goto        ("Qrius Main Window")
    click       ('Measurement Mode settings')
    click       ('Magnetic AC Susceptibility')
    
    set_XL_measurement_settings(final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value)
    write("Update_Database Lab_Space,PQMS,XTCON,Mode,Linear_Ramp")
    
    click ('Start Button')
    write ("Update_Database Lab_Space,PQMS,XLIA,Running,True")
    write ("execute : Wait until run comes to an end")
    
    write ("Update_Database Lab_Space,PQMS,XLIA,Running,False")
    save_graph()

def start_XT_linear_ramp_run (final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value):
    
    goto        ("Qrius Main Window")
    click       ('Measurement Mode settings')
    click       ('Magnetic AC Susceptibility')
    
    set_XT_linear_ramp_measurement_settings(final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value)
    write("Update_Database Lab_Space,PQMS,XTCON,Mode,Linear_Ramp")
    
    click ('Start Button')
    write ("Update_Database Lab_Space,PQMS,XLIA,Running,True")
    write ("execute : Wait until run comes to an end")
    
    write ("Update_Database Lab_Space,PQMS,XSMU,Running,False")
    save_graph()

def is_XL_run_needed(final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value):

    condition = raw_input("Do you want to do X-L run? (y/n): \n")
    if (condition == 'y'):
    	start_XL_run(final_temperature, ramp_rate, max_depth, step_size, amplitude, frequency, phase, delay, filter_length, drive_mode, drive_value)
	
	
###############################################################################
#IV_step_ramp functions functions

def set_IV_step_ramp_measurement_settings(initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance):
    
    move_cursor ('Run control')
    click       ('drop down menu')
    click       ('I-V (Step ramp)')
    
    move_cursor ('Toolbar')
    click       ('Settings->Temperature controller-Step ramp settings')
    
    #####       set step ramp settings here
    
    write       ("execute : Set Ramp index as '0'.")
    write       ("execute : Set Initial Temperature to " + str(initial_temperature) + " K")
    write       ("execute : Set Final Temperature to " + str(final_temperature) + " K")
    write       ("execute : Temperature Step to " + str(temperature_step) + " K")
    
    write       ("execute : Set Pre-stabilization Delay to " + str(pre_stabilization_delay))
    write       ("execute : Set Post-stabilization Delay to " + str(post_stabilization_delay))
    write       ("execute : Set Temperature Tolerance to " + str(tolerance))
    write       ("execute : Set Monitoring Period to " + str(monitoring_period))
    
    ################################
    click       ('File->Apply')
    
    
    move_cursor ('Toolbar')
    click       ('Settings->I-V Source and Measurement Unit')
    click       ("Settings-IV Source and Meaurement Unit->IV Measurement Settings")
    write       ("execute : Set voltage max as " + V_range + " mV")
    write       ("execute : Set voltage step size as " + V_step + " mV")
    write       ("execute : Set current max as " + I_range + " uA")
    write       ("execute : Set current step size as " + I_step + " uA")
    write       ("execute : Set power max as " + max_power + " mW")
    write       ("execute : Ensure that Bipolar option is set to \'Yes\'")
    move_cursor ("Top menu")
    click       ("\'File->Done\'")    


def start_IV_step_ramp_run (initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance):
    
    goto        ("Qrius Main Window")
    click       ('Measurement Mode settings')
    click       ('Electrical DC Conductivity')
    
    set_IV_step_ramp_measurement_settings(initial_temperature, final_temperature, temperature_step, V_range, V_step, I_range, I_step, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance)
    write("Update_Database Lab_Space,PQMS,XSMU,Mode,I-V")
    write("Update_Database Lab_Space,PQMS,XTCON,Mode,Stepped_Ramp")
    
    click ('Start Button')
    write ("Update_Database Lab_Space,PQMS,XSMU,Running,True")
    write ("execute : Wait until graph comes to an end")
    
    write ("Update_Database Lab_Space,PQMS,XSMU,Running,False")
    save_graph()

###############################################################################
# RT_stepped ramp functions

def set_RT_step_ramp_measurement_settings(initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance):
    
    move_cursor ('Run control')
    click       ('drop down menu')
    click       ('R-T (Step ramp)')
    
    move_cursor ('Toolbar')
    click       ('Settings->Temperature controller-Step ramp settings')
    
    #####       set step ramp settings here
    
    write       ("execute : Set Ramp index as '0'.")
    write       ("execute : Set Initial Temperature to " + str(initial_temperature) + " K")
    write       ("execute : Set Final Temperature to " + str(final_temperature) + " K")
    write       ("execute : Temperature Step to " + str(temperature_step) + " K")
    
    write       ("execute : Set Pre-stabilization Delay to " + str(pre_stabilization_delay))
    write       ("execute : Set Post-stabilization Delay to " + str(post_stabilization_delay))
    write       ("execute : Set Temperature Tolerance to " + str(tolerance))
    write       ("execute : Set Monitoring Period to " + str(monitoring_period))
    
    ################################
    click       ('File->Apply')
    
    
    move_cursor ('Toolbar')
    click       ('Settings->I-V Source and Measurement Unit')
    click       ("Settings-IV Source and Meaurement Unit->Resistance Measurement Settings")
    write       ("execute : Set voltage max as " + V_range + " mV")
    write       ("execute : Set current max as " + I_range + " uA")
    write       ("execute : Set power max as " + max_power + " mW")
    write       ("execute : Ensure that Bipolar option is set to \'Yes\'")
    move_cursor ("Top menu")
    click       ("\'File->Done\'")    


def start_RT_step_ramp_run (initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance):
    
    goto        ("Qrius Main Window")
    click       ('Measurement Mode settings')
    click       ('Electrical DC Conductivity')
    
    set_RT_step_ramp_measurement_settings(initial_temperature, final_temperature, temperature_step, V_range, I_range, max_power, pre_stabilization_delay, post_stabilization_delay, monitoring_period, tolerance)
    write("Update_Database Lab_Space,PQMS,XSMU,Mode,R-T")
    write("Update_Database Lab_Space,PQMS,XTCON,Mode,Stepped_Ramp")
    
    click ('Start Button')
    write ("Update_Database Lab_Space,PQMS,XSMU,Running,True")
    write ("execute : Wait until graph comes to an end")
    
    write ("Update_Database Lab_Space,PQMS,XSMU,Running,False")
    save_graph()




###############################################################################
#R_Tme_linear_ramp functions

def set_RT_linear_ramp_measurement_settings (final_temperature, ramp_rate, run_mode, I_range, V_range, max_power):
    
    move_cursor ('Run control')
    click       ('drop down menu')
    click       ('R-T (linear ramp)')
    
    move_cursor ('Toolbar')
    click       ('Settings->Temperature controller')
    click       ('Linear ramp settings')
    write       ("execute : Set Final Temperature to " + str(final_temperature))
    write       ("execute : Set Ramp rate to " + ramp_rate + " K/min")
    click       ('File->Apply')
   
    move_cursor ('Toolbar')
    click       ('Settings->I-V Source and Measurement Unit')
    click       ("Settings->Source Parameters")
    write       ("execute : Set mode as constant " + run_mode)
    move_cursor ("Top Menu")
    click       ("File->Done")
    
    move_cursor ("Top Menu")
    click       ("Settings->Resistance Measurement Settings")
    write       ("execute : Set voltage limit as " + V_range)
    write       ("execute : Set current limit as " + I_range)
    write       ("execute : Set max_power as " + max_power)
    write       ("execute : Set Bipolar as No")
    move_cursor ("Top Menu")
    click       ('File->Done')

def start_RT_linear_ramp (initial_temperature, final_temperature, ramp_rate, run_mode, I_range, V_range, max_power):
    
    goto        ("Qrius Main Window")
    click       ('Measurement Mode settings')
    click       ('Electrical DC Conductivity')
    
    set_RT_linear_ramp_measurement_settings (final_temperature, ramp_rate, run_mode, I_range, V_range, max_power)
    write("Update_Database Lab_Space,PQMS,XSMU,Mode,RT")
    write("Update_Database Lab_Space,PQMS,XTCON,Mode,Linear_Ramp")
    
    write       ("execute : Wait for heater temperature to reach"  + str(initial_temperature))
    
    click       ('Start')
    write       ("Update_Database Lab_Space,PQMS,XTCON,Running,True")
    write       ("Update_Database Lab_Space,PQMS,XSMU,Running,True")
    
    write       ("execute : Wait until graph comes to an end")
    
    write       ("Update_Database Lab_Space,PQMS,XTCON,Running,False")
    write       ("Update_Database Lab_Space,PQMS,XSMU,Running,False")
    save_graph()

###############################################################################
#R_Tme_isothermal functions

def set_R_Time_isothermal_measurement_settings (I_range, V_range, max_power, run_mode):
    move_cursor("Top Menu")
    click ("Settings->Source Parametres")
    write ("execute : Set mode as constant " + run_mode)
    move_cursor("Top Menu")
    click("File->Done")
    move_cursor("Top Menu")
    click("Settings->Resistance Measurement Settings")
    write ("execute : Set voltage limit as " + V_range)
    write ("execute : Set current limit as " + I_range)
    write ("execute : Set max_power as " + max_power)
    write("execute : Set Bipolar as No")
    move_cursor("Top Menu")
    click('File->Done')

def start_R_Time_isothermal( I_range, V_range, max_power, run_mode):
    
    click('I-V Source and measurement unit Window')
    move_cursor('Run Mode')
    click('Drop down menu')
    click('R-Time')
    set_R_Time_isothermal_measurement_settings( I_range, V_range, max_power, run_mode)
    write("Update_Database Lab_Space,PQMS,XSMU,Mode,R-Time")
    click ('Start Button')
    write ("Update_Database Lab_Space,PQMS,XSMU,Running,True")
    write ("execute : Wait until graph comes to an end")
    write ("Update_Database Lab_Space,PQMS,XSMU,Running,False")
    save_graph()

###############################################################################
#cryostat environment control functions

def set_up_pump ():
    
    write   ("execute : Ensure that any Insert is in the cryostat, and clamp is tightly fixed.")
    write   ("execute : Ensure that Pump.Release_Valve, Pump.Main_Valve, Sample_Chamber.Flush_Valve, Sample_Chamber.Evacuation_Valve, \
                        Heater_Chamber.Flush_Valve and Heater_Chamber.Evacuation_Valve are closed and all other valves connected to the pump are closed.")
    goto    ("Pump.Main_Valve")
    write   ("execute : Rotate Pump.Main_Valve in anticlockwise direction to turn the valve on.")
    write   ("Update_Database Lab_Space,PQMS,Pump,Main_Valve,State,ON")

def create_vaccum (chamber):
    
    write   ("execute : Turn on " + chamber + ".Evacuation_Valve by rotating in anticlockwise direction.")
    write   ("execute : Observe the Pirani Guage needle, and let it stabilize.")
    write   ("Update_Database Lab_Space,PQMS,Cryostat_Steel,Vaccum,YES")
    
def release_pressure (chamber):
    
        
    write   ("execute : Ensure that Pump.Release_Valve, Pump.Main_Valve, Sample_Chamber.Flush_Valve, Sample_Chamber.Evacuation_Valve, \
                    Heater_Chamber.Flush_Valve, Heater_Chamber.Evacuation_Valve and all other valves connected to Helium_Cylinder are closed")
    goto    ("Pump.Main_Valve")
    write   ("execute : Turn off Pump.Main_Valve by rotating it in clockwise direction.")
    write   ("execute : Turn on " + chamber + ".Evacuation_Valve by rotating in clockwise direction")
    write   ("execute : Open Pump.Release_Valve by turning in anticlockwise direction.")
    write   ("execute : Close the Pump.Release_Valve by turning in clockwise direction.")
    write   ("execute : Turn off " + chamber + ".Evacuation_Valve by rotating in anticlockwise direction")
    write   ("execute : Turn on Pump.Main_Valve by rotating it in anticlockwise direction.")
    write   ("Update_Database Lab_Space,PQMS,Cryostat_Steel,Vaccum,NO")
    write   ("Update_Database Lab_Space,PQMS,Cryostat_Steel,Helium,NO")
    
def restore_vaccum ():
    
    goto    ("Cryostat Cover")
    hold    ("Cryostat Cover")
    write   ("execute : Fix Cryostat cover on the cryostat opening")
    clamp   ()
    create_vaccum ("Sample_Chamber")
    create_vaccum ("Heater_Chamber")
    
def flush_helium (chamber):
    
    create_vaccum (chamber)
    write   ("execute : Ensure that any Insert is in the cryostat, and clamp is tightly fixed.")
    write   ("execute : Ensure that Pump.Release_Valve, Pump.Main_Valve, Sample_Chamber.Flush_Valve, Sample_Chamber.Evacuation_Valve, \
                        Heater_Chamber.Flush_Valve, Heater_Chamber.Evacuation_Valve and all other valves connected to Helium_Cylinder are closed")
    
    write   ("execute : Open " + chamber + ".Evacuation_Valve by rotating in anticlockwise direction.")
    write   ("execute : Turn off Pump.Main_Valve by rotating it in clockwise direction.")
    
    goto    ("Helium_Cylinder.Main_Valve")
    write   ("execute : Ensure that Helium_Cylinder.Pressure_Valve is closed (completely unscrewed loose in anticlockwise direction).")
    write   ("execute : Open the "+chamber+".Flush_Valve to relese residual pressure")
    write   ("execute : Close the "+chamber+".Flush_Valve when helium pressure gauge reads 0 psi") 
    write   ("execute : Open Helium_Cylinder.Main_Valve by rotating in anticlockwise direction.")
    write   ("execute : Turn the Helium_Cylinder.Pressure_Valve clockwise slightly until pressure guage reads about 10 psi.")
    
    rapid_movement()
    
    write   ("execute : Open " + chamber + ".Flush_Valve by rotating in anticlockwise direction.")
    write   ("execute : After 2 seconds, turn off " + chamber + ".Flush_Valve by rotating in clockwise direction")
    
    goto    ("Helium_Cylinder.Pressure_Valve")
    write   ("execute : Close Helium_Cylinder.Pressure_Valve by rotating in anticlockwise direction until completely unscrewed loose.")
    
    write   ("execute : Open Pump.Release_Valve by turning in anticlockwise direction.")
    write   ("execute : Immediately, close the Pump.Release_Valve by turning in clockwise direction.")
    
    write   ("execute : Close " + chamber + ".Evacuation_Valve by rotating in clockwise direction")
    write   ("execute : Turn on Pump.Main_Valve by rotating it in anticlockwise direction.")
    
    goto    ("Helium_Cylinder.Main_Valve")
    write   ("execute : Close Helium_Cylinder.Main_Valve by rotating in anticlockwise direction.")
    
    end_rapid_movement()
    
    write   ("Update_Database Lab_Space,PQMS,Cryostat_Steel,Helium,YES")
    
def pour_liquid_nitrogen ():
    
    start_XTCON_monitor()
    goto    ("Cryocan_BA11.Home_Coordinates")
    hold    ("Cryocan_BA11.Cap")
    write   ("execute : Remove the lid and cap from the cryocan")
    goto    ("Puck_Screwing_Coordinates")
    leave   ("Cryocan_BA11.Cap")
    
    write   ("execute : Check if there is liquid nitrogen in the BA11 cryocan: If yes, continue. If no, sample can't be cooled; abort")
    
    hold    ("Cryocan_BA11")
    goto    ("PQMS.Funnel")
    write   ("execute : Tilt the cryocan onto the funnel to pour liquid nitrogen into the funnel")
    write   ("execute : Fill the required amount of Liquid nitrogen")
    
    write   ("Update_Database Lab_Space,PQMS,Cryostat_Steel,Cryocan,Liquid_Nitrogen,YES")
    
    goto    ("Cryocan_BA11.Home_Coordinates")
    leave   ("Cryocan_BA11")
    goto    ("Puck_Screwing_Coordinates")
    hold    ("Cryocan_BA11.Cap")
    goto    ("Cryocan_BA11.Home_Coordinates")
    write   ("execute : Replace _Ba11.Cap")
    end_XTCON_monitor()

#####################################################################
#misc qrius utilities

def save_graph():
   
    move_cursor ("Toolbar below the graph")
    click ("Save Icon")
    write ("execute : Select the path, and choose an appropriate name")
    click ("'Save'")
        
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
    write("execute : In the 'Sample Details' section, fill in '" + sample_name + "' as sample name")
    write("execute : In the 'Sample Details' section, fill in '" + sample_number + "' as sample number")
    write("execute : In the 'Sample Details' section, fill in '" + sample_description + "' as description")
    click ("'File->Apply'")



