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
G = nx.random_partition_graph([50,30],.7,.2)
adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)

# G = nx.planted_partition_graph(2, 100, 0.5, 0.1,seed=42)
# adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)

# create dict for states and one infected
infectedstates = {}
for n in range(len(adjacencydict)):
	infectedstates.update({n:"S"})

startnode = random.randint(0,len(adjacencydict)) 
infectedstates.update({startnode:"I"})

def flipstateI(node): 
    num = random.randint(0,99)  # random number 0-9
    if num < 4: 
        return True
    return False 


def flipstateR(states):
    num2 = random.randint(0,99)
    if num2 < 5:
        return True
    return False


def flipstateS(states):
    num3 = random.randint(0,99)
    if num3 < 90:
        return True
    return False

reinject = [25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425]
infectedcount_by_iteration = [1]
recoveredcount_by_iteration = [0]
susceptiblecount_by_iteration = [len(infectedstates)]
infectedcount = 1
recoveredcount = 0
susceptiblecount = len(infectedstates) - 1
for i in range(426):
    for node, state in infectedstates.items():
        if state == "I": 
            for key, neighbors in adjacencydict.items():
                if key == node: 
                    for neighbor in neighbors:
                        if infectedstates[neighbor] == "S":
                            if flipstateI(neighbor) is True: 
                                infectedstates[neighbor] = "I"
                                infectedcount += 1 
                                susceptiblecount -= 1
            if flipstateS(node) is True: 
                infectedstates[node] = "S"
                susceptiblecount += 1
                infectedcount -= 1
            elif flipstateR(node) is True:
                infectedstates[node] = "R"
                recoveredcount += 1
                infectedcount -= 1
    for j in range(len(reinject)):
        if i == reinject[j]:
            reinfectedcount = 0
            nums = random.sample(range(0, 199), 10)
            for node1, state1 in infectedstates.items():
                for n in range(10):
                    if node1 == nums[n]:
                        if state1 == "S":
                            infectedstates[node1] = "I"
                            reinfectedcount += 1
                            infectedcount += 1
                            susceptiblecount -= 1
            print(reinfectedcount)

    # print(infectedstates)
    # print(infectedcount)
    # print(recoveredcount)
    infectedcount_by_iteration.append(infectedcount)
    recoveredcount_by_iteration.append(recoveredcount)
    susceptiblecount_by_iteration.append(susceptiblecount)

# print(infectedcount_by_iteration)
# print(recoveredcount_by_iteration)

# # export graph so can be visualized
# outputdir = "/Users/brookeistvan/Documents/Thesis/seniorthesis"
# nx.write_gexf(G, outputdir+"SISRgraph.gexf")

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