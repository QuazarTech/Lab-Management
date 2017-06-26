# Quazar Lab Management

This repo consists of a lab management software for Sample Characterization with the PQMS. Essentially, the attempt is to simulate the state of the lab, and to track the experiments in the lab computationally.

Our lab (and most labs) consists of two aspects

<ol>
<li>Tools, Equipments and other elements that define the lab space
<li>Experiments that are conducted in that space
</ol>

### Tools, Equipments and other elements

We have documented all the tools, equipments, and other elements of the lab in a yaml database (<b>lab_database.yaml</b>). The database states the item, it's physical/chemical properties and it's current states (on/off, in use/not in use etc). 

The database will also show state changes during an experiment, so that the user can track the progress of the experiment.

### Experiments

<ol>
<li>The back end of the system is the <b>data_logging.py</b>, which interacts with the database. 
<ul>
<li>It uses the <b>write()</b> function which forms the base of the software
<li>The write() function prints a command on the screen, and waits for the user to press 'enter' so that it can proceed to the next command
<li>After each step it logs the time
<li>When it receives the command 'Update_Database (key,value)', it updates the database value of that key
<li>When it receives the command 'Read_States (key, value)', it prints out that key,value'
<li>When it receives the command 'end', it aborts the program
<li>When it receives the command 'pause', it pauses the execution
</ul>
<li>Small steps, like goto, and hold, have been written into functions using write(), and together put into a python script called <b>primitive_ functions.py</b>
<li>Steps that are one level higher use the functions defined the primitive_functions.py to form more complicated functions in the script <b>complex_functions.py</b>. Some examples are load_sample, solder, clamp etceri
<li>These complex functions are further used by <b>wrapper_functions.py</b> to combine them into a logically meanigful sequence, pertenant to the experiment. For eg is_the_sample_loaded() function will first check if sample is already loaded, otherwise it will call load_sample from the complex_functions.py
<li>These wrapper functions are used in the experiment python file to define the complete process
<li>Finally, the <b>run_experiment.py</b> contains the list of experiments, and asks the user which one to execute. This is the file that interacts with the user


The hierarchy of the Lab-Management system is as follows<br><br>

Database  -> Data_logging -> Primitive Functions -> Complex Functions -> Wrapper Functions -> Experiment_File -> Run Experiment
