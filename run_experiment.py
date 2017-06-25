import time
import yaml as yaml
import sys
import os

import IV_stepped_ramp
import RT_stepped_ramp
import R_Time_isothermal
import RT_linear_ramp
import unload_sample
import lab_reset
import CV_isothermal
import AC_voltage_measure
import susceptibility_experiment
import remove_sample_from_cryostat

#####################################################################

experiments = ["IV_stepped_ramp", "RT_stepped_ramp", "R_Time_isothermal", "unload_sample", "RT_linear_ramp","CV_isothermal","AC_voltage_measure", "susceptibility_experiment", "remove_sample_from_cryostat"]

#create and init and array for timestamps
time_array = []

#####################################################################

#response = raw_input ("Run again? : y/n")
#     while (response != 'n') or (response != 'y'):
#         response = raw_input ("Run again? : y/n")def get_sample_info():

#####################################################################


def get_experiment():
    
    print "\n\n Available Experiments: "
    print "______________________________\n"
    for item in experiments:
        print item
    print "______________________________\n"
    experiment = raw_input("Please select the experiment you want to do : \n")
    
    while (experiment not in experiments):
        print "Experiment not in list."
        print "\n\n Available Experiments: "
        print "______________________________\n"
        for item in experiments:
            print item
        print "______________________________\n"
        experiment = raw_input("Please select the experiment you want to do : \n")
    
    return experiment


def get_user_data():
    robot = raw_input("\nEnter robot ID : \n")
    sensor = raw_input("\nEnter sensor ID: \n")
    observer = raw_input("\nEnter observer ID: \n")
    return robot, sensor, observer


def update_database(line, diff_file, new_dbase):
	with open(diff_file, "a") as dbase:
            dbase.write(line[16:])
        param_array, data = read_database(new_dbase, 16)
        write_to_database(param_array, data)

#####################################################################

def read_database(base, index):
	fbase = open(base + ".yaml", "r")
        data = yaml.safe_load(fbase)
        param_array = []
        param_array = line[index:].strip('\n').split(",")
        fbase.close()
        return param_array, data


def write_to_database(param_array, data):
	z = data['Lab_Space']
        for param in param_array[1:(len(param_array) - 2)]:
            z = z[param]
        z[param_array[len(param_array) - 2]] = param_array[len(param_array) - 1]
        fname = open(new_dbase + ".yaml", 'w')
        yaml.dump(data, fname, default_flow_style=False)
        fname.close()
        
def print_states (experiment, log, line, new_dbase):
	print(line + '\n')
        param_array, data = read_database(new_dbase, 25)
        z = data["Lab_Space"]
        for param in param_array[1:(len(param_array) - 1)]:
            z = z[param]
        param = param_array[len(param_array) - 1]
        print yaml.dump(z[param], allow_unicode=True, default_flow_style=False)
        user_input = raw_input("Comments, if any : (Press Enter to continue, type \
            'pause' to pause, or 'end' to abort) : ")
        temp = experiment.time_in_ist('%H:%M:%S')
        
        if(user_input == "end"):
            abort_execution(experiment, log, temp)
        
        elif (user_input == "pause"):
            pause_execution(log, temp)
            
        else:
            print temp + '\n'
        
        time_array.append(experiment.time_in_ist('%H:%M:%S'))
        time_stamp_and_comments(log, line, temp, user_input)

#####################################################################

def abort_execution(experiment, log, temp):
	print temp
        string = "***********" + "\n" + "EXECUTION ABORTED" + "\n" + "***********"
	with open (log.name, "a") as log:
        	log.write(string + '\n')
		log.write("Execution has come to an end due to error in line: " + line + '\n')
	log.close()
	return string


def pause_execution(log, temp):
	print temp
        string = "***********" + "\n" + "EXPERIMENT PAUSED" + "\n" + "***********"
	with open (log.name, "a") as log:
		log.write(string + '\n')
		log.write("Execution has been paused at: " + temp + '\n')
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

