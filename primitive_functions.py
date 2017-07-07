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

def check (obj, condition):
    write ("execute : Check if " + obj + " is " + condition)
    
def switch_on(obj):
    write("execute : Press the " + obj + " switch to turn it on.")
    
def switch_off(obj):
    write("execute : Press the " + obj + " switch to turn it off.")

def face(obj, direction):
    write("execute : Face the " + obj + " towards " + direction)
    
def align(obj1, obj2):
    write("execute : Align " + obj1 + " with " + obj2)