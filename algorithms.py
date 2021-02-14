from itertools import combinations
import random

# If true, extra inforamtion will appear
DEBUG = False

# O(n*log(n))
def greedy(v, w, W):
	n = len(w)
	profit = [(0, i) for i in range(n)]
	x = [False for i in range(n)]
	for i in range(n):
		profit[i] = (v[i]/w[i],i)
	profit.sort(key = lambda profit: profit[0], reverse = True)
	for e in profit:
		if (w[e[1]] > W): return x
		x[e[1]] = True
		W = W - w[e[1]]
	return x

# O(nW), 
def dynamic(v, w, W): 
	n = len(v)
	K = [[0 for i in range(W + 1)] for j in range(n + 1)] 
	for i in range(n + 1): 
		for j in range(W + 1): 
			if i == 0 or j == 0: 
				K[i][j] = 0
			elif w[i-1] <= j: 
				K[i][j] = max(v[i-1] + K[i-1][j-w[i-1]],  K[i-1][j]) 
			else: 
				K[i][j] = K[i-1][j] 

	i, j = n, W
	x = [False for i in range(n)]
	while i > 0 and j > 0:
		if (K[i][j] == K[i-1][j]):
			i -= 1
		else:
			x[i-1] = True
			j -= w[i-1]
			i -= 1
	return x

#O(2^n)
def bruteforce(v, w, W):
	n = len(v)
	x = []
	max_value = 0
	tuples = list(zip(w, v))
	for number_of_items in range(n):
		for combination in combinations(tuples, number_of_items+1):
			weight = sum([tup[0] for tup in combination])
			value = sum([tup[1] for tup in combination])
			if (max_value < value and weight <= W):
				max_value = value
				x = [False for i in range(n)]
				for tup in combination:
					x[tuples.index(tup)] = True
	return x

#O(n)
def genetic(v, w, W, POP_SIZE=10, MAX_GEN=200):

	N = len(v)
	PARENTS_PERCENTAGE = 0.4
	MUTATION_CHANCE = 0.2
	PARENT_CHANCE = 0.1

	def fitness(perm):
		value = 0
		weight = 0
		index = 0
		for i in perm:        
			if index >= N:
				break
			if (i == 1):
				value += v[index]
				weight += w[index]
			index += 1
			
		if weight > W: return 0
		else: return value

	def generate_population(number_of_individuals):
		return [[random.randint(0,1) for x in range (0,N)] for x in range (0,number_of_individuals)]

	def mutate(perm):
		r = random.randint(0,len(perm)-1)
		if (perm[r] == 1): perm[r] = 0
		else: perm[r] = 1

	def evolve(perm):
		parents_length = int(PARENTS_PERCENTAGE*len(perm))
		parents = perm[:parents_length]
		nonparents = perm[parents_length:]

		for np in nonparents:
			if PARENT_CHANCE > random.random():
				parents.append(np)

		for p in parents:
			if MUTATION_CHANCE > random.random():
				mutate(p)

		children = []
		desired_length = len(perm) - len(parents)
		while len(children) < desired_length :
			m = perm[random.randint(0,len(parents)-1)]
			f = perm[random.randint(0,len(parents)-1)]        
			half = round(len(m)/2)
			child = m[:half] + f[half:]
			if MUTATION_CHANCE > random.random():
				mutate(child)
			children.append(child)

		parents.extend(children)
		return parents

	generation = 1
	population = generate_population(POP_SIZE)
	for g in range(0,MAX_GEN):
		if DEBUG: print (f"Generation {generation} with {len(population)}")
		population = sorted(population, key=lambda x: fitness(x), reverse=True)
		if DEBUG:
			for i in population:        
				print(f"{i}, fit: {fitness(i) }")
		population = evolve(population)
		generation += 1
	if (fitness(population[0]) == 0): return [False for i in range(N)]
	else: return population[0]