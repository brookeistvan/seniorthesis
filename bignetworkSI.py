import os
import json
from pprint import pprint
import networkx as nx 
import matplotlib.pyplot as plt
import codecs
import time
import datetime
import random
import time
import sys
import io

# Generate the graph overwhich to run simulation, set ([group sizes], P(connecting within group), P(connecting between group)
G = nx.random_partition_graph([70,30],.1,.02)

# Create adjacency dict documenting network connections
adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)

## Make a visualization of above graph - output file can be imported into gephi to see visualization
# outputdir = "/Users/brookeistvan/Documents/Thesis/seniorthesis"
# nx.write_gexf(G, outputdir+"SIgraph.gexf")

# Create dict for states of each node starting as susceptible
infectedstates = {}
for n in range(len(adjacencydict)):
	infectedstates.update({n:"S"})

# Randomly choose one node to start infected 
startnode = random.randint(0,len(adjacencydict)) 
infectedstates.update({startnode:"I"})

# Define functions 
def isallinfected(states): 
    for k,v in states.items():
        if v == "S":    
            return False
    return True  

def flipstate(node): 
    num = random.randint(0,99)  
    # This sets infection probability (Beta): 20 = 20% chance of infection
    if num < 20: 
        return True
    return False 

## Run simulation
# define variables
infectedcount_by_iteration = [1]
susceptiblecount_by_iteration = [len(infectedstates)]
infectedcount = 1
susceptiblecount = len(infectedstates) - 1

# run 50 iterations
for i in range(50):

	# for each infected node
    for node, state in infectedstates.items():
        if state == "I": 
        	# for each neighbor of each infected node
            for key, neighbors in adjacencydict.items():
                if key == node: 
                	# if neighbor is susceptible, flip a weighted coin to see if they become infected
                    for neighbor in neighbors:
                        if infectedstates[neighbor] == "S":
                            if flipstate(neighbor) is True: 
                                infectedstates[neighbor] = "I"
                                infectedcount += 1 
                                susceptiblecount -= 1
    infectedcount_by_iteration.append(infectedcount)
    susceptiblecount_by_iteration.append(susceptiblecount)

# Plot number of iterations (x) and the number of infecteds (y)
x = []
for n in range(len(infectedcount_by_iteration)):
    x.append(n)
plt.plot(x, infectedcount_by_iteration, label="infected", color='r')
plt.plot(x, susceptiblecount_by_iteration, label="susceptible", color='b')
plt.xlabel("iteration")
plt.ylabel("number of infected nodes")
plt.legend()
plt.show()


## Run simulation looking at iterations until 100% infected
## Note this usually works but will ocassionally glitch when one or two nodes fail to get infected (dependent on network)
# itercount = 0 
# infectedcount_each_smalliter = [1]
# susceptiblecount_each_iter = [len(adjacencydict)]
# itercount_by_iteration = []
# susceptiblecount = len(adjacencydict)
# infectedcount = 1
# while isallinfected(infectedstates) is not True:
#     itercount += 1
#     for node, state in infectedstates.items():
#         if state == "I": 
#             for key, neighbors in adjacencydict.items():
#                 if key == node: 
#                     for neighbor in neighbors:
#                         if infectedstates[neighbor] == "S":
#                             if flipstate(neighbor) is True: 
#                                 infectedstates[neighbor] = "I"
#                                 infectedcount += 1
#                                 susceptiblecount -= 1
#     print(infectedcount)
#     infectedcount_each_smalliter.append(infectedcount)
#     susceptiblecount_each_iter.append(susceptiblecount)
# itercount_by_iteration.append(itercount)

# # Plot with number of iterations (x) and the number of infecteds (y)
# x = []
# for n in range(len(infectedcount_each_smalliter)):
#     x.append(n)
# plt.plot(x, infectedcount_each_smalliter, label = "infected")
# plt.plot(x, susceptiblecount_each_iter, label = "susceptible")
# plt.xlabel("iteration")
# plt.ylabel("number of infected nodes")
# plt.legend()
# plt.show()


