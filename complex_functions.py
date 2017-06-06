import time
import primitive_functions
from primitive_functions import *

#####################################################################

def sample_is_mounted():
    write ("Sample is already mounted. Continuing to next step...") 

def do_not_unmount():
    write ("Not unmounting the sample")

def set_up_soldering_iron():
    '''Set up soldering space and iron for use'''
    
    goto('SOLDERING_STATION')
    write("execute : Check if soldering station is free or not")
    write("execute : If 'Free' then Leave test_object or else wait until it gets free and then Leave test_object")
    write("execute Switch On Soldering_Iron")
    write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,ON")
    write("execute : Wait for the soldering iron LED to start blinking.")
    
def solder (terminal_a, terminal_b, Sample, Sample_Box):
    '''Solder terminal_b onto terminal_b, given Sample from Sample_Box'''
    
    write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,State,IN_USE")
    
    goto   ('Soldering_Iron.Home_Coordinates')
    hold   ('Soldering_Iron')
    
    goto   ('Flux.Home_Coordinates')
    write  ("execute : Plunge the Tip into the Flux")
    write  ("execute : Retract the Tip")
    
    goto   ('Solder.Home_Coordinates')
    write  ("execute : Move the Soldering_Iron along the Solder")
    
    write  ("execute : Goto juntion of " + terminal_a + " and "+terminal_b)
    write  ("execute : Wait until sensor deems soldering between " + terminal_a + " and " + terminal_b + " to be complete")
    
    write  ("Update_Database Lab_Space,Sample_Table,Sample_Boxes," + Sample_Box + "," + terminal_a + ",Soldered,YES")
    write  ("Update_Database Lab_Space,PQMS," + terminal_b + ",Soldered,YES")
    
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


def clamp():
    '''Clamp PQMS insert to Cryostat'''
    
    read_state ('Lab_Space,PQMS,Clamp')
    move       ('Clamp.Home_Coordinates', 'PQMS.Clamp_Coordinates')    
    write      ("execute : Use the other hand to revolve the clamp till 180 degrees")
    write      ("execute : Revolve the screw of the clamp till it is in closing position")
    rotate     ('Screw','14 turns','clockwise')
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


def connect_cable (cable, test_object):
    '''Connects 'cable' to its respective connector on test_object.'''
    
    read_state  ('Lab_Space,PQMS,Cables,' + cable)
    move        (cable + ".Cryostat_End", test_object + "." + cable + "_Terminal")
    write       ("Align " + cable + "'s connector with "  + test_object + "'s connector")
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
        solder(Sample +',Terminal_1', 'Insert_RT_Puck,Puck,Terminal_4', Sample, Sample_Box)
        
        write ("execute : Bend " + Sample + "'s terminals as required.")

        move(Sample+"'s Terminal_2", "Insert_RT_Puck,Puck,Terminal_1")
        solder(Sample + "'s,Terminal_2", "Insert_RT_Puck,Puck,Terminal_1", Sample, Sample_Box)

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
        solder(Sample + ',Terminal_1', 'Insert_RT_Old,Terminal_1', Sample, Sample_Box)
        
        write ("execute : Bend " + Sample + "'s terminals as required.")

        move(Sample+'.Terminal_2', 'Insert_RT_Old,Terminal_4')
        solder(Sample+',Terminal_2', 'Insert_RT_Old,Terminal_4', Sample, Sample_Box)

        write("Update_Database Lab_Space,PQMS,Insert_RT_Old,Sample_Mounted,YES")
        write("execute : Switch off the soldering iron")
        write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,OFF")
        #SOLDERING PROCESS
        
        write("execute : Stick " + Sample + "'s body to the mounting surface with Kapton tape")
        
    
    goto('Tweezers.Home_Coordinates')
    leave('Tweezers')


