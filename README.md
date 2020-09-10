# COSFiC:
## a Component Optimiser for Simple Filter Circuits

This little Python script helps automate picking the components for elementary RC/RL/LC filter circuits to get as close as possible to the specified cutoff parameter.


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
Simply fire up `python3 cosfic.py` in your terminal and follow the prompts.

The cutoff parameter is requested formatted as follows:
`[w, f] [x]e±[exp]`, where:
- `w` and `f` are the *(exclusive)* switches for **pulsation (ω)** or **frequency (f)** as quantities to specify the value for;
- `x` is the figure for the selected quantity;
- `exp` is the power of 10 by which multiply the figure, with `+` or `-` preposed.