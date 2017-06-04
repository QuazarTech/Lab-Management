import yaml

folder_name = raw_input("Enter folder name:")

with open(folder_name+"/run_data_new_database.yaml", "r") as f:
    data = yaml.load(f)
    with open("lab_database.yaml", "r") as fo:
        data_original = yaml.load(fo)
    fo.close()
f.close()

val_array_original = []
val_array_data = []


def get_val_array(d, val_array):
    for k,v in d.items():
        if((v == type(str)) or (v == type(bool))):
            val_array.append(k + "," + str(v))
        else:
            try:
                get_val_array(v , val_array)
            except AttributeError:
                val_array.append(k + "," + str(v))

get_val_array(data, val_array_data)
get_val_array(data_original, val_array_original)

print len(val_array_data), len(val_array_original)
print list(set(val_array_data) - set(val_array_original))
