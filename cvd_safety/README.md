## Alert System for use with CVD Systems

The code in this module implements a QDA (Quazar Data Acquisition System) based approach to detect malfunction in the CVD (Chemical Vapour Deposition) setup.

The following parameters are monitored :
    1. Smoke Concentration
    2. LPG Concentration
    3. Methane Concentration
    4. Hydrogen Concentration
    5. Temperature outside the CVD furnace

## Hardware Setup

- QDAL414B (Qty : 1)
- MQ-2 Gas Sensors (Qty : 2)
- PT100 Temperature Sensors (Qty : 2)

The MQ-2 are interfaced to Channel-1 and Channel-2 of QDAL414B. The PT100 Temperature Sensors are interfaced to Channel-3 and Channel-4.

The QDAL414B is connected to a computer using a USB interface.

## Prerequisites

- Configure ssmtp to send mail from the terminal using your gmail account.
- Install QDAL41xB driver

## Usage

- Compile using `make`. Make sure the QDAL41xB driver is installed before this step.
- Make sure the QDAL414B is connected and powered on.
- Use `./test` to execute the program
