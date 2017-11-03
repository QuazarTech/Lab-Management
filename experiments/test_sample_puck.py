from complex_functions import *
from wrapper_functions import *

name = "test_sample_puck"

def run():

    ##########################################
    # Set up Sample Puck

    move ("Sample_Puck", "Puck_Board")
    align ("Sample_Puck_Connector", "Puck_Board_Connector")
    write ("execute : Insert Sample_Puck_Connector into Puck_Board_Connector")

    #####################
    # Set up Multimeter (specific to Quazar's Multimeter)

    rotate ("Multimeter knob", "Continuity mode", "Anticlockwise")
    press ("Yellow button")
    touch ("Multimeter_Positive_Probe", "Multimeter_Negative_Probe")
    wait ("Multimeter", "beeping")

    ##########################################
    # Check I+ Terminal connection

    touch ("Multimeter_Positive_Probe", "Sample_Puck Terminal_1")
    touch ("Multimeter_Negative_Probe", "Puck_Board Terminal_I+")
    wait ("Multimeter", "beeping")

    #####################
    # Check V+ Terminal connection

    touch ("Multimeter_Positive_Probe", "Sample_Puck Terminal_2")
    touch ("Multimeter_Negative_Probe", "Puck_Board Terminal_V+")
    wait ("Multimeter", "beeping")

    #####################
    # Check V- Terminal connection

    touch ("Multimeter_Positive_Probe", "Sample_Puck Terminal_3")
    touch ("Multimeter_Negative_Probe", "Puck_Board Terminal_V-")
    wait ("Multimeter", "beeping")

    #####################
    # Check I- Terminal connection

    touch ("Multimeter_Positive_Probe", "Sample_Puck Terminal_4")
    touch ("Multimeter_Negative_Probe", "Puck_Board Terminal_I-")
    wait ("Multimeter", "beeping")

    ##########################################
    # Check that copper block body is not shorted to the terminals

    touch ("Multimeter_Positive_Probe", "Sample_Puck Copper_Block")
    touch ("Multimeter_Negative_Probe", "Puck_Board Terminal_I+")
    check ("Multimeter", "not beeping")

    touch ("Multimeter_Positive_Probe", "Sample_Puck Copper_Block")
    touch ("Multimeter_Negative_Probe", "Puck_Board Terminal_V+")
    check ("Multimeter", "not beeping")

    touch ("Multimeter_Positive_Probe", "Sample_Puck Copper_Block")
    touch ("Multimeter_Negative_Probe", "Puck_Board Terminal_V-")
    check ("Multimeter", "not beeping")

    touch ("Multimeter_Positive_Probe", "Sample_Puck Copper_Block")
    touch ("Multimeter_Negative_Probe", "Puck_Board Terminal_I-")
    check ("Multimeter", "not beeping")

    ##########################################
