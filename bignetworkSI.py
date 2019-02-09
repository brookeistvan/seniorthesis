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


G = nx.random_partition_graph([50,30],.7,.2)
adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)

# make a visual graph to represent the network underlying simulation
# outputdir = "/Users/brookeistvan/Documents/Thesis/seniorthesis"
# nx.write_gexf(G, outputdir+"SIgraph.gexf")

# create dict for states and one infected
infectedstates = {}
for n in range(len(adjacencydict)):
	infectedstates.update({n:"S"})

startnode = random.randint(0,len(adjacencydict)) 
infectedstates.update({startnode:"I"})

# define functions 
def isallinfected(states): 
    for k,v in states.items():
        if v == "S":    # there is still a susceptible ie not all infected 
            return False
    return True  # ie all are I 

def flipstate(node): 
    num = random.randint(0,9)  # random number 0-9
    if num < 2: 
        return True
    return False 

# run simulation 
itercount = 0 
infectedcount_each_smalliter = [1]
susceptiblecount_each_iter = [len(adjacencydict)]
itercount_by_iteration = []
susceptiblecount = len(adjacencydict)
infectedcount = 1
while isallinfected(infectedstates) is not True:
    itercount += 1
    for node, state in infectedstates.items():
        if state == "I": 
            for key, neighbors in adjacencydict.items():
                if key == node: 
                    for neighbor in neighbors:
                        if infectedstates[neighbor] == "S":
                            if flipstate(neighbor) is True: 
                                infectedstates[neighbor] = "I"
                                infectedcount += 1
                                susceptiblecount -= 1
    print(infectedstates)
    print(infectedcount)
    infectedcount_each_smalliter.append(infectedcount)
    susceptiblecount_each_iter.append(susceptiblecount)
itercount_by_iteration.append(itercount)

print(infectedcount_each_smalliter)
print(itercount_by_iteration)


# want number of iterations (x) and the number of infecteds (y)
x = []
for n in range(len(infectedcount_each_smalliter)):
    x.append(n)
plt.plot(x, infectedcount_each_smalliter, label = "infected")
plt.plot(x, susceptiblecount_each_iter, label = "susceptible")
plt.xlabel("iteration")
plt.ylabel("number of infected nodes")
plt.legend()
plt.show()