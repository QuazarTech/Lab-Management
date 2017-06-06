import time
import os


filename = "work_list_"+str(time.strftime('%D'))+".txt"
dirname = os.path.dirname(filename)
if not os.path.exists(dirname):
    os.makedirs(dirname)

programs = raw_input("What programs to be written, comma separated:")
program_array = programs.split(",")

functions = raw_input("Functions to be executed, in order, comma separated:")
functions_array = functions.split(",")

f = open(filename, 'w+')
f.write ("Programs to write:\n")

for i in range(len(program_array)):
  f.write (str(i+1) + "." + program_array[i] + "\n")
  
f.write("\n")
f.write ("Functions to execute:\n")

for i in range(len(functions_array)):
  f.write (str(i+1) + "." + functions_array[i] + "\n")
f.close()
