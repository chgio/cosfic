# COSFiC:
# Component Optimiser for Simple Filter Circuits
# ------------------------------------------------
### author:	Giorgio Ciacchella
### 		https://github.com/ciakkig
### created:		Feb 2020
### last updated:	Aug 2020


import math

res_file = "components/resistors.txt"
ind_file = "components/inductors.txt"
cap_file = "components/capacitors.txt"

res_list, ind_list, cap_list = [], [], []

comp_dict = {
	"r": res_list,
	"l": ind_list,
	"c": cap_list
}

mag_dict = {
	"T":	12,
	"G":	9,
	"M":	6,
	"K":	3,
	"-":	0,
	"m":	-3,
	"u":	-6,
	"n":	-9,
	"p":	-12
}

fn_dict = {
	"rc": lambda r, c: 1 / (r*c),
	"rl": lambda r, l: r / l,
    "lc": lambda l, c: 1 / math.sqrt(l*c)
}



def lineprocess(line):
	# split the line and convert the exponent
	f, m = line.split()
	fig, mag = float(f), m
	val =  fig * 10**(mag_dict[mag])

	return val


def loader(res_file, ind_file, cap_file, res_list, ind_list, cap_list):
	# load the values for resistors, capacitors and inductors
	# from the component files to the respective lists
	with open(res_file) as res:
		for line in res:
			line = line.strip()
			if len(line) != 0:
				res_val = lineprocess(line)
				res_list.append(res_val)
	
	with open(cap_file) as cap:
		for line in cap:
			line = line.strip()
			if len(line) != 0:
				cap_val = lineprocess(line)
				cap_list.append(cap_val)
	
	with open(ind_file) as ind:
		for line in ind:
			line = line.strip()
			if len(line) != 0:
				ind_val = lineprocess(line)
				ind_list.append(ind_val)
	
	return res_list, cap_list, ind_list


def asker():
	# ask for the circuit's characteristic parameter
	bode = input("input cutoff pulsation/frequency: [w, f] [x]e±[exp]: ")
	flag, bode_n = bode.split()
	bode_n = float(bode_n)

	# switch the parameter according to the flag
	if flag == "f":
		bode_omega = 2*math.pi*bode_n
	else:
		bode_omega = bode_n
	print(f"{flag} ok.")

	# ask for the circuit composition
	comp = input("input circuit type: [RC, RL, LC]: ")
	c1 = comp.lower()
	circuit = c1.strip()
	print(f"{circuit} ok.")

	return bode_omega, circuit


def selector(res_list, ind_list, cap_list, comp):
	# select the correct component lists and function
	a, b = comp[0], comp[1]
	list_a, list_b = comp_dict[a], comp_dict[b]
	if comp in fn_dict.keys():
		fn = fn_dict[comp]
	else:
		fn = fn_dict[comp[::-1]]

	return list_a, list_b, fn


def optimiser(list_a, list_b, bode_omega, fn):
	# the minimum error is initialised as "infinity" so that
	# any number overwrites it on the first less-than check
	err_min = float("inf")
	omega_best = 0
	comb_best = ()

	# cycle through all the combinations of components
	# keeping track of which returns the closest value
	for a in list_a:
		for b in list_b:
			omega_temp = fn(a, b)
			err = math.fabs(bode_omega - omega_temp)
			if err < err_min:
				err_min = err
				omega_best = omega_temp
				comb_best = (a, b)

	return omega_best, comb_best


def printer(comp, comb_best, omega_best, bode_omega):
	# pretty print out relevant info about the best combination
	a, b = comp[0], comp[1]
	a_val, b_val = comb_best
	err = bode_omega - omega_best
	err_pct = 100 * err / bode_omega

	to_print = f"""best combination:\t{a.upper()}={a_val:.3e}, {b.upper()}={b_val:.3e}
with omega:\t\t{omega_best:.3e}
and error:\t\t{err:.3e} ({err_pct:.2f}%) off the input value of {bode_omega:.3e}"""

	print(to_print)



# load the files, ask for input, select the correct quantities, run the optimiser and print the result
res_list, cap_list, ind_list = loader(res_file, ind_file, cap_file, res_list, ind_list, cap_list)
bode_omega, circuit = asker()
list_a, list_b, fn = selector(res_list, ind_list, cap_list, circuit)
omega_best, comb_best = optimiser(list_a, list_b, bode_omega, fn)
printer(circuit, comb_best, omega_best, bode_omega)