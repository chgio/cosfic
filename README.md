# PyCOSFiC: a Python Component Optimiser for Simple Filter Circuits.

This little script helps automate the picking of components for elementary R-C / R-L filter circuits to get as close as possible to the specified cutoff parameter.

## Dependencies

Just Python. Version 3.6 is required, but for anything other than the f-string formatting style any 3.x version will do too.


## Installation

Simply clone this repo or download the files and install the folder wherever you prefer.


## Usage

##### COMPONENTS
The text files in the `components` folder are dedicated to hosting the lists of available components. Do modify them according to your current availability, just make sure to format them as follows:    
`[value] [magnitude]`, where `value` is the value's figure and `magnitude` is the power of 10 by which multiply the figure:
- `T`: 12
- `G`: 9
- `M`: 6
- `K`: 3
- `-`: 1
- `m`: -3
- `u`: -6
- `n`: -9
- `p`: -12

Not unlike scientific notation.

The `components` files are shipped with a handful of the most common values for both convenience and example.

##### SCRIPT
Simply fire up `Python cosfic.py` in your terminal and follow the prompts.
The cutoff parameter is requested formatted as:
`[f, w] [x]e±[ex]`, where:
- `f` and `w` are the *(exclusive)* switches for **frequency** or **pulsation (ω)** as quantities to specify the value for;
- `x` is the figure for the selected quantity;
- `ex` is the power of 10 by which multiply the figure, with + or - preposed.