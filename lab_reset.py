import yaml
import os
from pytz import timezone
import datetime
import time

time_zone = timezone("Asia/Kolkata")

def time_in_ist(param):
    now_utc   = datetime.datetime.now(timezone("UTC"))
    now_india = now_utc.astimezone(time_zone)
    return now_india.strftime(param)

def lab_reset(folder_name):

	with open(folder_name+"/run_data_new_database.yaml", "r") as f:
    		new_data      = yaml.load(f)
    		with open("lab_database.yaml", "r") as fo:
        		original_data = yaml.load(fo)
    		fo.close()
	f.close()
	database_original = []
	new_database      = []
	get_differences(new_data, new_database)
	get_differences(original_data, database_original)

	print "The difference between the new and old databases are"
	print "#####################################################\n"
	print list(set(new_database) - set(database_original))
	print "#####################################################\n"


def get_differences(d, val_array):
    for k,v in d.items():
            try:
                get_differences(v , val_array)
            except AttributeError:
                val_array.append(k + "," + str(v))

def put_in_folder (experiment, log, diff_file, new_dbase):        
	t = time_in_ist('%Y_%m_%d_%H:%M:%S')
	folder_name = "run_data_" + experiment.name + "_" + t
	os.system("mkdir " + folder_name)
	os.system("mv " + log + " " + folder_name + "/")
	os.system("mv " + diff_file + " " + folder_name + "/")
	os.system("mv " + new_dbase + ".yaml " + folder_name + "/")
	lab_reset(folder_name)

def put_in_folder_aborted (log, diff_file, new_dbase):        
	t = time_in_ist('%Y_%m_%d_%H:%M:%S')
	folder_name = "run_data_aborted_run"  + "_" + t
	os.system("mkdir " + folder_name)
	os.system("mv " + log.name + " " + folder_name + "/")
	os.system("mv " + diff_file + " " + folder_name + "/")
	os.system("mv " + new_dbase + ".yaml " + folder_name + "/")
	lab_reset(folder_name)
