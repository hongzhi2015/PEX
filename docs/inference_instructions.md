# User Guide

The inference flow (def2spef) takes design layout information (DEF)
and generates an output SPEF using the RC technology information 
stored in the configuration file generated by the calibration flow.

## Feature
* Generate SPEF for a given RC corner (configuration file) and a Liberty file

## Running the Flow
1. Change the path of these variables to their corresponding directories:
    * DEF_DIR 
    * TECH_LEF_DIR 
    * MACRO_LEF_DIR 
    * CONFIG_FILE_DIR (Select the desired RC corner)
    * LIB_DIR

2. In the terminal: make inference

## Testcase
[Sample designs](../example/) and a generic open-source, standard-cell
library are available to the user for testing the flow.  
  
To run the flow, In the terminal: 
```
make inference
```
  
The output of the flow can be found in the output directory by the name of <design_name>.spef.
