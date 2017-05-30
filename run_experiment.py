import time
from datetime import tzinfo
from datetime import datetime
from pytz import timezone
import datetime
import yaml as yaml
import numpy as np
import sys

import zener_experiment
#import service_log

#####################################################################

experiments = ["service_log", "zener_experiment"]

#create and init and array for timestamps
time_array = []

#####################################################################


def get_sample_info():
    sample_box = raw_input("Which Sample box : (Box_Zener, Box_Resistor)")
    while((sample_box != "Box_Zener") and (sample_box != "Box_Resistor")):
        sample_box = raw_input("Which Sample box : (Box_Zener, Box_Resistor)")

    if(sample_box=="Box_Zener"):
        sample = raw_input("Which sample you want to load : (Zener_1,Zener_2,Zener_3)\n")
        while((sample != "Zener_1") and (sample != "Zener_2") and (sample != "Zener_3")):
            sample = raw_input("Which sample you want to load : (Zener_1,Zener_2,Zener_3)\n")
    elif(sample_box=="Box_Resistor"):
        sample = raw_input("Which sample you want to load : (Res_1,Res_2,Res_3,Res_4,Res_5)\n")
        while((sample != "Res_1") and (sample != "Res_2") and (sample != "Res_3")):
            sample = raw_input("Which sample you want to load : (Res_1,Res_2,Res_3,Res_4,Res_5)\n")
    
    sample_description = raw_input("Give a brief sample desciption:")        
    return sample, sample_box, sample_description


def get_experimental_parameters():
    V_range            = raw_input("Enter Voltage Sweep Range : \n")
    V_step             = raw_input("Enter Voltage Step Size : \n")
    temp_set_point     = raw_input("Enter Heater Setpoint Temperature in Kelvin : \n")

    address            = raw_input("Give the path where you want to store experimental data :")

    return address, temp_set_point, V_range, V_step


def get_experiment():
    print ""
    for item in experiments:
        print item
    experiment = raw_input("\nPlease enter the experiment you want to do:")
    while (experiment not in experiments):
        print "Experiment not in list."
        experiment = raw_input("\nPlease enter the experiment you want to do:")
    return experiment


#####################################################################

#user inputs

Sample, Sample_Box, sample_description = get_sample_info()
    
experiment = eval(get_experiment())
read_file =  experiment.log
address, temperature, V_range, V_step = get_experimental_parameters()
experiment.run(Sample, Sample_Box, V_range, V_step, temperature, sample_description, address)

#user data
robot = raw_input("Enter robot ID : ")
sensor = raw_input("Enter sensor ID: ")
observer = raw_input("Enter observer ID: ")

#create and init log file with user data
log = open (read_file[:-13] + "_execution_log.txt", "w")
log.write("Robot : " + robot + "\n")
log.write("Sensor : " + sensor + "\n")
log.write("Observer : " + observer + "\n")
log.write("Time : " + zener_experiment.time_in_ist() + "\n")
log.close()
time_array.append(zener_experiment.time_in_ist())

diff_file = read_file[:-13] + "_diff.txt"
new_dbase = read_file[:-13] + "new_database"
dbase = open(diff_file + ".txt", "w")
dbase.close()


with open("lab_database.yaml", "r") as f:
    data = yaml.load(f)
    fbase = open(new_dbase + ".yaml", "w")
    yaml.dump(data, fbase, default_flow_style=False)
    fbase.close()
    f.close()
#read, execute and update log for each step of the experiment procedure

with open(read_file, "r") as fdata:
    for line in fdata:
        if (line[0:7] != 'execute'):
            with open(diff_file + ".txt", "a") as dbase:
                dbase.write(line[16:])
                dbase.close()
            fbase = open(new_dbase + ".yaml", "r")
            data = yaml.safe_load(fbase)
            param_array = []
            param_array = line[16:].strip('\n').split(",")
            print param_array
            z = data['Lab_Space']
            for param in param_array[1:(len(param_array) - 2)]:
                z = z[param]
            z[param_array[len(param_array) - 2]] = param_array[len(param_array) - 1]
            fname = open(new_dbase + ".yaml", 'w')
            yaml.dump(data, fname, default_flow_style=False)
            fname.close()
            fbase.close()

        else:
            if(line[10:14] != 'Read'):
                print(line + '\n')
                user_input = raw_input("Comments, if any : (Press Enter to continue, or type end to abort) : ")
                if(user_input == "end"):
                    temp = zener_experiment.time_in_ist()
                    print temp
                    string = "***********" + "\n" + "EXECUTION ABORTED" + "\n" + "***********"
                    with open (log.name, "a") as log:
                        log.write(string + '\n')
                        log.write("Execution has come to an end due to error in line: " + line + '\n')
                    log.close()
                    sys.exit(string)
                else:
                    temp = zener_experiment.time_in_ist()
                    print temp + '\n'

                time_array.append(zener_experiment.time_in_ist())

                with open (log.name, "a") as log:
                    log.write(line + 'end:\t\t\t\t' + temp + '\n\n')
                log.close()
                if(user_input != ""):
                    with open (log.name, "a") as log:
                        log.write("Comment : " + user_input + '\n\n')
                        log.close()

            else:
                print(line + '\n')
                fbase = open(new_dbase + ".yaml", "r")
                data = yaml.safe_load(fbase)
                param_array = []
                param_array = line[25:].strip('\n').split(",")
                z = data["Lab_Space"]
                for param in param_array[1:(len(param_array) - 1)]:
                    z = z[param]
                param = param_array[len(param_array) - 1]
#                dict_base = z[param]
#                for k, v in dict_base.items():
#                    print k,'\n', v
#                    print '\n'
                print yaml.dump(z[param], allow_unicode=True, default_flow_style=False)
                user_input = raw_input("Comments, if any : (Press Enter to continue, or type end to abort) : ")
                if(user_input == "end"):
                    temp = zener_experiment.time_in_ist()
                    print temp
                    string = "***********" + "\n" + "EXECUTION ABORTED" + "\n" + "***********"
                    with open (log.name, "a") as log:
                        log.write(string + '\n')
                        log.write("Execution has come to an end due to error in line: " + line + '\n')
                    log.close()
                    sys.exit(string)
                else:
                    temp = zener_experiment.time_in_ist()
                    print temp + '\n'

                time_array.append(zener_experiment.time_in_ist())

                with open (log.name, "a") as log:
                    log.write(line + 'end:\t\t\t\t' + temp + '\n\n')
                log.close()
                if(user_input != ""):
                      with open (log.name, "a") as log:
                        log.write("Comment : " + user_input + '\n\n')
                        log.close()
fdata.close()
#close all open files