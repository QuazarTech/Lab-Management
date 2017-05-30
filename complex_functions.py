import time
import primitive_functions
from primitive_functions import *


def solder(obj1,obj2, Sample, Sample_Box):
        write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Status,IN_USE")
	write("execute : Check if soldering station is free or not")
	write("execute : If 'Free' then Leave Puck_Board or else wait until it gets free and then Leave Puck_Board")
	write("execute Switch On Soldering_Iron")
	write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,ON")

	write("execute : Wait for the soldering iron to heat up.")

	read_state('Lab_Space,Sample_Table,Soldering')
	read_state('Lab_Space,Sample_Table,Sample_Boxes,' + Sample_Box + ',' + Sample)
	goto('Soldering_Iron.Home_Coordinates')
	hold('Soldering_Iron')
	goto('Soldering_Iron.Exit_Coordinates')
	goto('Flux.Home_Coordinates')
	write("execute : Plunge the Tip into the Flux")
	write("execute : Retract the Tip")
	goto ('Solder.Home_Coordinates')
	write("execute : Move the Soldering_Iron along the Solder")
	write("execute : Goto juntion of "+obj1+ " and "+obj2)
	write("execute : Wait until sensor deems soldering between " + obj1 + " and " + obj2 + " to be complete")
	write("Update_Database Lab_Space,Sample_Table,Sample_Boxes," + Sample_Box + "," + Sample + ",Terminal_1,Soldered,YES")
	write("Update_Database Lab_Space,PQMS,Insert_RT_Puck," + obj2 + ",Soldered,YES")
	goto('Cleaning_Pad.Home_Coordinates')
	write("execute : Plunge Tip in Cleaning Pad")
	write("execute : Retract Tip")
	goto('Soldering_Iron.Exit_Coordinates')
	goto('Soldering_Iron.Home_Coordinates')
	leave('Soldering_Iron')
	write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Status,NOT_IN_USE")
    
def clamp():
	read_state('Lab_Space,PQMS,Clamp')
	goto('Clamp.Home_Coordinates')
	hold('Clamp')
	goto('PQMS.Clamp_Coordinates')	
	write("execute : Use the other hand to revolve the clamp till 180 degrees")
	write("execute : Revolve the screw of the clamp till it is in closing position")
	rotate('Screw','7 turns','clockwise')
	write("Update_Database Lab_Space,PQMS,Clamp,Status,LOCKED")

def connect_cable(obj):
	read_state('Lab_Space,PQMS,Cables,'+obj)
	locate(obj)
	goto(obj)
	hold(obj)
	goto(obj+'.Cryostat_End')
	write("execute : Align "+obj+" with pins")
	write("execute : Insert and fasten "+obj)
	write("Update_Database Lab_Space,PQMS,Cables,"+obj+",Status,CONNECTED")



def unclamp():
    read_state("Lab_Space,PQMS,Clamp")
    read_state("Lab_Space,PQMS,Insert_RT_Puck")
    goto("Clamp.Current_Coordinates")
    hold("the clamp with one hand")
    write("execute : With other hand, Rotate the screw anti-clockwise for required number of turns")
    write("execute : Revolve the screw of the clamp till it is in opening position")
    write("execute : Use the other hand to revolve the clamp till it's straight.")
    write("Update_Database Lab_Space,PQMS,Clamp,Status,UNLOCKED")
    goto("Clamp.Home_Coordinates")
    leave("Clamp")