def load_sample(Sample, Sample_Box, test_object):
    
    if (test_object == "Insert_RT_Puck"):
        remove('Puck','Puck_Board')
        write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Puck_Board_Connection,DISCONNECTED")

        goto('Puck_Screwing_Coordinates')
        leave('Puck')
        read_state('Lab_Space,PQMS,Insert_RT_Puck')
        move('Insert_RT_Puck', 'Insert_RT_Puck.Exit_Coordinates')
        goto('Puck_Screwing_Coordinates')
        hold('Puck')
        write("execute : Align Puck for screwing")
        rotate('Puck','14 turns','clockwise')
        write("execute : Align Insert2Puck Cable with Puck Pins")
        write("execute : Insert the pin_holes into the puck pins")
        write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Insert_Connection,CONNECTED")
        write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Insert2Puck_Cable,State,CONNECTED")
        goto('Insert_RT_Puck.Exit_Coordinates')
        goto('Insert_RT_Puck.Home_Coordinates')

        clamp()
        
        connect_cable('RT_Cable', test_object)
        connect_cable('HT_Cable', test_object)
        
    elif (test_object == "Puck_Board"):
        
        write ("Sample Puck is already connected to Puck_Board")
        move ("Puck_Board", "PQMS.Home_Coordinates")
        connect_cable('RT_Cable', test_object)
    
    elif (test_object == "Insert_RT_Old"):
        
        move('Insert_RT_Old', 'Insert_RT_Puck.Exit_Coordinates')
        goto('Insert_RT_Puck.Home_Coordinates')
        
        clamp()
        
        connect_cable('RT_Cable', test_object)
        connect_cable('HT_Cable', test_object)
        
        
        
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
        goto    (Sample_Box + ".Exit_Coordinates")
        goto    (Sample+".Rest_ Coordinates")
        leave   (Sample)
        
        write   ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+","+Sample+",State,NOT_IN_USE")
        goto    (Sample_Box+".Exit_Coordinates")
        write   ("execute : close the lid of the box")
        write   ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,CLOSED")
        goto    ("Tweezer.Rest_Coordinates")
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
        goto    (Sample+"_Terminal_1")
        hold    (Sample+"_terminal_1")
        goto    (Sample_Box + ".Exit_Coordinates")
        goto    (Sample+".Rest_ Coordinates")
        leave   (Sample)
        
        write   ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+","+Sample+",State,NOT_IN_USE")
        goto    (Sample_Box+".Exit_Coordinates")
        write   ("execute : close the lid of the box")
        write   ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,CLOSED")
        goto    ("Tweezer.Rest_Coordinates")
        leave   ("Tweezer")


def unload_sample(Sample, Sample_Box, test_object):
    
    if (test_object == "Insert_RT_Puck"):
        
        disconnect_cable("RT_Cable")
        disconnect_cable("HT_Cable")
        unclamp()
        
        goto("Insert_RT_Puck")
        hold("Insert_RT_Puck")
      
        goto("Insert_RT_Puck.Exit_Coordinates")
        goto("Sample_Table.Puck_Screwing_Coordinates")
        remove("Insert2Puck_Cable", "Insert_RT_Puck")
        
        write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Insert_Connection,DISCONNECTED")
        write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Insert2Puck_Cable,State,DISCONNECTED")
        read_state("Lab_Space,PQMS,Insert_RT_Puck,Puck")
        
        goto("Puck")
        hold("Puck")
        rotate('Puck','14 turns','anticlockwise')
        leave("Puck")
        
        goto("Insert_RT_Puck.Exit_Coordinates")
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
        
        disconnect_cable("RT_Cable")
        disconnect_cable("HT_Cable")
        move ("Puck_Board", "Puck_Board.Home_Coordinates")
        
    elif (test_object == "Insert_RT_Old"):
        disconnect_cable("RT_Cable")
        move ("Insert_RT_Old", "Insert_RT_Old.Exit_Coordinates")
        goto ("Sample_Mounting_Coordinates")
        

#####################################################################


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
    
    goto   ("PQMS.Pump.Power_Cable")
    write  ("execute : Switch on Pump.Power_Cable")
    write  ("Update_Database Lab_Space,PQMS,Pump,State,ON")
    
    #goto ("PQMS.Pirani_Gauge.Power_Cable")
    #write ("execute : Switch on Pirani_Gauge.Power_Cable")
    #write ("Update_Database Lab_Space,PQMS,Pump,State,ON")

