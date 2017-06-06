from primitive_functions import *

def run(Sample, Sample_Box, sample_description, address):
  remove(Sample_Box+".Cap", Sample_Box)
  leave(Sample_Box)
  hold_sample(Sample,Sample_Box)
  close_lid(Sample_Box)
  leave(Sample)
  move("Polyvinyl_Alcohol", "Puck_Screwing_Coordinates")
  leave("Polyvinyl_Alcohol")
  move("Test_Tube_1", "Puck_Board_Home_Coordinates")
  leave("Test_Tube_1")
  move("Polyvinyl_Alcohol", "Test_Tube_1.Home_Coordinates")
  leave("Polyvinyl_Alcohol")
  goto("Tweezers.Home_Coordinates")
  leave("Tweezers")
  
    
