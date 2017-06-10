import yaml

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
        if((v == type(str)) or (v == type(bool))):
            val_array.append(k + "," + str(v))
        else:
            try:
                get_differences(v , val_array)
            except AttributeError:
                val_array.append(k + "," + str(v))
