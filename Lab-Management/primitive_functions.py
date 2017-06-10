import time
from pylab import *
from pytz import timezone
import datetime

######################################################

time_zone = timezone("Asia/Kolkata")

procedure = "run_data_procedure.txt"
f = open(procedure, 'w')
f.close()

######################################################


def time_in_ist():
    now_utc = datetime.datetime.now(timezone("UTC"))
    now_india = now_utc.astimezone(time_zone)
    return now_india.strftime('%H:%M:%S')

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

    write ("execute : Goto "+ Sample+".Home_Coordinates")
    write ("execute : Hold "+ Sample +".Terminal_1")
    goto  ("Sample_Mounting_Coordinates")

    write ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,"+Sample_Box+","+Sample+",State,IN_USE")

def close_lid(obj1):
    write ("execute : Close the lid of " + obj1)
    write ("Update_Database Lab_Space,Sample_Table,Sample_Boxes,Box_Zener,State,CLOSED")
    
def click(obj):
    write("execute : Click on "+ obj)

def move_cursor(obj):
    write("execute : Move Cursor to "+ obj)

def write (command):
    with open(procedure, 'a') as f:
        f.write(command + '\n')
    f.close()