import time
from datetime import datetime
from pytz import timezone
import datetime
import yaml as yaml
import sys
import os
import zener_experiment
import practice_experiments
#import service_log


#####################################################################

experiments = ["service_log", "zener_experiment", "practice_experiments"]

#create and init and array for timestamps
time_array = []

#####################################################################

#response = raw_input ("Run again? : y/n")
#     while (response != 'n') or (response != 'y'):
#         response = raw_input ("Run again? : y/n")def get_sample_info():

#####################################################################             

def get_sample_info():
    
    sample_box = raw_input("\nSelect Sample box : (Box_Zener, Box_Resistor)\n")
    while((sample_box != "Box_Zener") and (sample_box != "Box_Resistor")):
        sample_box = raw_input("\nSelect Sample box : (Box_Zener, Box_Resistor)\n")

    if(sample_box=="Box_Zener"):
        sample = raw_input("\nSelect sample : (Zener_1, Zener_2, Zener_3)\n")
        while((sample != "Zener_1") and (sample != "Zener_2") and (sample != "Zener_3")):
            sample = raw_input("\nSelect sample : (Zener_1, Zener_2, Zener_3)\n")
    elif(sample_box=="Box_Resistor"):
        sample = raw_input("\nSelect sample : (Res_1,Res_2,Res_3,Res_4,Res_5)\n")
        while((sample != "Res_1") and (sample != "Res_2") and (sample != "Res_3") and (sample != "Res_4") and (sample != "Res_5")):
            sample = raw_input("\nSelect sample : (Res_1,Res_2,Res_3,Res_4,Res_5)\n")
    
    sample_description  = raw_input("\nGive a brief sample desciption: \n")
    address             = raw_input("\nGive the path where you want to store experimental data : \n")
    return address, sample, sample_box, sample_description


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


def abort_execution(experiment, log):
	print temp
        string = "***********" + "\n" + "EXECUTION ABORTED" + "\n" + "***********"
	with open (log.name, "a") as log:
        	log.write(string + '\n')
		log.write("Execution has come to an end due to error in line: " + line + '\n')
	log.close()
	put_in_folder(experiment, log.name, diff_file, new_dbase)
	sys.exit(string)


def pause_execution(log):
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
	

def print_states (experiment, log, line, new_dbase):
	print(line + '\n')
        param_array, data = read_database(new_dbase, 25)
        z = data["Lab_Space"]
        for param in param_array[1:(len(param_array) - 1)]:
            z = z[param]
        param = param_array[len(param_array) - 1]
        print yaml.dump(z[param], allow_unicode=True, default_flow_style=False)
        user_input = raw_input("Comments, if any : (Press Enter to continue, type 'pause' to pause, or 'end' to abort) : ")
        temp = experiment.time_in_ist()
        
        if(user_input == "end"):
            abort_execution(experiment, log)
        
        elif (user_input == "pause"):
            pause_execution(log)
            
        else:
            print temp + '\n'
        
        time_array.append(experiment.time_in_ist())
        time_stamp_and_comments(log, line, temp, user_input)
	


def put_in_folder (experiment, log, diff_file, new_dbase):        
	t = experiment.time_in_ist()
	folder_name = "run_data_" + experiment.name + "_" + t
	os.system("mkdir " + folder_name)
	os.system("mv " + experiment.procedure + " " + folder_name + "/")
	os.system("mv " + log + " " + folder_name + "/")
	os.system("mv " + diff_file + " " + folder_name + "/")
	os.system("mv " + new_dbase + ".yaml " + folder_name + "/")
	create_duration_log (folder_name)

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

def create_duration_log (folder_name):
	f = open(folder_name + "/run_data_procedure.txt", "r")
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
	 	i += 1 
 	fnew.close()
 	f.close()


#####################################################################

#user inputs

address, Sample, Sample_Box, sample_description = get_sample_info()
    
experiment  = eval(get_experiment())
read_file   =  experiment.procedure

experiment.run(Sample, Sample_Box, sample_description, address)

robot, sensor, observer = get_user_data()

#create and init log file with user data
log = open (read_file[:-13] + "execution_log.txt", "w")
log.write("Robot : " + robot + "\n")
log.write("Sensor : " + sensor + "\n")
log.write("Observer : " + observer + "\n")
log.write("Time : " + experiment.time_in_ist() + "\n")
log.close()

time_array.append(experiment.time_in_ist())

diff_file = read_file[:-13] + "diff.txt"
new_dbase = read_file[:-13] + "new_database"
dbase = open(diff_file, "w")
dbase.close()

database = "lab_database"
initialize_database (database)
			
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
                temp = experiment.time_in_ist()
                
                if (user_input == "end"):
                    abort_execution(experiment, log)
                
                elif (user_input == "pause"):
                    pause_execution(log)
                    
                else:
                    print temp + '\n'

                time_array.append (experiment.time_in_ist())
		time_stamp_and_comments(log, line, temp, user_input)

            else:
            	print_states(experiment, log, line, new_dbase)

fdata.close()

put_in_folder(experiment, log.name, diff_file, new_dbase)

#close all open files
