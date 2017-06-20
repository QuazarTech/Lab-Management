from complex_functions import *
from wrapper_functions import *
name = "XLIA_service"

def run (Sample, Sample_Box, sample_description, address):
  #Unplug the XLIA Cable
  unplug_cable("XLIA")
  leave ("XLIA.USB_Cable_Module")
  
  #Unplug the XTCON Cable
  unplug_cable("XTCON")
  
  #Plug XTCON Cable into XLIA
  plug_into("XTCON", "XLIA")
  
  #Plug XLIA Cable into XTCON
  locate("XLIA.USB_Cable_Module")
  plug_into("XLIA", "XTCON")

def unplug_cable(cable):
  locate(cable + ".USB_Cable_Module")
  goto  (cable + ".USB_Cable_Module")
  hold  (cable + ".USB_Cable_Module")
  write ("execute : Unplug" + cable + ".USB_Cable_Module")
  write ("Update_Database Lab_Space,PQMS,"+cable+",USB_Cable_Module,DISCONNECTED")

def plug_into(cable, destination):
  goto  (destination + ".USB_Cable_Module Port")
  write ("execute : Plug the cable into "+ destination +".USB_Cable_Module Port")
  leave (cable + ".USB_Cable_Module")
  write ("Update_Database Lab_Space,PQMS,"+destination+",USB_Cable_Module,CONNECTED")
  
  
