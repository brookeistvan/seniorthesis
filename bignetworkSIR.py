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

# (# groups, # vertices in each group, probability of connecting within group, probability of connecting between groups, seed for random number generator)
G = nx.planted_partition_graph(2, 100, 0.5, 0.1,seed=42)
adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)

# create dict for states and one infected
infectedstates = {}
for n in range(len(adjacencydict)):
	infectedstates.update({n:"S"})

startnode = random.randint(0,len(adjacencydict)) 
infectedstates.update({startnode:"I"})

def flipstate(node): 
    num = random.randint(0,9)  # random number 0-9
    if num < 5: 
        return True
    return False 


def flipstate2(states):
    num2 = random.randint(0,9)
    if num2 < 3:
        return True
    return False

infectedcount_by_iteration = [1]
recoveredcount_by_iteration = [0]
susceptiblecount_by_iteration = [len(infectedstates)]
infectedcount = 1
recoveredcount = 0
susceptiblecount = len(infectedstates) - 1
for i in range(20):
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
            if flipstate2(node) is True:
                infectedstates[node] = "R"
                recoveredcount += 1
                infectedcount -= 1
    # print(infectedstates)
    # print(infectedcount)
    # print(recoveredcount)
    infectedcount_by_iteration.append(infectedcount)
    recoveredcount_by_iteration.append(recoveredcount)
    susceptiblecount_by_iteration.append(susceptiblecount)

# print(infectedcount_by_iteration)
# print(recoveredcount_by_iteration)

# export graph so can be visualized
outputdir = "/Users/brookeistvan/Documents/Thesis/seniorthesis"
nx.write_gexf(G, outputdir+"SIRgraph.gexf")

# want number of iterations (x) and the number of infecteds (y)
x = []
for n in range(len(infectedcount_by_iteration)):
    x.append(n)
plt.plot(x, infectedcount_by_iteration, label="infected")
plt.plot(x, recoveredcount_by_iteration, label="recovered")
plt.plot(x, susceptiblecount_by_iteration, label="susceptible")
plt.xlabel("iteration")
plt.ylabel("number of infected nodes")
plt.legend()
plt.show()