def put_in_folder (experiment, log, diff_file, new_dbase):        
	t = experiment.time_in_ist('%Y_%m_%d_%H:%M:%S')
	folder_name = "run_data_" + experiment.name + "_" + t
	os.system("mkdir " + folder_name)
	os.system("mv " + experiment.procedure + " " + folder_name + "/")
	os.system("mv " + log + " " + folder_name + "/")
	os.system("mv " + diff_file + " " + folder_name + "/")
	os.system("mv " + new_dbase + ".yaml " + folder_name + "/")
	lab_reset.lab_reset(folder_name)
	create_duration_log (experiment, folder_name)

def time_stamp_and_comments(log, line, temp, user_input):
	with open (log.name, "a") as log:
            log.write(line + 'end:\t\t\t\t' + temp + '\n\n')
        log.close()
        if(user_input != ""):
            with open (log.name, "a") as log:
                log.write("Comment : " + user_input + '\n\n')
            log.close()

def initialize_database(database_name):
	with open(database_name+".yaml", "r") as f:
    		data = yaml.load(f)
    		fbase = open(new_dbase + ".yaml", "w")
    		yaml.dump(data, fbase, default_flow_style=False)
    		fbase.close()
    		f.close()

def create_duration_log (experiment, folder_name):
	f = open(folder_name + "/" + experiment.procedure, "r")
	fnew = open(folder_name + "/duration_log.txt", "w")
	fnew.write ("PQMS Data Run Time\n\n")
	i = 0
	for line in f:
		if (line == 'execute : Wait till sample temperature stabilizes\n'):
			a = str(time_array[i]) + "-" + str(time_array[i+1])
			fnew.write("Temperature Stabilization time:" + str(a) + "\n\n")
		elif (line == 'execute : Wait until graph comes to an end\n'):
			a = str(time_array[i]) + "-" + str(time_array[i+1])
			fnew.write("I_V run time:" + str(a) + "\n\n")
	        if(i == len(time_array) - 1):
	        	break
	 	i += 1 
 	fnew.close()
 	f.close()


#####################################################################

#user inputs

experiment  = eval(get_experiment())
read_file   =  experiment.procedure


robot, sensor, observer = get_user_data()

#create and init log file with user data
log = open (read_file[:-13] + "execution_log.txt", "w")
log.write("Robot : " + robot + "\n")
log.write("Sensor : " + sensor + "\n")
log.write("Observer : " + observer + "\n")
log.write("Time : " + experiment.time_in_ist('%H:%M:%S') + "\n")
log.close()

time_array.append(experiment.time_in_ist('%H:%M:%S'))

diff_file = read_file[:-13] + "diff.txt"
new_dbase = read_file[:-13] + "new_database"
dbase = open(diff_file, "w")
dbase.close()

database = "lab_database"
initialize_database (database)
			
experiment.run()

#####################################################################

#read, execute and update log for each step of the experiment procedure

with open(read_file, "r") as fdata:
    for line in fdata:
        if (line[0:7] != 'execute'):
            if(line[0:6] == 'Update'):
            	update_database(line, diff_file, new_dbase)
            else :
                print(line)
                with open (log.name, "a") as log:
                        log.write(line)
                        log.close()

        else:
            if(line[10:14] != 'Read'):
                print(line + '\n')
                user_input = raw_input("Comments, if any : (Press Enter to continue, type 'pause' to pause or 'end' to abort) : ")
                temp = experiment.time_in_ist('%H:%M:%S')
                
                if (user_input == "end"):
                    string = abort_execution(experiment, log, temp)
                    put_in_folder(experiment, log.name, diff_file, new_dbase)
                    sys.exit(string)
                
                elif (user_input == "pause"):
                    pause_execution(log, temp)
                    
                else:
                    print temp + '\n'

                time_array.append (experiment.time_in_ist('%H:%M:%S'))
		time_stamp_and_comments(log, line, temp, user_input)

            else:
            	print_states(experiment, log, line, new_dbase)

fdata.close()

put_in_folder(experiment, log.name, diff_file, new_dbase)

#close all open files
