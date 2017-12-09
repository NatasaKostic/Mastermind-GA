# source of algorithm: https://lirias.kuleuven.be/bitstream/123456789/164803/1/kbi_0806.pdf

import sys
import numpy
import tkinter
import random

P_CROSS_OVER = 0.5
P_INVERT = 0.03
P_MUTATE = 0.03
P_PERMUTE = 0.03
MAX_GEN = 100
MAX_POP = 60
REQ_FIT = 1


def remove_dups(mylist):
	seen = set()
	newlist = []
	for item in mylist:
		t = tuple(item)
		if t not in seen:
			newlist.append(item)
			seen.add(t)
	return newlist


def cross_over(g1,g2, n_peg):
	#if random.random() < P_CROSS_OVER:
	cross_loc = random.randint(1, n_peg-1)
	new_g1 = g1[0:cross_loc] + g2[cross_loc:]
	new_g2 = g2[0:cross_loc] + g1[cross_loc:]
	return([new_g1, new_g2])


def mutate(g1, n_peg, n_col):
	if(random.random() < P_MUTATE):
		loc = random.randint(0, n_peg-1)
		col = random.randint(1, n_col)
		g1[loc] = col
	return(g1)

def get_fitness(prev_guesses, g2, responses, n_peg):
	a = 1
	b = 2
	X_vals = []
	Y_vals = []
	for i in range(len(prev_guesses)):
		g1 = prev_guesses[i][:]

		X_i = responses[i][0]
		Y_i = responses[i][1]
		Xi_g2 = 0
		Yi_g2 = 0

		for i in range(len(g1)):
			if(g2[i] == g1[i]):
				Xi_g2 += 1
				g1[i] = 0
			elif g2[i] in g1:
				Yi_g2 += 1
				idx = g1.index(g2[i])
				g1[idx] = 0

		X_vals.append(abs(Xi_g2 - X_i))
		Y_vals.append(abs(Yi_g2 - Y_i))

	fitness_g2 = a * sum(X_vals) + sum(Y_vals) + b * n_peg * (len(prev_guesses) -1)
	return(fitness_g2)


def GA(n_peg, n_col, prev_guesses, responses):

	print("new GA iter")
# fitne'ss fxn that's inversely proportional to the difference between the solution and the value a decoded chromosome represents


	# initialize the population and remove any duplicates
	population = [[random.randint(1, n_col) for i in range(n_peg)] for j in range(MAX_POP)]
	
	# h = iteration number
	h = 1
	# E = set of eligible/elite codes at iteration h
	E_h = []
	
	while(h <= MAX_GEN and len(E_h) <= MAX_POP):


		# first evaluate the population and take some of the best + some random
		fitness = []
		for indiv in population:
			fitness.append(get_fitness(prev_guesses, indiv, responses, n_peg))

		# the new generation will contain some of the best indivs in this gen + randoms,
		# crossed over offspring of some,
		# mutations of some
		# use fitness values as probabilities to choose best indivs to keep same
		pop_elts = list(range(len(population)))
		probs = [x / sum(fitness) for x in fitness]
		ng = numpy.random.choice(pop_elts, size = int(MAX_POP*(1-P_CROSS_OVER)), replace=False, p = probs)
		
		new_gen = [population[i] for i in ng]
		
		# select parents from previous gen using fitness values as probabilities
		par = numpy.random.choice(pop_elts, size= int(MAX_POP*P_CROSS_OVER-10), replace=False, p = probs)
		# add some random indiv to parental pool promote genetic diversity
		parents = [population[i] for i in par]

		while len(parents) < MAX_POP*P_CROSS_OVER:
			parents.append([random.randint(1, n_col) for i in range(n_peg)])

		random.shuffle(parents)

		children = []
		i = 0
		while i < len(parents):
			child = cross_over(parents[i], parents[i+1], n_peg)
			if random.random() <= P_MUTATE:
				child = [mutate(child[0],n_peg, n_col), mutate(child[1],n_peg, n_col)]
			children.extend(child)
			i += 2

		# add the kids to the new population
		new_gen.extend(children)

		#get fitness of the elements in this new gen
		fitness = []
		for indiv in new_gen:
			fitness.append(get_fitness(prev_guesses,indiv, responses, n_peg))
		print("new gen:" + str(new_gen))
		print("fitness vals:" + str(fitness))
		# add eligible codes to E_h e.g. codes with fitness above a required value
		for f in range(len(fitness)):
			if fitness[f] >= REQ_FIT:
				E_h.append(new_gen[f])

		# remove dups in eligibles
		E_h = remove_dups(E_h)

		population = E_h
		# fill remaining spot with random and remove duplicates again
		while len(population) < MAX_POP:
			population.append([random.randint(1, n_col) for i in range(n_peg)])
			population = remove_dups(population)

	return E_h


def AI_play(guesses, n_col, n_peg, responses):

	print("response:" + str(responses[-1]))

	# # if this is the first guess, generate randomly
	# if response == None:
	# 	# assign an interger to each possible color
	# 	colors = range(1,n_col)
	# 	# play initial random guess
	# 	curr_guess = numpy.random.choice(colors, n_peg)

	# else:
	X_i = responses[-1][0]
	Y_i = responses[-1][1]
	if(X_i != n_peg):
		options = GA(n_peg, n_col, guesses, responses)
		curr_guess = options[1]
	return curr_guess



def person_play(guess, code):
	print("guess used in respose:" + str(guess))
	# X_i = exact number of matches in iteration i (red pegs)
	X_i = 0
	# Y_i = number of partial matches in iteration i (white pegs)
	Y_i = 0
	
	c = code[:]

	#simulate response from person
	j = 0
	for i in range(len(c)):
		if(guess[i] == c[i]):
			X_i += 1
			c[i] = 0
		elif guess[i] in c:
			Y_i += 1
			idx = c.index(guess[i])
			c[idx] = 0

	return [X_i, Y_i]




# method that controls the alternating turns
def play(n_col, n_peg, n_turns):
	
	turn = 0
	response = None
	responses = []
	guess = None
	guesses = []
	while(turn <= n_turns):

		if turn == 0:
			#code = start_game()
			colors = range(1,n_col)
			guess = list(numpy.random.choice(colors, n_peg))
			guesses.append(guess)
			print("AI guess:" + str(guess))

		elif turn % 2 == 0:
			guess = AI_play(guesses, n_col, n_peg, responses)
			print("AI guess:" + str(guess))
			guesses.append(guess)

		else:
			# get real code from gui
			response = person_play(guess, [1,2,2,4])
			responses.append(response)
			# show the response on the GUI

		turn += 1


def main():

	# DEFINITIONS
	# num_colors = the number of color options
	num_colors = int(sys.argv[1])
	# the number of pegs that can be used in a code
	num_pegs = int(sys.argv[2])

	play(num_colors, num_pegs, 4)




if __name__ == "__main__":
	main()
