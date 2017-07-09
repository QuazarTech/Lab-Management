import time
from lab_reset import put_in_folder_aborted
from pylab import *
from lab_reset import *
import yaml as yaml
import sys
import os

diff_file  = "run_data_diff.txt"
new_dbase  = "run_data_new_database"
time_array = []

####################################################################

def get_user_data():
    robot    = raw_input("\nEnter robot ID : \n")
    sensor   = raw_input("\nEnter sensor ID: \n")
    observer = raw_input("\nEnter observer ID: \n")
    return robot, sensor, observer

def initialize_database(database_name):
	with open(database_name+".yaml", "r") as f:
		data = yaml.load(f)
		fbase = open(new_dbase + ".yaml", "w")
		yaml.dump(data, fbase, default_flow_style=False)
		fbase.close()
		f.close()

def check_database_validity(database):	
	try:	
		initialize_database (database)
	except Exception as e:
		print ("Invalid Database!!\n. Error : "+ str(e))
		database  = raw_input("Enter the starting database (lab_database, if starting from scratch) :\n")
		check_database_validity(database)

####################################################################

database  = raw_input("Enter the starting database (lab_database, if starting from scratch) :\n")
check_database_validity (database)
robot,sensor,observer = get_user_data()

log = open ("run_data_execution_log.txt", "w")
log.write  ("Robot              : " + robot + "\n")
log.write  ("Sensor             : " + sensor + "\n")
log.write  ("Observer           : " + observer + "\n")
log.write  ("Time               : " + time_in_ist('%H:%M:%S') + "\n")
log.write  ("Starting Database  : " + database + "\n\n")
log.close()

dbase = open(diff_file, "w")
dbase.close()

####################################################################
    		
def update_database(line):
	with open(diff_file, "a") as dbase:
            dbase.write(line +'\n')
        param_array, data = read_database(line, new_dbase, 0)
        write_to_database(param_array, data)


def read_database(line, base, index):
	fbase = open(base + ".yaml", "r")
        data = yaml.safe_load(fbase)
        param_array = []
        param_array = line[index:].strip('\n').split(",")
        fbase.close()
        return param_array, data

def return_value(param_array):
	fbase = open(new_dbase + ".yaml", "r")
	data = yaml.safe_load(fbase)
	z = data['Lab_Space']
        for param in param_array[1:(len(param_array) - 1)]:
            z = z[param]
        return z[param_array[len(param_array) - 1]]

def write_to_database(param_array, data):
	z = data['Lab_Space']
        for param in param_array[1:(len(param_array) - 2)]:
            z = z[param]
        z[param_array[len(param_array) - 2]] = param_array[len(param_array) - 1]
        fname = open(new_dbase + ".yaml", 'w')
        yaml.dump(data, fname, default_flow_style=False)
        fname.close()
        
def print_states (log, line, new_dbase):
	print(line + '\n')
        param_array, data = read_database(line, new_dbase, 25)
        z = data["Lab_Space"]
        for param in param_array[1:(len(param_array) - 1)]:
            z = z[param]
        param = param_array[len(param_array) - 1]
        print yaml.dump(z[param], allow_unicode=True, default_flow_style=False)
        user_input = raw_input("Comments, if any : (Press Enter to continue, type \
            'pause' to pause, or 'end' to abort) : ")
        temp = time_in_ist('%H:%M:%S')
        
        if(user_input == "end"):
            abort_execution(log, temp)
        
        elif (user_input == "pause"):
            pause_execution(log, temp)
            
        else:
            print temp + '\n'
        
        time_array.append(time_in_ist('%H:%M:%S'))
        time_stamp_and_comments(log, line, temp, user_input)

#####################################################################

def abort_execution(line, log, temp):
	print temp
        string = "***********" + "\n" + "EXECUTION ABORTED" + "\n" + "***********"
        reason = raw_input("What is the reason for aborting the execution?\n")
	with open (log.name, "a") as log:
        	log.write(string + '\n')
		log.write("Execution has come to an end due to error in line: " + line + '\n')
		log.write("ERROR - " + reason + '\n')
	log.close() 
	return string


def pause_execution(log, temp):
	print temp
        string = "***********" + "\n" + "EXPERIMENT PAUSED" + "\n" + "***********"
        reason = raw_input("Why has the execution been paused?\n")
	with open (log.name, "a") as log:
		log.write(string + '\n')
		log.write("Execution has been paused at: " + temp + '\n')
		log.write("PAUSE - " + reason + '\n')
	log.close()

	response = raw_input("Type 'resume' to resume the experiment :")
	while (response != 'resume'):
		response = raw_input("Type 'resume' to resume the experiment :")

	string = "***********" + "\n" + "EXPERIMENT RESUMED" + "\n" + "***********"
	with open (log.name, "a") as log:
		log.write(string + '\n')
		log.write("Execution has been resumed at: " + temp + '\n')
	log.close()
	
#####################################################################

def time_stamp_and_comments(log, line, temp, user_input):
	with open (log.name, "a") as log:
            log.write(line + '\nend:\t\t\t\t' + temp + '\n\n')
        log.close()
        if(user_input != ""):
            with open (log.name, "a") as log:
                log.write("Comment : " + user_input + '\n\n')
            log.close()


def write(line):
	log = open ("run_data_execution_log.txt", "a")
	if (line[0:7] != 'execute'):
		print(line)
		with open (log.name, "a") as log:
			log.write(line + '\n')
			log.close()

	else:
		if(line[10:14] != 'Read'):
			print(line + '\n')
			user_input = raw_input("Comments, if any : (Press Enter to continue, type 'pause' to pause or 'end' to abort) : ")
			temp = time_in_ist('%H:%M:%S')
			if (user_input == "end"):
				string = abort_execution(line, log, temp)
				put_in_folder_aborted (log, diff_file, new_dbase)
				sys.exit(string)

			elif (user_input == "pause"):
				pause_execution(log, temp)

			else:
				print temp + '\n'

			time_array.append (time_in_ist('%H:%M:%S'))
			time_stamp_and_comments(log, line, temp, user_input)

		else:
			print_states(log, line, new_dbase)
