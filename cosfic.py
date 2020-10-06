# COSFiC:
# Component Optimiser for Simple Filter Circuits
# ----------------------------------------------
### author:	Giorgio Ciacchella
### 		https://github.com/ciakkig
### created:		Feb 2020
### last updated:	Oct 2020


import math
from quantiphy import Quantity

res_file = "components/resistors.txt"
ind_file = "components/inductors.txt"
cap_file = "components/capacitors.txt"

res_list, ind_list, cap_list = [], [], []

comp_dict = {
	"r": res_list,
	"l": ind_list,
	"c": cap_list
}

fn_dict = {
	"rc": lambda r, c: 1 / (r*c),
	"rl": lambda r, l: r / l,
    "lc": lambda l, c: 1 / math.sqrt(l*c)
}

# handy functions
def to_omega(freq):
	omega = freq * (2 * math.pi)
	return omega

def to_freq(omega):
	freq = omega / (2 * math.pi)
	return freq


def loader(res_file, ind_file, cap_file, res_list, ind_list, cap_list):
	# load the values for resistors, capacitors and inductors
	# from the component files to the respective lists
	with open(res_file) as res:
		for line in res:
			line = line.strip()
			if len(line) != 0:
				res_val = Quantity(line)
				res_list.append(res_val)
	
	with open(cap_file) as cap:
		for line in cap:
			line = line.strip()
			if len(line) != 0:
				cap_val = Quantity(line)
				cap_list.append(cap_val)
	
	with open(ind_file) as ind:
		for line in ind:
			line = line.strip()
			if len(line) != 0:
				ind_val = Quantity(line)
				ind_list.append(ind_val)
	
	return res_list, cap_list, ind_list


def asker():
	# ask for the circuit's characteristic parameter
	bode = input("input cutoff frequency/omega: [f/w] [value][prefix][unit]: ")
	inputs = bode.split()
	if len(inputs) == 2:
		fw_flag, val = inputs
		val_bode = Quantity(val)
	elif len(inputs) == 3:
		fw_flag, val, unit = inputs
		val_bode = Quantity(str(val)+unit)
	elif len(inputs) == 4:
		fw_flag, val, prefix, unit = inputs
		val_bode = Quantity(str(val)+prefix+unit)
	

	# switch the parameter according to the frequency/omega flag
	if fw_flag == "w":
		omega_bode = float(val_bode)
	else:
		omega_bode = to_omega(val_bode)
	print(f"{fw_flag} ok.")

	# ask for the circuit composition
	circuit = input("input circuit type: [RC, RL, LC]: ")
	c1 = circuit.lower()
	circuit = c1.strip()
	print(f"{circuit} ok.")

	return omega_bode, circuit, fw_flag


def selector(res_list, ind_list, cap_list, circuit):
	# select the correct component lists and circuit function
	a, b = circuit
	list_a, list_b = comp_dict[a], comp_dict[b]
	if circuit in fn_dict.keys():
		fn = fn_dict[circuit]
	else:
		fn = fn_dict[circuit[::-1]]

	return list_a, list_b, fn


def optimiser(list_a, list_b, omega_bode, fn):
	# the minimum error is initialised as "infinity" so that
	# any number overwrites it on the first less-than check
	err_min = float("inf")
	omega_best = 0
	combo_best = ()

	# cycle through all the combinations of components
	# keeping track of which returns the closest value
	for a in list_a:
		for b in list_b:
			omega_temp = fn(a, b)
			err = math.fabs(omega_bode - omega_temp)
			if err < err_min:
				err_min = err
				omega_best = omega_temp
				combo_best = (a, b)

	return omega_best, combo_best


def printer(circuit, combo_best, omega_best, omega_bode, fw_flag):
	# pretty print out relevant info about the best combination
	# taking into account the frequency/omega flag specified earlier
	a, b = circuit
	a_val, b_val = combo_best

	if fw_flag == "w":
		err = omega_bode - omega_best
		err_pct = err / omega_bode

		to_print = f"""best combination:\t{a.upper()}={a_val}, {b.upper()}={b_val}
with omega:\t\tω={Quantity(omega_best, "Hz")}
and error:\t\t{Quantity(err, "Hz")} ({err_pct:.2%}) off the input value of {Quantity(omega_bode, "Hz")}"""

	else:
		freq_best = to_freq(omega_best)
		freq_bode = to_freq(omega_bode)
		
		err = freq_bode - freq_best
		err_pct = err / freq_best

		to_print = f"""best combination:\t{a.upper()}={a_val}, {b.upper()}={b_val}
with frequency:\t\tf={Quantity(freq_best, "Hz")}
and error:\t\t{Quantity(err, "Hz")} ({err_pct:.2%}) off the input value of {Quantity(freq_bode, "Hz")}"""

	print(to_print)



# load the files, ask for input, select the correct quantities, run the optimiser and print the result
res_list, cap_list, ind_list = loader(res_file, ind_file, cap_file, res_list, ind_list, cap_list)
omega_bode, circuit, fw_flag = asker()
list_a, list_b, fn = selector(res_list, ind_list, cap_list, circuit)
omega_best, combo_best = optimiser(list_a, list_b, omega_bode, fn)
printer(circuit, combo_best, omega_best, omega_bode, fw_flag)