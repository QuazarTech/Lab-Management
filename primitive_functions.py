import time
from pylab import *
from pytz import timezone
import datetime

###############################################################################

procedure = "run_data_procedure.txt"
f = open(procedure, 'w')
f.close()

time_zone = timezone("Asia/Kolkata")

def time_in_ist():
    now_utc = datetime.datetime.now(timezone("UTC"))
    now_india = now_utc.astimezone(time_zone)
    return now_india.strftime('%H:%M:%S')

###############################################################################

def write(command):
    
    with open(procedure, 'a') as f:
        f.write(command + '\n')
    f.close()
    
    #print (command)
    #raw_input("Press Enter to continue")

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

###############################################################################