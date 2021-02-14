#	Generating random values for 0-1 knapsack problem
#	upperBound - max weight/value
#	numberOfItems - number of items in generated array

from numpy import random

def randomArray(upperBound, numberOfItems):
	return [random.randint(1,upperBound) for i in range(numberOfItems)]