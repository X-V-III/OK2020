from algorithms import greedy,dynamic,bruteforce,genetic
import random
from generator import randomArray
import numpy as np
import matplotlib.pyplot as plt
from time import time



def plot_polynominal(x, y, clr):
	coefficients = np.polyfit(x, y, 3)
	poly = np.poly1d(coefficients)
	new_x = np.linspace(x[0], x[-1])
	new_y = poly(new_x)
	plt.plot(new_x, new_y, clr)

def measure_time(method, v, w, W):
	start = time()
	method(v, w, W)
	elapsed = time() - start
	return elapsed

def measure_efficiency(method, v, w, W):
	temp = [0 for i in range(1)]
	x = method(v, w, W)
	res = get_number(w, x)
	return res

def get_number(v, x):
	n = len(v)
	out = 0
	for i in range(n):
		if (x[i]):
			out += v[i]
	return out

if __name__ == '__main__':
	N = 2
	UPPER_BOUND = 1000
	TIMES = 10
	n = N
	W = 1000
	x = [i for i in range(N,(TIMES+1)*N,N)]

	dyn = []
	gr = []
	br = []
	gen = []
	for i in range(TIMES):
		v = randomArray(UPPER_BOUND, n)
		w = randomArray(UPPER_BOUND, n)

		#dyn.append(measure_time(dynamic, v, w, W))
		#gr.append(measure_time(greedy, v, w, W))
		#br.append(measure_time(bruteforce, v, w, W))
		#gen.append(measure_time(genetic, v, w, W))

		dyn.append(measure_efficiency(dynamic, v, w, W))
		#gr.append(measure_efficiency(greedy, v, w, W))
		#br.append(measure_efficiency(bruteforce, v, w, W))
		gen.append(measure_efficiency(genetic, v, w, W))

		n += N
	'''
	dyngr = [0 for i in range(TIMES)]
	for i in range(TIMES):
		dyngr[i] = dyn[i]/gr[i]
	plt.plot(x, dyngr, "r", label="dynamic/greedy")
	'''
	'''dynbr = [0 for i in range(TIMES)]
	for i in range(TIMES):
		dynbr[i] = dyn[i]/br[i]
	plt.plot(x, dynbr, "r", label="dynamic/greedy")'''

	dyngen = [0 for i in range(TIMES)]
	for i in range(TIMES):
		if (gen[i] == 0): dyngen[i] = dyngen[i-1]
		else: dyngen[i] = dyn[i]/gen[i]
	plt.plot(x, dyngen, "r", label="dynamic/genetic")
	
	#plt.plot(x, gr, "ro", label="greedy")
	#plot_polynominal(x, gr, "r")
	#plt.plot(x, dyn, "go", label="dynamic")
	#plot_polynominal(x, dyn, "g")
	#plt.plot(x, gen, "bo", label="genetic")
	#plot_polynominal(x, gen, "b")
	
	#plt.plot(x, br, "b", label="brute-force")
	
	plt.legend()

	plt.xlabel("Number of items")
	plt.ylabel("Result")
	#plt.ylabel("Elapsed time [s]")
	plt.show()