def desolder(Sample, Sample_Box):
    write("execute : Check if soldering station is free")
    write("execute : if Yes,Then leave(Puck_board). if not, wait until free and then leave(Puck_board)")
    write("execute : Switch on Soldering_Iron")
    write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,ON")
    write("execute : Wait for the soldering iron to heat up.")
    read_state("Lab_Space,Sample_Table,Soldering")
    read_state("Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+","+Sample+",Terminal_1")
    write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Status,IN_USE")
    goto("Soldering_Iron")
    hold("Soldering_Iron")
    goto("Soldering_Iron.Exit_Coordinates")
    read_state("Lab_Space,Sample_Table,Soldering")
    goto("Flux.Home_Coordinates")
    write("execute : Plunge the tip into the flux")
    write("execute : Retract the tip")
    goto (Sample +"_Terminal_1")
    write("execute : Wait until sensor deems soldering removed")
    goto("Cleaning_Pad.Home_Coordinates")
    write("execute : Plunge tip in Cleaning_Pad")
    write("execute : Retract Tip")
    write("Update_Database Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,Zener_1,Terminal_1,Soldered,NO")
    write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Terminal_1,Soldered,NO")
    goto (Sample+"_terminal_2")
    write("execute : Wait until sensor deems soldering removed")
    write("Update_Database Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,Zener_1,Terminal_2,Soldered,NO")
    write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Terminal_4,Soldered,NO")
    write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Sample_Mounted,NO")
    goto("Cleaning_Pad.Home_Coordinates")
    write("execute : Plunge tip in Cleaning_Pad")
    write("execute : Retract Tip")
    goto("Soldering_Iron.Exit_Coordinates")
    goto("Soldering_Iron.Home_Coordinates")
    leave("Soldering_Iron")
    write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Status,NOT_IN_USE")
    write("execute : Switch off Soldering Iron")
    write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,OFF")

def load_sample(Sample, Sample_Box):
    read_state('Lab_Space,Sample_Table')
    read_state('Lab_Space,PQMS')

    move('Puck_Board','Sample_Mounting_Coordinates')
    leave('Puck_Board')
    remove('cap',Sample_Box)
    write("Update_Database Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+",State,OPEN")

    hold_sample(Sample, Sample_Box)
    close_lid(Sample_Box)

    write("execute : Remove Sticky Tape from "+ Sample)
    goto('Puck_Board')
    hold('Puck_Board')
    #SOLDERING PROCESS STARTS
    goto('SOLDERING_STATION')

    move(Sample+'.Terminal_1', 'Puck.Terminal_1')
    solder(Sample+'.Terminal_1', 'Puck,Terminal_1', Sample, Sample_Box)

    move(Sample+'.Terminal_2', 'Puck,Terminal_4')
    solder(Sample+'.Terminal_1', 'Puck,Terminal_4', Sample, Sample_Box)

    write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Sample_Mounted,YES")
    write("execute : Switch off the soldering iron")
    write("Update_Database Lab_Space,Sample_Table,Soldering,Soldering_Iron,Power,OFF")
    #SOLDERING PROCESS ENDS

    read_state('Lab_Space,Sample_Table')
    read_state('Lab_Space,PQMS')
    
    move ('Puck_Board', 'Puck_Board.Home_Coordinates')
    leave('Puck_Board')
    
    goto('Tweezers.Home_Coordinates')
    leave('Tweezers')

    remove('Puck','Puck_Board')
    write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Puck_Board_Connection,DISCONNECTED")

    goto('Puck_Screwing_Coordinates')
    leave('Puck')
    read_state('Lab_Space,PQMS,Insert_RT_Puck')
    move('Insert_RT_Puck', 'Insert_RT_Puck.Exit_Coordinates')
    goto('Puck_Screwing_Coordinates')
    hold('Puck')
    write("execute : Align Puck for screwing")
    rotate('Puck','7 turns','clockwise')
    write("execute : Align Insert2Puck Cable with Puck Pins")
    write("execute : Insert the pin_holes into the puck pins")
    write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Insert_Connection,CONNECTED")
    write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Insert2Puck_Cable,Status,CONNECTED")
    goto('Insert_RT_Puck.Exit_Coordinates')
    goto('Insert_RT_Puck.Home_Coordinates')

    clamp()
    connect_cable('RT_Cable')
    connect_cable('HT_Cable')


def unload_sample(Sample, Sample_Box):
    read_state("Lab_Space,Sample_Table,Sample_Boxes")
    read_state("Lab_Space,PQMS")
    read_state("Lab_Space,Sample_Table,Soldering")
    locate("RT_Cable.Cryostat_End")
    goto("RT_Cable.Cryostat_End")
    hold("RT_Cable.Cryostat_End")
    write("execute : Unfasten and Remove RT_Cable")
    write("Update_Database Lab_Space,PQMS,Cables,RT_Cable,Status,DISCONNECTED")
    leave("RT_Cable.Cryostat_End")
    write("execute : Locate HT_Cable.Cryostat_End")
    goto("HT_Cable.Cryostat_End")
    hold("RT_Cable.Cryostat_End")
    write("execute : Unfasten and Remove HT_Cable")
    write("Update_Database Lab_Space,PQMS,Cables,HT_Cable,Status,DISCONNECTED")
    goto("Insert HT cable.Cryostat_End.Rest_Coordinates")
    leave("HT_Cable.Cryostat_End")
    move("RT_Cable.Cryostat_End" , "RT_Cable.Home_Coordinates")
    leave("RT_Cable.Cryostat_End")
    unclamp()
    locate("Insert_RT_Puck")
    goto("Insert_RT_Puck")
    hold("Insert_RT_Puck")
    write("execute : Take the Insert out of the Cryostat")
    goto("Sample_Table.Puck_Screwing_Coordinates")
    remove("Insert_RT_Puck.Insert2Puck_Cable", "Insert_RT_Puck")
    write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Insert_Connection,DISCONNECTED")
    write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Insert2Puck_Cable,Status,DISCONNECTED")
    read_state("Lab_Space,PQMS,Insert_RT_Puck,Puck")
    goto("Puck")
    hold("Puck")
    write("execute : Rotate it anticlockwise for required number of turns")
    leave("Puck")
    goto("Cryostat entrance")
    goto("Insert_RT_Puck.Home_Coordinates")
    leave("Insert_RT_Puck")
    goto("Sample_Table.Puck_Screwing_Coordinates")
    hold("Insert_RT_Puck.Puck")
    goto("Puck_Board.Home_Coordinates")
    write("execute : Align Puck pins with Puck_Board")
    write("execute : Insert Puck into Puck_Board")
    leave("Puck")
    write("Update_Database Lab_Space,PQMS,Insert_RT_Puck,Puck,Puck_Board_Connection,CONNECTED")
    hold("Puck_Board")
    goto ("Tweezers.Home_Coordinates")
    hold("Tweezers")
    goto(Sample + ".Terminal_1")
    hold(Sample + ".Terminal_1")
    goto("Soldering_Station")
    desolder(Sample, Sample_Box)
    locate("Puck_Board")
    goto("Puck_Board")
    hold("Puck_Board") 
    goto("Puck_Board.Home_Coordinates")
    leave("Puck_Board")
    goto("Sample_Table.Sample_Mounting_Coordinates")
    write("execute : straighten sample")
    write("execute : put a sticky note on the sample")
    leave(Sample)
    read_state("Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box)
    goto(Sample_Box +"'s Cap")
    hold("The Cap")
    write("execute : With other hand hold the " + Sample_Box + " and keep it fixed")
    write("execute : Move(cap, just above current coordinates) and separate it from sample_box")
    write("Update_Database Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,OPEN")
    goto(Sample+"_Terminal_1")
    hold(Sample+"_terminal_1")
    goto(Sample_Box + ".Exit_coordinates")
    goto(Sample+".Rest_ Coordinates")
    leave(Sample)
    write("Update_Database Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,Zener_1,State,NOT_IN_USE")
    goto(Sample_Box+".Exit_Coordinates")
    write("execute : close the lid of the box")
    write("Update_Database Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,CLOSED")
    goto("Tweezer.Rest_Coordinates")
    leave("Tweezer")
    
def switch_on_PQMS_modules():
    read_state("Lab_Space,PQMS")
    
    goto('Stabilizer.Power_Switch')
    write("execute : Switch On Stabilizer.Power_Switch")
    write("Update_Database Lab_Space,PQMS,Stabilizer,Power_Switch,State,ON")
    
    goto ("PQMS.XPLORE_Power_Supply.Power_Cable")
    write ("execute : Switch on XPLORE_Power_Supply.Power_Cable")
    write ("Update_Database Lab_Space,PQMS,XPLORE_Power_Supply,State,ON")
    
    goto ("PQMS.XSMU.Power_Cable")
    write ("execute : Switch on XSMU.Power_Cable")
    write ("Update_Database Lab_Space,PQMS,XSMU,State,ON")
    
    goto ("PQMS.XTCON.Power_Cable")
    write ("execute : Switch on XTCON.Power_Cable")
    write ("Update_Database Lab_Space,PQMS,XTCON,State,ON")
    
    goto ("PQMS.Pump.Power_Cable")
    write ("execute : Switch on Pump.Power_Cable")
    write ("Update_Database Lab_Space,PQMS,Pump,State,ON")
    
    
        
    #goto ("PQMS.Pirani_Gauge.Power_Cable")
    #write ("execute : Switch on Pirani_Gauge.Power_Cable")
    #write ("Update_Database Lab_Space,PQMS,Pump,State,ON")

def switch_off_PQMS_modules():
    read_state("Lab_Space,PQMS")
    
    goto ("PQMS.XPLORE_Power_Supply.Power_Cable")
    write ("execute : Switch off XPLORE_Power_Supply.Power_Cable")
    write ("Update_Database Lab_Space,PQMS,XPLORE_Power_Supply,State,OFF")
    
    goto ("PQMS.XSMU.Power_Cable")
    write ("execute : Switch off XSMU.Power_Cable")
    write ("Update_Database Lab_Space,PQMS,XSMU,State,OFF")
    
    goto ("PQMS.XTCON.Power_Cable")
    write ("execute : Switch off XTCON.Power_Cable")
    write ("Update_Database Lab_Space,PQMS,XTCON,State,OFF")
    
    goto ("PQMS.Pump.Power_Cable")
    write ("execute : Switch off Pump.Power_Cable")
    write ("Update_Database Lab_Space,PQMS,Pump,State,OFF")
    
    goto('Stabilizer.Power_Switch')
    write("execute : Switch OFF Stabilizer.Power_Switch")
    write("Update_Database Lab_Space,PQMS,Stabilizer,Power_Switch,State,OFF")
    
def switch_on_computer():
    locate('Computer')
    write ("execute : Switch on 'Computer'")
    write("execute : Press CPU Power Button")
    write("execute : Press Monitor Power Button")
    write("execute : Switch on the USB_Power_Adaptor")
    write("execute : Login to user account")
    locate ('Qrius')
    write("execute : Open Qrius ")
    
def configure_XTCON(set_point):
    goto('Qrius Main Window')
    click('Modules Manages')
    click('Temperature Controller')
    move_cursor('Toolbar')
    click('Settings')
    click('Isothermal Settings')
    write("execute : Set 'Heater Set point' Temperature to "+set_point)
    move_cursor('Toolbar')
    click('File')
    click('Apply')
    move_cursor('Control mode')
    click('drop down menu')
    click('Isothermal')
    move_cursor('Instrument Control')
    click('Cryostat and Insert')
    click('Cryostat Type')
    click('Double Walled Steel Cryostat')
    click('Insert Type')
    click('R-T insert with heater')
    click('File')
    click('Apply')
    write ("Update_Database Lab_Space,PQMS,XTCON,Mode,ISOTHERMAL")
    write ("Update_Database Lab_Space,PQMS,XTCON,Running,YES")

def configure_SMU(V_range , V_step):
    goto('Qrius Main Window')
    click('I-V Source and measurement unit')
    move_cursor('Run Mode')
    click('Drop down menu')
    click('I-V')
    set_measurement_settings(V_range, V_step)
    write("Update_Database Lab_Space,PQMS,XSMU,Mode,I-V")
    
#def select_mode (mode):
#    move_cursor('Run Mode')
#    click('Drop down menu')
#    click('I-V')

def start_run ():
    click ('Start Button')
    write ("Update_Database Lab_Space,PQMS,XSMU,Running,YES")
    write ("execute : Wait until graph comes to an end")
    save_graph()

    
def set_measurement_settings(V_range, V_step):
    write ("execute : In the top menu, click on \'Settings->Source Parameters\'")
    #from the drop down menu, click on constant voltage
    #click on file, and then done

    move_cursor ("Top menu")
    click ("\'Settings->I-V Measurement Settings\'")
    write ("execute : Set voltage range as " + V_range)
    write ("execute : Set voltage step size as " + V_step)
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
    write("execute : Ensure that the Temperature Controller is switched on and connected to PC")
    move_cursor("Toolbar at the top of Temperature Controller window")
    click("'File->Connect'")
   
    click ("IV Source and Measurement")
    write ("execute : Ensure that the IV Source and Measurement Unit is switched on and connected to PC")
    move_cursor ("Toolbar at the top of IV Source and Measurement window")
    click ("'File->Connect'")
    
def set_save_folder (sample_name, sample_number, sample_description, address):
    move_cursor ("Toolbar at the top of the Qrius Window")
    click ("'Global Settings'.")
    move_cursor ("'User Settings' section, next to the 'Data Folder' selection bar")
    click ("'Browse'")
    write ("execute : Select " + address + " as the path to store data.")
    click ("'OK'")
    write("execute : Exit the Global Settings")
    click ("'Sample Settings'")
    move_cursor ("Top of the window")
    click ("'File->New'")
    write("execute : In the 'Sample Details' section, fill in " + sample_name + " " + sample_number + " and " + sample_description + " in respective textboxes.")
    click ("'File->Apply'")