def switch_off_PQMS_modules():
    read_state ("Lab_Space,PQMS")

    goto   ("PQMS.XPLORE_Power_Supply.Power_Cable")
    write  ("execute : Switch off XPLORE_Power_Supply.Power_Cable")
    write  ("Update_Database Lab_Space,PQMS,XPLORE_Power_Supply,State,OFF")
    write  ("Update_Database Lab_Space,PQMS,XSMU,State,OFF")
    
    goto   ("PQMS.XTCON.Power_Cable")
    write  ("execute : Switch off XTCON.Power_Cable")
    write  ("Update_Database Lab_Space,PQMS,XTCON,State,OFF")
    
    goto   ("PQMS.Pump.Power_Cable")
    write  ("execute : Switch off Pump.Power_Cable")
    write  ("Update_Database Lab_Space,PQMS,Pump,State,OFF")
    
    goto   ('Stabilizer.Power_Switch')
    write  ("execute : Switch OFF Stabilizer.Power_Switch")
    write  ("Update_Database Lab_Space,PQMS,Stabilizer,Power_Switch,State,OFF")
    
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

    
def init_XTCON_isothermal(test_object):
    
    click       ('Temperature Controller Window')
    move_cursor ('Control mode')
    click       ('drop down menu')
    click       ('Isothermal')
    move_cursor ('Instrument Control')
    click       ('Cryostat and Insert')
    click       ('Cryostat Type')
    click       ('Double Walled Steel Cryostat')
    click       ('Insert Type')
    click       (test_object)
    click       ('File->Hide')
    click       ('Start Button')
    write       ("Update_Database Lab_Space,PQMS,XTCON,Running,True")

def set_XTCON_temp (temperature_set_point):
    
    click       ('Temperature Controller Window')
    move_cursor ('Toolbar')
    click       ('Settings')
    click       ('Isothermal Settings')
    write       ("Update_Database Lab_Space,PQMS,XTCON,Mode,ISOTHERMAL")
    write       ("execute : Set 'Heater Set point' Temperature to " + temperature_set_point + " K")
    move_cursor ('Toolbar')
    click       ('File->Apply')
    write       ("execute : Wait till sample temperature stabilizes")

def stop_XTCON_run():
    click   ('Temperature Controller Window')
    write   ("execute : Stop Temperature Controller Run")
    write   ("Update_Database Lab_Space,PQMS,XTCON,Running,False")
	
def start_IV_run (V_range , V_step, I_max, I_step, power):
    click('I-V Source and measurement unit Window')
    move_cursor('Run Mode')
    click('Drop down menu')
    click('I-V')
    set_measurement_settings(V_range, V_step, I_max, I_step, power)
    write("Update_Database Lab_Space,PQMS,XSMU,Mode,I-V")
    click ('Start Button')
    write ("Update_Database Lab_Space,PQMS,XSMU,Running,True")
    write ("execute : Wait until graph comes to an end")
    write ("Update_Database Lab_Space,PQMS,XSMU,Running,False")
    save_graph()
        
def set_measurement_settings(V_range, V_step, I_max, I_step, power):
    #write ("execute : In the top menu, click on \'Settings->Source Parameters\'")
    #from the drop down menu, click on constant voltage
    #click on file, and then done
    move_cursor ("Top menu")
    click ("\'Settings->I-V Measurement Settings\'")
    write ("execute : Set voltage max as " + V_range + " mV")
    write ("execute : Set voltage step size as " + V_step + " mV")
    write ("execute : Set current max as " + I_max + " uA")
    write ("execute : Set current step size as " + I_step + " uA")
    write ("execute : Set power max as " + power + " mW")
    write ("execute : Ensure that Bipolar option is set to \'Yes\'")
    move_cursor ("Top menu")
    click ("\'File->Done\'")
    
def save_graph():
   
    move_cursor ("Toolbar below the graph")
    click ("Save Icon")
    write ("execute : Select the path, and choose an appropriate name")
    click ("'Save'")
    
def set_up_PQMS_modules ():

    write ("execute : In the Qrius window, click on 'Modules Manager'.")
    
    click ("Temperature Controller")
    write("execute : Check if XTCON PC Connection has been established")
    write("execute : If No, then click on 'File->Connect'. If Yes, do nothing.")
   
    click ("IV Source and Measurement")
    write("execute : Check if XSMU PC Connection has been established")
    write("execute : If No, then click on 'File->Connect'. If Yes, do nothing.")
    
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


#####################################################################
