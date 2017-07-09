from data_logging import *

###############################################################################

def press (obj):
	write ("execute : Press the " + obj)

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
    
def switch_on(obj):
    write("execute : Press the " + obj + " switch to turn it on.")
    
def switch_off(obj):
    write("execute : Press the " + obj + " switch to turn it off.")

def face(obj, direction):
    write("execute : Face the " + obj + " towards " + direction)
    
def align(obj1, obj2):
    write("execute : Align " + obj1 + " with " + obj2)

def enter(text):
	write("execute : Type " + text)

def sample_is_mounted():
    write("Sample is already mounted. Continuing to next step...") 

def do_not_unmount():
    write("Not unmounting the sample")

#################################################################################
#Run Time responses

def check (obj, condition):
    write ("execute : Check if " + obj + " is " + condition)

def throw_exception (error):
    write("\n########### ERROR ###########\n")
    write(error)
    write("Terminating Execution\n")
    write("\n#############################\n")
    sys.exit(0)

def check_database(key, value):
    param_array      = key.strip('\n').split(',')
    database_value   = return_value(param_array)
    if (database_value == value):
        return True
    else:
        return False 
