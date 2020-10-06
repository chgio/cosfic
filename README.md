# COSFiC:
## a Component Optimiser for Simple Filter Circuits

This little Python script helps automate the process of picking the components for elementary RC/RL/LC filter circuits to get as close as possible to the specified cutoff parameter.


## Dependencies

- Python 3.6 -- for anything other than f-string formatting, though, any 3+ version will do;
- [QuantiPhy](https://github.com/KenKundert/quantiphy).

## Installation

Install QuantiPhy with `pip3 install quantiphy`.

Then, clone this repo or download the files and install the folder wherever you fancy.


## Usage

##### COMPONENTS
The text files in the `components` folder are dedicated to hosting the lists of available components.
Do modify them according to your current availability!      
The values are expected in a flexible formatting: in a pinch, just write them down as you're used to doing normally, and you'll most likely be fine.

Here is the full formatting specification:
**`[value]`** `[prefix][unit]`, where:
- **`value`** is the value of the component -- **required;**
- `prefix` is the value's [SI prefix](https://en.wikipedia.org/wiki/Metric_prefix#List_of_SI_prefixes) multiplier:
  - `T` = 10^12,
  - `G` = 10^9,
  - `M` = 10^6,
  - `k` = 10^3,
  - ` ` (none/whitespace) = 1,
  - `m` = 10^-3,
  - `u` = 10^-6,
  - `n` = 10^-9,
  - `p` = 10^-1,;
- `unit` is the value's SI measurement unit:
  - Ohm `Ω` for resistors;
  - Farad `F` for capacitors;
  - Henry `H` for inductors. 

The `components` files are shipped with the 3 most common decades of **[E24](https://en.wikipedia.org/wiki/E_series_of_preferred_numbers)** values for each component.

##### SCRIPT
Simply fire up `python3 cosfic.py` in your terminal and follow the prompts.     
Again, the cutoff parameter is requested in a flexible formatting: just write it down however you prefer.

Here is the full formatting specification:
**`[f/w] [value]`** `[prefix][unit]`, where:
- **`f`** and **`w`** are the switches for **frequency (f)** or **pulsation (ω)** as quantities to specify the value for -- **required,** *mutually exclusive,* and defaulting to **`f`;**
- **`x`** is the value of the selected quantity -- **required;**
- `p` is the value's SI prefix, as mentioned above;
- `u` is the value's SI measurement unit, as mentioned above.