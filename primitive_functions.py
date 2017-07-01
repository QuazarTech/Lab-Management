import data_logging
from data_logging import write,time_in_ist

###############################################################################

def read_state(obj):
    write ("execute : Read states of " + obj)
    
def goto(coord):
    write ("execute : Goto " + coord)

def hold(obj):
    write ("execute : Hold " + obj)

def leave(obj):
    write ("execute : Leave "+ obj)

def rotate(obj, number_of_turns, direction):
    write ("execute : Rotate "+ obj + " by " + number_of_turns + " in " + direction + " direction.")
    
def click(obj):
    write("execute : Click on "+ obj)

def move_cursor(obj):
    write("execute : Move Cursor to "+ obj)  

def take_photo(obj):
	write("execute : Take photo of "+ obj)


###############################################################################

def rapid_movement():
    write("***********Next few steps have to be performed rapidly********************")

def end_rapid_movement():
    write("***********Rapid Movement period is over, steps can be performed at normal speed****************")

###############################################################################
	
