### COSFiC:
### Component Optimiser for Simple Filter Circuits
# ------------------------------------------------
# by Giorgio Ciacchella (https://github.com/ciakkig)
# created:		Feb 2020
# last updated:	Feb 2020

import math

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
	"rl": lambda r, l: r / l
}

res_name = "components/resistors.txt"
cap_name = "components/capacitors.txt"
ind_name = "components/inductors.txt"

def lineprocess(line):
	l = line.strip()
	f, m = l.split()
	fig, mag = float(f), m
	val =  fig * 10**(mag_dict[mag])
	return val

def loader(res_name, cap_name, ind_name):
	res_list, cap_list, ind_list = [], [], []

	# load the values for resistors, capacitors and inductors
	# from the component files
	with open(res_name) as res:
		for line in res:
			if len(line) != 0:
				res_val = lineprocess(line)
				res_list.append(res_val)
	
	with open(cap_name) as cap:
		for line in cap:
			if len(line) != 0:
				cap_val = lineprocess(line)
				cap_list.append(cap_val)
	
	with open(ind_name) as ind:
		for line in ind:
			if len(line) != 0:
				ind_val = lineprocess(line)
				ind_list.append(ind_val)
	
	return res_list, cap_list, ind_list

def inputter():
	# ask for the circuit's characteristic parameter
	bode = input("input cutoff freq/puls: [f, w] [x]e±[ex] >")
	switch, bode_n = bode.split()
	bode_n = float(bode_n)

	# switch according to the switches
	if switch == "f":
		bode_omega = 2*math.pi*bode_n
	else:
		bode_omega = bode_n
	print(f"{switch} ok.")

	# ask for the circuit type
	circuit = input("input circuit type: [RC, RL] >")
	c1 = circuit.lower()
	comp = c1.strip()
	fn = fn_dict[comp]
	print(f"{comp} ok.")

	return bode_omega, fn

def optimiser(list_a, list_b, bode_omega, fn):
	# the minimum error is initialised as "infinity" so that
	# any number overwrites it on the first less-than check
	err_min = float("inf")
	omega_best = 0
	comb_best = ()

	# cycle through all the combinations of components
	for a in list_a:
		for b in list_b:
			omega_temp = fn(a, b)
			err = math.fabs(bode_omega - omega_temp)
			if err < err_min:
				err_min = err
				omega_best = omega_temp
				comb_best = (a, b)
	return omega_best, comb_best

def printer(comb_best, omega_best, bode_omega):
	# pretty print out relevant info about the combination
	a, b = comb_best
	err = bode_omega - omega_best
	err_pct = 100 * err / bode_omega

	to_print = f"""best combination:\t{a:.3e}, {b:.3e}
with omega:\t\t{omega_best:.3e}
and error:\t\t{err:.3e} ({err_pct:.1f}%) off the input value of {bode_omega:.3e}"""

	print(to_print)

# ------------------------------------------------

res_list, cap_list, ind_list = loader(res_name, cap_name, ind_name)
bode_omega, fn = inputter()
omega_best, comb_best = optimiser(res_list, cap_list, bode_omega, fn)

printer(comb_best, omega_best, bode_omega)