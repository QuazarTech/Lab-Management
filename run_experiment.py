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

#####################################################################

#user inputs

experiment  = eval(get_experiment())

#create and init log file with user data

time_array.append(experiment.time_in_ist('%H:%M:%S'))

experiment.run()

#####################################################################

#put_in_folder(experiment, log.name, diff_file, new_dbase)
