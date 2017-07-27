# FreeCAD Models
CAD models of all equipment/tools in the lab will be made using python scripts that run with FreeCAD. All these models together make up the entire labspace, over which the procedure for an experiment can be simulated (dry run), before performing the actual experiment.
The dry run of an experiment will give visual instructions to the person performing the experiment.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

FreeCAD latest version
Follow the instructions given on the following link to get a local copy of FreeCAD running on your computer.
https://www.freecadweb.org/wiki/CompileOnUnix

In particular,

- Get Source Code :

From the terminal, navigate to a desired directory and type
`git clone https://github.com/FreeCAD/FreeCAD.git free-cad-code`

This will place the source code in a folder called free-cad-code.

- Get Dependencies :

To get all the required depenencies, just copy the following line and paste it in your terminal.

`sudo apt install build-essential cmake python python-matplotlib libtool libcoin80-dev libsoqt4-dev libxerces-c-dev libboost-dev libboost-filesystem-dev libboost-regex-dev libboost-program-options-dev libboost-signals-dev libboost-thread-dev libboost-python-dev libqt4-dev libqt4-opengl-dev qt4-dev-tools python-dev python-pyside pyside-tools libeigen3-dev libqtwebkit-dev libshiboken-dev libpyside-dev libode-dev swig libzipios++-dev libfreetype6 libfreetype6-dev liboce-foundation-dev liboce-modeling-dev liboce-ocaf-dev liboce-visualization-dev liboce-ocaf-lite-dev libsimage-dev checkinstall python-pivy python-qt4 doxygen libspnav-dev oce-draw liboce-foundation-dev liboce-foundation10 liboce-foundation8 liboce-modeling-dev liboce-modeling10 liboce-modeling8 liboce-ocaf-dev liboce-ocaf-lite-dev liboce-ocaf-lite10 liboce-ocaf-lite8 liboce-ocaf10 liboce-ocaf8 liboce-visualization-dev liboce-visualization10 liboce-visualization8 libmedc-dev libvtk6-dev libproj-dev`

Note : Follow the additional instructions for Ubuntu 16.04 users given in the following link

https://forum.freecadweb.org/viewtopic.php?f=4&t=16292

In particular, do the following

`sudo apt-get install libmedc-dev`
`sudo apt-get install libvtk6-dev`
`sudo apt-get install libproj-dev`

`sudo ln -s /usr/lib/x86_64-linux-gnu/libfreeimage.so.3 /usr/lib/libfreeimage.so`

- Building FreeCAD

Navigate to the folder where you cloned freecad :
`cd free-cad-code`

Now type
`make`

This will take some time (~3 hours). Make sure no errors are thrown up during the build.

### Installing

Now go to a desired directory in your terminal, where you want to store the Lab-Management code

Clone the Lab-Management repo.
`git clone https://github.com/gitansh95/Lab-Management.git Lab-Management`

This will download all the source code for Lab-Management in the folder called Lab-Management.

Now in the terminal navigate to the freecad_models directory
`cd Lab-Management/freecad_models`

Run the FreeCAD application by typing
`./relative_path_of_directory_where_you_cloned_the_freecad_code/free-cad-code/bin/FreeCAD`

Once inside FreeCAD, enable the python console by making sure that `View -> Panels -> Python Console` is checked.
The Python Console should show up at the bottom of the screen.

In the Python Console, type
`execfile('core.py')`

This should launch the python script that generates the FreeCAD model for the core used in the Electromagnetic coupling experiment.

If you want to save the model that has been generated, press `Ctrl + s`, and type in appropriate file name.
