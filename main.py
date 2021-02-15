from generator import randomArray
from time import time
from algorithms import dynamic,greedy,bruteforce,genetic
import argparse

#method names
BRUTE_FORCE_METHOD = "bruteforce"
DYNAMIC_PROGRAMMING_METHOD = "dynamic"
GREEDY_METHOD = "greedy"
GENETIC_METHOD = "genetic"

def printl(list):
	for i in list:
		print(i)

def get_input_from_file(input_file_path):
	with open(input_file_path, "r") as file:
		content = file.read().strip()
		lines = content.split('\n')
		W = int(lines[0])
		w = [int(i) for i in lines[1].split()]
		v = [int(i) for i in lines[2].split()]
	if len(w) == len(v):
		return W, w, v
	else:
		raise Exception("Wrong file format")

def run_script(algorithm, v, w, W, POP_SIZE = 10, MAX_GEN = 20):
	start = time()
	if algorithm == genetic:
		result = algorithm(v, w, W, POP_SIZE, MAX_GEN)
	else:
		result = algorithm(v, w, W)
	elapsed = time() - start
	return result, elapsed


if __name__ == "__main__":

	#cmd script arguments parser
	parser = argparse.ArgumentParser(description='Program for solving discrete knapsack program using different algorithms')
	parser.add_argument('-f',
						type=str,
						dest="input_file_path",
						default="in.txt",
						help='Path to input .txt file. Default: ./in.txt')
	parser.add_argument("-m",
						required=True,
						type=str,
						dest="algorithm",
						choices=[BRUTE_FORCE_METHOD, GREEDY_METHOD, DYNAMIC_PROGRAMMING_METHOD, GENETIC_METHOD],
						help="Solving algorithm.")
	parser.add_argument("-r",
						action="store_true",
						dest="random",
						help="Start with random values.")
	parser.add_argument('--upper-bound',
						type=int,
						dest="upper_bound",
						default=100,
						help='Max value or weight for random generation. Default: 100')
	parser.add_argument('-n',
						type=int,
						dest="number_of_items",
						default=10,
						help='Number of items for random generation. Default: 10')
	parser.add_argument('--capacity',
						type=int,
						dest="capacity",
						default=10,
						help='Capacity for random generation. Default: 10')	
	parser.add_argument('--pop-size',
						type=int,
						dest="pop_size",
						default=10,
						help='Population size for genetic algorithm. Default: 10')
	parser.add_argument('--max-gen',
						type=int,
						dest="max_gen",
						default=20,
						help='Max number of generations for genetic algorithm. Default: 20')
	args = parser.parse_args()

	if not args.random:
		W, w, v = get_input_from_file(args.input_file_path)
	else:
		v = randomArray(args.upper_bound, args.number_of_items)
		w = randomArray(args.upper_bound, args.number_of_items)
		W = args.capacity

	if args.algorithm == BRUTE_FORCE_METHOD:
		result, elapsed = run_script(bruteforce, v, w, W)
	elif args.algorithm == DYNAMIC_PROGRAMMING_METHOD:
		result, elapsed = run_script(dynamic, v, w, W)
	elif args.algorithm == GREEDY_METHOD:
		result, elapsed = run_script(greedy, v, w, W)
	elif args.algorithm == GENETIC_METHOD:
		result, elapsed = run_script(genetic, v, w, W, args.pop_size, args.max_gen)
	else:
		raise Exception("No such method")

	result_numbers = []
	best_value = 0
	for i in range(len(result)):
		if result[i]:
			result_numbers.append(i+1)
			best_value += v[i]

	print("Knapsack data:")
	print(f"\tCapacity = {W}")
	print(f"\tWeights = {w}") if len(w) < 16 else print(f"\tWeights = {w[0:16]}...")
	print(f"\tValues = {v}") if len(v) < 16 else print(f"\tValues = {v[0:16]}...")
	print(f"Picked elements: {result_numbers}") if len(result_numbers) < 16 else print(f"Picked elements: {result_numbers[0:16]}...")
	print(f"Best value: {best_value}")
	print(f"Elapsed: {elapsed}[ms]")
