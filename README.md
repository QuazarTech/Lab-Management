# Quazar Lab Management

This repo currently consists of a lab management software for Sample Characterization with the PQMS. Essentially, the attempt is to track the state of the lab, and to track the experiments in the lab computationally.

Our lab (and most labs) consists of two aspects

<ol>
<li>Tools, Equipments and other elements that define the lab space
<li>Experiments that are conducted in that space
</ol>

### Tools, Equipments and other elements

We have documented all the tools, equipments, and other elements of the lab in a yaml database (<b>lab_database.yaml</b>). The database states the item, it's physical/chemical properties and it's current states (on/off, in use/not in use etc). 

The database will also show state changes during an experiment, so that the user can track the progress of the experiment.

### Algorithm

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

### Experiments

<ol>
<li>IV
<ul>
<li>Stepped Ramp
<li>Linear Ramp
</ul>
<li>RT
<ul>
<li>Stepped Ramp
<li>Linear Ramp
<li> R-Time Isothermal
</ul>
<li> X-T
<ul>
<li>Stepped Ramp
<li>Linear Ramp
</ul>
</ol>

### Using Quazar Lab Management

To use the Lab Management system, first clone this repo in a directory of your choice

<code>
git clone https://github.com/QuazarTech/Lab-Management.git
</code>

#### Setting up the physical system

You first need to set up your lab. You can skip this step if you are only interested in learning the procedure involved and the changes that will take place in the Lab_Space during the experiment, but if you want to do actual experiments, you will need to also set up a physical system

Replicate the space shown in the below photos
(----insert photos of lab space here-----)

Use the lab_database.yaml to identify the individual elements of the lab space and set them to their rest positions/rest states. <newline>
<i>It is strictly advised not to modify lab_database, unless absolutely needed. The database has been optimized such that all the pre-requisite states needed for performing the experiment have been satisfied. Any modification to that could give errors during execution.</i>

#### Starting Lab-Management
Open a terminal in the cloned directory, and type

<code>
python run_experiment.py
</code>

You will be asked to enter a starting database. Enter lab_database

<code>
Enter the starting database (lab_database, if starting from scratch) :
lab_database
</code>

Then you will be asked to enter the IDs of the robot, sensor and the observer. It's important to understand the what these three signify

<b>Robot</b>
She/He is the one who is doing the experiments. The robot knows nothing of nature of the experiment or expected results. Ideally, the robot shouldn't even know if what she/he is doing is even sensible. The robot only follows instructions. The idea behind this is to ensure that there is repeatability, i.e every time the same procedure is followed 

<b>Sensor</b>
The sensor is the one who checks the activity of the robot. The sensor ensures that the robot is following the procedure that is layed out instead of injecting it's own logic.

<b>Observer</b>
The observer's responsibility is to note down any redudancies/inefficiencies in the process and pass them on so that they can be corrected.

So choose the robot,sensor,observer and enter the names, For eg

<code>

Enter robot ID : 

A

Enter sensor ID:

B

Enter observer ID: 

C

</code>

